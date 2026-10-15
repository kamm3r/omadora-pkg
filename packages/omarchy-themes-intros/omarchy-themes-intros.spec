%global debug_package %{nil}
%global source_commit ecf0eb362283efad6404b939981c7ef8d58039b3

Name:           omarchy-themes-intros
Version:        2026.10.14
Release:        1%{?dist}
Summary:        Background intro videos for the Omarchy themes
License:        MIT
URL:            https://github.com/basecamp/omarchy
Source0:        %{url}/archive/%{source_commit}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
Background intro videos for the stock Omarchy themes. These optional
assets are packaged separately from the Omadora desktop code.

%prep
%autosetup -n omarchy-%{source_commit}

%build
:

%install
for intros in themes/*/backgrounds/intros; do
  install -d %{buildroot}%{_datadir}/omarchy/"$intros"
  cp -a "$intros/." %{buildroot}%{_datadir}/omarchy/"$intros/"
done

%files
%license LICENSE
%{_datadir}/omarchy/themes/*/backgrounds/intros

%changelog
* Thu Oct 15 2026 kamm3r - 2026.10.14-1
- Package the separately maintained theme intro videos.
