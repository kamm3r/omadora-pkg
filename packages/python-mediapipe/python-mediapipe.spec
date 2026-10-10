# The optimized Bazel wheel has no collectable DWARF source paths.
# Keep native debuginfo, but do not declare an empty debug-source package.
%undefine _debugsource_packages

Name:           python-mediapipe
Version:        1.1.0
Release:        1%{?dist}
Summary:        Cross-platform customizable ML solutions for live and streaming media
License:        Apache-2.0
URL:            https://github.com/google-ai-edge/mediapipe
%global _bazel_version 7.4.1
%global omarchy_pkgs_commit 8787c23f0386eaf1df5ccd07b8402080da48b1ef
Source0:        https://github.com/google-ai-edge/mediapipe/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/bazelbuild/bazel/releases/download/%{_bazel_version}/bazel-%{_bazel_version}-linux-x86_64
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/python-mediapipe/0005-set-hermetic-python-version-and-disable-odml-converter.patch
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/python-mediapipe/0007-bump-rules-java.patch
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/python-mediapipe/0008-drop-semantic-retriever-from-libmediapipe.patch
ExclusiveArch:  x86_64
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  gcc-c++
BuildRequires:  patchelf
BuildRequires:  perl-interpreter
BuildRequires:  python3-build
BuildRequires:  python3-devel
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-rpm-macros
BuildRequires:  opencv-devel
Requires:       libgcc
Requires:       glibc
Requires:       libglvnd
Requires:       mesa-libGL
Requires:       opencv
Requires:       python3-attrs
Requires:       python3-flatbuffers
Requires:       python3-matplotlib
Requires:       python3-numpy
Requires:       python3-opencv
Requires:       python3-pillow
Requires:       python3-protobuf
Requires:       python3-scipy
Requires:       python3-six
Requires:       python3-sounddevice
Requires:       python3-absl
Provides:       python3-mediapipe = %{version}-%{release}
# Fedora 44 ships opencv 4.13 under /usr/include/opencv4, which is what
# upstream expects, so the Arch-only opencv5 header patches (0004, 0006) are
# intentionally dropped here; the hermetic-python, rules-java and semantic
# retriever removal fixes are carried. python-tensorflow stays out of
# Requires; the wheel links what the hermetic build needs.

%description
MediaPipe offers cross-platform, customizable machine learning solutions
for live and streaming media. This package builds the upstream wheel with a
pinned Bazel binary, mirroring the upstream Omarchy recipe.

%prep
%setup -q -n mediapipe-%{version}
# Bazel in Fedora (9.x) is too new for this tree; use the pinned upstream
# binary the Omarchy recipe uses.
mkdir -p bin
install -Dm755 "%{SOURCE1}" bin/bazel
patch -Np1 -i "%{SOURCE2}"
patch -Np1 -i "%{SOURCE3}"
patch -Np1 -i "%{SOURCE4}"
# set __version__
sed -i "s/__version__ = 'dev'/__version__ = '%{version}'/" setup.py
# Fedora provides cv2 as the opencv Python distribution.
sed -i 's/opencv-contrib-python/opencv/g' requirements.txt
# set link_opencv to True
sed -i "s/self.link_opencv = False/self.link_opencv = True/g" setup.py
# Upstream leaves the OpenCV 4 header rules commented out.
sed -i 's|#"include/opencv4/|"include/opencv4/|' third_party/opencv_linux.BUILD
# Stray characters in the upstream test prevent RPM's Python byte-compilation.
sed -i 's/0\.9624276,∂ç/0.9624276,/' mediapipe/tasks/python/test/text/text_embedder_test.py

%build
export PATH="$PWD/bin:$PATH"
MEDIAPIPE_DISABLE_GPU=0 \
  python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl
# remove rpath and fix permission
find %{buildroot} -type f -name "*.so" -exec patchelf --remove-rpath {} \;
find %{buildroot} -type f -name "*.so" -exec chmod 755 {} \;

%files
%license LICENSE
%{python3_sitearch}/mediapipe/
%{python3_sitearch}/mediapipe-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 kamm3r - 1.1.0-1
- Update to the release pinned in upstream 8787c23f.

* Sat Oct 03 2026 kamm3r - 1.0.0-3
- Add EGL and GLES development headers for the GPU-enabled wheel.
- Enable the system OpenCV 4 include rules in the Bazel target.
- Own the platform wheel under the Python architecture-specific directory.
- Add Perl for TensorFlow Lite's schema generation rule.
- Remove stray characters from the upstream text embedder test.
- Preserve native debuginfo without an empty Bazel debug-source package.
- Require Fedora's opencv distribution instead of the PyPI wheel name.

* Thu Oct 01 2026 kamm3r - 1.0.0-2
- Port the upstream Omarchy MediaPipe Python recipe to Fedora.
