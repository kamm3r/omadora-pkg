%global debug_package %{nil}
%global __brp_python_bytecompile %{nil}
%global source_commit 844e34ead02328eff011b42b96a27329ef704c65
%global source_epoch 1791360001

Name:           ghost
Version:        0.6.0
Release:        1%{?dist}
Summary:        Ghost desktop HUD for Omadora
License:        Apache-2.0
URL:            https://github.com/ferdousbhai/ghost
Source0:        %{url}/releases/download/v%{version}/ghost-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/ghost-runtime-%{version}-linux-any.tar.zst
BuildArch:      noarch
BuildRequires:  bun >= 1.4.0
BuildRequires:  desktop-file-utils
BuildRequires:  python3
BuildRequires:  zstd
BuildRequires:  systemd-rpm-macros
Requires:       ghost-runtime = %{version}-%{release}
Requires:       omarchy
Requires:       qt6-qt5compat >= 6.8
Requires:       quickshell >= 0.3
Requires:       xdg-utils
Conflicts:      ghost-dev

%description
Ghost's desktop HUD integrates its AI assistant with the Omadora shell.
Enable the shipped plugin from your graphical user session using the
instructions in the package documentation.

%package runtime
Summary:        Ghost daemon, CLI, and desktop automation runtime
Requires:       at-spi2-core >= 2.58
Requires:       bun >= 1.3.14
Requires:       grim >= 1.5
Requires:       hyprland >= 0.56
Requires:       libnotify >= 0.8
Requires:       qrencode
Requires:       systemd
Requires:       wl-clipboard
Requires:       wtype >= 0.4
Recommends:     chromium
Recommends:     npm
Conflicts:      ghost-runtime-dev

%description runtime
Ghost's assistant daemon, authenticated API, CLI, and desktop/browser
automation runtime. It can be installed independently of the desktop HUD.

%prep
%setup -q
bash packaging/release/verify-release-source.sh "$PWD" "%{version}" "%{source_commit}" "%{source_epoch}"
mkdir runtime-artifact
tar -xf "%{SOURCE1}" -C runtime-artifact
bash packaging/release/verify-runtime-source.sh "$PWD/runtime-artifact/ghost-runtime-%{version}-linux-any" "$PWD" "%{version}" any "%{source_commit}" "%{source_epoch}"
# RPM assigns root ownership when it packs the payload; build users cannot
# chown staging files. Keep the upstream payload and smoke checks otherwise.
sed -i -e 's/ -o root -g root//g' -e '/^chown -hR 0:0 /d' packaging/release/install-payload.sh
sed -i 's/python -m json.tool/python3 -m json.tool/' packaging/arch/smoke.sh

%build
:

%check
desktop-file-validate packages/shell/contrib/ghost.desktop

%install
runtime_root="$PWD/runtime-artifact/ghost-runtime-%{version}-linux-any"
rm -rf runtime-root ui-root
bash packaging/release/install-payload.sh "$PWD" "$runtime_root" "$PWD/runtime-root" ghost-runtime runtime
bash packaging/release/install-payload.sh "$PWD" "$runtime_root" "$PWD/ui-root" ghost ui
cp -a runtime-root/. %{buildroot}/
cp -a ui-root/. %{buildroot}/

%files
%license %{_datadir}/licenses/ghost
%{_datadir}/ghost/plugin
%{_datadir}/applications/ghost.desktop
%{_datadir}/icons/hicolor/*/apps/ghost.*
%{_datadir}/doc/ghost/shell-contrib

%files runtime
%license %{_datadir}/licenses/ghost-runtime
%dir %{_datadir}/doc/ghost
%{_bindir}/ghost
%{_bindir}/ghostd
%{_bindir}/ghost-desktop
%{_prefix}/lib/ghost
%{_userunitdir}/ghostd.service
%{_datadir}/doc/ghost/ARCH.md
%{_datadir}/doc/ghost/README.md
%{_datadir}/doc/ghost/CONTRACTS.md
%{_datadir}/doc/ghost/THIRD_PARTY_NOTICES.md
%{_datadir}/doc/ghost/docs

%changelog
* Sat Oct 10 2026 kamm3r - 0.6.0-1
- Package the verified Ghost runtime and optional desktop HUD for Fedora.
