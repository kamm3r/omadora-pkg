%global source_commit c82d32e3e1adbc6578a148962002ddf6e3e8a15a
%global source_stem cua-hyprland-plugin-%{version}-%{source_commit}
%global source_sha256 79596a9a5e7300546ad4ab0646430edcf3e0c0456a541458de2a52b8c44a8fad
%global kit_filename %{source_stem}-profile-omarchy-edge-20261004-kit-1.3.0-0ada2c227d0817b0228e9d8127e2363a785c13175a9b74fbebaedc9825d3a4fd-%{source_commit}.tar.gz
# Hyprland plugins load into the compositor process and have no stable ABI, so
# the module is built and pinned against exactly this Hyprland version.
%global hyprland_version 0.56.2
# CMakeLists forces -fno-lto on every target; keep Fedora's flags in line.
%global _lto_cflags %{nil}

Name:           cua-hyprland-plugin
Version:        0.33.2
Release:        1%{?dist}
Summary:        Optional Cua background-input plugin for Hyprland
License:        MIT
URL:            https://github.com/trycua/cua
%global omarchy_pkgs_commit e499d021c69d27e0750f77f9af7cd68534c8016f
Source0:        %{url}/releases/download/cua-hyprland-kit-v1.3.0-omarchy-edge-20261004/%{kit_filename}#/%{name}-%{version}-kit.tar.gz
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
%setup -q -c -T -n %{source_stem}
mkdir profile-kit
tar -xzf "%{SOURCE0}" -C profile-kit
echo '%{source_sha256}  profile-kit/%{source_stem}.tar.gz' | sha256sum -c -
tar -xzf profile-kit/%{source_stem}.tar.gz --strip-components=1
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
install -D -m 0644 profile-kit/KIT-PROVENANCE.json \
    %{buildroot}%{_datadir}/%{name}/KIT-PROVENANCE.json

%check
%ctest

%files
%license LICENSE.md
%dir %{_prefix}/lib/cua
%dir %{_prefix}/lib/cua/hyprland
%{_prefix}/lib/cua/hyprland/cua-hyprland-plugin.so
%{_datadir}/%{name}/

%changelog
* Tue Oct 13 2026 kamm3r - 0.33.2-1
- Update to the release pinned in upstream e499d021.
- Verify and extract the native source from the published profile kit.

* Tue Oct 06 2026 kamm3r - 0.32.0-1
- Update to the release pinned on upstream master.
- Apply the rebased downstream patch and retain the Hyprland ABI pin.
- Recommend the separately versioned Driver without equating its release.

* Fri Oct 02 2026 kamm3r - 0.28.2-1
- Build the upstream Omarchy Cua Hyprland plugin for Fedora against Hyprland 0.56.2.
