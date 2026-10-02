Name:           omarchy-billboard-generator
Version:        0.2.0
Release:        1%{?dist}
Summary:        Desktop app and CLI that renders animated Omarchy domain videos
License:        MIT AND Apache-2.0 AND 0BSD AND OFL-1.1 AND LicenseRef-Omarchy
URL:            https://github.com/llstrk/omarchy-billboard-generator
Source0:        %{url}/releases/download/v%{version}/%{name}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  nodejs >= 22
BuildRequires:  npm
Requires:       nodejs >= 22
Requires:       chromium
Requires:       ffmpeg
Requires:       xdg-utils

%description
Omarchy Billboard Generator renders animated Omarchy domain videos
locally, through both a desktop app and a CLI. Chromium and ffmpeg are
runtime dependencies found on PATH, never downloaded.

%prep
# The release tarball root is unversioned (%{name}); only the file is renamed.
%autosetup -n %{name}

%build
# The same install the upstream release installer performs: locked
# production dependencies, no lifecycle scripts (mirrors upstream).
npm ci --omit=dev --ignore-scripts --cache "$PWD/.npm-cache"

%check
# The catalogs prefer a synced snapshot in the user data directory, so point
# them at an empty one: the build must read the bundled data, not whatever
# the builder's home happens to hold (mirrors upstream).
export BILLBOARD_DATA_DIR="$PWD/data-home" BILLBOARD_CACHE_DIR="$PWD/cache-home"
# Upstream's own startup check, plus the catalogs that load the bundled data.
node bin/omarchy-billboard --help >/dev/null
node bin/omarchy-billboard --list-themes >/dev/null
node bin/omarchy-billboard --list-languages >/dev/null
node bin/omarchy-billboard --list-animations >/dev/null
node bin/omarchy-billboard-app --help >/dev/null

%install
_appdir=%{_prefix}/lib/%{name}
install -d %{buildroot}$_appdir
# Only what runs: no tests, release scripts, CI, or the curl|bash installer.
cp -a bin src app web assets data examples node_modules package.json %{buildroot}$_appdir/
# The entry points resolve their sources through the real path of the
# script, so a symlink is enough and keeps the launcher's node on PATH.
install -d %{buildroot}%{_bindir}
ln -s $_appdir/bin/omarchy-billboard %{buildroot}%{_bindir}/omarchy-billboard
ln -s $_appdir/bin/omarchy-billboard-app %{buildroot}%{_bindir}/omarchy-billboard-app
# Written here rather than shipped as a second source: the source flow
# rewrites checksums wholesale from the release manifest on version bumps,
# so a local file's checksum would not survive (mirrors upstream). The WM
# class is what Chromium derives for this app-mode window, so the
# launcher's icon follows it.
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'DESKTOP_EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Omarchy Billboard Generator
Comment=Create animated Omarchy domain videos locally
Exec=omarchy-billboard-app
Icon=omarchy-billboard-generator
Terminal=false
Categories=AudioVideo;Video;
StartupWMClass=chrome-127.0.0.1__omarchy-billboard-Default
DESKTOP_EOF
chmod 0644 %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m 0644 app/icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files
%license LICENSE PROVENANCE.md assets/fonts/*-OFL.txt
%doc README.md THEMES.md
/usr/lib/%{name}
%{_bindir}/omarchy-billboard
%{_bindir}/omarchy-billboard-app
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Wed Sep 30 2026 kamm3r - 0.2.0-1
- Port the upstream Omarchy billboard generator to Fedora.
