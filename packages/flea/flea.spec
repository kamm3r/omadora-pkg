%global debug_package %{nil}

Name:           flea
Version:        0.3.7
Release:        1%{?dist}
Summary:        Fast, keyboard-first file manager for Omarchy
License:        MIT
URL:            https://github.com/thisisgm/flea
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
Requires:       bubblewrap
Requires:       expect
Requires:       glib2
Requires:       gvfs
Requires:       gvfs-afc
Requires:       gvfs-gphoto2
Requires:       gvfs-mtp
Requires:       gvfs-nfs
Requires:       gvfs-smb
Requires:       hicolor-icon-theme
Requires:       kf6-kimageformats
Requires:       libheif
Requires:       omarchy
Requires:       python3
Requires:       python3-gobject
Requires:       quickshell
Requires:       qt6-qtmultimedia
Requires:       qt6-qtwebengine
Requires:       shared-mime-info
Requires:       usbmuxd
Requires:       util-linux
Requires:       wl-clipboard
Requires:       xdg-terminal-exec
Requires:       xdg-utils

%description
Flea is a fast, keyboard-first file manager for Omarchy with file previews,
archive browsing, and shelf support.

%prep
%autosetup

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/flea %{buildroot}%{_bindir}/flea
install -D -m 0755 tools/flea-gio-auth %{buildroot}/usr/lib/flea/flea-gio-auth
install -D -m 0755 tools/flea-portal %{buildroot}/usr/lib/flea/flea-portal
install -D -m 0644 packaging/flea.portal %{buildroot}%{_datadir}/xdg-desktop-portal/portals/flea.portal
install -D -m 0644 packaging/org.freedesktop.impl.portal.desktop.flea.service %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.flea.service
install -D -m 0755 tools/flea-filemanager1 %{buildroot}/usr/lib/flea/flea-filemanager1
install -D -m 0644 packaging/com.thisisgm.flea.FileManager1.service %{buildroot}%{_datadir}/dbus-1/services/com.thisisgm.flea.FileManager1.service
install -D -m 0644 packaging/com.thisisgm.flea.desktop %{buildroot}%{_datadir}/applications/com.thisisgm.flea.desktop
install -D -m 0644 packaging/com.thisisgm.flea.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/com.thisisgm.flea.svg
install -D -m 0644 ui/qmldir ui/*.qml -t %{buildroot}%{_datadir}/flea/ui
install -D -m 0644 ui/js/*.js -t %{buildroot}%{_datadir}/flea/ui/js
install -D -m 0644 ui/boot/shell.qml ui/boot/picker.qml -t %{buildroot}%{_datadir}/flea/ui/boot
install -D -m 0644 shelf/manifest.json shelf/README.md shelf/*.qml shelf/*.js -t %{buildroot}%{_datadir}/flea/shelf
ln -s /usr/share/omarchy/shell/Commons %{buildroot}%{_datadir}/flea/ui/Commons
ln -s /usr/share/omarchy/shell/Ui %{buildroot}%{_datadir}/flea/ui/Ui
ln -s /usr/share/omarchy/shell/Commons %{buildroot}%{_datadir}/flea/ui/boot/Commons
ln -s /usr/share/omarchy/shell/Ui %{buildroot}%{_datadir}/flea/ui/boot/Ui

%files
%license LICENSE
%doc README.md
%{_bindir}/flea
/usr/lib/flea/flea-gio-auth
/usr/lib/flea/flea-portal
/usr/lib/flea/flea-filemanager1
%{_datadir}/xdg-desktop-portal/portals/flea.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.flea.service
%{_datadir}/dbus-1/services/com.thisisgm.flea.FileManager1.service
%{_datadir}/applications/com.thisisgm.flea.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.thisisgm.flea.svg
%{_datadir}/flea

%changelog
* Tue Oct 06 2026 kamm3r - 0.3.7-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 0.3.5-1
- Port the upstream Omarchy recipe to Fedora.
