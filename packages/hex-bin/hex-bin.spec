%global debug_package %{nil}
# Upstream ships a prebuilt, unstripped binary (PKGBUILD options=!strip).
%global __strip /bin/true
%global omarchy_pkgs_commit 99aa5aa6585ed6f17dde56218d83a0a56256b112
%global release_sha256 5541eb3fdf971813ce72a9ada04f43ea09ebb90f9545fabca648adc9b4e3349c

Name:           hex-bin
Version:        3.0.0
Release:        1%{?dist}
Summary:        Hex voice dictation app by Anomaly
License:        MIT
URL:            https://github.com/anomalyco/hex
# Release files live under their own SHA-256 from Hex's stable manifest.
Source0:        https://anoma.ly/release/hex/files/%{release_sha256}/hex#/%{name}-%{version}-linux-x64
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hex-bin/hex.desktop
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hex-bin/hex.service
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/hex-bin/LICENSE
ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
# Linked or loaded at runtime, as listed by the upstream recipe.
Requires:       alsa-lib
Requires:       curl
Requires:       libX11
Requires:       libXcursor
Requires:       libXi
Requires:       libwayland-client
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       openblas
Requires:       vulkan-loader
Recommends:     mesa-vulkan-drivers
Recommends:     wireplumber
Recommends:     wl-clipboard
Recommends:     wtype
Recommends:     xdg-utils

%description
Hex is a voice dictation app: hold a key, speak, and it types. The first run
downloads a speech model. This package repacks the upstream Linux beta binary.
It is not the hex dump tool. Start it at login with
systemctl --user enable hex.service.

%prep
%setup -q -c -T
cp "%{SOURCE3}" LICENSE

%build
:

%install
install -D -m 0755 "%{SOURCE0}" %{buildroot}%{_bindir}/hex
install -D -m 0644 "%{SOURCE1}" %{buildroot}%{_datadir}/applications/hex.desktop
install -D -m 0644 "%{SOURCE2}" %{buildroot}%{_userunitdir}/hex.service

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/hex.desktop

%files
%license LICENSE
%{_bindir}/hex
%{_datadir}/applications/hex.desktop
%{_userunitdir}/hex.service

%changelog
* Mon Nov 02 2026 kamm3r - 3.0.0-1
- Port the recipe added in upstream 99aa5aa6 to Fedora.
