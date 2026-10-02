Epoch:           1
Name:           vi
Version:        070224
Release:        9%{?dist}
Summary:        The original ex/vi text editor
License:        BSD-4-Clause-UC AND Caldera-no-preamble
URL:            https://ex-vi.sourceforge.net/
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://sources.archlinux.org/other/vi/ex-%{version}.tar.xz#/%{name}-%{version}.tar.xz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/vi/fix-tubesize-short-overflow.patch
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/vi/navkeys.patch
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/vi/format-security.patch
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/vi/linenum.patch
Source5:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/vi/preserve-dir.patch
ExclusiveArch:  x86_64 aarch64
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
Requires:       ncurses
# Upstream installs /usr/bin/vi plus ex/edit/vedit/view symlinks; on Fedora
# vim-minimal owns /usr/bin/vi, so this package file-conflicts with it.
# Install with --allowerasing or remove vim-minimal first (mirrors the
# upstream PKGBUILD provides/conflicts split).

%description
The original ex/vi text editor. This package builds the traditional ex/vi
sources with the same feature set and preserve-directory layout as the
upstream Omarchy recipe.

%prep
%setup -q -n ex-%{version}
# Extract the two license texts from the bundled LICENSE, mirroring the
# upstream PKGBUILD prepare step.
sed -n '1,36p' LICENSE > BSD-4-Clause-UC.txt
sed -n '39,69p' LICENSE > Caldera-no-preamble.txt
patch -Np1 -i "%{SOURCE1}"
patch -Np1 -i "%{SOURCE2}"
patch -Np1 -i "%{SOURCE3}"
patch -Np1 -i "%{SOURCE4}"
patch -Np1 -i "%{SOURCE5}"

%build
export CFLAGS="$RPM_OPT_FLAGS -std=gnu90"
make PREFIX=/usr LIBEXECDIR=/usr/lib/ex PRESERVEDIR=/var/lib/ex \
  TERMLIB=ncurses FEATURES="-DCHDIR -DFASTTAG -DUCVISUAL -DMB -DBIT8"

%install
make PREFIX=/usr LIBEXECDIR=/usr/lib/ex PRESERVEDIR=/var/lib/ex \
  INSTALL=/usr/bin/install DESTDIR=%{buildroot} install
install -vDm 644 BSD-4-Clause-UC.txt Caldera-no-preamble.txt -t "%{buildroot}%{_datadir}/licenses/%{name}/"
# The Makefile creates the preserve dir with mode 1777; keep it in the RPM.
chmod 1777 %{buildroot}/var/lib/ex

%files
%license %{_datadir}/licenses/%{name}/BSD-4-Clause-UC.txt %{_datadir}/licenses/%{name}/Caldera-no-preamble.txt
%{_bindir}/ex
%{_bindir}/edit
%{_bindir}/vedit
%{_bindir}/vi
%{_bindir}/view
%{_prefix}/lib/ex/expreserve
%{_prefix}/lib/ex/exrecover
%{_mandir}/man1/ex.1*
%{_mandir}/man1/edit.1*
%{_mandir}/man1/vedit.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%dir %attr(1777,root,root) /var/lib/ex

%changelog
* Thu Oct 01 2026 kamm3r - 1:070224-9
- Port the upstream Omarchy original ex/vi recipe to Fedora.
