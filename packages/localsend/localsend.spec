%global debug_package %{nil}
%global toolchain clang

Name:           localsend
Version:        1.18.2
Release:        2%{?dist}
Summary:        Open source cross-platform alternative to AirDrop
License:        Apache-2.0
URL:            https://github.com/localsend/localsend
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-vendor-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64
BuildRequires:  binutils
BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  flutter
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gtk3-devel
BuildRequires:  libappindicator-gtk3-devel
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  ninja-build
BuildRequires:  patchelf
BuildRequires:  rust
Requires:       at-spi2-core
Requires:       cairo
Requires:       fontconfig
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libayatana-appindicator-gtk3
Requires:       libepoxy
Requires:       pango
# NOTE: this is the from-source recipe. The binary repack of the upstream
# .deb (AUR's localsend-bin) stays a separate recipe; see catalog.tsv.

%description
LocalSend shares files and messages with nearby devices over the local
network. This package builds the Flutter desktop app, its Rust core, and
the localsend-cli companion from source.

%prep
%autosetup -a 1

%build
# The Flutter tool resolves the target arch itself; only the Rust isolate
# copy below needs the mapping (mirrors the upstream PKGBUILD).
case "%{_arch}" in
  x86_64) _arch=x64 ;;
  aarch64) _arch=arm64 ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
# Cargokit shells out to rustup; Fedora has no rustup, so provide the same
# no-op shim the upstream PKGBUILD uses to satisfy its version check.
mkdir -p fakebin
printf '#!/usr/bin/env true\n' > fakebin/rustup
chmod 0755 fakebin/rustup
export PATH="$PWD/fakebin:$PATH"

export CARGO_TARGET_DIR=target
# Keep link memory in check on small builders (mirrors upstream).
export CARGO_PROFILE_RELEASE_LTO=false
cargo build --frozen --release --all-features

# Copy the Rust isolate where the Flutter build expects it.
mkdir -p "app/build/linux/$_arch/release/plugins/rust_lib_localsend_app"
cp "target/release/librust_lib_localsend_app.so" "app/build/linux/$_arch/release/plugins/rust_lib_localsend_app/"

# Use a private SDK copy: Flutter writes its cache and inspects its Git tree.
# The packaged SDK is root-owned in a clean builder.
mkdir -p flutter-sdk
# Terra's packaged cache contains unreadable root-owned artifacts.
# Copy the SDK sources and let Flutter populate a fresh user-owned cache.
tar -C /usr/share/flutter --exclude='./bin/cache' -cf - . | tar -xf - -C flutter-sdk
chmod -R u+w flutter-sdk
export PATH="$PWD/flutter-sdk/bin:$PATH"

# Upstream pins Flutter via fvm (.fvmrc); here the packaged Flutter SDK is
# used directly (COPR resolves it from Terra).
cd app
flutter --disable-analytics
flutter --no-version-check pub get
flutter build linux --no-pub --release

%install
case "%{_arch}" in
  x86_64) _arch=x64 ;;
  aarch64) _arch=arm64 ;;
esac
_appdir=%{_prefix}/lib/%{name}
# CLI and headless server from the Cargo workspace.
install -D -m 0755 target/release/localsend-cli -t %{buildroot}$_appdir/
install -D -m 0755 target/release/server -t %{buildroot}$_appdir/
# Flutter app, its private libraries, and its data bundle.
cd "app/build/linux/$_arch/release/bundle"
install -D -m 0755 localsend_app -t %{buildroot}$_appdir
cp -r lib/ %{buildroot}$_appdir/
cp -r data/ %{buildroot}$_appdir/
# Point the bundled loaders at the bundled libraries (mirrors upstream).
for i in %{buildroot}$_appdir %{buildroot}$_appdir/lib/*; do
  if [ -f "$i" ] && readelf -h "$i" >/dev/null 2>&1; then
    case "$i" in
      */lib/*) patchelf --set-rpath '$ORIGIN' "$i" ;;
      *) patchelf --set-rpath '$ORIGIN/lib' "$i" ;;
    esac
  fi
done
install -d %{buildroot}%{_bindir}
ln -s $_appdir/localsend_app %{buildroot}%{_bindir}/localsend
ln -s $_appdir/localsend-cli %{buildroot}%{_bindir}/localsend-cli
install -D -m 0644 "%{buildroot}$_appdir/data/flutter_assets/assets/img/logo-512.png" %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'DESKTOP_EOF'
[Desktop Entry]
Type=Application
Name=LocalSend
Comment=An open source cross-platform alternative to AirDrop
Exec=localsend
Icon=localsend
Terminal=false
Categories=Utility;Network;
DESKTOP_EOF
chmod 0644 %{buildroot}%{_datadir}/applications/%{name}.desktop
# Permissions (mirrors upstream).
chmod -R u+rwX,go+rX,go-w %{buildroot}/

%files
%license LICENSE
/usr/lib/%{name}
%{_bindir}/localsend
%{_bindir}/localsend-cli
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%changelog
* Sat Oct 03 2026 kamm3r - 1.18.2-2
- Build with a writable Flutter SDK and use the installed asset path.
- Select Clang-compatible RPM compiler flags for the Flutter build.

* Wed Sep 30 2026 kamm3r - 1.18.2-1
- Port the upstream Omarchy LocalSend recipe to Fedora.
