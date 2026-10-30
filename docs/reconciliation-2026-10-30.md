# October 30 upstream update — partial reconciliation

Pinned target: `b766e177b0ab827f2154e4b76cf8c7c158d3b86b` from https://github.com/omacom/omarchy-pkgs.git, fetched into a separate checkout. The complete target has **220 recipes**, with **32 changed recipe directories** since `37c404a57f271a87163b9e628826b908100da965`. All 32 changed directories have individual review records at the target. This does not complete the initial audit of unchanged catalog entries.

## Published

All **21 submitted recipe builds succeeded** in Fedora 44 x86_64 COPR. All **22 binary package/subpackage artifacts**, including `ghost-runtime`, have the exact expected version-release in primary repository metadata and matching HTTP Content-Length. Evidence, checksums, artifact locations and build IDs are in [the publication record](../.copr/publications/2026-10-30.json).

- `claude-code` 2.1.314-1.fc44: [build 11229278](https://copr.fedorainfracloud.org/coprs/build/11229278/).
- `claude-desktop` 4.4212.0-1.fc44: [build 11229279](https://copr.fedorainfracloud.org/coprs/build/11229279/).
- `collie-bin` 1.24.3-1.fc44: [build 11229280](https://copr.fedorainfracloud.org/coprs/build/11229280/).
- `crush-bin` 0.99.0-1.fc44: [build 11229281](https://copr.fedorainfracloud.org/coprs/build/11229281/).
- `ghost` 0.11.0-1.fc44: [build 11229282](https://copr.fedorainfracloud.org/coprs/build/11229282/).
- `google-chrome` 156.0.8078.79-1.fc44: [build 11229283](https://copr.fedorainfracloud.org/coprs/build/11229283/).
- `lmstudio-bin` 0.4.27-1.fc44: [build 11229284](https://copr.fedorainfracloud.org/coprs/build/11229284/).
- `microsoft-edge-stable-bin` 156.0.4314.56-1.fc44: [build 11229285](https://copr.fedorainfracloud.org/coprs/build/11229285/).
- `mise-bin` 2026.10.22-1.fc44: [build 11229286](https://copr.fedorainfracloud.org/coprs/build/11229286/).
- `openai-codex-desktop` 26.1027.30824-1.fc44: [build 11229287](https://copr.fedorainfracloud.org/coprs/build/11229287/).
- `rawmakase-bin` 0.4.8-1.fc44: [build 11229288](https://copr.fedorainfracloud.org/coprs/build/11229288/).
- `t3code-bin` 0.1.5-1.fc44: [build 11229289](https://copr.fedorainfracloud.org/coprs/build/11229289/).
- `t3code-nightly-bin` 0.1.6_nightly.20261029.3892-1.fc44: [build 11229290](https://copr.fedorainfracloud.org/coprs/build/11229290/).
- `zen-browser-bin` 1.24b-1.fc44: [build 11229291](https://copr.fedorainfracloud.org/coprs/build/11229291/).
- `gridcraft-bin` 0.13.0-1.fc44: [build 11229292](https://copr.fedorainfracloud.org/coprs/build/11229292/).
- `wordcraft-bin` 0.12.0-1.fc44: [build 11229293](https://copr.fedorainfracloud.org/coprs/build/11229293/).
- `omakeyboard` 0.1.0-2.fc44: [build 11229303](https://copr.fedorainfracloud.org/coprs/build/11229303/).
- `omarchy-hyprland-titlebars` 0.3.0-1.fc44: [build 11229295](https://copr.fedorainfracloud.org/coprs/build/11229295/).
- `ufw-docker` 20261029-1.fc44: [build 11229296](https://copr.fedorainfracloud.org/coprs/build/11229296/).
- `wayshare` 0.3.0-3.fc44: [build 11229297](https://copr.fedorainfracloud.org/coprs/build/11229297/).
- `omarchy-speedtest` 0.2.1-2.fc44: [build 11229305](https://copr.fedorainfracloud.org/coprs/build/11229305/).

## Porting and validation

- Pinned source checksums and SRPM generation passed through `.copr/Makefile` for all 21 recipes. Chrome's downloaded payload also matched upstream SHA512. LM Studio follows vendor build 2. Ghost's source/runtime manifest identity was updated and validated.
- New native recipes: Gridcraft, Wordcraft, OmaKeyboard, Hyprland titlebars, Speedtest, and the existing local UFW Docker helper now published. Gridcraft/Wordcraft ship CLI, desktop metadata, MIME integration and bundled font/license notices.
- OmaKeyboard: 61 engine tests passed, zero failed/skipped, and the offscreen all-page interface smoke test passed. Its first build failed on an empty debugsource list; Fedora qmake flags and explicit Lua/xkbcli dependencies corrected this.
- Speedtest: upstream requires Go 1.27. A SHA256-verified official Go 1.27.3 toolchain is included for build use only and is not installed. The replacement clean build passes upstream tests. The first build's app tests passed, but recursive discovery also scanned compiler test fixtures; placing the compiler in a hidden directory fixed that packaging error without disabling application tests.
- Wayshare retains version 0.3.0 with Fedora release 3, zlib dependency, RDP description and third-party license notices. Existing setups can rerun `wayshare setup` to update access for TCP 3389; RPM installation does not silently alter firewall rules.
- Titlebars compiled against Fedora Hyprland 0.57.0-1.fc44 and requires that exact runtime build. The plugin is not loaded automatically. A live Hyprland plugin-load test was not performed.
- Cirrus pending assessment resolved: Fedora `cirrus-audio-firmware-20261019-1.fc44` already owns all nine required Dell aliases and the CS35L56 Rev4.5.9 firmware; symlink targets were checked. No duplicate firmware recipe is needed.
- Historical `hyprland-guiutils`, `hyprtoolkit`, and `linux-firmware-cirrus` overrides were removed upstream in 7d70768c; no local recipe or Omadora COPR definition exists. Their catalog entries now say retired. The retirement inventory was rechecked against upstream, local directories and live COPR definitions.
- Bun and OpenVINO remain reviewed Fedora-specific exceptions needed by Ghost and OpenVINO GenAI. Limine Snapper's external recipe is recorded at kamm3r/limine-pkg.
- ARM changes remain explicitly excluded from this x86_64 target: Zenbook A16 audio, Surface Laptop 8 support, Apple ANE split, Aurora kernel/Mesa rebuilds, and Qualcomm ARM kernel patches. Bitwarden's updated upstream recipe remains ARM-only; Rumb still requires an Arch backend.
- Focused tests passed: `test/reconcile-test.py`, both channels in `test/t3code-appimage-layout-test.py`, and `test/core-packaging-test.sh` including the exact pinned core SRPM. No new core source pin was introduced; the existing Omadora pin is retained.
- `git diff --check` passed. No installed-system package transaction, firewall activation or live compositor change was performed by this update.

## Reconciliation and blockers

Both required final checks ran against the full pinned target and exited **1**. There are **168 initial review/accounting issues** and **10 pending entries**. All remaining accounting issues are missing individual reviews; no structural inconsistencies remain. The initial audit is unfinished work, not an external blocker. Older README snapshot claims were not used to fabricate review records. The fully audited README snapshot is unchanged.

- **dingtalk-bin**: Redistribution hold: vendor service agreement section 14 requires written authorization for copying and republication; no COPR payload published.
- **feishu-bin**: Vendor terms restrict redistribution without written permission; not eligible for COPR publication on current evidence.
- **geekbench6**: Upstream 6.7.1 proprietary binary archive contains no license notice granting redistribution; COPR publication needs vendor redistribution permission.
- **hyprland**: Fedora Hyprland COPR supplies 0.57.0-1, but provider spec lacks upstream NVIDIA teardown, wl_output grace and monitor VRR patches; coordinated Fedora stack patching and compositor runtime tests required.
- **linuxqq**: Redistribution hold: QQ license sections 2.4.1-2.4.3 grant personal use and one backup; other rights require written permission.
- **nvidia-sync**: New upstream recipe 0.117.3_12; NVIDIA redistribution terms need review before COPR publication.
- **omarchy-amiga-screensaver**: Upstream 2026.10.27 bundles custom-licensed Amiga demos; clear redistribution grant required before COPR publication.
- **superwhisper-bin**: Proprietary signed vendor bundle; COPR distribution eligibility unresolved; upstream 1.1.2 reviewed.
- **wechat-bin**: Redistribution hold: WeChat Software terms prohibit distribution and redistribution without prior written consent.
- **wps-office-cn**: Redistribution hold: upstream addition 03305349 is explicitly labelled draft because the licence forbids redistribution.

The Hyprland gap is material: the checked LionHeartP/hyprlandRPM provider (commit `1a2422834d0db4889a33621556eb094b01aba32b`) has 0.57.0 but lacks Omarchy's NVIDIA teardown, wl_output grace and monitor VRR patches. The catalog now marks this pending, requiring coordinated stack patching and compositor runtime testing. Matching versions alone are not proof of equivalent behavior.

Vendor entries remain pending for the documented redistribution assessment/permission gaps. The unchanged vendor recipes and stored notices were reassessed; no new vendor permission has been established. Geekbench's checksum-verified 6.7.1 archive contains binaries/data with no redistribution grant, so no COPR payload was submitted. NVIDIA's conditional distribution terms still need classification and obligations resolved for this use. Pending does not mean publication succeeded or that a new definitive legal prohibition was established.

## Publication procedure

The 130 previously enabled SCM webhooks were paused throughout maintenance pushes. The final action restores those and the six new recipe entries after successful final GitHub webhook delivery, while preserving previously disabled definitions. Only the 21 selected recipes were manually built. Recipe changes, catalog dispositions, individual reviews and publication evidence are committed together across the maintenance commits. Existing installed retired packages are not uninstalled automatically.
