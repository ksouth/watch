# Generic watch template structure

The template separates four concerns:

1. WATCH_CONFIG.py: project-specific URLs and policy.
2. scraper/: reusable capture, robots, hashing, manifest, and reporting logic.
3. archive/: captured source bytes and machine-readable inventories.
4. wiki/ and docs/: human-authored documentation and methodology.

A new monitored project should be created by copying the configuration example,
running the validator, and reviewing the first dry-run output before enabling
scheduled GitHub Actions.
