%global debug_package %{nil}
# /opt/obsidian bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so|/usr/bin/node)

Name:           obsidian
Version:        1.13.7
Release:        1%{?dist}
Summary:        Knowledge base on top of a local folder of plain-text Markdown files
License:        LicenseRef-Obsidian
URL:            https://obsidian.md/
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://github.com/obsidianmd/obsidian-releases/releases/download/v%{version}/obsidian-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/obsidian/obsidian.desktop
ExclusiveArch:  x86_64
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       fontconfig
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
Requires:       libdrm
Requires:       libgcc
Requires:       libnotify
Requires:       libsecret
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
Obsidian is a knowledge base on top of a local folder of plain-text
Markdown files. This package repacks the upstream binary release, keeping
its bundled Electron runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a tarball with a top-level obsidian-%{version} directory,
# so unpack manually without autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE0}"

%build
:

%install
install -d %{buildroot}/opt/obsidian
cp -a --no-preserve=ownership obsidian-%{version}/. %{buildroot}/opt/obsidian/

find %{buildroot}/opt/obsidian -type d -exec chmod 0755 {} +
find %{buildroot}/opt/obsidian -type f -exec chmod 0644 {} +
chmod 0755 \
  %{buildroot}/opt/obsidian/chrome_crashpad_handler \
  %{buildroot}/opt/obsidian/obsidian \
  %{buildroot}/opt/obsidian/obsidian-cli
# Chromium sandboxes through unprivileged user namespaces; a setuid-root
# helper is not needed (mirrors the upstream PKGBUILD).
chmod 0755 %{buildroot}/opt/obsidian/chrome-sandbox

install -d %{buildroot}%{_bindir}
ln -s /opt/obsidian/obsidian %{buildroot}%{_bindir}/obsidian
ln -s /opt/obsidian/obsidian-cli %{buildroot}%{_bindir}/obsidian-cli
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/obsidian.desktop
install -D -m 0644 obsidian-%{version}/resources/icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/obsidian.png
install -D -m 0644 obsidian-%{version}/LICENSE.electron.txt %{buildroot}%{_licensedir}/obsidian/LICENSE.electron.txt
install -D -m 0644 obsidian-%{version}/LICENSES.chromium.html %{buildroot}%{_licensedir}/obsidian/LICENSES.chromium.html

%files
%license %{_licensedir}/obsidian/LICENSE.electron.txt
%license %{_licensedir}/obsidian/LICENSES.chromium.html
/opt/obsidian
%{_bindir}/obsidian
%{_bindir}/obsidian-cli
%{_datadir}/applications/obsidian.desktop
%{_datadir}/icons/hicolor/512x512/apps/obsidian.png

%changelog
* Thu Oct 01 2026 kamm3r - 1.13.7-1
- Repackage the upstream Omarchy Obsidian release for Fedora.
