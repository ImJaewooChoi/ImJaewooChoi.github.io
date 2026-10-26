#!/usr/bin/env python3
"""Quiet research ledger. Facts come from build_site.

Direction: quiet-instrument, seed 398551681 (Albert Sans, sheet and biro).
The dealt hero is two doors on a dark wall, and the ledger blueprint is a
560px column with a hover preview. Neither can hold this record: the owner
asked for a white page, and the first screen has to show the name, the role,
eight dated results, the patent and Kaggle lines, and the contact links.
Pictures sit below that, smaller, with no crossfade.
"""

import shutil

from build_site import (
    DISPLAY,
    EMAIL,
    GITHUB,
    GROUPS,
    KAGGLE,
    LINKEDIN,
    MATCH,
    PATENT_TITLE,
    PROJECTS,
    PUBLISH_KO,
    ROOT,
    SITE,
    VIDEOS,
    WHALE,
    abs_url,
    esc,
    harden_html,
    project_href,
)

FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
)

# Employment is the only date the CV gives a project. Present has not ended,
# so it sorts ahead of every finished role. Projects that share a period keep
# the order they already have in PROJECTS: nothing in the content ends one
# of them later than the others.
_END = {
    "daedong": (9999, 12),
    "plaif": (2024, 4),
    "fs": (2022, 12),
}
_START = {
    "daedong": (2024, 5),
    "plaif": (2023, 1),
    "fs": (2022, 5),
}

FOCUS = "Perception for robots that leave the lab."

# Kept to one line on a 390px screen. The project pages carry the full sentences.
RESULT = {
    "strawberry-cultivation": "93.8% / 87.5% / 65%, 1,000 trials. CES 2025.",
    "cad-free-assembly": "93% success, 1,000 trials. Patent 10-2694987.",
    "bin-picking": "89% success, 1,000 trials, five object types.",
    "language-distilled-segmentation": "Production RT100. Teacher is training-only.",
    "orchard-obstacle-mapping": "Occupancy grid on RT100, Jetson Nano.",
    "auto-labeling": "About USD 1.05 to about 0.036 (96.6%).",
    "ros-6d-vision": "Base and camera-frame poses over ROS.",
    "license-plate": "Detection locates the plate. OCR reads it.",
}

HEADS = {
    "strawberry-cultivation": "Strawberry tasks",
    "cad-free-assembly": "Assembly",
    "bin-picking": "Bin picking",
    "language-distilled-segmentation": "Orchard masks",
    "orchard-obstacle-mapping": "Obstacle maps",
    "auto-labeling": "Labeling cost",
    "ros-6d-vision": "Poses over ROS",
    "license-plate": "License plates",
}

FIGURES = {
    "strawberry-cultivation": [
        ("93.8%", "Transplanting"),
        ("87.5%", "Flower thinning"),
        ("65%", "Runner handling"),
        ("1,000", "Fixed-lab trials"),
    ],
    "cad-free-assembly": [
        ("93%", "Task success"),
        ("1,000", "In-house trials"),
        ("2D", "Camera at run time"),
        ("10-2694987", "Korean patent"),
    ],
    "bin-picking": [
        ("89%", "Task success"),
        ("1,000", "In-house trials"),
        ("5", "Object types"),
    ],
    "language-distilled-segmentation": [
        ("RT100", "Production pipeline"),
        ("None", "Added inference cost"),
    ],
    "orchard-obstacle-mapping": [
        ("RT100", "Production robots"),
        ("Nano", "TensorRT on Jetson"),
    ],
    "auto-labeling": [
        ("1.05", "USD per image, before"),
        ("0.036", "USD per image, after"),
        ("96.6%", "Cost reduction"),
    ],
    "ros-6d-vision": [
        ("6D", "Poses returned"),
        ("AX=YB", "Eye-to-hand batch"),
    ],
    "license-plate": [
        ("Detect", "Find the plate"),
        ("OCR", "Letters and digits"),
    ],
}

