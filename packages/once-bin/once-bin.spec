%global debug_package %{nil}

Name:           once-bin
Version:        0.3.3
Release:        1%{?dist}
Summary:        Manager for self-hosted web applications
License:        MIT
URL:            https://github.com/basecamp/once
# Upstream ships a bare binary plus a license file, not a tarball, so there
# is no top directory to autosetup.
Source0:        %{url}/releases/download/v%{version}/once-linux-amd64#/%{name}-%{version}-linux-amd64
Source1:        https://raw.githubusercontent.com/basecamp/once/v%{version}/MIT-LICENSE#/%{name}-MIT-LICENSE-%{version}
ExclusiveArch:  x86_64
Provides:       once = %{version}-%{release}
# PKGBUILD depends on 'docker'; Fedora has no such package, moby-engine and
# podman-docker are the docker-compatible daemons.
Requires:       (moby-engine or podman-docker)

%description
CLI/TUI for installing and managing self-hosted web applications.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" once
cp "%{SOURCE1}" MIT-LICENSE

%build
:

%install
install -D -m 0755 once %{buildroot}%{_bindir}/once
install -d %{buildroot}%{_unitdir}
# Unit file is verbatim from the upstream PKGBUILD's once-background.service.
cat > %{buildroot}%{_unitdir}/once-background.service <<'EOF'
[Unit]
Description=Once background tasks (once)
After=network.target docker.service

[Service]
Type=simple
Environment=ONCE_NO_SELF_UPDATE=1
ExecStart=/usr/bin/once background run --namespace once
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
chmod 0644 %{buildroot}%{_unitdir}/once-background.service

%post
echo ':: Enable the background service with: systemctl enable --now once-background.service'

%preun
if [ $1 -eq 0 ]; then
  systemctl disable --now once-background.service > /dev/null 2>&1 || :
fi

%files
%license MIT-LICENSE
%{_bindir}/once
%{_unitdir}/once-background.service

%changelog
* Wed Sep 30 2026 kamm3r - 0.3.3-1
- Repackage the upstream Omarchy Once release for Fedora.
