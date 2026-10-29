%global debug_package %{nil}

Name:           omasnap
Version:        1.24.0
Release:        2%{?dist}
Summary:        Wayland screenshot and annotation overlay for Hyprland
License:        MIT AND OFL-1.1 AND ISC
URL:            https://github.com/omacom/omasnap
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  pkgconfig(libdeflate)
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  tesseract
BuildRequires:  tesseract-langpack-eng
BuildRequires:  google-noto-sans-fonts
Requires:       hyprland
Requires:       layer-shell-qt
Requires:       tesseract
Requires:       tesseract-langpack-eng
Requires:       wl-clipboard

%description
Omasnap captures and annotates screenshots on the Hyprland desktop.

%prep
%autosetup

# The offscreen smoke test must establish its initial hover state explicitly.
# Keep all shelf assertions; queued motion from preceding overlays is not input
# belonging to this test case.
python3 - <<'PYTEST'
from pathlib import Path
path = Path('tests/editor-smoke.cpp')
source = path.read_text()
anchor = '    if (editor.recentsOpenForTest()) {\n      error = QStringLiteral("Shelf opened before the pointer reached it");'
setup = '    // Establish the initial pointer state explicitly: previous overlays and\n    // the offscreen platform may leave it over the recents shelf.\n    const QPointF initialPointer(100, 300);\n    QMouseEvent initialMove(QEvent::MouseMove, initialPointer,\n                            editor.mapToGlobal(initialPointer.toPoint()),\n                            Qt::NoButton, Qt::NoButton, Qt::NoModifier);\n    QApplication::sendEvent(&editor, &initialMove);\n'
assert source.count(anchor) == 1, 'recents smoke test changed upstream'
path.write_text(source.replace(anchor, setup + anchor))
PYTEST

%build
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} -DBUILD_TESTING=ON
cmake --build build --parallel 4

%install
DESTDIR=%{buildroot} cmake --install build

%check
runtime_dir=$(mktemp -d /dev/shm/omasnap-runtime.XXXXXX)
trap 'rm -rf "$runtime_dir"' EXIT
sync
XDG_RUNTIME_DIR="$runtime_dir" QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME= QT_STYLE_OVERRIDE= QT_FORCE_STDERR_LOGGING=1 ctest --test-dir build --output-on-failure

%files
%license LICENSE
%doc README.md
%{_bindir}/omasnap
%{_datadir}/applications/omasnap.desktop
%{_datadir}/licenses/omasnap/*.txt

%changelog
* Thu Oct 29 2026 kamm3r - 1.24.0-2
- Establish a deterministic initial pointer state in the shelf smoke test.

* Wed Oct 28 2026 kamm3r - 1.24.0-1
- Update to the release pinned in upstream aa38eb00.

* Mon Oct 26 2026 kamm3r - 1.23.0-1
- Update to the release pinned in upstream d5e4ad59.

* Mon Sep 28 2026 kamm3r - 1.21.0-3
- Install the OCR engine, English model, and test font in the buildroot.

* Mon Sep 28 2026 kamm3r - 1.21.0-2
- Provide an XDG runtime directory for the smoke test in clean builds.

* Mon Sep 28 2026 kamm3r - 1.21.0-1
- Port the upstream Omarchy screenshot overlay to Fedora.
