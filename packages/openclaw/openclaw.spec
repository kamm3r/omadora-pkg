%global debug_package %{nil}

Name:           openclaw
Version:        2026.9.6
Release:        2%{?dist}
Summary:        Multi-channel AI gateway with extensible messaging integrations
License:        MIT
URL:            https://github.com/openclaw/openclaw
Source0:        https://registry.npmjs.org/openclaw/-/openclaw-%{version}.tgz#/%{name}-%{version}.tgz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  nodejs24 >= 1:24.16.0
BuildRequires:  nodejs24-npm
Requires:       nodejs24 >= 1:24.16.0
Recommends:     curl
Recommends:     ffmpeg
Recommends:     gh
Recommends:     jq
Recommends:     ripgrep
Recommends:     tmux

%description
OpenClaw is a multi-channel AI gateway with extensible messaging
integrations. This package installs the upstream npm release, mirroring the
upstream Omarchy PKGBUILD (global npm install with lifecycle scripts
allow-listed, scratch HOME, and a /usr/bin wrapper).

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" %{name}-%{version}.tgz

%build
:

%install
mkdir -p home npm-cache node-bin
ln -s /usr/bin/node-24 node-bin/node
export PATH="$PWD/node-bin:$PATH"
export SHARP_IGNORE_GLOBAL_LIBVIPS=1
# npm 12 blocks install-time lifecycle scripts unless the package is
# allow-listed, and for a local tarball the allow-list key is the tarball's
# own file: spec (mirrors upstream). The postinstall prunes stale dist files
# and clears the .openclaw-lifecycle-pending marker the tarball ships with,
# so it gets a scratch HOME: a maintainer's own OpenClaw is not the build's
# to touch.
env -u OPENCLAW_HOME -u OPENCLAW_STATE_DIR -u OPENCLAW_CONFIG_PATH HOME="$PWD/home" \
  npm-24 install --global --cache "$PWD/npm-cache" \
  --allow-scripts="file:$PWD/%{name}-%{version}.tgz" \
  --prefix "%{buildroot}%{_prefix}" "$PWD/%{name}-%{version}.tgz"
if [ -e "%{buildroot}%{_prefix}/lib/node_modules/%{name}/.openclaw-lifecycle-pending" ]; then
  echo "openclaw's postinstall did not run; the package would fail on first use" >&2
  exit 1
fi
# Wrapper is verbatim from the upstream PKGBUILD: keep Sharp on its bundled
# libvips and exec the gateway entry point with the system node.
# npm leaves a bin symlink at this path; remove it first so the wrapper
# replaces the link instead of following it.
rm -f "%{buildroot}%{_bindir}/openclaw"
cat > "%{buildroot}%{_bindir}/openclaw" <<'EOF'
#!/bin/sh
export SHARP_IGNORE_GLOBAL_LIBVIPS=1
exec node-24 /usr/lib/node_modules/openclaw/openclaw.mjs "$@"
EOF
chmod 0755 "%{buildroot}%{_bindir}/openclaw"
find "%{buildroot}%{_prefix}" -type d -exec chmod 755 {} +
moddir="%{buildroot}%{_prefix}/lib/node_modules/%{name}"
install -Dm644 -t "%{buildroot}%{_datadir}/licenses/%{name}/" "$moddir/LICENSE"
install -Dm644 -t "%{buildroot}%{_datadir}/doc/%{name}/" "$moddir/README.md" "$moddir/CHANGELOG.md"
for f in "$moddir"/docs/*; do
  ln -s "/usr/lib/node_modules/%{name}/docs/$(basename "$f")" "%{buildroot}%{_datadir}/doc/%{name}/"
done

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/
%{_bindir}/openclaw
%{_prefix}/lib/node_modules/%{name}/

%changelog
* Sat Oct 03 2026 kamm3r - 2026.9.6-2
- Use the required Node 24 runtime and package native npm dependencies by arch.
- Keep npm failures visible in the build log.

* Thu Oct 01 2026 kamm3r - 2026.9.6-1
- Port the upstream Omarchy OpenClaw npm release to Fedora.
