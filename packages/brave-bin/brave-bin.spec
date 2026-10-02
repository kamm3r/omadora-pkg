%global debug_package %{nil}
# /opt/brave-bin bundles its own Chromium runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(vk_swiftshader|vulkan|qt.*_shim)\\.so
%global __requires_exclude ^lib(vk_swiftshader|vulkan|qt.*_shim)\\.so

Name:           brave-bin
Version:        1.96.59
Release:        1%{?dist}
Summary:        Web browser that blocks ads and trackers by default (binary release)
License:        MPL-2.0-only AND BSD-3-Clause AND LicenseRef-Chromium
URL:            https://brave.com
Epoch:          1
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://github.com/brave/brave-browser/releases/download/v%{version}/brave-browser-%{version}-linux-amd64.zip#/%{name}-%{version}.zip
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/brave-bin/brave-bin.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/brave-bin/brave-browser.desktop
ExclusiveArch:  x86_64
Provides:       brave = %{version}-%{release}
Provides:       brave-browser = %{version}-%{release}
BuildRequires:  unzip
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       fontconfig
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXScrnSaver
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXrandr
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
Brave is a web browser that blocks ads and trackers by default. This
package repacks the upstream binary release, keeping its bundled Chromium
runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a zip without a top directory, not a tarball, so there is
# no top directory to autosetup; it is unpacked with unzip.
%setup -q -c -T -n %{name}-%{version}
unzip -q "%{SOURCE0}" -d brave
chmod +x brave/brave

%build
:

%install
install -d %{buildroot}/opt
cp -a brave %{buildroot}/opt/brave-bin

# Allow firejail users to get the suid sandbox working, mirroring upstream.
chmod 4755 %{buildroot}/opt/brave-bin/chrome-sandbox

install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/brave
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/brave-browser.desktop
install -D -m 0644 brave/LICENSE %{buildroot}%{_licensedir}/brave-bin/LICENSE
for size in 16 24 32 48 64 128 256; do
  # NOTE: ${size/x*/} strips the x<size> suffix; no RPM escaping needed here.
  install -D -m 0644 brave/product_logo_${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/brave-desktop.png
done

%files
%license %{_licensedir}/brave-bin/LICENSE
/opt/brave-bin
%{_bindir}/brave
%{_datadir}/applications/brave-browser.desktop
%{_datadir}/icons/hicolor/*/apps/brave-desktop.png

%changelog
* Wed Sep 30 2026 kamm3r - 1.96.59-1
- Repackage the upstream Omarchy release for Fedora.
