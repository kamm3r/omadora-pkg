%global omadots_commit 556354683664f4143776296d76df75c0fa29059a

Name:           omarchy-zsh
Version:        1.5.0
Release:        1%{?dist}
Summary:        Omarchy configuration for Zsh shell
License:        MIT
URL:            https://github.com/omacom-io/omarchy-zsh
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/omacom-io/omadots/archive/%{omadots_commit}.tar.gz#/omadots-%{omadots_commit}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       zsh
Requires:       omarchy
Requires:       eza
Requires:       mise
Requires:       zoxide
Requires:       starship
Requires:       fzf
Requires:       fd-find
Requires:       bat
Requires:       zsh-syntax-highlighting

%description
Zsh shell defaults, shared Omarchy functions, and command completion.

%prep
%autosetup -a 1

%build

%install
install -d %{buildroot}%{_datadir}/%{name}/shell
cp -a omadots-%{omadots_commit}/config/shell/. %{buildroot}%{_datadir}/%{name}/shell/
find %{buildroot}%{_datadir}/%{name}/shell -type f -exec sed -i -e 's|"\$HOME"/\.config/shell|/usr/share/omarchy-zsh/shell|g' -e 's|\$HOME/\.config/shell|/usr/share/omarchy-zsh/shell|g' {} +
install -m 0644 shell/zoptions %{buildroot}%{_datadir}/%{name}/shell/zoptions
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -m 0644 shell/completions/* %{buildroot}%{_datadir}/zsh/site-functions/
cp -a templates %{buildroot}%{_datadir}/%{name}/
install -D -m 0755 bin/omarchy-setup-zsh %{buildroot}%{_bindir}/omarchy-setup-zsh

%files
%license LICENSE
%doc README.md
%{_bindir}/omarchy-setup-zsh
%{_datadir}/%{name}
%{_datadir}/zsh/site-functions/_omarchy

%changelog
* Mon Sep 28 2026 kamm3r - 1.5.0-1
- Port the upstream Omarchy Zsh configuration to Fedora.
