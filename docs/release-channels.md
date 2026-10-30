# COPR release channels

Omadora uses `edge -> rc -> stable` for Fedora 44 x86_64. Stable remains `kammer/omadora`, so existing installations keep their repository URL. The other projects are `kammer/omadora-edge` and `kammer/omadora-rc`. Enable exactly one Omadora channel on a machine. Channel switching does not automatically downgrade installed RPMs.

New builds run in edge. RC and stable have package automatic rebuilds disabled and receive copies of tested builds. The existing GitHub integration targets edge, with package sources explicitly pinned to `main` (external recipes retain their reviewed source configuration). Each automatic edge recipe sets its COPR subdirectory to its own `packages/<name>` directory, so documentation and other recipes do not rebuild it. The root `.copr/Makefile` supports COPR invoking it from those directories. Shared build-helper changes need an explicit review and targeted rebuilds with increased releases where appropriate. The separate `omadora-hyprland-testing` sandbox is not automatically promoted; its remaining hardware qualification still applies. Limine and gaming remain separate repositories.

## Promotion unit and identity

COPR's supported fork operation copies a whole project's latest successful build for each package/chroot; it does not select arbitrary packages. We therefore promote a frozen **whole-channel snapshot**, not individual package names. This keeps coordinated packages in one reviewed set. COPR copies RPMs without recompiling, then signs them with the destination project's key. Full RPM checksums can differ between channels. All three channels use `max_builds=0` (retain build records), because repeated whole-project copies include unchanged NEVRAs; pruning those records can delete shared Pulp artifacts. Promotion reasserts this setting on source and destination definitions. Cleanup requires a separate artifact-reference review. We compare immutable header SHA256 and payload SHA256, and verify downloaded RPM bytes against each repository's own metadata checksums.

The [channel policy](../.copr/channels.json) and [promotion tool](../tools/channels.py) enforce:

- Only edge to rc, or rc to stable. No skipping or reverse transitions.
- RPM epoch/version/release comparisons reject downgrades, including numeric releases and prereleases.
- A changed build under the same NEVRA is rejected; increase `Release` and test again. A new project signature alone is allowed.
- Source must include destination packages; removals require a separate reviewed retirement.
- Core and Hyprland/titlebars package groups must be complete when changing. Titlebars must require the exact staged compositor release.
- Only the configured single chroot is supported. Latest successful build outputs must match the visible latest RPMs; COPR's build-time selection cannot silently pick an older version.
- Source and destination must have no active builds or automatic rebuilds. Plans pin definitions, build IDs, repository checksums and immutable content digests. A stale plan is rejected.
- Test evidence must reference the plan hash. RC requires automated-test evidence; stable also requires desktop-test evidence.
- The tool writes a `submission-intent` receipt before calling COPR, preserving recovery information even if the request fails. An intent receipt alone does not prove submission or publication. Submission and publication verification are separate. Copy failures or partial copies never become a verified release receipt. Receipts cannot overwrite earlier records.

This is a maintainer workflow, not a COPR server authorization feature. Project administrators can bypass it with direct builds or fork commands. Do not submit manual builds, edit definitions or perform another promotion while a snapshot is frozen. COPR does not offer an atomic lock across projects, and a fork is asynchronous; an unsuccessful copy may leave partial content visible. Keep rc/stable promotion credentials restricted to release maintainers, and investigate a failed copy before retrying. The tool does not claim atomic multi-package publication or a full DNF dependency solve.

## Core builds

The `omarchy` and `omarchy-settings` definitions are manual in edge: their shared `omadora-revision` lives outside their recipe directories, and a broad root webhook would rebuild unchanged versions on every documentation push. After changing that pin, explicitly build `omarchy-settings` and then `omarchy` in **edge**. Check their matching version/release before creating the release plan. The other 134 previously automatic recipes retain automatic edge builds, now scoped to their own directories. New recipe definitions must also use `main`, a recipe subdirectory, `make_srpm`, and `max_builds=0`.

## Run a release

Install `python3-copr` and `python3-rpm` and configure COPR credentials normally. Use the system Python so the RPM bindings are available. Keep plans, evidence and receipts under `.copr/promotions/` with unique names and commit them after verification. No credentials belong in those files.

Pause automatic builds before the first maintenance push. Keep them paused until the final push webhook is delivered, then restore exactly the edge enabled set from the freeze receipt. RC and stable stay disabled.

```bash
python3 tools/channels.py freeze edge --out .copr/promotions/release-freeze.json
# Wait for existing builds to finish; freezing does not cancel them.
python3 tools/channels.py plan --from edge --to rc --out .copr/promotions/release-edge-rc-plan.json
```

Run the automated checks for that exact snapshot. Write evidence with its printed plan SHA256:

```json
{
  "plan_sha256": "<printed plan hash>",
  "checks": {
    "automated-tests": {
      "result": "passed",
      "details": "Path or URL to the test report for these build IDs, commands and results"
    }
  }
}
```

The tool validates the evidence binding and gate status; it does not execute tests or establish the truth of a maintainer's attestation. Evidence must describe measured results, including applicable hardware tests. Do not mark unperformed checks passed.

```bash
python3 tools/channels.py apply --plan .copr/promotions/release-edge-rc-plan.json --evidence .copr/promotions/release-edge-rc-tests.json --out .copr/promotions/release-edge-rc-submitted.json
# COPR copies asynchronously. Run verification once it has finished.
python3 tools/channels.py verify --receipt .copr/promotions/release-edge-rc-submitted.json --out .copr/promotions/release-edge-rc-verified.json
```

After real desktop testing, create a **new** rc-to-stable plan and evidence containing both `automated-tests` and `desktop-tests`. Use the same apply/verify commands. Reuse neither the edge plan nor its hash. Keep edge frozen through verification, or complete edge-to-rc verification before thawing edge for another development cycle. RC remains frozen while it is tested and promoted.

Commit the evidence and verified receipts, verify the final GitHub delivery, then resume edge:

```bash
python3 tools/channels.py thaw --receipt .copr/promotions/release-freeze.json
```

If a stable package is broken, publish a corrected build with a higher epoch/version/release through edge and rc. Any exceptional rollback, retirement, chroot change or emergency direct publication is a separate explicitly reviewed operation outside this forward-only tool.

## Bootstrap

The initial creation copies the already-published stable baseline into empty edge and rc projects. This one-time seed is not a reverse release promotion, introduces no new stable package, and is recorded separately. After bootstrap there is no reverse-copy command in the release tool. The configuration report is in `.copr/promotions/bootstrap-2026-10-30.json`.
