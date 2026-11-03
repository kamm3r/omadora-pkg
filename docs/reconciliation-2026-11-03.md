# November 3 upstream reconciliation and edge candidates

Target: upstream `30fed321658234101126fc7d553e94d27f94462e` (228 recipes), Omadora `7c6d343ce553d24d3bafacc6d905f8d17afc73d3`.

This update is **partial**. The ordinary reconciliation check passes; `--complete` still exits 1 because 13 packages are pending and 34 are `ready` in edge only.

## Published to edge

CI runs [41589131886](https://github.com/kamm3r/omadora-pkg/actions/runs/41589131886) and [41593100460](https://github.com/kamm3r/omadora-pkg/actions/runs/41593100460) tested and submitted the recipes. CI run [41589463851](https://github.com/kamm3r/omadora-pkg/actions/runs/41589463851) tested the core pin; `omarchy-settings` and then `omarchy` were built manually at that commit. All 15 current builds succeeded, and every RPM's bytes match its checksum and size in edge repository metadata. The [publication record](../.copr/publications/2026-11-03-edge.json) lists the build IDs and checksums.

- Version updates: `claude-code` 2.1.317, `gridcraft-bin` 0.15.0, `grok-bot` 0.78.4, `herdr-app` 0.1.12, `herdr-core` 0.1.17, `obsidian` 1.15.0, `omacharts` 0.2.9, `omarchy-local-ai` 0.4.0, `perplexity` 26.10.3+build141572, `splinterm` 0.2.0, `t3code-nightly-bin` 0.1.7 nightly 4106, `visual-studio-code-bin` 1.144.1, `wordcraft-bin` 0.14.0.
- Core: `omarchy` and `omarchy-settings` 4.0.0~alpha-0.79.git7c6d343ce5. `omarchy-settings` now packages every systemd user drop-in, including the new WirePlumber camera-access drop-in; the built RPM's file list confirms it.

`t3code-nightly-bin` was built twice because upstream published a newer nightly during the update. Build 11248144 is superseded by 11248229.

Nothing was built or installed locally, and none of these packages has been run on a desktop. RC and stable were not changed. The `herdr` ghostty pins did not change at the new tags.

## Reviewed without a build

- `nvidia-utils`, `nvidia-open-dkms`, `lib32-nvidia-utils`: upstream now carries these on x86_64 so they stay pinned to its prebuilt-module `linux-omarchy` kernels. Fedora uses the stock kernel and RPM Fusion akmods, so that constraint does not apply here.
- `linux-n1x`: removed upstream and never published here; retired.
- `aquamarine`: the Hyprland provider ships 0.16.0, the same upstream version, and upstream's two dropped patches are included in that release.
- `hyprland`: upstream's `-3` and `-4` are dependency rebuilds. The existing patch blocker stands.
- `quickshell`, `quickshell-git`: upstream dependency rebuilds; the Hyprland provider supplies `quickshell`.
- `bitwarden`, `linux-omarchy`, `linux-omarchy-aarch64`, `qcom-firmware-extract`: ARM-only or Arch kernel changes. `omarchy-dev` and `omarchy-settings-dev`: covered by the core specs.

## Blockers

- `omarchy-hyprland-titlebars`: the stable package requires Hyprland exactly 0.57.0-1, but the provider's newest build is 0.57.0-2, so a system on the newest build cannot install it. This was not rebuilt: edge does not carry the Hyprland group, and a lone plugin build there would make the RC plan fail its group check. The fix belongs with the Hyprland qualification.
- `hyprland`: the provider lacks upstream's NVIDIA teardown, `wl_output` grace and monitor VRR patches. It needs stack patching and physical NVIDIA, VRR, suspend and dock testing.
- `sunshine`: upstream's x86_64 CUDA-on build is not ported. It needs Fedora CUDA toolchain integration and encoder testing.
- `cua-hyprland-plugin`: the spec requires `hyprland = 0.56.2`, so it needs that older compositor build until the stack moves.
- Redistribution (11): `dingtalk-bin`, `feishu-bin`, `geekbench`, `geekbench6`, `linuxqq`, `notion-desktop`, `nvidia-sync`, `omarchy-amiga-screensaver`, `superwhisper-bin`, `wechat-bin`, `wps-office-cn`. Each needs a vendor grant.
- Promotion: `ready` packages stay in edge until RC and stable test evidence exists.

The Limine and gaming repositories needed no update on the same day.
