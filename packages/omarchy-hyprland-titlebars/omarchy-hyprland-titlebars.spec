%global debug_package %{nil}
%global _lto_cflags %{nil}
Name:           omarchy-hyprland-titlebars
Version:        0.3.0
Release:        4.omadora%{?dist}
Summary:        Titlebars for Omarchy floating workspaces
License:        BSD-3-Clause AND MIT
URL:            https://github.com/omacom/omarchy-hyprland-titlebars
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++ cmake ninja-build pkgconf-pkg-config
BuildRequires:  hyprland-devel = 0.57.0-4.omadora%{?dist}
BuildRequires:  pkgconfig(libdrm) pkgconfig(libinput) pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) pkgconfig(wayland-server) pkgconfig(xkbcommon)
# Plugin ABI must match the exact Fedora Hyprland build used for compilation.
Requires:       hyprland%{?_isa} = 0.57.0-4.omadora%{?dist}

%description
Hyprland plugin adding titlebars for Omarchy floating workspaces. It is pinned
to the exact Hyprland package build used to compile it. Rebuild this package
when updating Hyprland. Loading it is an explicit user-session action.

%prep
%autosetup

%build
%cmake -G Ninja
%cmake_build

%install
%cmake_install

%check
test -s %{buildroot}%{_prefix}/lib/%{name}/titlebars.so

%files
%license LICENSE LICENSE.MIT
%doc README.md
%{_prefix}/lib/%{name}

%changelog
* Fri Oct 30 2026 kamm3r - 0.3.0-4.omadora
- Pin the matching 0.57.0-4.omadora staged compositor and patch-specific ABI.

* Fri Oct 30 2026 kamm3r - 0.3.0-2.omadora
- Rebuild against the staged Omarchy-patched Fedora Hyprland ABI.

* Fri Oct 30 2026 kamm3r - 0.3.0-1
- Port upstream plugin against Fedora Hyprland 0.57.0-1 with exact ABI dependency.
