%global debug_package %{nil}

Name:           signed
Version:        0.1.1
Release:        1%{?dist}
Summary:        Sign PDFs and place text and dates on their pages
License:        MIT
URL:            https://github.com/omacom/signed
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  pkgconfig(poppler-qt6)
BuildRequires:  pkgconfig(libqpdf)
BuildRequires:  google-noto-sans-fonts
BuildRequires:  desktop-file-utils
Requires:       google-noto-sans-fonts
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme

%description
Signed is a Qt Quick application for placing signature images, text, and dates
on PDF pages and saving a signed copy while preserving the original document.

%prep
%autosetup

%build
./bin/build

%check
./bin/test
desktop-file-validate pkgbuild/signed.desktop

%install
install -D -m 0755 build/signed %{buildroot}%{_bindir}/signed
install -D -m 0644 pkgbuild/signed.desktop %{buildroot}%{_datadir}/applications/signed.desktop
install -D -m 0644 pkgbuild/signed.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/signed.svg

%files
%license LICENSE
%doc README.md
%{_bindir}/signed
%{_datadir}/applications/signed.desktop
%{_datadir}/icons/hicolor/scalable/apps/signed.svg

%changelog
* Wed Oct 14 2026 kamm3r - 0.1.1-1
- Update to the release pinned in upstream 430bdd13.

* Tue Oct 13 2026 kamm3r - 0.1.0-1
- Port the upstream PDF signing application to Fedora, including its offscreen tests.
