Name:           ttf-ia-writer
Version:        20261002.r63
Release:        1%{?dist}
Summary:        iA Writer Mono, Duo, Quattro, and Duospace fonts
License:        OFL-1.1
URL:            https://github.com/iaolo/iA-Fonts
Source0:        %{url}/archive/c6588670c71e9ac628acc27b72cde4bf12726b7f.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{url}/archive/b337fe1a4c93026268f70e4b2678371f3e89e2ce.tar.gz#/%{name}-legacy-%{version}.tar.gz
BuildArch:      noarch
Requires:       fontconfig
Provides:       ttf-ia-writer-duospace = %{version}-%{release}

%description
Static iA Writer fonts, including the legacy Duospace family pinned by the
upstream Omarchy recipe.

%prep
%setup -q -n iA-Fonts-c6588670c71e9ac628acc27b72cde4bf12726b7f -a 1
cp -a iA-Fonts-b337fe1a4c93026268f70e4b2678371f3e89e2ce/'iA Writer Duospace' .

%build
:

%install
install -d %{buildroot}%{_datadir}/fonts/ttf-ia-writer
install -m 0644 'iA Writer Mono'/Static/*.ttf %{buildroot}%{_datadir}/fonts/ttf-ia-writer/
install -m 0644 'iA Writer Duo'/Static/*.ttf %{buildroot}%{_datadir}/fonts/ttf-ia-writer/
install -m 0644 'iA Writer Quattro'/Static/*.ttf %{buildroot}%{_datadir}/fonts/ttf-ia-writer/
install -m 0644 'iA Writer Duospace'/'TTF (PC)'/*.ttf %{buildroot}%{_datadir}/fonts/ttf-ia-writer/

%files
%license iA\ Writer\ Mono/LICENSE.md
%{_datadir}/fonts/ttf-ia-writer/*.ttf

%changelog
* Tue Oct 06 2026 kamm3r - 20261002.r63-1
- Update to the release pinned on upstream master.

* Mon Sep 28 2026 kamm3r - 20230616.r62-1
- Port the upstream Omarchy iA Writer font subset to Fedora.
