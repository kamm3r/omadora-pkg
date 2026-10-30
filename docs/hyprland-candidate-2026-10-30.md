# Hyprland candidate validation — October 30, 2026

This is a staged Fedora 44 x86_64 port, not a production promotion or a completed full upstream audit. Sources are on `hyprland-testing`; packages are published only in [kammer/omadora-hyprland-testing](https://copr.fedorainfracloud.org/coprs/kammer/omadora-hyprland-testing/). The installed desktop and production Hyprland provider remain unchanged. No testing repository was enabled on the host.

## Source and packaging

- Upstream Omarchy recipe target: `b766e177b0ab827f2154e4b76cf8c7c158d3b86b` (220 recipes).
- Compositor: official Hyprland 0.57.0 release archive, with unchanged NVIDIA EGL teardown, retired `wl_output` grace and monitor-rule VRR patches from that Omarchy commit.
- Fedora integration/macros: LionHeartP/hyprlandRPM `1a2422834d0db4889a33621556eb094b01aba32b`.
- Additional Fedora regression/ABI patch: immutable packaging commit `af93df57b2b1ba69f7ccee4fe354f82ddcd028e3`; all sources and patches have SHA256 manifests. Every patch applies with `--fuzz=0`.
- Candidate versions: `hyprland-0.57.0-4.omadora.fc44` and `omarchy-hyprland-titlebars-0.3.0-4.omadora.fc44`. Titlebars build and runtime requirements pin that exact compositor/SDK release. Companion libraries continue to use the existing Fedora Hyprland provider.
- Client and server API hashes include `_omadora_912521ee8a53_` so unpatched plugins cannot silently load against the patched compositor. Other plugins require rebuilding; none were active on the test host.

## Validation

Both source RPMs were generated through `.copr/Makefile` with successful source checksum validation. The clean Fedora compositor build [11229543](https://copr.fedorainfracloud.org/coprs/build/11229543/) succeeded. Its `%check` ran **836 tests from 98 suites**, all passing, against the same uninstrumented release library shipped by the package. Five added tests cover two VRR rule comparisons, two removed-output lifetime cases, and client/server ABI agreement. Existing resource-drain tests remain active.

The runtime probe runs a separate nested Wayland compositor with private HOME, config, state, runtime directory, D-Bus session and IPC socket. Seat acquisition and systemd environment/session integration are disabled. It never addresses the running desktop's IPC. The Wayland client holds an unbound output ID while an output is removed and recreated with the same name, then sends the stale bind.

- Installed unpatched Fedora `0.57.0-1`: reproduced `global wl_output … is unavailable`, client EPROTO 71.
- Extracted candidate RPM: stale bind and release pass; the production titlebars plugin is rejected for version mismatch; compositor exits with status 0.
- Matching titlebars: clean Fedora build [11229633](https://copr.fedorainfracloud.org/coprs/build/11229633/) succeeded. The extracted plugin loads and unloads successfully in the candidate compositor. The combined runtime probe passes all four checks (late bind, old-plugin rejection, matching-plugin load/unload, clean exit).

Candidate downloads are verified against primary repository metadata for exact version, full byte length and SHA256. See `.copr/publications/hyprland-candidate-2026-10-30.json` for artifacts and final results.

## Production protection

An initial staging-branch push exposed 106 production SCM definitions with an empty branch field, which reacts to staging pushes as well. All 106 incidental builds were canceled before success; none published. All 136 previously enabled production webhooks were then paused. The 106 empty branch fields were corrected to `committish=main`; other source fields and retention settings were preserved. All 22 artifacts from the earlier October 30 production publication were independently rechecked: expected versions, metadata checksums/sizes and download Content-Length remain unchanged.

Production webhooks are restored only after the final evidence push is delivered. The machine-readable record includes the paused-state verification and the restoration policy; restoration is verified separately after that final push. Testing-project webhooks remain disabled.

## Remaining work

The host has AMD GPUs. Real NVIDIA teardown, physical-monitor VRR changes, suspend/resume and real dock hotplug have not been qualified. These are explicit blockers to full runtime qualification and production promotion. Automated and nested tests do not establish hardware behavior. Production retains the existing Hyprland provider and titlebars 0.3.0-1.

This work reviews only Hyprland and its matching titlebars package. The nine other pending proprietary-package redistribution decisions and the existing initial-adoption review backlog remain unresolved. The fully audited README snapshot is not advanced. Final ordinary and complete reconciliation results are recorded below.

Final reconciliation against the pinned target: ordinary and `--complete` checks both exit 1. There are 168 existing initial-adoption reviews outstanding, nine pending redistribution decisions, and two testing candidates marked `ready` rather than production-published. The Hyprland and titlebars reviews are current. See the machine-readable record for every unresolved entry and review issue.
