%global debug_package %{nil}
# /usr/lib/claude-desktop bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           claude-desktop
Version:        2.7032.0
Release:        1%{?dist}
Summary:        Official Claude desktop app with Claude Code
License:        LicenseRef-proprietary
URL:            https://claude.ai
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_%{version}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/claude-desktop/claude-desktop-launcher.sh
ExclusiveArch:  x86_64
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
Requires:       systemd-libs
Requires:       xdg-utils

%description
Official Claude desktop app with Claude Code. This package repacks the
upstream Debian release, keeping its bundled Electron runtime and replacing
the /usr/bin symlink with the flags-aware launcher from the upstream
Omarchy package, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD.
cp -a usr %{buildroot}/
# Upstream's /usr/bin/claude-desktop is a bare symlink to the Electron
# binary; replace it with the Ozone-aware launcher.
rm -f %{buildroot}/usr/bin/claude-desktop
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/claude-desktop
# Move the Debian copyright to the Fedora license dir.
install -D -m 0644 %{buildroot}%{_datadir}/doc/claude-desktop/copyright %{buildroot}%{_licensedir}/claude-desktop/copyright
# Debian package-policy files are not used on Fedora.
rm -rf %{buildroot}%{_datadir}/doc %{buildroot}%{_datadir}/lintian
# Cowork VM symlinks from the PKGBUILD are Arch-specific (/usr/lib/virtiofsd
# and /usr/share/edk2/x64/...); Fedora's virtiofsd lives at
# /usr/libexec/virtiofsd already and edk2-ovmf uses a different layout, and
# shipping a /usr/libexec/virtiofsd symlink would conflict with the real
# virtiofsd package, so no links are created here.
# Use Electron's unprivileged namespace sandbox.
if [ -f %{buildroot}/usr/lib/claude-desktop/chrome-sandbox ]; then
  chmod 0755 %{buildroot}/usr/lib/claude-desktop/chrome-sandbox
fi

%files
%license %{_licensedir}/claude-desktop/copyright
/usr/lib/claude-desktop
%{_bindir}/claude-desktop
%{_datadir}/applications/com.anthropic.Claude.desktop
%{_datadir}/icons/hicolor/*/apps/claude-desktop.png

%changelog
* Thu Oct 01 2026 kamm3r - 2.7032.0-1
- Repackage the upstream Omarchy Claude Desktop release for Fedora.
