Name:           omakeyboard
Version:        0.1.0
Release:        1%{?dist}
Summary:        Keyboard remapping and shortcuts for Omarchy
License:        MIT
URL:            https://github.com/gabamnml/omakeyboard
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++ make desktop-file-utils
BuildRequires:  qt6-qtbase-devel qt6-qtdeclarative-devel
Requires:       hyprland
Requires:       lua
Requires:       qt6-qtwayland
Requires:       qt6-qtdeclarative
Requires:       hicolor-icon-theme
Requires:       libxkbcommon

%description
Qt Quick keyboard remapper and shortcut editor for Omarchy. Uses hyprctl
and Lua to read and apply keyboard configuration in the user's session.

%prep
%autosetup

%build
%set_build_flags
mkdir build
cd build
qmake6 ../omakeyboard.pro
%make_build

%check
./bin/test
desktop-file-validate packaging/omakeyboard.desktop

%install
install -Dm755 build/omakeyboard %{buildroot}%{_bindir}/omakeyboard
install -Dm644 packaging/omakeyboard.desktop %{buildroot}%{_datadir}/applications/omakeyboard.desktop
for size in 16 22 24 32 48 64 96 128 256 512; do
  install -Dm644 resources/icons/$size.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/omakeyboard.png
done
install -Dm644 resources/wordmark.svg %{buildroot}%{_datadir}/omakeyboard/wordmark.svg

%files
%license LICENSE
%doc README.md
%{_bindir}/omakeyboard
%{_datadir}/applications/omakeyboard.desktop
%{_datadir}/icons/hicolor/*/apps/omakeyboard.png
%{_datadir}/omakeyboard

%changelog
* Fri Oct 30 2026 kamm3r - 0.1.0-1
- Port the Qt Quick application with upstream engine and interface smoke tests.
