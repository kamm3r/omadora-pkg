%global debug_package %{nil}
# /usr/lib/nordvpn bundles private libraries. Keep those out of the RPM
# dependency namespace; system libraries stay explicitly required below.
%global __provides_exclude_from ^/usr/lib/nordvpn/.*
%global __requires_exclude_from ^/usr/lib/nordvpn/.*

Name:           nordvpn-bin
Version:        5.4.0
Release:        1%{?dist}
Summary:        NordVPN CLI tool for Linux
License:        GPL-3.0-only
URL:            https://nordvpn.com/download/linux/
Source0:        https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/n/nordvpn/nordvpn_%{version}_amd64.deb#/%{name}-%{version}-x86_64.deb
Source1:        https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/n/nordvpn/nordvpn_%{version}_arm64.deb#/%{name}-%{version}-aarch64.deb
ExclusiveArch:  x86_64 aarch64
Provides:       nordvpn = %{version}-%{release}
BuildRequires:  binutils
BuildRequires:  systemd-rpm-macros
Requires:       ca-certificates
Requires:       iptables
Requires:       iproute
Requires:       libidn2
Requires:       libnl3
Requires:       libxslt
Requires:       procps-ng
Requires:       sqlite-libs
Requires:       systemd
Requires:       zlib
Requires(pre):  shadow-utils

%description
NordVPN command line tool for Linux. This package repacks the upstream
Debian release, mirroring the upstream PKGBUILD.

%prep
# Upstream ships Debian packages (data.tar.gz payload), not a tarball,
# so there is no top directory to autosetup; the data payload is unpacked
# with ar+tar.
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64) _deb="%{SOURCE0}" ;;
  aarch64) _deb="%{SOURCE1}" ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
ar p "$_deb" data.tar.gz | tar -xzf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring upstream.
# Point the systemd unit at /usr/bin (Fedora) instead of /usr/sbin
# (Debian) before installing. nordvpn.service is a symlink to /dev/null
# (masked upstream), so only the real unit is edited.
sed -i 's|/usr/sbin/nordvpnd|%{_bindir}/nordvpnd|' usr/lib/systemd/system/nordvpnd.service
cp -a etc usr var %{buildroot}/
# Upstream keeps nordvpnd under /usr/sbin on Debian; Fedora uses /usr/bin.
mv %{buildroot}/usr/sbin/nordvpnd %{buildroot}%{_bindir}/nordvpnd
rmdir %{buildroot}/usr/sbin 2>/dev/null || :
# Debian SysV leftovers are not used on Fedora.
rm -rf %{buildroot}/etc/init.d
chmod 0750 %{buildroot}/var/lib/nordvpn %{buildroot}/var/lib/nordvpn/data
# Group for the daemon, via sysusers.d, mirroring upstream.
install -D -m 0644 /dev/null %{buildroot}%{_sysusersdir}/%{name}.conf
echo 'g nordvpn - -' > %{buildroot}%{_sysusersdir}/%{name}.conf
chmod -R go-w %{buildroot}/usr/share %{buildroot}/usr/lib/nordvpn 2>/dev/null || :

%pre
getent group nordvpn >/dev/null || groupadd -r nordvpn

%files
%{_sysusersdir}/%{name}.conf
%{_bindir}/nordvpn
%{_bindir}/nordvpnd
/usr/lib/nordvpn/
/usr/lib/tmpfiles.d/nordvpn.conf
%{_unitdir}/nordvpn.service
%{_unitdir}/nordvpnd.service
%{_unitdir}/nordvpnd.socket
%{_unitdir}/nordvpnd-killswitch.service
/var/lib/nordvpn
%{_datadir}/applications/nordvpn.desktop
%{_datadir}/bash-completion/completions/nordvpn
%{_datadir}/doc/nordvpn/
%{_datadir}/icons/hicolor/scalable/apps/nordvpn*.svg
%{_datadir}/licenses/nordvpn/
%{_mandir}/man1/nordvpn.1.gz
%{_datadir}/zsh/functions/Completion/Unix/_nordvpn_auto_complete

%changelog
* Thu Oct 01 2026 kamm3r - 5.4.0-1
- Repackage the upstream Omarchy release for Fedora.
