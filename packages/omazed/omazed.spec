Name:           omazed
Version:        2.2.0
Release:        1%{?dist}
Summary:        Sync Zed editor theme with Omarchy
License:        MIT
URL:            https://github.com/aps6/omazed
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       jq
Requires:       perl
Requires:       omarchy

%description
Omazed updates the Zed editor theme when the Omarchy theme changes.

%prep
%autosetup

%build

%install
install -D -m 0755 omazed %{buildroot}%{_bindir}/omazed
install -D -m 0755 omazed-generator.sh %{buildroot}%{_bindir}/omazed-generator.sh
install -D -m 0755 omazed-font.sh %{buildroot}%{_bindir}/omazed-font.sh
install -D -m 0644 omazed-theme.tpl %{buildroot}%{_bindir}/omazed-theme.tpl

%files
%license LICENSE
%doc README.md
%{_bindir}/omazed
%{_bindir}/omazed-generator.sh
%{_bindir}/omazed-font.sh
%{_bindir}/omazed-theme.tpl

%changelog
* Mon Sep 28 2026 kamm3r - 2.2.0-1
- Port the upstream Omarchy recipe to Fedora.
