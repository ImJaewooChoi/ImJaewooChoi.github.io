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
    esc,
    harden_html,
    project_href,
)

# Short titles and the five sections. Numbers and claims are the CV figures.
# The strawberry ownership sentence is stated once, under My role.
PAGES = {
    "language-distilled-segmentation": {
        "title": "Open-vocabulary segmentation and mapping",
        "result": "Built two versions of an open-vocabulary segmenter and the obstacle-mapping step. Version 1 runs on production RT100 robots with TensorRT on Jetson Orin Nano.",
        "desc": "Two versions of an open-vocabulary segmenter for the RT100 orchard platform, and the occupancy grid built from the masks. Version 1 runs on production RT100 with TensorRT on Jetson Orin Nano.",
        "video": None,
        "problem": "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set, and those masks have to become a navigable map under embedded compute limits.",
        "role": "I pre-trained a DINOv3 and SigLIP2 segmenter (Version 1), implemented and trained a second open-vocabulary segmenter (Version 2), and built the occupancy-grid mapping from the instance masks.",
        "method": [
            (
                "Version 1",
                "With the DINOv3 and SigLIP2 encoders frozen, I pre-trained the image adapter, PAN-FPN neck, text adapter, and instance and semantic heads on multiple datasets. The two heads were trained together on alternating batches. A region-text alignment loss supervised the instance head, and the semantic head classified each pixel against the class-name text embeddings. I added text-prompt inference and fixed-vocabulary conversion, and adapted the model to the orchard domain.",
            ),
            (
                "Version 2",
                "Version 2 is a DETR-style instance segmentation model. Its frozen DINOv3 backbone feeds a multi-scale projector and a three-layer decoder. A trainable MiniLM text encoder embeds category names, and a query-based mask head predicts masks from the highest-resolution features. Training uses category names, mask captions, and image captions. During training only, a precomputed language teacher aligns the captions with matched queries and pooled image features and reweights related negatives. Masks are matched and trained with BCE/Dice losses.",
            ),
            (
                "Post-processing",
                "Point-cloud voxel centers were projected into the image and associated with the instance masks. I added virtual voxels from valid anchor depths, and obstacles were mapped into a navigable occupancy grid with decay, hysteresis, and cost inflation.",
            ),
        ],
        "outcome": "Version 1 is integrated into the production RT100 perception pipeline. I deployed it and optimized it with TensorRT on Jetson Orin Nano. For Version 2, the detection model exports to ONNX and TensorRT with parity checks against PyTorch and ONNX Runtime. Full-dataset training and accuracy evaluation of Version 2 are pending.",
    },
    "auto-labeling": {
        "title": "Prompt-guided image and video auto-labeling",
        "nav_title": "Auto-labeling pipeline",
        "result": "Shared visual features, prompt-guided mask correction, and temporal object memory support image previews and video label propagation. Per-image labeling cost fell from about USD 1.05 to about USD 0.036 (96.6%).",
        "desc": "Prompt-guided image and video auto-labeling with shared visual features, mask correction, and temporal object memory. Labeling cost fell by 96.6%, from about USD 1.05 to about USD 0.036 per image.",
        "video": "auto",
        "problem": "Segmentation data and region-grounded vision-language data were labeled by hand.",
        "role": "I adapted an existing segmentation model to the image and video annotation workflow, set the label taxonomy and annotation guidelines, and compiled the COCO-format training datasets.",
        "method": [
            "Point prompts and mask corrections were turned into tracked masks with consistent IDs across frames.",
            "Qwen-series vision-language models wrote the region-grounded object captions and checked them. I sent uncertain cases to a second review and linked the verified captions to the instance annotations.",
        ],
        "outcome": "Labeling one image cost about USD 1.05 before this pipeline and about USD 0.036 after it, a 96.6% reduction.",
        "stack": "TensorRT, Qwen-series vision-language models, and COCO.",
    },
    "strawberry-cultivation": {
        "title": "Strawberry cultivation tasks",
        "result": "Transplanting 93.8%, flower thinning 87.5%, and runner handling 65% across 1,000 work cycles in a fixed lab. Shown at CES 2025.",
        "desc": "I trained Diffusion Policy on UMI demonstrations for transplanting, flower thinning, and runner handling. In 1,000 work cycles in a fixed lab, success was 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The work was exhibited at CES 2025.",
        "video": "strawberry",
        "problem": "Transplanting, flower thinning, and runner handling are learned from human demonstrations collected with a Universal Manipulation Interface (UMI).",
        "role": "I led the data pipeline and the policy training for all three tasks, and built everything except the robot-side post-processing.",
        "method": [
            "GoPro RGB and IMU data were collected, and I calibrated the camera to the IMU.",
            "ORB-SLAM3 visual-inertial SLAM trajectories were turned into training sets.",
            "Diffusion Policy was trained with RGB features and robot state as global conditioning.",
        ],
        "outcome": "Across 1,000 work cycles in a fixed lab, transplanting succeeded 93.8% of the time, flower thinning 87.5%, and runner handling 65%. The work was exhibited at CES 2025.",
        "stack": "UMI, GoPro, IMU, ORB-SLAM3, Diffusion Policy, U-Net, and ViT.",
    },
    "cad-free-assembly": {
        "title": "CAD-free assembly",
        "result": "93% task success across 1,000 in-house trials, with no CAD model of the part.",
        "desc": "I estimated 6D tool poses for assembly from a 2D camera at run time, with no CAD model of the part. Task success was 93% across 1,000 in-house trials.",
        "video": "cad",
        "problem": "Assembly needs a target 6D tool pose when the part has no CAD model. At run time the sensor is a 2D camera.",
        "role": "I prototyped a two-view baseline and built the final pose pipeline.",
        "method": [
            "The final pipeline matches the live 2D image to a stored reference RGB-D capture with LightGlue, so each match carries depth.",
            "From the 3D-2D matches, solvePnP with RANSAC recovers the camera pose, which I chain with the hand-eye calibration and the stored reference pose to get the target 6D tool pose.",
        ],
        "outcome": "93% of 1,000 in-house trials succeeded. This work is the basis of Korean Patent 10-2694987.",
        "stack": "LightGlue, USAC, solvePnP, RANSAC, and hand-eye calibration.",
    },
    "bin-picking": {
        "title": "CAD-based bin picking",
        "result": "89% task success across 1,000 in-house trials on five object types.",
        "desc": "I estimated picking poses from RGB-D images for objects with known CAD geometry. Task success was 89% in 1,000 in-house, fixed-environment trials.",
        "video": "bin",
        "problem": "Picking poses for objects with known CAD geometry come from RGB-D images of a bin.",
        "role": "I trained the segmenter and aligned visible-surface CAD templates to the segmented points.",
        "method": [
            "The instance segmentation model was trained with separate unoccluded and hole classes. Hole masks were subtracted from object masks, and the remaining instance masks segmented the point cloud.",
            "For each pick pose, I built a visible-surface CAD template by hidden-point removal and aligned it to the segmented points with PCA initialization and point-to-point ICP.",
            "Poses were filtered by registration fitness and inlier RMSE, then ranked and transformed into the robot base with the camera extrinsics.",
        ],
        "outcome": "In 1,000 in-house, fixed-environment trials, the robot moved five object types into an empty container with 89% task success.",
        "stack": "An instance segmentation model, PCA, and point-to-point ICP.",
    },
    "ros-6d-vision": {
        "title": "Hand-eye calibration and 6D pose server",
        "result": "Wrote the ROS server that returns camera and robot-base poses on each request, plus eye-to-hand calibration tools that report residual error.",
        "desc": "Capture, segmentation, and pose estimation run on each request and return poses with matching scores. The eye-to-hand tools report residual error.",
        "video": None,
        "problem": "A caller needs each object pose in the robot base frame, so the camera has to be calibrated to the robot.",
        "role": "I wrote the ROS action server and the eye-to-hand calibration tools.",
        "method": [],
        "outcome": "Each request returns the pose in the camera frame and in the robot base, with a matching score.",
        "stack": "ROS, Zivid, RealSense, ArUco, OpenCV, and dynamic_reconfigure.",
    },
    "license-plate": {
        "title": "License plate recognition",
        "result": "Built the plate recognition pipeline end to end.",
        "desc": "Object detection locates a car license plate, and OCR reads the letters and digits.",
        "video": None,
        "problem": "Reading the letters and digits on a car license plate meant first finding the plate in the image.",
        "role": "I built the recognition pipeline.",
        "method": [
            "A detection model finds the plate.",
            "OCR reads the letters and digits.",
        ],
        "outcome": "",
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


def employment(project):
    group = group_of(project)
    return f"{group['org']}, {group['role']['en']}, {WHEN[project['group']]}."


def head(title, desc, path):
    canon = SITE + "/" if path == "/" else SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/source-serif-4-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/source-serif-4-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
"""


def nav(home):
    prefix = "" if home else "/"
    return f"""<a class="skip" href="#{'glance' if home else 'content'}">Skip to content</a>
<header class="bar wrap">
<a href="{prefix}#work">Work</a>
<a href="{prefix}#record">Patent and awards</a>
<a href="{prefix}#education">Education</a>
<a href="{prefix}#experience">Experience</a>
</header>
"""


def slot(page):
    video = page["video"]
    if not video:
        return ""
    clip = CLIPS[video]
    label = esc(clip["label"])
    return (
        '<div class="slot">'
        f'<img src="{clip["poster"]}" alt="{label}" width="{clip["home_w"]}" height="{clip["home_h"]}">'
        f'<video width="{clip["home_w"]}" height="{clip["home_h"]}" muted loop playsinline autoplay preload="metadata" poster="{clip["poster"]}" aria-label="{label}">'
        f'<source src="{clip["home"]}" type="video/mp4">'
        "</video></div>"
    )


# Home intro, version A in out/r15_for_slop.md.
INTRO = (
    "I build perception for real robots, covering image segmentation, point-cloud perception for obstacle mapping, "
    "object pose estimation, and imitation learning for manipulation. This work has been tested on robots deployed "
    "in orchards and on robot arms. Next, I want to move toward vision-language-action models."
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


def home_page():
    rows = []
    for project in PROJECTS:
        page = PAGES[project["slug"]]
        href = project_href("en", project["slug"])
        kind = "proj" if page["video"] else "proj proj-plain"
        rows.append(
            f'<article class="{kind}" id="{esc(project["slug"])}">'
            f"{slot(page)}"
            '<div class="proj-copy">'
            f'<h2><a href="{href}">{esc(page["title"])}</a></h2>'
            f'<p>{esc(page["result"])} <a href="{href}">details</a></p>'
            "</div></article>"
        )
    body = f"""{head("Jaewoo Choi", "Perception engineer building segmentation, point-cloud perception, pose estimation, and manipulation learning for orchard robots and robot arms.", "/")}
<body>
{nav(True)}
<main class="wrap glance" id="glance">
<div class="who">
<h1>Jaewoo Choi</h1>
<p class="role">Perception Engineer</p>
<p class="interest">{esc(INTRO)}</p>
<p class="contacts">{contact_icons()}</p>
</div>
<div class="work" id="work">
{''.join(rows)}
</div>
<div class="below">
<section id="record">
<h2>Patent and awards</h2>
<ul>
<li>Korean Patent 10-2694987, registered Aug. 2024. Applicant PLAIF. Co-inventor. {esc(PATENT_TITLE)} The basis is the <a href="{project_href("en", "cad-free-assembly")}">CAD-free assembly</a> work.</li>
<li>Kaggle UBC-OCEAN: bronze medal, team rank 83/1,326, Jan. 2024.</li>
<li>Kaggle Image Matching Challenge 2022: silver medal, team rank 50/642, June 2022. <a href="{esc(MATCH)}">Code</a>.</li>
<li>Kaggle Happywhale (Whale and Dolphin Identification): bronze medal, team rank 127/1,588, Apr. 2022. <a href="{esc(WHALE)}">Code</a>.</li>
</ul>
</section>
<section id="education">
<h2>Education</h2>
<ul>
<li>Bachelor of Engineering, Industrial Management Systems Engineering, Seokyeong University, Seoul, Mar. 2016–Aug. 2022. Multidisciplinary major: Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies). GPA 3.34/4.5 overall; 3.91/4.5 in the final two years.</li>
<li>Mandatory military service as a conscripted auxiliary police officer, Korean National Police Agency, 2017–2019.</li>
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
</div>
</main>
{SCRIPT}
</body>
</html>
"""
    return harden_html(body)


def film(page):
    video = page["video"]
    if not video:
        return ""
    clip = CLIPS[video]
    label = esc(clip["label"])
    return (
        f'<figure class="film {clip["orient"]}">'
        f'<video width="{clip["full_w"]}" height="{clip["full_h"]}" muted playsinline controls preload="metadata" poster="{clip["poster"]}" aria-label="{label}">'
        f'<source src="{clip["full"]}" type="video/mp4">'
        "</video>"
        f"<figcaption>{label}</figcaption>"
        "</figure>"
    )


def pager(project):
    idx = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    prev = '<span></span>'
    nxt = '<span></span>'
    if idx > 0:
        item = PROJECTS[idx - 1]
        prev = (
            f'<a href="{project_href("en", item["slug"])}">'
            '<span class="dir quiet">Previous</span>'
            f'{esc(PAGES[item["slug"]].get("nav_title", PAGES[item["slug"]]["title"]))}</a>'
        )
    if idx + 1 < len(PROJECTS):
        item = PROJECTS[idx + 1]
        nxt = (
            f'<a href="{project_href("en", item["slug"])}">'
            '<span class="dir quiet">Next</span>'
            f'{esc(PAGES[item["slug"]].get("nav_title", PAGES[item["slug"]]["title"]))}</a>'
        )
    return (
        '<nav class="pager" aria-label="Adjacent projects">'
        f"{prev}"
        '<a href="/#work">All work</a>'
        f"{nxt}"
        "</nav>"
    )


DIAGRAMS = {
    "language-distilled-segmentation": """<figure class="flow">
<div class="flow-step">
<p class="flow-k">RGB image input</p>
</div>
<div class="flow-step">
<p class="flow-k">Open-vocabulary instance segmentation</p>
</div>
<div class="flow-fork">
<div>
<p class="flow-k">Version 1</p>
<p>Frozen DINOv3 + SigLIP2 encoders. Trained image and text adapters, PAN-FPN neck, instance and semantic heads.</p>
</div>
<div>
<p class="flow-k">Version 2</p>
<p>DETR-style model. Language-teacher supervision during training only.</p>
</div>
</div>
<div class="flow-step">
<p class="flow-k">Instance masks</p>
</div>
<div class="flow-step">
<p class="flow-k">Associate the masks</p>
<p>Point-cloud voxel centers projected into the image. Virtual voxels from valid anchor depths.</p>
</div>
<div class="flow-step">
<p class="flow-k">Occupancy grid</p>
<p>Decay, hysteresis, and cost inflation, for navigation.</p>
</div>
<figcaption>Both versions write instance masks. On production RT100, the occupancy grid is built from the Version 1 masks.</figcaption>
</figure>
""",
    "ros-6d-vision": """<figure class="flow">
<p class="flow-k">Per request, config-driven</p>
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
    ("language-distilled-segmentation", "Version 1"): {
        "src": "/assets/figures/open-vocab-v1.png",
        "w": 1920,
        "h": 930,
        "alt": "Version 1: frozen DINOv3 image and SigLIP2 text encoders, with a trained image adapter, PAN-FPN neck, text adapter, and instance and semantic heads.",
        "caption": "Version 1. DINOv3 and SigLIP2 stay frozen. The image adapter, PAN-FPN neck, text adapter, and instance and semantic heads are trained.",
    },
    ("language-distilled-segmentation", "Version 2"): {
        "src": "/assets/figures/open-vocab-v2.png",
        "w": 2000,
        "h": 1230,
        "alt": "Diagram of Version 2. A frozen image encoder feeds a multi-scale projector and a three-layer decoder with 300 queries, which drive mask, box and class heads. Category names pass through a trainable text encoder to select queries and score classes. In a training-only branch, mask and image captions pass through a frozen teacher text encoder and are aligned with matched queries and pooled image features.",
        "caption": "Version 2: open-vocabulary instance segmentation model. Category names (teal) are used at inference. Mask captions (magenta) and image captions (gold) are used only in training.",
    },
}


