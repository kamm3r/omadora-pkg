%global debug_package %{nil}

Name:           asusctl
Version:        6.5.0
Release:        1%{?dist}
Summary:        Daemon and tools to control ASUS ROG laptops
License:        MPL-2.0
URL:            https://asus-linux.org
Source0:        https://github.com/OpenGamingCollective/asusctl/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  git
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)
Requires:       systemd
Requires:       hicolor-icon-theme
ExclusiveArch:  x86_64

%description
Asusctl provides a daemon and command line tools to control many aspects
of various ASUS ROG laptops, plus the ROG Control Center graphical
interface.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/asusd %{buildroot}%{_bindir}/asusd
install -D -m 0755 target/release/asus-shutdown %{buildroot}%{_bindir}/asus-shutdown
install -D -m 0755 target/release/asusd-user %{buildroot}%{_bindir}/asusd-user
install -D -m 0755 target/release/asusctl %{buildroot}%{_bindir}/asusctl
install -D -m 0755 target/release/rog-control-center %{buildroot}%{_bindir}/rog-control-center
install -D -m 0644 data/asusd.service %{buildroot}%{_unitdir}/asusd.service
install -D -m 0644 data/asus-shutdown.service %{buildroot}%{_unitdir}/asus-shutdown.service
install -D -m 0644 data/asusd-user.service %{buildroot}%{_userunitdir}/asusd-user.service
install -D -m 0644 data/asusd.rules %{buildroot}%{_udevrulesdir}/99-asusd.rules
install -D -m 0644 data/asusd.conf %{buildroot}%{_datadir}/dbus-1/system.d/asusd.conf
install -D -m 0644 rog-aura/data/aura_support.ron %{buildroot}%{_datadir}/asusd/aura_support.ron
cp -r rog-anime/data/anime %{buildroot}%{_datadir}/asusd/
install -D -m 0644 rog-control-center/data/org.opengamingcollective.rog-control-center.desktop %{buildroot}%{_datadir}/applications/org.opengamingcollective.rog-control-center.desktop
install -D -m 0644 rog-control-center/data/org.opengamingcollective.rog-control-center.metainfo.xml %{buildroot}%{_datadir}/metainfo/org.opengamingcollective.rog-control-center.metainfo.xml
install -D -m 0644 rog-control-center/data/rog-control-center.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/rog-control-center.png
mkdir -p %{buildroot}%{_datadir}/rog-gui/layouts
cp rog-aura/data/layouts/*.ron %{buildroot}%{_datadir}/rog-gui/layouts/
install -D -m 0644 data/icons/asus_notif_yellow.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_yellow.png
install -D -m 0644 data/icons/asus_notif_green.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_green.png
install -D -m 0644 data/icons/asus_notif_blue.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_blue.png
install -D -m 0644 data/icons/asus_notif_red.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_red.png
install -D -m 0644 data/icons/asus_notif_orange.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_orange.png
install -D -m 0644 data/icons/asus_notif_white.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/asus_notif_white.png
install -D -m 0644 data/icons/scalable/gpu-compute.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/gpu-compute.svg
install -D -m 0644 data/icons/scalable/gpu-hybrid.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/gpu-hybrid.svg
install -D -m 0644 data/icons/scalable/gpu-integrated.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/gpu-integrated.svg
install -D -m 0644 data/icons/scalable/gpu-nvidia.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/gpu-nvidia.svg
install -D -m 0644 data/icons/scalable/gpu-vfio.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/gpu-vfio.svg
install -D -m 0644 data/icons/scalable/notification-reboot.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/status/notification-reboot.svg
install -D -m 0644 LICENSE %{buildroot}%{_datadir}/asusctl/LICENSE
desktop-file-validate %{buildroot}%{_datadir}/applications/org.opengamingcollective.rog-control-center.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/asusd
%{_bindir}/asus-shutdown
%{_bindir}/asusd-user
%{_bindir}/asusctl
%{_bindir}/rog-control-center
%{_unitdir}/asusd.service
%{_unitdir}/asus-shutdown.service
%{_userunitdir}/asusd-user.service
%{_udevrulesdir}/99-asusd.rules
%{_datadir}/dbus-1/system.d/asusd.conf
%{_datadir}/asusd/
%{_datadir}/asusctl/
%{_datadir}/rog-gui/
%{_datadir}/applications/org.opengamingcollective.rog-control-center.desktop
%{_datadir}/metainfo/org.opengamingcollective.rog-control-center.metainfo.xml
%{_datadir}/icons/hicolor/512x512/apps/rog-control-center.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_yellow.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_green.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_blue.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_red.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_orange.png
%{_datadir}/icons/hicolor/512x512/apps/asus_notif_white.png
%{_datadir}/icons/hicolor/scalable/status/gpu-compute.svg
%{_datadir}/icons/hicolor/scalable/status/gpu-hybrid.svg
%{_datadir}/icons/hicolor/scalable/status/gpu-integrated.svg
%{_datadir}/icons/hicolor/scalable/status/gpu-nvidia.svg
%{_datadir}/icons/hicolor/scalable/status/gpu-vfio.svg
%{_datadir}/icons/hicolor/scalable/status/notification-reboot.svg

%changelog
* Wed Sep 30 2026 kamm3r - 6.5.0-1
- Port the upstream Omarchy recipe to Fedora.