STILLS = [
    ("strawberry-cultivation", "CES booth", "/assets/frames/strawberry-booth.jpg", "Flower thinning at the CES 2025 booth."),
    ("strawberry-cultivation", "Close view", "/assets/frames/strawberry-close.jpg", "A closer view of flower thinning at the CES 2025 booth."),
    ("cad-free-assembly", "Assembly", "/assets/frames/cad-room.jpg", "UR arm with a gripper and wrist camera, assembling a part on a fixture."),
    ("bin-picking", "Bin picking", "/assets/frames/bin-arm.jpg", "A Doosan cobot during CAD-based bin picking."),
]

GROUP_BY = {g["id"]: g for g in GROUPS}


def ordered_projects():
    indexed = list(enumerate(PROJECTS))
    indexed.sort(key=lambda pair: (-_END[pair[1]["group"]][0], -_END[pair[1]["group"]][1], -_START[pair[1]["group"]][0], -_START[pair[1]["group"]][1], pair[0]))
    return [project for _, project in indexed]


def when_of(project):
    return GROUP_BY[project["group"]]["when"]["en"]


SCRIPT = """<script>
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("video").forEach(function (v) {
    v.muted = true;
    if (reduce) {
      v.removeAttribute("autoplay");
      v.pause();
      v.controls = true;
    }
  });
})();
</script>"""


def head(title, desc, path):
    canonical = abs_url(path)
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Jaewoo Choi">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(canonical)}">
<link rel="alternate" hreflang="x-default" href="{esc(canonical)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="/assets/css/site.css">
</head>"""


def document(title, desc, path, body):
    return f"""<!DOCTYPE html>
<html lang="en">
{head(title, desc, path)}
<body>
<a class="skip" href="#content">Skip to content</a>
{body}
{footer()}
{SCRIPT}
</body>
</html>
"""


def bar(home=False):
    _ = home
    return f"""<header class="bar">
<a class="wordmark rise" style="--d:0ms" href="/">Jaewoo Choi</a>
<nav aria-label="Sections">
<a class="rise" style="--d:30ms" href="/#work">Work</a>
<a class="rise" style="--d:50ms" href="/#record">Record</a>
<a class="rise" style="--d:70ms" href="/#practice">Practice</a>
</nav>
</header>"""


def work_index():
    chunks = []
    current = None
    delay = 0
    for project in ordered_projects():
        group = GROUP_BY[project["group"]]
        if group["id"] != current:
            current = group["id"]
            chunks.append(f'<h3>{esc(group["org"])}</h3>')
        slug = project["slug"]
        delay += 30
        chunks.append(
            f'<li class="rise" style="--d:{delay}ms">'
            f'<a href="{esc(project_href("en", slug))}">'
            f'<span class="name">{esc(HEADS[slug])}</span>'
            f'<span class="when">{esc(when_of(project))}</span>'
            f'<span class="result">{esc(RESULT[slug])}</span>'
            f"</a></li>"
        )
    # h3 siblings of li is invalid. Wrap each group.
    grouped = []
    bucket = []
    heading = ""
    for part in chunks:
        if part.startswith("<h3>"):
            if heading:
                grouped.append(f"<div class=\"group\">{heading}<ul>{''.join(bucket)}</ul></div>")
            heading = part
            bucket = []
        else:
            bucket.append(part)
    if heading:
        grouped.append(f"<div class=\"group\">{heading}<ul>{''.join(bucket)}</ul></div>")
    return "\n".join(grouped)


def home_frames():
    # Only three projects were filmed. Two frames each, same size, newest
    # project first. The other five have no footage, so they stay in the
    # index only. No clip on the home page: the strawberry trial would
    # become the main item again.
    frames = [
        ("strawberry-cultivation", "/assets/frames/strawberry-booth.jpg", "Flower thinning at the CES 2025 booth."),
        ("strawberry-cultivation", "/assets/frames/strawberry-close.jpg", "A closer view of flower thinning at the CES 2025 booth."),
        ("cad-free-assembly", "/assets/frames/cad-room.jpg", "UR arm with a gripper and wrist camera, assembling a part on a fixture."),
        ("cad-free-assembly", "/assets/frames/cad-detail.jpg", "A closer view of the UR arm, gripper, wrist camera, and fixture."),
        ("bin-picking", "/assets/frames/bin-arm.jpg", "A Doosan cobot during CAD-based bin picking."),
        ("bin-picking", "/assets/frames/bin-ring.jpg", "A Doosan cobot with a suction gripper picking ring parts from a bin."),
    ]
    items = []
    for i, (slug, src, alt) in enumerate(frames):
        items.append(
            f'<li class="rise" style="--d:{i * 40}ms"><a href="{esc(project_href("en", slug))}">'
            f'<img src="{esc(src)}" alt="{esc(alt)}" width="1280" height="720">'
            f"<span>{esc(HEADS[slug])}</span></a></li>"
        )
    return f"""<section class="films frames" id="frames">
