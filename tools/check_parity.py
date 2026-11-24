#!/usr/bin/env python3
"""Compare the numbers on every English page with its Korean pair.

Text, title, meta description, alt and aria-label are read from each built
page. Before comparing:
- non-breaking hyphens and spaces are normalized;
- English dates "May 2024" become "2024년 5월", the Korean form.
A number is a digit run (with , or . inside, optional % M K) that is not part
of a name such as RT100, SigLIP2, FP16 or 6D. The multisets must be equal.
"""

import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
NUM = re.compile(r"(?<![A-Za-z0-9.,])\d+(?:[.,]\d+)*(?:%|[MK](?![A-Za-z]))?(?![A-Za-z0-9])")


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        for key in ("alt", "aria-label"):
            if a.get(key):
                self.parts.append(a[key])
        if tag == "meta" and a.get("name") == "description":
            self.parts.append(a.get("content", ""))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def page_text(path):
    parser = Text()
    parser.feed(path.read_text(encoding="utf-8"))
    text = " ".join(parser.parts)
    return text.replace("\u2011", "-").replace("\u00a0", " ")


def numbers(text, lang):
    if lang == "en":
        text = re.sub(
            r"\b(Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)\.?\s+(\d{4})",
            lambda m: f"{m.group(2)}년 {MONTHS[m.group(1)[:3]]}월",
            text,
        )
    return Counter(NUM.findall(text))


def pairs():
    out = []
    for ko in sorted((ROOT / "ko").rglob("*.html")):
        en = ROOT / ko.relative_to(ROOT / "ko")
        out.append((en, ko))
    return out


def compare():
    problems = []
    for en, ko in pairs():
        if not en.exists():
            problems.append(f"{ko.relative_to(ROOT)} has no English pair")
            continue
        a, b = numbers(page_text(en), "en"), numbers(page_text(ko), "ko")
        if a != b:
            problems.append(
                f"{en.relative_to(ROOT)}: only EN {dict(a - b)}, only KO {dict(b - a)}"
            )
    return problems


def main():
    rows = pairs()
    problems = compare()
    for en, ko in rows:
        n = sum(numbers(page_text(en), "en").values()) if en.exists() else 0
        print(f"{en.relative_to(ROOT)} <-> {ko.relative_to(ROOT)}: {n} numbers")
    if problems:
        print(f"FAIL {len(problems)}")
        for p in problems:
            print(" -", p)
        return 1
    print(f"PASS {len(rows)} pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
