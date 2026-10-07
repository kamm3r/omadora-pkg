%global debug_package %{nil}
# /opt/1Password bundles its own Electron runtime plus private libraries.
# Keep those out of the RPM dependency namespace; system libraries stay
# explicitly required below.
%global __provides_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|op_sdk.*)\\.so
%global __requires_exclude ^lib(EGL|GLESv2|ffmpeg|vk_swiftshader|vulkan|op_sdk.*)\\.so

Name:           1password
Version:        8.12.38
Release:        1%{?dist}
Summary:        Password manager and secure wallet
License:        LicenseRef-1Password
URL:            https://1password.com
Source0:        https://downloads.1password.com/linux/tar/stable/x86_64/1password-%{version}.x64.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch:  x86_64
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       nss
Requires:       polkit
Requires:       xdg-utils
Requires(pre):  shadow-utils

%description
1Password is a password manager and secure wallet. This package repacks
the upstream binary release, mirroring the upstream PKGBUILD.

%prep
%autosetup -n 1password-%{version}.x64

%build
:

%install
# Icons and desktop entry, mirroring the upstream PKGBUILD.
for res in 32x32 64x64 256x256 512x512; do
  install -D -m 0644 resources/icons/hicolor/${res}/apps/1password.png %{buildroot}%{_datadir}/icons/hicolor/${res}/apps/1password.png
done
install -D -m 0644 resources/com.onepassword.OnePassword.desktop %{buildroot}%{_datadir}/applications/1password.desktop
# 1Password reads the display scale itself, the way Electron apps do, and
# comes up oversized next to every other window on a scaled monitor. Pin it
# and let the compositor do the scaling. NOTE: %%U below is an escaped %U
# for the RPM parser; the installed desktop file sees %U.
sed -i 's|^Exec=.*|Exec=/opt/1Password/1password --force-device-scale-factor=1 %%U|' %{buildroot}%{_datadir}/applications/1password.desktop

# Fill in policy kit file with a list of (the first 10) human users of the
# system, mirroring the upstream PKGBUILD (which expands the template at
# package time from the builder passwd).
export POLICY_OWNERS
POLICY_OWNERS="$(cut -d: -f1,3 /etc/passwd | grep -E ':[0-9]{4}$' | cut -d: -f1 | head -n 10 | sed 's/^/unix-user:/' | tr '\n' ' ')"
eval "cat <<EOF
$(cat ./com.1password.1Password.policy.tpl)
EOF" > ./com.1password.1Password.policy
install -D -m 0644 com.1password.1Password.policy -t %{buildroot}%{_datadir}/polkit-1/actions/
install -D -m 0644 resources/custom_allowed_browsers -t %{buildroot}%{_datadir}/doc/1password/examples/

# Move package contents to /opt/1Password, mirroring the upstream PKGBUILD.
install -d %{buildroot}/opt
cp -a . %{buildroot}/opt/1Password

# Cleanup un-needed files, mirroring the upstream PKGBUILD.
rm %{buildroot}/opt/1Password/com.1password.1Password.policy %{buildroot}/opt/1Password/com.1password.1Password.policy.tpl %{buildroot}/opt/1Password/install_biometrics_policy.sh
rm -r %{buildroot}/opt/1Password/resources/icons/
rm %{buildroot}/opt/1Password/resources/com.onepassword.OnePassword.desktop %{buildroot}/opt/1Password/resources/custom_allowed_browsers

# Symlink /usr/bin executable to opt, mirroring the upstream PKGBUILD.
install -d %{buildroot}%{_bindir}
ln -s /opt/1Password/1password %{buildroot}%{_bindir}/1password

# chrome-sandbox requires the setuid bit to be specifically set.
chmod 4755 %{buildroot}/opt/1Password/chrome-sandbox

%pre
getent group onepassword >/dev/null || groupadd -r onepassword

%post
chgrp onepassword /opt/1Password/1Password-BrowserSupport
chmod g+s /opt/1Password/1Password-BrowserSupport

%postun
if [[ $1 == 0 ]]; then
  groupdel onepassword 2>/dev/null || :
fi

%files
/opt/1Password
%{_bindir}/1password
%{_datadir}/applications/1password.desktop
%{_datadir}/icons/hicolor/*/apps/1password.png
%{_datadir}/polkit-1/actions/com.1password.1Password.policy
%{_datadir}/doc/1password/examples/custom_allowed_browsers

%changelog
* Tue Oct 06 2026 kamm3r - 8.12.38-1
- Update to the release pinned on upstream master.

* Thu Oct 01 2026 kamm3r - 8.12.36-1
- Repackage the upstream Omarchy release for Fedora.
