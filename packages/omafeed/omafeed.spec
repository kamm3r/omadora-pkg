%global debug_package %{nil}
%global _lto_cflags %{nil}

Name:           omafeed
Version:        0.2.4
Release:        1%{?dist}
Summary:        Native Rust RSS reader for Linux and Omarchy
License:        MIT
URL:            https://github.com/pch/omafeed
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo >= 1.88
BuildRequires:  rust >= 1.88
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(webkitgtk-6.0)
Requires:       hicolor-icon-theme

%description
Omafeed is a native RSS reader with a three-pane library, article list and
reading view. It supports RSS, Atom and JSON Feed, nested folders, content
filters and OPML import and export.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%check
export CARGO_TARGET_DIR=target
cargo test --frozen --workspace
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.pch.Omafeed.desktop

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} PKGNAME=%{name}
rm -rf %{buildroot}%{_datadir}/licenses/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/omafeed
%{_datadir}/applications/io.github.pch.Omafeed.desktop
%{_datadir}/metainfo/io.github.pch.Omafeed.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/io.github.pch.Omafeed.svg

%changelog
* Wed Nov 04 2026 kamm3r - 0.2.4-1
- Port the upstream recipe added in 6959cc08 to Fedora.
