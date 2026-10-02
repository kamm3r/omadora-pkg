%global debug_package %{nil}
# Upstream binary carries a build-tree RUNPATH; this is a binary repack so
# the RPATH QA check is skipped (mirrors other binary-only Fedora packs).
%undefine __brp_check_rpaths
# /opt/bambustudio-bin bundles its own ffmpeg libraries. Keep those out of
# the RPM dependency namespace; system libraries stay explicitly required
# below.
%global __provides_exclude ^lib(avcodec|avutil|swresample|swscale).*\\.so
%global __requires_exclude ^lib(avcodec|avutil|swresample|swscale).*\\.so

Name:           bambustudio-bin
Version:        02.08.02.61
Release:        1%{?dist}
Summary:        PC Software for BambuLab's 3D printers
License:        AGPL-3.0-only
URL:            https://github.com/bambulab/BambuStudio
%global _build 20260820225108
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://github.com/bambulab/BambuStudio/releases/download/v%{version}/BambuStudio_ubuntu24.04-v%{version}-%{_build}.AppImage#/%{name}-%{version}.AppImage
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/bambustudio-bin/BambuStudio.desktop
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/bambustudio-bin/bambu-studio
ExclusiveArch:  x86_64
Provides:       bambustudio = %{version}-%{release}
BuildRequires:  7zip
Requires:       cairo
Requires:       dbus-libs
Requires:       fontconfig
Requires:       glib2
Requires:       glibc
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libgcc
Requires:       libglvnd
Requires:       libstdc++
Requires:       mesa-libGL
Requires:       pango
Requires:       libwayland-client
Requires:       webkit2gtk4.1

%description
Bambu Studio is PC software for BambuLab's 3D printers. This package
repacks the upstream AppImage release, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a bare AppImage (plus a vendored desktop entry and launcher),
# not a tarball, so there is no top directory to autosetup; it is extracted
# with 7z in %install after sources are available.
%setup -q -c -T -n %{name}-%{version}

%build
:

%install
# Read the embedded SquashFS without executing the AppImage, mirroring the
# upstream PKGBUILD's prepare step.
7z x "%{SOURCE0}" -osquashfs-root > /dev/null
cd squashfs-root
install -D -m 0755 AppRun %{buildroot}/opt/%{name}/AppRun
cp -a bin resources %{buildroot}/opt/%{name}/

for icon in usr/share/icons/hicolor/*/apps/BambuStudio.png; do
  size="${icon#usr/share/icons/hicolor/}"
  install -D -m 0644 "$icon" "%{buildroot}%{_datadir}/icons/hicolor/${size}"
done

install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/bambu-studio
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/BambuStudio.desktop

%files
/opt/%{name}
%{_bindir}/bambu-studio
%{_datadir}/applications/BambuStudio.desktop
%{_datadir}/icons/hicolor/*/apps/BambuStudio.png

%changelog
* Wed Sep 30 2026 kamm3r - 02.08.02.61-1
- Repackage the upstream Omarchy release for Fedora.
