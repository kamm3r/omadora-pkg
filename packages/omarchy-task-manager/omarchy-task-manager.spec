Name:           omarchy-task-manager
Version:        0.1.1
Release:        1%{?dist}
Summary:        Floating native task manager for Omarchy
License:        MIT
URL:            https://github.com/tcballard/omarchy-task-manager
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
Requires:       hicolor-icon-theme
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       qt6-qtsvg

%description
Omarchy Task Manager is a floating native task manager with live process
metrics, GPU telemetry, and Hyprland integration.

%prep
%autosetup

%build
%cmake -G Ninja -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
# Ship the license via %license instead of the cmake-installed copy.
rm %{buildroot}%{_datadir}/licenses/omarchy-task-manager/LICENSE
rmdir %{buildroot}%{_datadir}/licenses/omarchy-task-manager

%files
%license LICENSE
%{_bindir}/omarchy-task-manager
# CMake installs these under the literal lib/ prefix (LIBDIR=lib upstream).
%{_prefix}/lib/omarchy-task-manager/omarchy-task-manager-core
%{_prefix}/lib/systemd/user/omarchy-task-manager-monitor.service
%{_datadir}/applications/io.github.tcballard.TaskManager.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.tcballard.TaskManager.svg
%{_datadir}/omarchy-task-manager/bindings.lua.example

%changelog
* Wed Sep 30 2026 kamm3r - 0.1.1-1
- Port the upstream Omarchy recipe to Fedora.
