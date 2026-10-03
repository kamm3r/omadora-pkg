Name:           link-studio
Version:        1.0.4
Release:        2%{?dist}
Summary:        Native Linux controller for Insta360 Link webcams
License:        MIT
URL:            https://jweaver60.github.io/link-studio/
Source0:        https://github.com/jweaver60/link-studio/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-rpm-macros
# Test-only dependencies for the unittest suite in %check.
BuildRequires:  gobject-introspection
BuildRequires:  gtk4
BuildRequires:  libadwaita
BuildRequires:  gstreamer1
BuildRequires:  python3-gobject
BuildRequires:  python3-numpy
BuildRequires:  python3-opencv
Requires:       gtk4
Requires:       gstreamer1-libav
Requires:       gstreamer1-plugins-bad-free
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       libadwaita
Requires:       python3-gobject
Requires:       python3-mediapipe
Requires:       python3-numpy
Requires:       python3-opencv
Requires:       python3-pillow
Requires:       python3-qrcode
Requires:       v4l-utils
# Processed virtual-camera output needs a loopback device; the module itself
# is not in Fedora proper (RPM Fusion ships akmod-v4l2loopback), so this
# stays a weak dependency.
Recommends:     v4l2loopback

%description
Link Studio controls Insta360 Link webcams on Linux, with camera controls,
a processed virtual-camera output, and offline transcription helpers.

%prep
# The release tarball uses an underscore root (link_studio-VERSION).
%autosetup -n link_studio-%{version}

%build
python3 -m build --wheel --no-isolation

%check
PYTHONPATH=src python3 -m unittest discover -v

%install
python3 -m installer --destdir=%{buildroot} --prefix=/usr dist/*.whl
# Upstream rewrites the entry-point shebang to /usr/bin/python (an Archism);
# Fedora only guarantees /usr/bin/python3.
sed -i '1c#!/usr/bin/python3' %{buildroot}%{_bindir}/link-studio
install -D -m 0644 data/io.github.linkstudio.LinkStudio.desktop %{buildroot}%{_datadir}/applications/io.github.linkstudio.LinkStudio.desktop
install -D -m 0644 data/io.github.linkstudio.LinkStudio.metainfo.xml %{buildroot}%{_datadir}/metainfo/io.github.linkstudio.LinkStudio.metainfo.xml
install -D -m 0755 scripts/setup-virtual-camera %{buildroot}%{_bindir}/link-studio-setup-virtual-camera
install -D -m 0755 scripts/setup-local-ai %{buildroot}%{_bindir}/link-studio-setup-local-ai

%files
%license LICENSE THIRD_PARTY_NOTICES.md
%doc README.md docs/PARITY.md
%{_bindir}/link-studio
%{_bindir}/link-studio-setup-virtual-camera
%{_bindir}/link-studio-setup-local-ai
%{python3_sitelib}/link_studio
%{python3_sitelib}/link_studio-%{version}.dist-info
%{_datadir}/applications/io.github.linkstudio.LinkStudio.desktop
%{_datadir}/metainfo/io.github.linkstudio.LinkStudio.metainfo.xml

%changelog
* Sat Oct 03 2026 kamm3r - 1.0.4-2
- Install GTK and Adwaita typelibs for the test suite.

* Wed Sep 30 2026 kamm3r - 1.0.4-1
- Port the upstream Omarchy Link Studio recipe to Fedora.
