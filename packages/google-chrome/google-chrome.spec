%global debug_package %{nil}
# /opt/google/chrome bundles its own Chromium runtime plus private
# libraries. Keep those out of the RPM dependency namespace; system
# libraries stay explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|widevinecdm)\\.so
%global __requires_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|widevinecdm)\\.so

Name:           google-chrome
Version:        154.0.8037.97
Release:        1%{?dist}
Summary:        Popular web browser by Google (Stable Channel)
License:        LicenseRef-Google-Chrome
URL:            https://www.google.com/chrome
%global _channel stable
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-%{_channel}/google-chrome-%{_channel}_%{version}-1_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/google-chrome/google-chrome-stable.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/google-chrome/eula_text.html
ExclusiveArch:  x86_64
Provides:       google-chrome-stable = %{version}-%{release}
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
Requires:       liberation-sans-fonts
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
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxml2
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils

%description
Google Chrome is the popular web browser by Google (Stable Channel). This
package repacks the upstream binary release, keeping its bundled Chromium
runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD (which drops the Debian cron job and installs a flags-aware
# launcher plus icons and license).
cp -a opt usr %{buildroot}/
rm -rf %{buildroot}/opt/google/chrome/cron

# Launcher, verbatim from the upstream package sources.
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/google-chrome-stable

# Icons, mirroring the upstream PKGBUILD.
for i in 16x16 24x24 32x32 48x48 64x64 128x128 256x256; do
  install -D -m 0644 opt/google/chrome/product_logo_${i/x*/}.png %{buildroot}%{_datadir}/icons/hicolor/$i/apps/google-chrome.png
done
rm -f %{buildroot}/opt/google/chrome/product_logo_*.png

# License, verbatim from the upstream package sources, plus the bundled
# Widevine license.
install -D -m 0644 %{SOURCE2} %{buildroot}%{_licensedir}/google-chrome/eula_text.html
install -D -m 0644 opt/google/chrome/WidevineCdm/LICENSE %{buildroot}%{_licensedir}/google-chrome-stable/WidevineCdm-LICENSE.txt

# Fix both Chrome desktop entries, mirroring the upstream PKGBUILD.
sed -i \
  -e "/Exec=/iStartupWMClass=Google-chrome" \
  -e "s/x-scheme-handler\/ftp;\?//g" \
  %{buildroot}%{_datadir}/applications/*.desktop

# The Debian cron job is never copied (only opt and usr are installed),
# mirroring upstream's removal.
rm -rf %{buildroot}/etc

%files
%license %{_licensedir}/google-chrome/eula_text.html
%license %{_licensedir}/google-chrome-stable/WidevineCdm-LICENSE.txt
/opt/google/chrome
%{_bindir}/google-chrome-stable
%{_datadir}/applications/google-chrome.desktop
%{_datadir}/applications/com.google.Chrome.desktop
%{_datadir}/appdata/google-chrome.appdata.xml
%{_datadir}/man/man1/google-chrome.1.gz
%{_datadir}/man/man1/google-chrome-stable.1.gz
%{_datadir}/gnome-control-center/default-apps/google-chrome.xml
%{_datadir}/icons/hicolor/*/apps/google-chrome.png
%{_datadir}/doc/google-chrome-stable/changelog.gz

%changelog
* Tue Oct 06 2026 kamm3r - 154.0.8037.97-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 154.0.8037.57-1
- Repackage the upstream Omarchy release for Fedora.
