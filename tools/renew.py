#!/usr/bin/env python3
"""Write the faculty-skim site. Facts come from build_site."""

import shutil

from build_site import (
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
    WHALE,
    FACTS,
    esc,
    harden_html,
    project_href,
)

import ko_copy as KO

LANGS = ("en", "ko")

UI = {
    "en": {
        "skip": "Skip to content",
        "work": "Work",
        "record": "Patent and awards",
        "experience": "Experience",
        "education": "Education",
        "details": "details",
        "problem": "Problem",
        "role": "My role",
        "method": "Method",
        "result": "Result",
        "prev": "Previous",
        "next": "Next",
        "all": "All work",
        "pager": "Adjacent projects",
        "code": "Code",
        "missing": "Page not found",
        "missing_body": "This address is not on the site.",
        "home_desc": "Perception engineer building segmentation, point-cloud perception, pose estimation, and manipulation learning for orchard robots and robot arms.",
    },
    "ko": KO.UI,
}

# Short titles and the five sections. Numbers and claims are the CV figures.
# The strawberry ownership sentence is stated once, under My role.
PAGES = {
    "language-distilled-segmentation": {
        "title": "Open-vocabulary segmentation and mapping",
        "result": "I built two generations of open-vocabulary perception, a class-name segmenter and then a caption-trained detector, and trained both on labels from my auto-labeling pipeline. Both output boxes and instance masks for the obstacle-mapping step I wrote, and both run on production RT100 robots with TensorRT on Jetson Orin Nano.",
        "desc": "Two generations of open-vocabulary perception for the RT100 orchard platform, a class-name open-vocabulary segmenter for semantic and instance segmentation and a caption-trained open-vocabulary detector, and the occupancy grid built from their instance masks. Both generations are deployed on production RT100 with TensorRT on Jetson Orin Nano.",
        "video": None,
        "thumb": {
            "src": "/assets/figures/open-vocab-v2.png",
            "w": 2000,
            "h": 1230,
            "alt": "Diagram of the second-generation caption-trained open-vocabulary detector.",
        },
        "problem": "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set, and those masks have to become a navigable map on a Jetson Orin Nano.",
        "role": "I pre-trained the first generation, a class-name open-vocabulary segmenter for semantic and instance segmentation, on frozen DINOv3 and SigLIP2 encoders, then developed the second, a caption-trained open-vocabulary detector with a mask head. On RT100, I deployed both generations and built the occupancy-grid mapping from their instance masks.",
        "method": [
            (
                "First generation: class-name segmenter",
                "With the DINOv3 and SigLIP2 encoders frozen, I pre-trained the image adapter, PAN-FPN neck, text adapter, and instance and semantic heads on multiple datasets. The two heads were trained together on alternating batches. A region-text alignment loss supervised the instance head, which outputs boxes and instance masks, and the semantic head classified each pixel against the class-name text embeddings. I added text-prompt inference and fixed-vocabulary conversion, and adapted the model to the orchard domain.",
            ),
            (
                "Why a second generation",
                "The first generation learned only from class names, and its SigLIP2 text encoder stayed frozen. On a validation subset it missed thin structures such as streetlights and small objects such as books, and it confused similar classes. Its semantic head picks the best class from a fixed list and cannot reject an unknown object, so on RT100 images some white reflectors were labeled as snow. I built the second generation, a caption-trained open-vocabulary detector, to learn from richer text than class names. Its compact text encoder is trained with object and image captions, which are used only during training and add no inference cost. The occupancy grid needs instance masks, so the detector has a mask head and outputs them along with boxes.",
            ),
            (
                "Second generation: caption-trained detector",
                "The second generation uses a query-based transformer architecture. Its frozen DINOv3 backbone feeds a multi-scale projector and a three-layer decoder. A trainable compact text encoder embeds category names. At inference it takes any list of category names, and those embeddings select the decoder queries and score each class. The mask head reads the highest-resolution features together with the decoder queries, and masks are returned at the original image resolution. Training uses category names, object captions, and image captions. During training only, a precomputed language teacher aligns the captions with matched queries and pooled image features and reweights related negatives. Masks are matched and trained with BCE/Dice losses.",
            ),
            (
                "Mapping masks into the occupancy grid",
                "The same mapping step serves both generations. The point cloud is reduced to voxels, and each voxel center is projected into the camera image. A voxel that lands inside an instance mask takes that mask's object and class. I added virtual voxels from valid anchor depths. The labeled voxels are then written into a navigable occupancy grid. Decay lets cells that are no longer observed fade out, hysteresis keeps a cell from flipping between free and occupied, and cost inflation keeps planned paths clear of obstacle edges. Navigation reads this grid.",
            ),
        ],
        "outcome": "Both generations run in the production RT100 perception pipeline on Jetson Orin Nano, optimized with TensorRT and trained on labels from my auto-labeling system. Both output boxes and instance masks, and the first generation also gives semantic masks. The second generation exports to ONNX and TensorRT with parity checks against PyTorch and ONNX Runtime. Small objects and rejecting objects that match none of the given category names are still open problems after the second generation.",
    },
    "auto-labeling": {
        "title": "Prompt-guided image and video auto-labeling",
        "nav_title": "Auto-labeling pipeline",
        "result": "The deployed labeling pipeline turns clicks into image masks and tracks them across video frames. Per-image labeling cost fell from USD 1.05 to USD 0.036 (96.6%) compared with Prolific. Its labels trained both generations of my open-vocabulary model.",
        "desc": "A deployed, prompt-guided auto-labeling pipeline for images and video. Labeling cost per image fell from USD 1.05 to USD 0.036 (96.6%) compared with Prolific.",
        "video": "auto",
        "problem": "Before this pipeline, segmentation data and region-grounded vision-language data were labeled by hand.",
        "role": "I built image and video annotation on an existing prompt-guided video segmentation model: an image-only decoder graph, a click-refinement flow, selective memory writes, and one shared encoder for both paths. Beyond the annotation tool, I also set the label taxonomy, wrote the annotation guidelines, and built the COCO-format training datasets.",
        "method": [
            "Clicks and mask corrections become tracked masks that keep the same ID across frames.",
            "Open-weight vision-language models wrote the region-grounded object captions and checked them. I sent uncertain cases to a second review and linked the verified captions to the instance annotations.",
        ],
        "outcome": "Labeling one image cost USD 1.05 with crowdsourced labeling on Prolific and USD 0.036 with this pipeline, a 96.6% reduction. The pipeline is deployed at Daedong AILab, where it has produced 13.0M instance-mask labels for 1.1M training records (662K images). These labels trained both generations of the open-vocabulary model.",
        "stack": "TensorRT, open-weight vision-language models, and COCO.",
    },
    "strawberry-cultivation": {
        "title": "Strawberry cultivation tasks",
        "result": "Transplanting 93.8%, flower thinning 87.5%, and runner handling 65% over 1,000 work cycles in a fixed lab environment. Exhibited at CES 2025.",
        "desc": "Diffusion Policy controllers for transplanting, flower thinning, and runner handling, trained on UMI demonstrations. Task-level success rates measured over 1,000 work cycles in a fixed lab environment were 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The work was exhibited at CES 2025.",
        "video": "strawberry",
        "problem": "A strawberry cultivation robot has to transplant seedlings, thin flowers, and handle runners. Each task policy is learned from human demonstrations collected with a Universal Manipulation Interface (UMI).",
        "role": "I led the data pipeline and the policy training for all three tasks, and built everything except the robot-side post-processing.",
        "method": [
        ],
        "outcome": "The three task policies run on the cultivation robot. Task-level success rates measured over 1,000 work cycles in a fixed lab environment were 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The work was exhibited at CES 2025.",
        "stack": "UMI, GoPro, IMU, ORB-SLAM3, Diffusion Policy, U-Net, and ViT.",
    },
    "cad-free-assembly": {
        "title": "CAD-free assembly",
        "result": "93% task success across 1,000 in-house trials, with no CAD model of the part. Completed five rounds.",
        "desc": "6D tool-pose estimation for robot assembly from a 2D camera, with no CAD model of the part. Task success was 93% across 1,000 in-house trials, and the work completed five rounds.",
        "video": "cad",
        "problem": "The robot has to assemble a part that has no CAD model, using only a 2D camera at run time, so it needs the target 6D tool pose from that image.",
        "role": "I built the pose pipeline, from image matching to the target 6D tool pose.",
        "method": [
            "The pipeline matches the live 2D image to a stored reference RGB-D capture with LightGlue, so each match carries depth.",
            "From the 3D-2D matches, solvePnP with RANSAC recovers the camera pose, which I chain with the eye-to-hand calibration and the stored reference pose to get the target 6D tool pose.",
        ],
        "outcome": "The pipeline completed five rounds. 93% of 1,000 in-house trials succeeded. This work is the basis of Korean Patent 10-2694987, on which I am a co-inventor.",
        "stack": "LightGlue, solvePnP with RANSAC, and eye-to-hand calibration.",
    },
    "bin-picking": {
        "title": "CAD-based bin picking",
        "result": "89% task success across 1,000 in-house, fixed-environment trials on five object types. Completed three rounds.",
        "desc": "RGB-D bin picking for objects with known CAD geometry. Task success was 89% in 1,000 in-house, fixed-environment trials on five object types, and the work completed three rounds.",
        "video": "bin",
        "problem": "The robot has to pick objects with known CAD geometry out of a bin, so it needs a pick pose for each object from an RGB-D image of the bin.",
        "role": "I trained the instance segmentation model and built the step that aligns visible-surface CAD templates to the segmented points.",
        "method": [
            "The instance segmentation model was trained with separate unoccluded and hole classes. Hole masks were subtracted from object masks, and the remaining instance masks segmented the point cloud.",
            "For each pick pose, I built a visible-surface CAD template by hidden-point removal and aligned it to the segmented points with PCA initialization and point-to-point ICP.",
            "Poses with low registration fitness or high inlier RMSE were dropped. The rest were ranked and transformed into the robot base frame with the camera extrinsics.",
        ],
        "outcome": "The system completed three rounds. In 1,000 in-house, fixed-environment trials, the robot moved five object types into an empty container with 89% task success.",
        "stack": "An instance segmentation model, PCA, and point-to-point ICP.",
    },
    "ros-6d-vision": {
        "title": "6D pose estimation with eye-to-hand calibration",
        "result": "Wrote the ROS action server, which returns object poses in the camera and robot-base frames on each request, and the eye-to-hand calibration tools, which report residual error.",
        "desc": "A deployed ROS action server runs capture, segmentation, and pose estimation on each request and returns poses with matching scores. The eye-to-hand calibration tools report residual error.",
        "video": None,
        "problem": "A caller needs each object pose in the robot base frame, so the camera has to be calibrated to the robot.",
        "role": "I wrote the ROS action server and the eye-to-hand calibration tools.",
        "method": [],
        "outcome": "Each request returns the pose in the camera frame and in the robot base, with a matching score. The server and the calibration tools are deployed and in use.",
        "stack": "ROS, Zivid, RealSense, ArUco, OpenCV, and dynamic_reconfigure.",
    },
    "license-plate": {
        "title": "License plate recognition",
        "result": "Built the plate recognition pipeline: plate detection, then OCR.",
        "desc": "Object detection locates a car license plate, and OCR reads the letters and digits.",
        "video": None,
        "problem": "To read a license plate, the system first has to find the plate in the image.",
        "role": "I built the deployed recognition pipeline.",
        "method": [
            "A detection model finds the plate.",
            "OCR reads the letters and digits.",
        ],
        "outcome": "The recognition pipeline is deployed and in use.",
        "stack": "Object detection and OCR.",
    },
}

