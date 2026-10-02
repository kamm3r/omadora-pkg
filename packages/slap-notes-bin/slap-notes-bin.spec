%global debug_package %{nil}
# The tarball bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           slap-notes-bin
Version:        0.2.3
Release:        1%{?dist}
Summary:        Local-first block notes with wiki-link graph and AI research agent
License:        LicenseRef-proprietary
URL:            https://slapnotes.com
Source0:        https://github.com/Onefailatatime/slap-notes/releases/download/%{version}/slap-notes-%{version}-linux-x64.tar.zst#/%{name}-%{version}.tar.zst
ExclusiveArch:  x86_64
Provides:       slap-notes = %{version}-%{release}
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
Local-first block notes with a wiki-link graph and a built-in AI research
agent. This package repacks the vendor Electron tree, mirroring the
upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
tar --zstd -xf "%{SOURCE0}"

%build
:

%install
cd slap-notes-%{version}
install -d %{buildroot}/opt/slap-notes
cp -a app/. %{buildroot}/opt/slap-notes/
chmod -R a+rX %{buildroot}/opt/slap-notes
# Use Electron's unprivileged namespace sandbox.
chmod 0755 %{buildroot}/opt/slap-notes/chrome-sandbox
# Launcher wrapper, verbatim from the upstream Omarchy package sources.
cat > slap-notes-launcher.sh <<'LAUNCHER_EOF'
#!/bin/bash
set -euo pipefail

user_flags=()
config_home="${XDG_CONFIG_HOME:-}"
[[ -n "$config_home" || -z "${HOME:-}" ]] || config_home="$HOME/.config"
flags_file="${config_home:+$config_home/slap-notes-flags.conf}"

if [[ -n "$flags_file" && -f "$flags_file" && -r "$flags_file" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"
    [[ -n "${line//[[:space:]]/}" ]] || continue
    read -r -a flags <<<"$line"
    user_flags+=("${flags[@]}")
  done <"$flags_file"
fi

# Chromium's own Ozone detection falls back to XWayland often enough to matter,
# and the result is a blurry window on every scaled display. Ask for Wayland
# directly, unless the user has already picked a platform themselves.
platform_flags=()
if [[ -n "${WAYLAND_DISPLAY:-}" || "${XDG_SESSION_TYPE:-}" == wayland ]]; then
  platform_flags=(--ozone-platform=wayland)

  for flag in "${user_flags[@]}" "$@"; do
    case "$flag" in
      --ozone-platform=* | --ozone-platform-hint=*) platform_flags=() ;;
    esac
  done
fi

exec /opt/slap-notes/slap-notes "${platform_flags[@]}" "${user_flags[@]}" "$@"
LAUNCHER_EOF
install -D -m 0755 slap-notes-launcher.sh %{buildroot}%{_bindir}/slap-notes
sed -e "s|^Exec=.*|Exec=slap-notes %U|" slap-notes.desktop > slap-notes.desktop.arch
install -D -m 0644 slap-notes.desktop.arch %{buildroot}%{_datadir}/applications/slap-notes.desktop
for size in 16 32 48 64 128 256 512 1024; do
  install -D -m 0644 icons/${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/slap-notes.png
done
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%license %{_datadir}/licenses/%{name}/LICENSE
/opt/slap-notes
%{_bindir}/slap-notes
%{_datadir}/applications/slap-notes.desktop
%{_datadir}/icons/hicolor/*/apps/slap-notes.png

%changelog
* Wed Sep 30 2026 kamm3r - 0.2.3-1
- Repackage the upstream Omarchy Slap Notes release for Fedora.
