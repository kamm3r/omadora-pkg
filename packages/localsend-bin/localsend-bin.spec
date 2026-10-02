%global debug_package %{nil}
# Upstream binary carries a build-tree RUNPATH; this is a binary repack so
# the RPATH QA check is skipped (mirrors other binary-only Fedora packs).
%undefine __brp_check_rpaths
# /opt/localsend bundles its own Flutter runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude_from ^/opt/localsend/.*
%global __requires_exclude_from ^/opt/localsend/.*

Name:           localsend-bin
Version:        1.18.2
Release:        1%{?dist}
Summary:        An open source cross-platform alternative to AirDrop
License:        Apache-2.0
URL:            https://github.com/localsend/localsend
Source0:        %{url}/releases/download/v%{version}/LocalSend-%{version}-linux-x86-64.deb#/%{name}-%{version}-x86_64.deb
Source1:        %{url}/releases/download/v%{version}/LocalSend-%{version}-linux-arm-64.deb#/%{name}-%{version}-aarch64.deb
ExclusiveArch:  x86_64 aarch64
Provides:       localsend = %{version}-%{release}
Conflicts:      localsend
BuildRequires:  binutils
BuildRequires:  zstd
Requires:       at-spi2-core
Requires:       cairo
Requires:       fontconfig
Requires:       fuse-libs
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libayatana-appindicator-gtk3
Requires:       libepoxy
Requires:       pango
Requires:       xdg-user-dirs

%description
LocalSend shares files and messages with nearby devices over the local
network. This package repacks the upstream .deb release, mirroring the
upstream PKGBUILD. The from-source Flutter build stays a separate recipe
under the `localsend` name.

%prep
# Upstream ships Debian packages (data.tar.zst payload), not a tarball,
# so there is no top directory to autosetup; the data payload is unpacked
# with ar+tar.
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64) _deb="%{SOURCE0}" ;;
  aarch64) _deb="%{SOURCE1}" ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
ar p "$_deb" data.tar.zst | tar --use-compress-program=unzstd -xf -
# Desktop tweaks, mirroring the upstream PKGBUILD build().
sed -i -E 's|Exec=localsend_app|Exec=localsend|' usr/share/applications/localsend_app.desktop
sed -i -E 's/^Icon=.+/Icon=localsend/' usr/share/applications/localsend_app.desktop
sed -i -E '/^Exec=localsend/a StartupWMClass=org.localsend.localsend_app' usr/share/applications/localsend_app.desktop

%build
:

%install
# Desktop entry, renamed to the shared name, mirroring upstream.
install -D -m 0644 usr/share/applications/localsend_app.desktop %{buildroot}%{_datadir}/applications/localsend.desktop
# Icons, renamed from localsend_app to localsend, mirroring upstream.
cp -a usr/share/icons %{buildroot}%{_datadir}/
find %{buildroot}%{_datadir}/icons -name 'localsend_app.png' -execdir mv {} localsend.png \;
# App tree under /opt, binary renamed to localsend, mirroring upstream.
install -d %{buildroot}/opt/localsend
cp -a opt/localsend_app/. %{buildroot}/opt/localsend/
mv %{buildroot}/opt/localsend/localsend_app %{buildroot}/opt/localsend/localsend
install -d %{buildroot}%{_bindir}
ln -s /opt/localsend/localsend %{buildroot}%{_bindir}/localsend
chmod -R go-w %{buildroot}

%files
/opt/localsend
%{_bindir}/localsend
%{_datadir}/applications/localsend.desktop
%{_datadir}/icons/hicolor/*/apps/localsend.png

%changelog
* Thu Oct 01 2026 kamm3r - 1.18.2-1
- Repackage the upstream Omarchy release for Fedora.
