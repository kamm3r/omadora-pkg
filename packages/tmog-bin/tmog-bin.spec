%global debug_package %{nil}

Name:           tmog-bin
Version:        1.0.0
Release:        1%{?dist}
Summary:        Native system monitor and task manager
License:        LicenseRef-proprietary
URL:            https://tmog.org/
Source0:        %{url}rtm/downloads/TaskManagerOG-%{version}-linux-x86_64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       tmog = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       libgcc
Requires:       glibc
Requires:       qt6-qtbase
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       systemd-libs

%description
Native system monitor and task manager. This package repacks the vendor
Linux tarball against the system Qt, mirroring the upstream PKGBUILD.

%prep
%autosetup -n TaskManagerOG-%{version}-linux-x86_64

%build
:

%install
install -D -m 0755 bin/tmog-task-manager %{buildroot}%{_bindir}/tmog-task-manager
install -D -m 0644 share/applications/com.tmog.taskmanager.desktop %{buildroot}%{_datadir}/applications/com.tmog.taskmanager.desktop
install -D -m 0644 share/metainfo/com.tmog.taskmanager.metainfo.xml %{buildroot}%{_datadir}/metainfo/com.tmog.taskmanager.metainfo.xml
install -D -m 0644 share/pixmaps/tmog-task-manager.png %{buildroot}%{_datadir}/pixmaps/tmog-task-manager.png
for icon in share/icons/hicolor/*/apps/tmog-task-manager.png; do
  install -D -m 0644 "$icon" "%{buildroot}%{_datadir}/${icon#share/}"
done
for doc in share/doc/tmog/* share/doc/taskmanagerog/copyright; do
  install -D -m 0644 "$doc" "%{buildroot}%{_datadir}/licenses/%{name}/${doc##*/}"
done

%files
%license %{_datadir}/licenses/%{name}/*
%{_bindir}/tmog-task-manager
%{_datadir}/applications/com.tmog.taskmanager.desktop
%{_datadir}/metainfo/com.tmog.taskmanager.metainfo.xml
%{_datadir}/pixmaps/tmog-task-manager.png
%{_datadir}/icons/hicolor/*/apps/tmog-task-manager.png

%changelog
* Wed Sep 30 2026 kamm3r - 1.0.0-1
- Repackage the upstream Omarchy TMOG release for Fedora.
