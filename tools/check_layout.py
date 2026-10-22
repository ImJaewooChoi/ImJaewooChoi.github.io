#!/usr/bin/env python3
"""Overflow, line measure, hyphen breaks, and robots meta for the static site."""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8765"
WIDTHS = [360, 390, 768, 1024, 1280, 1440, 1920]
HYPHEN_END = ("-", "‐", "‑")  # hyphen-minus, hyphen, non-breaking hyphen

PROSE_JS = r"""
() => {
  const proseSel = "p.bio, p.measure, p.dek, .prose p:not(.stack), .entry > p:not(.tools)";
  const hyphenSel = "main p, main h1, main h2, main h3, main li, main figcaption";

  function lineStrings(el) {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    const range = document.createRange();
    const buckets = new Map();
    for (const node of nodes) {
      const text = node.textContent;
      for (let i = 0; i < text.length; i++) {
        range.setStart(node, i);
        range.setEnd(node, i + 1);
        const rect = range.getClientRects()[0];
        if (!rect || rect.width < 0.2) continue;
        const key = Math.round(rect.top);
        const prev = buckets.get(key) || { text: "", width: 0, right: 0, left: rect.left };
        prev.text += text[i];
        prev.right = Math.max(prev.right, rect.right);
        prev.left = Math.min(prev.left, rect.left);
        prev.width = prev.right - prev.left;
        buckets.set(key, prev);
      }
    }
    return [...buckets.entries()].sort((a, b) => a[0] - b[0]).map((x) => x[1]);
  }

  const thin = [];
  for (const el of document.querySelectorAll(proseSel)) {
    const lines = lineStrings(el);
    if (!lines.length) continue;
    const box = el.getBoundingClientRect().width;
    if (box < 8) continue;
    const avg = lines.reduce((s, l) => s + l.width, 0) / lines.length;
    const ratio = avg / box;
    if (ratio < 0.6) {
      thin.push({
        ratio: Math.round(ratio * 1000) / 1000,
        lines: lines.length,
        box: Math.round(box),
        text: (el.innerText || "").replace(/\s+/g, " ").slice(0, 140),
      });
    }
  }

  const hyphens = [];
  for (const el of document.querySelectorAll(hyphenSel)) {
    const lines = lineStrings(el);
    lines.forEach((line, i) => {
      const trimmed = line.text.replace(/\s+$/g, "");
      const last = trimmed.slice(-1);
      if (last === "-" || last === "‐" || last === "‑") {
        hyphens.push({
          line: i + 1,
          end: trimmed.slice(-24),
          text: (el.innerText || "").replace(/\s+/g, " ").slice(0, 120),
        });
      }
    });
  }

  const doc = document.documentElement;
  const overflow = doc.scrollWidth > doc.clientWidth + 1;
  const wrap = document.querySelector(".wrap");
  const wrapBox = wrap ? Math.round(wrap.getBoundingClientRect().width) : 0;
  return {
    overflow,
    scrollWidth: doc.scrollWidth,
    clientWidth: doc.clientWidth,
    wrap: wrapBox,
    thin,
    hyphens,
  };
}
"""

ROBOTS_JS = r"""
() => {
  const robots = document.querySelector('meta[name="robots"]');
  const og = document.querySelector('[property^="og:"], meta[name^="twitter:"]');
  const br = document.body.innerHTML.includes("<br");
  return {
    robots: robots ? robots.getAttribute("content") : "",
    share: og ? (og.getAttribute("property") || og.getAttribute("name")) : "",
    br,
  };
}
"""

CONTRAST_JS = r"""
() => {
  function parse(c) {
    const m = c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    return m ? [+m[1], +m[2], +m[3]] : null;
  }
  const picks = [
    ["body", "body"],
    ["muted", ".loc"],
    ["link", "main a"],
    ["h1", "h1"],
  ];
  const out = [];
  for (const [name, sel] of picks) {
    const el = document.querySelector(sel);
    if (!el) continue;
    const cs = getComputedStyle(el);
    out.push({
      name,
      fg: parse(cs.color),
      bg: parse(getComputedStyle(document.body).backgroundColor),
      size: cs.fontSize,
    });
  }
  return out;
}
"""


