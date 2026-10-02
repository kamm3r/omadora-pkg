%global debug_package %{nil}

Name:           symfony-cli
Version:        5.20.0
Release:        1%{?dist}
Summary:        Symfony client for creating and managing Symfony applications
License:        AGPL-3.0-only
URL:            https://github.com/symfony-cli/symfony-cli
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  golang >= 1.26.5
BuildRequires:  gcc

%description
The Symfony client helps developers create and manage Symfony
applications.

%prep
%autosetup -a 1

%build
export CGO_ENABLED=1 GOTOOLCHAIN=local GOFLAGS=-mod=vendor
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
go build -trimpath -buildmode=pie -ldflags="-s -w -X main.channel=stable -X main.buildDate=${DATE} -X main.version=v%{version}" -o symfony.bin .

%install
install -D -m 0755 symfony.bin %{buildroot}%{_bindir}/symfony

%files
%license LICENSE
%doc README.md
%{_bindir}/symfony

%changelog
* Wed Sep 30 2026 kamm3r - 5.20.0-1
- Port the upstream Omarchy recipe to Fedora.
