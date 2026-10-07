%global debug_package %{nil}

Name:           mise-bin
Version:        2026.10.0
Release:        1%{?dist}
Summary:        Dev tools, env vars, task runner
License:        MIT
URL:            https://github.com/jdx/mise
Source0:        %{url}/releases/download/v%{version}/mise-v%{version}-linux-x64.tar.xz#/%{name}-%{version}-linux-x64.tar.xz
Source1:        %{url}/releases/download/v%{version}/mise-v%{version}-linux-arm64.tar.xz#/%{name}-%{version}-linux-arm64.tar.xz
ExclusiveArch:  x86_64 aarch64
Provides:       mise = %{version}-%{release}

%description
Mise manages dev tools, environment variables, and tasks. This package
repacks the upstream binary release, keeping its man page and fish
activation script while disabling mise's self-updater so updates stay
managed by the package manager, mirroring the upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64) tar -xf "%{SOURCE0}" ;;
  aarch64) tar -xf "%{SOURCE1}" ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac

%build
# Completions are generated with the freshly downloaded binary, mirroring
# the upstream PKGBUILD's approach of shipping shell integration.
# (mise/bin/mise.d is PGO profile data used to build the binary; it is
# intentionally not shipped.)
mkdir -p completions
./mise/bin/mise completion bash > completions/mise.bash
./mise/bin/mise completion zsh > completions/_mise
./mise/bin/mise completion fish > completions/mise.fish

%install
install -D -m 0755 mise/bin/mise %{buildroot}%{_bindir}/mise
# Disable mise self-update (managed by the package manager).
install -D -m 0644 /dev/null %{buildroot}%{_prefix}/lib/mise/.disable-self-update
install -D -m 0644 mise/man/man1/mise.1 %{buildroot}%{_mandir}/man1/mise.1
install -D -m 0644 mise/share/fish/vendor_conf.d/mise-activate.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/mise-activate.fish
install -D -m 0644 completions/mise.bash %{buildroot}%{_datadir}/bash-completion/completions/mise
install -D -m 0644 completions/_mise %{buildroot}%{_datadir}/zsh/site-functions/_mise
install -D -m 0644 completions/mise.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/mise.fish

%files
%license mise/LICENSE
%doc mise/README.md
%{_bindir}/mise
%{_mandir}/man1/mise.1*
%{_prefix}/lib/mise/.disable-self-update
%{_datadir}/fish/vendor_conf.d/mise-activate.fish
%{_datadir}/bash-completion/completions/mise
%{_datadir}/zsh/site-functions/_mise
%{_datadir}/fish/vendor_completions.d/mise.fish

%changelog
* Tue Oct 06 2026 kamm3r - 2026.10.0-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 2026.9.14-1
- Repackage the upstream Omarchy Mise release for Fedora.
