%global go_version 1.27.1
%global debug_package %{nil}

Name:           elephant-unicode
Version:        2.22.1
Release:        1%{?dist}
Summary:        Unicode provider for elephant
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
# Go plugins only load into a core built from the identical module set.
Requires:       elephant = %{version}-%{release}
# Upstream README lists wl-clipboard (wl-copy is the default copy command).
Requires:       wl-clipboard

%description
Unicode provider for elephant. It searches unicode symbols backed by the
unicode character database and copies the selection via wl-copy.

%prep
# Shared upstream tarball: the archive root is always elephant-%{version}.
%autosetup -n elephant-%{version} -a 1
mkdir .go
tar -xzf %{SOURCE2} -C .go --strip-components=1

%build
export GOROOT=$PWD/.go PATH=$PWD/.go/bin:$PATH
export CGO_ENABLED=1 GOTOOLCHAIN=local GOFLAGS=-mod=vendor
go build -trimpath -buildmode=plugin -ldflags='-s -w' -o unicode.so ./internal/providers/unicode

%install
install -D -m 0755 unicode.so %{buildroot}%{_libdir}/elephant/unicode.so

%files
%license LICENSE
%doc README.md
%{_libdir}/elephant/unicode.so

%changelog
* Wed Sep 30 2026 kamm3r - 2.22.1-1
- Port the upstream Omarchy recipe to Fedora.