# Extra sections placed after Method. Raw HTML; harden_html adds the text hyphen handling.
EXTRA_SECTIONS = {
    "auto-labeling": """<section>
<h2>Model structure</h2>
<p>The pipeline builds on an existing prompt-conditioned segmentation model. A visual backbone and feature-projection stage provide shared image features, while point- and mask-conditioned decoding initializes or refines object masks. Temporal object memory carries information between frames for video tracking.</p>
<figure class="arch"><img src="/assets/figures/video-tracker.png" width="2040" height="900" alt="Prompt-guided segmentation and tracking: an image encoder and feature-projection stage feed point- and mask-conditioned decoding. Temporal object memory carries information between frames. Mask logits go to CPU post-processing for COCO polygons and RLE masks."><figcaption>The GPU service runs the tracker. A CPU service turns its mask logits into COCO polygons and RLE masks.</figcaption></figure>
<p>The model runtime uses an existing open-source TensorRT implementation.</p>
</section>
<section>
<h2>Adapting the model to annotation</h2>
<p>My work focused on adapting this architecture to the annotation workflow:</p>
<ol>
<li>I derived an image-only execution graph that excludes video-specific output branches without changing retained weights or operations.</li>
<li>I reused visual features on the GPU and retained intermediate mask predictions on-device during iterative correction. Only the final correction is committed to persistent tracking memory.</li>
<li>GPU inference and CPU post-processing run as separate services, supporting interactive previews and video label propagation within the same workflow.</li>
</ol>
</section>
<section>
<h2>Captioning after labeling</h2>
<p>After auto-labeling finished, Qwen-series vision-language models captioned the labeled data in three stages:</p>
<ul>
<li>Each mask got a caption of the object it covers.</li>
<li>Each mask also got a caption of its relationship to the image.</li>
<li>The whole image got a caption of its own.</li>
</ul>
</section>
""",
}


