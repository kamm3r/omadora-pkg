%global debug_package %{nil}
# /opt/Grok Bot bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below. The path contains a space, so the find-provides
# filters see the same basenames as any other Electron tree.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           grok-bot
Version:        0.77.0
Release:        1%{?dist}
Summary:        Grok Bot desktop agent
License:        LicenseRef-proprietary
URL:            https://x.ai/bot
%global omarchy_pkgs_commit a18022b72ccdff9e9e08120eda08513e2eaf14b8
# The release feed moves before Cursor's apt pool; pin its release commit.
%global upstream_commit fe85646036572e2b9a531b337a0dcb56a32f9369
Source0:        https://downloads.cursor.com/grokbot/stable/%{upstream_commit}/linux/x64/grok-bot_%{version}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/grok-bot/grok-bot.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/grok-bot/grok-bot.desktop
ExclusiveArch:  x86_64
Provides:       sand = %{version}-%{release}
Conflicts:      sand
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libnotify
Requires:       libsecret
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       nss
Requires:       libuuid
Requires:       xdg-utils

%description
Grok Bot desktop agent. This package repacks the upstream Debian release,
keeping its bundled Electron runtime and installing the Wayland wrapper and
desktop entry from the upstream Omarchy package, mirroring the upstream
PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD, then drop the Debian-only and superseded entries.
cp -a opt usr %{buildroot}/
rm -rf %{buildroot}%{_datadir}/doc
rm -f %{buildroot}%{_datadir}/applications/sand.desktop %{buildroot}%{_datadir}/applications/grok-bot.desktop
# Always install the Wayland wrapper; do not keep any /usr/bin from the .deb.
rm -f %{buildroot}/usr/bin/grok-bot %{buildroot}/usr/bin/sand
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/grok-bot
ln -s grok-bot %{buildroot}%{_bindir}/sand
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/grok-bot.desktop
# Licenses live inside the app tree, as in the upstream PKGBUILD.
install -D -m 0644 "%{buildroot}/opt/Grok Bot/LICENSE.electron.txt" %{buildroot}%{_licensedir}/grok-bot/LICENSE.electron.txt
install -D -m 0644 "%{buildroot}/opt/Grok Bot/LICENSES.chromium.html" %{buildroot}%{_licensedir}/grok-bot/LICENSES.chromium.html
# Ship chrome-sandbox without setuid. Upstream's build-time userns probe
# would measure the CI container, not the user's machine, and a setuid
# helper cannot exec from "/opt/Grok Bot/" (electron#44414). Hosts without
# unprivileged user namespaces can add --no-sandbox to
# ~/.config/grok-bot-flags.conf.
chmod 0755 "%{buildroot}/opt/Grok Bot/chrome-sandbox"

%files
%license %{_licensedir}/grok-bot/LICENSE.electron.txt
%license %{_licensedir}/grok-bot/LICENSES.chromium.html
"/opt/Grok Bot"
%{_bindir}/grok-bot
%{_bindir}/sand
%{_datadir}/applications/grok-bot.desktop
%{_datadir}/icons/hicolor/*/apps/grok-bot.png

%changelog
* Tue Oct 27 2026 kamm3r - 0.77.0-1
- Update to the release pinned in upstream a18022b7.
- Use the pinned release-feed download because the apt pool lags releases.

* Mon Oct 26 2026 kamm3r - 0.75.8-1
- Update to the release pinned in upstream d5e4ad59.

* Fri Oct 23 2026 kamm3r - 0.75.3-1
- Update to the release pinned in upstream 5cf42189.

* Thu Oct 22 2026 kamm3r - 0.75.0-1
- Update to the release pinned in upstream de5c031f.

* Wed Oct 21 2026 kamm3r - 0.72.1-1
- Update to the release pinned in upstream 4c2785f4.

* Tue Oct 20 2026 kamm3r - 0.72.0-1
- Update to the release pinned in upstream 3e3a4343.

* Thu Oct 15 2026 kamm3r - 0.71.2-1
- Update to the release pinned in upstream d9ebd3f6.

* Tue Oct 13 2026 kamm3r - 0.70.2-1
- Update to the release pinned in upstream e499d021.

* Sat Oct 10 2026 kamm3r - 0.68.1-1
- Update to the release pinned in upstream 8787c23f.

* Thu Oct 01 2026 kamm3r - 0.47.0-1
- Repackage the upstream Omarchy Grok Bot release for Fedora.
