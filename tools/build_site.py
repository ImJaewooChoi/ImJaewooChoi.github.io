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


def _tf(left, right, post=None):
    """Transform with a leading superscript frame: {}^{left}T_{right}^{post}."""
    post_sup = f"<mtext>{post}</mtext>" if post else "<none/>"
    right_ml = right if right.startswith("<") else f"<mi>{right}</mi>"
    return (f"<mmultiscripts><mi>T</mi>{right_ml}{post_sup}"
            f"<mprescripts/><none/><mi>{left}</mi></mmultiscripts>")


def _pt(frame):
    return (f"<mmultiscripts><mi>X</mi><mi>i</mi><none/>"
            f"<mprescripts/><none/><mi>{frame}</mi></mmultiscripts>")


def _eq(body, label):
    return (f'<div class="eq"><math display="block" aria-label="{label}">'
            f"<mrow>{body}</mrow></math></div>")


# CAD-free assembly pose chain. Same markup in English and Korean.
CADFREE_EQUATIONS = "\n".join([
    _eq(f"{_tf('O', 'E')}<mo>=</mo>"
        f"<msup><mrow><mo>(</mo>{_tf('B', 'R')}<mo>)</mo></mrow><mrow><mo>&#8722;</mo><mn>1</mn></mrow></msup>"
        f"<mo>&#8290;</mo>{_tf('B', 'E', 'ref')}",
        "O T E equals the inverse of B T R times B T E ref"),
    _eq(f"{_pt('O')}<mo>=</mo><msub><mi>d</mi><mi>i</mi></msub><mo>&#8290;</mo>"
        f"<msubsup><mi>K</mi><mi>R</mi><mrow><mo>&#8722;</mo><mn>1</mn></mrow></msubsup><mo>&#8290;</mo>"
        f"<msup><mrow><mo>[</mo><msub><mi>u</mi><mi>i</mi></msub><mo>,</mo><msub><mi>v</mi><mi>i</mi></msub>"
        f"<mo>,</mo><mn>1</mn><mo>]</mo></mrow><mi>&#8868;</mi></msup>",
        "O X i equals d i times K R inverse times u i, v i, 1 transposed"),
    _eq(f"{_tf('C', 'O')}<mo>=</mo><msub><mtext>solvePnP</mtext><mtext>RANSAC</mtext></msub>"
        f"<mrow><mo>(</mo><mo>{{</mo><mo>(</mo>{_pt('O')}<mo>,</mo><msub><mi>x</mi><mi>i</mi></msub>"
        f"<mo>)</mo><mo>}}</mo><mo>)</mo></mrow>",
        "C T O equals solvePnP RANSAC of the pairs O X i, x i"),
    _eq(f"{_tf('B', 'E', 'target')}<mo>=</mo>{_tf('B', 'C')}<mo>&#8290;</mo>{_tf('C', 'O')}"
        f"<mo>&#8290;</mo>{_tf('O', 'E')}",
        "B T E target equals B T C times C T O times O T E"),
])


def _vec(sym, frame, idx):
    """Point with a leading frame superscript: {}^{frame}sym_{idx}."""
    idx_ml = idx if idx.startswith("<") else f"<mi>{idx}</mi>"
    return (f"<mmultiscripts><mi>{sym}</mi>{idx_ml}<none/>"
            f"<mprescripts/><none/><mi>{frame}</mi></mmultiscripts>")


_INV = "<mrow><mo>&#8722;</mo><mn>1</mn></mrow>"
_PS = "<msub><mi>P</mi><mi>s</mi></msub>"
_PT = "<msub><mi>P</mi><mi>t</mi></msub>"
_JI = "<mrow><mi>j</mi><mo>(</mo><mi>i</mi><mo>)</mo></mrow>"

# CAD-based bin picking pose chain. Same markup in English and Korean.
BINPICK_EQUATIONS = "\n".join([
    _eq(f"{_vec('p', 'E', 'i')}<mo>=</mo>"
        f"<msup><mrow><mo>(</mo>{_tf('O', 'E')}<mo>)</mo></mrow>{_INV}</msup>"
        f"<mo>&#8290;</mo>{_vec('p', 'O', 'i')}",
        "E p i equals the inverse of O T E times O p i"),
    _eq(f"{_tf('C', 'E', '(0)')}<mo>=</mo>{_tf('C', _PS)}<mo>&#8290;</mo>"
        f"<msup><mrow><mo>(</mo>{_tf('E', _PT)}<mo>)</mo></mrow>{_INV}</msup>",
        "C T E initial equals C T P s times the inverse of E T P t"),
    _eq(f"{_tf('C', 'E')}<mo>=</mo>"
        f"<munder><mo movablelimits=\"false\">argmin</mo><mrow><mi>R</mi><mo>&#8712;</mo><mi>SO</mi><mo>(</mo><mn>3</mn><mo>)</mo>"
        f"<mo>,</mo><mi>t</mi><mo>&#8712;</mo><msup><mi>&#8477;</mi><mn>3</mn></msup></mrow></munder>"
        f"<munder><mo movablelimits=\"false\">&#8721;</mo><mi>i</mi></munder>"
        f"<msup><mrow><mo>&#8214;</mo><mi>R</mi><mo>&#8290;</mo>{_vec('p', 'E', 'i')}<mo>+</mo><mi>t</mi>"
        f"<mo>&#8722;</mo>{_vec('q', 'C', _JI)}<mo>&#8214;</mo></mrow><mn>2</mn></msup>",
        "C T E equals argmin over R in SO 3 and t in R 3 of the sum over i of the squared norm of R E p i plus t minus C q j of i"),
    _eq(f"{_tf('B', 'E')}<mo>=</mo>{_tf('B', 'C')}<mo>&#8290;</mo>{_tf('C', 'E')}"
        f"<mo>=</mo>{_tf('B', 'C')}<mo>&#8290;</mo>{_tf('C', 'O')}<mo>&#8290;</mo>{_tf('O', 'E')}",
        "B T E equals B T C times C T E, which equals B T C times C T O times O T E"),
])

def tf_html(left, right):
    """Inline HTML form of {}^{left}T_{right} for running text."""
    return f'<span class="tf"><sup>{left}</sup>T<sub>{right}</sub></span>'


def main():
    from renew import write_all
    write_all()


if __name__ == "__main__":
    main()
