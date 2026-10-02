Name:           dropbox-cli
Version:        2026.05.06
Release:        1%{?dist}
Summary:        Command line interface for Dropbox
License:        GPL-3.0-or-later
URL:            https://www.dropbox.com
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://linux.dropbox.com/packages/nautilus-dropbox-%{version}.tar.bz2#/%{name}-%{version}.tar.bz2
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/dropbox-cli/dropboxd-fallback.patch
BuildArch:      noarch
BuildRequires:  python3
Requires:       dropbox
Requires:       python3-gobject

%description
Command line interface for Dropbox. This package builds the dropbox
frontend script from the upstream nautilus-dropbox sources, mirroring the
upstream PKGBUILD.

%prep
%setup -q -n nautilus-dropbox-%{version}
# Point to /opt/dropbox/dropboxd when the user dist path does not exist,
# mirroring the upstream PKGBUILD patch.
patch -Np1 -i "%{SOURCE1}"

%build
python3 build_dropbox.py "%{version}" "/usr/share/applications" < "dropbox.in" > "%{name}"

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license COPYING
%{_bindir}/%{name}

%changelog
* Thu Oct 01 2026 kamm3r - 2026.05.06-1
- Port the upstream Omarchy recipe to Fedora.
