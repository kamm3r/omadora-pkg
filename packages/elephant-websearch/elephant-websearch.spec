%global go_version 1.27.1
%global debug_package %{nil}

Name:           elephant-websearch
Version:        2.22.1
Release:        1%{?dist}
Summary:        Websearch provider for elephant
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
# The default open command is xdg-open.
Requires:       xdg-utils

%description
Websearch provider for elephant. It searches the web through user-defined
search engines opened with xdg-open.

%prep
# Shared upstream tarball: the archive root is always elephant-%{version}.
%autosetup -n elephant-%{version} -a 1
mkdir .go
tar -xzf %{SOURCE2} -C .go --strip-components=1

%build
export GOROOT=$PWD/.go PATH=$PWD/.go/bin:$PATH
export CGO_ENABLED=1 GOTOOLCHAIN=local GOFLAGS=-mod=vendor
go build -trimpath -buildmode=plugin -ldflags='-s -w' -o websearch.so ./internal/providers/websearch

%install
install -D -m 0755 websearch.so %{buildroot}%{_libdir}/elephant/websearch.so

%files
%license LICENSE
%doc README.md
%{_libdir}/elephant/websearch.so

%changelog
* Wed Sep 30 2026 kamm3r - 2.22.1-1
- Port the upstream Omarchy recipe to Fedora.
