%global debug_package %{nil}
%global __strip /bin/true
# ONNX Runtime is private to the application and must not provide system libraries.
%global __provides_exclude_from ^/usr/share/omadesign/lib/.*
%global __requires_exclude ^libonnxruntime\.so

Name:           omadesign-bin
Version:        0.6.8
Release:        1%{?dist}
Summary:        Native design, painting, photography, and motion studio
License:        MIT AND CDDL-1.0
URL:            https://github.com/michaelmonetized/omadesign
Source0:        %{url}/releases/download/v%{version}/omadesign-%{version}-x86_64-unknown-linux-gnu.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       omadesign = %{version}-%{release}
BuildRequires:  desktop-file-utils
Requires:       fontconfig
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       hicolor-icon-theme
Requires:       mesa-libGL
Requires:       mesa-libEGL
Requires:       libX11
Requires:       libXcursor
Requires:       libXi
Requires:       libXrandr
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       vulkan-loader
Requires:       libwayland-client
Requires:       libwayland-cursor
Requires:       libwayland-egl
Requires:       xdg-desktop-portal
Recommends:     ghostscript

%description
OmaDesign is a native Linux studio for design, layout, painting, photography,
and motion. This package ships the upstream binary release with its private
libraries, documentation, optional agent skills, and import plugins.

%prep
%autosetup -n omadesign-%{version}-x86_64-unknown-linux-gnu

%build
:

%check
./omadesign --version
desktop-file-validate omadesign.desktop

%install
install -D -m 0755 omadesign %{buildroot}%{_bindir}/omadesign
install -D -m 0644 omadesign.desktop %{buildroot}%{_datadir}/applications/omadesign.desktop
install -D -m 0644 omadesign.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omadesign.svg
install -D -m 0644 omadesign-mime.xml %{buildroot}%{_datadir}/mime/packages/omadesign.xml
install -d %{buildroot}%{_datadir}/omadesign
cp -a lib licenses docs skills plugins %{buildroot}%{_datadir}/omadesign/

%files
%license LICENSE LICENSE-Phosphor
%doc README.md
%{_bindir}/omadesign
%{_datadir}/applications/omadesign.desktop
%{_datadir}/icons/hicolor/scalable/apps/omadesign.svg
%{_datadir}/mime/packages/omadesign.xml
%{_datadir}/omadesign

%changelog
* Tue Oct 20 2026 kamm3r - 0.6.8-1
- Update to the release pinned in upstream 2762cded.

* Tue Oct 13 2026 kamm3r - 0.6.3-1
- Package the upstream Linux studio with its private libraries and offline assets.
