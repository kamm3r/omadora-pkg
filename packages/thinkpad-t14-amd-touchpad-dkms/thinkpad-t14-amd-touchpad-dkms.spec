%global debug_package %{nil}
%global module_name thinkpad-t14-amd-touchpad
%global omarchy_pkgs_commit d9ebd3f6e196ffb6fed494eb0d241e4d654b1f2a

Name:           thinkpad-t14-amd-touchpad-dkms
Version:        0.2.3
Release:        1%{?dist}
Summary:        RMI4 touchpad support for ThinkPad T14 and P14s AMD laptops
License:        GPL-2.0-only
URL:            https://github.com/orospakr/thinkpad-t14-amd-touchpad
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/%{name}/%{module_name}.conf#/%{module_name}.conf
ExclusiveArch:  x86_64
BuildArch:      noarch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  python3
BuildRequires:  kernel-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:  openssl-devel
Requires:       dkms
Requires:       gcc
Requires:       make
Requires:       patch
Conflicts:      i2c-piix4-asf-dkms

%description
Patched i2c-piix4, rmi_smbus and psmouse modules enable RMI4/SMBus touchpad
operation on ThinkPad T14 and P14s Gen 1 and Gen 2 AMD laptops. DKMS
builds the modules for the installed kernel. A build against Fedora's
kernel development files validates the carried sources and patches.

%prep
%autosetup -n %{module_name}-%{version}

%build
:

%check
cp -a . ../module-check
pushd ../module-check
python3 - <<'PY'
import pathlib, re, subprocess
config = pathlib.Path("dkms.conf").read_text()
for patch in re.findall(r'^PATCH\[\d+\]="([^"]+)"', config, re.M):
    subprocess.run(["patch", "-p1", "--batch", "-i", "patches/" + patch], check=True)
PY
kernel_version=$(rpm -q kernel-devel --qf '%%{VERSION}-%%{RELEASE}.%%{ARCH}\n' | sort -V | tail -1)
bash tools/pre-build.sh "$kernel_version"
make -C /usr/src/kernels/"$kernel_version" M="$PWD" modules -j%{_smp_build_ncpus}
test -s drivers/i2c/busses/i2c-piix4.ko
test -s drivers/input/rmi4/rmi_smbus.ko
test -s drivers/input/mouse/psmouse.ko
echo "PASS: all three touchpad modules build against Fedora kernel $kernel_version"
popd

%install
dest=%{buildroot}%{_prefix}/src/%{module_name}-%{version}
install -d "$dest"
cp -a drivers patches tools "$dest/"
rm -rf "$dest/tools/check" "$dest/tools/ci"
install -m 0644 dkms.conf Makefile KERNEL_SOURCE "$dest/"
install -D -m 0755 tools/check %{buildroot}%{_bindir}/%{module_name}-check
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/%{module_name}.conf

%post
dkms add -m %{module_name} -v %{version} -q --rpm_safe_upgrade || :
dkms build -m %{module_name} -v %{version} -q || :
dkms install -m %{module_name} -v %{version} -q || :

%preun
dkms remove -m %{module_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md
%{_prefix}/src/%{module_name}-%{version}
%{_bindir}/%{module_name}-check
%{_prefix}/lib/modprobe.d/%{module_name}.conf

%changelog
* Thu Oct 15 2026 kamm3r - 0.2.3-1
- Port the ThinkPad AMD touchpad modules and verify compilation on Fedora.
