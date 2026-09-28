Name:           python-terminaltexteffects
Version:        0.15.0
Release:        1%{?dist}
Summary:        Terminal visual effects engine for text
License:        MIT
URL:            https://github.com/ChrisBuilds/terminaltexteffects
Source0:        %{url}/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-hatchling
BuildRequires:  python3-rpm-macros
Requires:       python3
Provides:       tte = %{version}-%{release}

%description
TerminalTextEffects applies animated visual effects to text in a terminal.

%prep
%autosetup -n terminaltexteffects-release-%{version}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl
rm -f %{buildroot}%{_bindir}/terminaltexteffects

%files
%license LICENSE
%doc README.md
%{_bindir}/tte
%{python3_sitelib}/terminaltexteffects
%{python3_sitelib}/terminaltexteffects-%{version}.dist-info

%changelog
* Mon Sep 28 2026 kamm3r - 0.15.0-1
- Port the upstream Omarchy Python package to Fedora.
