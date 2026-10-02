Name:           openvino-genai
Version:        2026.4.0.0
Release:        1%{?dist}
Summary:        OpenVINO GenAI C and C++ runtime libraries
License:        Apache-2.0
URL:            https://github.com/openvinotoolkit/openvino.genai
%global _commit 7ea2546852a382cd16bd22dea0cfad2db70ed744
%global _tokenizers_commit a04accf6282d9b304214b492694b18c3979f667a
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867
Source0:        https://github.com/openvinotoolkit/openvino.genai/archive/%{_commit}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openvino-genai/gcc-16-char8_t.patch
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openvino-genai/linear-attention-guard-constructor.patch
Source3:        https://github.com/openvinotoolkit/openvino_tokenizers/archive/%{_tokenizers_commit}.tar.gz#/%{name}-tokenizers-%{version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  openvino-devel >= 2026.4.0
BuildRequires:  tbb-devel
Requires:       libgcc
Requires:       glibc
Requires:       tbb
Requires:       openvino >= 2026.4.0
# Fedora 44 ships openvino 2025.1.0; this recipe tracks upstream 2026.4.0 and
# stays uninstallable until the newer runtime lands (mirrors the upstream
# PKGBUILD exact openvino=2026.4.0 dependency).

%description
OpenVINO GenAI C and C++ runtime libraries. This package builds the upstream
commit pinned by the Omarchy recipe, with its gcc-16 and linear-attention
fixes, and ships only the C/C++ runtime libraries (no Python, JS, samples,
or tools).

%prep
%setup -q -n openvino.genai-%{_commit}
# The GitHub archive omits the thirdparty/openvino_tokenizers submodule
# (empty dir); fill it from its pinned commit (mirrors upstream's
# git submodule update --init --recursive).
rmdir thirdparty/openvino_tokenizers
mkdir -p thirdparty/openvino_tokenizers
tar -xzf "%{SOURCE3}" --strip-components=1 -C thirdparty/openvino_tokenizers
patch -Np1 -i "%{SOURCE1}"
patch -Np1 -i "%{SOURCE2}"

%build
CFLAGS="$RPM_OPT_FLAGS -ffile-prefix-map=$PWD=/usr/src/%{name}"
CXXFLAGS="$RPM_OPT_FLAGS -ffile-prefix-map=$PWD=/usr/src/%{name}"
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_SKIP_RPATH=ON \
  -DENABLE_JS=OFF \
  -DENABLE_MISAKI_CPP=OFF \
  -DENABLE_PYTHON=OFF \
  -DENABLE_SAMPLES=OFF \
  -DENABLE_TESTS=OFF \
  -DENABLE_TOOLS=OFF \
  -DENABLE_XGRAMMAR=OFF
cmake --build build

%check
LD_LIBRARY_PATH="$PWD/build/openvino_genai:$PWD/build/src/c${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  python3 -c 'import ctypes; ctypes.CDLL("libopenvino_c.so"); ctypes.CDLL("libopenvino_genai_c.so")'

%install
install -d %{buildroot}%{_libdir} %{buildroot}%{_datadir}/licenses/%{name}
cp -a build/openvino_genai/libopenvino_genai.so* %{buildroot}%{_libdir}/
cp -a build/openvino_genai/libopenvino_tokenizers.so* %{buildroot}%{_libdir}/
cp -a build/src/c/libopenvino_genai_c.so* %{buildroot}%{_libdir}/
# Consumers such as omawake load the unversioned name dynamically.
# Reject a missing/empty library or a broken symlink before publishing.
if [ ! -s "%{buildroot}%{_libdir}/libopenvino_genai_c.so" ]; then
  echo 'Required C binding is missing or empty: libopenvino_genai_c.so' >&2
  exit 1
fi
install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dm644 third-party-programs.txt %{buildroot}%{_datadir}/licenses/%{name}/third-party-programs.txt
install -Dm644 thirdparty/openvino_tokenizers/LICENSE %{buildroot}%{_datadir}/licenses/%{name}/openvino-tokenizers-LICENSE
install -Dm644 thirdparty/openvino_tokenizers/third-party-programs.txt %{buildroot}%{_datadir}/licenses/%{name}/openvino-tokenizers-third-party-programs.txt

%files
%license %{_datadir}/licenses/%{name}/LICENSE %{_datadir}/licenses/%{name}/third-party-programs.txt %{_datadir}/licenses/%{name}/openvino-tokenizers-LICENSE %{_datadir}/licenses/%{name}/openvino-tokenizers-third-party-programs.txt
%{_libdir}/libopenvino_genai.so*
%{_libdir}/libopenvino_tokenizers.so*
%{_libdir}/libopenvino_genai_c.so*

%changelog
* Thu Oct 01 2026 kamm3r - 2026.4.0.0-1
- Port the upstream Omarchy OpenVINO GenAI runtime to Fedora.
