%global debug_package %{nil}
%global _lto_cflags %{nil}

Name:           flea
Version:        0.4.0
Release:        1%{?dist}
Summary:        Fast, keyboard-first file manager for Omarchy
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND ISC AND MIT AND MPL-2.0 AND Unicode-3.0 AND Zlib
URL:            https://github.com/thisisgm/flea
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
Requires:       bat
Requires:       bubblewrap
Requires:       expect
Requires:       fontconfig
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gvfs
Requires:       gvfs-afc
Requires:       gvfs-gphoto2
Requires:       gvfs-mtp
Requires:       gvfs-nfs
Requires:       gvfs-smb
Requires:       hicolor-icon-theme
Requires:       jq
Requires:       libglvnd-egl
Requires:       libheif
Requires:       libmpv.so.2()(64bit)
Requires:       libwayland-client
Requires:       libwayland-egl
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       omarchy
Requires:       poppler-glib
Requires:       python3
Requires:       python3-gobject
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwebengine
Requires:       quickjs-ng
Requires:       ripgrep
Requires:       shared-mime-info
Requires:       udisks2
Requires:       usbmuxd
Requires:       util-linux
Requires:       vulkan-loader
Requires:       wl-clipboard
Requires:       xdg-terminal-exec
Requires:       xdg-utils
Recommends:     mesa-vulkan-drivers
Suggests:       7zip
Suggests:       bsdtar
Suggests:       ffmpegthumbnailer
Suggests:       ImageMagick
Suggests:       libreoffice-core
Suggests:       zoxide

%description
Flea is a fast, keyboard-first file manager for Omarchy with file previews,
archive browsing, and shelf support. Its window is a native GPUI application.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release --workspace --bins

%check
./target/release/flea --version

%install
make DESTDIR=%{buildroot} VERSION=%{version}-%{release} install
# Arch's removal hook has no RPM equivalent, and the licenses are marked below.
rm -rf %{buildroot}%{_datadir}/libalpm %{buildroot}%{_datadir}/licenses/flea

%files
%license LICENSE THIRD-PARTY-LICENSES.txt
%doc README.md
%{_bindir}/flea
%{_bindir}/flea-gui
/usr/lib/flea
%{_datadir}/xdg-desktop-portal/portals/flea.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.flea.service
%{_datadir}/dbus-1/services/com.thisisgm.flea.FileManager1.service
%{_datadir}/applications/com.thisisgm.flea.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.thisisgm.flea.svg
%{_datadir}/flea

%changelog
* Wed Nov 04 2026 kamm3r - 0.4.0-1
- Update to 0.4.0, which adds the GPUI window and vendors its Cargo sources.

* Mon Oct 19 2026 kamm3r - 0.3.12-1
- Update to the release pinned in upstream de0326b9.

* Tue Oct 13 2026 kamm3r - 0.3.9-1
- Update to the release pinned in upstream e499d021.

* Sat Oct 10 2026 kamm3r - 0.3.8-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 0.3.7-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 0.3.5-1
- Port the upstream Omarchy recipe to Fedora.
