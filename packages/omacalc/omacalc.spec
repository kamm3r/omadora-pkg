%global debug_package %{nil}
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867

Name:           omacalc
Version:        0.2.2
Release:        1%{?dist}
Summary:        Simple calculator built with Qt Quick
License:        MIT AND OFL-1.1
URL:            https://github.com/omacom-io/omacalc
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omacalc/omacalc.desktop
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omacalc/omacalc.svg
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
Requires:       qt6-qtdeclarative
Requires:       hicolor-icon-theme
Requires:       xdg-desktop-portal

%description
A small desktop calculator with a Qt Quick interface.

%prep
%autosetup

%build
./bin/build

%install
install -D -m 0755 build/omacalc %{buildroot}%{_bindir}/omacalc
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/omacalc.desktop
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omacalc.svg

%files
%license LICENSE
%license fonts/OFL.txt
%{_bindir}/omacalc
%{_datadir}/applications/omacalc.desktop
%{_datadir}/icons/hicolor/scalable/apps/omacalc.svg

%changelog
* Mon Sep 28 2026 kamm3r - 0.2.2-1
- Port the upstream Omarchy calculator recipe to Fedora.
