%global debug_package %{nil}
# Prebuilt ONNX provider libs carry upstream build-host RPATHs
# (/home/runner/..., /opt/rocm-...); they are dlopened from their own
# directory and the RPATHs are harmless, so skip the check.
%global __brp_check_rpaths %{nil}
# Private ONNX runtime libs live under /usr/lib64/voxtype and are dlopened
# by path; keep them out of the RPM dependency namespace. GPU/GTK
# accelerator libs are optional at runtime (mirroring upstream optdepends),
# so exclude them from auto-Requires to keep the package installable
# without CUDA/ROCm.
%global __provides_exclude ^(libonnxruntime.*|libonnxruntime_providers_.*)$
%global __requires_exclude ^(libcublas.*|libcudart.*|libcudnn.*|libcufft.*|libcurand.*|libamdhip64.*|libmigraphx_c.*|libonnxruntime.*|libonnxruntime_providers_.*|libvulkan\.so.*|libgtk-4\.so.*|libgtk4-layer-shell.*)$

Name:           voxtype-bin
Version:        1.1.0
Release:        1%{?dist}
Summary:        Push-to-talk voice-to-text for Linux
License:        MIT
URL:            https://voxtype.io
Source0:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/config/default.toml#/%{name}-config-%{version}.toml
Source1:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/systemd/voxtype.service#/%{name}-service-%{version}
Source2:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/completions/voxtype.bash#/%{name}-bash-%{version}
Source3:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/completions/voxtype.zsh#/%{name}-zsh-%{version}
Source4:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/completions/voxtype.fish#/%{name}-fish-%{version}
Source5:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/LICENSE#/%{name}-LICENSE-%{version}
Source6:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/README.md#/%{name}-README-%{version}.md
Source7:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/voxtype-configure.desktop#/%{name}-configure-%{version}.desktop
Source8:        https://raw.githubusercontent.com/peteonrails/voxtype/v%{version}/packaging/scripts/voxtype-configure-launcher#/%{name}-configure-launcher-%{version}
Source9:        https://github.com/peteonrails/voxtype/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source10:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-baseline#/%{name}-%{version}-baseline
Source11:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-avx2#/%{name}-%{version}-avx2
Source12:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-avx512#/%{name}-%{version}-avx512
Source13:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-vulkan#/%{name}-%{version}-vulkan
Source14:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-avx2#/%{name}-%{version}-onnx-avx2
Source15:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-avx512#/%{name}-%{version}-onnx-avx512
Source16:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-12#/%{name}-%{version}-onnx-cuda-12
Source17:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-12.libonnxruntime_providers_cuda.so#/%{name}-%{version}-cuda-12-providers-cuda.so
Source18:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-12.libonnxruntime_providers_shared.so#/%{name}-%{version}-cuda-12-providers-shared.so
Source19:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-13#/%{name}-%{version}-onnx-cuda-13
Source20:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-13.libonnxruntime_providers_cuda.so#/%{name}-%{version}-cuda-13-providers-cuda.so
Source21:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-13.libonnxruntime_providers_shared.so#/%{name}-%{version}-cuda-13-providers-shared.so
Source22:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-cuda-13.libonnxruntime.so.1.24.4#/%{name}-%{version}-cuda-13-libonnxruntime.so.1.24.4
Source23:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-migraphx#/%{name}-%{version}-onnx-migraphx
Source24:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-migraphx.libonnxruntime_providers_migraphx.so#/%{name}-%{version}-migraphx-providers-migraphx.so
Source25:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-onnx-migraphx.libonnxruntime_providers_shared.so#/%{name}-%{version}-migraphx-providers-shared.so
Source26:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-osd#/%{name}-%{version}-osd
Source27:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-osd-gtk4#/%{name}-%{version}-osd-gtk4
Source28:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-osd-quickshell#/%{name}-%{version}-osd-quickshell
Source29:       https://github.com/peteonrails/voxtype/releases/download/v%{version}/voxtype-%{version}-linux-x86_64-audio-bridge#/%{name}-%{version}-audio-bridge
ExclusiveArch:  x86_64
Provides:       voxtype = %{version}-%{release}
Requires:       alsa-lib
Requires:       curl
Requires:       glibc
Requires:       libgcc

%description
Push-to-talk voice-to-text for Linux. This package repacks the upstream
pre-built binaries, mirroring the upstream PKGBUILD x86_64 layout.