<h2>Frames</h2>
<ul class="stills">{"".join(items)}</ul>
</section>"""


def home_page():
    body = f"""{bar(home=True)}
<main id="content">
<section class="sheet">
<div class="identity">
<h1>Jaewoo Choi</h1>
<p class="role">Senior AI Researcher, Daedong AILab, <span class="keep">since May 2024</span></p>
<p class="focus">{esc(FOCUS)}</p>
</div>
<div class="reach">
<a class="btn" href="mailto:{esc(EMAIL)}">Email Jaewoo</a>
<p class="socials">
<a href="{esc(GITHUB)}" rel="me">GitHub</a>
<a href="{esc(KAGGLE)}" rel="me">Kaggle</a>
<a href="{esc(LINKEDIN)}" rel="me">LinkedIn</a>
</p>
<a class="mail" href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a>
</div>
<div class="index" id="work">
<h2>Work</h2>
{work_index()}
</div>
<div class="record" id="record">
<h2>Record</h2>
<ul>
<li class="rise" style="--d:40ms"><a href="{esc(project_href("en", "cad-free-assembly"))}">Patent 10-2694987</a>, Aug 2024. Co-inventor.</li>
<li class="rise" style="--d:70ms">UBC-OCEAN, bronze, 83/1,326, Jan 2024.</li>
<li class="rise" style="--d:100ms"><a href="{esc(MATCH)}">Image Matching Challenge 2022</a>, silver, 50/642.</li>
<li class="rise" style="--d:130ms"><a href="{esc(WHALE)}">Happywhale</a>, bronze, 127/1,588, Apr 2022. Whale and Dolphin Identification.</li>
<li class="rise" style="--d:160ms">Code: <a href="{esc(GITHUB)}" rel="me">GitHub</a>, <a href="{esc(MATCH)}">Image Matching</a>, <a href="{esc(WHALE)}">Happywhale</a>.</li>
</ul>
</div>
</section>
<section class="practice" id="practice">
<h2>Practice</h2>
<div class="practice-grid">
<div class="prose">
<p class="rise" style="--d:40ms">Open-vocabulary RGB-D segmentation, point-cloud and image fusion for obstacle mapping, 6D pose estimation, and imitation learning for manipulation. Tested on deployed orchard robots and on manipulation robots.</p>
<p class="rise" style="--d:80ms">Bachelor of Engineering, Industrial Management Systems Engineering, at Seokyeong University, Seoul, Mar 2016 to Aug 2022. Multidisciplinary major: Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies).</p>
<p class="rise" style="--d:120ms">Co-inventor of Korean Patent 10-2694987, registered Aug 2024. Applicant PLAIF. The basis is the CAD-free assembly work. The registered title is: {esc(PATENT_TITLE)}</p>
</div>
<div>
<h3>Roles</h3>
<ul class="roles">
<li><span>Daedong AILab, Senior AI Researcher</span><span>May 2024 to present</span></li>
<li><span>PLAIF, Computer Vision Engineer</span><span>Jan 2023 to Apr 2024</span></li>
<li><span>FS Solution Co., Ltd., Computer Vision Engineer</span><span>May 2022 to Dec 2022</span></li>
</ul>
</div>
</div>
</section>
{home_frames()}
</main>"""
    title = "Jaewoo Choi, Senior AI Researcher"
    desc = "Senior AI Researcher at Daedong AILab. Perception for orchard robots and manipulation arms."
    return document(title, desc, "/", body)


def footer():
    return f"""<footer class="foot">
