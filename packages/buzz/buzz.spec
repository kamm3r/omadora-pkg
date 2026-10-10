%global debug_package %{nil}
%global _lto_cflags %{nil}
%global pnpm_version 11.4.0
%global omarchy_pkgs_commit 8787c23f0386eaf1df5ccd07b8402080da48b1ef

Name:           buzz
Version:        0.5.28
Release:        1%{?dist}
Summary:        Desktop workspace for people and AI agents
License:        Apache-2.0
URL:            https://github.com/block/buzz
Source0:        %{url}/archive/refs/tags/desktop-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/buzz/buzz.desktop
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  nodejs24
BuildRequires:  nodejs24-npm
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       gstreamer1-plugins-good

%description
Buzz is a desktop workspace where people and AI agents collaborate through
a Nostr relay. This package includes the desktop application and its CLI
and agent helper programs.

%prep
%autosetup -n buzz-desktop-v%{version}

%build
mkdir -p node-bin
ln -s /usr/bin/node-24 node-bin/node
export PATH="$PWD/node-bin:$PATH"
export npm_config_cache="$PWD/npm-cache"
export npm_config_store_dir="$PWD/pnpm-store"
export CARGO_TARGET_DIR="$PWD/target"
export CARGO_BUILD_JOBS=%{_smp_build_ncpus}
export CMAKE_POLICY_VERSION_MINIMUM=3.5
env -u BUZZ_UPDATER_PUBLIC_KEY -u BUZZ_UPDATER_ENDPOINT \
  npm-24 exec --yes --package pnpm@%{pnpm_version} -- pnpm install --frozen-lockfile
# The lockfiles contain identical crate versions from distinct Git and
# registry sources. Cargo fetch preserves each source; a common directory
# vendor would collide. Fetch both locked graphs before the frozen builds.
cargo fetch --locked
cargo fetch --locked --manifest-path desktop/src-tauri/Cargo.toml
cargo build --frozen --release -p buzz-acp -p buzz-agent -p buzz-backend-kubernetes -p buzz-dev-mcp -p git-credential-nostr -p buzz-cli
./scripts/bundle-sidecars.sh
cd desktop
env -u BUZZ_UPDATER_PUBLIC_KEY -u BUZZ_UPDATER_ENDPOINT \
  npm-24 exec --yes --package pnpm@%{pnpm_version} -- pnpm tauri build --ci --no-bundle --features mesh-llm -- --frozen

%install
install -D -m 0755 target/release/buzz-desktop %{buildroot}%{_bindir}/buzz-desktop
for bin in buzz-acp buzz-agent buzz-backend-kubernetes buzz-dev-mcp git-credential-nostr buzz; do
  install -D -m 0755 target/release/$bin %{buildroot}%{_bindir}/$bin
done
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/buzz-desktop.desktop
for size in 32 64 128; do
  install -D -m 0644 desktop/src-tauri/icons/${size}x${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/buzz-desktop.png
done
install -D -m 0644 desktop/src-tauri/icons/128x128@2x.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/buzz-desktop.png
install -D -m 0644 desktop/src-tauri/icons/icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/buzz-desktop.png
desktop-file-validate %{buildroot}%{_datadir}/applications/buzz-desktop.desktop

%files
%license LICENSE
%{_bindir}/buzz*
%{_bindir}/git-credential-nostr
%{_datadir}/applications/buzz-desktop.desktop
%{_datadir}/icons/hicolor/*/apps/buzz-desktop.png

%changelog
* Sat Oct 10 2026 kamm3r - 0.5.28-1
- Port the upstream desktop workspace and agent helpers to Fedora.
