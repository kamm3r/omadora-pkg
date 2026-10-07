%global debug_package %{nil}
# Prebuilt libonnxruntime.so carries an upstream build-host RPATH; it is
# dlopened from its own directory and the RPATH is harmless, so skip the
# check (mirrors voxtype-bin).
%global __brp_check_rpaths %{nil}
# /opt/zen-browser-bin bundles its own Gecko runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(vk_swiftshader|vulkan|qt.*_shim)\\.so
%global __requires_exclude ^lib(vk_swiftshader|vulkan|qt.*_shim)\\.so

Name:           zen-browser-bin
Version:        1.23b
Release:        1%{?dist}
Summary:        Privacy-focused, feature packed Firefox-based web browser (binary release)
License:        MPL-2.0-only
URL:            https://github.com/zen-browser/desktop
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-x86_64.tar.xz#/%{name}-%{version}.tar.xz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/zen-browser-bin/zen-browser.sh
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/zen-browser-bin/zen.desktop
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/zen-browser-bin/policies.json
ExclusiveArch:  x86_64
Provides:       zen-browser = %{version}-%{release}
Requires:       alsa-lib
Requires:       dbus-glib
Requires:       gtk3
Requires:       hunspell
Requires:       hyphen
Requires:       libXt
Requires:       mailcap
Requires:       nss
Requires:       systemd-libs
Requires:       ffmpeg-libs

%description
Zen is a privacy-focused, feature packed Firefox-based web browser. This
package repacks the upstream binary release, keeping its bundled Gecko
runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a tarball with a top-level zen directory, so unpack
# manually without autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xf "%{SOURCE0}"
cp "%{SOURCE1}" zen-browser.sh
cp "%{SOURCE2}" zen.desktop
cp "%{SOURCE3}" policies.json

%build
:

%install
install -d %{buildroot}/opt
cp -a zen %{buildroot}/opt/zen-browser-bin

# Launcher, mirroring the upstream PKGBUILD.
install -D -m 0755 zen-browser.sh %{buildroot}%{_bindir}/zen-browser

# Desktop entry, verbatim from the upstream package sources.
install -D -m 0644 zen.desktop %{buildroot}%{_datadir}/applications/zen.desktop

# Icons, mirroring the upstream PKGBUILD (symlinks into the bundle).
for i in 16x16 32x32 48x48 64x64 128x128; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/$i/apps/
  ln -s /opt/zen-browser-bin/browser/chrome/icons/default/default${i/x*}.png \
    %{buildroot}%{_datadir}/icons/hicolor/$i/apps/zen-browser.png
done

# Use system-provided dictionaries.
ln -Ts /usr/share/hunspell %{buildroot}/opt/zen-browser-bin/dictionaries
ln -Ts /usr/share/hyphen %{buildroot}/opt/zen-browser-bin/hyphenation

# Use system certificates.
ln -sf %{_libdir}/libnssckbi.so %{buildroot}/opt/zen-browser-bin/libnssckbi.so

# Disable update checks (managed by the package manager).
install -d %{buildroot}/opt/zen-browser-bin/distribution
install -m 0644 policies.json %{buildroot}/opt/zen-browser-bin/distribution/policies.json

%files
/opt/zen-browser-bin
%{_bindir}/zen-browser
%{_datadir}/applications/zen.desktop
%{_datadir}/icons/hicolor/*/apps/zen-browser.png

%changelog
* Tue Oct 06 2026 kamm3r - 1.23b-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 1.22.3b-1
- Repackage the upstream Omarchy Zen Browser release for Fedora.
