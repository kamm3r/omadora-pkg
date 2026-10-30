# Reconcile an upstream update

Use `tools/reconcile.py` to account for the complete upstream tree. It reads Git objects without executing PKGBUILDs and hashes every file in each recipe directory, including patches and auxiliary files. It also hashes the local recipe and catalog disposition so a later edit requires another review.

1. Fetch `https://github.com/omacom/omarchy-pkgs.git` into a separate checkout. Resolve `origin/master` to a full commit and use that same `--ref` throughout the update. Run the check before editing:

   ```bash
   python3 tools/reconcile.py --upstream /path/to/omarchy-pkgs --ref <commit> check
   ```

2. Handle every reported recipe. Add new Fedora specs and checksum files, port changed versions, sources, patches, dependencies, and packaging behavior, and retire deleted recipes and their COPR definitions. Check dependencies against Fedora rather than translating names mechanically. Keep `catalog.tsv` current. A removed recipe retained for Fedora needs a reason and `review --retain-removed`; one maintained in another repository needs `--external-recipe <location>`.

3. Reassess every `pending` entry on every update. Resolve feasible ports; document a concrete remaining blocker for the rest. Check whether `not-applicable` decisions still apply whenever their upstream recipe changes. During initial adoption every entry requires review: the tool deliberately has no bulk accept command, and a previous README snapshot hash is not proof that a recipe was reviewed.

4. Validate changed source checksums and source RPMs with `.copr/Makefile`, then run focused tests and clean Fedora binary builds. For each completed recipe review, record the result:

   ```bash
   python3 tools/reconcile.py --upstream /path/to/omarchy-pkgs --ref <commit> review <package> --reason 'Describe the upstream change, Fedora disposition, and validation evidence'
   ```

   A review records a manual decision, not a successful build. Keep `pending` and `ready` truthful; acknowledging a blocker does not make a package published.

5. Follow the README's webhook pause and publication procedure. Verify COPR results and repository metadata for every submitted build, update the publication record and catalog, then record reviews again for changed catalog rows. Distinguish submitted, failed, published, and intentionally excluded packages. Removing a recipe from the repository or COPR does not uninstall it from existing systems.

6. Run both final checks against the pinned target:

   ```bash
   python3 tools/reconcile.py --upstream /path/to/omarchy-pkgs --ref <commit> check
   python3 tools/reconcile.py --upstream /path/to/omarchy-pkgs --ref <commit> check --complete --json
   ```

   The ordinary check fails for unaccounted changes and structural inconsistencies, and always lists pending/unpublished work. `--complete` also fails while any catalog package is pending or ready. Report the exact target commit, validations, publication results, exclusions, and unresolved work. Describe an update with remaining blockers as partial; advance the README's fully audited snapshot only when the ordinary check passes. Commit `upstream-reviews.json` with the corresponding recipes and catalog changes.

The tool checks accounting, not semantic equivalence or live COPR availability. A human or agent must port recipes and verify build/publication evidence. Nothing fetches, builds, publishes, deletes COPR packages, or changes installed software automatically.