<p class="rise" style="--d:40ms">Robot vision, measured.</p>
<p class="foot-links rise" style="--d:60ms">
<a href="mailto:{esc(EMAIL)}">Email</a>
<a href="{esc(GITHUB)}" rel="me">GitHub</a>
<a href="{esc(KAGGLE)}" rel="me">Kaggle</a>
<a href="{esc(LINKEDIN)}" rel="me">LinkedIn</a>
</p>
<p class="rise" style="--d:80ms">© Jaewoo Choi</p>
</footer>"""


def stills():
    items = []
    for i, (slug, label, src, alt) in enumerate(STILLS):
        items.append(
            f'<li class="rise" style="--d:{i * 40}ms"><a href="{esc(project_href("en", slug))}">'
            f'<img src="{esc(src)}" alt="{esc(alt)}" width="1280" height="720">'
            f"<span>{esc(label)}</span></a></li>"
        )
    return f'<ul class="stills">{"".join(items)}</ul>'


def figures(slug):
    rows = FIGURES.get(slug) or []
    items = "\n".join(
        f'<li class="rise" style="--d:{i * 40}ms"><strong>{esc(value)}</strong><span>{esc(label)}</span></li>'
        for i, (value, label) in enumerate(rows)
    )
    return f'<ul class="figures">\n{items}\n</ul>'


def split_sections(project):
    blocks = []
    sections = list(project["sections"]["en"])
    if project["slug"] == "cad-free-assembly":
        sections.append((
            "Patent",
            f"<p>Korean Patent 10-2694987, registered Aug 2024. Applicant PLAIF. Co-inventor. The registered title is: {esc(PATENT_TITLE)}</p>",
        ))
    for heading, html in sections:
        paras = html if isinstance(html, str) else ""
        # Two columns when a section has more than one paragraph, so the
        # right side of a wide screen is part of the same section.
        parts = [p for p in paras.split("</p>") if p.strip()]
        marked = paras.replace("<p>", '<p class="rise" style="--d:50ms">')
        if len(parts) >= 2:
            bits = [p for p in marked.split("</p>") if p.strip()]
            mid = (len(bits) + 1) // 2
            left = "</p>".join(bits[:mid]) + "</p>"
            right = "</p>".join(bits[mid:]) + "</p>"
            prose = f'<div class="prose split"><div>{left}</div><div>{right}</div></div>'
        else:
            prose = f'<div class="prose">{marked}</div>'
        blocks.append(
            f'<section class="block"><h2 class="rise" style="--d:30ms">{esc(heading)}</h2>{prose}</section>'
        )
    return "\n".join(blocks)


def pager(project):
    projects = ordered_projects()
    idx = next(i for i, item in enumerate(projects) if item["slug"] == project["slug"])
    links = []
    if idx > 0:
        prev = projects[idx - 1]
        links.append(
            f'<a class="rise" style="--d:40ms" href="{esc(project_href("en", prev["slug"]))}">'
            f'{esc(HEADS[prev["slug"]])} <span>{esc(when_of(prev))}</span></a>'
        )
    if idx + 1 < len(projects):
        nxt = projects[idx + 1]
        links.append(
            f'<a class="rise" style="--d:70ms" href="{esc(project_href("en", nxt["slug"]))}">'
            f'{esc(HEADS[nxt["slug"]])} <span>{esc(when_of(nxt))}</span></a>'
        )
    return f'<nav class="pager" aria-label="Adjacent projects">{"".join(links)}</nav>'


def project_page(project):
    slug = project["slug"]
    info = DISPLAY[slug]
    group = GROUP_BY[project["group"]]
    title = HEADS[slug]
    media = ""
    if project["video"]:
        v = VIDEOS[project["video"]]
        src = f"/assets/video/{v['file']}.mp4"
        poster = f"/assets/video/{v['file']}.jpg"
        media = f"""<figure class="project-media">
