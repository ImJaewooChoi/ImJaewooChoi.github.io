# Jaewoo Choi

Personal site: https://imjaewoochoi.github.io

Static HTML and CSS. English is at `/` and Korean at `/ko/`, page for page. Korean copy is in `tools/ko_copy.py` and takes every figure from `FACTS` in `tools/build_site.py`. The build stops if a Korean page and its English pair carry different numbers (`tools/check_parity.py`). `PUBLISH_KO = False` writes English only.

Each page has a KO/EN switch in the top bar and `hreflang` links for en, ko and x-default (English). The switch saves the choice in `localStorage` (`lang`). With no saved choice, a visitor whose browser language starts with `ko` and who opens the English home page `/` with no referrer or a same-site referrer is sent to `/ko/` once. Deep links and links from other sites are never redirected. There is no IP lookup.

The home page is a faculty skim: name and role, a short research intro, icon contact links, then seven project rows. A filmed project has a short muted clip on the left of its row. A project without footage has the same empty slot. Patent and awards, education, and experience sit below the list.

`python3 tools/build_site.py` rewrites `index.html`, `projects/*.html`, and `404.html`, and the same files under `ko/`. Project videos are in `assets/video/`. Home-row clips are in `assets/video/home/`. The pages do not link to `/cv.pdf`.

Every page sends `noindex, nofollow, noarchive`, plus `og:title` and `og:description`. There is no `og:image`. `robots.txt` stays allow-all. There is no sitemap.
