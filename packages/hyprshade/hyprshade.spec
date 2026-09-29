Name:           hyprshade
Version:        5.0.0
Release:        2%{?dist}
Summary:        Manage Hyprland shaders and schedules
License:        MIT
URL:            https://github.com/loqusion/hyprshade
Source0:        https://files.pythonhosted.org/packages/source/h/hyprshade/hyprshade-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/loqusion/hyprshade/%{version}/examples/config.toml
BuildArch:      noarch
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-hatchling
BuildRequires:  python3-click
BuildRequires:  python3-more-itertools
BuildRequires:  python3-rpm-macros
Requires:       python3-click
Requires:       python3-more-itertools
Requires:       hyprland
Requires:       util-linux

%description
Hyprshade selects Hyprland display shaders and can activate them on a schedule.

%prep
%autosetup
install -D -m 0644 %{SOURCE1} examples/config.toml

%build
python3 -m build --wheel --no-isolation

%install
python3 -m installer --destdir=%{buildroot} dist/*.whl
mkdir -p assets/completions
PYTHONPATH=%{buildroot}%{python3_sitelib} _HYPRSHADE_COMPLETE=bash_source %{buildroot}%{_bindir}/hyprshade >assets/completions/hyprshade.bash
PYTHONPATH=%{buildroot}%{python3_sitelib} _HYPRSHADE_COMPLETE=fish_source %{buildroot}%{_bindir}/hyprshade >assets/completions/hyprshade.fish
PYTHONPATH=%{buildroot}%{python3_sitelib} _HYPRSHADE_COMPLETE=zsh_source %{buildroot}%{_bindir}/hyprshade >assets/completions/_hyprshade
install -D -m 0644 examples/config.toml %{buildroot}%{_datadir}/hyprshade/examples/config.toml
install -D -m 0644 assets/completions/hyprshade.bash %{buildroot}%{_datadir}/bash-completion/completions/hyprshade
install -D -m 0644 assets/completions/hyprshade.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/hyprshade.fish
install -D -m 0644 assets/completions/_hyprshade %{buildroot}%{_datadir}/zsh/site-functions/_hyprshade

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprshade
%{python3_sitelib}/hyprshade
%{python3_sitelib}/hyprshade-%{version}.dist-info
%{_datadir}/hyprshade
%{_datadir}/bash-completion/completions/hyprshade
%{_datadir}/fish/vendor_completions.d/hyprshade.fish
%{_datadir}/zsh/site-functions/_hyprshade

%changelog
* Mon Sep 28 2026 kamm3r - 5.0.0-2
- Generate completions through the installed hyprshade entry point.

* Mon Sep 28 2026 kamm3r - 5.0.0-1
- Port the upstream Omarchy Hyprland shader helper to Fedora.
