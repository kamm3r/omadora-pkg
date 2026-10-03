%global debug_package %{nil}

Name:           omasnap-git
Version:        1.21.0.r76.g614cdf5
Release:        2%{?dist}
Summary:        Wayland screenshot and annotation overlay for Hyprland (main-branch build)
License:        MIT AND OFL-1.1 AND ISC
URL:            https://github.com/omacom/omasnap
# Pinned main-branch commit, mirroring the upstream -git PKGBUILD: every
# main tip becomes a commit pin, versioned <last tag>.r<commits>.g<sha> so
# it sorts above the tagged release it follows and below the next one.
%global _commit 614cdf55b42a43c1dcee2c85cd01e4764a52bdae
Source0:        %{url}/archive/%{_commit}.tar.gz#/%{name}-%{version}.tar.gz
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
Provides:       omasnap = %{version}-%{release}
Conflicts:      omasnap

%description
Omasnap captures and annotates screenshots on the Hyprland desktop. This
is the main-branch build, pinned to the same upstream commit as the
Omarchy omasnap-git package.

%prep
%autosetup -n omasnap-%{_commit}

%build
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix}
cmake --build build --parallel

%install
DESTDIR=%{buildroot} cmake --install build

%check
# Mirrors the PKGBUILD check(): flush dirty pages first so the smoke
# suite's fsync settle windows are not overrun, and give Qt an offscreen
# runtime directory in clean builds.
runtime_dir=$(mktemp -d /dev/shm/omasnap-runtime.XXXXXX)
trap 'rm -rf "$runtime_dir"' EXIT
sync
XDG_RUNTIME_DIR="$runtime_dir" QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME= QT_STYLE_OVERRIDE= QT_FORCE_STDERR_LOGGING=1 ./build/omasnap-smoke ./omasnap-smoke-output

%files
%license LICENSE
%doc README.md
%{_bindir}/omasnap
%{_datadir}/applications/omasnap.desktop
%{_datadir}/licenses/omasnap/*.txt

%changelog
* Sat Oct 03 2026 kamm3r - 1.21.0.r76.g614cdf5-2
- Add libdeflate for the main-branch screenshot encoder.

* Thu Oct 01 2026 kamm3r - 1.21.0.r76.g614cdf5-1
- Port the upstream Omarchy main-branch screenshot overlay to Fedora.
