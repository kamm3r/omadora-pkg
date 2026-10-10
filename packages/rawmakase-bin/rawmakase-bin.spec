%global debug_package %{nil}
%global __provides_exclude_from ^/usr/lib/rawmakase/.*
%global __requires_exclude ^lib(raw_r|lcms2|jpeg|onnxruntime)\.so

Name:           rawmakase-bin
Version:        0.2.2
Release:        1%{?dist}
Summary:        RAW photo editor compatible with Lightroom workflows
License:        MIT AND LGPL-2.1-or-later AND CDDL-1.0 AND OFL-1.1 AND Ubuntu-font-1.0 AND ISC AND BSD-3-Clause AND IJG
URL:            https://github.com/pch/rawmakase
Source0:        %{url}/releases/download/v%{version}/rawmakase-%{version}-x86_64-linux.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Provides:       rawmakase = %{version}-%{release}
Conflicts:      rawmakase
Requires:       dbus-libs
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       hicolor-icon-theme
Requires:       mesa-libGL
Requires:       mesa-libEGL
Requires:       libX11
Requires:       libxcb
Requires:       libXcursor
Requires:       libXi
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       libXrandr
Requires:       vulkan-loader
Requires:       libwayland-client
Requires:       libwayland-cursor
Requires:       libwayland-egl
Requires:       zlib
Recommends:     mesa-vulkan-drivers
Recommends:     xdg-desktop-portal

%description
Rawmakase is a GPU-accelerated RAW photo editor. This package installs the
upstream Linux release and its private processing libraries.

%prep
%setup -q -c -n %{name}-%{version}

%build
:

%install
cp -a usr %{buildroot}%{_prefix}
mv %{buildroot}%{_datadir}/licenses/rawmakase %{buildroot}%{_datadir}/licenses/%{name}
desktop-file-validate %{buildroot}%{_datadir}/applications/rawmakase.desktop

%files
%license %{_datadir}/licenses/%{name}
%{_bindir}/rawmakase
%{_prefix}/lib/rawmakase
%{_datadir}/applications/rawmakase.desktop
%{_datadir}/icons/hicolor/scalable/apps/rawmakase.svg

%changelog
* Sat Oct 10 2026 kamm3r - 0.2.2-1
- Package the upstream RAW photo editor release for Fedora.