CLIPS = {
    "auto": {
        "home": "/assets/video/home/auto-labeling.mp4",
        "full": "/assets/video/auto-labeling.mp4",
        "poster": "/assets/frames/auto-labeling-canvas.jpg",
        "home_w": 720,
        "home_h": 404,
        "full_w": 1280,
        "full_h": 678,
        "orient": "landscape",
        "label": "Orchard video in the labeling tool, with masks carried to the next frames.",
    },
    "strawberry": {
        "home": "/assets/video/home/strawberry.mp4",
        "full": "/assets/video/strawberry-ces2025.mp4",
        "poster": "/assets/frames/strawberry-booth.jpg",
        "home_w": 720,
        "home_h": 404,
        "full_w": 540,
        "full_h": 960,
        "orient": "portrait",
        "label": "Strawberry cultivation at the CES 2025 booth.",
    },
    "cad": {
        "home": "/assets/video/home/assembly.mp4",
        "full": "/assets/video/cad-free-assembly.mp4",
        "poster": "/assets/frames/cad-room.jpg",
        "home_w": 720,
        "home_h": 404,
        "full_w": 1280,
        "full_h": 720,
        "orient": "landscape",
        "label": "Robot arm with a gripper and wrist camera, assembling a part on a fixture.",
    },
    "bin": {
        "home": "/assets/video/home/bin-picking.mp4",
        "full": "/assets/video/bin-picking.mp4",
        "poster": "/assets/frames/bin-arm.jpg",
        "home_w": 720,
        "home_h": 404,
        "full_w": 1280,
        "full_h": 720,
        "orient": "landscape",
        "label": "A cobot arm during CAD-based bin picking.",
    },
}

