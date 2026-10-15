%global debug_package %{nil}

Name:           omairc
Version:        1.10.3
Release:        1%{?dist}
Summary:        IRC client with a Qt Quick desktop interface and local CLI
License:        MIT AND LGPL-3.0-or-later AND OFL-1.1
URL:            https://github.com/fredimachado/omairc
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qtkeychain-qt6-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       qt6-qtdeclarative
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       xdg-desktop-portal

%description
OmaIRC is an IRC client with multiple networks, encrypted connections,
desktop notifications, and a local command interface. Its colors follow
the Omadora desktop theme.

%prep
%autosetup

%build
qmake6 PREFIX=%{_prefix}
%make_build

%check
# This includes the protocol, credential-store, CLI and offscreen UI suites.
./bin/test
desktop-file-validate data/omairc.desktop

%install
make INSTALL_ROOT=%{buildroot} install

%files
%license %{_licensedir}/%{name}
%{_bindir}/omairc
%{_datadir}/applications/omairc.desktop
%{_datadir}/icons/hicolor/scalable/apps/omairc.svg
%{_datadir}/bash-completion/completions/omairc

%changelog
* Thu Oct 15 2026 kamm3r - 1.10.3-1
- Port the upstream IRC client to Fedora with its protocol and UI tests.
