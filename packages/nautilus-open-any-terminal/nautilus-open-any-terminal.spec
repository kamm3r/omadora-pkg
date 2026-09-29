Name:           nautilus-open-any-terminal
Version:        0.8.3
Release:        1%{?dist}
Summary:        Open a chosen terminal from Nautilus
License:        GPL-3.0-or-later
URL:            https://github.com/Stunkymonkey/nautilus-open-any-terminal
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  gettext
Requires:       nautilus-python
Conflicts:      python3-nautilus-open-any-terminal

%description
Adds an action to Nautilus for opening the configured terminal in the
selected directory.

%package -n caja-open-any-terminal
Summary:        Open a chosen terminal from Caja
Requires:       %{name} = %{version}-%{release}
Requires:       python3-caja

%description -n caja-open-any-terminal
Adds the same terminal action to the Caja file manager.

%prep
%autosetup

%build
%make_build build

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install-nautilus install-caja

%files
%license LICENSE
%doc README.md
%{_datadir}/nautilus-python/extensions/nautilus_open_any_terminal.py
%{_datadir}/glib-2.0/schemas/com.github.stunkymonkey.nautilus-open-any-terminal.gschema.xml
%{_datadir}/locale/*/LC_MESSAGES/nautilus-open-any-terminal.mo

%files -n caja-open-any-terminal
%{_datadir}/caja-python/extensions/nautilus_open_any_terminal.py

%changelog
* Mon Sep 28 2026 kamm3r - 0.8.3-1
- Port the upstream Omarchy file manager terminal extension to Fedora.
