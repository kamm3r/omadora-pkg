%global debug_package %{nil}

Name:           elephant-all
Version:        2.22.1
Release:        1%{?dist}
Summary:        Elephant with all official providers
License:        GPL-3.0-only
URL:            https://github.com/abenz1267/elephant
BuildArch:      noarch
# Meta package: upstream elephant-all builds the binary plus every provider
# from one tarball. On Fedora the binary and each provider ship as separate
# RPMs, so this package only Requires the set Omadora ports. Arch-only
# providers (e.g. elephant-archlinuxpkgs) are intentionally excluded.
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
Meta package pulling in elephant and all official Elephant providers
packaged for Omadora.

%prep
%build
%install
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
cat > %{buildroot}%{_datadir}/doc/%{name}/README <<'EOF'
elephant-all is a meta package: it ships no files of its own and pulls in
elephant plus all official Elephant providers packaged for Omadora.
EOF

%files
%{_datadir}/doc/%{name}/README

%changelog
* Wed Sep 30 2026 kamm3r - 2.22.1-1
- Port the upstream Omarchy recipe to Fedora.
