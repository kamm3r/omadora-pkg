%global upstream_name power-profiles-daemon
%global patches_ref 37c404a57f271a87163b9e628826b908100da965
Name:           omarchy-power-profiles-daemon
Version:        0.30
Release:        1%{?dist}
Summary:        Omarchy power profiles with ARM CPPC and boost support
License:        GPL-3.0-or-later
URL:            https://gitlab.freedesktop.org/upower/power-profiles-daemon
Source0:        %{url}/-/archive/%{version}/%{upstream_name}-%{version}.tar.gz
Patch0:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{patches_ref}/pkgbuilds/%{name}/nvidia-rtx-spark-power-profiles.patch
Patch1:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{patches_ref}/pkgbuilds/%{name}/balanced-performance-spelling.patch
Patch2:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{patches_ref}/pkgbuilds/%{name}/cpufreq-boost-driver.patch
Patch3:         https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{patches_ref}/pkgbuilds/%{name}/cpufreq-caps.patch
BuildRequires:  gcc meson systemd-rpm-macros
BuildRequires:  argparse-manpage python3dist(shtab)
BuildRequires:  pkgconfig(bash-completion) pkgconfig(gio-2.0) pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(polkit-gobject-1) pkgconfig(systemd) pkgconfig(upower-glib)
BuildRequires:  umockdev python3dist(python-dbusmock) python3dist(pygobject)
Requires:       python3-gobject-base
Provides:       power-profiles-daemon = %{version}-%{release}
Provides:       ppd-service
Conflicts:      ppd-service
Obsoletes:      power-profiles-daemon < 0.31

%description
Power profiles daemon with Omarchy's upstream patches for NVIDIA CPPC,
Apple Silicon boost control and Snapdragon frequency caps. Existing AMD
and Intel driver selection is preserved. Uses Fedora service integration.

%prep
%autosetup -n %{upstream_name}-%{version} -p1

%build
%meson -Dgtk_doc=false -Dpylint=disabled -Dzshcomp=%{_datadir}/zsh/site-functions -Dbashcomp=enabled -Dmanpage=enabled
%meson_build

%install
%meson_install
install -d %{buildroot}%{_localstatedir}/lib/power-profiles-daemon
sed -i '1c #!/usr/bin/python3' %{buildroot}%{_bindir}/powerprofilesctl

%check
# The hardware mock tests must not race each other, as in Fedora's own recipe.
%define _smp_build_ncpus 1
%meson_test

%post
%systemd_post power-profiles-daemon.service

%preun
%systemd_preun power-profiles-daemon.service

%postun
%systemd_postun_with_restart power-profiles-daemon.service

%files
%license COPYING
%doc README.md
%{_bindir}/powerprofilesctl
%{_libexecdir}/power-profiles-daemon
%{_unitdir}/power-profiles-daemon.service
%{_datadir}/dbus-1/system.d/*.PowerProfiles.conf
%{_datadir}/dbus-1/system-services/*.PowerProfiles.service
%{_datadir}/polkit-1/actions/power-profiles-daemon.policy
%dir %{_localstatedir}/lib/power-profiles-daemon
%{_mandir}/man1/powerprofilesctl.1*
%{_datadir}/bash-completion/completions/powerprofilesctl
%{_datadir}/zsh/site-functions/_powerprofilesctl
