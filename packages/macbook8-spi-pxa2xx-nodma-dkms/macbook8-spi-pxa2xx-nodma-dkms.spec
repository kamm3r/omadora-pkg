%global debug_package %{nil}
%global _pkgbase spi-pxa2xx-pci-nodma

Name:           macbook8-spi-pxa2xx-nodma-dkms
Version:        1.0
Release:        1%{?dist}
Summary:        Patched SPI PXA2xx PCI driver forcing PIO mode for MacBook8,1
License:        GPL-2.0-only
URL:            https://github.com/basecamp/omarchy
# Recipe files live in omarchy-pkgs (no tarball); pin each one to the upstream
# snapshot tracked in catalog.tsv so spectool fetches byte-exact sources.
Source0:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/spi-pxa2xx-pci-nodma.c#/spi-pxa2xx-pci-nodma.c
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/spi-pxa2xx.h#/spi-pxa2xx.h
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/Makefile#/Makefile
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dkms.conf#/dkms.conf
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/macbook8-spi-nodma.conf#/macbook8-spi-nodma.conf
ExclusiveArch:  x86_64
BuildArch:      noarch
# The module compiles on the target machine via DKMS (AUTOINSTALL=yes in
# dkms.conf, and dkms itself pulls the matched kernel-devel), so there is no
# kernel-devel BuildRequires here. The toolchain mirrors the Fedora DKMS
# precedent (dkms-rtl8821cu).
Requires:       bc
Requires:       dkms
Requires:       gcc
Requires:       make
# Upstream's conflicts name the in-tree module (spi_pxa2xx_pci), not an RPM,
# so there is nothing to conflict with here. macbook12-spi-driver-dkms is
# not-applicable on Fedora (dracut add_drivers covers it).

%description
PIO-mode override of the in-tree SPI PXA2xx PCI glue driver for the
MacBook8,1 (2015 12-inch Retina) Wildcat Point GSPI (8086:9ce6), whose
keyboard and trackpad need IRQ-polled PIO instead of DMA. The DKMS module
builds as spi_pxa2xx_pci_nodma against the running kernel, while the shipped
modprobe drop-in blacklists the in-tree spi_pxa2xx_pci so this version binds
the device instead. The module is unsigned, so hosts with Secure Boot enabled
must enroll their own Machine Owner Key and sign it before it will load.

%prep
# Sources are installed verbatim; nothing to unpack.

%build
# The kernel module builds on the target machine via DKMS, not here.

%install
install -d %{buildroot}%{_prefix}/src/%{_pkgbase}-%{version}
install -D -m 0644 %{SOURCE0} %{buildroot}%{_prefix}/src/%{_pkgbase}-%{version}/spi-pxa2xx-pci-nodma.c
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/src/%{_pkgbase}-%{version}/spi-pxa2xx.h
install -D -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/src/%{_pkgbase}-%{version}/Makefile
install -D -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/src/%{_pkgbase}-%{version}/dkms.conf
install -D -m 0644 %{SOURCE4} %{buildroot}%{_prefix}/lib/modprobe.d/macbook8-spi-nodma.conf

%post
dkms add -m %{_pkgbase} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{_pkgbase} -v %{version} -q || :
dkms install -m %{_pkgbase} -v %{version} -q --force || :

%preun
# Remove all versions from the DKMS registry:
dkms remove -m %{_pkgbase} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_prefix}/src/%{_pkgbase}-%{version}/
%{_prefix}/lib/modprobe.d/macbook8-spi-nodma.conf

%changelog
* Thu Oct 01 2026 kamm3r - 1.0-1
- Port the upstream Omarchy MacBook8,1 SPI PIO-mode DKMS override to Fedora.
