%global debug_package %{nil}
# Upstream binary carries a build-tree RUNPATH; this is a binary repack so
# the RPATH QA check is skipped (mirrors other binary-only Fedora packs).
%undefine __brp_check_rpaths
# /opt/dropbox bundles its own Python runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(python|ffi|atomic|dropbox).*\\.so
%global __requires_exclude ^lib(python|ffi|atomic|dropbox).*\\.so

Name:           dropbox
Version:        272.4.3798
Release:        1%{?dist}
Summary:        Free service that lets you bring your photos, docs, and videos anywhere and share them easily
License:        LicenseRef-Dropbox
URL:            https://www.dropbox.com
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        https://edge.dropboxstatic.com/dbx-releng/client/dropbox-lnx.x86_64-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/dropbox/DropboxGlyph_Blue.svg
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/dropbox/terms.txt
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/dropbox/dropbox.service
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/dropbox/dropbox@.service
ExclusiveArch:  x86_64
BuildRequires:  systemd-rpm-macros
Requires:       dbus-libs
Requires:       fontconfig
Requires:       hicolor-icon-theme
Requires:       libSM
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXmu
Requires:       libXrender
Requires:       libxslt
Requires:       libXxf86vm

%description
Dropbox is a free service that lets you bring your photos, docs, and
videos anywhere and share them easily. This package repacks the upstream
binary release, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a tarball whose top level is .dropbox-dist, not a plain
# source directory, so there is no top directory to autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE0}"

%build
:

%install
install -d %{buildroot}/opt
cp -dr --no-preserve=ownership .dropbox-dist/dropbox-lnx.x86_64-%{version} %{buildroot}/opt/dropbox
chmod 755 %{buildroot}/opt/dropbox/*.so

install -d %{buildroot}%{_bindir}
ln -s /opt/dropbox/dropbox %{buildroot}%{_bindir}/dropbox

# Desktop entry, generated upstream with gendesk from the package name,
# description, and Network category; reproduced statically since Fedora has
# no gendesk.
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/dropbox.desktop <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Dropbox
Comment=A free service that lets you bring your photos, docs, and videos anywhere and share them easily.
Exec=dropbox
Icon=dropbox
Terminal=false
Categories=Network;
StartupNotify=false
EOF
chmod 0644 %{buildroot}%{_datadir}/applications/dropbox.desktop
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/dropbox.svg
install -D -m 0644 %{SOURCE2} %{buildroot}%{_licensedir}/dropbox/terms.txt
install -D -m 0644 %{SOURCE3} %{buildroot}%{_userunitdir}/dropbox.service
install -D -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/dropbox@.service

%files
%license %{_licensedir}/dropbox/terms.txt
/opt/dropbox
%{_bindir}/dropbox
%{_datadir}/applications/dropbox.desktop
%{_datadir}/pixmaps/dropbox.svg
%{_userunitdir}/dropbox.service
%{_unitdir}/dropbox@.service

%changelog
* Tue Oct 06 2026 kamm3r - 272.4.3798-1
- Update to the release pinned on upstream master.

* Sat Oct 03 2026 kamm3r - 270.4.3312-2
- Require systemd RPM macros for the system and user service paths.

* Thu Oct 01 2026 kamm3r - 270.4.3312-1
- Repackage the upstream Omarchy release for Fedora.
