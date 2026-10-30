%global debug_package %{nil}
%global __strip /bin/true
%global appname wordcraft

Name:           wordcraft-bin
Version:        0.12.0
Release:        1%{?dist}
Summary:        Word processor and CLI for Word documents
License:        (Apache-2.0 OR MIT) AND OFL-1.1
URL:            https://github.com/storytold/wordcraft
Source0:        %{url}/releases/download/v%{version}/%{appname}-%{version}-linux-x86_64.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
Provides:       %{appname} = %{version}-%{release}
Conflicts:      %{appname}
Requires:       dbus-libs
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       wayland-libs
Requires:       vulkan-loader
Requires:       hicolor-icon-theme

%description
Word processor and CLI for Word documents. This package installs the upstream native Linux binary,
desktop integration, command line tools, and bundled font license notices.

%prep
%setup -q -n %{appname}-%{version}-linux-x86_64

%build
:

%install
install -Dm755 bin/%{appname} bin/%{appname}-cli -t %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}
cp -a share/. %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_licensedir}/%{name}
cp -a share/doc/%{appname}/LICENSE-* share/doc/%{appname}/NOTICE share/doc/%{appname}/OFL-* %{buildroot}%{_licensedir}/%{name}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/ai.storyteller.%{appname}.desktop
test -x %{buildroot}%{_bindir}/%{appname}
test -x %{buildroot}%{_bindir}/%{appname}-cli

%files
%license %{_licensedir}/%{name}
%{_bindir}/%{appname}
%{_bindir}/%{appname}-cli
%{_datadir}/applications/ai.storyteller.%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/ai.storyteller.%{appname}.*
%{_datadir}/metainfo/ai.storyteller.%{appname}.metainfo.xml
%{_datadir}/mime/packages/ai.storyteller.%{appname}.xml
%{_datadir}/doc/%{appname}

%changelog
* Fri Oct 30 2026 kamm3r - 0.12.0-1
- Port upstream b766e177 native release to Fedora.
