# NDIA Accountability dry-run procedure

1. Open GitHub Actions.
2. Select “Dry run — NDIA Accountability Project”.
3. Choose “Run workflow” on the template-draft-1 branch.
4. Download the ndia-accountability-dry-run artifact.
5. Review the manifest, errors, robots exclusions, source paths, and hashes.
6. Do not merge or schedule the archive until the coverage and privacy review is complete.

The workflow has read-only repository permissions. It does not commit captured pages
or documents back into the repository. It uploads the temporary result for seven
days so it can be inspected and discarded by expiry.

The separate public API is intentionally not included in this dry run.
