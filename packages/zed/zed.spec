%global debug_package %{nil}

Name:           zed
Version:        1.23.2
Release:        1%{?dist}
Summary:        High-performance, multiplayer code editor
License:        GPL-3.0-or-later AND AGPL-3.0-or-later AND Apache-2.0
URL:            https://zed.dev
Source0:        https://github.com/zed-industries/zed/releases/download/v%{version}/zed-linux-x86_64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Provides:       zeditor = %{version}-%{release}
Requires:       alsa-lib
Requires:       glib2
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       libX11
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       libwayland-client
Requires:       mesa-vulkan-drivers
Requires:       vulkan-loader
Requires:       zlib

%description
Zed is a high-performance, multiplayer code editor from the creators of
Atom and Tree-sitter. This package repacks the upstream binary release,
mirroring the upstream PKGBUILD (the vendor lib/ tree is deliberately not
shipped; system libraries are used instead).

%prep
# Upstream ships a tarball with a top-level zed.app directory, so unpack
# manually without autosetup.
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE0}"

%build
:

%install
# CLI as zed.real, wrapped so the editor never self-updates: it reads
# ZED_UPDATE_EXPLANATION at startup and skips its own update polling when
# it is set. Updates arrive through the package manager.
install -D -m 0755 zed.app/bin/zed %{buildroot}%{_bindir}/zed.real
cat > %{buildroot}%{_bindir}/zed <<'SH'
#!/bin/sh
export ZED_UPDATE_EXPLANATION='Updates are handled by your package manager'
exec /usr/bin/zed.real "$@"
SH
chmod 0755 %{buildroot}%{_bindir}/zed
# Fedora equivalent of the Arch extra zeditor spelling.
ln -s zed %{buildroot}%{_bindir}/zeditor

# The CLI looks for ../libexec/zed-editor, then ../lib/zed/zed-editor, so
# this must live under /usr/lib even on 64-bit (mirrors the PKGBUILD's
# /usr/lib/zed path; %{_libdir} would break lookup from /usr/bin).
install -D -m 0755 zed.app/libexec/zed-editor %{buildroot}/usr/lib/zed/zed-editor

# Vendor desktop entry verbatim: Exec=zed and Icon=zed resolve through
# PATH and hicolor.
install -D -m 0644 zed.app/share/applications/dev.zed.Zed.desktop %{buildroot}%{_datadir}/applications/dev.zed.Zed.desktop

for size in 512x512 1024x1024; do
  install -D -m 0644 zed.app/share/icons/hicolor/${size}/apps/zed.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/zed.png
done

install -D -m 0644 zed.app/licenses.md %{buildroot}%{_licensedir}/zed/licenses.md

%files
%license %{_licensedir}/zed/licenses.md
%{_bindir}/zed
%{_bindir}/zed.real
%{_bindir}/zeditor
/usr/lib/zed/zed-editor
%{_datadir}/applications/dev.zed.Zed.desktop
%{_datadir}/icons/hicolor/*/apps/zed.png

%changelog
* Sat Oct 10 2026 kamm3r - 1.23.2-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 1.22.0-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 1.21.0-1
- Repackage the upstream Omarchy Zed release for Fedora.
