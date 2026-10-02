%global debug_package %{nil}

Name:           omarchy-steam-fex
Version:        1.0.0
Release:        1%{?dist}
Summary:        Steam launcher with login workarounds for Apple Silicon using muvm and FEX
License:        MIT
URL:            https://github.com/omacom/omarchy-pkgs/tree/master/pkgbuilds/omarchy-steam-fex
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-steam-fex/omarchy-launch-steam#/%{name}-launcher-%{version}
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-steam-fex/LICENSE#/%{name}-LICENSE-%{version}
# Offline launcher test suite, mirroring the PKGBUILD check().
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-steam-fex/test-launcher.py#/%{name}-test-launcher-%{version}.py
ExclusiveArch:  aarch64
# The Asahi muvm/FEX-steam stack (Arch package FEX-Emu) is Fedora's fex-emu
# plus muvm; steam comes from RPM Fusion or Terra. Without the FEX launcher
# layout the script falls back to plain steam, so it stays useful.
Requires:       bash
Requires:       coreutils
Requires:       python3
Requires:       steam
Requires:       muvm
Requires:       fex-emu

%description
Omarchy-launch-steam runs Steam through muvm and FEXBash with the CEF
occlusion workaround on Apple Silicon, patching the Steam UI network
initialization block that can leave login waiting indefinitely. If the
FEX launcher layout is unavailable it falls back to plain steam.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" omarchy-launch-steam
cp "%{SOURCE1}" LICENSE
cp "%{SOURCE2}" test-launcher.py

%build
:

%check
python3 test-launcher.py

%install
install -D -m 0755 omarchy-launch-steam %{buildroot}%{_bindir}/omarchy-launch-steam
install -D -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/omarchy-launch-steam

%changelog
* Thu Oct 01 2026 kamm3r - 1.0.0-1
- Port the upstream Omarchy Apple Silicon Steam launcher to Fedora.
