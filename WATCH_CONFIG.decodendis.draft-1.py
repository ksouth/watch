"""Decode NDIS target configuration for a controlled dry run.

This is kept separate from the generic template config so the repository remains
usable as a blank template. The site is a client-rendered single-page app:
the visible navigation uses hash routes and does not expose a conventional
HTML sitemap in the observed page.
"""
PROJECT_NAME = "NDIS Decoded"
BASE_URL = "https://decodendis.pplx.app/"
SITEMAP_URL = BASE_URL
ARCHIVE_ROOT = "archive/decodendis"
PUBLISHED_ARCHIVE_BASE_URL = None
USER_AGENT = "WatchArchiveBot/1.0 (+https://github.com/ksouth/watch)"
REQUEST_DELAY_SECONDS = 0.75
REQUEST_TIMEOUT_SECONDS = 30
MAX_URLS = 100
DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".zip"]
CAPTURE_ASSETS_FOR_PATHS = ["/"]
