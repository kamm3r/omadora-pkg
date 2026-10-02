%global debug_package %{nil}
# /opt/Heroic bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so

Name:           heroic-games-launcher-bin
Version:        2.22.3
Release:        1%{?dist}
Summary:        Open source launcher for Epic, Amazon and GOG games
License:        GPL-3.0-only
URL:            https://heroicgameslauncher.com/
Source0:        https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/download/v%{version}/Heroic-%{version}-linux-x64.pacman#/%{name}-%{version}.pacman
ExclusiveArch:  x86_64
Provides:       heroic-games-launcher = %{version}-%{release}
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
Requires:       which
Requires:       xdg-utils

%description
Heroic is an open source launcher for Epic, Amazon and GOG games. This
package repacks the upstream binary release, keeping its bundled Electron
runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships an Arch pacman tarball (xz-compressed), not a tarball with
# a top directory, so there is nothing to autosetup; it is unpacked with tar.
%setup -q -c -T -n %{name}-%{version}
tar -xf "%{SOURCE0}"

%build
:

%install
# Install verbatim from the upstream tarball, mirroring the upstream
# PKGBUILD (which extracts only usr and opt, leaving .PKGINFO/.MTREE behind).
cp -a opt usr %{buildroot}/
install -d %{buildroot}%{_bindir}
ln -s /opt/Heroic/heroic %{buildroot}%{_bindir}/heroic
chmod 4755 %{buildroot}/opt/Heroic/chrome-sandbox

%files
/opt/Heroic
%{_bindir}/heroic
%{_datadir}/applications/heroic.desktop
%{_datadir}/icons/hicolor/*/apps/heroic.png

%changelog
* Wed Sep 30 2026 kamm3r - 2.22.3-1
- Repackage the upstream Omarchy Heroic Games Launcher release for Fedora.
