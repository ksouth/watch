# Configuration

The intended user entry point is WATCH_CONFIG.py.

Configure project identity, starting URLs, allowed hosts, external-document
policy, robots.txt checking, request delay, safety limits, and output paths.

Do not put monitored URLs directly in scraper modules, workflows, dashboards, or
wiki pages. A validator should reject site-specific URLs outside configuration
and explicitly marked examples.

A failed request is not proof that a source was deleted. Preserve the last
successful capture and record the failed attempt separately.
