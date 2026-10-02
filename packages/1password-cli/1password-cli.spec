%global debug_package %{nil}

Name:           1password-cli
Version:        2.39.0
Release:        1%{?dist}
Summary:        1Password command line tool
License:        LicenseRef-1Password
URL:            https://app-updates.agilebits.com/product_history/CLI2
Source0:        https://cache.agilebits.com/dist/1P/op2/pkg/v%{version}/op_linux_amd64_v%{version}.zip#/%{name}-%{version}.zip
ExclusiveArch:  x86_64
Requires(pre):  shadow-utils

%description
1Password command line tool. This package repacks the upstream binary
release, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a zip with the op binary plus its detached signature, not
# a tarball, so there is no top directory to autosetup; it is unpacked with
# unzip. The .sig is only used for the upstream PGP check and is not shipped.
%setup -q -c -T -n %{name}-%{version}
unzip -q "%{SOURCE0}"

%build
:

%install
install -D -m 0755 op %{buildroot}%{_bindir}/op

%pre
getent group onepassword-cli >/dev/null || groupadd -r onepassword-cli

%post
chgrp onepassword-cli %{_bindir}/op
chmod g+s %{_bindir}/op

%postun
if [[ $1 == 0 ]]; then
  groupdel onepassword-cli 2>/dev/null || :
fi

%files
%{_bindir}/op

%changelog
* Thu Oct 01 2026 kamm3r - 2.39.0-1
- Repackage the upstream Omarchy release for Fedora.
