%global debug_package %{nil}

Name:           claude-code
Version:        2.1.312
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
* Wed Oct 28 2026 kamm3r - 2.1.312-1
- Update to the release pinned in upstream aa38eb00.

* Tue Oct 27 2026 kamm3r - 2.1.311-1
- Update to the release pinned in upstream a18022b7.

* Mon Oct 26 2026 kamm3r - 2.1.310-1
- Update to the release pinned in upstream d5e4ad59.

* Fri Oct 23 2026 kamm3r - 2.1.309-1
- Update to the release pinned in upstream 5cf42189.

* Thu Oct 22 2026 kamm3r - 2.1.308-1
- Update to the release pinned in upstream de5c031f.

* Wed Oct 21 2026 kamm3r - 2.1.306-1
- Update to the release pinned in upstream 4c2785f4.

* Tue Oct 20 2026 kamm3r - 2.1.304-1
- Update to the release pinned in upstream 3e3a4343.

* Mon Oct 19 2026 kamm3r - 2.1.303-1
- Update to the release pinned in upstream de0326b9.

* Sat Oct 17 2026 kamm3r - 2.1.302-1
- Update to the release pinned in upstream 64e8fbc2.

* Fri Oct 16 2026 kamm3r - 2.1.301-1
- Update to the release pinned in upstream 99243000.

* Thu Oct 15 2026 kamm3r - 2.1.300-1
- Update to the release pinned in upstream d9ebd3f6.

* Sat Oct 10 2026 kamm3r - 2.1.296-1
- Update to the release pinned in upstream 8787c23f.

* Tue Oct 06 2026 kamm3r - 2.1.289-1
- Update to the release pinned on upstream master.

* Wed Sep 30 2026 kamm3r - 2.1.283-1
- Repackage the upstream Omarchy Claude Code release for Fedora.
