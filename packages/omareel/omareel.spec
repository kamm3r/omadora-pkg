%global debug_package %{nil}

Name:           omareel
Version:        0.1.0
Release:        1%{?dist}
Summary:        Screen recorder and editor for Omarchy
License:        MIT
URL:            https://github.com/omacom/omareel
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Conflicts:      omarecord
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  libevdev-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libdrm-devel
BuildRequires:  pixman-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
Requires:       ffmpeg
Requires:       gpu-screen-recorder
Requires:       hyprland
Requires:       slurp
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme
Requires:       layer-shell-qt
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland

%description
Omareel is a screen recorder and editor for Omarchy with a synthetic
cursor, auto zooms, and a camera bubble.

%prep
%autosetup

%build
./bin/build

%install
install -D -m 0755 build/omareel %{buildroot}%{_bindir}/omareel
ln -s omareel %{buildroot}%{_bindir}/omarecord
mkdir -p %{buildroot}%{_prefix}/lib/omareel
# The capture-exclusion plugin only builds when Hyprland headers are present.
if [[ -f build/plugin/omareel-capture-exclude.so ]]; then
  install -D -m 0755 build/plugin/omareel-capture-exclude.so %{buildroot}%{_prefix}/lib/omareel/omareel-capture-exclude.so
  install -D -m 0644 build/plugin/omareel-capture-exclude.so.hash %{buildroot}%{_prefix}/lib/omareel/omareel-capture-exclude.so.hash
fi
install -D -m 0644 pkg/omareel.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omareel.svg
for size in 16 32 48 64 128 256 512; do
  install -D -m 0644 pkg/icons/omareel-$size.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/omareel.png
done
install -D -m 0644 pkg/omareel.desktop %{buildroot}%{_datadir}/applications/omareel.desktop

%files
%license LICENSE
%license LICENSES/lucide.txt
%doc README.md
%{_bindir}/omareel
%{_bindir}/omarecord
%{_prefix}/lib/omareel/
%{_datadir}/applications/omareel.desktop
%{_datadir}/icons/hicolor/scalable/apps/omareel.svg
%{_datadir}/icons/hicolor/16x16/apps/omareel.png
%{_datadir}/icons/hicolor/32x32/apps/omareel.png
%{_datadir}/icons/hicolor/48x48/apps/omareel.png
%{_datadir}/icons/hicolor/64x64/apps/omareel.png
%{_datadir}/icons/hicolor/128x128/apps/omareel.png
%{_datadir}/icons/hicolor/256x256/apps/omareel.png
%{_datadir}/icons/hicolor/512x512/apps/omareel.png

%changelog
* Wed Sep 30 2026 kamm3r - 0.1.0-1
- Port the upstream Omarchy recipe to Fedora.
