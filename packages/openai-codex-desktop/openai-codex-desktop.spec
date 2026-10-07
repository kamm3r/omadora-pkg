%global debug_package %{nil}
# /usr/lib/chatgpt bundles its own Electron runtime plus private libraries
# (including Qt shims, a musl/NDK toolchain and libvips). Keep those out of
# the RPM dependency namespace; system libraries stay explicitly required
# below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|vips.*|log|c.._shared)\.so
%global __requires_exclude ^((lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|vips.*|log|c.._shared)\.so|libc\.musl.*|libc\.so($|[^.])|libdl\.so($|[^.])|libm\.so($|[^.])|libpthread\.so($|[^.])|libgcc_s\.so($|[^.]))|/usr/bin/(node|pwsh)$)

Name:           openai-codex-desktop
Version:        26.930.41038
Release:        1%{?dist}
Summary:        Official ChatGPT desktop app with Codex
License:        LicenseRef-proprietary
URL:            https://chatgpt.com/codex/
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        https://persistent.oaistatic.com/codex-app-prod/linux/deb/pool/main/c/chatgpt/chatgpt_%{version}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openai-codex-desktop/chatgpt-launcher.sh
ExclusiveArch:  x86_64
Provides:       chatgpt = %{version}-%{release}
Provides:       codex-desktop = %{version}-%{release}
Conflicts:      chatgpt
Requires:       alsa-lib
Requires:       at-spi2-core
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
Requires:       libdrm
Requires:       libgcc
Requires:       libnotify
Requires:       libusb1
Requires:       libxcb
Requires:       libxkbcommon
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       openssl-libs
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils
Requires:       xz-libs

%description
Official ChatGPT desktop app with Codex. This package repacks the upstream
Debian release, keeping its bundled Electron runtime and replacing the
/usr/bin entry with the flags-aware launcher from the upstream Omarchy
package, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD (which keeps the deb's AppArmor profile).
cp -a etc usr %{buildroot}/
rm -f %{buildroot}/usr/bin/chatgpt
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/chatgpt
ln -s chatgpt %{buildroot}%{_bindir}/codex-desktop
# Move the Debian copyright to the Fedora license dir.
install -D -m 0644 %{buildroot}%{_datadir}/doc/chatgpt/copyright %{buildroot}%{_licensedir}/openai-codex-desktop/copyright
# Debian package-policy files are not used on Fedora.
rm -rf %{buildroot}%{_datadir}/doc %{buildroot}%{_datadir}/lintian
# Use Electron's unprivileged namespace sandbox.
if [ -f %{buildroot}/usr/lib/chatgpt/chrome-sandbox ]; then
  chmod 0755 %{buildroot}/usr/lib/chatgpt/chrome-sandbox
fi

%files
%license %{_licensedir}/openai-codex-desktop/copyright
%config(noreplace) /etc/apparmor.d/chatgpt
/usr/lib/chatgpt
%{_bindir}/chatgpt
%{_bindir}/codex-desktop
%{_datadir}/applications/chatgpt.desktop
%{_datadir}/pixmaps/chatgpt.png
%{_datadir}/metainfo/com.openai.chatgpt.metainfo.xml
%{_datadir}/swcatalog/xml/com.openai.chatgpt.xml

%changelog
* Tue Oct 06 2026 kamm3r - 26.930.41038-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 26.924.22138-1
- Repackage the upstream Omarchy ChatGPT/Codex desktop release for Fedora.
