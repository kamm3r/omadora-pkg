%global debug_package %{nil}
# /opt/Perplexity bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           perplexity
Version:        26.9.6+build95799
Release:        1%{?dist}
Summary:        Official Perplexity desktop app
License:        LicenseRef-proprietary
URL:            https://www.perplexity.ai
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
# The pool filename carries a build number the index's Version field drops,
# and upstream rebuilds under the same marketing version. The PKGBUILD
# reconstructs the pool URL from pkgver with a literal '+' encoded as %2B
# (the pool treats a literal '+' as a space and answers 403). RPM Version
# keeps the '+' verbatim; only the URL encodes it.
Source0:        https://packages.perplexity.ai/deb/pool/main/p/perplexity/perplexity_26.9.6%2Bbuild95799_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/perplexity/perplexity-launcher.sh
ExclusiveArch:  x86_64
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       bubblewrap
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXrandr
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       libdrm
Requires:       libgcc
Requires:       libnotify
Requires:       libsecret
Requires:       libuuid
Requires:       libxcb
Requires:       libxkbcommon
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       psmisc
Requires:       systemd-libs
Requires:       vulkan-loader
Requires:       xdg-utils

%description
Official Perplexity desktop app. This package repacks the upstream Debian
release, keeping its bundled Electron runtime and installing the
flags-aware launcher from the upstream Omarchy package, mirroring the
upstream PKGBUILD. The 26.9.6+build95799 build is the current pool
revision; the PKGBUILD's 26.9.6+build89647 file no longer exists upstream.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -

%build
:

%install
# The 26.9.1+ tree started shipping a systemd unit under /lib, which Fedora
# owns as a symlink; the unit is a no-op here (its setup script apt-installs
# Docker and exits on non-Ubuntu), so drop it like the PKGBUILD does. Only
# opt/ and usr/ are installed; anything else left stops the build.
rm -f lib/systemd/system/perplexity-local-runtime-setup.service
rmdir -p lib/systemd/system 2>/dev/null || true
unexpected=$(find . -mindepth 1 -path ./opt -prune -o -path ./usr -prune -o -print)
if [ -n "$unexpected" ]; then
  echo "Unexpected entries outside opt/ and usr/ in the upstream deb:" >&2
  echo "$unexpected" >&2
  exit 1
fi
cp -a opt usr %{buildroot}/
# The deb's postinst would symlink /usr/bin; install the launcher instead,
# and point the menu entry through it so the flags file applies there too.
# NOTE: %%U below is an escaped %U for the RPM parser; the installed
# desktop file sees %U.
rm -f %{buildroot}/usr/bin/perplexity
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/perplexity
sed -i 's|^Exec=.*|Exec=perplexity %%U|' %{buildroot}%{_datadir}/applications/perplexity.desktop
# The deb leaves the sandbox bit to its postinst; set it like the PKGBUILD.
chmod 4755 %{buildroot}/opt/Perplexity/chrome-sandbox
# The profile upstream's postinst would install. It names /opt/Perplexity
# paths, which this package keeps.
install -D -m 0644 %{buildroot}/opt/Perplexity/resources/apparmor-profile %{buildroot}%{_sysconfdir}/apparmor.d/perplexity
# Debian package-policy files are not used on Fedora.
rm -rf %{buildroot}%{_datadir}/doc

%files
%config(noreplace) %{_sysconfdir}/apparmor.d/perplexity
/opt/Perplexity
%{_bindir}/perplexity
%{_datadir}/applications/perplexity.desktop
%{_datadir}/icons/hicolor/*/apps/perplexity.png

%changelog
* Thu Oct 01 2026 kamm3r - 26.9.6+build95799-1
- Repackage the upstream Omarchy Perplexity release for Fedora.