WHEN = {
    "daedong": "May 2024–Present",
    "plaif": "Jan. 2023–Apr. 2024",
    "fs": "May 2022–Dec. 2022",
}

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
</script>
"""


def group_of(project):
    return next(g for g in GROUPS if g["id"] == project["group"])


def employment(project, lang="en"):
    group = group_of(project)
    when = WHEN[project["group"]] if lang == "en" else KO.WHEN[project["group"]]
    return f"{group['org']}, {group['role']['en']}, {when}."


def lang_path(path, lang):
    """English path to the same page in lang. '/' and '/projects/x.html' style."""
    if lang == "en":
        return path
    return "/ko" + path


# Runs before paint on every page.
# - A stored choice (localStorage "lang", set by the KO/EN switch or by the
#   first visit) always wins, and nothing redirects.
# - First visit only (no stored value): if the visitor lands on the English
#   home page "/", the browser's first language starts with "ko", and the
#   referrer is empty or this site, go to /ko/ with location.replace.
#   Any other first visit, including a direct link to an English project
#   page or a link from another site, stays where it is.
# - The first visit stores the language it ends up on, so the rule runs once.
# No IP lookup.
LANG_SCRIPT = """<script>
(function () {
  var KEY = "lang";
  var page = document.documentElement.lang === "ko" ? "ko" : "en";
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { return; }
  if (stored === "en" || stored === "ko") return;
  var nav = ((navigator.languages && navigator.languages[0]) || navigator.language || "").toLowerCase();
  var ref = document.referrer;
  var local = !ref || ref.indexOf(location.origin + "/") === 0;
  var home = location.pathname === "/" || location.pathname === "/index.html";
  if (page === "en" && home && local && nav.slice(0, 2) === "ko") {
    try { localStorage.setItem(KEY, "ko"); } catch (e) {}
    location.replace("/ko/" + location.hash);
    return;
  }
  try { localStorage.setItem(KEY, page); } catch (e) {}
})();
</script>
"""

# Saves the choice when the KO/EN switch is clicked. The link still works without script.
SWITCH_SCRIPT = """<script>
document.querySelectorAll("a[data-lang]").forEach(function (a) {
  a.addEventListener("click", function () {
    try { localStorage.setItem("lang", a.getAttribute("data-lang")); } catch (e) {}
  });
});
</script>
"""


def head(title, desc, path, lang="en"):
    own = lang_path(path, lang)
    canon = SITE + own
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{esc(SITE + lang_path(path, target))}">\n'
        for code, target in (("en", "en"), ("ko", "ko"), ("x-default", "en"))
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Jaewoo Choi">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
{alternates}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/source-serif-4-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/source-serif-4-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
{LANG_SCRIPT}</head>
"""


