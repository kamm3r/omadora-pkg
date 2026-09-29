%global debug_package %{nil}

Name:           omapresent
Version:        0.1.3
Release:        1%{?dist}
Summary:        Markdown presentation app built with Qt Quick
License:        MIT AND LicenseRef-Omarchy
URL:            https://github.com/jethrojones/omapresent
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtwebengine-devel
BuildRequires:  qt6-qtwebchannel-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  ImageMagick
Requires:       qt6-qtwebengine
Requires:       qt6-qtwebchannel
Requires:       qt6-qtmultimedia
Requires:       xdg-desktop-portal
Requires:       ttf-ia-writer
Requires:       hicolor-icon-theme

%description
Omapresent renders Markdown presentations with a Qt desktop interface.

%prep
%autosetup

%build
./bin/build

%install
install -D -m 0755 build/omapresent %{buildroot}%{_bindir}/omapresent
install -D -m 0644 skill/SKILL.md %{buildroot}%{_datadir}/omapresent/skill/SKILL.md
install -d %{buildroot}%{_datadir}/omapresent/skill/reference
install -m 0644 skill/reference/*.md %{buildroot}%{_datadir}/omapresent/skill/reference/
install -D -m 0755 pkgbuild/omapresent-theme-refresh %{buildroot}%{_datadir}/omapresent/hooks/omapresent-theme-refresh
install -D -m 0644 welcome/welcome.md %{buildroot}%{_datadir}/omapresent/welcome.md
install -D -m 0644 pkgbuild/omapresent.desktop %{buildroot}%{_datadir}/applications/omapresent.desktop
install -d %{buildroot}%{_datadir}/licenses/omapresent/vendor
install -m 0644 src/renderer/vendor/LICENSE* %{buildroot}%{_datadir}/licenses/omapresent/vendor/
for size in 16 22 24 32 48 64 128 256 512; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  magick pkgbuild/omapresent.png -filter Lanczos -resize ${size}x${size} -strip %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/omapresent.png
  chmod 0644 %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/omapresent.png
done

%files
%license LICENSE NOTICE
%{_bindir}/omapresent
%{_datadir}/omapresent
%{_datadir}/applications/omapresent.desktop
%{_datadir}/icons/hicolor/*/apps/omapresent.png
%{_datadir}/licenses/omapresent/vendor

%changelog
* Mon Sep 28 2026 kamm3r - 0.1.3-1
- Port the upstream Omarchy presentation app to Fedora.
