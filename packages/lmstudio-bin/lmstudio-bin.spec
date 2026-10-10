%global debug_package %{nil}
%global omarchy_pkgs_commit 8787c23f0386eaf1df5ccd07b8402080da48b1ef
%global _build 4

Name:           lmstudio-bin
Version:        0.4.26
Release:        1%{?dist}
Summary:        Desktop app for exploring and running large language models locally
License:        LicenseRef-LMStudio
URL:            https://lmstudio.ai
Source0:        https://installers.lmstudio.ai/linux/x64/%{version}-%{_build}/LM-Studio-%{version}-%{_build}-x64.AppImage#/%{name}-%{version}.AppImage
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/lmstudio-bin/lmstudio.desktop
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/lmstudio-bin/lmstudio.png
ExclusiveArch:  x86_64
Provides:       lmstudio = %{version}-%{release}
Requires:       fuse-libs
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libxcrypt-compat
Requires:       nss
Requires:       zlib

%description
LM Studio is a desktop app for exploring and running large language models
locally. This package repacks the upstream AppImage release, mirroring the
upstream PKGBUILD.

%prep
# Upstream ships a bare AppImage (plus a vendored icon and desktop entry),
# not a tarball, so there is no top directory to autosetup.
%setup -q -c -T -n %{name}-%{version}

%build
:

%install
# Install the AppImage under /opt and put a symlink on PATH, mirroring the
# upstream PKGBUILD.
install -D -m 0755 %{SOURCE0} %{buildroot}/opt/lm-studio/lm-studio.AppImage
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/lmstudio-bin.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/lmstudio-bin.png
# Desktop entry, under LM Studio's own desktop ID, which matches its window class.
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/ai.elementlabs.lmstudio.desktop
install -d %{buildroot}%{_bindir}
ln -s /opt/lm-studio/lm-studio.AppImage %{buildroot}%{_bindir}/lm-studio

%files
/opt/lm-studio/lm-studio.AppImage
%{_bindir}/lm-studio
%{_datadir}/applications/ai.elementlabs.lmstudio.desktop
%{_datadir}/icons/hicolor/512x512/apps/lmstudio-bin.png
%{_datadir}/pixmaps/lmstudio-bin.png

%changelog
* Sat Oct 10 2026 kamm3r - 0.4.26-1
- Update to the release pinned in upstream 8787c23f.

* Wed Sep 30 2026 kamm3r - 0.4.25-1
- Repackage the upstream Omarchy LM Studio release for Fedora.
