%global debug_package %{nil}
%global __strip /bin/true

Name:           kujo
Version:        1.9.0
Release:        1%{?dist}
Summary:        Programming language and runtime for AI-native software
License:        MIT
URL:            https://kujolang.ai
Source0:        https://github.com/kujolang/kujo/releases/download/v%{version}/kujo-v%{version}-linux-x64.tar.gz
Source1:        https://raw.githubusercontent.com/kujolang/kujo/v%{version}/LICENSE#/%{name}-LICENSE
ExclusiveArch:  x86_64
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       zlib

%description
Kujo provides a programming language and runtime for AI-native software.

%prep
%setup -q -c -T
 tar -xzf %{SOURCE0}

%build
:

%install
install -Dm755 kujo %{buildroot}%{_bindir}/kujo
install -Dm644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE

%check
./kujo --version

%files
%license %{_licensedir}/%{name}/LICENSE
%{_bindir}/kujo

%changelog
* Fri Oct 23 2026 kamm3r - 1.9.0-1
- Update to the release pinned in upstream 5cf42189.

* Tue Oct 20 2026 kamm3r - 1.8.2-1
- Port the upstream Kujo recipe to Fedora.
