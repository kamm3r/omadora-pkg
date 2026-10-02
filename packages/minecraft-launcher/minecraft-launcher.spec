%global debug_package %{nil}
# /usr/bin/minecraft-launcher bundles its own CEF runtime plus private
# libraries. Keep those out of the RPM dependency namespace; system
# libraries stay explicitly required below.
%global __provides_exclude ^lib(cef|EGL|GLESv2|vk_swiftshader|vulkan)\\.so
%global __requires_exclude ^lib(cef|EGL|GLESv2|vk_swiftshader|vulkan)\\.so

Name:           minecraft-launcher
Version:        2.1.3
Release:        1%{?dist}
Summary:        Official Minecraft Launcher
License:        LicenseRef-Minecraft
URL:            https://mojang.com/
Epoch:          1
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://launcher.mojang.com/download/Minecraft.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://launcher.mojang.com/download/minecraft-launcher.svg#/%{name}.svg
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/minecraft-launcher/minecraft-launcher.sh
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/minecraft-launcher/minecraft-launcher.desktop
ExclusiveArch:  x86_64
Provides:       minecraft-launcher-beta = %{version}-%{release}
Conflicts:      minecraft-launcher-beta
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libgcc
Requires:       libgpg-error
Requires:       zlib

%description
The official Minecraft Launcher. This package repacks the upstream binary
release, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a tarball whose top level is minecraft-launcher, plus a
# vendored icon, wrapper script, and desktop entry, so unpack manually
# without autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE0}"
cp "%{SOURCE1}" minecraft-launcher.svg
cp "%{SOURCE2}" minecraft-launcher.sh
cp "%{SOURCE3}" minecraft-launcher.desktop

%build
:

%install
install -D -m 0755 minecraft-launcher/minecraft-launcher %{buildroot}%{_bindir}/minecraft-launcher
install -D -m 0755 minecraft-launcher.sh %{buildroot}%{_bindir}/minecraft-launcher.sh
install -D -m 0644 minecraft-launcher.desktop %{buildroot}%{_datadir}/applications/minecraft-launcher.desktop
install -D -m 0644 minecraft-launcher.svg %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/minecraft-launcher.svg

%files
%{_bindir}/minecraft-launcher
%{_bindir}/minecraft-launcher.sh
%{_datadir}/applications/minecraft-launcher.desktop
%{_datadir}/icons/hicolor/symbolic/apps/minecraft-launcher.svg

%changelog
* Thu Oct 01 2026 kamm3r - 2.1.3-1
- Repackage the upstream Omarchy release for Fedora.
