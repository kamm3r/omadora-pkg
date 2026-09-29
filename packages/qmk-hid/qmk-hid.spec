%global debug_package %{nil}

Name:           qmk-hid
Version:        0.1.13
Release:        1%{?dist}
Summary:        Control QMK keyboards over their raw HID interface
License:        BSD-3-Clause
URL:            https://github.com/FrameworkComputer/qmk_hid
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(libudev)

%description
QMK HID is a command line tool for communicating with QMK keyboard firmware
over its raw HID interface.

%prep
%autosetup -n qmk_hid-%{version} -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release --all-features

%install
install -D -m 0755 target/release/qmk_hid %{buildroot}%{_bindir}/qmk_hid

%files
%license LICENSE.md
%doc README.md
%{_bindir}/qmk_hid

%changelog
* Mon Sep 28 2026 kamm3r - 0.1.13-1
- Port the upstream Omarchy QMK HID tool to Fedora.
