%global debug_package %{nil}

Name:           omacalc
Version:        0.3.1
Release:        1%{?dist}
Summary:        Simple calculator built with Qt Quick
License:        MIT AND OFL-1.1
URL:            https://github.com/omacom-io/omacalc
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
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
install -D -m 0644 pkgbuild/omacalc.desktop %{buildroot}%{_datadir}/applications/omacalc.desktop
install -D -m 0644 pkgbuild/omacalc.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omacalc.svg

%files
%license LICENSE
%license fonts/OFL.txt
%{_bindir}/omacalc
%{_datadir}/applications/omacalc.desktop
%{_datadir}/icons/hicolor/scalable/apps/omacalc.svg

%changelog
* Thu Oct 15 2026 kamm3r - 0.3.1-1
- Update to the release pinned in upstream d9ebd3f6.

* Mon Sep 28 2026 kamm3r - 0.2.2-1
- Port the upstream Omarchy calculator recipe to Fedora.
