# November 4 upstream reconciliation and edge candidates

Target: upstream `96cd7d5831cd007e3faa4cd9b788de09c1213034` (231 recipes, 40 changed directories since `30fed321`). Omadora stays at `7c6d343ce553d24d3bafacc6d905f8d17afc73d3`.

This update is **partial**. The ordinary reconciliation check passes. `--complete` still exits 1 because 14 packages are pending and 41 are `ready` in edge only.

## Published to edge

CI runs [41784700977](https://github.com/kamm3r/omadora-pkg/actions/runs/41784700977) and [41788908193](https://github.com/kamm3r/omadora-pkg/actions/runs/41788908193) tested and submitted the recipes. All 18 current builds succeeded, and all 19 RPMs match their checksum and size in edge repository metadata. The [publication record](../.copr/publications/2026-11-04-edge.json) lists the build IDs and checksums.

- Version updates: `1password` 8.12.44, `claude-code` 2.1.318, `claude-desktop` 4.16336.0, `collie-bin` 1.25.6, `cursor-bin` 3.28.7, `ghost` 0.11.2, `google-chrome` 157.0.8103.38, `gridcraft-bin` 0.16.0, `grok-bot` 0.78.5, `hex-bin` 3.3.0, `omacharts` 0.2.11, `openai-codex-desktop` 26.1029.61003, `openclaw` 2026.10.10, `t3code-nightly-bin` 0.1.7 nightly 4151, `wordcraft-bin` 0.15.0.
- `flea` 0.4.0: upstream added a GPUI window with new runtime dependencies. The spec now vendors the Cargo sources, including the pinned GPUI fork, and follows upstream's dependency list in Fedora names. Upstream's `libalpm` removal hook has no RPM equivalent and is dropped.
- New port: `omafeed` 0.2.4; 170 upstream Rust tests passed in its build, with 1 ignored.
- Patch update: `omarchy-power-profiles-daemon` 0.30-3 carries the Apple Silicon no-boost patch; 183 tests passed in its build. The patch only changes behavior on Apple Silicon.

`t3code-nightly-bin` was built twice because upstream published a newer nightly during the update. Build 11253699 is superseded by 11253775.

**`flea` carries the most risk in this update.** Upstream's test suite was not run, because its recipe is written around the Arch builder; the build's `%check` only runs `flea --version`, and `flea-gui` has never been opened. Check it on a desktop before promotion.

Nothing was built or installed locally, and none of these packages has been run on a desktop. RC and stable were not changed.

## Reviewed without a build

- `dell-xps-touchpad-haptics`, `dell-xps13-sidecar-amps`, `link-studio`, `macbook8-spi-pxa2xx-nodma-dkms`, `omapresent`, `omarchy-audio-tuner`, `omarchy-emacs`, `omarchy-fish`, `omarchy-zsh`, `python-sounddevice`, `python-terminaltexteffects`, `v4l2-relayd`: upstream only raises `pkgrel`, to correct Arch's "Unknown Packager" metadata.
- `bitwarden`: upstream fixes file ownership in its aarch64-only recipe.
- `ffmpeg`, `omarchy-ane-dkms`, `omarchy-mac-boot`: aarch64-only.
- `rumb`: the Arch-specific disposition stands.
- `omarchy-dev`, `omarchy-settings-dev`: covered by the core specs. The core pair was not rebuilt because Omadora has no newer commit.

## Blockers

- `omarchy-hyprland-titlebars`: the stable package requires Hyprland exactly 0.57.0-1, and the provider's newest build is 0.57.1-1. A matching build needs the coordinated Hyprland group, which edge does not carry.
- `hyprland`: upstream 0.57.1-2 carries three local patches that the provider's 0.57.1-1 spec has not been shown to include. It needs stack patching and physical NVIDIA, VRR, suspend and dock testing.
- `sunshine`: upstream's x86_64 CUDA-on build is not ported. It needs Fedora CUDA toolchain integration and encoder testing.
- `cua-hyprland-plugin`: the spec requires `hyprland = 0.56.2`, so it needs that older compositor build until the stack moves.
- Redistribution (12): `amp-desktop-bin`, `dingtalk-bin`, `feishu-bin`, `geekbench`, `geekbench6`, `linuxqq`, `notion-desktop`, `nvidia-sync`, `omarchy-amiga-screensaver`, `superwhisper-bin`, `wechat-bin`, `wps-office-cn`. Each needs a vendor grant. `amp-desktop-bin` is new: Amp's terms grant only a non-transferable, non-sublicensable user license.
- Omadora sync: Omarchy has moved past `ae64a4be7`, so a newer core build needs an Omadora sync first.
- Promotion: `ready` packages stay in edge until RC and stable test evidence exists.

The Limine and gaming repositories needed no update on the same day.
