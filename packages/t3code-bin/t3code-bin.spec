%global debug_package %{nil}
# The AppImage bundles its own Electron runtime plus prebuilt Node helpers.
# Keep those private libraries and interpreter scraps out of the RPM
# dependency namespace; system libraries stay explicitly required below.
%global __provides_exclude ^lib(fff_c|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(fff_c|ffmpeg|vk_swiftshader|vulkan)\.so|libc\.musl|libc\.so\(\)|/usr/bin/node)

Name:           t3code-bin
Version:        0.0.44
Release:        1%{?dist}
Summary:        Open-source control plane for coding agents
License:        MIT
URL:            https://t3.codes
# Upstream ships a bare AppImage (plus a license file), not a tarball, so
# there is no top directory to autosetup; it is extracted with 7z in %prep.
Source0:        https://github.com/pingdotgg/t3code/releases/download/v%{version}/T3-Code-%{version}-x86_64.AppImage#/%{name}-%{version}-x86_64.AppImage
Source1:        https://raw.githubusercontent.com/pingdotgg/t3code/v%{version}/LICENSE#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64
Provides:       t3code = %{version}-%{release}
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
flags_file="${config_home:+$config_home/t3code-flags.conf}"

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

exec /usr/lib/t3code/t3code "${platform_flags[@]}" "${user_flags[@]}" "$@"
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
exec /usr/lib/t3code/t3code /usr/lib/t3code/resources/app.asar/apps/server/dist/bin.mjs "$@"
LAUNCHER_EOF

cd squashfs-root

# The x86_64 AppImage also bundles node-pty's ARM prebuild. It is unused here
# and would add ARM loader requirements to this x86_64 RPM.
rm -rf resources/app.asar.unpacked/node_modules/node-pty/prebuilds/linux-arm64

# Guard from the upstream PKGBUILD: the AppImage's usr/ tree must only carry
# icons and compatibility libraries; anything else stops the build.
unexpected=$(find usr \( -type f -o -type l \) | grep -vE '^usr/share/icons/hicolor/[0-9]+x[0-9]+/apps/t3code\.png$|^usr/lib/lib(Xss\.so\.1|Xtst\.so\.6|appindicator\.so\.1|gconf-2\.so\.4|indicator\.so\.7|notify\.so\.4)$' || true)
if [ -n "$unexpected" ]; then
  echo "Unexpected files in the AppImage's usr/ tree:" >&2
  echo "$unexpected" >&2
  exit 1
fi

for icon in usr/share/icons/hicolor/*/apps/t3code.png; do
  size=${icon#usr/share/icons/hicolor/}
  # NOTE: %%%% below is an escaped %% for the RPM parser; the shell sees ${size%%/*}.
  install -D -m 0644 "$icon" "%{buildroot}%{_datadir}/icons/hicolor/${size%%%%/*}/apps/t3code.png"
done

# Upstream's own desktop entry carries the t3code:// scheme handlers; only the
# launcher command, the display name, and the AppImage stamp are rewritten.
sed -e 's|^Exec=.*|Exec=t3code %%U|' -e 's|^Name=.*|Name=T3 Code|' -e '/^X-AppImage-Version=/d' t3code.desktop > ../t3code.desktop.arch
install -D -m 0644 ../t3code.desktop.arch %{buildroot}%{_datadir}/applications/t3code.desktop

rm -rf AppRun .DirIcon usr t3code.desktop t3code.png
install -d %{buildroot}/usr/lib/t3code
cp -a . %{buildroot}/usr/lib/t3code/
chmod -R a+rX %{buildroot}/usr/lib/t3code
chmod 4755 %{buildroot}/usr/lib/t3code/chrome-sandbox

install -D -m 0755 ../t3code-launcher.sh %{buildroot}%{_bindir}/t3code
install -D -m 0755 ../t3-launcher.sh %{buildroot}%{_bindir}/t3

%files
%license LICENSE
/usr/lib/t3code
%{_bindir}/t3code
%{_bindir}/t3
%{_datadir}/applications/t3code.desktop
%{_datadir}/icons/hicolor/*/apps/t3code.png

%changelog
* Sat Oct 03 2026 kamm3r - 0.0.44-1
- Update to the release pinned on upstream master.
- Remove the unused ARM terminal helper from the x86_64 bundle.

* Wed Sep 30 2026 kamm3r - 0.0.42-1
- Repackage the upstream Omarchy T3 Code release for Fedora.
