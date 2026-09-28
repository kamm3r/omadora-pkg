%global debug_package %{nil}

Name:           tzupdate
Version:        3.1.0
Release:        1%{?dist}
Summary:        Set the system timezone using IP geolocation
License:        MIT
URL:            https://github.com/cdown/tzupdate
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust

%description
Tzupdate determines a timezone from an IP geolocation service and updates the
system timezone.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/tzupdate %{buildroot}%{_bindir}/tzupdate

%files
%license LICENSE
%doc README.md
%{_bindir}/tzupdate

%changelog
* Mon Sep 28 2026 kamm3r - 3.1.0-1
- Port the upstream Omarchy timezone tool to Fedora.
