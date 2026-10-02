%global debug_package %{nil}
# /usr/share/typora bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so
%global __requires_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so

Name:           typora
Version:        1.14.9
Release:        1%{?dist}
Summary:        Minimal markdown editor and reader
License:        LicenseRef-Typora
URL:            https://typora.io/
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://download.typora.io/linux/typora_%{version}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/typora/typora.sh
ExclusiveArch:  x86_64
BuildRequires:  zstd
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
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
Requires:       libgcc
Requires:       libnotify
Requires:       libxcb
Requires:       libxkbcommon
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils

%description
Typora is a minimal markdown editor and reader. This package repacks the
upstream binary release, keeping its bundled Electron runtime, mirroring
the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.zst | tar -I zstd -xf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD (which drops lintian overrides and replaces the /usr/bin link
# with a flags-aware launcher).
cp -a usr %{buildroot}/
rm -rf %{buildroot}/usr/share/lintian
rm -f %{buildroot}/usr/bin/typora
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/typora
# Move the Debian copyright to the Fedora license dir.
install -D -m 0644 %{buildroot}%{_datadir}/doc/typora/copyright %{buildroot}%{_licensedir}/typora/LICENSE
rm %{buildroot}%{_datadir}/doc/typora/copyright
rmdir --ignore-fail-on-non-empty %{buildroot}%{_datadir}/doc/typora %{buildroot}%{_datadir}/doc
# Remove the change log from the application comment, mirroring upstream.
sed -i '/Change Log/d' %{buildroot}%{_datadir}/applications/typora.desktop
chmod 0644 %{buildroot}%{_datadir}/applications/typora.desktop
chmod 0644 %{buildroot}%{_datadir}/typora/resources/packages/node-spellchecker/vendor/hunspell_dictionaries/en_US.dic %{buildroot}%{_datadir}/typora/resources/packages/node-spellchecker/vendor/hunspell_dictionaries/en_US.aff
find %{buildroot} -type d -exec chmod 0755 {} \;

%files
%license %{_licensedir}/typora/LICENSE
/usr/share/typora
%{_bindir}/typora
%{_datadir}/applications/typora.desktop
%{_datadir}/icons/hicolor/*/apps/typora.png

%changelog
* Wed Sep 30 2026 kamm3r - 1.14.9-1
- Repackage the upstream Omarchy release for Fedora.
