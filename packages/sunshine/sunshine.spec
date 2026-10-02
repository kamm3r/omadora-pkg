%global debug_package %{nil}
%undefine _hardened_build

Name:           sunshine
Version:        2026.914.233613
Release:        1%{?dist}
Summary:        Self-hosted game stream host for Moonlight
License:        GPL-3.0-only
URL:            https://app.lizardbyte.dev/Sunshine
%global _commit 63d35f702ee9e362e43263742981836ec0710384
Source0:        https://github.com/LizardByte/Sunshine/archive/%{_commit}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  appstream
BuildRequires:  cmake >= 3.25.0
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  glslc
BuildRequires:  libappstream-glib
BuildRequires:  libcap-devel
BuildRequires:  libcurl-devel
BuildRequires:  libdrm-devel
BuildRequires:  libevdev-devel
BuildRequires:  libgudev-devel
BuildRequires:  libva-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXtst-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  nodejs
BuildRequires:  nodejs-npm
BuildRequires:  numactl-devel
BuildRequires:  openssl-devel
BuildRequires:  opus-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python3-jinja2
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  vulkan-loader-devel
BuildRequires:  which
BuildRequires:  wget
%ifarch x86_64
BuildRequires:  intel-mediasdk-devel
%endif
%ifarch aarch64
BuildRequires:  vulkan-headers
%endif
Requires:       avahi
Requires:       hicolor-icon-theme
Requires:       libcap
Requires:       libcurl
Requires:       libdrm
Requires:       libevdev
Requires:       libva
Requires:       libX11
Requires:       libxcb
Requires:       libXfixes
Requires:       libXrandr
Requires:       libXtst
Requires:       miniupnpc >= 2.2.4
Requires:       numactl-libs
Requires:       openssl-libs
Requires:       opus
Requires:       pipewire-libs
Requires:       pulseaudio-libs
Requires:       qt6-qtbase
Requires:       qt6-qtsvg
Requires:       systemd-udev
Requires:       vulkan-loader
Requires:       which

%description
Sunshine is a self-hosted game stream host for Moonlight. This package
builds the pinned upstream commit, mirroring the upstream PKGBUILD and
the upstream COPR recipe, with Omarchy publisher branding. CUDA encoding
stays disabled, matching the PKGBUILD default when CUDA is absent. Fedora
also ships Sunshine via RPM Fusion; this recipe exists so the catalog has
a COPR source for the Omarchy-pinned commit.

%prep
# Upstream sources live in git with recursive submodules, which GitHub
# archives do not include, so clone the pinned commit at build time
# (builders have network access). Source0 stays the pinned archive for
# source-RPM verification.
%setup -q -c -T -n %{name}-%{version}
git clone https://github.com/LizardByte/Sunshine.git sunshine-git
cd sunshine-git
git checkout %{_commit}
git submodule update --init --recursive --depth 1

%build
export BRANCH="master"
export BUILD_VERSION="%{version}"
export COMMIT="%{_commit}"
export CC="gcc"
export CXX="g++"
export MAKEFLAGS="${MAKEFLAGS:--j$(nproc)}"
cd sunshine-git
cmake -S . -B build -G "Unix Makefiles" -Wno-dev \
  -D BUILD_DOCS=OFF \
  -D BUILD_WERROR=ON \
  -D BUILD_TESTS=OFF \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX=/usr \
  -D SUNSHINE_EXECUTABLE_PATH=/usr/bin/sunshine \
  -D SUNSHINE_ASSETS_DIR="share/sunshine" \
  -D SUNSHINE_ENABLE_CUDA=OFF \
  -D CUDA_FAIL_ON_MISSING=OFF \
  -D SUNSHINE_ENABLE_DRM=ON \
  -D SUNSHINE_ENABLE_KWIN=ON \
  -D SUNSHINE_ENABLE_PORTAL=ON \
  -D SUNSHINE_ENABLE_WAYLAND=ON \
  -D SUNSHINE_ENABLE_X11=ON \
  -D SUNSHINE_PUBLISHER_NAME='Omarchy' \
  -D SUNSHINE_PUBLISHER_WEBSITE='https://omarchy.org' \
  -D SUNSHINE_PUBLISHER_ISSUE_URL='https://github.com/omacom/omarchy-pkgs/issues'
appstreamcli validate --no-net build/dev.lizardbyte.app.Sunshine.metainfo.xml || :
appstream-util validate build/dev.lizardbyte.app.Sunshine.metainfo.xml || :
desktop-file-validate build/dev.lizardbyte.app.Sunshine.desktop || :
desktop-file-validate build/dev.lizardbyte.app.Sunshine.terminal.desktop || :
cmake --build build

%install
cd sunshine-git
DESTDIR="%{buildroot}" cmake --install build

%check
cd sunshine-git/build
./sunshine --version

%post
modprobe uhid 2>/dev/null || :
if [ -x "$(command -v udevadm)" ]; then
  udevadm control --reload-rules 2>/dev/null || :
  udevadm trigger --property-match=DEVNAME=/dev/uinput 2>/dev/null || :
  udevadm trigger --property-match=DEVNAME=/dev/uhid 2>/dev/null || :
  udevadm trigger --subsystem-match=hidraw 2>/dev/null || :
  udevadm trigger --subsystem-match=input 2>/dev/null || :
fi

%files
%caps(cap_sys_admin,cap_sys_nice+p) %{_bindir}/sunshine
%{_userunitdir}/*.service
%{_udevrulesdir}/*-sunshine.rules
%{_modulesloaddir}/*-sunshine.conf
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.Sunshine.svg
%{_datadir}/metainfo/*.metainfo.xml
%{_datadir}/sunshine/

%changelog
* Thu Oct 01 2026 kamm3r - 2026.914.233613-1
- Port the upstream Omarchy recipe to Fedora.
