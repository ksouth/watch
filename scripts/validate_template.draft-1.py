#!/usr/bin/env python3
"""Fail if project-specific URLs leak outside the configuration surface."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
allowed_files = {"WATCH_CONFIG.py", "WATCH_CONFIG.draft-1.py"}
blocked = ("ndis.gov.au", "myndiswiki.github.io", "myNDISwiki/MyNDIS")
found = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.name in allowed_files or path.suffix in {".pyc", ".bin"}:
        continue
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        continue
    for needle in blocked:
        if needle.lower() in text.lower():
            found.append(f"{path.relative_to(ROOT)}: {needle}")
if found:
    print("\n".join(found))
    raise SystemExit("template validation failed")
print("template validation passed")
