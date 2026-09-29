Name:           retroarch-joypad-autoconfig-git
Version:        1.22.0.r96.g0331510
Release:        1%{?dist}
Summary:        RetroArch joypad autoconfig profiles
License:        MIT
URL:            https://github.com/libretro/retroarch-joypad-autoconfig
Source0:        %{url}/archive/033151045d378b64e712a92592467800d7924227.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Provides:       retroarch-joypad-autoconfig = %{version}-%{release}

%description
Controller profiles from RetroArch's joypad autoconfig repository, pinned to
the same upstream commit as the Omarchy package.

%prep
%autosetup -n retroarch-joypad-autoconfig-033151045d378b64e712a92592467800d7924227
rm -rf dinput mfi qnx xinput

%build
:

%install
find . -type f -iname '*.cfg' -exec install -D -m 0644 {} %{buildroot}%{_datadir}/libretro/autoconfig/{} \;

%files
%license COPYING
%doc README.md retropad_layout.png
%{_datadir}/libretro/autoconfig/

%changelog
* Tue Sep 29 2026 kamm3r - 1.22.0.r96.g0331510-1
- Port the pinned RetroArch joypad profiles to Fedora.
