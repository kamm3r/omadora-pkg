%global debug_package %{nil}
%global _lto_cflags %{nil}
%global zigver 0.16.0
%global omarchy_pkgs_commit 99aa5aa6585ed6f17dde56218d83a0a56256b112
# vendor/ghostty gitlink recorded by the v0.1.11 tag; GitHub archives leave it empty.
%global ghostty_commit 291fd050b9e9c293c8adb6a140742649b7e42d3a

Name:           herdr-app
Version:        0.1.11
Release:        1%{?dist}
Summary:        Herdr desktop app: terminals and coding agents that keep running
License:        Apache-2.0
URL:            https://github.com/herdrdev/herdr-app
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://ziglang.org/download/%{zigver}/zig-x86_64-linux-%{zigver}.tar.xz
Source2:        https://github.com/ghostty-org/ghostty/archive/%{ghostty_commit}.tar.gz#/ghostty-%{ghostty_commit}.tar.gz
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/herdr-app/herdr-app.desktop
Source4:        %{name}-vendor-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  rust
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
# The oldest core this app works with is upstream's distribution/core-version.
Requires:       herdr-core >= 0.1.11
Requires:       vulkan-loader
Recommends:     mesa-vulkan-drivers

%description
The Herdr desktop app: terminals and coding agents that keep running, on top
of herdr-core. HERDR_APP_RELEASE stays unset, so this build neither updates
itself nor sends telemetry.

%prep
%autosetup -a 4
rmdir vendor/ghostty
tar -xf "%{SOURCE2}"
mv ghostty-%{ghostty_commit} vendor/ghostty
tar -xf "%{SOURCE1}"

%build
export ZIG="$PWD/zig-x86_64-linux-%{zigver}/zig"
export ZIG_GLOBAL_CACHE_DIR="$PWD/zig-cache"
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/herdr-app %{buildroot}%{_bindir}/herdr-app
install -D -m 0644 "%{SOURCE3}" %{buildroot}%{_datadir}/applications/herdr-app.desktop
install -D -m 0644 assets/icons/herdr-ui-icon-clean.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/herdr-app.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/herdr-app.desktop

%files
%license LICENSE THIRD-PARTY-NOTICES
%{_bindir}/herdr-app
%{_datadir}/applications/herdr-app.desktop
%{_datadir}/icons/hicolor/scalable/apps/herdr-app.svg

%changelog
* Mon Nov 02 2026 kamm3r - 0.1.11-1
- Port the recipe added in upstream 99aa5aa6 to Fedora.
