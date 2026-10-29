%global debug_package %{nil}
# The AppImage bundles its own Electron runtime plus prebuilt Node helpers.
# Keep those private libraries and interpreter scraps out of the RPM
# dependency namespace; system libraries stay explicitly required below.
%global __provides_exclude ^lib(fff_c|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(fff_c|ffmpeg|vk_swiftshader|vulkan)\.so|libc\.musl|libc\.so\(\)|/usr/bin/node)

Name:           t3code-nightly-bin
Version:        0.1.4_nightly.20261029.3853
Release:        1%{?dist}
Summary:        Open-source control plane for coding agents (nightly)
License:        MIT
URL:            https://t3.codes
# Upstream ships a bare AppImage (plus a license file), not a tarball, so
# there is no top directory to autosetup; it is extracted with 7z in %%prep.
%global upstream_version 0.1.4-nightly.20261029.3853
Source0:        https://github.com/pingdotgg/t3code/releases/download/v%{upstream_version}/T3-Code-%{upstream_version}-x86_64.AppImage#/%{name}-%{version}-x86_64.AppImage
Source1:        https://raw.githubusercontent.com/pingdotgg/t3code/v%{upstream_version}/LICENSE#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64
Provides:       t3code-nightly = %{version}-%{release}
BuildRequires:  7zip
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
Open-source control plane for coding agents.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE1}" LICENSE
7z x "%{SOURCE0}" -osquashfs-root > /dev/null

%build
:

%install
# Launcher wrappers, verbatim from the upstream Omarchy package sources.
cat > t3code-launcher.sh <<'LAUNCHER_EOF'
#!/bin/bash
set -euo pipefail

user_flags=()
config_home="${XDG_CONFIG_HOME:-}"
[[ -n "$config_home" || -z "${HOME:-}" ]] || config_home="$HOME/.config"
flags_file="${config_home:+$config_home/t3code-nightly-flags.conf}"