def switch(path, lang):
    """KO/EN switch. path is the English path of the current page."""
    items = []
    for code, label, name in (("en", "EN", "English"), ("ko", "KO", "한국어")):
        cur = ' aria-current="true"' if code == lang else ""
        items.append(
            f'<a href="{esc(lang_path(path, code))}" hreflang="{code}" lang="{code}" '
            f'data-lang="{code}" title="{name}"{cur}>{label}</a>'
        )
    aria = "Language" if lang == "en" else "언어"
    return f'<span class="lang" role="group" aria-label="{aria}">{items[0]}<span aria-hidden="true">/</span>{items[1]}</span>'


def nav(home, lang="en", path="/"):
    t = UI[lang]
    prefix = "" if home else lang_path("/", lang)
    return f"""<a class="skip" href="#{'glance' if home else 'content'}">{t['skip']}</a>
<header class="bar wrap">
<a href="{prefix}#work">{t['work']}</a>
<a href="{prefix}#record">{t['record']}</a>
<a href="{prefix}#experience">{t['experience']}</a>
<a href="{prefix}#education">{t['education']}</a>
{switch(path, lang)}
</header>
"""


def clip_label(video, lang):
    return CLIPS[video]["label"] if lang == "en" else KO.CLIP_LABELS[video]


def slot(page, lang="en", slug=None):
    video = page["video"]
    if not video:
        thumb = page.get("thumb")
        if not thumb:
            return ""
        alt = thumb["alt"] if lang == "en" else KO.PAGES[slug]["thumb_alt"]
        return (
            '<div class="slot slot-fig">'
            f'<img src="{thumb["src"]}" alt="{esc(alt)}" width="{thumb["w"]}" height="{thumb["h"]}" loading="lazy">'
            "</div>"
        )
    clip = CLIPS[video]
    label = esc(clip_label(video, lang))
    return (
        '<div class="slot">'
        f'<img src="{clip["poster"]}" alt="{label}" width="{clip["home_w"]}" height="{clip["home_h"]}">'
        f'<video width="{clip["home_w"]}" height="{clip["home_h"]}" muted loop playsinline autoplay preload="metadata" poster="{clip["poster"]}" aria-label="{label}">'
        f'<source src="{clip["home"]}" type="video/mp4">'
        "</video></div>"
    )


# Home intro, version A in out/r15_for_slop.md.
INTRO = (
    "I build perception for robots: image segmentation, point-cloud obstacle mapping, "
    "object pose estimation, and imitation learning for manipulation. My open-vocabulary models run on "
    "production orchard robots with Jetson Orin Nano. Their training labels come from my auto-labeling pipeline, "
    "which has produced 13.0M instance-mask labels at 96.6% lower cost per image than Prolific."
)

# Monochrome 24x24 paths. GitHub, Kaggle, and LinkedIn are Simple Icons (CC0); Email is an envelope.
ICONS = {
    "Email": "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z",
    "GitHub": "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12",
    "Kaggle": "M18.825 23.859c-.022.092-.117.141-.281.141h-3.139c-.187 0-.351-.082-.492-.248l-5.178-6.589-1.448 1.374v5.111c0 .235-.117.352-.351.352H5.505c-.236 0-.354-.117-.354-.352V.353c0-.233.118-.353.354-.353h2.431c.234 0 .351.12.351.353v14.343l6.203-6.272c.165-.165.33-.246.495-.246h3.239c.144 0 .236.06.285.18.046.149.034.255-.036.315l-6.555 6.344 6.836 8.507c.095.104.117.208.07.358",
    "LinkedIn": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
}


def contact_icons():
    links = [
        ("Email", f"mailto:{EMAIL}", ""),
        ("GitHub", GITHUB, ' rel="me"'),
        ("Kaggle", KAGGLE, ' rel="me"'),
        ("LinkedIn", LINKEDIN, ' rel="me"'),
    ]
    return "".join(
        f'<a href="{esc(href)}"{rel} aria-label="{name}" title="{name}">'
        f'<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true" focusable="false">'
        f'<path d="{ICONS[name]}"/></svg></a>'
        for name, href, rel in links
    )


