# Omadora packages

Fedora RPM build entry point for [Omadora](https://github.com/kamm3r/omadora), modeled after the separate upstream [Omarchy package repository](https://github.com/omacom/omarchy-pkgs). The [kammer/omadora COPR](https://copr.fedorainfracloud.org/coprs/kammer/omadora/) publishes the packages.

The `omarchy-settings` and `omarchy` RPM specs and source packaging rules live in the Omadora source tree under `packaging/rpm/` and `.copr/Makefile`. This repository pins one Omadora commit in `omadora-revision` so both COPR builds use exactly the same source and version. Fedora recipes for upstream Omarchy packages live under `packages/`.

The upstream `omarchy-pkgs` snapshot at commit `29465fb750ed2b7a8b3f409cf1a61989ac2d3867` contains 175 PKGBUILDs. [`catalog.tsv`](catalog.tsv) tracks each recipe. `published` means a successful build exists in COPR; `ready` means a source RPM builds and the clean COPR build is next; `pending` needs a Fedora port; `not-applicable` records recipes tied to Arch facilities Omadora replaced. The goal is a COPR RPM for each feasible recipe, including packages also available elsewhere, after their build and runtime dependencies are checked on Fedora.

## Build from this repository

COPR SCM packages use the `make_srpm` method and this repository's `.copr/Makefile`. The core package entries use these spec paths:

| COPR package | Spec path |
| --- | --- |
| `omarchy-settings` | `packaging/rpm/omarchy-settings/omarchy-settings.spec` |
| `omarchy` | `packaging/rpm/omarchy/omarchy.spec` |

The entry point clones Omadora, checks out the revision in `omadora-revision`, and calls Omadora's COPR source RPM builder. To try a core build against the checked-out source locally, set `OMADORA_SOURCE` to its absolute path:

```bash
OMADORA_SOURCE=/path/to/omadora make -f .copr/Makefile srpm outdir=/tmp/omadora-srpm spec=packaging/rpm/omarchy-settings/omarchy-settings.spec
```

Additional package entries use `packages/<name>/<name>.spec`. Their `sources.sha256` file verifies upstream downloads before the source RPM is created. Rust recipes with a `cargo-vendor` marker also include dependency sources checked against their `Cargo.lock` hashes, so the binary build does not need network access. To test one locally:

```bash
make -f .copr/Makefile srpm outdir=/tmp/omadora-srpm spec=packages/tobi-try/tobi-try.spec
rpmbuild --rebuild /tmp/omadora-srpm/tobi-try-*.src.rpm
```

After an Omadora source change is ready, update `omadora-revision` to the published commit and push this repository. The GitHub webhook queues all SCM packages for rebuild. For a manual core retry, build `omarchy-settings` before `omarchy`.

## Install

```bash
sudo dnf copr enable kammer/omadora
sudo dnf install omarchy
```

The RPMs are built for Fedora 44 x86_64. Omadora's setup also uses Terra, RPM Fusion, and a Hyprland COPR as documented in [FEDORA.md](https://github.com/kamm3r/omadora/blob/main/FEDORA.md).
