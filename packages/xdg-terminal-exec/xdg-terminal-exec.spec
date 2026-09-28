Name:           xdg-terminal-exec
Version:        0.14.3
Release:        1%{?dist}
Summary:        Launch a preferred terminal for desktop applications
License:        GPL-3.0-or-later
URL:            https://gitlab.freedesktop.org/Vladimir-csp/xdg-terminal-exec
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  scdoc
BuildRequires:  bats

%description
xdg-terminal-exec chooses the configured desktop terminal for applications
that need to start inside one.

%prep
%autosetup -n xdg-terminal-exec-v%{version}

%build
%make_build

%check
make test

%install
%make_install prefix=%{_prefix}

%files
%license LICENSE
%doc README.md
%{_bindir}/xdg-terminal-exec
%{_datadir}/xdg-terminal-exec/xdg-terminals.list
%{_mandir}/man1/xdg-terminal-exec.1*

%changelog
* Mon Sep 28 2026 kamm3r - 0.14.3-1
- Port the upstream Omarchy terminal selection helper to Fedora.
