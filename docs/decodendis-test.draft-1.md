# Decode NDIS dry run

Target: https://decodendis.pplx.app/

The site is visibly a client-rendered single-page application. Its navigation
uses hash routes such as the glossary, blog, policy, ART cases, roundups, and
about sections. A normal server-side sitemap crawl may capture the application
shell but miss content generated after JavaScript execution.

Therefore the first dry run should be treated as a structural test, not a
claim of complete coverage. The next adapter should:

- preserve the root HTML/application shell;
- enumerate the visible hash routes;
- capture each rendered route with a browser-capable runner;
- record route, title, capture time, and content hash;
- preserve linked source URLs separately from the site's own content;
- report routes that fail to render or expose no readable content.

No Decode NDIS source content is copied into the template by this configuration
file.
