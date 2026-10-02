%global debug_package %{nil}

Name:           supergfxctl
Version:        5.2.7
Release:        1%{?dist}
Summary:        Graphics switching utility for Intel/AMD iGPU and NVIDIA dGPU laptops
License:        MPL-2.0
URL:            https://gitlab.com/asus-linux/supergfxctl
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  systemd-rpm-macros
Requires:       lsof
Requires:       systemd
ExclusiveArch:  x86_64

%description
Supergfxctl switches graphics modes on Intel/AMD iGPU plus NVIDIA dGPU
laptops and provides the supergfxd system daemon.

%prep
%autosetup -a 1
# Arch drops the sudo-group D-Bus policy because dbus-broker rejects unknown
# groups by name on every bus reload; Fedora has no sudo group either and
# the wheel policy in the same file is the one that applies.
sed -i '/<policy group="sudo">/,/<\/policy>/d' data/org.supergfxctl.Daemon.conf

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release --features "daemon cli"

%install
make DESTDIR=%{buildroot} install

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/supergfxd
%{_bindir}/supergfxctl
%{_unitdir}/supergfxd.service
%{_presetdir}/supergfxd.preset
%{_datadir}/dbus-1/system.d/org.supergfxctl.Daemon.conf
%{_datadir}/X11/xorg.conf.d/90-nvidia-screen-G05.conf
%{_udevrulesdir}/90-supergfxd-nvidia-pm.rules

%changelog
* Wed Sep 30 2026 kamm3r - 5.2.7-1
- Port the upstream Omarchy recipe to Fedora.
