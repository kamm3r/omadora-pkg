Name:           tobi-try
Version:        1.10.1
Release:        1%{?dist}
Summary:        Fresh directories for every development experiment
License:        MIT
URL:            https://github.com/tobi/try
Source0:        https://github.com/tobi/try/archive/refs/tags/v%{version}.tar.gz#/try-%{version}.tar.gz
BuildArch:      noarch
Requires:       ruby
Provides:       try = %{version}-%{release}

%description
Try creates and manages fresh directories for short development experiments.

%prep
%autosetup -n try-%{version}

%build
sed -i '1c#!/usr/bin/ruby' try.rb

%install
install -D -m 0755 try.rb %{buildroot}%{_datadir}/%{name}/try.rb
install -D -m 0644 lib/tui.rb %{buildroot}%{_datadir}/%{name}/lib/tui.rb
install -D -m 0644 lib/fuzzy.rb %{buildroot}%{_datadir}/%{name}/lib/fuzzy.rb
install -d %{buildroot}%{_bindir}
ln -s ../share/%{name}/try.rb %{buildroot}%{_bindir}/try

%files
%license LICENSE
%doc README.md
%{_bindir}/try
%{_datadir}/%{name}

%changelog
* Mon Sep 28 2026 kamm3r - 1.10.1-1
- Port the upstream Omarchy recipe to Fedora.
