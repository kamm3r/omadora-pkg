%global debug_package %{nil}
# Bun's compiled executable contains an embedded application bundle.
%global __strip /bin/true

Name:           collie-bin
Version:        1.22.6
Release:        1%{?dist}
Summary:        Phone interface for terminal AI agents over Tailscale
License:        MIT
URL:            https://github.com/AltanS/collie
Source0:        %{url}/releases/download/v%{version}/collie-%{version}-linux-x64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       collie = %{version}-%{release}
Requires:       bash
Requires:       glibc
Recommends:     tailscale
Recommends:     tmux

%description
Collie provides a phone web interface for AI agents running in terminal sessions.
It ships the official compiled executable and its web assets. The user starts
the service and enables phone access with Collie's CLI.

%prep
%autosetup -n collie-%{version}-linux-x64

%build
:

%check
bin/collie --version

%install
# The binary finds its assets relative to the resolved executable's parent tree.
install -d %{buildroot}/opt/collie %{buildroot}%{_bindir}
cp -a . %{buildroot}/opt/collie/
rm -rf %{buildroot}/opt/collie/LICENSE %{buildroot}/opt/collie/README.md \
       %{buildroot}/opt/collie/CHANGELOG.md %{buildroot}/opt/collie/docs
ln -s /opt/collie/bin/collie %{buildroot}%{_bindir}/collie
chmod -R go-w %{buildroot}/opt/collie

%files
%license LICENSE
%doc README.md CHANGELOG.md docs
/opt/collie
%{_bindir}/collie

%changelog
* Mon Oct 19 2026 kamm3r - 1.22.6-1
- Update to the release pinned in upstream de0326b9.

* Sat Oct 17 2026 kamm3r - 1.22.0-1
- Update to the release pinned in upstream 64e8fbc2.

* Thu Oct 15 2026 kamm3r - 1.21.3-1
- Update to the release pinned in upstream d9ebd3f6.

* Tue Oct 13 2026 kamm3r - 1.21.0-1
- Package the official Collie executable and its version-matched web assets.
- Preserve the embedded Bun bundle and leave service setup to the user.