def below_en():
    return f"""<section id="record">
<h2>Patent and awards</h2>
<ul>
<li>Korean Patent 10-2694987, registered Aug. 2024. Applicant PLAIF. Co-inventor. {esc(PATENT_TITLE)} My <a href="{project_href("en", "cad-free-assembly")}">CAD-free assembly</a> work is the basis of the patent.</li>
<li>Kaggle UBC-OCEAN: bronze medal, team rank 83/1,326, Jan. 2024.</li>
<li>Kaggle Image Matching Challenge 2022: silver medal, team rank 50/642, June 2022. <a href="{esc(MATCH)}">Code</a>.</li>
<li>Kaggle Happywhale (Whale and Dolphin Identification): bronze medal, team rank 127/1,588, Apr. 2022. <a href="{esc(WHALE)}">Code</a>.</li>
</ul>
</section>
<section id="experience">
<h2>Experience</h2>
<ul>
<li>Daedong AILab, Senior AI Researcher, May 2024–Present.</li>
<li>PLAIF, Computer Vision Engineer, Jan. 2023–Apr. 2024.</li>
<li>FS Solution Co., Ltd., Computer Vision Engineer, May 2022–Dec. 2022.</li>
</ul>
</section>
<section id="education">
<h2>Education</h2>
<ul>
<li>Bachelor of Engineering, Industrial Management Systems Engineering, Seokyeong University, Seoul, Mar. 2016–Aug. 2022. GPA {FACTS['gpa']}. Multidisciplinary major: Big Data.</li>
</ul>
</section>"""


def below_ko():
    t = UI["ko"]
    link = f'<a href="{project_href("ko", "cad-free-assembly")}">CAD-free assembly</a>'
    record = [
        esc(KO.RECORD[0]).format(title=esc(PATENT_TITLE), link=link),
        esc(KO.RECORD[1]),
        esc(KO.RECORD[2]).format(code=f'<a href="{esc(MATCH)}">{t["code"]}</a>.'),
        esc(KO.RECORD[3]).format(code=f'<a href="{esc(WHALE)}">{t["code"]}</a>.'),
    ]
    items = lambda rows: "\n".join(f"<li>{row}</li>" for row in rows)
    return f"""<section id="record">
<h2>{t['record']}</h2>
<ul>
{items(record)}
</ul>
</section>
<section id="experience">
<h2>{t['experience']}</h2>
<ul>
{items(esc(x) for x in KO.EXPERIENCE)}
</ul>
</section>
<section id="education">
<h2>{t['education']}</h2>
<ul>
{items(esc(x) for x in KO.EDUCATION)}
</ul>
</section>"""


def tie(text, lang):
    """Korean headings: keep the last two words together so no line holds one word."""
    if lang != "ko" or " " not in text:
        return text
    head, last = text.rsplit(" ", 1)
    return head + "\u00a0" + last


def page_copy(slug, lang):
    return PAGES[slug] if lang == "en" else KO.PAGES[slug]


def home_page(lang="en"):
    t = UI[lang]
    rows = []
    for project in PROJECTS:
        page = PAGES[project["slug"]]
        copy = page_copy(project["slug"], lang)
        href = project_href(lang, project["slug"])
        kind = "proj" if page["video"] or page.get("thumb") else "proj proj-plain"
        rows.append(
            f'<article class="{kind}" id="{esc(project["slug"])}">'
            f"{slot(page, lang, project['slug'])}"
            '<div class="proj-copy">'
            f'<h2><a href="{href}">{esc(copy["title"])}</a></h2>'
            f'<p>{esc(copy["result"])} <a href="{href}">{t["details"]}</a></p>'
            "</div></article>"
        )
    intro = INTRO if lang == "en" else KO.INTRO
    below = below_en() if lang == "en" else below_ko()
    body = f"""{head("Jaewoo Choi", t["home_desc"], "/", lang)}
<body>
{nav(True, lang, "/")}
<main class="wrap glance" id="glance">
<div class="who">
<h1>Jaewoo Choi</h1>
<p class="role">Perception Engineer</p>
<p class="interest">{esc(intro)}</p>
<p class="contacts">{contact_icons()}</p>
</div>
<div class="work" id="work">
{''.join(rows)}
</div>
<div class="below">
{below}
</div>
</main>
{SCRIPT}{SWITCH_SCRIPT}</body>
</html>
"""
    return harden_html(body)


def film(page, lang="en"):
    video = page["video"]
    if not video:
        return ""
    clip = CLIPS[video]
    label = esc(clip_label(video, lang))
    return (
        f'<figure class="film {clip["orient"]}">'
        f'<video width="{clip["full_w"]}" height="{clip["full_h"]}" muted playsinline controls preload="metadata" poster="{clip["poster"]}" aria-label="{label}">'
        f'<source src="{clip["full"]}" type="video/mp4">'
        "</video>"
        f"<figcaption>{label}</figcaption>"
        "</figure>"
    )


def pager(project, lang="en"):
    t = UI[lang]
    idx = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    prev = '<span></span>'
    nxt = '<span></span>'

    def label(slug):
        copy = page_copy(slug, lang)
        return esc(copy.get("nav_title", copy["title"]))

    if idx > 0:
        item = PROJECTS[idx - 1]
        prev = (
            f'<a href="{project_href(lang, item["slug"])}">'
            f'<span class="dir quiet">{t["prev"]}</span>'
            f'{label(item["slug"])}</a>'
        )
    if idx + 1 < len(PROJECTS):
        item = PROJECTS[idx + 1]
        nxt = (
            f'<a href="{project_href(lang, item["slug"])}">'
            f'<span class="dir quiet">{t["next"]}</span>'
            f'{label(item["slug"])}</a>'
        )
    return (
        f'<nav class="pager" aria-label="{t["pager"]}">'
        f"{prev}"
        f'<a href="{lang_path("/", lang)}#work">{t["all"]}</a>'
        f"{nxt}"
        "</nav>"
    )


