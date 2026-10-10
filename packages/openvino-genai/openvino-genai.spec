Name:           openvino-genai
Version:        2026.4.1.0
Release:        1%{?dist}
Summary:        OpenVINO GenAI C and C++ runtime libraries
License:        Apache-2.0
URL:            https://github.com/openvinotoolkit/openvino.genai
%global _commit ab01d1771e4adaa0e1e08e9d630def170572506c
%global _tokenizers_commit 9bfda52960774da1b9afafb37f8618673fe4d7c8
%global _openvino_version 2026.4.1
%global omarchy_pkgs_commit 8787c23f0386eaf1df5ccd07b8402080da48b1ef
Source0:        https://github.com/openvinotoolkit/openvino.genai/archive/%{_commit}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openvino-genai/gcc-16-char8_t.patch
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/openvino-genai/linear-attention-guard-constructor.patch
Source3:        https://github.com/openvinotoolkit/openvino_tokenizers/archive/%{_tokenizers_commit}.tar.gz#/%{name}-tokenizers-%{version}.tar.gz
Source4:        https://github.com/openvinotoolkit/openvino/archive/%{_openvino_version}/openvino-%{_openvino_version}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  openvino-devel = %{_openvino_version}
BuildRequires:  tbb-devel
Requires:       libgcc
Requires:       glibc
Requires:       tbb
Requires:       openvino = %{_openvino_version}
# Fedora 44 ships openvino 2025.1.0; build packages/openvino first to provide
# the matching 2026.4 runtime required by this recipe.

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
# Tokenizers uses public conversion interfaces that link against core runtime.
# Fedora's disabled ONNX/TF frontends omit these headers from the SDK.
mkdir frontend-headers
tar -xf "%{SOURCE4}" --wildcards --strip-components=6 -C frontend-headers \
  'openvino-%{_openvino_version}/src/frontends/onnx/frontend/include/*'
tar -xf "%{SOURCE4}" --wildcards --strip-components=5 -C frontend-headers \
  'openvino-%{_openvino_version}/src/frontends/tensorflow/include/*'

%build
# Keep source paths available to RPM's debugedit and debug-source collector.
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_FLAGS="$CXXFLAGS -I$PWD/frontend-headers" \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_INSTALL_BINDIR=%{_bindir} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
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
  python3 -c 'import ctypes; [ctypes.CDLL(n) for n in ("libopenvino_c.so", "libopenvino_genai.so", "libopenvino_tokenizers.so", "libopenvino_genai_c.so")]'

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
%license %{_datadir}/licenses/%{name}/LICENSE
%license %{_datadir}/licenses/%{name}/third-party-programs.txt
%license %{_datadir}/licenses/%{name}/openvino-tokenizers-LICENSE
%license %{_datadir}/licenses/%{name}/openvino-tokenizers-third-party-programs.txt
%{_libdir}/libopenvino_genai.so*
%{_libdir}/libopenvino_tokenizers.so*
%{_libdir}/libopenvino_genai_c.so*

%changelog
* Sat Oct 10 2026 kamm3r - 2026.4.1.0-1
- Update to the release pinned in upstream 8787c23f.
- Set install directories explicitly for the bundled PCRE2 configuration.

* Sat Oct 03 2026 kamm3r - 2026.4.0.0-2
- List installed license paths separately for RPM 6.
- Supply matching public frontend interfaces for the tokenizer extensions.
- Let RPM map native source paths when generating debug packages.

* Thu Oct 01 2026 kamm3r - 2026.4.0.0-1
- Port the upstream Omarchy OpenVINO GenAI runtime to Fedora.
