Name:           yaru-icon-theme
Version:        26.10.3
Release:        1%{?dist}
Summary:        Yaru default Ubuntu icon theme
License:        GPL-3.0-or-later AND CC-BY-SA-4.0
URL:            https://github.com/ubuntu/yaru
Source0:        https://github.com/ubuntu/yaru/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  sassc
Requires:       hicolor-icon-theme
Requires:       gtk-update-icon-cache
Requires:       librsvg2

%description
Yaru is the default Ubuntu theme. This package ships only the icon theme
split from the upstream Omarchy recipe, which builds every Yaru component
and keeps the icons (mirrors the upstream PKGBUILD icon split).

%prep
%autosetup -n yaru-%{version}

%build
# Build only the icons component; the other Yaru components (gtk,
# gnome-shell, sounds, sessions, etc.) are skipped. Upstream enables
# ubuntu-unity and xfwm4 extras; those only add panel icons, so they stay
# off here and the icon theme keeps its default flavours.
%meson -Dicons=true -Dgtk=false -Dgnome-shell=false -Dgtksourceview=false -Dmetacity=false -Dsounds=false -Dsessions=false -Dubuntu-unity=false -Dxfwm4=false -Dcinnamon-shell=false
%meson_build

%install
%meson_install

%files
%license COPYING COPYING.LGPL-2.1 COPYING.LGPL-3.0 LICENSE_CCBYSA
%{_datadir}/icons/Yaru*

%changelog
* Thu Oct 01 2026 kamm3r - 26.10.3-1
- Port the upstream Omarchy Yaru icon theme split to Fedora.
