%global debug_package %{nil}

Name:           owe
Version:        0.2.9
Release:        1%{?dist}
Summary:        Wallpaper engine for Omarchy
License:        MIT
URL:            https://github.com/omacom/owe
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(mpv)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  systemd-rpm-macros
Requires:       mpv
Requires:       ffmpeg
Requires:       socat

%description
OWE renders still and video wallpapers and provides a user session daemon.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install
install -D -m 0644 systemd/owed.service %{buildroot}%{_userunitdir}/owed.service
sed -i 's|%h/.local/bin/owed|%{_bindir}/owed|' %{buildroot}%{_userunitdir}/owed.service
install -D -m 0755 hooks/owe-idle %{buildroot}%{_bindir}/owe-idle
install -D -m 0644 hooks/theme-set.d/10-owe-sync %{buildroot}%{_datadir}/owe/10-owe-sync

%files
%doc README.md
%doc config/config.toml
%{_bindir}/owe
%{_bindir}/owed
%{_bindir}/owe-render
%{_bindir}/owe-idle
%{_userunitdir}/owed.service
%{_datadir}/owe/10-owe-sync

%changelog
* Tue Oct 06 2026 kamm3r - 0.2.9-1
- Update to the release pinned on upstream master.

* Mon Sep 28 2026 kamm3r - 0.2.7-1
- Port the upstream Omarchy wallpaper engine to Fedora.
