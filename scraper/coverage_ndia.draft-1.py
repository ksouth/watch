#!/usr/bin/env python3
"""Build a conservative coverage report for the NDIA Accountability website."""
from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import requests
from bs4 import BeautifulSoup

BASE = "https://ndiaaccountability.org/"
EXPECTED = [
    "/", "/about/", "/faq/", "/status/", "/links/", "/news/",
    "/library/documents/", "/library/requests/",
    "/library/external-submissions/", "/library/statistics/",
    "/code/", "/experiences/", "/deaths/",
]
EXTERNAL_HOSTS = {"corpus-rag.fly.dev"}
OUT = Path("archive/ndia-accountability/coverage")

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def inspect(session, path):
    url = urljoin(BASE, path)
    row = {"path": path, "url": url, "checked_at": now()}
    try:
        response = session.get(url, timeout=30, allow_redirects=True)
        row.update(status=response.status_code, final_url=response.url,
                   content_type=response.headers.get("content-type", ""))
        soup = BeautifulSoup(response.text, "html.parser")
        links = sorted({urljoin(response.url, a.get("href")) for a in soup.select("a[href]")})
        same = [u for u in links if urlsplit(u).netloc == urlsplit(BASE).netloc]
        external = [u for u in links if urlsplit(u).hostname in EXTERNAL_HOSTS]
        text = soup.get_text(" ", strip=True).lower()
        row.update(
            title=soup.title.get_text(" ", strip=True) if soup.title else "",
            same_host_links=len(same),
            external_api_links=external,
            pagination_signals=sorted(set(re.findall(r"(?:page|paged|offset|limit|next|older|load more)", text))),
            has_api_reference=bool(external) or "api" in text,
            text_length=len(text),
        )
    except requests.RequestException as exc:
        row.update(status=None, error=str(exc))
    return row

def main():
    session = requests.Session()
    session.headers["User-Agent"] = "WatchCoverageBot/1.0 (+https://github.com/ksouth/watch)"
    rows = [inspect(session, path) for path in EXPECTED]
    report = {
        "project": "NDIA Accountability Project",
        "checked_at": now(),
        "coverage_type": "route inventory, not complete corpus capture",
        "expected_routes": EXPECTED,
        "routes": rows,
        "limitations": [
            "This report does not enumerate every document, request, or submission.",
            "The separate public API requires a dedicated pagination and data-handling adapter.",
            "A successful route response does not prove complete linked-resource coverage.",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "coverage.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# NDIA Accountability coverage report",
        "",
        f"Checked: {report['checked_at']}",
        "",
        "This is a route inventory, not a complete corpus capture.",
        "",
        "| Route | Status | Title | Text chars | Pagination signals | API reference |",
        "| --- | ---: | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append("| {path} | {status} | {title} | {text_length} | {pagination_signals} | {has_api_reference} |".format(
            path=row["path"], status=row.get("status", "error"), title=row.get("title", "").replace("|", "\\|"),
            text_length=row.get("text_length", 0), pagination_signals=", ".join(row.get("pagination_signals", [])) or "none",
            has_api_reference=row.get("has_api_reference", False)))
    lines += ["", "## Limits", ""] + [f"- {item}" for item in report["limitations"]]
    (OUT / "coverage.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT / 'coverage.json'} and {OUT / 'coverage.md'}")

if __name__ == "__main__":
    main()
