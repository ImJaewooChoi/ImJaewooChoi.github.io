# Jaewoo Choi

Personal site: https://imjaewoochoi.github.io

Static HTML and CSS. The published site is English. Korean copy stays in `tools/build_site.py` (`PUBLISH_KO = False`) and is not written to `ko/`.

The home page is a faculty skim: name and role, one research sentence, contact links, one evidence line, then eight project rows. A filmed project has a short muted clip on the left of its row. A project without footage has the same empty slot. Patent and awards, education, and experience sit below the list.

`python3 tools/build_site.py` rewrites `index.html`, `projects/*.html`, and `404.html`. Project videos are in `assets/video/`. Home-row clips are in `assets/video/home/`. The pages do not link to `/cv.pdf`.

Every page sends `noindex, nofollow, noarchive`, plus `og:title` and `og:description`. There is no `og:image`. `robots.txt` stays allow-all. There is no sitemap.
