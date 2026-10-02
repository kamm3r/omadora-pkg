%global debug_package %{nil}

Name:           crush-bin
Version:        0.96.1
Release:        1%{?dist}
Summary:        Terminal-based AI assistant for developers
License:        FSL-1.1-MIT
URL:            https://github.com/charmbracelet/crush
Source0:        %{url}/releases/download/v%{version}/crush_%{version}_Linux_x86_64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       crush = %{version}-%{release}

%description
A powerful terminal-based AI assistant for developers, providing intelligent
coding assistance directly in your terminal.

%prep
%autosetup -n crush_%{version}_Linux_x86_64

%build
:

%install
install -D -m 0755 crush %{buildroot}%{_bindir}/crush
install -D -m 0644 completions/crush.bash %{buildroot}%{_datadir}/bash-completion/completions/crush
install -D -m 0644 completions/crush.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/crush.fish
install -D -m 0644 completions/crush.zsh %{buildroot}%{_datadir}/zsh/site-functions/_crush
install -D -m 0644 manpages/crush.1.gz %{buildroot}%{_mandir}/man1/crush.1.gz

%files
%license LICENSE.md
%doc README.md
%{_bindir}/crush
%{_datadir}/bash-completion/completions/crush
%{_datadir}/fish/vendor_completions.d/crush.fish
%{_datadir}/zsh/site-functions/_crush
%{_mandir}/man1/crush.1.gz

%changelog
* Wed Sep 30 2026 kamm3r - 0.96.1-1
- Repackage the upstream Omarchy Crush release for Fedora.
