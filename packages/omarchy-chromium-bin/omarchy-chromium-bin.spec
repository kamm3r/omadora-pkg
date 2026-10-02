%global debug_package %{nil}
# /usr/lib/chromium bundles its own runtime plus private libraries. Keep
# those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|vk_swiftshader|vulkan|qt6_shim)\\.so
%global __requires_exclude ^lib(EGL|GLESv2|vk_swiftshader|vulkan|qt6_shim)\\.so

Name:           omarchy-chromium-bin
Version:        148.0.7778.96
Release:        1%{?dist}
Summary:        Web browser built for speed, simplicity, and security, with patches for Omarchy (binary package)
License:        BSD-3-Clause
URL:            https://www.chromium.org/Home
# Upstream release revision (the -<build> suffix on the release tag).
# Bump Release when _build increases at the same Version.
%global _build 21
Source0:        https://github.com/omacom-io/omarchy-chromium/releases/download/v%{version}-%{_build}/omarchy-chromium-%{version}-%{_build}-x86_64.pkg.tar.zst#/%{name}-%{version}-%{_build}-x86_64.pkg.tar.zst
Source1:        https://github.com/omacom-io/omarchy-chromium/releases/download/v%{version}-%{_build}/omarchy-chromium-%{version}-%{_build}-aarch64.pkg.tar.zst#/%{name}-%{version}-%{_build}-aarch64.pkg.tar.zst
ExclusiveArch:  x86_64 aarch64
BuildRequires:  zstd
Provides:       chromium = %{version}-%{release}
Conflicts:      chromium
Conflicts:      omarchy-chromium
Requires:       alsa-lib
Requires:       cups-libs
Requires:       dbus-libs
Requires:       desktop-file-utils
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       liberation-sans-fonts
Requires:       libXScrnSaver
Requires:       libffi
Requires:       libgcrypt
Requires:       libva
Requires:       nss
Requires:       pciutils
Requires:       pulseaudio-libs
Requires:       systemd-libs
Requires:       xdg-utils

%description
Chromium with patches for Omarchy. This package repacks the upstream
binary release, mirroring the upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64) tar -xf "%{SOURCE0}" ;;
  aarch64) tar -xf "%{SOURCE1}" ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac

%build
:

%install
# The Arch payload (usr/bin, usr/lib/chromium, usr/share) is copied
# verbatim like the PKGBUILD does. The launcher hardcodes
# /usr/lib/chromium, so the lib tree keeps that path instead of %%{_libdir}.
cp -a usr %{buildroot}/

%files
%license %{_datadir}/licenses/chromium/LICENSE
%license %{_datadir}/licenses/chromium/LICENSE.launcher
%{_bindir}/chromium
%{_bindir}/chromedriver
%{_prefix}/lib/chromium/
%{_datadir}/applications/chromium.desktop
%{_datadir}/icons/hicolor/*/apps/chromium.png
%{_datadir}/man/man1/chromium.1.gz
%{_datadir}/metainfo/chromium.appdata.xml

%changelog
* Thu Oct 01 2026 kamm3r - 148.0.7778.96-1
- Repackage the upstream Omarchy Chromium release for Fedora.
