Name:           python-sounddevice
Version:        0.5.6
Release:        1%{?dist}
Summary:        Record and play audio through PortAudio with Python
License:        MIT
URL:            https://python-sounddevice.readthedocs.io/
Source0:        https://files.pythonhosted.org/packages/source/s/sounddevice/sounddevice-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-cffi
BuildRequires:  python3-wheel
BuildRequires:  python3-rpm-macros
Requires:       python3-cffi
Requires:       portaudio
Provides:       python3-sounddevice = %{version}-%{release}

%description
The sounddevice module records and plays audio with Python and PortAudio.

%prep
%autosetup -n sounddevice-%{version}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/sounddevice.py
%{python3_sitelib}/_sounddevice.py
%{python3_sitelib}/sounddevice-%{version}.dist-info

%changelog
* Mon Sep 28 2026 kamm3r - 0.5.6-1
- Port the upstream Omarchy Python audio module to Fedora.
