Name:           omakade
Version:        1.16.2
Release:        1%{?dist}
Summary:        Local game library and launcher for Omarchy desktops
License:        GPL-3.0-or-later AND CC-BY-SA-3.0
URL:            https://github.com/btsouth/omakade
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  openssl-devel
BuildRequires:  SDL3-devel
BuildRequires:  libzstd-devel
BuildRequires:  libsecret-devel
BuildRequires:  libzip-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  systemd-rpm-macros
Requires:       python3
Requires:       layer-shell-qt
Recommends:     pulseaudio-utils
Requires:       qt6-qtsvg
Requires:       qt6-qtimageformats
Requires:       qt6-qtwayland
Requires:       hicolor-icon-theme

%description
Omakade is a local game library with a Qt desktop interface, session tracking,
and gamepad support.

%prep
%autosetup

%build
# The only files installed under libdir are architecture-independent user units.
%cmake -G Ninja -DBUILD_TESTING=OFF -DCMAKE_INSTALL_LIBDIR=lib
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_datadir}/licenses/omakade/LICENSE %{buildroot}%{_datadir}/licenses/omakade/COPYRIGHT

%files
%license LICENSE COPYRIGHT
%{_bindir}/omakade
%{_bindir}/omakade-sessiond
%{_bindir}/omakade-guide-button
%{_bindir}/omakade-guide-guard
%{_userunitdir}/omakade-sessiond.service
%{_userunitdir}/omakade-guide-button.service
%dir %{_userunitdir}/graphical-session.target.wants
%{_userunitdir}/graphical-session.target.wants/omakade-sessiond.service
%{_datadir}/omakade
%{_datadir}/applications/io.github.tsouth89.Omakade.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.tsouth89.Omakade.svg
%{_datadir}/metainfo/io.github.tsouth89.Omakade.metainfo.xml
%{_datadir}/licenses/omakade/ARTWORK.md
%{_datadir}/licenses/omakade/GENERATION.json
%{_datadir}/doc/omakade

%changelog
* Tue Oct 13 2026 kamm3r - 1.16.2-1
- Update to the release pinned in upstream e499d021.
- Add the Qt GUI private headers required for controller input.
- Package the new guide guard and install user units in Fedora's systemd directory.

* Tue Oct 06 2026 kamm3r - 1.15.0-1
- Update to the release pinned on upstream master.
- Add the layer-shell and Python dependencies and artwork license.
- Package the new controller guide-button helper and user service.

* Mon Sep 28 2026 kamm3r - 1.12.0-1
- Port the upstream Omarchy game library to Fedora.
