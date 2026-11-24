#!/usr/bin/env python3
"""Shared facts and helpers for the personal site.

`python3 tools/build_site.py` writes the HTML through renew.write_all.
English copy is in tools/renew.py and Korean copy in tools/ko_copy.py.
PUBLISH_KO turns the Korean pages on.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# True writes the Korean pages under ko/ and the KO/EN switch. False writes
# English only and deletes ko/ (GitHub Pages serves every committed path).
PUBLISH_KO = True

# Figures shared by the English and Korean pages. Korean copy (tools/ko_copy.py)
# takes every number from here, and renew.write_all() refuses to write the site
# if a Korean page and its English pair carry different numbers.
FACTS = {
    "cost_before": "USD 1.05",
    "cost_after": "USD 0.036",
    "cost_cut": "96.6%",
    "cycles": "1,000",
    "transplant": "93.8%",
    "thinning": "87.5%",
    "runner": "65%",
    "ces": "CES 2025",
    "trials": "1,000",
    "cad_success": "93%",
    "bin_success": "89%",
    "patent": "10-2694987",
    "queries": "300",
    "gpa": "3.34/4.5",
}
SITE = "https://imjaewoochoi.github.io"
EMAIL = "iam.jaewoochoi@gmail.com"
GITHUB = "https://github.com/ImJaewooChoi"
KAGGLE = "https://www.kaggle.com/loveacaji"
LINKEDIN = "https://www.linkedin.com/in/jaewoo-choi-955340356"
WHALE = "https://github.com/ImJaewooChoi/kaggle_happy_whale"
MATCH = "https://github.com/ImJaewooChoi/kaggle_image_matching2022"

GROUPS = [
    {
        "id": "daedong",
        "org": "Daedong AILab",
        "role": {"en": "Senior AI Researcher", "ko": "Senior AI Researcher"},
        "when": {"en": "May 2024 to present", "ko": "2024년 5월부터 현재"},
    },
    {
        "id": "plaif",
        "org": "PLAIF",
        "role": {"en": "Computer Vision Engineer", "ko": "Computer Vision Engineer"},
        "when": {"en": "Jan 2023 to Apr 2024", "ko": "2023년 1월부터 2024년 4월"},
    },
    {
        "id": "fs",
        "org": "FS Solution Co., Ltd.",
        "role": {"en": "Computer Vision Engineer", "ko": "Computer Vision Engineer"},
        "when": {"en": "May 2022 to Dec 2022", "ko": "2022년 5월부터 2022년 12월"},
    },
]


# Order of the project rows and pages, and the employer each belongs to.
PROJECTS = [
    {"slug": "language-distilled-segmentation", "group": "daedong"},
    {"slug": "auto-labeling", "group": "daedong"},
    {"slug": "strawberry-cultivation", "group": "daedong"},
    {"slug": "cad-free-assembly", "group": "plaif"},
    {"slug": "bin-picking", "group": "plaif"},
    {"slug": "ros-6d-vision", "group": "plaif"},
    {"slug": "license-plate", "group": "fs"},
]

def esc(s):
    return html.escape(s, quote=True)


def home_href(lang):
    return "/" if lang == "en" else "/ko/"


def project_href(lang, slug):
    prefix = "/projects/" if lang == "en" else "/ko/projects/"
    return f"{prefix}{slug}.html"


def abs_url(path):
    if path == "/":
        return SITE + "/"
    return SITE + path



PATENT_TITLE = (
    "Pose estimating device and method using artificial intelligence to "
    "estimate pose of robot's end effector for object and robot control "
    "system including the same."
)


def glue_tokens(text):
    text = re.sub(
        r"\b((?:January|February|March|April|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?)\s+(\d{4})",
        lambda m: f"{m.group(1)}\u00a0{m.group(2)}",
        text,
    )
    text = text.replace(" to present", "\u00a0\u2013\u00a0present")
    text = re.sub(
        r" to (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
        lambda m: f"\u00a0\u2013\u00a0{m.group(1)}",
        text,
    )
    text = re.sub(r"\bUSD\s+", "USD\u00a0", text)
    text = re.sub(r"\bPatent\s+(?=\d)", "Patent\u00a0", text)
    text = re.sub(r"\bCES\s+", "CES\u00a0", text)
    text = re.sub(r"\b6D\s+", "6D\u00a0", text)
    return text


def harden_text(text):
    text = glue_tokens(text)
    text = re.sub(r"(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])", "\u2011", text)
    return text


def harden_html(doc):
    parts = re.split(r"(<[^>]*>)", doc)
    out = []
    skip = False
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<script", "<style", "<title")) and not low.startswith("</"):
                skip = True
            out.append(part)
            if low.startswith(("</script", "</style", "</title")):
                skip = False
            continue
        out.append(part if skip else harden_text(part))
    return "".join(out)


def main():
    from renew import write_all
    write_all()


if __name__ == "__main__":
    main()
