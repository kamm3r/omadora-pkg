%global debug_package %{nil}

Name:           github-copilot-cli
Version:        1.0.88
Release:        1%{?dist}
Summary:        GitHub Copilot CLI for the terminal
License:        LicenseRef-GitHub-Copilot
URL:            https://github.com/github/copilot-cli
Source0:        https://registry.npmjs.org/@github/copilot/-/copilot-%{version}.tgz#/%{name}-%{version}.tgz
Source1:        https://raw.githubusercontent.com/github/copilot-cli/v%{version}/changelog.md#/%{name}-CHANGELOG-%{version}.md
ExclusiveArch:  x86_64
Provides:       copilot = %{version}-%{release}
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  jq
Requires:       glib2
Requires:       glibc
Requires:       libgcc
Requires:       libsecret
Requires:       nodejs

%description
GitHub Copilot CLI brings the power of the Copilot coding agent directly
to your terminal. This package installs the upstream npm release,
mirroring the upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" copilot-%{version}.tgz
cp "%{SOURCE1}" CHANGELOG-%{version}.md

%build
:

%install
npm install -s -g \
  --cache ./npm-cache \
  --prefix "%{buildroot}%{_prefix}" \
  ./copilot-%{version}.tgz
moddir="%{buildroot}%{_prefix}/lib/node_modules/@github/copilot"
# Remove prebuilds for other platforms (x86_64 keeps linux-x64 only),
# mirroring the upstream PKGBUILD cleanup. Missing directories are no-ops.
if [ -d "$moddir/prebuilds" ]; then
  find "$moddir/prebuilds" -mindepth 1 -maxdepth 1 -type d ! -name "linux-x64" -exec rm -rf {} +
fi
if [ -d "$moddir/mxc-bin" ]; then
  find "$moddir/mxc-bin" -mindepth 1 -maxdepth 1 -type d ! -name "x64" -exec rm -rf {} +
fi
if [ -d "$moddir/ripgrep/bin" ]; then
  find "$moddir/ripgrep/bin" -mindepth 1 -maxdepth 1 -type d ! -name "linux-x64" -exec rm -rf {} +
fi
if [ -d "$moddir/clipboard/node_modules/@teddyzhu" ]; then
  find "$moddir/clipboard/node_modules/@teddyzhu" -mindepth 1 -maxdepth 1 -type d ! -name "clipboard-linux-x64-gnu" -exec rm -rf {} +
fi
if [ -d "$moddir/foundry-local-sdk/node_modules/foundry-local-sdk/prebuilds" ]; then
  find "$moddir/foundry-local-sdk/node_modules/foundry-local-sdk/prebuilds" -mindepth 1 -maxdepth 1 -type d ! -name "linux-x64" -exec rm -rf {} +
fi
if [ -d "$moddir/pvrecorder/node_modules/@picovoice/pvrecorder-node/lib" ]; then
  find "$moddir/pvrecorder/node_modules/@picovoice/pvrecorder-node/lib" -mindepth 1 -maxdepth 1 -type d ! -name 'linux' -exec rm -rf {} +
  find "$moddir/pvrecorder/node_modules/@picovoice/pvrecorder-node/lib/linux" -mindepth 1 -maxdepth 1 -type d ! -name 'x86_64' -exec rm -rf {} +
fi
find "%{buildroot}%{_prefix}" -type d -exec chmod 755 {} +
find "%{buildroot}" -name package.json -print0 | xargs -r -0 sed -i '/_where/d'
tmppackage=$(mktemp)
pkgjson="$moddir/package.json"
jq '.|=with_entries(select(.key|test("_.+")|not))' "$pkgjson" > "$tmppackage"
mv "$tmppackage" "$pkgjson"
chmod 644 "$pkgjson"
find "%{buildroot}" -type f -name package.json | while read pkgjson; do
  tmppackage=$(mktemp)
  jq 'del(.man)' "$pkgjson" > "$tmppackage"
  mv "$tmppackage" "$pkgjson"
  chmod 644 "$pkgjson"
done
"%{buildroot}%{_bindir}/copilot" completion bash > copilot
install -D -m 0644 copilot %{buildroot}%{_datadir}/bash-completion/completions/copilot
"%{buildroot}%{_bindir}/copilot" completion zsh > _copilot
install -D -m 0644 _copilot %{buildroot}%{_datadir}/zsh/site-functions/_copilot
"%{buildroot}%{_bindir}/copilot" completion fish > copilot.fish
install -D -m 0644 copilot.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/copilot.fish
cp "$moddir/LICENSE.md" LICENSE.md
cp "$moddir/README.md" README.md
cp CHANGELOG-%{version}.md CHANGELOG.md

%files
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_bindir}/copilot
%{_prefix}/lib/node_modules/@github/copilot
%{_datadir}/bash-completion/completions/copilot
%{_datadir}/zsh/site-functions/_copilot
%{_datadir}/fish/vendor_completions.d/copilot.fish

%changelog
* Wed Sep 30 2026 kamm3r - 1.0.88-1
- Port the upstream Omarchy GitHub Copilot CLI release to Fedora.
