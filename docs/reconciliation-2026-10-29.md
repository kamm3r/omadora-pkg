# October 29 upstream reconciliation — partial

Target: `37c404a57f271a87163b9e628826b908100da965` (origin/master fetched from https://github.com/omacom/omarchy-pkgs.git in a separate checkout).

The complete `pkgbuilds/` tree is identical to `941cc6bf115242d7564c6c7b602fd0c634030df9`: 214 recipes, no added, removed, or changed recipe files. No source/spec changes or new builds were needed for this target.

## Publication verified

All 33 builds in `.copr/publications/2026-10-29.json` report `succeeded` through the COPR API. Their exact version-release values are present in the Fedora 44 x86_64 primary repository metadata. Eight catalog rows moved from ready to published: Basecamp CLI, Helium, OmaCharts, Omasnap, T3 Code nightly, tmog, Wayshare, and Splinterm. Individual reviews for these eight packages are recorded in `upstream-reviews.json`.

No maintenance push, webhook change, COPR submission, retirement, or installed-system change was performed. Existing user changes were preserved. Changes remain local and uncommitted.

## Validation

- Full Git recipe-tree comparison against the previous snapshot: no changes.
- Live COPR build API and exact repository version-release verification: 33/33 passed.
- `python3 test/reconcile-test.py`: passed.
- `python3 test/t3code-appimage-layout-test.py`: both channels passed.
- Both required final reconciliation checks ran against the pinned target and exited 1: 242 accounting issues and 13 pending packages. Full details are in `reconciliation-2026-10-29.json`.

Source checksum/SRPM validation was not rerun: this pass changes publication accounting and documentation only, with no source recipe changes. Successful existing clean Fedora builds were verified; no new binary build was submitted.

## Remaining work and blockers

The new reconciliation tool has no prior review baseline. The remaining initial adoption reviews are **unfinished work**, not an external blocker; old README snapshot claims were not used to manufacture review records. The fully audited README snapshot is therefore unchanged. Retained upstream removals and the external Limine recipe also require explicit exception records in the initial audit.

Every pending catalog entry remains visible below. Technical entries were inspected in the upstream recipes; no Fedora port, hardware/ABI validation, or fresh vendor permission assessment was completed in this pass. Existing redistribution holds remain in place and are not new legal determinations.

- **dingtalk-bin**: Redistribution hold: vendor service agreement section 14 requires written authorization for copying and republication; no COPR payload published
- **feishu-bin**: Vendor terms restrict redistribution without written permission; not eligible for COPR publication on current evidence
- **linux-firmware-cirrus-dx13260**: Hardware-specific Cirrus firmware aliases; needs Fedora firmware coverage assessment
- **linuxqq**: Redistribution hold: QQ license sections 2.4.1-2.4.3 grant personal use and one backup; other rights require written permission
- **nvidia-sync**: New upstream recipe 0.117.3_12; NVIDIA redistribution terms need review before COPR publication
- **omakeyboard**: Qt keyboard remapper needs a Fedora port and runtime validation
- **omarchy-amiga-screensaver**: Upstream 2026.10.27 bundles custom-licensed Amiga demos; clear redistribution grant required before COPR publication
- **omarchy-hyprland-titlebars**: Needs Fedora Hyprland ABI compatibility validation before publishing
- **omarchy-power-profiles-daemon**: Custom power-profiles daemon needs Fedora hardware patch assessment
- **omarchy-speedtest**: Upstream 0.2.1 requires Go 1.27; Fedora 44 currently supplies Go 1.26
- **superwhisper-bin**: Proprietary signed vendor bundle; COPR distribution eligibility unresolved; upstream 1.1.2 reviewed
- **wechat-bin**: Redistribution hold: WeChat Software terms prohibit distribution and redistribution without prior written consent
- **wps-office-cn**: Redistribution hold: upstream addition 03305349 is explicitly labelled draft because the licence forbids redistribution

ARM-only and other not-applicable dispositions remain unchanged. Their initial individual reconciliation reviews are still required. This is a partial reconciliation, not a completed upstream audit or a claim that the pending backlog is resolved.
