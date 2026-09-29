Name:           omakade
Version:        1.12.0
Release:        1%{?dist}
Summary:        Local game library and launcher for Omarchy desktops
License:        GPL-3.0-or-later
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
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
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
%cmake -G Ninja -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_datadir}/licenses/omakade/LICENSE %{buildroot}%{_datadir}/licenses/omakade/COPYRIGHT

%files
%license LICENSE COPYRIGHT
%{_bindir}/omakade
%{_bindir}/omakade-sessiond
%{_libdir}/systemd/user/omakade-sessiond.service
%{_datadir}/omakade
%{_datadir}/applications/io.github.tsouth89.Omakade.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.tsouth89.Omakade.svg
%{_datadir}/metainfo/io.github.tsouth89.Omakade.metainfo.xml
%{_datadir}/licenses/omakade/ARTWORK.md
%{_datadir}/licenses/omakade/GENERATION.json
%{_datadir}/doc/omakade

%changelog
* Mon Sep 28 2026 kamm3r - 1.12.0-1
- Port the upstream Omarchy game library to Fedora.
