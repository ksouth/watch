# watch — generic monitoring and archival template (draft 1)

This branch is an additive template extraction based on the reusable parts of
MyNDIS. It contains no MyNDIS or NDIS archive data and is not configured for a
real monitored site.

Start by copying WATCH_CONFIG.draft-1.py to WATCH_CONFIG.py and replacing the
example values. The URL configuration is intentionally centralized there.

The template preserves the following design principles: source bytes remain
distinct from interpretation; SHA-256 hashes and capture times are recorded;
robots decisions and failures are explicit; a missing or failed request never
deletes a prior capture; and generated reports are derived artifacts.

This is draft 1. Review before enabling scheduled automation.
