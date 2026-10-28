%global debug_package %{nil}

Name:           omarchy-screensaver
Version:        1.3.1
Release:        1%{?dist}
Summary:        Native Wayland screensaver for Omarchy
License:        MIT
URL:            https://github.com/omacom/omarchy-screensaver
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config
BuildRequires:  libxkbcommon-devel
BuildRequires:  fontconfig-devel
Requires:       fontconfig

%description
Native Wayland layer-shell screensaver with terminal text effects.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
# Omarchy's launcher dispatches to this fixed, architecture-independent path.
install -D -m 0755 target/release/omarchy-launch-screensaver %{buildroot}%{_prefix}/lib/omarchy-screensaver/omarchy-screensaver

%check
target/release/omarchy-launch-screensaver --help >/dev/null

%files
%license LICENSE
%doc README.md
%{_prefix}/lib/omarchy-screensaver/

%changelog
* Wed Oct 28 2026 kamm3r - 1.3.1-1
- Port the native Wayland screensaver to Fedora.
