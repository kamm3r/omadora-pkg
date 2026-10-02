%global debug_package %{nil}
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867

Name:           asdcontrol
Version:        0.6.0
Release:        2%{?dist}
Summary:        Control brightness on Apple Displays connected via USB-C
License:        GPL-2.0-only
URL:            https://github.com/omakasui/asdcontrol
Epoch:          1
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/asdcontrol/asdcontrol.sudoers
ExclusiveArch:  x86_64 aarch64
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
Requires:       glibc

%description
Control brightness on Apple Displays connected via USB-C.

%prep
%autosetup

%build
%make_build

%install
install -D -m 0755 asdcontrol %{buildroot}%{_bindir}/asdcontrol
install -dm 0750 %{buildroot}%{_sysconfdir}/sudoers.d
install -m 0440 %{SOURCE1} %{buildroot}%{_sysconfdir}/sudoers.d/50-asdcontrol

%files
%license LICENSE
%doc README.md
%{_bindir}/asdcontrol
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers.d/50-asdcontrol

%changelog
* Thu Oct 01 2026 kamm3r - 1:0.6.0-2
- Port the upstream Omarchy Apple display brightness tool to Fedora.
