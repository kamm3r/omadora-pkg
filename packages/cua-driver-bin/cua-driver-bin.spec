%global debug_package %{nil}
# /usr/lib/cua-driver bundles the private SDK library plus the node runtime.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude_from ^/usr/lib/cua-driver/.*
%global __requires_exclude_from ^/usr/lib/cua-driver/.*

Name:           cua-driver-bin
Version:        0.28.2
Release:        1%{?dist}
Summary:        Computer-use driver for native GUI apps: accessibility-tree snapshots and input injection
License:        MIT
URL:            https://github.com/trycua/cua
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        %{url}/releases/download/cua-driver-rs-v%{version}/cua-driver-rs-%{version}-linux-x86_64.tar.gz#/%{name}-%{version}-linux-x86_64.tar.gz
Source1:        %{url}/releases/download/cua-driver-rs-v%{version}/cua-driver-rs-%{version}-linux-arm64.tar.gz#/%{name}-%{version}-linux-arm64.tar.gz
# Stand-in for the vendor installer, from the upstream recipe. The binary's
# `update --apply` is rewritten to point here instead of the vendor
# installer, which would install a second copy under ~/.cua-driver.
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/cua-driver-bin/pm.sh#/%{name}-pm.sh-%{version}
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/cua-driver-bin/LICENSE#/%{name}-LICENSE-%{version}
ExclusiveArch:  x86_64 aarch64
Provides:       cua-driver = %{version}-%{release}
Conflicts:      cua-driver
# at-spi2-core carries the AT-SPI accessibility bus the driver reads GUI
# trees through; the X libraries are linked, not dlopen'd.
Requires:       at-spi2-core
Requires:       libX11
Requires:       libXext
Requires:       libXi
Requires:       libxcb
Requires:       libxkbcommon

%description
Computer-use driver for native GUI apps: accessibility-tree snapshots and
input injection. This package repacks the upstream prebuilt release,
keeping the whole vendor tree together under /usr/lib/cua-driver with a
/usr/bin symlink, mirroring the upstream PKGBUILD. The binary's self-updater
is redirected to a stand-in that declines and names the package manager
instead, so updates stay gated on this repository's releases. Held at
0.28.2: newer releases break screenshots, so bump by hand only once a
fixed release is verified.

%prep
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64)
    tar -xzf "%{SOURCE0}"
    release_root="cua-driver-rs-%{version}-linux-x86_64"
    ;;
  aarch64)
    tar -xzf "%{SOURCE1}"
    release_root="cua-driver-rs-%{version}-linux-arm64"
    ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
cp "%{SOURCE2}" pm.sh
cp "%{SOURCE3}" LICENSE
# Fedora names the package manager dnf, not pacman.
sed -i 's/pacman/dnf/g' pm.sh
sed -i 's/sudo dnf -Syu cua-driver-bin/sudo dnf upgrade cua-driver-bin/' pm.sh
# Installer-URL rewrite, mirroring the upstream PKGBUILD prepare(): the
# binary resolves its helpers as siblings of /proc/self/exe, and Rust
# strings carry their length out of band, so the replacement has to be
# exactly as long as the original, which is what fixes the stand-in's
# short name and location.
vendor_installer='https://cua.ai/driver/install.sh'
local_installer='file:///usr/lib/cua-driver/pm.sh'
if (( ${#vendor_installer} != ${#local_installer} )); then
  echo "installer URLs must be the same length to rewrite in place" >&2
  exit 1
fi
# In 0.28.1 the URL appears in the updater, the printed reinstall command,
# and two embedded copies of Skills/cua-driver/README.md. Rewrite all four
# so the embedded instructions also defer to the package manager. Any other
# count means the release layout changed and needs review before packaging.
expected=4
found=$(grep -obUaF "$vendor_installer" "$release_root/cua-driver" | wc -l)
if (( found != expected )); then
  echo "expected the vendor installer URL $expected times in cua-driver, found $found" >&2
  exit 1
fi
size_before=$(stat -c %s "$release_root/cua-driver")
sed -i "s|${vendor_installer//./\\.}|${local_installer}|g" "$release_root/cua-driver"
size_after=$(stat -c %s "$release_root/cua-driver")
if (( size_before != size_after )) \
    || grep -qUaF "$vendor_installer" "$release_root/cua-driver" \
    || (( $(grep -obUaF "$local_installer" "$release_root/cua-driver" | wc -l) != expected )); then
  echo "installer URL rewrite did not land cleanly in cua-driver" >&2
  exit 1
fi

%build
:

%install
case "%{_arch}" in
  x86_64) release_root="cua-driver-rs-%{version}-linux-x86_64" ;;
  aarch64) release_root="cua-driver-rs-%{version}-linux-arm64" ;;
esac
# The vendor tree stays together: cua-driver execs cua-cursor-theme as a
# sibling of the resolved binary, and the SDK library, node runtime, ABI
# header, and the GNOME wayland-helper extension are versioned with it. The
# private tree keeps the upstream /usr/lib path instead of %%{_libdir},
# mirroring the PKGBUILD exactly.
install -d %{buildroot}%{_prefix}/lib/cua-driver
cp -a "$release_root/." %{buildroot}%{_prefix}/lib/cua-driver/
chmod -R a+rX %{buildroot}%{_prefix}/lib/cua-driver
# The path the rewrite above wrote into the binary.
install -D -m 0755 pm.sh %{buildroot}%{_prefix}/lib/cua-driver/pm.sh
install -d %{buildroot}%{_bindir}
ln -s ../lib/cua-driver/cua-driver %{buildroot}%{_bindir}/cua-driver

%files
%license LICENSE
%{_prefix}/lib/cua-driver/
%{_bindir}/cua-driver

%changelog
* Thu Oct 01 2026 kamm3r - 0.28.2-1
- Repackage the upstream Omarchy Cua driver release for Fedora.
