# Omadora packages

Fedora RPM build entry point for [Omadora](https://github.com/kamm3r/omadora), modeled after the separate upstream [Omarchy package repository](https://github.com/omacom/omarchy-pkgs). The [kammer/omadora COPR](https://copr.fedorainfracloud.org/coprs/kammer/omadora/) publishes the packages.

The first two packages are `omarchy-settings` and `omarchy`. Their RPM specs and source packaging rules live in the Omadora source tree under `packaging/rpm/` and `.copr/Makefile`. This repository pins one Omadora commit in `omadora-revision` so both COPR builds use exactly the same source and version. Future Fedora package recipes can be added here without changing that core package layout.

## Build from this repository

COPR SCM packages use the `make_srpm` method and this repository's `.copr/Makefile`. Configure the two package entries with these spec paths:

| COPR package | Spec path |
| --- | --- |
| `omarchy-settings` | `packaging/rpm/omarchy-settings/omarchy-settings.spec` |
| `omarchy` | `packaging/rpm/omarchy/omarchy.spec` |

The entry point clones Omadora, checks out the revision in `omadora-revision`, and calls Omadora's COPR source RPM builder. To try a build against the checked-out source locally, set `OMADORA_SOURCE` to its absolute path:

```bash
OMADORA_SOURCE=/path/to/omadora make -f .copr/Makefile srpm outdir=/tmp/omadora-srpm spec=packaging/rpm/omarchy-settings/omarchy-settings.spec
```

After an Omadora source change is ready, update `omadora-revision` to the published commit and rebuild `omarchy-settings` before `omarchy`.

## Install

```bash
sudo dnf copr enable kammer/omadora
sudo dnf install omarchy
```

The RPMs are built for Fedora 44 x86_64. Omadora's setup also uses Terra, RPM Fusion, and a Hyprland COPR as documented in [FEDORA.md](https://github.com/kamm3r/omadora/blob/main/FEDORA.md).