def rel_luminance(rgb):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    L1, L2 = rel_luminance(a), rel_luminance(b)
    hi, lo = max(L1, L2), min(L1, L2)
    return (hi + 0.05) / (lo + 0.05)


def is_published(path):
    rel = path.relative_to(ROOT)
    return not any(part.startswith(("_", ".")) for part in rel.parts)


def pages():
    found = []
    for path in sorted(ROOT.rglob("*.html")):
        if not is_published(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "index.html":
            found.append("/")
        elif rel == "ko/index.html":
            found.append("/ko/")
        else:
            found.append("/" + rel)
    return found


def static_checks():
    errors = []
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if re.search(r"(?i)disallow", robots):
        errors.append("robots.txt contains Disallow")
    if re.search(r"(?i)sitemap", robots):
        errors.append("robots.txt points at a sitemap")
    if (ROOT / "sitemap.xml").exists():
        errors.append("sitemap.xml exists")
    for path in ROOT.rglob("*.html"):
        if not is_published(path):
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if 'hreflang="ko"' in text or "/ko/" in text or 'href="/ko"' in text:
            errors.append(f"{rel} still points at a Korean page")
        if 'name="robots" content="noindex, nofollow, noarchive"' not in text:
            errors.append(f"{rel} missing robots noindex meta")
        if "og:" in text or "twitter:" in text:
            errors.append(f"{rel} has share metadata")
        if "<br" in text.lower():
            errors.append(f"{rel} has a br")
        if "No media yet" in text or "미디어 없음" in text:
            errors.append(f"{rel} still has an empty-media label")
    return errors


def main():
    errors = static_checks()
    urls = pages()
    print(f"pages {len(urls)}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": 900})
            for url in urls:
                page.goto(BASE + url, wait_until="domcontentloaded")
                page.evaluate("document.fonts.ready")
                meta = page.evaluate(ROBOTS_JS)
                if meta["robots"] != "noindex, nofollow, noarchive":
                    errors.append(f"{url} @{width} robots={meta['robots']!r}")
                if meta["share"]:
                    errors.append(f"{url} @{width} share tag {meta['share']}")
                if meta["br"]:
                    errors.append(f"{url} @{width} rendered br")
                layout = page.evaluate(PROSE_JS)
                if layout["overflow"]:
                    errors.append(
                        f"{url} @{width} overflow {layout['scrollWidth']}>{layout['clientWidth']}"
                    )
                for item in layout["thin"]:
                    errors.append(
                        f"{url} @{width} thin {item['ratio']:.0%} of {item['box']}px "
                        f"({item['lines']} lines) {item['text']}"
                    )
                for item in layout["hyphens"]:
                    errors.append(
                        f"{url} @{width} hyphen line {item['line']} …{item['end']}"
                    )
            if width == 1440:
                page.goto(BASE + "/", wait_until="domcontentloaded")
                page.evaluate("document.fonts.ready")
                info = page.evaluate(PROSE_JS)
                print(f"home wrap {info['wrap']}px at {width}")
                for scheme in ("light", "dark"):
                    page.emulate_media(color_scheme=scheme)
                    samples = page.evaluate(CONTRAST_JS)
                    for sample in samples:
                        if not sample["fg"] or not sample["bg"]:
                            errors.append(f"contrast {scheme} {sample['name']} unparsed")
                            continue
                        ratio = contrast(sample["fg"], sample["bg"])
                        print(f"contrast {scheme} {sample['name']} {ratio:.2f}")
                        if ratio < 4.5:
                            errors.append(
                                f"contrast {scheme} {sample['name']} {ratio:.2f} < 4.5"
                            )
            page.close()
        browser.close()

    if errors:
        print(f"FAIL {len(errors)}")
        for err in errors:
            print(" -", err)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
