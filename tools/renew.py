#!/usr/bin/env python3
"""Pinned-poster pages. Facts come from build_site; the sheet drives the form."""

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
    '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">'
)

MARQUEE = [
    "Transplanting",
    "Flower thinning",
    "Runner handling",
    "Assembly",
    "Bin picking",
    "Patent 10-2694987",
    "UBC-OCEAN",
    "Image Matching",
    "Happywhale",
]

# Short names for the held square. Facts are the measured ones.
WORK = [
    ("strawberry-cultivation", "Strawberry", "strawberry", "Imitation learning", "93.8%", ""),
    ("cad-free-assembly", "Assembly", "assembly", "6D pose", "93%", ""),
    ("bin-picking", "Bin picking", "bin", "RGB-D", "89%", ""),
    ("language-distilled-segmentation", "Orchard", "", "RT100", "Training only", "RT100"),
    ("orchard-obstacle-mapping", "Obstacles", "", "Occupancy grid", "Jetson Nano", "Jetson"),
    ("auto-labeling", "Labeling", "", "Auto-labeling", "USD 0.036", "0.036"),
    ("ros-6d-vision", "ROS vision", "", "Eye to hand", "6D", "6D"),
    ("license-plate", "Plates", "", "Detection", "OCR", "OCR"),
]

FRAMES = {
    "strawberry": "/assets/frames/strawberry-booth.jpg",
    "assembly": "/assets/frames/cad-room.jpg",
    "bin": "/assets/frames/bin-arm.jpg",
}

STILLS = [
    ("strawberry-cultivation", "CES booth", "/assets/frames/strawberry-booth.jpg", "Flower thinning at the CES 2025 booth."),
    ("strawberry-cultivation", "Close view", "/assets/frames/strawberry-close.jpg", "A closer view of flower thinning at the CES 2025 booth."),
    ("cad-free-assembly", "Assembly", "/assets/frames/cad-room.jpg", "UR arm with a gripper and wrist camera, assembling a part on a fixture."),
    ("bin-picking", "Bin picking", "/assets/frames/bin-arm.jpg", "A Doosan cobot during CAD-based bin picking."),
]

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

