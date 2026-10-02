%global debug_package %{nil}

Name:           bun-bin
Version:        1.4.2
Release:        1%{?dist}
Summary:        All-in-one JavaScript runtime built for speed
License:        MIT
URL:            https://github.com/oven-sh/bun
Source0:        %{url}/releases/download/bun-v%{version}/bun-linux-x64.zip#/%{name}-%{version}.zip
Source1:        https://raw.githubusercontent.com/oven-sh/bun/bun-v%{version}/LICENSE.md#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64
Provides:       bun = %{version}-%{release}
BuildRequires:  unzip

%description
Bun is an all-in-one JavaScript runtime built for speed, with a bundler,
transpiler, test runner, and package manager. This package repacks the
upstream binary release, including the bunx symlink and shell completions.

%prep
%setup -q -c -T -n %{name}-%{version}
unzip -q "%{SOURCE0}"
cp "%{SOURCE1}" LICENSE.md

%build
# Completions are generated with the freshly downloaded binary, mirroring
# the upstream PKGBUILD's build step.
mkdir -p completions
SHELL=zsh ./bun-linux-x64/bun completions > completions/bun.zsh
SHELL=bash ./bun-linux-x64/bun completions > completions/bun.bash
SHELL=fish ./bun-linux-x64/bun completions > completions/bun.fish

%install
install -D -m 0755 bun-linux-x64/bun %{buildroot}%{_bindir}/bun
# Symlink as bunx, as in the official install.sh.
ln -s bun %{buildroot}%{_bindir}/bunx
install -D -m 0644 completions/bun.zsh %{buildroot}%{_datadir}/zsh/site-functions/_bun
install -D -m 0644 completions/bun.bash %{buildroot}%{_datadir}/bash-completion/completions/bun
install -D -m 0644 completions/bun.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/bun.fish

%files
%license LICENSE.md
%{_bindir}/bun
%{_bindir}/bunx
%{_datadir}/bash-completion/completions/bun
%{_datadir}/fish/vendor_completions.d/bun.fish
%{_datadir}/zsh/site-functions/_bun

%changelog
* Wed Sep 30 2026 kamm3r - 1.4.2-1
- Repackage the upstream Omarchy Bun release for Fedora.
