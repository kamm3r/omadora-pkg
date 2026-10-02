%global _commit cd3fcdda3f8e15fda73288f6cf3803164138a7e4
%global lua_version 5.4.7
%global sol2_tag d805d027e0a0a7222e936926139f06e23828ce9f
%global sol2_short d805d027

Name:           omatrack
Version:        1.8.6
Release:        1%{?dist}
Summary:        Cross-format motorsport telemetry analysis workstation
License:        MIT
URL:            https://github.com/tobi/omatrack
Source0:        %{url}/archive/%{_commit}.tar.gz#/omatrack-%{_commit}.tar.gz
Source1:        https://www.lua.org/ftp/lua-%{lua_version}.tar.gz
Source2:        https://github.com/ThePhD/sol2/archive/%{sol2_tag}.tar.gz#/sol2-%{sol2_short}.tar.gz
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  mpv-libs-devel
BuildRequires:  libyaml-devel
Requires:       hicolor-icon-theme
Requires:       mpv-libs
Requires:       libyaml
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland

%description
Omatrack is a cross-format motorsport telemetry analysis workstation.

%prep
# NOTE: %%autosetup honors only a single -a flag (the last one wins), so unpack
# the Lua bundle explicitly after the sol2 bundle.
%autosetup -n omatrack-%{_commit} -a 2
tar -xzf %{SOURCE1}
# Mirror the upstream prepare(): prefetch the Rust bridge crates.
cd third_party/motorsport-telemetry
cargo fetch --locked

%build
%cmake -G Ninja \
  -DFETCHCONTENT_SOURCE_DIR_LUA_SRC=%{_builddir}/omatrack-%{_commit}/lua-%{lua_version} \
  -DFETCHCONTENT_SOURCE_DIR_SOL2=%{_builddir}/omatrack-%{_commit}/sol2-%{sol2_tag} \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON
%cmake_build

%install
%cmake_install
# Ship the license via %license instead of the cmake-installed copy.
rm %{buildroot}%{_datadir}/doc/omatrack/LICENSE

%files
%license LICENSE
%{_bindir}/omatrack
%{_datadir}/applications/io.github.tobi.omatrack.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.tobi.omatrack.svg
%{_datadir}/metainfo/io.github.tobi.omatrack.metainfo.xml
%{_datadir}/mime/packages/omatrack.xml
%{_datadir}/doc/omatrack/README.md
%{_datadir}/doc/omatrack/THIRD_PARTY_NOTICES.md

%changelog
* Wed Sep 30 2026 kamm3r - 1.8.6-1
- Port the upstream Omarchy recipe to Fedora.
