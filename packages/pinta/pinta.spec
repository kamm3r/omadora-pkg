%global debug_package %{nil}

Name:           pinta
Version:        3.1.2
Release:        1%{?dist}
Summary:        Drawing/editing program modeled after Paint.NET
License:        MIT
URL:            https://pinta-project.com
Source0:        https://github.com/PintaProject/Pinta/releases/download/%{version}/pinta-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  dotnet-sdk-8.0
BuildRequires:  gcc
BuildRequires:  intltool
BuildRequires:  make
BuildRequires:  pkgconf
Requires:       dotnet-runtime-8.0
Requires:       gdk-pixbuf2
Requires:       hicolor-icon-theme
Requires:       libadwaita

%description
Pinta is a drawing/editing program modeled after Paint.NET. Its goal is to
provide a simplified alternative to GIMP for casual users. This package
builds the upstream release with the .NET 8 SDK, mirroring the upstream
Omarchy recipe (which targets linux-arm64 on Arch ARM; here the runtime
identifier follows the build arch).

%prep
%autosetup

%build
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --localstatedir=/var
case "%{_arch}" in
  x86_64) _rid=linux-x64 ;;
  aarch64) _rid=linux-arm64 ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
make PINTA_BUILD_OPTS="--configuration Release -p:BuildTranslations=true -p:RuntimeIdentifier=$_rid"

%install
make DESTDIR=%{buildroot} install
install -Dm644 -t "%{buildroot}%{_datadir}/doc/%{name}/" readme.md
install -Dm644 -t "%{buildroot}%{_datadir}/licenses/%{name}/" license-*.txt

%files
%license %{_datadir}/licenses/%{name}/license-*.txt
%doc %{_datadir}/doc/%{name}/readme.md
%{_bindir}/pinta
/usr/lib/pinta/
%{_libdir}/pkgconfig/pinta.pc
%{_datadir}/applications/com.github.PintaProject.Pinta.desktop
%{_datadir}/metainfo/com.github.PintaProject.Pinta.metainfo.xml
%{_datadir}/icons/
%{_datadir}/locale/*/LC_MESSAGES/pinta.mo
%{_mandir}/man1/pinta.1*

%changelog
* Thu Oct 01 2026 kamm3r - 3.1.2-1
- Port the upstream Omarchy Pinta recipe to Fedora.
