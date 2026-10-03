%global debug_package %{nil}

Name:           openclaw
Version:        2026.9.6
Release:        3%{?dist}
Summary:        Multi-channel AI gateway with extensible messaging integrations
License:        MIT
URL:            https://github.com/openclaw/openclaw
Source0:        https://registry.npmjs.org/openclaw/-/openclaw-%{version}.tgz#/%{name}-%{version}.tgz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  nodejs24 >= 1:24.16.0
BuildRequires:  nodejs24-npm
Requires:       bash
Requires:       curl
Requires:       git
Requires:       nodejs24 >= 1:24.16.0
Recommends:     ffmpeg
Recommends:     gh
Recommends:     jq
Recommends:     ripgrep
Recommends:     tmux

%description
OpenClaw is a multi-channel AI gateway with extensible messaging
integrations. This package installs the upstream npm release, mirroring the
upstream Omarchy release. It also ships the release tarball, CLI installer
and icon for a self-updating user installation. The system CLI remains as
a fallback for Omadora runtimes that predate the user-install migration.

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
# Prefer the self-updating user CLI; the system fallback uses bundled libvips.
# npm leaves a bin symlink at this path; remove it first so the wrapper
# replaces the link instead of following it.
rm -f "%{buildroot}%{_bindir}/openclaw"
cat > "%{buildroot}%{_bindir}/openclaw" <<'EOF'
#!/bin/sh
user_cli="${OPENCLAW_PREFIX:-$HOME/.openclaw}/bin/openclaw"
if [ -x "$user_cli" ] && [ "$user_cli" -ef /usr/bin/openclaw ]; then
  echo "OpenClaw user launcher points back to the system launcher" >&2
  exit 1
fi
if [ -x "$user_cli" ]; then
  exec "$user_cli" "$@"
fi
export SHARP_IGNORE_GLOBAL_LIBVIPS=1
exec node-24 /usr/lib/node_modules/openclaw/openclaw.mjs "$@"
EOF
chmod 0755 "%{buildroot}%{_bindir}/openclaw"
find "%{buildroot}%{_prefix}" -type d -exec chmod 755 {} +
moddir="%{buildroot}%{_prefix}/lib/node_modules/%{name}"
# Koffi bundles both libc variants; Fedora loads the glibc variant.
# Do not add an unavailable musl runtime dependency for the unused variant.
rm -rf "$moddir"/node_modules/@koromix/koffi-linux-*/musl_*
install -Dm644 -t "%{buildroot}%{_datadir}/licenses/%{name}/" "$moddir/LICENSE"
install -Dm644 -t "%{buildroot}%{_datadir}/doc/%{name}/" "$moddir/README.md" "$moddir/CHANGELOG.md"
for f in "$moddir"/docs/*; do
  ln -s "/usr/lib/node_modules/%{name}/docs/$(basename "$f")" "%{buildroot}%{_datadir}/doc/%{name}/"
done

# Keep the upstream master's installer payload alongside the compatibility CLI.
install -Dm644 "%{SOURCE0}" %{buildroot}%{_datadir}/%{name}/%{name}.tgz
install -Dm644 "$moddir/scripts/install-cli.sh" %{buildroot}%{_datadir}/%{name}/install-cli.sh
install -Dm644 "$moddir/dist/control-ui/apple-touch-icon.png" %{buildroot}%{_datadir}/%{name}/%{name}.png

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/
%{_bindir}/openclaw
%{_prefix}/lib/node_modules/%{name}/
%{_datadir}/%{name}/

%changelog
* Sat Oct 03 2026 kamm3r - 2026.9.6-3
- Ship upstream master's installer payload and prefer the user-owned CLI.
- Retain the system CLI until Omadora migrates existing user gateway services.
- Remove Koffi's unused musl variant from the glibc package.

* Sat Oct 03 2026 kamm3r - 2026.9.6-2
- Use the required Node 24 runtime and package native npm dependencies by arch.
- Keep npm failures visible in the build log.

* Thu Oct 01 2026 kamm3r - 2026.9.6-1
- Port the upstream Omarchy OpenClaw npm release to Fedora.
