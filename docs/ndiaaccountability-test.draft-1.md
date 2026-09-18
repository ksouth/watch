# NDIA Accountability Project dry run

Target: https://ndiaaccountability.org/

The site is server-rendered and exposes ordinary page routes, including the
document library, FOI requests, inquiry submissions, statistics, Service Code,
lived experiences, deaths, project status, news, and FAQ pages.

The first run should crawl the public website and linked public documents while
recording robots decisions, failures, hashes, and content changes. It should
not automatically harvest the separate public API at corpus-rag.fly.dev. API
coverage is a distinct scope because it may expose a very large, changing
document corpus and needs its own rate limits, pagination rules, and data
handling review.

The site contains sensitive subject matter, including disability, health,
death, institutional conduct, and lived-experience records. The archive should
preserve public source provenance and access boundaries, but generated indexes
must not add unnecessary personal-data summaries.
