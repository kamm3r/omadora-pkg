%global debug_package %{nil}
%global go_version 1.27.3
Name:           omarchy-speedtest
Version:        0.2.1
Release:        2%{?dist}
Summary:        Omarchy network speed test client
License:        MIT
URL:            https://github.com/omacom/omarchy-speedtest
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Fedora 44's Go 1.26 cannot compile the upstream Go 1.27 module. This pinned
# toolchain is used only during the build and is not installed in the RPM.
Source1:        https://go.dev/dl/go%{go_version}.linux-amd64.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  gcc

%description
Omarchy's command line network speed tester, installed at the upstream
private helper path for desktop integration.

%prep
%autosetup
mkdir .toolchain
tar -xf %{SOURCE1} -C .toolchain --strip-components=1

%build
%set_build_flags
export GOROOT=$PWD/.toolchain GOTOOLCHAIN=local GOCACHE=$PWD/.gocache
export CGO_ENABLED=1 GOFLAGS='-buildmode=pie -trimpath -mod=readonly -modcacherw'
$GOROOT/bin/go build -ldflags "-linkmode external -extldflags '$LDFLAGS' -X main.version=%{version}" -o omarchy-speedtest .

%check
export GOROOT=$PWD/.toolchain GOTOOLCHAIN=local GOCACHE=$PWD/.gocache
$GOROOT/bin/go test ./...

%install
install -Dm755 omarchy-speedtest %{buildroot}%{_prefix}/lib/omarchy/speedtest

%files
%license LICENSE
%{_prefix}/lib/omarchy/speedtest

%changelog
* Fri Oct 30 2026 kamm3r - 0.2.1-2
- Keep the private compiler outside Go package discovery for upstream tests.

* Fri Oct 30 2026 kamm3r - 0.2.1-1
- Port upstream release using verified Go 1.27.3 as a private build toolchain.
