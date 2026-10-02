%global debug_package %{nil}
# /usr/share/cursor bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
# The tree bundles its own Node runtime; the only #!/usr/bin/env node
# shebangs belong to bundled node_modules CLI helpers that run under the
# bundled runtime, so keep that interpreter scrap out of the RPM dependency
# namespace (mirrors cursor-cli).
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)$

Name:           cursor-bin
Version:        3.22.7
Release:        1%{?dist}
Summary:        AI-first coding environment
License:        LicenseRef-Cursor
URL:            https://www.cursor.com
%global _commit 37076c6c3f9e253c0fa2305197e45befd13a2268
Source0:        https://downloads.cursor.com/production/%{_commit}/linux/x64/deb/amd64/deb/cursor_%{version}_amd64.deb#/%{name}-%{version}.deb
ExclusiveArch:  x86_64
Provides:       cursor = %{version}-%{release}
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
Requires:       libxkbfile
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils

%description
Cursor is an AI-first coding environment. This package repacks the upstream
binary release, keeping its bundled Electron runtime and disabling Cursor's
bundled updater so updates stay managed by the package manager, mirroring
the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
# Extract the deb payload, dropping Debian-only configuration (AppArmor and
# sysctl settings), mirroring the upstream PKGBUILD's etc exclusion.
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -
rm -rf etc
# Disable Cursor's bundled updater; Omarchy manages updates via the package
# manager (mirrors the upstream PKGBUILD's product.json edit).
sed -i '/^[[:space:]]*"\(backupUpdateUrl\|updateUrl\)":/d' \
  usr/share/cursor/resources/app/product.json
# Fedora uses site-functions, not vendor-completions, for zsh completions.
mv usr/share/zsh/vendor-completions usr/share/zsh/site-functions

%build
:

%install
# Install verbatim from the unpacked payload, keeping the bundled Electron,
# node, and ripgrep runtimes (mirrors the upstream aarch64 packaging path,
# since Fedora has no system electron42 to link against).
cp -a usr %{buildroot}/
install -d %{buildroot}%{_bindir}
ln -s /usr/share/cursor/bin/cursor %{buildroot}%{_bindir}/cursor
# Use Electron's unprivileged namespace sandbox.
chmod 0755 %{buildroot}/usr/share/cursor/chrome-sandbox

%files
%license usr/share/cursor/resources/app/LICENSE.txt
/usr/share/cursor
%{_bindir}/cursor
%{_datadir}/applications/cursor.desktop
%{_datadir}/applications/cursor-url-handler.desktop
%{_datadir}/appdata/cursor.appdata.xml
%{_datadir}/bash-completion/completions/cursor
%{_datadir}/zsh/site-functions/_cursor
%{_datadir}/mime/packages/cursor-workspace.xml
%{_datadir}/pixmaps/co.anysphere.cursor.png

%changelog
* Wed Sep 30 2026 kamm3r - 3.22.7-1
- Repackage the upstream Omarchy Cursor release for Fedora.
