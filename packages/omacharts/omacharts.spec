%global debug_package %{nil}
%global _lto_cflags %{nil}

Name:           omacharts
Version:        0.1.10
Release:        1%{?dist}
Summary:        Charting desktop application and command line tools
License:        MIT
URL:            https://github.com/jorgemanrubia/omacharts
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5
BuildRequires:  pkgconfig(gio-2.0) >= 2.80
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
OmaCharts creates and edits charts through a GTK desktop application and
a command line interface. It also ships an optional agent skill.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release --bin omacharts

%check
cargo test --frozen --release --workspace

%install
install -D -m 0755 target/release/omacharts %{buildroot}%{_bindir}/omacharts
id=com.jorgemanrubia.Omacharts
install -D -m 0644 packaging/$id.desktop %{buildroot}%{_datadir}/applications/$id.desktop
for size in 16 24 32 48 64 128 256 512; do
  install -D -m 0644 assets/icons/${size}x${size}/$id.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/$id.png
done
install -D -m 0644 assets/icons/$id.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/$id.svg
agents=%{buildroot}%{_datadir}/%{name}/agents
install -D -m 0644 agents/.claude-plugin/plugin.json "$agents/.claude-plugin/plugin.json"
install -D -m 0644 agents/.claude-plugin/marketplace.json "$agents/.claude-plugin/marketplace.json"
install -D -m 0644 agents/skills/omacharts/SKILL.md "$agents/skills/omacharts/SKILL.md"
export DBUS_SESSION_BUS_ADDRESS=
target/release/omacharts surface --completions bash | install -D -m 0644 /dev/stdin %{buildroot}%{_datadir}/bash-completion/completions/omacharts
target/release/omacharts surface --completions zsh | install -D -m 0644 /dev/stdin %{buildroot}%{_datadir}/zsh/site-functions/_omacharts
target/release/omacharts surface --completions fish | install -D -m 0644 /dev/stdin %{buildroot}%{_datadir}/fish/vendor_completions.d/omacharts.fish
target/release/omacharts surface --man | install -D -m 0644 /dev/stdin %{buildroot}%{_mandir}/man1/omacharts.1
desktop-file-validate %{buildroot}%{_datadir}/applications/$id.desktop

%files
%license LICENSE
%doc README.md doc/cli.md
%{_bindir}/omacharts
%{_datadir}/applications/com.jorgemanrubia.Omacharts.desktop
%{_datadir}/icons/hicolor/*/apps/com.jorgemanrubia.Omacharts.*
%{_datadir}/omacharts/agents
%{_datadir}/bash-completion/completions/omacharts
%{_datadir}/zsh/site-functions/_omacharts
%{_datadir}/fish/vendor_completions.d/omacharts.fish
%{_mandir}/man1/omacharts.1*

%changelog
* Sat Oct 10 2026 kamm3r - 0.1.10-1
- Port the upstream charting application and CLI to Fedora.
