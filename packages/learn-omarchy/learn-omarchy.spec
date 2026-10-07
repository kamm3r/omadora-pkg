Name:           learn-omarchy
Version:        0.2.5
Release:        1%{?dist}
Summary:        Interactive courses for learning the Omarchy desktop
License:        MIT AND CC-BY-4.0 AND CC0-1.0
URL:            https://github.com/DanWahlin/learn-omarchy
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  nodejs >= 22.6
Requires:       omarchy
Requires:       quickshell
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       mpv
Requires:       nodejs >= 22.6
Requires:       xdg-terminal-exec
Requires:       nautilus
Requires:       grim
Requires:       slurp
Requires:       ffmpeg
Requires:       hicolor-icon-theme

%description
Learn Omarchy provides interactive courses and practice activities for the
Omarchy desktop.

%prep
%autosetup

%build
node tools/prepare-release.mjs --check .

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%files
%license %{_datadir}/licenses/learn-omarchy
%{_bindir}/hexon-lab
%{_bindir}/learn-omarchy
%{_bindir}/learn-omarchy-validate
%{_datadir}/learn-omarchy
%{_datadir}/applications/learn-omarchy.desktop
%{_datadir}/icons/hicolor/256x256/apps/learn-omarchy.png

%changelog
* Tue Oct 06 2026 kamm3r - 0.2.5-1
- Update to the release pinned on upstream master.

* Mon Sep 28 2026 kamm3r - 0.2.4-1
- Port the upstream Omarchy learning app to Fedora.
