%global debug_package %{nil}
%global _commit 2edbfba52780c7ace15dbb05ca92177f493d4bc9

Name:           gliff
Version:        0.1.0
Release:        1%{?dist}
Summary:        Hyprland remote desktop over SSH
License:        MIT
URL:            https://github.com/kevinmcconnell/gliff
Source0:        %{url}/archive/%{_commit}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(vulkan)
Requires:       openssh
Requires:       vulkan-loader
ExclusiveArch:  x86_64

%description
Gliff streams a Hyprland desktop over SSH using Vulkan Video with 4:4:4
color.

%prep
%autosetup -n %{name}-%{_commit} -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/gliff %{buildroot}%{_bindir}/gliff
install -D -m 0755 target/release/gliff-server %{buildroot}%{_bindir}/gliff-server
install -D -m 0755 target/release/gliff-probe %{buildroot}%{_bindir}/gliff-probe

%files
%license LICENSE
%doc README.md docs/hardware-quirks.md
%{_bindir}/gliff
%{_bindir}/gliff-server
%{_bindir}/gliff-probe

%changelog
* Tue Sep 30 2026 kamm3r - 0.1.0-1
- Port the upstream Omarchy recipe to Fedora.
