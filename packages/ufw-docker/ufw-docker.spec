Name:           ufw-docker
Version:        20261029
Release:        1%{?dist}
Summary:        Docker integration for Uncomplicated Firewall
License:        GPL-3.0-only
URL:            https://github.com/chaifeng/ufw-docker
%global commit 020a8699f95592561f254d8d4ad1bb40d401dfc7
Source0:        https://github.com/chaifeng/ufw-docker/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       ufw
Requires:       docker-cli
Requires:       iptables
Requires:       diffutils
Requires:       procps-ng

%description
Manage UFW forwarding rules for Docker containers and install DOCKER-USER
chain integration. Installing this RPM does not activate or change firewall
rules; the firewall setup installs the integration explicitly.

%prep
%setup -q -n %{name}-%{commit}

%build
bash -n ufw-docker

%install
install -Dm755 ufw-docker %{buildroot}%{_bindir}/ufw-docker

%files
%license LICENSE
%doc README.md
%{_bindir}/ufw-docker

%changelog
* Thu Oct 29 2026 Omadora maintainers <packages@omadora.local> - 20261029-1
- Package pinned upstream Docker forwarding integration for UFW.
