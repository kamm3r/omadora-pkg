%global debug_package %{nil}

Name:           dell-xps-touchpad-haptics
Version:        1.0.0
Release:        2%{?dist}
Summary:        Synaptics haptic touchpad presets for Dell XPS on Omarchy
License:        MIT
URL:            https://github.com/omacom-io/omarchy-pkgs
# Recipe files live in omarchy-pkgs (no tarball); pin each one to the upstream
# snapshot tracked in catalog.tsv so spectool fetches byte-exact sources.
Source0:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/99-dell-xps-touchpad-haptics.rules#/99-dell-xps-touchpad-haptics.rules
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/README.package.md#/README.package.md
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dell-xps-touchpad-haptics#/dell-xps-touchpad-haptics
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dell-xps-touchpad-haptics-daemon#/dell-xps-touchpad-haptics-daemon
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/29465fb750ed2b7a8b3f409cf1a61989ac2d3867/pkgbuilds/%{name}/dell-xps-touchpad-haptics.service#/dell-xps-touchpad-haptics.service
ExclusiveArch:  x86_64
BuildRequires:  systemd-rpm-macros
BuildArch:      noarch
# Upstream depends is just python (the CLI and daemon are bash/python3 with
# stdlib only); systemd owns the unit/udev/preset machinery used below.
Requires:       python3
Requires:       systemd
Requires:       util-linux-core
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# Carries the old Arch package name like the PKGBUILD provides entry does.
Provides:       omarchy-dell-haptic-touchpad

%description
Synaptics haptic touchpad daemon and preset CLI for Dell XPS laptops: a
systemd service drives the Manual Trigger gain, udev rules keep the
controller powered, and dell-xps-touchpad-haptics switches low/mid/high
presets. The menu touchpad-haptics triggers and
install/hardware/dell-xps-touchpad-haptics.sh light up once this RPM is
installable.

%prep
cp %{SOURCE1} ./README.package.md

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_prefix}/lib/udev/rules.d/99-dell-xps-touchpad-haptics.rules
install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/dell-xps-touchpad-haptics
install -D -m 0755 %{SOURCE3} %{buildroot}%{_bindir}/dell-xps-touchpad-haptics-daemon
install -D -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/dell-xps-touchpad-haptics.service

%post
# Fedora port of the ALPM post_install/post_upgrade hook
# (dell-xps-touchpad-haptics.install): pick the desktop user, write the
# daemon env file, seed its config, and enable/start the service. Unit and
# udev reloads ride along with the rpm/systemd file triggers, so this only
# does the parts triggers cannot. Never fail the transaction here.
_haptics_env=/etc/dell-xps-touchpad-haptics.env
_haptics_service=dell-xps-touchpad-haptics.service
_haptics_user=""
if [[ -n ${SUDO_USER:-} && ${SUDO_USER} != "root" ]]; then
  _haptics_user=${SUDO_USER}
elif command -v logname >/dev/null 2>&1; then
  _haptics_user=$(logname 2>/dev/null || true)
  [[ ${_haptics_user} == "root" ]] && _haptics_user=""
fi
if [[ -z ${_haptics_user} ]] && command -v loginctl >/dev/null 2>&1; then
  _haptics_user=$(loginctl list-users --no-legend 2>/dev/null | awk '$2 != "root" && $4 == "active" { print $2; exit }')
fi
if [[ -z ${_haptics_user} ]]; then
  _haptics_user=$(getent passwd | awk -F: '$3 >= 1000 && $1 != "nobody" && $7 !~ /(nologin|false)$/ { print $1; exit }')
fi
# Drop state from the renamed omarchy-dell-haptic-touchpad package.
rm -f /etc/omarchy-dell-haptic-touchpad.env
rm -f /etc/systemd/system/dell-xps-haptic-touchpad.service.d/override.conf
rmdir /etc/systemd/system/dell-xps-haptic-touchpad.service.d 2>/dev/null || :
if [[ -n ${_haptics_user} ]]; then
  _haptics_home=$(getent passwd "${_haptics_user}" | cut -d: -f6)
  if [[ -n ${_haptics_home} && -d ${_haptics_home} ]]; then
    _haptics_tmp=$(mktemp)
    printf 'DELL_XPS_TOUCHPAD_HAPTICS_HOME=%%s\n' "${_haptics_home}" >"${_haptics_tmp}"
    install -D -m 644 "${_haptics_tmp}" "${_haptics_env}"
    rm -f "${_haptics_tmp}"
    if [[ ! -f ${_haptics_home}/.config/omarchy/dell-haptic.conf ]]; then
      runuser --user "${_haptics_user}" -- /usr/bin/env HOME="${_haptics_home}" USER="${_haptics_user}" LOGNAME="${_haptics_user}" /usr/bin/dell-xps-touchpad-haptics set high || echo ":: Could not seed ${_haptics_home}/.config/omarchy/dell-haptic.conf." >&2
    fi
  else
    echo ":: No usable home for user '${_haptics_user}'; skipping ${_haptics_env}." >&2
  fi
else
  echo ":: No desktop user found; reinstall after logging in to finish setup." >&2
fi
if command -v omarchy-restart-trackpad >/dev/null 2>&1; then
  omarchy-restart-trackpad 2>/dev/null || :
fi
systemctl enable "${_haptics_service}" >/dev/null 2>&1 || echo ":: Failed to enable ${_haptics_service}." >&2
if [[ -d /run/systemd/system ]]; then
  systemctl restart "${_haptics_service}" >/dev/null 2>&1 || echo ":: Failed to start ${_haptics_service}." >&2
else
  echo ":: ${_haptics_service} enabled; it will start on next boot."
fi

%preun
# Mirrors the ALPM pre_remove hook.
if [ "$1" = "0" ]; then
  systemctl disable dell-xps-touchpad-haptics.service >/dev/null 2>&1 || :
  systemctl stop dell-xps-touchpad-haptics.service >/dev/null 2>&1 || :
fi

%postun
# Mirrors the ALPM post_remove hook; reloads ride with file triggers.
if [ "$1" = "0" ]; then
  rm -f /etc/dell-xps-touchpad-haptics.env
fi

%files
# Upstream ships no license file (license is declared in PKGBUILD metadata).
%doc README.package.md
%{_bindir}/dell-xps-touchpad-haptics
%{_bindir}/dell-xps-touchpad-haptics-daemon
%{_prefix}/lib/udev/rules.d/99-dell-xps-touchpad-haptics.rules
%{_unitdir}/dell-xps-touchpad-haptics.service

%changelog
* Sat Oct 03 2026 kamm3r - 1.0.0-2
- Require systemd RPM macros for the service path.

* Thu Oct 01 2026 kamm3r - 1.0.0-1
- Port the upstream Omarchy haptic touchpad daemon to Fedora (RPM
  scriptlets replace the ALPM install hook; reloads via file triggers).