LEADS = {
    "strawberry-cultivation": "Three strawberry tasks, learned from UMI demonstrations and Diffusion Policy.",
    "cad-free-assembly": "6D tool poses from a 2D camera, with no CAD model of the part.",
    "bin-picking": "Picking poses from RGB-D images and known CAD geometry.",
    "language-distilled-segmentation": "Instance masks for the RT100. The language teacher is used only while training.",
    "orchard-obstacle-mapping": "Open-set obstacles go into an occupancy grid on the production RT100.",
    "auto-labeling": "Point prompts become tracked masks. Region-grounded captions follow.",
    "ros-6d-vision": "A ROS action server returns robot-base and camera-frame poses.",
    "license-plate": "Object detection locates the plate. OCR reads the letters and digits.",
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

SCRIPT = """<script>
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var stage = document.querySelector(".stage");
  if (stage && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var n = entry.target.getAttribute("data-stage");
        stage.classList.toggle("is-2", n === "2");
        stage.classList.toggle("is-3", n === "3");
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: [0, 0.25] });
    stage.querySelectorAll("[data-stage]").forEach(function (m) { io.observe(m); });
  }
  var links = document.querySelectorAll(".names a");
  var imgs = document.querySelectorAll(".square img");
  var fig = document.querySelector(".square-figure");
  var left = document.querySelector(".fact-l");
  var right = document.querySelector(".fact-r");
  function showWork(a) {
    var id = a.getAttribute("data-img") || "";
    imgs.forEach(function (img) {
      img.classList.toggle("is-on", id !== "" && img.getAttribute("data-for") === id);
    });
    if (fig) fig.textContent = id ? "" : (a.getAttribute("data-fig") || "");
    if (left) left.textContent = a.getAttribute("data-left") || "";
    if (right) right.textContent = a.getAttribute("data-right") || "";
    links.forEach(function (x) { x.classList.toggle("is-current", x === a); });
  }
  if (links.length && "IntersectionObserver" in window) {
    var nio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) showWork(entry.target);
      });
    }, { rootMargin: "-46% 0px -46% 0px", threshold: 0 });
    links.forEach(function (a) {
      nio.observe(a);
      a.addEventListener("focus", function () { showWork(a); });
      a.addEventListener("mouseenter", function () { showWork(a); });
    });
  }
  document.querySelectorAll("video").forEach(function (v) {
    v.muted = true;
    v.removeAttribute("autoplay");
    if (reduce) v.controls = true;
  });
  if (reduce || !("IntersectionObserver" in window)) return;
  var vio = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var v = entry.target;
      if (entry.isIntersecting && entry.intersectionRatio >= 0.25) {
        var pending = v.play();
        if (pending && pending.catch) pending.catch(function () {});
      } else {
        v.pause();
      }
    });
  }, { threshold: [0, 0.25, 0.6] });
  document.querySelectorAll("video").forEach(function (v) { vio.observe(v); });
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
<meta name="theme-color" content="#ff7a1f">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(canonical)}">
<link rel="alternate" hreflang="x-default" href="{esc(canonical)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="/assets/css/site.css">
<script>document.documentElement.classList.add("js")</script>
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


def footer():
    items = [
        ("Trials", "/#trials"),
        ("Record", "/#record"),
        ("Work", "/#work"),
        ("Practice", "/#practice"),
        ("Write", "/#write"),
    ]
    menu = "\n".join(
        f'<li><a href="{esc(href)}" data-rise style="--d:{i * 50}ms">{esc(label)}</a></li>'
        for i, (label, href) in enumerate(items)
    )
    return f"""<footer class="foot">
<div class="foot-photo">
<img src="/assets/frames/strawberry-close.jpg" alt="A closer view of flower thinning at the CES 2025 booth.">
</div>
<div class="foot-menu">
<a class="wordmark" href="/">Jaewoo Choi</a>
<ul class="menu">
{menu}
</ul>
<div class="foot-meta">
<p><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></p>
<p>
<a href="{esc(GITHUB)}" rel="me">GitHub</a>
<a href="{esc(KAGGLE)}" rel="me">Kaggle</a>
<a href="{esc(LINKEDIN)}" rel="me">LinkedIn</a>
</p>
</div>
<p class="legal">© Jaewoo Choi</p>
</div>
</footer>"""


def marquee():
    bits = []
    for name in MARQUEE:
        bits.append(f"<span>{esc(name)}</span>")
        bits.append('<span class="dot" aria-hidden="true"></span>')
    seq = "".join(bits)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{seq}{seq}</div></div>'


def home_page():
    imgs = "\n".join(
        f'<img src="{esc(src)}" alt="" data-for="{esc(key)}" width="1280" height="720"'
        + (' class="is-on"' if key == "strawberry" else "")
        + ">"
        for key, src in FRAMES.items()
    )
    names = []
    for i, (slug, name, img, left, right, fig) in enumerate(WORK):
        names.append(
            f'<li><a href="{esc(project_href("en", slug))}" data-img="{esc(img)}" '
            f'data-left="{esc(left)}" data-right="{esc(right)}" data-fig="{esc(fig)}" '
            f'data-rise style="--d:{i * 40}ms">{esc(name)}</a></li>'
        )
    body = f"""<main id="content">
<section class="hero">
<img class="hero-photo" src="/assets/frames/cad-room.jpg" alt="UR arm with a gripper and wrist camera, assembling a part on a fixture.">
<div class="card">
<h1><span>Robot</span><span>vision</span><span>trials</span></h1>
<div class="card-facts" data-rise style="--d:40ms">
<p>Daedong AILab</p>
<p>Senior AI Researcher</p>
<p>Since May 2024</p>
</div>
<p class="card-lead" data-rise style="--d:90ms">Jaewoo Choi builds perception for robots that leave the lab.</p>
<div class="card-foot" data-rise style="--d:140ms">
<p class="credit">UR arm, gripper, and wrist camera, on a fixture.</p>
<a class="btn" href="#trials">Watch a trial</a>
<a class="textlink" href="#write">Write</a>
</div>
</div>
</section>
<section class="stage" id="trials">
<div class="markers" aria-hidden="true">
<div data-stage="1"></div>
<div data-stage="2"></div>
<div data-stage="3"></div>
</div>
<div class="stage-sticky">
<h2 class="half-a"><span class="s1">Three tasks</span><span class="s2">Fixed lab</span><span class="s3">CES 2025</span></h2>
<div class="frame">
<video width="540" height="960" muted loop playsinline preload="none" poster="/assets/video/strawberry-ces2025.jpg" aria-label="Silent. Flower thinning at the CES 2025 booth">
<source src="/assets/video/strawberry-ces2025.mp4" type="video/mp4">
</video>
</div>
<p class="half-b"><span class="s2">A thousand trials</span><span class="s3">Flower thinning</span></p>
<p class="stage-cap">Flower thinning at the CES 2025 booth. Transplanting 93.8%, flower thinning 87.5%, runner handling 65%, across 1,000 fixed-lab trials.</p>
</div>
</section>
<section class="proof" id="record">
<h2 data-rise style="--d:40ms">The measured record</h2>
{marquee()}
<p class="proof-line" data-rise style="--d:80ms">These names are the strawberry tasks, the assembly and picking trials, Korean Patent 10-2694987, and three Kaggle medals.</p>
</section>
<section class="work" id="work">
<div class="work-stage">
<p class="fact fact-l">Imitation learning</p>
<div class="square">
{imgs}
<p class="square-figure"></p>
</div>
<p class="fact fact-r">93.8%</p>
</div>
<h2 data-rise style="--d:40ms">The work</h2>
<ul class="names">
{"".join(names)}
</ul>
</section>
<section class="about" id="practice">
<h2 data-rise style="--d:40ms">Practice</h2>
<div class="about-row">
<dl class="facts">
<div><dt>Role</dt><dd>Senior AI Researcher, Daedong AILab</dd></div>
<div><dt>Since</dt><dd>May 2024</dd></div>
<div><dt>School</dt><dd>Seokyeong University, Seoul</dd></div>
</dl>
<div class="about-copy" data-rise style="--d:80ms">
<p>Open-vocabulary RGB-D segmentation, point-cloud and image fusion for obstacle mapping, 6D pose estimation, and imitation learning for manipulation. Tested on deployed orchard robots and on manipulation robots.</p>
<p>Bachelor of Engineering, Industrial Management Systems Engineering, at Seokyeong University, Seoul, Mar 2016 to Aug 2022. Multidisciplinary major: Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies).</p>
<p>Co-inventor of Korean Patent 10-2694987, registered Aug 2024. Applicant PLAIF. The basis is the CAD-free assembly work. The registered title is: {esc(PATENT_TITLE)}</p>
</div>
</div>
<div class="record" data-rise style="--d:120ms">
<h3>Roles</h3>
<ul>
<li><span>Daedong AILab, Senior AI Researcher</span><span class="when">May 2024 to present</span></li>
<li><span>PLAIF, Computer Vision Engineer</span><span class="when">Jan 2023 to Apr 2024</span></li>
<li><span>FS Solution Co., Ltd., Computer Vision Engineer</span><span class="when">May 2022 to Dec 2022</span></li>
</ul>
<div>
<h3>Medals</h3>
<ul>
<li><span>UBC-OCEAN, bronze, team rank 83/1,326</span><span class="when">Jan 2024</span></li>
<li><span><a href="{esc(MATCH)}">Image Matching Challenge 2022, silver, 50/642</a></span><span class="when">Jun 2022</span></li>
<li><span><a href="{esc(WHALE)}">Happywhale, bronze, 127/1,588</a></span><span class="when">Apr 2022</span></li>
</ul>
<p>Happywhale is the Whale and Dolphin Identification competition.</p>
</div>
</div>
</section>
<section class="write" id="write">
<h2 data-rise style="--d:40ms">Write about a robot or a role.</h2>
<a class="email" href="mailto:{esc(EMAIL)}"><span>iam.jaewoochoi@</span><span>gmail.com</span></a>
<div class="write-foot">
<p>Seoul, South Korea</p>
<p>
<a href="{esc(GITHUB)}" rel="me">GitHub</a>
<a href="{esc(KAGGLE)}" rel="me">Kaggle</a>
<a href="{esc(LINKEDIN)}" rel="me">LinkedIn</a>
</p>
</div>
</section>
</main>"""
    title = "Jaewoo Choi, robot vision trials"
    desc = "Jaewoo Choi builds perception for robots that leave the lab."
    return document(title, desc, "/", body)


def bar():
    return """<header class="bar">
