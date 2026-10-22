# Jaewoo Choi

Personal site: https://imjaewoochoi.github.io

Static HTML and CSS. The published site is English. Korean copy stays in `tools/build_site.py` (`PUBLISH_KO = False`) and is not written to `ko/`. Pages send `noindex, nofollow, noarchive`. `robots.txt` stays allow-all so a crawler can see that tag. There is no sitemap.

`python3 tools/build_site.py` rewrites the HTML. Project videos are in `assets/video/`. Put a CV file at `cv.pdf` when it is ready. That file is not in the repo yet.
