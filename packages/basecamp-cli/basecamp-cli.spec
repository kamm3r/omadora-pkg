%global debug_package %{nil}

Name:           basecamp-cli
Version:        0.11.0
Release:        1%{?dist}
Summary:        Command line client for Basecamp
License:        MIT
URL:            https://github.com/basecamp/basecamp-cli
Source0:        %{url}/releases/download/v%{version}/basecamp_%{version}_linux_amd64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       basecamp = %{version}-%{release}

%description
The Basecamp command line client manages projects, messages, and other
Basecamp resources from a terminal.

%prep
%setup -q -c -n basecamp-cli-%{version}

%build
:

%install
install -D -m 0755 basecamp %{buildroot}%{_bindir}/basecamp
install -D -m 0644 completions/basecamp.bash %{buildroot}%{_datadir}/bash-completion/completions/basecamp
install -D -m 0644 completions/basecamp.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/basecamp.fish
install -D -m 0644 completions/_basecamp %{buildroot}%{_datadir}/zsh/site-functions/_basecamp

%files
%license MIT-LICENSE
%doc README.md
%{_bindir}/basecamp
%{_datadir}/bash-completion/completions/basecamp
%{_datadir}/fish/vendor_completions.d/basecamp.fish
%{_datadir}/zsh/site-functions/_basecamp

%changelog
* Mon Sep 28 2026 kamm3r - 0.11.0-1
- Repackage the upstream Omarchy Basecamp CLI release for Fedora.
