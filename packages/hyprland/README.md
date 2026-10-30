# Omarchy-patched Fedora Hyprland candidate

This recipe starts from the Fedora integration in [LionHeartP/hyprlandRPM](https://github.com/LionHeartP/hyprlandRPM/tree/1a2422834d0db4889a33621556eb094b01aba32b/hyprland-git) and builds the official Hyprland 0.57.0 release archive. Companion libraries remain provided by that Fedora COPR. No replacement library stack is bundled.

The unchanged Omarchy patches are pinned to `omacom/omarchy-pkgs` commit `b766e177b0ab827f2154e4b76cf8c7c158d3b86b`:

- Release the EGL context and thread in the NVIDIA-compatible teardown order.
- Keep retired `wl_output` globals alive for five seconds, including globals with no bound resources, so late binds during connector flaps do not disconnect clients.
- Treat VRR-only monitor-rule changes as soft differences and refresh VRR after the deferred monitor-rule application.

All archive, macro and patch downloads are checked with `sources.sha256`. The Fedora regression/ABI patch is fetched from an immutable packaging commit. Its source includes the upstream project's existing license terms.

## ABI and tests

The client/server plugin hash includes `_omadora_912521ee8a53_`, derived from the three upstream patch files. This distinguishes patched headers from unpatched headers without falsifying the upstream Git commit identity. Titlebars is rebuilt against, and requires, the exact candidate Hyprland RPM release. Other plugins must be rebuilt for the candidate headers too.

The release library is compiled once. An optional Fedora CMake target links the upstream GTests directly against that same uninstrumented library; it neither instruments the shipped executable nor installs the interactive test harness. The additional tests cover VRR-only comparisons, inherited VRR settings, removed/unbound output grace, output lifetime after the grace period while resources remain bound, and matching plugin ABI hashes. The output fixture advances the real timer deterministically and retains the original resource-drain tests.

`test/hyprland-runtime-test.py` launches a disposable nested compositor under a private D-Bus session and temporary HOME/config/runtime paths. It disables seat acquisition and systemd environment/target integration, and sends requests only to its own IPC socket. Its C client deliberately sends a stale `wl_registry.bind` after removal and recreation of an output with the same name. The unpatched Fedora 0.57.0-1 build reproduces `global wl_output … is unavailable` (EPROTO 71). The candidate must let that same request bind and release normally. Optional arguments test rejection of an unpatched plugin and load/unload of matching titlebars, followed by clean compositor exit.

## Publication scope

Candidates are built in [kammer/omadora-hyprland-testing](https://copr.fedorainfracloud.org/coprs/kammer/omadora-hyprland-testing/) from the `hyprland-testing` branch. The production Omadora source definitions and installed desktop are not switched by this work. No test repository is enabled on the host.

Physical NVIDIA exit behavior, physical monitor VRR, suspend/resume and real dock hotplug require a separate hardware/session test before full runtime qualification. The available host has AMD GPUs. See the candidate validation report for measured results and remaining work.
