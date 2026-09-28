%global debug_package %{nil}

Name:           tensaku
Version:        0.29.0
Release:        1%{?dist}
Summary:        Screenshot annotation tool for Wayland
License:        MPL-2.0
URL:            https://github.com/jondkinney/tensaku
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(xkbcommon)
Requires:       wl-clipboard
Requires:       hicolor-icon-theme

%description
Tensaku provides a graphical screenshot annotation editor for Wayland.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release --features ci-release

%install
install -D -m 0755 target/release/tensaku %{buildroot}%{_bindir}/tensaku
install -D -m 0755 assets/tensaku-edit %{buildroot}%{_bindir}/tensaku-edit
install -D -m 0644 dev.tensaku.Tensaku.desktop %{buildroot}%{_datadir}/applications/dev.tensaku.Tensaku.desktop
install -D -m 0644 assets/tensaku.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/dev.tensaku.Tensaku.svg
install -D -m 0644 man/tensaku.1 %{buildroot}%{_mandir}/man1/tensaku.1
install -D -m 0644 completions/tensaku.bash %{buildroot}%{_datadir}/bash-completion/completions/tensaku
install -D -m 0644 completions/tensaku.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/tensaku.fish
install -D -m 0644 completions/_tensaku %{buildroot}%{_datadir}/zsh/site-functions/_tensaku

%files
%license LICENSE NOTICE
%doc README.md
%{_bindir}/tensaku
%{_bindir}/tensaku-edit
%{_datadir}/applications/dev.tensaku.Tensaku.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.tensaku.Tensaku.svg
%{_mandir}/man1/tensaku.1*
%{_datadir}/bash-completion/completions/tensaku
%{_datadir}/fish/vendor_completions.d/tensaku.fish
%{_datadir}/zsh/site-functions/_tensaku

%changelog
* Mon Sep 28 2026 kamm3r - 0.29.0-1
- Port the upstream Omarchy screenshot editor to Fedora.
