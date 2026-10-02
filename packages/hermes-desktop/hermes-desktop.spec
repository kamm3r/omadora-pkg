%global debug_package %{nil}
# /opt/hermes-desktop bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           hermes-desktop
Version:        2026.9.7
Release:        1%{?dist}
Summary:        Native desktop shell for Hermes Agent
License:        MIT
URL:            https://github.com/NousResearch/hermes-agent
# The tag's commit. apps/desktop/scripts/write-build-stamp.mjs pins the app's
# first-launch bootstrap to a Hermes commit, resolved from $GITHUB_SHA.
%global _commit 2237be355906fbe6065ce1815711eee52b2d646e
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hermes-desktop/hermes-desktop.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hermes-desktop/hermes-desktop.desktop
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hermes-desktop/hermes-desktop.png
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hermes-desktop/runtime.patch
Source5:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hermes-desktop/runtime-test.py
ExclusiveArch:  x86_64
BuildRequires:  ImageMagick
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  python3
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       curl
Requires:       dbus-libs
Requires:       expat
Requires:       gcc
Requires:       gdk-pixbuf2
Requires:       git
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       cups-libs
Requires:       libdrm
Requires:       libnotify
Requires:       libsecret
Requires:       libX11
Requires:       libxcb
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libxkbcommon
Requires:       libXrandr
Requires:       make
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nodejs
Requires:       npm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       python3
Requires:       systemd-libs
Requires:       util-linux
Requires:       xdg-utils

%description
Native desktop shell for Hermes Agent. This package builds the prebuilt
release from the upstream tag with the repo's own npm workspace (which
fetches Electron and rebuilds node-pty against it) and seeds it so the
upstream updater can rebuild and relaunch it in place, mirroring the
upstream PKGBUILD.

%prep
%autosetup -n hermes-agent-%{version}
cp "%{SOURCE1}" hermes-desktop.sh
cp "%{SOURCE2}" hermes-desktop.desktop
cp "%{SOURCE3}" hermes-desktop.png
cp "%{SOURCE4}" runtime.patch
cp "%{SOURCE5}" runtime-test.py

%build
export GITHUB_SHA="%{_commit}"
export GITHUB_REF_NAME="main"
# Upstream's .npmrc sets engine-strict=true and engines.npm to
# "<11.10.0 || >=11.17.0". Fedora 44 ships npm 11.12.1, inside the excluded
# gap, while its node (v24) satisfies engines.node. The npm range gates the
# min-release-age freshness feature (unknown to this npm, warn-only) while
# npm ci itself stays pinned to package-lock.json, so relax just the strict
# gate; Arch (newer npm) needs no override.
export npm_config_engine_strict=false
# The desktop workspace resolves against the repo root, so the install has
# to happen there rather than in apps/desktop.
npm ci
cd apps/desktop
npm run pack

%check
python3 runtime-test.py "$PWD" "$PWD/runtime.patch" "$PWD/hermes-desktop.sh"

%install
cd apps/desktop/release/linux-unpacked
install -dm755 %{buildroot}/opt/%{name}
cp -a . %{buildroot}/opt/%{name}/
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 ../../../../scripts/install.sh %{buildroot}%{_datadir}/%{name}/install.sh
# The installer still requires this patch. The release includes the fix, so
# the installer recognizes it through its reverse-apply check.
install -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/runtime.patch
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png
for size in 512 256 128 64 48; do
  magick %{SOURCE3} -resize "${size}x${size}" icon-${size}.png
  install -D -m 0644 icon-${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done
install -D -m 0644 ../../../../LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -D -m 0644 LICENSE.electron.txt %{buildroot}%{_licensedir}/%{name}/LICENSE.electron.txt
# The launcher requires the namespace sandbox on the target host.
chmod 0755 %{buildroot}/opt/%{name}/chrome-sandbox

%files
%license %{_licensedir}/%{name}/LICENSE
%license %{_licensedir}/%{name}/LICENSE.electron.txt
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}/install.sh
%{_datadir}/%{name}/runtime.patch

%changelog
* Thu Oct 01 2026 kamm3r - 2026.9.7-1
- Build the upstream Omarchy Hermes Desktop release for Fedora.
