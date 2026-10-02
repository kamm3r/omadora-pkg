%global debug_package %{nil}

Name:           dbxcli-bin
Version:        3.7.4
Release:        1%{?dist}
Summary:        Command line client for Dropbox
License:        Apache-2.0
URL:            https://github.com/dropbox/dbxcli
Source0:        %{url}/releases/download/v%{version}/dbxcli_%{version}_linux_amd64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       dbxcli = %{version}-%{release}

%description
A command line client for Dropbox built using the Go SDK.

%prep
%autosetup -n dbxcli_%{version}_linux_amd64

%build
:

%install
install -D -m 0755 dbxcli %{buildroot}%{_bindir}/dbxcli
mkdir -p completions
for shell in bash fish zsh; do
  ./dbxcli completion "$shell" > "completions/dbxcli.$shell"
done
install -D -m 0644 completions/dbxcli.bash %{buildroot}%{_datadir}/bash-completion/completions/dbxcli
install -D -m 0644 completions/dbxcli.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/dbxcli.fish
install -D -m 0644 completions/dbxcli.zsh %{buildroot}%{_datadir}/zsh/site-functions/_dbxcli

%files
%license LICENSE
%doc README.md
%{_bindir}/dbxcli
%{_datadir}/bash-completion/completions/dbxcli
%{_datadir}/fish/vendor_completions.d/dbxcli.fish
%{_datadir}/zsh/site-functions/_dbxcli

%changelog
* Wed Sep 30 2026 kamm3r - 3.7.4-1
- Repackage the upstream Omarchy Dbxcli release for Fedora.
