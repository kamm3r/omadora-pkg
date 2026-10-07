%global debug_package %{nil}

Name:           claude-code
Version:        2.1.289
Release:        1%{?dist}
Summary:        Agentic coding tool that lives in your terminal
License:        LicenseRef-claude-code
URL:            https://github.com/anthropics/claude-code
# Upstream ships a bare binary plus a legal notice, not a tarball, so there
# is no top directory to autosetup; the binary is renamed on download.
Source0:        https://downloads.claude.ai/claude-code-releases/%{version}/linux-x64/claude#/%{name}-%{version}
Source1:        https://code.claude.com/docs/en/legal-and-compliance.md#/%{name}-legal-%{version}.md
ExclusiveArch:  x86_64
Requires:       bash

%description
Claude Code is an agentic coding tool that lives in your terminal. This
package repacks the upstream binary release, with upstream self-update
paths disabled and the native-install health check suppressed, mirroring
the upstream PKGBUILD's wrapper script.

%prep
%setup -q -c -T -n %{name}-%{version}
cp "%{SOURCE0}" claude
cp "%{SOURCE1}" cc-legal.md

%build
:

%install
install -D -m 0755 claude %{buildroot}/opt/claude-code/bin/claude
install -d %{buildroot}%{_bindir}
# Wrapper script is verbatim from the upstream PKGBUILD: it disables
# upstream update paths and suppresses the native-install health check,
# since the package installs to /opt plus /usr/bin instead of ~/.local.
cat > %{buildroot}%{_bindir}/claude <<'EOF'
#!/bin/sh
export DISABLE_UPDATES=1
export DISABLE_INSTALLATION_CHECKS=1
exec /opt/claude-code/bin/claude "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/claude

%files
%license cc-legal.md
/opt/claude-code/bin/claude
%{_bindir}/claude

%changelog
* Tue Oct 06 2026 kamm3r - 2.1.289-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 2.1.283-1
- Repackage the upstream Omarchy Claude Code release for Fedora.
