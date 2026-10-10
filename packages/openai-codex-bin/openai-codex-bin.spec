%global debug_package %{nil}

Name:           openai-codex-bin
Version:        0.162.1
Release:        1%{?dist}
Summary:        OpenAI Codex CLI
License:        Apache-2.0
URL:            https://github.com/openai/codex
Source0:        %{url}/releases/download/rust-v%{version}/codex-x86_64-unknown-linux-musl.tar.gz#/%{name}-%{version}-codex.tar.gz
Source1:        %{url}/releases/download/rust-v%{version}/codex-code-mode-host-x86_64-unknown-linux-musl.tar.gz#/%{name}-%{version}-code-mode-host.tar.gz
Source2:        https://raw.githubusercontent.com/openai/codex/rust-v%{version}/LICENSE#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64
Provides:       openai-codex = %{version}-%{release}

%description
OpenAI Codex CLI. This package repacks the upstream musl release,
including the code mode host binary and shell completions, mirroring the
upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE0}"
tar -xzf "%{SOURCE1}"
cp "%{SOURCE2}" LICENSE

%build
mkdir -p completions
./codex-x86_64-unknown-linux-musl completion bash > completions/codex.bash
./codex-x86_64-unknown-linux-musl completion zsh > completions/codex.zsh
./codex-x86_64-unknown-linux-musl completion fish > completions/codex.fish
./codex-x86_64-unknown-linux-musl completion elvish > completions/codex.elvish
./codex-x86_64-unknown-linux-musl completion powershell > completions/codex.ps1

%install
install -D -m 0755 codex-x86_64-unknown-linux-musl %{buildroot}%{_bindir}/codex
install -D -m 0755 codex-code-mode-host-x86_64-unknown-linux-musl %{buildroot}%{_bindir}/codex-code-mode-host
install -D -m 0644 completions/codex.bash %{buildroot}%{_datadir}/bash-completion/completions/codex
install -D -m 0644 completions/codex.zsh %{buildroot}%{_datadir}/zsh/site-functions/_codex
install -D -m 0644 completions/codex.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/codex.fish
install -D -m 0644 completions/codex.elvish %{buildroot}%{_datadir}/elvish/lib/codex.elv
install -D -m 0644 completions/codex.ps1 %{buildroot}%{_datadir}/powershell/Completions/codex.ps1

%files
%license LICENSE
%{_bindir}/codex
%{_bindir}/codex-code-mode-host
%{_datadir}/bash-completion/completions/codex
%{_datadir}/zsh/site-functions/_codex
%{_datadir}/fish/vendor_completions.d/codex.fish
%{_datadir}/elvish/lib/codex.elv
%{_datadir}/powershell/Completions/codex.ps1

%changelog
* Sat Oct 10 2026 kamm3r - 0.162.1-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 0.160.0-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 0.157.1-1
- Repackage the upstream Omarchy OpenAI Codex release for Fedora.
