"""NDIA Accountability Project target configuration for a controlled dry run.

This remains separate from the blank template configuration. The site is
server-rendered and exposes a public navigation structure plus a separate
public API. The first run should crawl the website only; API harvesting needs
a separately reviewed adapter and rate limit.
"""
PROJECT_NAME = "NDIA Accountability Project"
BASE_URL = "https://ndiaaccountability.org/"
SITEMAP_URL = "https://ndiaaccountability.org/"
ARCHIVE_ROOT = "archive/ndia-accountability"
PUBLISHED_ARCHIVE_BASE_URL = None
USER_AGENT = "WatchArchiveBot/1.0 (+https://github.com/ksouth/watch)"
REQUEST_DELAY_SECONDS = 1.0
REQUEST_TIMEOUT_SECONDS = 30
MAX_URLS = 5000
DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".zip"]
CAPTURE_ASSETS_FOR_PATHS = ["/"]