if [[ -n "$flags_file" && -f "$flags_file" && -r "$flags_file" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"
    [[ -n "${line//[[:space:]]/}" ]] || continue
    read -r -a flags <<<"$line"
    user_flags+=("${flags[@]}")
  done <"$flags_file"
fi

# Chromium's own Ozone detection falls back to XWayland often enough to matter,
# and the result is a blurry window on every scaled display.
platform_flags=()
if [[ -n "${WAYLAND_DISPLAY:-}" || "${XDG_SESSION_TYPE:-}" == wayland ]]; then
  platform_flags=(--ozone-platform=wayland)

  for flag in "${user_flags[@]}" "$@"; do
    case "$flag" in
      --ozone-platform=* | --ozone-platform-hint=*) platform_flags=() ;;
    esac
  done
fi

exec /usr/lib/t3code-nightly/t3code "${platform_flags[@]}" "${user_flags[@]}" "$@"
LAUNCHER_EOF
cat > t3-launcher.sh <<'LAUNCHER_EOF'
#!/bin/bash
# The T3 Code server CLI (`t3`) ships inside the app bundle; upstream only
# distributes it separately through npm. The bundled Electron doubles as the
# Node runtime for it, so the desktop package can put the CLI on PATH without
# shipping a second runtime. Electron's fs layer reads app.asar transparently
# in this mode.
set -euo pipefail

export ELECTRON_RUN_AS_NODE=1
exec /usr/lib/t3code-nightly/t3code /usr/lib/t3code-nightly/resources/app.asar/apps/server/dist/bin.mjs "$@"
LAUNCHER_EOF

cd squashfs-root

# The x86_64 AppImage also bundles node-pty's ARM prebuild. It is unused here
# and would add ARM loader requirements to this x86_64 RPM.
rm -rf resources/app.asar.unpacked/node_modules/node-pty/prebuilds/linux-arm64

# Guard from the upstream PKGBUILD: the AppImage's usr/ tree must only carry
# icons and compatibility libraries; anything else stops the build.
unexpected=$(find usr \( -type f -o -type l \) | grep -vE '^usr/share/icons/hicolor/[0-9]+x[0-9]+/apps/t3code\.png$|^usr/lib/lib(Xss|Xtst|appindicator|appindicator3|gconf-2|indicator|indicator3|notify)\.so(\.[0-9]+)*$' || true)
if [ -n "$unexpected" ]; then
  echo "Unexpected files in the AppImage's usr/ tree:" >&2
  echo "$unexpected" >&2
  exit 1
fi

for icon in usr/share/icons/hicolor/*/apps/t3code.png; do
  size=${icon#usr/share/icons/hicolor/}
  # NOTE: %%%% below is an escaped %% for the RPM parser; the shell sees ${size%%/*}.
  install -D -m 0644 "$icon" "%{buildroot}%{_datadir}/icons/hicolor/${size%%%%/*}/apps/t3code-nightly.png"
done

# Upstream's own desktop entry carries the t3code:// scheme handlers; only the
# launcher command, the display name, and the AppImage stamp are rewritten.
sed -e 's|^Exec=.*|Exec=t3code-nightly %%U|' -e 's|^Name=.*|Name=T3 Code (Nightly)|' -e 's|^Icon=.*|Icon=t3code-nightly|' -e '/^X-AppImage-Version=/d' t3code.desktop > ../t3code.desktop.arch
install -D -m 0644 ../t3code.desktop.arch %{buildroot}%{_datadir}/applications/t3code-nightly.desktop

rm -rf AppRun .DirIcon usr t3code.desktop t3code.png
install -d %{buildroot}/usr/lib/t3code-nightly
cp -a . %{buildroot}/usr/lib/t3code-nightly/
chmod -R a+rX %{buildroot}/usr/lib/t3code-nightly
chmod 4755 %{buildroot}/usr/lib/t3code-nightly/chrome-sandbox

install -D -m 0755 ../t3code-launcher.sh %{buildroot}%{_bindir}/t3code-nightly
install -D -m 0755 ../t3-launcher.sh %{buildroot}%{_bindir}/t3-nightly

%files
%license LICENSE
/usr/lib/t3code-nightly
%{_bindir}/t3code-nightly
%{_bindir}/t3-nightly
%{_datadir}/applications/t3code-nightly.desktop
%{_datadir}/icons/hicolor/*/apps/t3code-nightly.png

%changelog
* Thu Oct 29 2026 kamm3r - 0.1.4_nightly.20261029.3853-1
- Update to the nightly pinned by upstream 941cc6bf.

* Thu Oct 29 2026 kamm3r - 0.1.4_nightly.20261028.3841-1
- Update to the release pinned in upstream 38a5e499.

* Wed Oct 28 2026 kamm3r - 0.1.4_nightly.20261028.3824-1
- Update to the release pinned in upstream aa38eb00.

* Tue Oct 27 2026 kamm3r - 0.1.3_nightly.20261026.3740-1
- Update to the release pinned in upstream a18022b7.

* Mon Oct 26 2026 kamm3r - 0.1.3_nightly.20261026.3717-1
- Update to the release pinned in upstream d5e4ad59.

* Fri Oct 23 2026 kamm3r - 0.1.3_nightly.20261023.3553-1
- Update to the release pinned in upstream 5cf42189.

* Thu Oct 22 2026 kamm3r - 0.1.2_nightly.20261021.3499-1
- Update to the release pinned in upstream de5c031f.

* Tue Oct 20 2026 kamm3r - 0.1.1_nightly.20261020.3411-1
- Update to the release pinned in upstream 3e3a4343.

* Mon Oct 19 2026 kamm3r - 0.1.1_nightly.20261018.3335-1
- Update to the release pinned in upstream de0326b9.

* Sat Oct 17 2026 kamm3r - 0.1.1_nightly.20261017.3238-1
- Update to the release pinned in upstream 64e8fbc2.

* Fri Oct 16 2026 kamm3r - 0.0.46_nightly.20261015.3176-1
- Update to the release pinned in upstream 99243000.

* Thu Oct 15 2026 kamm3r - 0.0.46_nightly.20261015.3145-1
- Update to the release pinned in upstream d9ebd3f6.

* Wed Oct 14 2026 kamm3r - 0.0.46_nightly.20261013.3080-1
- Update to the release pinned in upstream 430bdd13.

* Tue Oct 13 2026 kamm3r - 0.0.46_nightly.20261013.3053-1
- Update to the release pinned in upstream e499d021.

* Sat Oct 10 2026 kamm3r - 0.0.46_nightly.20261010.2908-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 0.0.46_nightly.20261004.2644-1
- Package the upstream nightly channel alongside stable T3 Code.
