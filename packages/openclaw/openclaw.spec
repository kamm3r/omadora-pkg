%global debug_package %{nil}
%global __strip /bin/true
%global node_version 24.22.0

Name:           openclaw
Version:        2026.10.5
Release:        2%{?dist}
Summary:        Multi-channel AI gateway with extensible messaging integrations
License:        MIT AND LicenseRef-Nodejs-Bundled-Dependencies
URL:            https://github.com/openclaw/openclaw
Source0:        https://registry.npmjs.org/openclaw/-/openclaw-%{version}.tgz#/%{name}-%{version}.tgz
Source1:        https://nodejs.org/dist/v%{node_version}/node-v%{node_version}-linux-x64.tar.xz
Source2:        https://nodejs.org/dist/v%{node_version}/SHASUMS256.txt#/%{name}-node-SHASUMS256.txt
ExclusiveArch:  x86_64
BuildRequires:  nodejs24 >= 1:24.16.0
BuildRequires:  nodejs24-npm
Requires:       bash
Requires:       curl
Requires:       git
Recommends:     ffmpeg
Recommends:     gh
Recommends:     jq
Recommends:     ripgrep
Recommends:     tmux

%description
OpenClaw is a multi-channel AI gateway with extensible messaging
integrations. This package installs the upstream npm release with a system
launcher and a private upstream Node runtime. Fedora 44's system Node links
SQLite 3.51.2, which this OpenClaw release rejects; the private runtime keeps
that compatibility requirement isolated from other applications.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" %{name}-%{version}.tgz
expected=$(awk '$2 == "node-v%{node_version}-linux-x64.tar.xz" { print $1 }' "%{SOURCE2}")
test -n "$expected"
echo "$expected  %{SOURCE1}" | sha256sum -c -
tar -xJf "%{SOURCE1}"

%build
:

%install
mkdir -p home npm-cache node-bin
ln -s "$PWD/node-v%{node_version}-linux-x64/bin/node" node-bin/node
export PATH="$PWD/node-bin:$PATH"
export SHARP_IGNORE_GLOBAL_LIBVIPS=1
# npm 12 blocks install-time lifecycle scripts unless the package is
# allow-listed, and for a local tarball the allow-list key is the tarball's
# own file: spec (mirrors upstream). The postinstall prunes stale dist files
# and clears the .openclaw-lifecycle-pending marker the tarball ships with,
# so it gets a scratch HOME: a maintainer's own OpenClaw is not the build's
# to touch.
env -u OPENCLAW_HOME -u OPENCLAW_STATE_DIR -u OPENCLAW_CONFIG_PATH HOME="$PWD/home" \
  "$PWD/node-bin/node" /usr/lib/node_modules_24/npm/bin/npm-cli.js install --global --cache "$PWD/npm-cache" \
  --allow-scripts="file:$PWD/%{name}-%{version}.tgz" \
  --prefix "%{buildroot}%{_prefix}" "$PWD/%{name}-%{version}.tgz"
if [ -e "%{buildroot}%{_prefix}/lib/node_modules/%{name}/.openclaw-lifecycle-pending" ]; then
  echo "openclaw's postinstall did not run; the package would fail on first use" >&2
  exit 1
fi
# npm leaves a bin symlink; replace it with a wrapper for the private runtime.
rm -f "%{buildroot}%{_bindir}/openclaw"
cat > "%{buildroot}%{_bindir}/openclaw" <<'EOF'
#!/bin/sh
export SHARP_IGNORE_GLOBAL_LIBVIPS=1
export PATH="/usr/libexec/openclaw:$PATH"
exec /usr/libexec/openclaw/node /usr/lib/node_modules/openclaw/openclaw.mjs "$@"
EOF
chmod 0755 "%{buildroot}%{_bindir}/openclaw"
install -Dm755 node-v%{node_version}-linux-x64/bin/node %{buildroot}%{_libexecdir}/openclaw/node
install -Dm644 node-v%{node_version}-linux-x64/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE.node
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

%check
# The version command runs OpenClaw's SQLite capability guard. Its diagnostic
# fallback exits successfully even on an unsupported runtime, so check stderr too.
mkdir -p check-home
env -u OPENCLAW_HOME -u OPENCLAW_STATE_DIR -u OPENCLAW_CONFIG_PATH HOME="$PWD/check-home" SHARP_IGNORE_GLOBAL_LIBVIPS=1 \
  %{buildroot}%{_libexecdir}/openclaw/node %{buildroot}%{_prefix}/lib/node_modules/%{name}/openclaw.mjs --version >version.out 2>version.err
cat version.out version.err
grep -q "^OpenClaw %{version} " version.out
test ! -s version.err

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%license %{_licensedir}/%{name}/LICENSE.node
%{_libexecdir}/openclaw
%doc %{_datadir}/doc/%{name}/
%{_bindir}/openclaw
%{_prefix}/lib/node_modules/%{name}/

%changelog
* Tue Oct 20 2026 kamm3r - 2026.10.5-2
- Bundle verified upstream Node 24.22 LTS with compatible SQLite privately.
- Check OpenClaw runtime compatibility during the binary build.

* Tue Oct 20 2026 kamm3r - 2026.10.5-1
- Update to the release pinned in upstream 3e3a4343.

* Sat Oct 17 2026 kamm3r - 2026.10.4-1
- Update to the release pinned in upstream 64e8fbc2.

* Thu Oct 15 2026 kamm3r - 2026.10.3-1
- Update to the release pinned in upstream d9ebd3f6.

* Tue Oct 13 2026 kamm3r - 2026.10.2-1
- Update to the release pinned in upstream e499d021.

* Sat Oct 10 2026 kamm3r - 2026.9.9-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 2026.9.6-4
- Follow upstream master and use the packaged system CLI.
- Drop the installer payload until upstream supports seeding this release.

* Sat Oct 03 2026 kamm3r - 2026.9.6-3
- Ship upstream master's installer payload and prefer the user-owned CLI.
- Retain the system CLI until Omadora migrates existing user gateway services.
- Remove Koffi's unused musl variant from the glibc package.

* Sat Oct 03 2026 kamm3r - 2026.9.6-2
- Use the required Node 24 runtime and package native npm dependencies by arch.
- Keep npm failures visible in the build log.

* Thu Oct 01 2026 kamm3r - 2026.9.6-1
- Port the upstream Omarchy OpenClaw npm release to Fedora.