DIAGRAMS = {
    "language-distilled-segmentation": """<figure class="flow">
<p class="flow-k">System flow on RT100</p>
<div class="flow-step">
<p class="flow-k">Inputs</p>
<p>RGB image, and a point cloud of the same scene.</p>
</div>
<div class="flow-step">
<p class="flow-k">Open-vocabulary segmentation</p>
<p>Category names are given as text, so the class list can change without retraining.</p>
</div>
<div class="flow-fork">
<div>
<p class="flow-k">First generation: class-name segmenter</p>
<p>Frozen DINOv3 and SigLIP2 encoders. Trained image and text adapters, PAN-FPN neck, instance and semantic heads.</p>
</div>
<div>
<p class="flow-k">Second generation: caption-trained detector</p>
<p>Frozen DINOv3 backbone, multi-scale projector, three-layer decoder, trainable compact text encoder, mask head. Object and image captions are used in training only.</p>
</div>
</div>
<div class="flow-step">
<p class="flow-k">Boxes and instance masks</p>
<p>Both generations. The first also outputs semantic masks.</p>
</div>
<div class="flow-step">
<p class="flow-k">Voxels to masks</p>
<p>Voxel centers projected into the image take the object and class of the mask they land in. Virtual voxels added from valid anchor depths.</p>
</div>
<div class="flow-step">
<p class="flow-k">Occupancy grid</p>
<p>Labeled voxels written into the grid with decay, hysteresis, and cost inflation.</p>
</div>
<div class="flow-step">
<p class="flow-k">Navigation</p>
<p>Reads the occupancy grid.</p>
</div>
<figcaption>I built the second generation after validation exposed errors in the first. Both feed the same mapping step.</figcaption>
</figure>
""",
    "strawberry-cultivation": """<figure class="flow">
<p class="flow-k">Whole system, per task</p>
<div class="flow-step">
<p class="flow-k">Demonstrations</p>
<p>A person performs the task with a hand-held UMI gripper. Its GoPro records RGB video and IMU data.</p>
</div>
<div class="flow-step">
<p class="flow-k">Calibration</p>
<p>The camera is calibrated to the IMU.</p>
</div>
<div class="flow-step">
<p class="flow-k">Trajectories</p>
<p>ORB-SLAM3 visual-inertial SLAM recovers the gripper trajectory from the video and IMU data.</p>
</div>
<div class="flow-step">
<p class="flow-k">Training sets</p>
<p>The trajectories and video frames are turned into training sets.</p>
</div>
<div class="flow-step">
<p class="flow-k">Policy</p>
<p>Diffusion Policy, conditioned on RGB features and robot state, outputs an action sequence.</p>
</div>
<div class="flow-step">
<p class="flow-k">Robot side</p>
<p>Robot-side post-processing passes the actions to robot control.</p>
</div>
<div class="flow-fork">
<div>
<p class="flow-k">Tasks</p>
<p>Transplanting, flower thinning, and runner handling.</p>
</div>
<div>
<p class="flow-k">Evaluation</p>
<p>1,000 work cycles in a fixed lab environment.</p>
</div>
</div>
<figcaption>The same pipeline runs once per task, and each task has its own policy.</figcaption>
</figure>
""",
    "ros-6d-vision": """<figure class="flow">
<p class="flow-k">Per request; camera, model, and pipeline set in a config file</p>
<div class="flow-step">
<p class="flow-k">Input</p>
<p>Zivid, RealSense, or recorded data</p>
</div>
<div class="flow-step">
<p class="flow-k">Capture</p>
</div>
<div class="flow-step">
<p class="flow-k">Segmentation</p>
</div>
<div class="flow-step">
<p class="flow-k">Pose estimation</p>
</div>
<div class="flow-step">
<p class="flow-k">Return</p>
<p>Robot-base and camera-frame poses, with matching scores</p>
</div>
<div class="flow-side">
<p class="flow-k">Eye-to-hand calibration</p>
<div class="flow-step">
<p>ArUco board poses</p>
</div>
<div class="flow-step">
<p>Batch AX = YB solve, OpenCV Park method</p>
</div>
<div class="flow-step">
<p>Camera-robot transform and residual error</p>
</div>
<div class="flow-step">
<p>Validation tool and dynamic_reconfigure tuning</p>
</div>
</div>
<figcaption>The action server runs the request chain. Calibration is a separate tool.</figcaption>
</figure>
""",
}


ARCH = {
    ("language-distilled-segmentation", "First generation: class-name segmenter"): {
        "src": "/assets/figures/open-vocab-v1.png",
        "w": 1920,
        "h": 930,
        "alt": "First generation, the class-name open-vocabulary segmenter: frozen DINOv3 image and SigLIP2 text encoders, with a trained image adapter, PAN-FPN neck, text adapter, and instance and semantic heads.",
        "caption": "First generation of the class-name segmenter.",
    },
    ("language-distilled-segmentation", "Second generation: caption-trained detector"): {
        "src": "/assets/figures/open-vocab-v2.png",
        "w": 2000,
        "h": 1230,
        "alt": "Diagram of the second generation, the caption-trained open-vocabulary detector. A frozen image encoder feeds a multi-scale projector and a three-layer decoder with 300 queries, which drive mask, box and class heads. Category names pass through a trainable text encoder to select queries and score classes. In a training-only branch, object and image captions pass through a frozen teacher text encoder and are aligned with matched queries and pooled image features.",
        "caption": "Second generation. Category names (teal) are used at inference. Object captions (magenta) and image captions (gold) are used only in training.",
    },
}


