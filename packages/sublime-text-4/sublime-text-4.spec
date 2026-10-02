%global debug_package %{nil}
# /opt/sublime_text bundles its own libssl, libcrypto, libsqlite and
# libpython. Keep those out of the RPM dependency namespace; system
# libraries stay explicitly required below.
%global __provides_exclude ^lib(ssl|crypto|sqlite3|python).*\\.so
%global __requires_exclude ^lib(ssl|crypto|sqlite3|python).*\\.so

Name:           sublime-text-4
Version:        4.4215
Release:        1%{?dist}
Summary:        Sophisticated text editor for code, html and prose - stable build
License:        LicenseRef-Sublime-Text
URL:            https://www.sublimetext.com/download
%global _build 4215
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://download.sublimetext.com/sublime_text_build_%{_build}_x64.tar.xz#/%{name}-%{version}.tar.xz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/sublime-text-4/sublime-text-4.sh
ExclusiveArch:  x86_64
Provides:       sublime-text = %{version}-%{release}
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libpng

%description
Sublime Text is a sophisticated text editor for code, markup and prose.
This package repacks the upstream binary release, mirroring the upstream
PKGBUILD.

%prep
# Upstream ships a tarball with a top-level sublime_text directory plus a
# vendored launcher script, so unpack manually without autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xf "%{SOURCE0}"
cp "%{SOURCE1}" sublime-text-4.sh
# Launcher points at /opt, mirroring the upstream PKGBUILD's @ST_PATH@ edit.
sed -i -e 's|@ST_PATH@|/opt/sublime_text|g' sublime-text-4.sh
# Desktop entry launches via /usr/bin/subl and carries a WM class,
# mirroring the upstream PKGBUILD's prepare edits.
sed -i -e 's#/opt/sublime_text/sublime_text#/usr/bin/subl#g' sublime_text/sublime_text.desktop
sed -i -e '/^StartupNotify=/a StartupWMClass=subl' sublime_text/sublime_text.desktop

%build
:

%install
# Install verbatim from the upstream tarball, mirroring the upstream
# PKGBUILD (which copies sublime_text to /opt and drops its desktop file).
install -d %{buildroot}/opt/sublime_text
cp -a sublime_text/. %{buildroot}/opt/sublime_text/
rm -f %{buildroot}/opt/sublime_text/sublime_text.desktop

for res in 128x128 16x16 256x256 32x32 48x48; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${res}/apps
  ln -s /opt/sublime_text/Icon/${res}/sublime-text.png %{buildroot}%{_datadir}/icons/hicolor/${res}/apps/sublime-text.png
done

install -D -m 0644 sublime_text/sublime_text.desktop %{buildroot}%{_datadir}/applications/sublime_text.desktop
install -D -m 0755 sublime-text-4.sh %{buildroot}%{_bindir}/subl

%files
/opt/sublime_text
%{_bindir}/subl
%{_datadir}/applications/sublime_text.desktop
%{_datadir}/icons/hicolor/*/apps/sublime-text.png

%changelog
* Wed Sep 30 2026 kamm3r - 4.4215-1
- Repackage the upstream Omarchy release for Fedora.
