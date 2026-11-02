Name:           omarchy-local-ai
Version:        0.3.2
Release:        1%{?dist}
Summary:        Run open models locally for Omarchy's coding agents
License:        MIT
URL:            https://github.com/omacom/omarchy-local-ai
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3
Requires:       python3
Requires:       systemd
# Installed by "omarchy agent local use" on Arch; these run the models.
Recommends:     crun
Recommends:     podman

%description
Runs open models locally for Omarchy's coding agents, with curated recipes per
machine. The engine drives models through the systemd user manager with Quadlet
units; Podman and crun run them as rootless containers.

%prep
%autosetup

%build
:

%install
# The engine reads its recipe catalog from the directory it is installed in.
install -d %{buildroot}%{_datadir}/%{name} %{buildroot}%{_bindir}
cp -a catalog.toml best.toml recipes runtimes reviews measurements %{buildroot}%{_datadir}/%{name}/
install -m 0644 agent_local.py %{buildroot}%{_datadir}/%{name}/agent_local.py
install -m 0755 omarchy-local-ai %{buildroot}%{_datadir}/%{name}/omarchy-local-ai
ln -s %{_datadir}/%{name}/omarchy-local-ai %{buildroot}%{_bindir}/%{name}

%check
./omarchy-local-ai validate .

%files
%license LICENSE
%doc README.md docs/engine.md
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Mon Nov 02 2026 kamm3r - 0.3.2-1
- Port the recipe added in upstream 99aa5aa6 to Fedora.
