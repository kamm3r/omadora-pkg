%global go_version 1.27.1
%global debug_package %{nil}

Name:           elephant
Version:        2.22.1
Release:        1%{?dist}
Summary:        General purpose datasource and executor
License:        GPL-3.0-only
URL:            https://github.com/abenz1267/elephant
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
# Every elephant RPM builds with this same toolchain: Go plugins only load
# into a core built by the identical Go release.
Source2:        https://go.dev/dl/go%{go_version}.linux-amd64.tar.gz
# go.mod requires go >= 1.27.1 and Fedora 44 ships 1.26.x, so the upstream
# toolchain is bundled instead of BuildRequiring golang.
ExclusiveArch:  x86_64
BuildRequires:  gcc

%description
Elephant is a general purpose datasource and executor. Providers are
separate Go plugins loaded from %{_libdir}/elephant.

%prep
%autosetup -a 1
mkdir .go
tar -xzf %{SOURCE2} -C .go --strip-components=1

%build
export GOROOT=$PWD/.go PATH=$PWD/.go/bin:$PATH
export CGO_ENABLED=1 GOTOOLCHAIN=local GOFLAGS=-mod=vendor
go build -trimpath -buildmode=pie -ldflags='-s -w' -o elephant ./cmd/elephant

%install
install -D -m 0755 elephant %{buildroot}%{_bindir}/elephant

%files
%license LICENSE
%doc README.md
%{_bindir}/elephant

%changelog
* Wed Sep 30 2026 kamm3r - 2.22.1-1
- Port the upstream Omarchy recipe to Fedora.
