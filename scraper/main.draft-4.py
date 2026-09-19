#!/usr/bin/env python3
"""Additive recursive crawler for the watch template.

This draft keeps the existing runner untouched and expands discovery by following
same-host HTML links, pagination links, linked documents, and JSON/API references.
It writes a new snapshot into the configured archive root.
"""
from __future__ import annotations
import hashlib, html, importlib.util, json, sys, time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "WATCH_CONFIG.py"
EXTS = {".pdf",".doc",".docx",".xls",".xlsx",".csv",".txt",".zip",".json"}
ASSET_EXTS = {".css",".js",".png",".jpg",".jpeg",".gif",".svg",".webp",".ico"," .woff"," .woff2"}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def digest(b): return hashlib.sha256(b).hexdigest()
def load():
    spec=importlib.util.spec_from_file_location("cfg",CFG); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
def canon(raw, base, keep_query=False):
    u=urljoin(base,raw); p=urlsplit(u); bp=urlsplit(base)
    if p.scheme not in {"http","https"} or (p.hostname or "").removeprefix("www.") != (bp.hostname or "").removeprefix("www."): return None
    path=p.path or "/"
    if path != "/": path=path.rstrip("/")
    return urlunsplit(("https",bp.netloc,path,p.query if keep_query else "", ""))
def parts(url):
    p=unquote(urlsplit(url).path).strip("/")
    return ["home"] if not p else ["".join(c if c.isalnum() or c in "._-" else "_" for c in x).strip(".") or "_" for x in p.split("/")]
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists() or path.read_bytes()!=data: path.write_bytes(data); return True
    return False
def main():
    m=load(); base=m.BASE_URL; root=ROOT/m.ARCHIVE_ROOT; root.mkdir(parents=True,exist_ok=True)
    delay=float(getattr(m,"REQUEST_DELAY_SECONDS",1)); timeout=int(getattr(m,"REQUEST_TIMEOUT_SECONDS",30)); limit=int(getattr(m,"MAX_URLS",5000))
    ua=getattr(m,"USER_AGENT","WatchArchiveBot/1.0"); s=requests.Session(); s.headers.update({"User-Agent":ua,"Accept":"text/html,application/xhtml+xml,application/pdf,application/json,*/*;q=0.8"})
    q=deque([canon(base,base,True)]); seen=set(); docs=set(); records=[]; errors=[]; checked=now()
    while q and len(seen)<limit:
        url=q.popleft()
        if not url or url in seen: continue
        seen.add(url)
        try:
            time.sleep(delay); r=s.get(url,timeout=timeout,allow_redirects=True); r.raise_for_status()
            final=canon(r.url,base,True) or url; typ=r.headers.get("content-type",""); data=r.content
            is_html="html" in typ.lower() or (not typ and data.lstrip().startswith(b"<"))
            if is_html:
                path=root/"pages"/Path(*parts(final))/ "index.html"; soup=BeautifulSoup(data,"html.parser")
                for a in soup.find_all("a",href=True):
                    raw=a["href"]; plain=canon(raw,final,True); nos=canon(raw,final,False)
                    ext=Path(urlsplit(plain or nos or "").path).suffix.lower()
                    if ext in EXTS: docs.add(plain or nos)
                    elif plain and len(seen)+len(q)<limit:
                        q.append(plain)
                for tag in soup.find_all(["script","link"],src=True):
                    ref=canon(tag.get("src"),final,False)
                    if ref and Path(urlsplit(ref).path).suffix.lower() in {".json",".js"}: records.append({"page":final,"reference":ref,"kind":"asset_or_api"})
                for tag in soup.find_all("link",href=True):
                    ref=canon(tag.get("href"),final,False)
                    if ref and "api" in ref.lower(): records.append({"page":final,"reference":ref,"kind":"api"})
                save(path,data); rel=path.relative_to(ROOT).as_posix()
            else:
                path=root/"files"/Path(*parts(final)); save(path,data); rel=path.relative_to(ROOT).as_posix()
            records.append({"url":final,"path":rel,"status":r.status_code,"content_type":typ,"sha256":digest(data),"discovered_from":url})
            print(f"[{len(seen)}] {final}")
        except requests.RequestException as e:
            errors.append({"url":url,"error":str(e)}); print(f"ERROR {url}: {e}",file=sys.stderr)
    for url in sorted(docs):
        if url in seen: continue
        try:
            time.sleep(delay); r=s.get(url,timeout=timeout,allow_redirects=True); r.raise_for_status(); final=canon(r.url,base,True) or url; data=r.content; path=root/"files"/Path(*parts(final)); save(path,data); records.append({"url":final,"path":path.relative_to(ROOT).as_posix(),"status":r.status_code,"content_type":r.headers.get("content-type",""),"sha256":digest(data),"kind":"linked_document"})
        except requests.RequestException as e: errors.append({"url":url,"error":str(e)})
    active=[x for x in records if x.get("path","").startswith((root/"pages").relative_to(ROOT).as_posix()+"/")]
    links="\n".join(f'<li><a href="{html.escape(Path(x["path"]).relative_to(ROOT).relative_to(root).as_posix(),quote=True)}">{html.escape(urlsplit(x["url"]).path or "/")}</a></li>' for x in sorted(active,key=lambda x:x["url"]))
    (root/"index.html").write_text(f'<!doctype html><meta charset="utf-8"><title>NDIA Accountability Archive</title><h1>NDIA Accountability Archive</h1><p>Recursive capture: {len(active)} HTML pages, {len(docs)} linked documents, checked {checked}.</p><ul>{links}</ul>',encoding="utf-8")
    (root/"crawl-report.json").write_text(json.dumps({"checked_at":checked,"pages_seen":len(seen),"html_pages":len(active),"linked_documents":len(docs),"queue_remaining":len(q),"api_or_asset_references":records,"errors":errors},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"DONE pages={len(active)} documents={len(docs)} errors={len(errors)} remaining={len(q)}")
if __name__=="__main__": raise SystemExit(main())
