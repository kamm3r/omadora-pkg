%global debug_package %{nil}

Name:           dell-xps13-sidecar-amps
Version:        1.0.0
Release:        1%{?dist}
Summary:        Temporary sidecar speaker amplifier enablement for the Dell XPS 13 DX13260
License:        MIT
URL:            https://github.com/omacom-io/omarchy-pkgs
# Recipe files live in omarchy-pkgs (no tarball); pin each one to the upstream
# snapshot tracked in catalog.tsv so spectool fetches byte-exact sources.
Source0:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dell-xps13-sidecar-amps-apply#/dell-xps13-sidecar-amps-apply
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dell-xps13-sidecar-amps.conf#/dell-xps13-sidecar-amps.conf
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/LICENSE#/LICENSE
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/README.md#/README.md
ExclusiveArch:  x86_64
BuildArch:      noarch
# Upstream depends minus mkinitcpio: Omadora rebuilds boot images with the
# dracut-backed limine-mkinitcpio helper (see FEDORA.md), which lives in
# /usr/local/bin and cannot be an RPM dependency.
Requires:       bash
Requires:       coreutils
Requires:       kmod

%description
Temporary workaround enabling the two CS35L56 sidecar speaker amplifiers on
the Dell XPS 13 DX13260 (PCI subsystem 1028:0e53) via a snd_soc_sof_sdw
quirk override. Upstream Linux commit efd80de2de9d folds this machine into
the driver quirk table; remove this package once every bootable kernel
contains it. The install script (install/hardware/dell-xps13-sidecar-amps.sh)
installs this RPM only where dnf offers it.

%prep
cp %{SOURCE2} ./LICENSE
cp %{SOURCE3} ./README.md

%install
install -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/dell-xps13-sidecar-amps-apply
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/dell-xps13-sidecar-amps.conf

%post
# Mirrors the ALPM post_install/post_upgrade hooks: drop the superseded
# legacy override and rebuild the boot images so the quirk reaches the
# initramfs/UKIs. Never fail the transaction from here.
if /usr/bin/dell-xps13-sidecar-amps-apply; then
  echo ":: Reboot to enable the Dell XPS 13 sidecar speaker amplifiers."
else
  echo ":: dell-xps13-sidecar-amps-apply did not finish; run it as root before rebooting." >&2
fi

%postun
# Mirrors the ALPM post_remove hook: the drop-in leaves with the package, so
# rebuild once more on erase so no temporary quirk stays embedded.
if [ "$1" = "0" ]; then
  if command -v limine-mkinitcpio >/dev/null 2>&1; then
    limine-mkinitcpio || echo ":: Boot image rebuild failed; rerun limine-mkinitcpio as root." >&2
  fi
  echo ":: Reboot to finish removing the Dell XPS 13 sidecar amplifier workaround."
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/dell-xps13-sidecar-amps-apply
%{_prefix}/lib/modprobe.d/dell-xps13-sidecar-amps.conf

%changelog
* Thu Oct 01 2026 kamm3r - 1.0.0-1
- Port the upstream Omarchy sidecar amplifier workaround to Fedora (dracut
  rebuild helper instead of the mkinitcpio dependency).
