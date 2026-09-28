Name:           omarchy-emacs
Version:        1.10.1
Release:        1%{?dist}
Summary:        Emacs integration with Omarchy themes and fonts
License:        MIT
URL:            https://github.com/scottjones/omarchy-emacs
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       emacs
Requires:       omarchy

%description
Configuration and helpers that synchronize Emacs fonts and themes with Omarchy.

%prep
%autosetup

%build
# Fedora ships the Wayland-capable Emacs package as emacs.
sed -i 's/omarchy-pkg-add emacs-wayland/omarchy-pkg-add emacs/' bin/omarchy-install-emacs

%install
install -D -m 0644 config/init.el %{buildroot}%{_datadir}/%{name}/config/init.el
install -D -m 0644 config/omarchy.el %{buildroot}%{_datadir}/%{name}/config/omarchy.el
install -D -m 0644 config/shell-bashrc %{buildroot}%{_datadir}/%{name}/config/shell-bashrc
install -D -m 0644 config/themes/omarchy-theme.el %{buildroot}%{_datadir}/%{name}/config/themes/omarchy-theme.el
install -D -m 0644 omarchy-colors.el.tpl %{buildroot}%{_datadir}/%{name}/omarchy-colors.el.tpl
install -D -m 0755 hooks/font-set %{buildroot}%{_datadir}/%{name}/hooks/font-set
install -D -m 0755 hooks/theme-set %{buildroot}%{_datadir}/%{name}/hooks/theme-set
for command in omarchy-emacs-setup omarchy-emacs-sync-hooks omarchy-restart-emacs omarchy-install-emacs; do
  install -D -m 0755 bin/"$command" %{buildroot}%{_bindir}/"$command"
done

%files
%license LICENSE
%doc README.md
%{_bindir}/omarchy-emacs-setup
%{_bindir}/omarchy-emacs-sync-hooks
%{_bindir}/omarchy-restart-emacs
%{_bindir}/omarchy-install-emacs
%{_datadir}/%{name}

%changelog
* Mon Sep 28 2026 kamm3r - 1.10.1-1
- Port the upstream Omarchy recipe to Fedora.
