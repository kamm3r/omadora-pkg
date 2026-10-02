%global debug_package %{nil}

Name:           walker
Version:        2.17.1
Release:        1%{?dist}
Summary:        Wayland application runner
License:        GPL-3.0-or-later
URL:            https://github.com/abenz1267/walker
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  gobject-introspection-devel
BuildRequires:  protobuf-compiler
Requires:       gtk4-layer-shell
Requires:       poppler-glib
Requires:       cairo

%description
Walker is an application runner for Wayland compositors.

%prep
%autosetup -a 1

%build
export CARGO_TARGET_DIR=target
cargo build --frozen --release

%install
install -D -m 0755 target/release/walker %{buildroot}%{_bindir}/walker
install -D -m 0644 resources/config.toml %{buildroot}%{_sysconfdir}/xdg/walker/config.toml
install -D -m 0644 resources/themes/default/item.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item.xml
install -D -m 0644 resources/themes/default/item_calc.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_calc.xml
install -D -m 0644 resources/themes/default/item_clipboard.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_clipboard.xml
install -D -m 0644 resources/themes/default/item_dmenu.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_dmenu.xml
install -D -m 0644 resources/themes/default/item_files.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_files.xml
install -D -m 0644 resources/themes/default/item_providerlist.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_providerlist.xml
install -D -m 0644 resources/themes/default/item_symbols.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_symbols.xml
install -D -m 0644 resources/themes/default/item_symbols_grid.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_symbols_grid.xml
install -D -m 0644 resources/themes/default/item_archlinuxpkgs.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_archlinuxpkgs.xml
install -D -m 0644 resources/themes/default/item_dnfpackages.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_dnfpackages.xml
install -D -m 0644 resources/themes/default/item_todo.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_todo.xml
install -D -m 0644 resources/themes/default/item_unicode.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/item_unicode.xml
install -D -m 0644 resources/themes/default/layout.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/layout.xml
install -D -m 0644 resources/themes/default/keybind.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/keybind.xml
install -D -m 0644 resources/themes/default/preview.xml %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/preview.xml
install -D -m 0644 resources/themes/default/style.css %{buildroot}%{_sysconfdir}/xdg/walker/themes/default/style.css

%files
%license LICENSE
%doc README.md
%{_bindir}/walker
%{_sysconfdir}/xdg/walker/config.toml
%{_sysconfdir}/xdg/walker/themes/default/item.xml
%{_sysconfdir}/xdg/walker/themes/default/item_calc.xml
%{_sysconfdir}/xdg/walker/themes/default/item_clipboard.xml
%{_sysconfdir}/xdg/walker/themes/default/item_dmenu.xml
%{_sysconfdir}/xdg/walker/themes/default/item_files.xml
%{_sysconfdir}/xdg/walker/themes/default/item_providerlist.xml
%{_sysconfdir}/xdg/walker/themes/default/item_symbols.xml
%{_sysconfdir}/xdg/walker/themes/default/item_symbols_grid.xml
%{_sysconfdir}/xdg/walker/themes/default/item_archlinuxpkgs.xml
%{_sysconfdir}/xdg/walker/themes/default/item_dnfpackages.xml
%{_sysconfdir}/xdg/walker/themes/default/item_todo.xml
%{_sysconfdir}/xdg/walker/themes/default/item_unicode.xml
%{_sysconfdir}/xdg/walker/themes/default/layout.xml
%{_sysconfdir}/xdg/walker/themes/default/keybind.xml
%{_sysconfdir}/xdg/walker/themes/default/preview.xml
%{_sysconfdir}/xdg/walker/themes/default/style.css

%changelog
* Tue Sep 30 2026 kamm3r - 2.17.1-1
- Port the upstream Omarchy recipe to Fedora.