<a class="wordmark" href="/">Jaewoo Choi</a>
<nav aria-label="Sections">
<a href="/#work">Work</a>
<a href="/#write">Write</a>
</nav>
</header>"""


def stills():
    items = []
    for slug, label, src, alt in STILLS:
        items.append(
            f'<li><a href="{esc(project_href("en", slug))}">'
            f'<img src="{esc(src)}" alt="{esc(alt)}" width="1280" height="720">'
            f"<span>{esc(label)}</span></a></li>"
        )
    return f"""<section class="stills">
<h2>Filmed trials</h2>
<ul class="still-row">
{"".join(items)}
</ul>
</section>"""


def figures(slug):
    rows = FIGURES.get(slug) or []
    if not rows:
        return ""
    items = "\n".join(
        f"<li data-rise style=\"--d:{i * 40}ms\"><strong>{esc(value)}</strong><span>{esc(label)}</span></li>"
        for i, (value, label) in enumerate(rows)
    )
    return f'<ul class="figures">\n{items}\n</ul>'


def project_page(project):
    slug = project["slug"]
    info = DISPLAY[slug]
    group = next(g for g in GROUPS if g["id"] == project["group"])
    title = HEADS[slug]
    lead = LEADS[slug]
    blocks = []
    for i, (heading, html) in enumerate(project["sections"]["en"]):
        blocks.append(
            f'<section class="block" data-rise style="--d:{i * 40}ms">'
            f"<h2>{esc(heading)}</h2><div class=\"prose\">{html}</div></section>"
        )
    if slug == "cad-free-assembly":
        blocks.append(
            '<section class="block"><h2>Patent</h2><div class="prose"><p>'
            f"Korean Patent {esc('10-2694987')}, registered Aug 2024. Applicant PLAIF. Co-inventor. "
            f"The registered title is: {esc(PATENT_TITLE)}</p></div></section>"
        )
    media = ""
    action = f'<a class="btn" href="mailto:{esc(EMAIL)}">Write about this</a>'
    if project["video"]:
        v = VIDEOS[project["video"]]
        src = f"/assets/video/{v['file']}.mp4"
        poster = f"/assets/video/{v['file']}.jpg"
        media = f"""<div class="project-media">