# Extra sections placed after Method. Raw HTML; harden_html adds the text hyphen handling.
EXTRA_SECTIONS = {
    "cad-free-assembly": """<section>
<h2>System diagram</h2>
<p>The reference RGB-D capture is taken once. At run time, the 2D camera image is cropped and converted to grayscale before matching.</p>
<figure class="arch"><img src="/assets/figures/cad-free-system.png" width="2040" height="760" alt="CAD-free assembly system. A reference RGB-D capture is taken once. At run time, the 2D camera image is cropped and converted to grayscale, LightGlue matches its keypoints to the reference RGB image, the reference depth turns the matches into 2D-3D matches, and solvePnP with RANSAC gives the camera pose. A transform chain with the eye-to-hand calibration and the stored reference tool pose gives the target 6D tool pose for robot motion."><figcaption>Dashed boxes mark steps described in the patent.</figcaption></figure>
</section>
""",
    "bin-picking": """<section>
<h2>System diagram</h2>
<p>Each request starts from one RGB-D frame with color, points, and normals. The masked points are downsampled and filtered by normal direction before PCA. Templates are built offline from the CAD mesh, and a reverse check scores each fit in both directions. The camera-to-base mapping uses the eye-to-hand calibration, and the kept poses return as a ROS action result. Robot motion is handled on the robot side.</p>
<figure class="arch"><img src="/assets/figures/bin-picking-system.png" width="1900" height="1090" alt="CAD-based bin picking system. An RGB-D frame goes to an instance segmentation model that segments objects and holes. Hole masks are removed, and for each object the masked points get an initial pose from PCA. Point-to-point ICP aligns a visible-surface template, built offline from the CAD mesh by hidden-point removal, and a fit check ranks the poses. The kept pose is mapped from the camera frame to the robot base with the eye-to-hand calibration and returned as a ROS action result for robot motion."><figcaption>Only the instance segmentation model is trained. Templates are built once per object, offline.</figcaption></figure>
</section>
""",
    "strawberry-cultivation": """<section>
<h2>Model structure</h2>
<p>The policy is Diffusion Policy. An image encoder turns the RGB frames into features. Those features and the robot state form the global conditioning. Starting from a noisy action sequence, the denoising network removes noise over repeated steps and returns an action sequence for the robot side.</p>
<figure class="arch"><img src="/assets/figures/strawberry-policy.png" width="2040" height="700" alt="Diffusion Policy for the strawberry tasks. RGB frames go through an image encoder to RGB features. RGB features and robot state form the global conditioning of a trained denoising network, which turns a noisy action sequence into an action sequence over repeated denoising steps. The action sequence goes to the robot side."></figure>
</section>
""",
    "auto-labeling": """<section>
<h2>Model structure</h2>
<p>The pipeline uses an existing prompt-guided video segmentation model. An image encoder and neck turn each frame into features, and a mask decoder turns point or mask prompts into mask logits. For video, a memory path stores each tracked mask and carries it to later frames.</p>
<figure class="arch"><img src="/assets/figures/auto-labeling-system.png" width="2040" height="1500" alt="Auto-labeling system. Top: an image encoder and neck feed point- and mask-prompt decoding, and memory attention with a memory bank carries tracked objects between frames. Mask logits go to a CPU service that writes COCO polygons and RLE masks. Bottom: the finished labels are captioned in three stages, an object caption per mask, a relation caption of each mask in the image, and an image caption. Captions are checked, with a second review for unsure cases, and linked to the instance annotations. Object and image captions feed training of the second-generation open-vocabulary detector. Relation captions are stored with the labels and not used in that training."><figcaption>The GPU service runs the model, and a CPU service turns its mask logits into COCO polygons and RLE masks.</figcaption></figure>
<p>The model runs on an existing open-source TensorRT export. That export split the model into separate graphs and made memory attention sparse. Those changes are its author's work. My changes do not change the model weights.</p>
</section>
<section>
<h2>Image labeling</h2>
<p>A still image has no past frames, so the memory encoder and object pointer are not used. I extracted a subgraph of the point-prompt decoder that keeps only the mask, object score and IoU outputs. Its operators and weights are the same as in the video graph. The encoder and neck run once per image. The first click goes to a first-click decoder. Each later click goes to a refine decoder together with all earlier clicks and the previous mask logits, which act as a mask prompt.</p>
</section>
<section>
<h2>Video labeling</h2>
<p>Existing labels on the first frame are resized to the model input, turned into mask logits and entered as conditioning frames. Region classes such as ground are first trimmed by the union of object masks, so tracking never starts from overlapping labels. Clicks go on top as point prompts, and a new object must start with a positive click. While an annotator is still clicking on a frame, intermediate masks are not written to memory; only the final mask is encoded and stored. A correction on a later frame is added the same way, as a new conditioning frame with the same track ID.</p>
</section>
<section>
<h2>Outputs</h2>
<p>Mask logits are filled at low resolution, upsampled and thresholded. Cleanup keeps objects and region classes from overlapping and gives small stray islands of a region class to their neighbors. It also removes overlapping duplicates of one object class. Pieces disconnected from every positive click are dropped. Objects are saved as COCO polygons and region classes as masks.</p>
</section>
<section>
<h2>Serving</h2>
<p>The image and video paths share one encoder and neck on the GPU. Image features stay cached on the GPU between clicks, and so does the previous mask. The point-prompt decoder is built in FP32 because the FP16 build failed the mask IoU check. GPU inference and CPU post-processing run as two separate services. None of these choices change the model.</p>
</section>
<section>
<h2>Captioning after labeling</h2>
<p>After auto-labeling finished, open-weight vision-language models captioned the labeled data in three stages:</p>
<ul>
<li>Each mask got a caption of the object it covers.</li>
<li>Each mask also got a caption of its relationship to the image.</li>
<li>The whole image got a caption of its own.</li>
</ul>
<p>The second generation of the <a href="/projects/language-distilled-segmentation.html">open-vocabulary model</a> trains on the object and image captions. It does not use the relationship captions, which are stored with the labels.</p>
</section>
""",
}