<video width="{v['w']}" height="{v['h']}" muted playsinline preload="metadata" controls poster="{esc(poster)}" aria-label="{esc(v['label']['en'])}">
<source src="{esc(src)}" type="video/mp4">
</video>
<figcaption>{esc(v['cap']['en'])}</figcaption>
</figure>"""
    else:
        # Pages without their own film still carry one labeled clip from the trials.
        v = VIDEOS["strawberry"]
        media = f"""<figure class="project-media">
<video width="{v['w']}" height="{v['h']}" muted playsinline preload="metadata" controls poster="/assets/video/strawberry-ces2025.jpg" aria-label="{esc(v['label']['en'])}">
<source src="/assets/video/strawberry-ces2025.mp4" type="video/mp4">
</video>
<figcaption>Another filmed trial. {esc(v['cap']['en'])}</figcaption>
</figure>"""
    body = f"""{bar()}
<main id="content">
<article class="project">
<div class="project-top">
<div class="project-copy">
<h1>{esc(title)}</h1>
<p class="meta rise" style="--d:40ms">{esc(group['org'])}. {esc(group['role']['en'])}. {esc(group['when']['en'])}.</p>
{figures(slug)}
<p class="did rise" style="--d:80ms">{esc(info['blurb'])}</p>
<p class="action"><a class="btn" href="mailto:{esc(EMAIL)}">Email Jaewoo</a></p>
</div>
{media}
</div>
{split_sections(project)}
<section class="films">
<h2>Filmed trials</h2>
{stills()}
</section>
{pager(project)}
</article>
</main>"""
    return document(f"{title}, Jaewoo Choi", info["blurb"], project_href("en", slug), body)


def not_found_page():
    body = f"""{bar()}
<main id="content" class="missing">
<h1>Not found</h1>
<p class="rise" style="--d:40ms">The address does not match a project or a section.</p>
<p class="action rise" style="--d:55ms"><a class="btn" href="/">Back to the index</a></p>
<section class="films">
<h2 class="rise" style="--d:70ms">Filmed trials</h2>
<figure class="clip rise" style="--d:90ms">
<video class="rise" style="--d:110ms" width="540" height="960" muted playsinline preload="metadata" controls poster="/assets/video/strawberry-ces2025.jpg" aria-label="Silent. Flower thinning at the CES 2025 booth">
<source src="/assets/video/strawberry-ces2025.mp4" type="video/mp4">
</video>
<figcaption>Flower thinning at the CES 2025 booth.</figcaption>
</figure>
{stills()}
</section>
</main>"""
    return document("Page not found", "This address is not on the site.", "/404.html", body)


def write_all():
    pages = {
        "index.html": home_page(),
        "404.html": not_found_page(),
    }
    for project in PROJECTS:
        pages[f"projects/{project['slug']}.html"] = project_page(project)
    ko_dir = ROOT / "ko"
    if not PUBLISH_KO and ko_dir.exists():
        shutil.rmtree(ko_dir)
        print("removed ko/")
    for rel, text in pages.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(harden_html(text), encoding="utf-8")
        print("wrote", rel)
    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        sitemap.unlink()
        print("removed sitemap.xml")
    _ = SITE
