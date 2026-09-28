%global debug_package %{nil}

Name:           omasnap
Version:        1.21.0
Release:        1%{?dist}
Summary:        Wayland screenshot and annotation overlay for Hyprland
License:        MIT AND OFL-1.1 AND ISC
URL:            https://github.com/omacom/omasnap
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
Requires:       hyprland
Requires:       layer-shell-qt
Requires:       tesseract
Requires:       tesseract-langpack-eng
Requires:       wl-clipboard

%description
Omasnap captures and annotates screenshots on the Hyprland desktop.

%prep
%autosetup

%build
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} -DBUILD_TESTING=ON
cmake --build build --parallel 4

%install
DESTDIR=%{buildroot} cmake --install build

%check
ctest --test-dir build --output-on-failure

%files
%license LICENSE
%doc README.md
%{_bindir}/omasnap
%{_datadir}/applications/omasnap.desktop
%{_datadir}/licenses/omasnap/*.txt

%changelog
* Mon Sep 28 2026 kamm3r - 1.21.0-1
- Port the upstream Omarchy screenshot overlay to Fedora.
