%global source_commit 58aba84b5b83d77e7e2b0f006547699eb594e50d
%global source_stem cua-hyprland-plugin-%{version}-%{source_commit}
# Hyprland plugins load into the compositor process and have no stable ABI, so
# the module is built and pinned against exactly this Hyprland version.
%global hyprland_version 0.56.2
# CMakeLists forces -fno-lto on every target; keep Fedora's flags in line.
%global _lto_cflags %{nil}

Name:           cua-hyprland-plugin
Version:        0.32.0
Release:        1%{?dist}
Summary:        Optional Cua background-input plugin for Hyprland
License:        MIT
URL:            https://github.com/trycua/cua
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        %{url}/releases/download/cua-driver-rs-v%{version}/%{source_stem}.tar.gz#/%{name}-%{version}.tar.gz
# Omarchy's keyboard-remap patch: independent agent keymaps, operation-specific
# foreground checks, and compatible Num Lock state.
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/cua-hyprland-plugin/downstream.patch#/%{name}-downstream.patch
ExclusiveArch:  x86_64
BuildRequires:  binutils
BuildRequires:  cmake >= 3.30
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  patch
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  hyprland-devel = %{hyprland_version}
Requires:       hyprland = %{hyprland_version}
Recommends:     cua-driver-bin

%description
Hyprland plugin that gives Cua Driver background input lanes with their own
canonical US keymap and modifier state, built from the plugin source published
with Cua Driver %{version} plus Omarchy's downstream keyboard-remap patch. It pairs
with Cua Driver over input protocol v3.

The plugin is optional: installation does not load it or enable input. Exit
Hyprland before installing, upgrading, or removing it, then in a fresh session
load it with:

  hyprctl plugin load /usr/lib/cua/hyprland/cua-hyprland-plugin.so

and enable input with the plugin.cua.enabled Hyprland setting. Never hot-unload
and reload the module.

The Arch recipe also pins compiler, glibc and libstdc++ package hashes through
Cua's profile kit and pacman; that verifier does not apply to Fedora, so this
package pins the Hyprland version instead.

%prep
%setup -q -n %{source_stem}
patch -p1 --fuzz=0 <%{SOURCE1}

%build
# Upstream's install rule targets lib/cua/hyprland under the prefix; keep the
# /usr/lib path the upstream package and documentation use on every arch.
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=ON \
    -DCUA_HYPRLAND_BUILD_PLUGIN=ON \
    -DCUA_HYPRLAND_EXPECTED_VERSION=%{hyprland_version} \
    -DCUA_HYPRLAND_INPUT=ON \
    -DCUA_HYPRLAND_TEST_INPUT=OFF \
    -DCUA_HYPRLAND_INPUT_TRACE=OFF \
    -DCUA_HYPRLAND_TEST_OPERATOR_KEY=
%cmake_build

%install
install -D -m 0755 %{__cmake_builddir}/cua-hyprland-plugin.so \
    %{buildroot}%{_prefix}/lib/cua/hyprland/cua-hyprland-plugin.so
install -D -m 0644 SOURCE-PROVENANCE.json \
    %{buildroot}%{_datadir}/%{name}/SOURCE-PROVENANCE.json
install -D -m 0644 %{SOURCE1} \
    %{buildroot}%{_datadir}/%{name}/downstream.patch

%check
%ctest

%files
%license LICENSE.md
%dir %{_prefix}/lib/cua
%dir %{_prefix}/lib/cua/hyprland
%{_prefix}/lib/cua/hyprland/cua-hyprland-plugin.so
%{_datadir}/%{name}/

%changelog
* Tue Oct 06 2026 kamm3r - 0.32.0-1
- Update to the release pinned on upstream master.
- Apply the rebased downstream patch and retain the Hyprland ABI pin.
- Recommend the separately versioned Driver without equating its release.

* Fri Oct 02 2026 kamm3r - 0.28.2-1
- Build the upstream Omarchy Cua Hyprland plugin for Fedora against Hyprland 0.56.2.
