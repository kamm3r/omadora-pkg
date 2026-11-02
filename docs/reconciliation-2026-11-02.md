# November 2 upstream reconciliation and edge candidates

Target: upstream `99aa5aa6585ed6f17dde56218d83a0a56256b112` (228 recipes, 39 changed directories since `acb60f95`), Omadora `9dca25244170b468ed579829e7df1376bf8faef2`.

This update is **partial**. The ordinary reconciliation check passes for the first time since the review tool was introduced: every recipe has an individual review. `--complete` still exits 1 because 13 packages are pending and 30 are `ready` in edge only.

## Published to edge

CI run [41453374602](https://github.com/kamm3r/omadora-pkg/actions/runs/41453374602) tested and submitted 18 recipes. CI run [41461386604](https://github.com/kamm3r/omadora-pkg/actions/runs/41461386604) tested the core pin; `omarchy-settings` and then `omarchy` were built manually at that commit, as the core procedure requires. All 20 builds succeeded, and every RPM's bytes match its checksum and size in edge repository metadata. The [publication record](../.copr/publications/2026-11-02-edge.json) has build IDs, source RPMs and digests.

- Version updates: `basecamp-cli` 0.22.1, `collie-bin` 1.25.5, `gridcraft-bin` 0.14.2, `grok-bot` 0.78.3, `mise-bin` 2026.10.25, `omacharts` 0.2.5, `openai-codex-desktop` 26.1027.51404, `rawmakase-bin` 0.4.10, `rustdesk` 1.5.1, `slap-notes-bin` 0.2.6, `t3code-bin` 0.1.6, `t3code-nightly-bin` 0.1.7 nightly, `wordcraft-bin` 0.13.2.
- Patch update: `omarchy-power-profiles-daemon` 0.30-2 carries the GB10 patch; 177 tests passed in its build. The patch only affects aarch64 GB10 desktops.
- New ports: `hex-bin` 3.0.0, `omarchy-local-ai` 0.3.2, `herdr-core` 0.1.16, `herdr-app` 0.1.11.
- Core: `omarchy` and `omarchy-settings` 4.0.0~alpha-0.78.git9dca252441. `omarchy` now requires `omarchy-speedtest`, which Omadora's base package list added. That list also moves the firewall to `ufw` and `ufw-docker` and adds `xsetroot`, all available to Fedora installs.

Nothing was built or installed locally, and none of these packages has been run on a desktop. RC and stable were not changed.

## Reviewed without a build

- `omairc`: upstream only moves an Arch Qt pin.
- `voxtype-bin`: upstream fixes a `/tmp` state file that the Fedora `%post` never used.
- `linux-omarchy` and its variants, Aurora components, `omarchy-mac`, `steam`, `umu-launcher`: Arch-only or aarch64-only.
- `omarchy-dev`, `omarchy-settings-dev`, `quickshell`, `quickshell-git`, `rumb`: existing dispositions kept.

## Scope of the backlog audit

The 153 outstanding initial-adoption reviews are recorded, and each reason states what was compared.

For published recipes, the audit compared upstream and Fedora versions, compared source checksums with the upstream recipe, and read every upstream change made after the packaged release. Where upstream's checksums were not comparable (another hash type or a git source), the review says so. Those reviews are a version and source audit, **not a line-by-line comparison of recipe logic**, and they do not prove runtime equivalence.

Every upstream release ahead of a Fedora spec was traced to its commits. Each was either CI or tracking metadata, already ported in Fedora form, or aarch64-only. No missing x86_64 change was found.

For `not-applicable` recipes, the disposition was kept after re-reading the upstream version and architecture. External providers were not all re-queried; the Terra query timed out, so the `ghostty`, `xpadneo-dkms` and `tuxedo-drivers-nocompatcheck-dkms` reviews say the provider was not re-checked.

## Blockers

**Porting and hardware**

- `sunshine`: upstream's x86_64 CUDA-on build is not ported. It needs Fedora CUDA toolchain integration and encoder testing. The CUDA-off package stays published.
- `hyprland`: the Fedora provider lacks upstream's NVIDIA teardown, `wl_output` grace and monitor VRR patches. It needs stack patching and physical NVIDIA, VRR, suspend and dock testing.
- `cua-hyprland-plugin`: the spec requires `hyprland = 0.56.2`, and the provider now also offers 0.57.0. It needs that older compositor build until the stack moves.

**Redistribution (11)**

`dingtalk-bin`, `feishu-bin`, `geekbench`, `geekbench6`, `linuxqq`, `notion-desktop`, `nvidia-sync`, `omarchy-amiga-screensaver`, `superwhisper-bin`, `wechat-bin`, `wps-office-cn`. Each needs a vendor grant. `geekbench` and `notion-desktop` are new in this update.

**Promotion**

The 30 `ready` packages stay in edge until RC and stable test evidence exists.

## Final checks

- `reconcile.py check`: exit 0, 0 review issues, 43 unresolved packages.
- `reconcile.py check --complete`: exit 1, 13 pending and 30 ready.

The Limine repository needed no update: Limine 12.9.6, `limine-entry-tool` 1.40.0 and `limine-snapper-sync` 1.32.1 are the latest upstream tags. The gaming repository was also current.
