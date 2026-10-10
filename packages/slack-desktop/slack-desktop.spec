%global debug_package %{nil}
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\.so|/usr/bin/node)

Name:           slack-desktop
Version:        4.52.178
Release:        1%{?dist}
Summary:        Slack desktop client
License:        LicenseRef-proprietary
URL:            https://slack.com/downloads
%global omarchy_pkgs_commit 8787c23f0386eaf1df5ccd07b8402080da48b1ef
Source0:        https://downloads.slack-edge.com/desktop-releases/linux/x64/%{version}/slack-desktop-%{version}-amd64.deb#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/slack-desktop/slack.desktop
ExclusiveArch:  x86_64
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       fontconfig
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXrandr
Requires:       libgcc
Requires:       libnotify
Requires:       libsecret
Requires:       libxcb
Requires:       libxkbcommon
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       xdg-utils
Provides:       slack = %{version}-%{release}

%description
Slack desktop client repackaged from the vendor's x86_64 Linux release.

%prep
%setup -q -c -T -n %{name}-%{version}
data_archive=$(ar t "%{SOURCE0}" | sed -n '/^data\.tar\./p')
test -n "$data_archive"
ar p "%{SOURCE0}" "$data_archive" > "$data_archive"
tar -xf "$data_archive"
rm -f "$data_archive"

%build
:

%install
install -d %{buildroot}/usr/lib/slack
cp -a usr/lib/slack/. %{buildroot}/usr/lib/slack/
rm -rf %{buildroot}/usr/lib/slack/src
install -D -m 0644 usr/lib/slack/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
rm -f %{buildroot}/usr/lib/slack/LICENSE
install -D -m 0644 usr/share/doc/slack-desktop/OPEN_SOURCE_LICENSE_ATTRIBUTIONS \
    %{buildroot}%{_licensedir}/%{name}/OPEN_SOURCE_LICENSE_ATTRIBUTIONS
install -D -m 0644 usr/lib/slack/resources/LICENSES.chromium.html \
    %{buildroot}%{_licensedir}/%{name}/LICENSES.chromium.html
chmod -R a+rX %{buildroot}/usr/lib/slack
chmod 4755 %{buildroot}/usr/lib/slack/chrome-sandbox
install -d %{buildroot}%{_bindir}
ln -s /usr/lib/slack/slack %{buildroot}%{_bindir}/slack
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/slack.desktop
install -D -m 0644 usr/share/pixmaps/slack.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/slack.png

%files
%license %{_licensedir}/%{name}/
/usr/lib/slack
%{_bindir}/slack
%{_datadir}/applications/slack.desktop
%{_datadir}/icons/hicolor/512x512/apps/slack.png

%changelog
* Sat Oct 10 2026 kamm3r - 4.52.178-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 4.52.171-1
- Port the upstream Omarchy x86_64 Slack package to Fedora.
