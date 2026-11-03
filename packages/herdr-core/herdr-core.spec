%global debug_package %{nil}
%global _lto_cflags %{nil}
%global zigver 0.16.0
# vendor/ghostty gitlink recorded by the v0.1.17 tag; GitHub archives leave it empty.
%global ghostty_commit 1e5cdb865807abc990181efb8ebfa9122955cce2

Name:           herdr-core
Version:        0.1.17
Release:        1%{?dist}
Summary:        Herdr core (hc): keeps Herdr terminals and coding agents running
License:        Apache-2.0
URL:            https://github.com/herdrdev/herdr-core
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://ziglang.org/download/%{zigver}/zig-x86_64-linux-%{zigver}.tar.xz
Source2:        https://github.com/ghostty-org/ghostty/archive/%{ghostty_commit}.tar.gz#/ghostty-%{ghostty_commit}.tar.gz
Source3:        %{name}-vendor-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  rust

%description
Herdr core (hc) is the server that keeps Herdr terminals and coding agents
running. A root-owned install reports the system package manager and never
updates itself.

%prep
%autosetup -a 3
rmdir vendor/ghostty
tar -xf "%{SOURCE2}"
mv ghostty-%{ghostty_commit} vendor/ghostty
tar -xf "%{SOURCE1}"

%build
export ZIG="$PWD/zig-x86_64-linux-%{zigver}/zig"
export ZIG_GLOBAL_CACHE_DIR="$PWD/zig-cache"
export CARGO_TARGET_DIR=target
cargo build --frozen --release -p herdr-core

%install
install -D -m 0755 target/release/herdr-core %{buildroot}%{_bindir}/herdr-core
ln -s herdr-core %{buildroot}%{_bindir}/hc

%files
%license LICENSE distribution/notices/*.txt
%{_bindir}/herdr-core
%{_bindir}/hc

%changelog
* Tue Nov 03 2026 kamm3r - 0.1.17-1
- Update to 0.1.17.

* Mon Nov 02 2026 kamm3r - 0.1.16-1
- Port the recipe added in upstream 99aa5aa6 to Fedora.