%prep
%setup -q -c -T -n %{name}-%{version}
tar -xzf "%{SOURCE9}"
cp "%{SOURCE5}" LICENSE

%build
:

%install
install -D -m 0755 "%{SOURCE10}" %{buildroot}%{_libdir}/voxtype/voxtype-baseline
install -D -m 0755 "%{SOURCE11}" %{buildroot}%{_libdir}/voxtype/voxtype-avx2
install -D -m 0755 "%{SOURCE12}" %{buildroot}%{_libdir}/voxtype/voxtype-avx512
install -D -m 0755 "%{SOURCE13}" %{buildroot}%{_libdir}/voxtype/voxtype-vulkan
install -D -m 0755 "%{SOURCE14}" %{buildroot}%{_libdir}/voxtype/voxtype-onnx-avx2
install -D -m 0755 "%{SOURCE15}" %{buildroot}%{_libdir}/voxtype/voxtype-onnx-avx512
install -D -m 0755 "%{SOURCE16}" %{buildroot}%{_libdir}/voxtype/cuda-12/voxtype-onnx-cuda-12
install -D -m 0644 "%{SOURCE17}" %{buildroot}%{_libdir}/voxtype/cuda-12/libonnxruntime_providers_cuda.so
install -D -m 0644 "%{SOURCE18}" %{buildroot}%{_libdir}/voxtype/cuda-12/libonnxruntime_providers_shared.so
ln -sf cuda-12/voxtype-onnx-cuda-12 %{buildroot}%{_libdir}/voxtype/voxtype-onnx-cuda-12
install -D -m 0755 "%{SOURCE19}" %{buildroot}%{_libdir}/voxtype/cuda-13/voxtype-onnx-cuda-13
install -D -m 0644 "%{SOURCE20}" %{buildroot}%{_libdir}/voxtype/cuda-13/libonnxruntime_providers_cuda.so
install -D -m 0644 "%{SOURCE21}" %{buildroot}%{_libdir}/voxtype/cuda-13/libonnxruntime_providers_shared.so
install -D -m 0644 "%{SOURCE22}" %{buildroot}%{_libdir}/voxtype/cuda-13/libonnxruntime.so.1.24.4
ln -sf libonnxruntime.so.1.24.4 %{buildroot}%{_libdir}/voxtype/cuda-13/libonnxruntime.so
ln -sf cuda-13/voxtype-onnx-cuda-13 %{buildroot}%{_libdir}/voxtype/voxtype-onnx-cuda-13
install -D -m 0755 "%{SOURCE23}" %{buildroot}%{_libdir}/voxtype/migraphx/voxtype-onnx-migraphx
install -D -m 0644 "%{SOURCE24}" %{buildroot}%{_libdir}/voxtype/migraphx/libonnxruntime_providers_migraphx.so
install -D -m 0644 "%{SOURCE25}" %{buildroot}%{_libdir}/voxtype/migraphx/libonnxruntime_providers_shared.so
ln -sf migraphx/voxtype-onnx-migraphx %{buildroot}%{_libdir}/voxtype/voxtype-onnx-migraphx
ln -sf voxtype-onnx-migraphx %{buildroot}%{_libdir}/voxtype/voxtype-onnx-rocm
install -D -m 0755 "%{SOURCE26}" %{buildroot}%{_libdir}/voxtype/voxtype-osd
install -D -m 0755 "%{SOURCE27}" %{buildroot}%{_libdir}/voxtype/voxtype-osd-gtk4
install -D -m 0755 "%{SOURCE28}" %{buildroot}%{_libdir}/voxtype/voxtype-osd-quickshell
install -d %{buildroot}%{_bindir}
ln -sf %{_libdir}/voxtype/voxtype-osd %{buildroot}%{_bindir}/voxtype-osd
ln -sf %{_libdir}/voxtype/voxtype-avx2 %{buildroot}%{_bindir}/voxtype
ln -sf cuda-13/voxtype-onnx-cuda-13 %{buildroot}%{_libdir}/voxtype/voxtype-onnx-cuda
install -D -m 0755 "%{SOURCE29}" %{buildroot}%{_bindir}/voxtype-audio-bridge
install -d %{buildroot}%{_datadir}/voxtype
cp -a voxtype-%{version}/quickshell %{buildroot}%{_datadir}/voxtype/
find %{buildroot}%{_datadir}/voxtype/quickshell -type f -exec chmod 644 {} +
find %{buildroot}%{_datadir}/voxtype/quickshell -type d -exec chmod 755 {} +
install -d %{buildroot}%{_datadir}/voxtype/osd %{buildroot}%{_datadir}/voxtype/osd-recipes
cp -a voxtype-%{version}/examples/osd-packages/. %{buildroot}%{_datadir}/voxtype/osd/
find %{buildroot}%{_datadir}/voxtype/osd -type f -exec chmod 644 {} +
find %{buildroot}%{_datadir}/voxtype/osd -type d -exec chmod 755 {} +
cp -a voxtype-%{version}/examples/osd-recipes/. %{buildroot}%{_datadir}/voxtype/osd-recipes/
find %{buildroot}%{_datadir}/voxtype/osd-recipes -type f -exec chmod 644 {} +
find %{buildroot}%{_datadir}/voxtype/osd-recipes -type d -exec chmod 755 {} +
install -D -m 0755 "%{SOURCE8}" %{buildroot}%{_bindir}/voxtype-configure-launcher
install -D -m 0644 "%{SOURCE7}" %{buildroot}%{_datadir}/applications/voxtype-configure.desktop
install -D -m 0644 "%{SOURCE0}" %{buildroot}%{_sysconfdir}/voxtype/config.toml
install -D -m 0644 "%{SOURCE1}" %{buildroot}%{_prefix}/lib/systemd/user/voxtype.service
install -D -m 0644 "%{SOURCE6}" %{buildroot}%{_datadir}/doc/%{name}/README.md
install -D -m 0644 "%{SOURCE2}" %{buildroot}%{_datadir}/bash-completion/completions/voxtype
install -D -m 0644 "%{SOURCE3}" %{buildroot}%{_datadir}/zsh/site-functions/_voxtype
install -D -m 0644 "%{SOURCE4}" %{buildroot}%{_datadir}/fish/vendor_completions.d/voxtype.fish

