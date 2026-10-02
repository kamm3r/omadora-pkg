%global debug_package %{nil}

Name:           schist-bin
Version:        0.15.0
Release:        1%{?dist}
Summary:        Layered image editor with PSD and Affinity support
License:        MIT
URL:            https://github.com/Infrawrench/schist
# Upstream publishes a pacman payload, not a plain tarball; it is
# extracted with tar --zstd in %prep and only its usr/ tree is packaged,
# mirroring the upstream PKGBUILD re-wrap.
Source0:        %{url}/releases/download/v%{version}/schist-%{version}-1-x86_64.pkg.tar.zst#/%{name}-%{version}.pkg.tar.zst
ExclusiveArch:  x86_64
Provides:       schist = %{version}-%{release}
BuildRequires:  zstd
Requires:       fontconfig
Requires:       freetype
Requires:       hicolor-icon-theme
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       libwayland-client
Requires:       vulkan-loader

%description
Layered image editor with PSD and Affinity support. This package
re-wraps the upstream binary release payload, mirroring the upstream
PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
tar --zstd -xf "%{SOURCE0}"

%build
:

%install
cp -a usr %{buildroot}/
mv %{buildroot}%{_datadir}/licenses/schist %{buildroot}%{_datadir}/licenses/%{name}

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/schist
%{_datadir}/applications/schist.desktop
%{_datadir}/icons/hicolor/256x256/apps/com.infrawrench.schist.png
%{_datadir}/mime/packages/com.infrawrench.schist.xml

%changelog
* Wed Sep 30 2026 kamm3r - 0.15.0-1
- Repackage the upstream Omarchy Schist release for Fedora.
