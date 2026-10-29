%global debug_package %{nil}
%global _lto_cflags %{nil}

Name:           splinterm
Version:        0.1.1
Release:        1%{?dist}
Summary:        Persistent Wayland terminal for interactive use and automation
License:        MIT
URL:            https://github.com/ministry-of-taste/splinterm
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo >= 1.88
BuildRequires:  rust >= 1.88
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
Requires:       hicolor-icon-theme
Requires:       python3
Requires:       xdg-terminal-exec
Recommends:     google-noto-sans-cjk-fonts
Recommends:     google-noto-color-emoji-fonts
Recommends:     jetbrains-mono-fonts

%description
Splinterm is a persistent Wayland terminal with a separate session daemon,
terminal launch helpers, and support for bounded automation.

%package mcp
Summary:        Policy-scoped MCP stdio adapter for Splinterm
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description mcp
An explicitly configured MCP stdio adapter for the Splinterm terminal.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
export CARGO_BUILD_JOBS=2
cargo build --frozen --release -p splinterm -p splinterd -p splinterm-relay -p splinterm-pty -p splinterm-mcp

%check
export CARGO_TARGET_DIR=target
export CARGO_BUILD_JOBS=2
cargo test --frozen --release -p splinterm-core -p splinterm-terminal --lib

%install
for bin in splinterm splinterd splinterm-relay splinterm-pty-child splinterm-mcp; do
  install -Dm755 target/release/$bin %{buildroot}%{_bindir}/$bin
done
install -Dm755 dist/bin/splinterm-xdg-terminal-exec %{buildroot}%{_bindir}/splinterm-xdg-terminal-exec
for alias in splinterm-dojos splinterm-sessions splinterm-reopen; do
  ln -s splinterm-xdg-terminal-exec %{buildroot}%{_bindir}/$alias
done
install -Dm755 tools/generate-omarchy-theme.py %{buildroot}%{_bindir}/generate-omarchy-theme.py
install -Dm755 tools/automation/splinterm-dojo-picker.py %{buildroot}%{_bindir}/splinterm-dojo-picker
ln -s splinterm-dojo-picker %{buildroot}%{_bindir}/splinterm-session-picker
id=com.oldjobobo.splinterm
install -Dm644 dist/applications/$id.desktop %{buildroot}%{_datadir}/applications/$id.desktop
install -Dm644 dist/metainfo/$id.metainfo.xml %{buildroot}%{_datadir}/metainfo/$id.metainfo.xml
install -Dm644 dist/icons/$id.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/$id.svg
install -Dm644 dist/systemd/user/splinterd.service %{buildroot}%{_userunitdir}/splinterd.service
install -Dm644 dist/systemd/user/app-splinterm.slice %{buildroot}%{_userunitdir}/app-splinterm.slice
install -Dm755 dist/omarchy/omarchy-launch-screensaver %{buildroot}%{_prefix}/lib/splinterm/integrations/omarchy-launch-screensaver
install -Dm644 dist/omarchy/screensaver.ini %{buildroot}%{_datadir}/splinterm/omarchy/screensaver.ini
mkdir -p %{buildroot}%{_docdir}/splinterm
install -m644 README.md config/splinterm/config.ini config/splinterm/theme.json dist/xdg-terminals.list docs/{packaging,headless,automation,cli,configuration,integrations,images,omarchy-tmux-reference,presets,remote,usage,accessibility}.md %{buildroot}%{_docdir}/splinterm/
install -m644 config/splinterm/presets.toml %{buildroot}%{_docdir}/splinterm/presets.example.toml
install -Dm644 docs/mcp.md %{buildroot}%{_docdir}/splinterm-mcp/mcp.md
desktop-file-validate %{buildroot}%{_datadir}/applications/$id.desktop

%files
%license LICENSE THIRD_PARTY.md
%{_bindir}/splinterm
%{_bindir}/splinterd
%{_bindir}/splinterm-relay
%{_bindir}/splinterm-pty-child
%{_bindir}/splinterm-xdg-terminal-exec
%{_bindir}/splinterm-dojos
%{_bindir}/splinterm-sessions
%{_bindir}/splinterm-reopen
%{_bindir}/splinterm-dojo-picker
%{_bindir}/splinterm-session-picker
%{_bindir}/generate-omarchy-theme.py
%{_datadir}/applications/com.oldjobobo.splinterm.desktop
%{_datadir}/metainfo/com.oldjobobo.splinterm.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/com.oldjobobo.splinterm.svg
%{_userunitdir}/splinterd.service
%{_userunitdir}/app-splinterm.slice
%{_prefix}/lib/splinterm/
%{_datadir}/splinterm/
%{_docdir}/splinterm/

%files mcp
%license LICENSE THIRD_PARTY.md
%{_bindir}/splinterm-mcp
%{_docdir}/splinterm-mcp/

%changelog
* Thu Oct 29 2026 kamm3r - 0.1.1-1
- Port the upstream terminal and optional MCP adapter to Fedora.
