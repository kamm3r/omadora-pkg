%global debug_package %{nil}

Name:           wayfreeze
Version:        0.2.0
Release:        1%{?dist}
Summary:        Freeze the screen of a Wayland compositor
License:        AGPL-3.0-only
URL:            https://github.com/Jappie3/wayfreeze
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)

%description
Wayfreeze captures the current Wayland frame and holds it on screen while
another tool selects or annotates part of the image.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/wayfreeze %{buildroot}%{_bindir}/wayfreeze

%files
%license LICENSE
%doc README.md
%{_bindir}/wayfreeze

%changelog
* Mon Sep 28 2026 kamm3r - 0.2.0-1
- Port the upstream Omarchy Wayland screen freeze tool to Fedora.
