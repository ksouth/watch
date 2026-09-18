#!/usr/bin/env python3
"""Generic URL inventory and archive scaffold for watch.

This draft is deliberately conservative: it separates configuration from
capture mechanics and records failures instead of treating them as deletion.
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

def timestamp():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def canonical_url(value: str, base: str = "") -> str | None:
    parsed = urlsplit(urljoin(base, value))
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    return urlunsplit((parsed.scheme, parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))

def in_scope(url: str, allowed_hosts: set[str]) -> bool:
    return (urlsplit(url).hostname or "").lower() in {h.lower() for h in allowed_hosts}

def empty_manifest(project_name: str) -> dict:
    return {"format_version": 1, "project": project_name, "checked_at": None,
            "status": "not-run", "entries": {}, "errors": [], "pending": []}

def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    temporary.replace(path)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
