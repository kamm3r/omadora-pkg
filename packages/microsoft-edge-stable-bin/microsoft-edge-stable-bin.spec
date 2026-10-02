%global debug_package %{nil}
# /opt/microsoft/msedge bundles its own Chromium runtime plus private
# libraries. Keep those out of the RPM dependency namespace; system
# libraries stay explicitly required below.
%global __provides_exclude ^lib(oneauth|oneds|telclient|mip_core_gn|onnxruntime|learning_tools|vk_swiftshader|vulkan|qt.*_shim|widevinecdm)\\.so
%global __requires_exclude ^lib(oneauth|oneds|telclient|mip_core_gn|onnxruntime|learning_tools|vk_swiftshader|vulkan|qt.*_shim|widevinecdm)\\.so

Name:           microsoft-edge-stable-bin
Version:        154.0.4258.37
Release:        1%{?dist}
Summary:        Minimal design browser with sophisticated technology to make the web faster, safer, and easier
License:        LicenseRef-Microsoft-Edge
URL:            https://www.microsoftedgeinsider.com/en-us/download
%global _pkgname microsoft-edge
%global _pkgshortname msedge
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/%{_pkgname}-stable_%{version}-1_amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/microsoft-edge-stable-bin/microsoft-edge-stable.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/microsoft-edge-stable-bin/Microsoft%%20Standard%%20Application%%20License%%20Terms%%20-%%20Standalone%%20(free)%%20Use%%20Terms.pdf#/%{name}-LICENSE-%{version}.pdf
ExclusiveArch:  x86_64
Provides:       microsoft-edge-stable = %{version}-%{release}
Provides:       edge-stable = %{version}-%{release}
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
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxml2
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils

%description
Microsoft Edge is a browser that combines a minimal design with
sophisticated technology to make the web faster, safer, and easier. This
package repacks the upstream binary release, keeping its bundled Chromium
runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -
rm -rf etc

%build
:

%install
# Install verbatim from the unpacked payload, mirroring the upstream
# PKGBUILD (which drops the Debian cron job and installs a flags-aware
# launcher plus icons and license).
cp -a opt usr %{buildroot}/
rm -rf %{buildroot}/opt/microsoft/%{_pkgshortname}/cron

# Suid sandbox, mirroring the upstream PKGBUILD.
chmod 4755 %{buildroot}/opt/microsoft/%{_pkgshortname}/msedge-sandbox

for res in 16 24 32 48 64 128 256; do
  install -D -m 0644 opt/microsoft/%{_pkgshortname}/product_logo_${res}.png %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/%{_pkgname}.png
done

# Flags-aware launcher replaces the Debian symlink.
rm -f %{buildroot}/usr/bin/microsoft-edge-stable
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/microsoft-edge-stable
install -D -m 0644 %{SOURCE2} %{buildroot}%{_licensedir}/%{_pkgname}/LICENSE.pdf
rm %{buildroot}/opt/microsoft/%{_pkgshortname}/product_logo_*.png

%files
%license %{_licensedir}/%{_pkgname}/LICENSE.pdf
/opt/microsoft/%{_pkgshortname}
/usr/bin/microsoft-edge-stable
%{_datadir}/applications/microsoft-edge.desktop
%{_datadir}/applications/com.microsoft.Edge.desktop
%{_datadir}/appdata/microsoft-edge.appdata.xml
%{_datadir}/gnome-control-center/default-apps/microsoft-edge.xml
%{_datadir}/man/man1/microsoft-edge-stable.1.gz
%{_datadir}/man/man1/microsoft-edge.1.gz
%{_datadir}/doc/microsoft-edge-stable/changelog.gz
%{_datadir}/icons/hicolor/*/apps/%{_pkgname}.png

%changelog
* Wed Sep 30 2026 kamm3r - 154.0.4258.37-1
- Repackage the upstream Omarchy release for Fedora.
