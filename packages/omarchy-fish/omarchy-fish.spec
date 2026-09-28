Name:           omarchy-fish
Version:        1.5.0
Release:        1%{?dist}
Summary:        Omarchy configuration for Fish shell
License:        MIT
URL:            https://github.com/omacom-io/omarchy-fish
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/PatrickF1/fzf.fish/archive/refs/tags/v10.3.tar.gz#/fzf.fish-v10.3.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       fish
Requires:       omarchy
Requires:       eza
Requires:       mise
Requires:       zoxide
Requires:       starship
Requires:       fzf
Requires:       fd-find
Requires:       bat

%description
Fish shell defaults, functions, completions, and fzf integration for Omarchy.

%prep
%autosetup -a 1

%build
sed -i 's/sudo pacman -S tobi-try/sudo dnf install tobi-try/' functions/try.fish

%install
install -d %{buildroot}%{_datadir}/fish/vendor_conf.d
install -d %{buildroot}%{_datadir}/fish/vendor_functions.d
install -d %{buildroot}%{_datadir}/fish/vendor_completions.d
cp -a fzf.fish-10.3/conf.d/. %{buildroot}%{_datadir}/fish/vendor_conf.d/
cp -a fzf.fish-10.3/functions/. %{buildroot}%{_datadir}/fish/vendor_functions.d/
cp -a fzf.fish-10.3/completions/. %{buildroot}%{_datadir}/fish/vendor_completions.d/
cp -a conf.d/. %{buildroot}%{_datadir}/fish/vendor_conf.d/
cp -a functions/. %{buildroot}%{_datadir}/fish/vendor_functions.d/
cp -a completions/. %{buildroot}%{_datadir}/fish/vendor_completions.d/
install -d %{buildroot}%{_datadir}/%{name}
cp -a templates %{buildroot}%{_datadir}/%{name}/
install -D -m 0755 bin/omarchy-setup-fish %{buildroot}%{_bindir}/omarchy-setup-fish

%files
%license LICENSE
%license fzf.fish-10.3/LICENSE.md
%doc README.md
%{_bindir}/omarchy-setup-fish
%{_datadir}/%{name}
%{_datadir}/fish/vendor_conf.d/*
%{_datadir}/fish/vendor_functions.d/*
%{_datadir}/fish/vendor_functions.d/.*.fish
%{_datadir}/fish/vendor_completions.d/*

%changelog
* Mon Sep 28 2026 kamm3r - 1.5.0-1
- Port the upstream Omarchy Fish configuration to Fedora.
