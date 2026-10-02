Name:           omarchy-walker
Version:        1.0.0
Release:        1%{?dist}
Summary:        Meta package for walker with Elephant providers for Omarchy
License:        MIT
URL:            https://omarchy.org
BuildArch:      noarch
Requires:       walker
Requires:       elephant
Requires:       elephant-bluetooth
Requires:       elephant-calc
Requires:       elephant-clipboard
Requires:       elephant-desktopapplications
Requires:       elephant-files
Requires:       elephant-menus
Requires:       elephant-providerlist
Requires:       elephant-runner
Requires:       elephant-symbols
Requires:       elephant-todo
Requires:       elephant-unicode
Requires:       elephant-websearch

%description
Meta package pulling in walker and the Elephant providers used by Omarchy.

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
cat > %{buildroot}%{_datadir}/doc/%{name}/README <<'EOF'
omarchy-walker is a meta package: it ships no files of its own and pulls in
walker plus the Elephant providers used by Omarchy.
EOF

%files
%{_datadir}/doc/%{name}/README

%changelog
* Wed Sep 30 2026 kamm3r - 1.0.0-1
- Port the upstream Omarchy recipe to Fedora.
