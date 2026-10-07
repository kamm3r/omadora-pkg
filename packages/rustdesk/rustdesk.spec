%global debug_package %{nil}

Name:           rustdesk
Version:        1.5.0
Release:        1%{?dist}
Summary:        Remote desktop software written in Rust
License:        AGPL-3.0-only
URL:            https://rustdesk.com/
Source0:        https://github.com/rustdesk/rustdesk/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
# The release tarball leaves the hbb_common submodule empty; pin the commit
# the upstream recipe uses. vendor-prep unpacks it before cargo vendor too.
%global hbb_commit 229b904508364c8997aad0fb5af57effac859f60
Source2:        https://github.com/rustdesk/hbb_common/archive/%{hbb_commit}.tar.gz#/hbb_common-%{hbb_commit}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(libyuv)
BuildRequires:  pkgconfig(opus)
BuildRequires:  systemd-rpm-macros
BuildRequires:  clang-libs
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  yasm
BuildRequires:  clang
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(appindicator3-0.1)
BuildRequires:  pkgconfig(atspi-2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  libxdo-devel
Requires:       xdotool
Requires:       alsa-lib
Requires:       libva
Requires:       pulseaudio-libs
Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires:       xdg-user-dirs
ExclusiveArch:  x86_64

%description
RustDesk is a remote desktop application written in Rust. It works out of
the box with no configuration required.
This Fedora port builds the default Rust workspace without the Flutter
client bundle and the vcpkg hwcodec third-party stack; see the spec file
for the full upstream Flutter plus vcpkg flow.

%prep
%autosetup -a 1
rm -rf libs/hbb_common
tar -xzf %{SOURCE2}
mv hbb_common-%{hbb_commit} libs/hbb_common

%build
export CARGO_TARGET_DIR=target
# Keep concurrent GTK/Rust compilation within the standard builder's memory.
export CARGO_BUILD_JOBS=2
# webm-sys 1.0.4 relies on an indirect cstdint include removed in GCC 16.
# Supply the header without altering the checksummed Cargo sources.
export CXXFLAGS="$CXXFLAGS -include cstdint"
OPENSSL_NO_VENDOR=1 cargo build --frozen --release --bin rustdesk --features linux-pkg-config

%install
install -D -m 0755 target/release/rustdesk %{buildroot}%{_bindir}/rustdesk
install -D -m 0644 res/rustdesk.service %{buildroot}%{_unitdir}/rustdesk.service
install -D -m 0644 res/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/rustdesk.png
install -D -m 0644 res/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/rustdesk.png
install -D -m 0644 res/128x128@2x.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/rustdesk.png
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/rustdesk.desktop <<'EOF'
[Desktop Entry]
Version=1.0
Name=RustDesk
GenericName=Remote Desktop
Comment=Remote Desktop
Exec=rustdesk %u
Icon=rustdesk
Terminal=false
Type=Application
StartupNotify=true
Categories=Network;RemoteAccess;GTK;
EOF

%files
%license LICENCE
%{_bindir}/rustdesk
%{_unitdir}/rustdesk.service
%{_datadir}/applications/rustdesk.desktop
%{_datadir}/icons/hicolor/32x32/apps/rustdesk.png
%{_datadir}/icons/hicolor/128x128/apps/rustdesk.png
%{_datadir}/icons/hicolor/256x256/apps/rustdesk.png

%changelog
* Tue Oct 06 2026 kamm3r - 1.5.0-1
- Update to the release pinned on upstream master and its hbb_common revision.
- Use current Clang with upstream bindgen and drop the retired PAM dependency.

* Sat Oct 03 2026 kamm3r - 1.4.9-2
- Use system OpenSSL and codec libraries through the upstream pkg-config feature.
- Add macros for the service path and create the desktop entry directory.
- Supply cstdint for the bundled libwebm with GCC 16.
- Use Clang 19's parser library for bindgen's VPX and AOM structs.
- Limit concurrent Rust compiler jobs on standard COPR builders.
- Build only the installed program, excluding platform helper executables.

* Wed Sep 30 2026 kamm3r - 1.4.9-1
- Port the upstream Omarchy recipe to Fedora.
