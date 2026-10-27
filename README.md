# Omadora packages

Fedora RPM build entry point for [Omadora](https://github.com/kamm3r/omadora), modeled after the separate upstream [Omarchy package repository](https://github.com/omacom/omarchy-pkgs). The [kammer/omadora COPR](https://copr.fedorainfracloud.org/coprs/kammer/omadora/) publishes the packages.

The `omarchy-settings` and `omarchy` RPM specs live here under `packaging/rpm/` (see [`packaging/README.md`](packaging/README.md)), and `.copr/core.mk` builds them from the Omadora commit pinned in `omadora-revision`, so both COPR builds use exactly the same source and version. Fedora recipes for upstream Omarchy packages live under `packages/`.

The upstream `omarchy-pkgs` snapshot at commit `e3dfdd376ce0aac7064497c7bd121f620fa26799` contains 181 PKGBUILDs. [`catalog.tsv`](catalog.tsv) tracks each recipe. `published` means a successful build exists in COPR; `ready` means a source RPM builds and the clean COPR build is next; `pending` needs a Fedora port; `not-applicable` records recipes tied to Arch facilities Omadora replaced; `retired` records recipes removed upstream and no longer maintained here. The goal is a COPR RPM for each feasible recipe, including packages also available elsewhere, after their build and runtime dependencies are checked on Fedora.

The Elephant package family and `omarchy-walker` were [retired upstream](https://github.com/omacom/omarchy-pkgs/commit/2cce621d95555c0cd7fbb7dfdf30479c2d6d71bf) because Omarchy 4 no longer uses them. Their Fedora recipes and COPR entries have been removed. `walker` remains available.

The upstream [seven-package retirement](https://github.com/omacom/omarchy-pkgs/commit/8125c215) also retires `hyprshade`, `localsend-bin`, `makima-bin`, `nautilus-open-any-terminal` (including its Caja subpackage), `openai-codex-bin`, and `wayfreeze` here. `localsend` remains available, and Omadora can also obtain `localsend-bin` from Terra. `bun-bin` remains maintained here because Ghost requires a system Bun executable at runtime and during builds; Fedora 44 has no matching provider, and Terra's `bun-bin` currently lacks the `bun` RPM capability that Ghost requires. Upstream’s user-managed mise installation does not satisfy that RPM dependency.

The latest version updates and added recipes follow upstream commit `a18022b72ccdff9e9e08120eda08513e2eaf14b8`. The catalogue also records additions after the original snapshot, including the matching OpenVINO runtime required by OpenVINO GenAI.

The latest snapshot contains 211 upstream recipes. The catalog records ARM-only additions outside the current x86_64 target and keeps DingTalk, Feishu, QQ, WeChat, and WPS Office CN pending because their vendor terms do not grant the redistribution needed for COPR.

The October 27 updates cover Basecamp CLI, Claude Code, GitHub Copilot CLI, Grok Bot, Microsoft Edge, and T3 Code nightly. All six packages passed Fedora 44 x86_64 COPR builds.

The October 26 publication includes 39 package updates, including new Fedora recipes for Omaroll and Wayshare. All builds passed for Fedora 44 x86_64. `omarchy-speedtest` remains pending until Go 1.27 is available for Fedora builds, and the ARM-only `spark-hwmon-dkms` is outside the current target.

The upstream override retirement in `7d70768c` also removes `asusctl` and `xdg-terminal-exec` here; Terra and Fedora/Nobara provide them. Bun remains a Fedora-specific dependency for Ghost, and the matching OpenVINO runtime remains required by OpenVINO GenAI. Retired packages are not removed automatically from existing installations.

Helium browser is packaged for x86_64. Aurora Apple Silicon additions are recorded as outside this target. Upstream retired `linux-ptl`, which was never published here. OpenClaw keeps its working system CLI until Omadora supplies the user-managed installer integration required by upstream’s seed-only package.

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

OpenClaw uses the packaged system CLI and a private upstream Node 24.22 LTS runtime. Its SQLite is new enough for OpenClaw’s WAL-reset safety check; Fedora 44’s system SQLite 3.51.2 remains unchanged. Its install-time lifecycle runs with a scratch home and must finish before the RPM is packed. The current upstream release cannot seed the user installer, so this package follows upstream master and ships the system CLI.

COPR networking must be enabled for recipes that fetch npm, Flutter, Gradle, Bazel, or Git dependencies during the binary build. The project uses `copr-cli modify kammer/omadora --enable-net on`; the vendored Rust and Go recipes still build without network access.

The Fedora 44 build chroot uses the Hyprland COPR, Terra, and RPM Fusion's free release and updates repositories. OWE's media tests use the full RPM Fusion `ffmpeg` package with its H.264 encoder at build time. Cliamp, Hype, Monologue, Omacut, and OWE require `/usr/bin/ffmpeg` at runtime so Fedora/Nobara's `ffmpeg-free` and the full `ffmpeg` package can both satisfy the dependency. The runtime build still needs the codecs used by the selected media and export settings; Nobara's `libavcodec-freeworld` supplies additional codecs without replacing its FFmpeg library stack.

OmaCharts ships its charting app, CLI, completions, and optional agent skill. Rawmakase installs the upstream RAW photo editor with its private processing libraries. Ghost provides separate `ghost-runtime` and `ghost` RPMs; the latter adds the desktop HUD, which users enable as an Omadora shell plugin. Buzz includes its desktop workspace and CLI helpers. Its two Rust lockfiles contain identical crate versions from different sources, so it fetches both locked dependency graphs during the network-enabled binary build before compiling with `--frozen`.

Signed provides PDF signing and text placement. OmaDesign ships the native design studio with its private libraries and offline documentation. Collie provides phone access to terminal agents through Tailscale; users start its service and configure phone access with the Collie CLI. OmaIRC provides a Qt Quick IRC client and local CLI. `omarchy-themes-intros` adds optional theme intro videos. `thinkpad-t14-amd-touchpad-dkms` enables RMI4/SMBus touchpads on affected AMD ThinkPad T14/P14s laptops; its build checks all three modules against Fedora kernel headers.

After an Omadora source change is ready, update `omadora-revision` to the published commit and push this repository. The GitHub webhook queues all SCM packages for rebuild. The COPR package definitions use `--max-builds 1` to retain only the latest build of each recipe. For a manual core retry, build `omarchy-settings` before `omarchy`.

## Install

```bash
sudo dnf copr enable kammer/omadora
sudo dnf install omarchy
```

The RPMs are built for Fedora 44 x86_64. Omadora's setup also uses Terra, RPM Fusion, and a Hyprland COPR as documented in [FEDORA.md](https://github.com/kamm3r/omadora/blob/main/FEDORA.md).

COPR retention exceptions for concurrent same-version rebuilds are recorded in [`.copr/retention-overrides.json`](.copr/retention-overrides.json). Keep both build records for these packages to preserve shared Pulp artifacts; return to one-build retention after publishing a different version-release.

Pause COPR automatic rebuilds before the first maintenance push, keep them paused through validation and publication-record commits, and restore them after the final push webhook is delivered. Concurrent pushes can otherwise queue unchanged recipes.

## Limine packaging

The Limine boot stack is maintained separately in [kamm3r/limine-pkg](https://github.com/kamm3r/limine-pkg) and published through [kammer/limine](https://copr.fedorainfracloud.org/coprs/kammer/limine/). This includes `limine`, `limine-entry-tool`, `limine-snapper-sync`, and the Fedora-specific `limine-dracut` integration. The Snapper recipe moved out of this repository; the existing Omadora COPR build remains available during transition, with automatic rebuilding disabled and its source redirected to the new repository.

Omadora branding, boot defaults, and hardware policy remain in Omadora. Existing `/usr/local` tools and `/etc/kernel/install.d` overrides need explicit migration before switching to the packaged helper stack; see the new repository's migration notes. The running bootloader is not changed by this source separation.
