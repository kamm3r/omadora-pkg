%global debug_package %{nil}

Name:           omarchy-meeting-recorder-bin
Version:        1.6.0
Release:        1%{?dist}
Summary:        Local meeting audio recorder and transcriber
License:        MIT
URL:            https://github.com/jankeesvw/omarchy-meeting-recorder
Source0:        %{url}/releases/download/v%{version}/omarchy-meeting-recorder-%{version}-x86_64-linux.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       omarchy-meeting-recorder = %{version}-%{release}
Requires:       ffmpeg
Requires:       hicolor-icon-theme

%description
Omarchy Meeting Recorder captures microphone and computer audio for local
transcription and playback.

%prep
%autosetup -n omarchy-meeting-recorder-%{version}

%build
:

%install
install -D -m 0755 omarchy-meeting-recorder %{buildroot}%{_bindir}/omarchy-meeting-recorder
install -D -m 0644 data/omarchy-meeting-recorder.desktop %{buildroot}%{_datadir}/applications/omarchy-meeting-recorder.desktop
install -D -m 0644 data/omarchy-meeting-recorder.xml %{buildroot}%{_datadir}/mime/packages/omarchy-meeting-recorder.xml
install -D -m 0644 plugin/manifest.json %{buildroot}%{_datadir}/omarchy-meeting-recorder/plugin/manifest.json
install -D -m 0644 plugin/Widget.qml %{buildroot}%{_datadir}/omarchy-meeting-recorder/plugin/Widget.qml

%files
%license LICENSE
%doc README.md INSTALL.md
%{_bindir}/omarchy-meeting-recorder
%{_datadir}/applications/omarchy-meeting-recorder.desktop
%{_datadir}/mime/packages/omarchy-meeting-recorder.xml
%{_datadir}/omarchy-meeting-recorder/plugin

%changelog
* Sat Oct 10 2026 kamm3r - 1.6.0-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 1.5.0-1
- Update to the release pinned on upstream master.

* Mon Sep 28 2026 kamm3r - 1.4.0-1
- Repackage the upstream Omarchy Meeting Recorder release for Fedora.
