"""Draft-2 configuration for the generic watch scraper."""
PROJECT_NAME = "Replace with project name"
BASE_URL = "https://example.org"
SITEMAP_URL = "https://example.org/sitemap.xml"
ARCHIVE_ROOT = "archive"
PUBLISHED_ARCHIVE_BASE_URL = None
USER_AGENT = "WatchArchiveBot/1.0 (+https://github.com/ksouth/watch)"
REQUEST_DELAY_SECONDS = 0.5
REQUEST_TIMEOUT_SECONDS = 30
MAX_URLS = 5000
DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".zip"]
CAPTURE_ASSETS_FOR_PATHS = ["/"]
