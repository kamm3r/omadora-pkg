# October 31 upstream reconciliation and edge candidates

This update is **partial**. All 30 changed upstream recipe directories are accounted for at `acb60f95615b3528774f9a43937e9bd88e9af558` (221 recipes), and all 16 maintained version updates passed clean remote Fedora 44 x86_64 source and binary builds. The remaining initial-adoption audit and pending ports/redistribution decisions are unresolved. The fully audited README snapshot is unchanged.

## CI and publication

Recipe versions, source selections, archive roots and checksum manifests were updated from the pinned upstream tree and checked against official creator releases, vendor download endpoints and npm metadata. The preview share picker carries the pinned `07602efe7a65dcef5399e22c162edf9fc331c46d` shm-pool fix, updated archive/vendor roots and generated version string. Native GTK/Wayland dependencies were reviewed.

GitHub CI now tests a main commit before submitting its changed recipe inputs to **kammer/omadora-edge** at that exact commit. The direct GitHub-to-COPR push webhook is disabled. CI uses an edge-only capability and records submitted build IDs/input fingerprints as an Actions artifact. Core builds retain their separate coordinated manual edge procedure. CI submission success is distinct from a successful COPR build and verified repository publication.

[Candidate CI run](https://github.com/kamm3r/omadora-pkg/actions/runs/41179485376) passed and submitted 16 builds. [Checksum-fix CI run](https://github.com/kamm3r/omadora-pkg/actions/runs/41180003351) passed and correctly submitted only Claude Code; the other 15 were not rebuilt. The current suite has 21 promotion/submission unit tests, the reconciliation regression test, AppImage layout checks and pinned core RPM packaging tests.

**No package builds ran locally.** Source checksums and source RPMs were validated remotely by `.copr/Makefile` on COPR. All 16 clean binary builds succeeded. Their exact versions, repository sizes, download Content-Length and full streamed SHA256 hashes were verified. The [publication record](../.copr/publications/2026-10-31-edge.json) contains every build ID, source-RPM URL and binary digest.

Claude Code's first source build, 11234475, stopped on the changed vendor legal-document hash. Its executable download hash passed. The current official legal document was reviewed and its checksum refreshed without disabling verification. Replacement 11234496 passed source and binary validation.

All candidates remain `ready` because RC/stable promotion still needs its test evidence. Stable's 350 retained RPMs and RC's 319 RPMs retain their previous metadata versions, checksums and sizes. No promotion or installation occurred.

## Candidate versions

- `basecamp-cli` 0.22.0-1.fc44: [build 11234474](https://copr.fedorainfracloud.org/coprs/build/11234474/).
- `brave-bin` 1.98.63-1.fc44: [build 11234483](https://copr.fedorainfracloud.org/coprs/build/11234483/).
- `brave-origin-bin` 1.98.63-1.fc44: [build 11234478](https://copr.fedorainfracloud.org/coprs/build/11234478/).
- `collie-bin` 1.25.2-1.fc44: [build 11234479](https://copr.fedorainfracloud.org/coprs/build/11234479/).
- `helium-browser-bin` 0.20.3.1-1.fc44: [build 11234484](https://copr.fedorainfracloud.org/coprs/build/11234484/).
- `lmstudio-bin` 0.4.28-1.fc44: [build 11234488](https://copr.fedorainfracloud.org/coprs/build/11234488/).
- `mise-bin` 2026.10.23-1.fc44: [build 11234487](https://copr.fedorainfracloud.org/coprs/build/11234487/).
- `owe` 0.2.13-1.fc44: [build 11234482](https://copr.fedorainfracloud.org/coprs/build/11234482/).
- `owe-lockfeed` 0.2.13-1.fc44: [build 11234480](https://copr.fedorainfracloud.org/coprs/build/11234480/).
- `rawmakase-bin` 0.4.9-1.fc44: [build 11234481](https://copr.fedorainfracloud.org/coprs/build/11234481/).
- `slap-notes-bin` 0.2.5-1.fc44: [build 11234486](https://copr.fedorainfracloud.org/coprs/build/11234486/).
- `t3code-nightly-bin` 0.1.6_nightly.20261031.3956-1.fc44: [build 11234477](https://copr.fedorainfracloud.org/coprs/build/11234477/).
- `hyprland-preview-share-picker` 0.3.0.r3.g07602ef-1.fc44: [build 11234476](https://copr.fedorainfracloud.org/coprs/build/11234476/).
- `microsoft-edge-stable-bin` 156.0.4314.58-1.fc44: [build 11234473](https://copr.fedorainfracloud.org/coprs/build/11234473/).
- `openclaw` 2026.10.9-1.fc44: [build 11234485](https://copr.fedorainfracloud.org/coprs/build/11234485/).
- `claude-code` 2.1.316-1.fc44: [build 11234496](https://copr.fedorainfracloud.org/coprs/build/11234496/).

## Exclusions and blockers

The new ASUS Zenbook A16 firmware is aarch64-only and is recorded outside the Fedora 44 x86_64 target. Changed ARM audio, firmware, Surface/Qualcomm/ANE and Arch-kernel integrations keep their reviewed exclusions; Fedora/Nobara native providers remain in place. Arch development recipes do not replace Omadora's separately pinned core source.

Sunshine's new upstream x86_64 CUDA-on default is **not ported**. Its existing 2026.914.233613-2 package remains published with CUDA disabled. Fedora CUDA-toolchain integration and encoder/runtime qualification are unfinished, so this changed behavior is explicitly pending and was not submitted as equivalent.

The nine proprietary redistribution holds remain: DingTalk, Feishu, Geekbench, QQ, NVIDIA Sync, Amiga demo assets, Superwhisper, WeChat and WPS Office CN. No new redistribution authorization was established. Hyprland retains its physical NVIDIA/VRR/suspend/dock qualification blocker; the separate tested sandbox is not promoted by this update. Every pending disposition was individually reassessed and recorded.

## Final accounting

Ordinary and `--complete` reconciliation checks both exit 1: **153 initial-adoption reviews** remain outstanding, all reported as review-required rather than structural inconsistencies. There are **11 pending blockers** and **16 ready edge candidates** (27 unresolved entries). All current changed recipes have an individual review. The machine-readable record lists every remaining issue and concrete pending reason.

The evidence-only final CI check exposed nonchronological GitHub artifact listing order. The version guard stopped a duplicate Claude submission before a webhook call. Receipt selection now sorts by creation time, with a regression test covering out-of-order artifact IDs; the final CI run validates a zero-build evidence push.
