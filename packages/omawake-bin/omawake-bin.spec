%global debug_package %{nil}

Name:           omawake-bin
Version:        0.1.1
Release:        1%{?dist}
Summary:        Configurable local wake-word daemon (pre-built binary)
License:        MIT AND Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/jacob-vincent-mink/omawake
%global _appname omawake
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        %{url}/releases/download/v%{version}/%{_appname}-%{version}-linux-x86_64.tar.xz#/%{name}-%{version}-linux-x86_64.tar.xz
Source1:        %{url}/releases/download/v%{version}/%{_appname}-%{version}-linux-aarch64.tar.xz#/%{name}-%{version}-linux-aarch64.tar.xz
# Shared user-service cleanup helper from the upstream recipe (also used by
# omaspeak-bin). The ALPM PreTransaction hook that invoked it has no dnf
# equivalent; %%preun below calls it on erase instead.
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omawake-bin/package-remove#/%{_appname}-package-remove-%{version}
ExclusiveArch:  x86_64 aarch64
Provides:       %{_appname} = %{version}-%{release}
Requires:       alsa-lib
# PipeWire audio support (upstream optdepend on pipewire-audio).
Recommends:     pipewire
# Accelerator runtimes (upstream optdepends). Fedora ships none of them
# under these names at the required versions, so they stay hints only.
Suggests:       openvino
Suggests:       openvino-genai
Suggests:       openvino-intel-gpu-plugin
Suggests:       openvino-intel-npu-plugin
Suggests:       cuda
Suggests:       cudnn

%description
Omawake is a configurable local wake-word daemon. This package repacks
the upstream pre-built binary release, mirroring the upstream PKGBUILD.

%prep
%setup -q -c -T -n %{name}-%{version}
case "%{_arch}" in
  x86_64) tar -xf "%{SOURCE0}" ;;
  aarch64) tar -xf "%{SOURCE1}" ;;
  *) echo "Unsupported arch %{_arch} for %{name}" >&2; exit 1 ;;
esac
cp "%{SOURCE2}" package-remove

%build
:

%install
# The daemon resolves its audio.cpp provider from the executable-relative
# release layout, so the private library keeps the upstream /usr/lib path
# instead of %%{_libdir}, mirroring the PKGBUILD exactly.
applib=%{buildroot}%{_prefix}/lib/%{_appname}
case "%{_arch}" in
  x86_64) release_root="%{_appname}-%{version}-linux-x86_64" ;;
  aarch64) release_root="%{_appname}-%{version}-linux-aarch64" ;;
esac
install -D -m 0755 package-remove "$applib/package-remove"
install -D -m 0755 "$release_root/%{_appname}" %{buildroot}%{_bindir}/%{_appname}
install -D -m 0755 "$release_root/lib/libaudiocpp.so.0.1.0" "$applib/libaudiocpp.so.0.1.0"
ln -s libaudiocpp.so.0.1.0 "$applib/libaudiocpp.so.0"
ln -s libaudiocpp.so.0 "$applib/libaudiocpp.so"
install -D -m 0644 "$release_root/packaging/systemd/%{_appname}.service" %{buildroot}%{_prefix}/lib/systemd/user/%{_appname}.service
docdir=%{buildroot}%{_datadir}/doc/%{name}
install -d "$docdir"
for document in README.md INSTALL.md ACCELERATOR_SETUP.md CHANGELOG.md RELEASE_NOTES.md DEMO.md RUNTIME.md config.example.toml; do
  install -m 0644 "$release_root/$document" "$docdir/"
done
cp -a "$release_root/assets" "$release_root/benchmarks" "$docdir/"
install -d %{buildroot}%{_datadir}/licenses/%{name}
cp -a "$release_root/licenses/." %{buildroot}%{_datadir}/licenses/%{name}/

%post
if [ $1 -eq 1 ]; then
  echo ':: Run omawake setup to configure a model and runtime.'
  echo ':: The optional user service remains disabled; enable it only when desired.'
  echo ':: Accelerator instructions: /usr/share/doc/omawake-bin/ACCELERATOR_SETUP.md'
else
  echo ':: Run omawake setup check to verify the current configuration.'
fi

%preun
# Replicates the upstream ALPM remove hook: stop and remove owned user
# services before the package goes away. Erase only, never on upgrade.
if [ $1 -eq 0 ]; then
  %{_prefix}/lib/%{_appname}/package-remove %{_appname} || exit 1
fi

%files
%{_bindir}/%{_appname}
%{_prefix}/lib/%{_appname}/
%{_prefix}/lib/systemd/user/%{_appname}.service
%license %{_datadir}/licenses/%{name}/
%{_datadir}/doc/%{name}/

%changelog
* Thu Oct 01 2026 kamm3r - 0.1.1-1
- Repackage the upstream Omarchy Omawake release for Fedora.