def arch_figure(slug, label):
    item = ARCH.get((slug, label))
    if not item:
        return ""
    return (
        '<figure class="arch">'
        f'<img src="{item["src"]}" width="{item["w"]}" height="{item["h"]}" alt="{esc(item["alt"])}">'
        f"<figcaption>{esc(item['caption'])}</figcaption>"
        "</figure>"
    )


def project_page(project):
    page = PAGES[project["slug"]]
    method = page["method"]
    if method and isinstance(method[0], tuple):
        blocks = []
        for label, text in method:
            blocks.append(f"<h3>{esc(label)}</h3>\n<p>{esc(text)}</p>")
            figure = arch_figure(project["slug"], label)
            if figure:
                blocks.append(figure)
        steps = "\n".join(blocks)
    elif method:
        items = "\n".join(f"<li>{esc(step)}</li>" for step in method)
        steps = f"<ol>\n{items}\n</ol>"
    else:
        steps = ""
    title = f"{page['title']}, Jaewoo Choi"
    path = project_href("en", project["slug"])
    extra = EXTRA_SECTIONS.get(project["slug"], "")
    if extra:
        extra = extra.strip() + "\n"
    result = ""
    if page["outcome"]:
        result = f"""<section>
<h2>Result</h2>
<p>{esc(page["outcome"])}</p>
</section>
"""
    diagram = DIAGRAMS.get(project["slug"], "")
    if diagram:
        diagram = diagram.strip() + "\n"
    body = f"""{head(title, page["desc"], path)}
<body class="page">
{nav(False)}
<main id="content">
<h1>{esc(page["title"])}</h1>
<p class="meta">{esc(employment(project))}</p>
{film(page)}
<section>
<h2>Problem</h2>
<p>{esc(page["problem"])}</p>
</section>
<section>
<h2>My role</h2>
<p>{esc(page["role"])}</p>
</section>
<section>
<h2>Method</h2>
{diagram}{steps}
</section>
{extra}{result}{pager(project)}
</main>
{SCRIPT}
</body>
</html>
"""
    return harden_html(body)


def not_found_page():
    body = f"""{head("Page not found", "This address is not on the site.", "/404.html")}
<body class="page">
{nav(False)}
<main id="content" class="missing">
<h1>Page not found</h1>
<p>This address is not on the site.</p>
<p><a href="/">All work</a></p>
</main>
</body>
</html>
"""
    return harden_html(body)


def write_all():
    if PUBLISH_KO:
        raise SystemExit("PUBLISH_KO is true. This writer publishes English only.")
    ko = ROOT / "ko"
    if ko.exists():
        shutil.rmtree(ko)
    (ROOT / "index.html").write_text(home_page(), encoding="utf-8")
    projects = ROOT / "projects"
    projects.mkdir(exist_ok=True)
    keep = set()
    for project in PROJECTS:
        name = project["slug"] + ".html"
        keep.add(name)
        (projects / name).write_text(project_page(project), encoding="utf-8")
    for path in projects.glob("*.html"):
        if path.name not in keep:
            path.unlink()
    (ROOT / "404.html").write_text(not_found_page(), encoding="utf-8")


if __name__ == "__main__":
    write_all()
