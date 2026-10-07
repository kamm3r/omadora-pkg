%global debug_package %{nil}
# /usr/share/code bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so
# The tree bundles its own Node runtime; the only #!/usr/bin/env node
# shebangs belong to bundled node_modules CLI helpers that run under the
# bundled runtime, so keep that interpreter scrap out of the RPM dependency
# namespace (mirrors cursor-bin).
%global __requires_exclude ^(lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan)\\.so|/usr/bin/node)

Name:           visual-studio-code-bin
Version:        1.140.0
Release:        1%{?dist}
Summary:        Editor for building and debugging modern web and cloud applications (official binary version)
License:        LicenseRef-VSCode
URL:            https://code.visualstudio.com/
%global omarchy_pkgs_commit e3dfdd376ce0aac7064497c7bd121f620fa26799
Source0:        https://update.code.visualstudio.com/%{version}/linux-deb-x64/stable#/%{name}-%{version}.deb
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/visual-studio-code-bin/visual-studio-code-bin.sh
ExclusiveArch:  x86_64
Provides:       code = %{version}-%{release}
Provides:       vscode = %{version}-%{release}
Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       glib2
Requires:       glibc
Requires:       gnupg2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXrandr
Requires:       libgcc
Requires:       libnotify
Requires:       libsecret
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbfile
Requires:       lsof
Requires:       mesa-libEGL
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       shared-mime-info
Requires:       systemd-libs
Requires:       xdg-utils

%description
Visual Studio Code is an editor for building and debugging modern web and
cloud applications. This package repacks the official binary release,
keeping its bundled Electron runtime, mirroring the upstream PKGBUILD.

%prep
# Upstream ships a Debian package, not a tarball, so there is no top
# directory to autosetup; the data payload is unpacked with ar+tar.
%setup -q -c -T -n %{name}-%{version}
# Extract the deb payload, dropping Debian-only configuration, mirroring
# the upstream PKGBUILD handling (cursor-bin drops its etc tree the same
# way).
ar p "%{SOURCE0}" data.tar.xz | tar -xJf -
rm -rf etc
# Fedora uses site-functions, not vendor-completions, for zsh completions.
if [ -d usr/share/zsh/vendor-completions ]; then
  mv usr/share/zsh/vendor-completions usr/share/zsh/site-functions
fi

%build
:

%install
# Install verbatim from the unpacked payload, keeping the bundled Electron
# runtime, mirroring the upstream PKGBUILD.
cp -a usr %{buildroot}/

# Launcher, verbatim from the upstream package sources.
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/code

# Fix the desktop entries, mirroring the upstream PKGBUILD.
sed -i -e 's/^\(Exec=\)[^ ]*/\1code/g' %{buildroot}%{_datadir}/applications/*.desktop

# Use Electron's unprivileged namespace sandbox (the upstream PKGBUILD
# strips the setuid bit for the same reason).
chmod 0755 %{buildroot}/usr/share/code/chrome-sandbox

%files
%license usr/share/code/resources/app/LICENSE.rtf
/usr/share/code
%{_bindir}/code
%{_datadir}/applications/com.microsoft.VSCode.desktop
%{_datadir}/applications/com.microsoft.VSCode.UrlHandler.desktop
%{_datadir}/appdata/com.microsoft.VSCode.appdata.xml
%{_datadir}/bash-completion/completions/code
%{_datadir}/zsh/site-functions/_code
%{_datadir}/mime/packages/code-workspace.xml
%{_datadir}/pixmaps/vscode.png

%changelog
* Tue Oct 06 2026 kamm3r - 1.140.0-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 1.139.1-1
- Repackage the upstream Omarchy release for Fedora.
