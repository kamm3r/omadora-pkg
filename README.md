# Omadora packages

Fedora RPM build entry point for [Omadora](https://github.com/kamm3r/omadora), modeled after the separate upstream [Omarchy package repository](https://github.com/omacom/omarchy-pkgs). The [kammer/omadora COPR](https://copr.fedorainfracloud.org/coprs/kammer/omadora/) publishes the packages.

The `omarchy-settings` and `omarchy` RPM specs live here under `packaging/rpm/` (see [`packaging/README.md`](packaging/README.md)), and `.copr/core.mk` builds them from the Omadora commit pinned in `omadora-revision`, so both COPR builds use exactly the same source and version. Fedora recipes for upstream Omarchy packages live under `packages/`.

The upstream `omarchy-pkgs` snapshot at commit `e3dfdd376ce0aac7064497c7bd121f620fa26799` contains 181 PKGBUILDs. [`catalog.tsv`](catalog.tsv) tracks each recipe. `published` means a successful build exists in COPR; `ready` means a source RPM builds and the clean COPR build is next; `pending` needs a Fedora port; `not-applicable` records recipes tied to Arch facilities Omadora replaced. The goal is a COPR RPM for each feasible recipe, including packages also available elsewhere, after their build and runtime dependencies are checked on Fedora.

## Build from this repository

COPR SCM packages use the `make_srpm` method and this repository's `.copr/Makefile`. The core package entries use these spec paths:

| COPR package | Spec path |
| --- | --- |
| `omarchy-settings` | `packaging/rpm/omarchy-settings/omarchy-settings.spec` |
| `omarchy` | `packaging/rpm/omarchy/omarchy.spec` |

The entry point clones Omadora, archives the revision in `omadora-revision`, and packs it with the spec from `packaging/rpm/`. To build from a local Omadora checkout that contains that commit instead of cloning, set `OMADORA_SOURCE` to its path:

```bash
OMADORA_SOURCE=/path/to/omadora make -f .copr/Makefile srpm outdir=/tmp/omadora-srpm spec=packaging/rpm/omarchy-settings/omarchy-settings.spec
```

Additional package entries use `packages/<name>/<name>.spec`. Their `sources.sha256` file verifies upstream downloads before the source RPM is created. Rust recipes with a `cargo-vendor` marker also include dependency sources checked against their `Cargo.lock` hashes in a separate `cargo-vendor/` directory (upstream `vendor/` path dependencies stay intact), so the binary build does not need network access. A nonempty marker can name a different archive root using `%version`, such as `qmk_hid-%version`. Go recipes with a `go-vendor` marker bundle their modules from the locked `go.mod` and `go.sum` into the source RPM for a networkless binary build. To test one locally:

```bash
make -f .copr/Makefile srpm outdir=/tmp/omadora-srpm spec=packages/tobi-try/tobi-try.spec
rpmbuild --rebuild /tmp/omadora-srpm/tobi-try-*.src.rpm
```

`slack-desktop` packages Slack's x86_64 Linux client. `t3code-nightly-bin` installs alongside `t3code-bin` and provides `t3code-nightly` and `t3-nightly`, with desktop flags in `~/.config/t3code-nightly-flags.conf`. The two T3 Code channels retain upstream's shared application state and URL scheme.

OpenClaw uses the packaged system CLI and the Fedora Node 24 runtime. Its install-time lifecycle runs with a scratch home and must finish before the RPM is packed. The current upstream release cannot seed the user installer, so this package follows upstream master and ships the system CLI.

COPR networking must be enabled for recipes that fetch npm, Flutter, Gradle, Bazel, or Git dependencies during the binary build. The project uses `copr-cli modify kammer/omadora --enable-net on`; the vendored Rust and Go recipes still build without network access.

After an Omadora source change is ready, update `omadora-revision` to the published commit and push this repository. The GitHub webhook queues all SCM packages for rebuild. For a manual core retry, build `omarchy-settings` before `omarchy`.

## Install

```bash
sudo dnf copr enable kammer/omadora
sudo dnf install omarchy
```

The RPMs are built for Fedora 44 x86_64. Omadora's setup also uses Terra, RPM Fusion, and a Hyprland COPR as documented in [FEDORA.md](https://github.com/kamm3r/omadora/blob/main/FEDORA.md).
