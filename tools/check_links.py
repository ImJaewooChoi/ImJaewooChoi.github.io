#!/usr/bin/env python3
"""Check that published pages only link to files that exist.

Off-site URLs are skipped. /cv.pdf is the known placeholder and is reported,
not failed. Korean output under a leading-underscore path is not part of the
published site.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://imjaewoochoi.github.io"
ALLOW_MISSING = {"/cv.pdf"}


def published(path):
    rel = path.relative_to(ROOT)
    if not rel.parts:
        return False
    if any(part.startswith(("_", ".")) for part in rel.parts):
        return False
    if rel.parts[0] == "tools":
        return False
    return True


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        for key in ("href", "src", "poster"):
            if data.get(key):
                self.found.append(data[key])


def local_target(url, base):
    url = url.strip().strip("\"'")
    if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    if url.startswith(SITE):
        url = url[len(SITE) :] or "/"
    elif url.startswith(("http://", "https://", "//")):
        return None
    path = url.split("#", 1)[0].split("?", 1)[0]
    if path in ("", "/"):
        return "/index.html"
    if path.startswith("/"):
        if path.endswith("/"):
            return "/" + path.strip("/") + "/index.html"
        return path
    joined = (base / path).resolve()
    try:
        rel = joined.relative_to(ROOT)
    except ValueError:
        return None
    text = "/" + rel.as_posix()
    if text.endswith("/"):
        return text + "index.html"
    return text


def main():
    missing = []
    allowed = []
    checked = 0
    pages = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or not published(path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        urls = []
        if path.suffix == ".html":
            pages += 1
            parser = Links()
            parser.feed(text)
            urls.extend(parser.found)
        elif path.suffix == ".css":
            urls.extend(re.findall(r"url\(\s*([^)]+?)\s*\)", text))
        else:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for url in urls:
            target = local_target(url, path.parent)
            if target is None:
                continue
            checked += 1
            file_path = ROOT / target.lstrip("/")
            if file_path.is_file():
                continue
            if target in ALLOW_MISSING:
                allowed.append(f"{rel} -> {target}")
                continue
            missing.append(f"{rel} -> {url}")

    print(f"pages {pages}")
    print(f"local links {checked}")
    print(f"missing {len(missing)}")
    for item in missing:
        print(" -", item)
    print(f"placeholder {len(allowed)}")
    for item in allowed:
        print(" -", item)
    if missing:
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