def arch_figure(slug, label, lang="en"):
    item = ARCH.get((slug, label))
    if not item:
        return ""
    words = item if lang == "en" else KO.ARCH[(slug, label)]
    return (
        '<figure class="arch">'
        f'<img src="{item["src"]}" width="{item["w"]}" height="{item["h"]}" alt="{esc(words["alt"])}">'
        f"<figcaption>{esc(words['caption'])}</figcaption>"
        "</figure>"
    )


def project_page(project, lang="en"):
    page = PAGES[project["slug"]]
    copy = page_copy(project["slug"], lang)
    t = UI[lang]
    method = copy["method"]
    if method and isinstance(method[0], tuple):
        blocks = []
        for i, (label, text) in enumerate(method):
            blocks.append(f"<h3>{esc(tie(label, lang))}</h3>\n<p>{esc(text)}</p>")
            figure = arch_figure(project["slug"], page["method"][i][0], lang)
            if figure:
                blocks.append(figure)
        steps = "\n".join(blocks)
    elif method:
        items = "\n".join(f"<li>{esc(step)}</li>" for step in method)
        steps = f"<ol>\n{items}\n</ol>"
    else:
        steps = ""
    title = f"{copy['title']}, Jaewoo Choi"
    path = project_href("en", project["slug"])
    extras = EXTRA_SECTIONS if lang == "en" else KO.EXTRA_SECTIONS
    extra = extras.get(project["slug"], "")
    if extra:
        extra = extra.strip() + "\n"
    result = ""
    if copy["outcome"]:
        result = f"""<section>
<h2>{t['result']}</h2>
<p>{esc(copy["outcome"])}</p>
</section>
"""
    diagrams = DIAGRAMS if lang == "en" else KO.DIAGRAMS
    diagram = diagrams.get(project["slug"], "")
    if diagram:
        diagram = diagram.strip() + "\n"
    body = f"""{head(title, copy["desc"], path, lang)}
<body class="page">
{nav(False, lang, path)}
<main id="content">
<h1>{esc(tie(copy["title"], lang))}</h1>
<p class="meta">{esc(employment(project, lang))}</p>
{film(page, lang)}
<section>
<h2>{t['problem']}</h2>
<p>{esc(copy["problem"])}</p>
</section>
<section>
<h2>{t['role']}</h2>
<p>{esc(copy["role"])}</p>
</section>
<section>
<h2>{t['method']}</h2>
{diagram}{steps}
</section>
{extra}{result}{pager(project, lang)}
</main>
{SCRIPT}{SWITCH_SCRIPT}</body>
</html>
"""
    return harden_html(body)


def not_found_page(lang="en"):
    t = UI[lang]
    body = f"""{head(t["missing"], t["missing_body"], "/404.html", lang)}
<body class="page">
{nav(False, lang, "/404.html")}
<main id="content" class="missing">
<h1>{t["missing"]}</h1>
<p>{t["missing_body"]}</p>
<p><a href="{lang_path("/", lang)}">{t["all"]}</a></p>
</main>
{SWITCH_SCRIPT}</body>
</html>
"""
    return harden_html(body)


def write_lang(lang):
    base = ROOT if lang == "en" else ROOT / "ko"
    base.mkdir(exist_ok=True)
    (base / "index.html").write_text(home_page(lang), encoding="utf-8")
    projects = base / "projects"
    projects.mkdir(exist_ok=True)
    keep = set()
    for project in PROJECTS:
        name = project["slug"] + ".html"
        keep.add(name)
        (projects / name).write_text(project_page(project, lang), encoding="utf-8")
    for path in projects.glob("*.html"):
        if path.name not in keep:
            path.unlink()
    (base / "404.html").write_text(not_found_page(lang), encoding="utf-8")


def write_all():
    ko = ROOT / "ko"
    if ko.exists():
        shutil.rmtree(ko)
    write_lang("en")
    if not PUBLISH_KO:
        return
    write_lang("ko")
    from check_parity import compare

    problems = compare()
    if problems:
        shutil.rmtree(ko)
        raise SystemExit("Korean numbers differ from English:\n" + "\n".join(problems))


if __name__ == "__main__":
    write_all()
