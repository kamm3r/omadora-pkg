%global debug_package %{nil}
%global _lto_cflags %{nil}

Name:           wayshare
Version:        0.2.4
Release:        1%{?dist}
Summary:        macOS Screen Sharing server for Hyprland
License:        Apache-2.0
URL:            https://github.com/wesleygrimes/wayshare
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust >= 1.89
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  wayland-devel
BuildRequires:  systemd-rpm-macros
Requires:       hyprland >= 0.56
Requires:       mesa-libgbm
Requires:       mesa-libEGL
Recommends:     libva
Recommends:     x265-libs
Recommends:     pulseaudio-libs

%description
Wayshare serves a Hyprland desktop to macOS Screen Sharing clients over
Apple's screen sharing protocol, with optional hardware video encoding.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%check
cargo test --frozen --release

%install
install -Dm755 target/release/wayshare %{buildroot}%{_bindir}/wayshare
sed 's|@bindir@|%{_bindir}|' contrib/wayshare.service.in > wayshare.service
install -Dm644 wayshare.service %{buildroot}%{_userunitdir}/wayshare.service
install -Dm644 contrib/config.example.toml %{buildroot}%{_docdir}/%{name}/config.example.toml

%files
%license LICENSE
%doc README.md
%{_docdir}/%{name}/config.example.toml
%{_bindir}/wayshare
%{_userunitdir}/wayshare.service

%changelog
* Mon Oct 26 2026 kamm3r - 0.2.4-1
- Port the upstream screen sharing server with vendored Cargo dependencies.
