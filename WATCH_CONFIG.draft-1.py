"""Project-specific configuration for the generic watch template.

Copy this file to WATCH_CONFIG.py and edit it for a monitored site.
The template intentionally contains no MyNDIS or NDIS URLs.
"""
PROJECT_NAME = "Replace with project name"
PROJECT_DESCRIPTION = "Replace with a short description"
START_URLS = ["https://example.org/"]
ALLOWED_HOSTS = {"example.org"}
FOLLOW_EXTERNAL_LINKS = False
ARCHIVE_EXTERNAL_DOCUMENTS = True
CHECK_ROBOTS = True
REQUEST_DELAY_SECONDS = 0.5
MAX_URLS = 5000
MAX_RUNTIME_SECONDS = 4200
ARCHIVE_ROOT = "archive"
WIKI_ROOT = "wiki"
USER_AGENT = "WatchArchiveBot/1.0 (+https://github.com/ksouth/watch)"
