%global _lto_cflags %{nil}
%global _smp_build_ncpus 2
%global omarchy_patches_ref b766e177b0ab827f2154e4b76cf8c7c158d3b86b
Name:           hyprland
Version:        0.57.0
Release:        3.omadora%{?dist}
Summary:        Hyprland compositor with Omarchy monitor and EGL fixes
License:        BSD-3-Clause AND BSD-2-Clause AND HPND-sell-variant AND LGPL-2.1-or-later
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source4:        https://raw.githubusercontent.com/LionHeartP/hyprlandRPM/1a2422834d0db4889a33621556eb094b01aba32b/hyprland-git/macros.hyprland
Patch0:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_patches_ref}/pkgbuilds/hyprland/nvidia-egl-teardown.patch
Patch1:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_patches_ref}/pkgbuilds/hyprland/wl-output-global-grace.patch
Patch2:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_patches_ref}/pkgbuilds/hyprland/monitor-rule-vrr.patch
# This branch artifact is pinned by sources.sha256, including test changes.
Patch3:         https://raw.githubusercontent.com/kamm3r/omadora-pkg/hyprland-testing/packages/hyprland/fedora-regression-tests.patch
ExclusiveArch:  x86_64
BuildRequires:  ninja-build gtest-devel patch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  muParser-devel
BuildRequires:  glaze-static
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glslang)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(hyprcursor)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.8.0
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(libinput) >= 1.29
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)
Provides:       bundled(udis86) = 1.7.2
Provides:       hyprland(omadora-patches) = 20261030
Requires:       xorg-x11-server-Xwayland%{?_isa}
Requires:       aquamarine%{?_isa} >= 0.9.2
Requires:       hyprcursor%{?_isa} >= 0.1.13
Requires:       hyprgraphics%{?_isa} >= 0.1.6
Requires:       hyprlang%{?_isa} >= 0.6.3
Requires:       hyprutils%{?_isa} >= 0.8.4
Recommends:     mesa-dri-drivers
Recommends:     polkit
Recommends:     %{name}-uwsm
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description
Fedora Hyprland compositor carrying Omarchy's NVIDIA EGL teardown,
wl_output global removal grace period and monitor-rule VRR refresh fixes.
This candidate is maintained in an isolated testing repository. Companion
libraries continue to come from the existing Fedora Hyprland provider.

%package uwsm
Summary:        Files for a uwsm-managed Hyprland session
Requires:       uwsm
%description uwsm
Desktop session entry for running Hyprland through uwsm.

%package devel
Summary:        Headers and protocols for the patched Hyprland build
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cpio git-core
Requires:       muParser-devel
Requires:       glaze-static
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(egl)
Requires:       pkgconfig(gbm)
Requires:       pkgconfig(gio-2.0)
Requires:       pkgconfig(glesv2)
Requires:       pkgconfig(glslang)
Requires:       pkgconfig(hwdata)
Requires:       pkgconfig(hyprcursor)
Requires:       pkgconfig(hyprgraphics)
Requires:       pkgconfig(hyprland-protocols) >= 0.8.0
Requires:       pkgconfig(hyprlang)
Requires:       pkgconfig(hyprutils)
Requires:       pkgconfig(hyprwayland-scanner)
Requires:       pkgconfig(hyprwire)
Requires:       pkgconfig(lcms2)
Requires:       pkgconfig(libcanberra)
Requires:       pkgconfig(libdisplay-info)
Requires:       pkgconfig(libdrm)
Requires:       pkgconfig(libeis-1.0)
Requires:       pkgconfig(libinput) >= 1.29
Requires:       pkgconfig(libliftoff)
Requires:       pkgconfig(libseat)
Requires:       pkgconfig(libudev)
Requires:       pkgconfig(lua)
Requires:       pkgconfig(pango)
Requires:       pkgconfig(pangocairo)
Requires:       pkgconfig(pixman-1)
Requires:       pkgconfig(re2)
Requires:       pkgconfig(readline)
Requires:       pkgconfig(sdbus-c++)
Requires:       pkgconfig(systemd)
Requires:       pkgconfig(tomlplusplus)
Requires:       pkgconfig(uuid)
Requires:       pkgconfig(wayland-client)
Requires:       pkgconfig(wayland-protocols) >= 1.49
Requires:       pkgconfig(wayland-scanner)
Requires:       pkgconfig(wayland-server)
Requires:       pkgconfig(xcb-composite)
Requires:       pkgconfig(xcb-dri3)
Requires:       pkgconfig(xcb-errors)
Requires:       pkgconfig(xcb-ewmh)
Requires:       pkgconfig(xcb-icccm)
Requires:       pkgconfig(xcb-present)
Requires:       pkgconfig(xcb-render)
Requires:       pkgconfig(xcb-renderutil)
Requires:       pkgconfig(xcb-res)
Requires:       pkgconfig(xcb-shm)
Requires:       pkgconfig(xcb-util)
Requires:       pkgconfig(xcb-xfixes)
Requires:       pkgconfig(xcb-xinput)
Requires:       pkgconfig(xcb)
Requires:       pkgconfig(xcursor)
Requires:       pkgconfig(xkbcommon)
Requires:       pkgconfig(xwayland)

%description devel
Development files for building plugins against this exact compositor build.

%prep
%autosetup -n hyprland-source -N
# Reject patch drift rather than silently accepting fuzzy application.
for patch in %{PATCH0} %{PATCH1} %{PATCH2} %{PATCH3}; do
    patch --fuzz=0 -p1 -i "$patch"
done
# Fedora's Lua pkg-config name differs from Arch's.
sed -i 's/lua55/lua/g' CMakeLists.txt
cp -p subprojects/udis86/LICENSE LICENSE-udis86
cp %{SOURCE4} macros.hyprland
sed -i 's/@@HYPRLAND_VERSION@@/%{version}/g' macros.hyprland

%build
%cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
install -Dpm644 macros.hyprland -t %{buildroot}%{_rpmconfigdir}/macros.d
install -d %{buildroot}%{_userunitdir}
mv %{buildroot}%{_libdir}/systemd/user/* %{buildroot}%{_userunitdir}/

%check
# Build tests separately so coverage instrumentation never reaches shipped binaries.
%cmake -B build-tests -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DWITH_TESTS=ON
cmake --build build-tests --target hyprland_gtests -j2
build-tests/hyprland_gtests
%{_vpath_builddir}/Hyprland --version

%files
%license LICENSE LICENSE-udis86
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_userunitdir}/hyprland-session.target
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{_datadir}/bash-completion/completions/hypr*
%{_datadir}/fish/vendor_completions.d/hypr*.fish
%{_datadir}/zsh/site-functions/_hypr*

%files uwsm
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop

%files devel
%{_datadir}/pkgconfig/hyprland.pc
%{_includedir}/hyprland/
%{_rpmconfigdir}/macros.d/macros.hyprland

%changelog
* Fri Oct 30 2026 kamm3r - 0.57.0-3.omadora
- Give patched plugin headers and compositor a matching patch-specific ABI tag.
- Use upstream WITH_TESTS switch and run GTests directly in the coverage build.

* Fri Oct 30 2026 kamm3r - 0.57.0-2.omadora
- Adapt Fedora provider integration for a staged Omarchy-patched compositor.
- Apply three unchanged upstream patches and exercise VRR/output regressions.
- Run upstream GTests in a separate coverage build; ship an uninstrumented binary.
