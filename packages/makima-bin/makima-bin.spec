%global debug_package %{nil}

Name:           makima-bin
Version:        0.10.3
Release:        2%{?dist}
Summary:        Input remapping daemon for keyboards, mice and controllers
License:        GPL-3.0-or-later
URL:            https://github.com/cyber-sushi/makima
# Upstream ships a bare binary, not a tarball, so there is no top directory
# to autosetup; the file is renamed without an extension on download.
Source0:        %{url}/releases/download/v%{version}/makima#/%{name}-%{version}
ExclusiveArch:  x86_64
BuildRequires:  systemd-rpm-macros
Provides:       makima = %{version}-%{release}

%description
Linux daemon to remap and create macros for keyboards, mice and controllers.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" makima

%build
:

%install
install -D -m 0755 makima %{buildroot}%{_bindir}/makima
install -d %{buildroot}%{_udevrulesdir} %{buildroot}%{_modulesloaddir} %{buildroot}%{_unitdir}
echo 'SUBSYSTEM=="misc", KERNEL=="uinput", MODE="0660", GROUP="input", TAG+="uaccess"' > %{buildroot}%{_udevrulesdir}/50-makima.rules
echo 'uinput' > %{buildroot}%{_modulesloaddir}/uinput.conf
# Service template is verbatim from the upstream PKGBUILD. $USER is left
# unexpanded on purpose: the RPM build-time user must not leak into the unit.
cat > %{buildroot}%{_unitdir}/makima.service <<'EOF'
[Unit]
Description=Makima remapping daemon

[Service]
Type=simple
Environment="MAKIMA_CONFIG=/home/$USER/.config/makima"
ExecStart=/usr/bin/makima
Restart=always
RestartSec=3
User=$USER
Group=input

[Install]
WantedBy=default.target
EOF
chmod 0644 %{buildroot}%{_unitdir}/makima.service

%files
%{_bindir}/makima
%{_udevrulesdir}/50-makima.rules
%{_modulesloaddir}/uinput.conf
%{_unitdir}/makima.service

%changelog
* Sat Oct 03 2026 kamm3r - 0.10.3-2
- Require systemd RPM macros for service, udev and modules-load paths.

* Wed Sep 30 2026 kamm3r - 0.10.3-1
- Repackage the upstream Omarchy Makima release for Fedora.