%post
# Select the best CPU backend for /usr/bin/voxtype, mirroring the upstream
# PKGBUILD install hooks. Defaults to avx2; avx512 when supported, baseline
# otherwise. Preserves a user-selected GPU/ONNX backend across upgrades.
if [ -f /usr/bin/voxtype ]; then
  target=$(readlink -f /usr/bin/voxtype 2>/dev/null || echo "")
  case "$target" in
    */voxtype-onnx-*|*/cuda-*/voxtype-*|*/migraphx/voxtype-*) ;;
    *)
      if grep -q avx512f /proc/cpuinfo 2>/dev/null; then
        ln -sf %{_libdir}/voxtype/voxtype-avx512 /usr/bin/voxtype
      elif grep -q avx2 /proc/cpuinfo 2>/dev/null; then
        ln -sf %{_libdir}/voxtype/voxtype-avx2 /usr/bin/voxtype
      else
        ln -sf %{_libdir}/voxtype/voxtype-baseline /usr/bin/voxtype
      fi
      ;;
  esac
fi
# Point the unversioned onnx-cuda symlink at the variant matching the host
# CUDA runtime, defaulting to cuda-13 when undetectable.
if /sbin/ldconfig -p 2>/dev/null | grep -q "libcudart.so.12"; then
  ln -sf cuda-12/voxtype-onnx-cuda-12 %{_libdir}/voxtype/voxtype-onnx-cuda 2>/dev/null || true
elif [ -f %{_libdir}/voxtype/cuda-13/voxtype-onnx-cuda-13 ]; then
  ln -sf cuda-13/voxtype-onnx-cuda-13 %{_libdir}/voxtype/voxtype-onnx-cuda 2>/dev/null || true
fi

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/voxtype/config.toml
%{_bindir}/voxtype
%{_bindir}/voxtype-osd
%{_bindir}/voxtype-audio-bridge
%{_bindir}/voxtype-configure-launcher
%{_libdir}/voxtype/
%{_datadir}/voxtype/
%{_datadir}/applications/voxtype-configure.desktop
%{_prefix}/lib/systemd/user/voxtype.service
%{_datadir}/doc/%{name}/README.md
%{_datadir}/bash-completion/completions/voxtype
%{_datadir}/zsh/site-functions/_voxtype
%{_datadir}/fish/vendor_completions.d/voxtype.fish

%changelog
* Wed Sep 30 2026 kamm3r - 1.1.0-1
- Repackage the upstream Omarchy Voxtype release for Fedora.
