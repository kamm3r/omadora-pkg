%global debug_package %{nil}
%global __provides_exclude_from ^/opt/helium-browser-bin/.*$
%global __requires_exclude ^lib(EGL|GLESv2|vk_swiftshader|vulkan)\.so
%global __strip /bin/true

Name:           helium-browser-bin
Version:        0.20.2.1
Release:        1%{?dist}
Summary:        Private Chromium-based web browser
License:        GPL-3.0-only AND BSD-3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz
Source1:        https://raw.githubusercontent.com/imputnet/helium-linux/%{version}/LICENSE.ungoogled_chromium
Source2:        https://raw.githubusercontent.com/imputnet/helium-linux/%{version}/LICENSE
ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Requires:       alsa-lib
Requires:       cups-libs
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       liberation-fonts
Requires:       libXScrnSaver
Requires:       libva
Requires:       nss
Requires:       pulseaudio-libs
Requires:       systemd-libs
Requires:       xdg-utils
Recommends:     pipewire

%description
Helium is a Chromium-based web browser with privacy-oriented defaults.
This package installs the upstream Linux release and desktop launcher.

%prep
%setup -q -n helium-%{version}-x86_64_linux
sed -i 's/CHROME_VERSION_EXTRA="custom"/CHROME_VERSION_EXTRA="fedora"/' helium-wrapper
sed -i -e 's/^Exec=helium/Exec=helium-browser/' -e 's/^Icon=helium$/Icon=helium-browser/' helium.desktop
# Chromium uses the unprivileged namespace sandbox on Fedora.
if test -e chrome-sandbox; then chmod 0755 chrome-sandbox; fi

%build
:

%install
mkdir -p %{buildroot}/opt/%{name}
cp -a . %{buildroot}/opt/%{name}/
install -d %{buildroot}%{_bindir}
ln -s /opt/%{name}/helium-wrapper %{buildroot}%{_bindir}/helium-browser
install -D -m0644 helium.desktop %{buildroot}%{_datadir}/applications/helium.desktop
install -D -m0644 product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium-browser.png
install -D -m0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE.ungoogled_chromium
install -D -m0644 %{SOURCE2} %{buildroot}%{_licensedir}/%{name}/LICENSE

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/helium.desktop
test -x %{buildroot}/opt/%{name}/helium-wrapper
test -x %{buildroot}/opt/%{name}/helium

%files
%license %{_licensedir}/%{name}/*
/opt/%{name}
%{_bindir}/helium-browser
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium-browser.png

%changelog
* Thu Oct 29 2026 kamm3r - 0.20.2.1-1
- Update to the release pinned in upstream 38a5e499.

* Fri Oct 23 2026 kamm3r - 0.20.1.1-1
- Update to the release pinned in upstream 5cf42189.

* Mon Oct 19 2026 kamm3r - 0.19.4.1-1
- Port the upstream Helium browser recipe to Fedora.
