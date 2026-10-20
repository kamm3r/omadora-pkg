Name:           maplemono-nf-cn
Version:        7.9
Release:        1%{?dist}
Summary:        Maple Mono with Nerd Font icons and Chinese glyphs
License:        OFL-1.1
URL:            https://github.com/subframe7536/maple-font
Source0:        %{url}/releases/download/v%{version}/MapleMono-NF-CN.zip#/MapleMono-NF-CN-%{version}.zip
BuildArch:      noarch
BuildRequires:  unzip
BuildRequires:  fontconfig
Requires:       fontpackages-filesystem
Requires:       fontconfig

%description
Hinted Maple Mono monospace fonts with Nerd Font icons and Chinese glyphs.

%prep
%setup -q -c -T
unzip -q %{SOURCE0}

%build
:

%install
install -dm755 %{buildroot}%{_datadir}/fonts/%{name}
install -m644 MapleMono-NF-CN-*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
install -Dm644 LICENSE.txt %{buildroot}%{_licensedir}/%{name}/LICENSE.txt

%check
for font in MapleMono-NF-CN-*.ttf; do
  fc-scan --format '%%{family}\n' "$font" | grep -q 'Maple Mono'
done

%files
%license %{_licensedir}/%{name}/LICENSE.txt
%{_datadir}/fonts/%{name}

%changelog
* Tue Oct 20 2026 kamm3r - 7.9-1
- Port the upstream Maple Mono NF CN recipe to Fedora.
