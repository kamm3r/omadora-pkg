%global debug_package %{nil}
# /usr/lib/chatgpt bundles its own Electron runtime plus private libraries
# (including Qt shims, a musl/NDK toolchain and libvips). Keep those out of
# the RPM dependency namespace; system libraries stay explicitly required
# below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|vips.*|log|c.._shared)\.so
%global __requires_exclude ^((lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|qt.*_shim|vips.*|log|c.._shared)\.so|libc\.musl.*|libc\.so($|[^.])|libdl\.so($|[^.])|libm\.so($|[^.])|libpthread\.so($|[^.])|libgcc_s\.so($|[^.]))|/usr/bin/(node|pwsh)$)

Name:           openai-codex-desktop
Version:        26.1027.30824
Release:        1%{?dist}
Summary:        Official ChatGPT desktop app with Codex
License:        LicenseRef-proprietary
URL:            https://chatgpt.com/codex/
%global omarchy_pkgs_commit aa38eb009b20230e008e5cf7005bbdd6b59463f5
%global device_kit_modules usr/lib/chatgpt/resources/app.asar.unpacked/node_modules/@worklouder/device-kit-oai/node_modules/@worklouder/wl-device-kit/node_modules
%global hid_prebuilds %{device_kit_modules}/node-hid/prebuilds
%global serial_prebuilds %{device_kit_modules}/serialport/node_modules/@serialport/bindings-cpp/prebuilds
Source0:        https://persistent.oaistatic.com/codex-app-prod/linux/deb/pool/main/c/chatgpt/chatgpt_%{version}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openai-codex-desktop/chatgpt-launcher.sh
ExclusiveArch:  x86_64
BuildRequires:  python3
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
# node-hid ships prebuilds for other operating systems, ARM and musl.
# Keep the two glibc x86_64 backends used by this package; foreign binaries
# otherwise generate unavailable ARM library dependencies on Fedora x86_64.
test -f "%{hid_prebuilds}/HID-linux-x64/node-napi-v4.node"
test -f "%{hid_prebuilds}/HID_hidraw-linux-x64/node-napi-v4.node"
find "%{hid_prebuilds}" -mindepth 1 -maxdepth 1 -type d ! -name HID-linux-x64 ! -name HID_hidraw-linux-x64 -exec rm -rf -- {} +
# The serial-port dependency also bundles unused ARM and Android modules.
test -f "%{serial_prebuilds}/linux-x64/node.napi.glibc.node"
find "%{serial_prebuilds}" -mindepth 1 -maxdepth 1 -type d ! -name linux-x64 -exec rm -rf -- {} +
rm -f "%{serial_prebuilds}/linux-x64/node.napi.musl.node"

%build
:

%check
python3 - <<'PY'
from pathlib import Path
count = 0
for path in Path("usr/lib/chatgpt").rglob("*"):
    if path.is_symlink() or not path.is_file():
        continue
    with path.open("rb") as stream:
        header = stream.read(20)
    if header[:4] != b"\x7fELF":
        continue
    machine = int.from_bytes(header[18:20], "little" if header[5] == 1 else "big")
    if machine != 62:
        raise SystemExit(f"Foreign ELF architecture {machine}: {path}")
    count += 1
assert count > 0
print(f"PASS: all {count} Codex runtime ELF objects target x86_64")
PY

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
* Fri Oct 30 2026 kamm3r - 26.1027.30824-1
- Update to upstream b766e177.

* Wed Oct 28 2026 kamm3r - 26.1023.51421-1
- Update to the release pinned in upstream aa38eb00.

* Mon Oct 26 2026 kamm3r - 26.1021.22027-1
- Update to the release pinned in upstream d5e4ad59.

* Thu Oct 22 2026 kamm3r - 26.1016.61520-1
- Update to the release pinned in upstream de5c031f.

* Wed Oct 21 2026 kamm3r - 26.1016.51333-1
- Update to the release pinned in upstream 4c2785f4.

* Sat Oct 17 2026 kamm3r - 26.1013.40934-1
- Update to the release pinned in upstream 64e8fbc2.

* Fri Oct 16 2026 kamm3r - 26.1013.31256-1
- Update to the release pinned in upstream 99243000.

* Wed Oct 14 2026 kamm3r - 26.1007.71326-3
- Also remove unused foreign serial-port prebuilds.
- Check every ELF object in the desktop runtime for x86_64 compatibility.

* Wed Oct 14 2026 kamm3r - 26.1007.71326-2
- Remove unused foreign-architecture HID prebuilds from the x86_64 payload.
- Verify both retained HID backends target x86_64.

* Wed Oct 14 2026 kamm3r - 26.1007.71326-1
- Update to the release pinned in upstream 430bdd13.

* Sat Oct 10 2026 kamm3r - 26.1007.21434-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 26.930.41038-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 26.924.22138-1
- Repackage the upstream Omarchy ChatGPT/Codex desktop release for Fedora.
