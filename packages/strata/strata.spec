%global debug_package %{nil}

Name:           strata
Version:        0.20.1
Release:        1%{?dist}
Summary:        Fast, keyboard-first file manager for modern Linux desktops
License:        MIT
URL:            https://github.com/lgse/strata
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(graphene-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(poppler-glib)
Requires:       bubblewrap
Requires:       cairo
Requires:       ffmpeg
Requires:       ffmpegthumbnailer
Requires:       fontconfig
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       graphene
Requires:       gstreamer1-libav
Requires:       gstreamer1-plugins-good
Requires:       gvfs
Requires:       gtk4
Requires:       gtksourceview5
Requires:       hicolor-icon-theme
Requires:       pango
Requires:       poppler-glib
Requires:       util-linux
Requires:       xdg-terminal-exec

%description
Strata is a fast, keyboard-first file manager for modern Linux desktops.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
export STRATA_RELEASE_TAG="v%{version}"
export STRATA_BUILD_KIND=stable
export STRATA_BUILD_COMMIT=unknown
cargo build --frozen --release

%install
install -D -m 0755 target/release/strata %{buildroot}%{_bindir}/strata
install -D -m 0644 data/io.github.lgse.Strata.desktop %{buildroot}%{_datadir}/applications/io.github.lgse.Strata.desktop
install -D -m 0644 data/icons/scalable/apps/io.github.lgse.Strata.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
install -D -m 0644 data/io.github.lgse.Strata.FileManager1.service %{buildroot}%{_datadir}/strata/io.github.lgse.Strata.FileManager1.service

%files
%license LICENSE
%doc README.md THIRD_PARTY_LICENSES.md
%{_bindir}/strata
%{_datadir}/applications/io.github.lgse.Strata.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
%{_datadir}/strata/io.github.lgse.Strata.FileManager1.service

%changelog
* Wed Sep 30 2026 kamm3r - 0.20.1-1
- Port the upstream Omarchy recipe to Fedora.