<video width="{v['w']}" height="{v['h']}" muted loop playsinline preload="none" poster="{esc(poster)}" aria-label="{esc(v['label']['en'])}">
<source src="{esc(src)}" type="video/mp4">
<a href="{esc(src)}">Watch the film</a>
</video>
</div>"""
        action = f'<a class="btn" href="{esc(src)}">Watch the film</a>'
    idx = next(i for i, p in enumerate(PROJECTS) if p["slug"] == slug)
    prev_link = ""
    next_link = ""
    if idx > 0:
        prev = PROJECTS[idx - 1]
        prev_link = f'<a href="{esc(project_href("en", prev["slug"]))}">{esc(HEADS[prev["slug"]])}</a>'
    if idx + 1 < len(PROJECTS):
        nxt = PROJECTS[idx + 1]
        next_link = f'<a href="{esc(project_href("en", nxt["slug"]))}">{esc(HEADS[nxt["slug"]])}</a>'
    body = f"""{bar()}
<main id="content">
<article class="project">
<h1>{esc(title)}</h1>
<p class="lead" data-rise style="--d:40ms">{esc(lead)}</p>
<p class="meta" data-rise style="--d:70ms">{esc(group['org'])}. {esc(group['role']['en'])}. {esc(group['when']['en'])}.</p>
<p data-rise style="--d:100ms">{action}</p>
{media}
{figures(slug)}
{"".join(blocks)}
{stills()}
<nav class="pager" aria-label="Adjacent projects">
{prev_link}
{next_link}
</nav>
</article>
</main>"""
    desc = info["blurb"]
    path = project_href("en", slug)
    return document(f"{title}, Jaewoo Choi", desc, path, body)


def not_found_page():
    body = f"""{bar()}
<main id="content" class="missing">
<h1>Not found</h1>
<p>This address is not on the site.</p>
<a class="btn" href="/">Back to the trials</a>
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
    # The constant is referenced so a future publish flag stays visible here.
    _ = SITE
