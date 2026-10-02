%global debug_package %{nil}
# /opt/spotify bundles its own CEF runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(cef|EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so
%global __requires_exclude ^lib(cef|EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so

Name:           spotify
Version:        1.2.96.518
Release:        1%{?dist}
Summary:        Proprietary music streaming service
License:        LicenseRef-Spotify
URL:            https://www.spotify.com
Epoch:          1
%global _commit g366879e1
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://repository.spotify.com/pool/non-free/s/spotify-client/spotify-client_%{version}.%{_commit}_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/spotify/spotify.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/spotify/spotify.protocol
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/spotify/LICENSE#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libSM
Requires:       libXScrnSaver
Requires:       libayatana-appindicator-gtk3
Requires:       libcurl
Requires:       libnotify
Requires:       nss
Requires:       openssl-libs

%description
Spotify is a proprietary music streaming service. This package repacks the
upstream binary release, keeping its bundled CEF runtime, mirroring the
upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.gz | tar -xzf -
cp "%{SOURCE3}" LICENSE

%build
:

%install
# Enable spotify to open URLs from the webapp, mirroring the upstream
# PKGBUILD. NOTE: %%U below is an escaped %U for the RPM parser; the
# installed desktop file sees %U.
sed -i 's/^Exec=.*/Exec=spotify --uri=%%U/' usr/share/spotify/spotify.desktop
cp -a usr %{buildroot}/

install -D -m 0644 %{buildroot}/usr/share/spotify/spotify.desktop %{buildroot}%{_datadir}/applications/spotify.desktop
install -D -m 0644 %{buildroot}/usr/share/spotify/icons/spotify-linux-512.png %{buildroot}%{_datadir}/pixmaps/spotify-client.png

for size in 22 24 32 48 64 128 256 512; do
  install -D -m 0644 %{buildroot}/usr/share/spotify/icons/spotify-linux-${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/spotify.png
done

# Move the app tree to /opt, mirroring the upstream PKGBUILD.
install -d %{buildroot}/opt/spotify
mv %{buildroot}/usr/share/spotify/* %{buildroot}/opt/spotify/
rmdir %{buildroot}/usr/share/spotify

# Replace the Debian /usr/bin symlink with the flags-aware launcher.
rm -f %{buildroot}/usr/bin/spotify
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/spotify

# KDE protocol file and license, verbatim from the upstream package sources.
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/kservices5/spotify.protocol
install -D -m 0644 LICENSE %{buildroot}%{_licensedir}/spotify/LICENSE

chmod -R go-w %{buildroot}

%files
%license %{_licensedir}/spotify/LICENSE
/opt/spotify
%{_bindir}/spotify
%{_datadir}/applications/spotify.desktop
%{_datadir}/pixmaps/spotify-client.png
%{_datadir}/icons/hicolor/*/apps/spotify.png
%{_datadir}/kservices5/spotify.protocol

%changelog
* Wed Sep 30 2026 kamm3r - 1.2.96.518-1
- Repackage the upstream Omarchy release for Fedora.
