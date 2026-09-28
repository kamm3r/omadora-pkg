Name:           omarchy-audio-tuner
Version:        0.1.0
Release:        1%{?dist}
Summary:        Tools for authoring Omarchy laptop speaker tunings
License:        MIT
URL:            https://github.com/omacom-io/omarchy-audio-tuner
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       python3
Requires:       ffmpeg
Requires:       mpv
Requires:       pulseaudio-utils
Requires:       lsp-plugins-lv2

%description
Tools to measure, fit, generate, and compare speaker equalization profiles.

%prep
%autosetup

%build

%install
install -d %{buildroot}%{_datadir}/%{name}
cp -a measure fit generate compare %{buildroot}%{_datadir}/%{name}/
install -m 0755 omarchy-audio-tuner %{buildroot}%{_datadir}/%{name}/omarchy-audio-tuner
install -d %{buildroot}%{_bindir}
ln -s ../share/%{name}/omarchy-audio-tuner %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}

%changelog
* Mon Sep 28 2026 kamm3r - 0.1.0-1
- Port the upstream Omarchy recipe to Fedora.
