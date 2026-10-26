%global debug_package %{nil}

Name:           omaroll
Version:        1.18.0
Release:        1%{?dist}
Summary:        Image, video, and PDF viewer for Omadora
License:        MIT
URL:            https://github.com/btsouth/omaroll
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel >= 6.8
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
Requires:       qt6-qtimageformats
Requires:       qt6-qtsvg
Requires:       kf6-kimageformats
Requires:       libavif
Requires:       libheif
Requires:       LibRaw
Requires:       hicolor-icon-theme
Requires:       xdg-desktop-portal
Requires:       /usr/bin/ffmpeg
Requires:       ffmpegthumbnailer
Requires:       poppler-utils
Requires:       wl-clipboard
Requires:       xdg-utils

%description
Omaroll browses images, videos, and PDFs with a Qt desktop interface,
thumbnail previews, image editing, and optional companion applications.

%prep
%autosetup

%build
%cmake -G Ninja -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/omaroll
%{_datadir}/applications/io.github.tsouth89.omaroll.desktop
%{_datadir}/metainfo/io.github.tsouth89.omaroll.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/io.github.tsouth89.omaroll.svg
%{_datadir}/omaroll
%{_docdir}/%{name}

%changelog
* Mon Oct 26 2026 kamm3r - 1.18.0-1
- Port the upstream media viewer to Fedora.
