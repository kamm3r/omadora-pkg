Name:           nautilus-dropbox
Version:        2026.05.06
Release:        1%{?dist}
Summary:        Dropbox Nautilus Extension
License:        CC-BY-ND-3.0 AND GPL-3.0-or-later
URL:            https://www.dropbox.com/
Source0:        https://github.com/dropbox/nautilus-dropbox/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnome-common
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  nautilus-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  python3-docutils
BuildRequires:  python3-gobject
Requires:       dropbox
Requires:       nautilus

%description
Dropbox extension for the Nautilus file manager. This package builds the
Nautilus extension from source, mirroring the upstream PKGBUILD, and
depends on the `dropbox` package for the daemon instead of shipping its
own copy.

%prep
%autosetup

%build
./autogen.sh --prefix=%{_prefix}
%make_build

%install
%make_install
# Depend on the `dropbox` package for the daemon, mirroring upstream.
rm %{buildroot}%{_bindir}/dropbox
rm %{buildroot}%{_datadir}/applications/dropbox.desktop
rm %{buildroot}%{_mandir}/man1/dropbox.1
# Static archive is not shipped.
rm -f %{buildroot}%{_libdir}/nautilus/extensions-*/libnautilus-dropbox.a

%files
%license COPYING
%{_libdir}/nautilus/extensions-*/libnautilus-dropbox.so
%{_datadir}/nautilus-dropbox/
%{_datadir}/icons/hicolor/*/apps/dropbox.png

%changelog
* Thu Oct 01 2026 kamm3r - 2026.05.06-1
- Port the upstream Omarchy recipe to Fedora.
