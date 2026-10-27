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
        "result": "Instance masks and an occupancy grid run on production RT100, with TensorRT on Jetson Nano.",
        "desc": "Two versions of an open-vocabulary segmenter for RT100, and the occupancy-grid mapping that uses the masks. Deployed on production RT100.",
        "video": None,
        "problem": "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set, and those masks have to become a navigable map under embedded compute limits. A language teacher is available during training. The deployed model does not add inference cost.",
        "role": "I pre-trained one segmentation stack, adapted a DETR-based segmenter for the RT100 orchard platform, and built the occupancy-grid mapping from the instance masks.",
        "method": [
            (
                "Version 1",
                "I pre-trained the adapter, neck, and segmentation head on multiple datasets over frozen DINOv2 and SigLIP2 encoders, with region-text alignment for instance and semantic segmentation. The model takes text prompts at inference and can run with a fixed vocabulary. I adapted it to the orchard domain.",
            ),
            (
                "Version 2",
                "A DETR-based segmenter uses a frozen DINOv3 backbone, a trainable lightweight text encoder, a multi-scale feature projector, and a three-layer decoder. The decoder predicts masks from dot products between queries and refined spatial features. During training only, object queries and pooled image features are matched to precomputed language-teacher embeddings of object and image descriptions. Semantically related negatives are reweighted so they are not pushed apart. The language teacher adds no inference cost.",
            ),
            (
                "Post-processing",
                "Point-cloud voxel centers are projected into the image and tied to the instance masks. Virtual voxels are added from valid anchor depths. Obstacles go into a navigable occupancy grid with decay, hysteresis, and cost inflation.",
            ),
        ],
        "outcome": "The work runs in the production RT100 perception pipeline. It is deployed on production RT100 platforms and optimized with TensorRT on Jetson Nano.",
        "stack": "DINOv2, SigLIP2, DETR, a frozen DINOv3 backbone, a lightweight text encoder, a multi-scale feature projector, a three-layer decoder, TensorRT, and Jetson Nano.",
    },
    "auto-labeling": {
        "title": "Auto-labeling pipeline",
        "result": "Per-image labeling cost fell from about USD 1.05 to about USD 0.036 (96.6%).",
        "desc": "Video auto-labeling and region-grounded captions. Per-image cost fell from about USD 1.05 to about USD 0.036.",
        "video": None,
        "problem": "Manual annotation cost limits the supply of segmentation data and region-grounded vision-language training data.",
        "role": "I built the video auto-labeling pipeline, set the label taxonomy and the annotation guidelines, and compiled the COCO-format training datasets.",
        "method": [
            "Point prompts and mask corrections become tracked masks with consistent IDs across frames.",
            "Image and video inputs share TensorRT engines, so the same computation is not duplicated.",
            "Qwen-series vision-language models write region-grounded object descriptions and check them. Uncertain cases go to a second review. Verified descriptions are linked to the instance annotations.",
        ],
        "outcome": "Per-image labeling cost fell from about USD 1.05 to about USD 0.036, a 96.6% reduction.",
        "stack": "TensorRT, Qwen-series vision-language models, and COCO.",
    },
    "strawberry-cultivation": {
        "title": "Strawberry cultivation tasks",
        "result": "Transplanting 93.8%, flower thinning 87.5%, and runner handling 65% across 1,000 fixed-lab trials. Shown at CES 2025.",
        "desc": "Diffusion Policy on UMI demonstrations for three strawberry tasks. 93.8%, 87.5%, and 65% across 1,000 fixed-lab trials. Exhibited at CES 2025.",
        "video": "strawberry",
        "problem": "Three strawberry cultivation tasks had to be learned from human demonstrations: transplanting, flower thinning, and runner handling. The demonstrations were collected with a Universal Manipulation Interface (UMI).",
        "role": "I led the data pipeline and the policy training for all three tasks. I built everything except the robot-side post-processing.",
        "method": [
            "I collected GoPro RGB and IMU data and calibrated the camera to the IMU.",
            "I turned ORB-SLAM3 visual-inertial SLAM trajectories into training sets.",
            "I trained Diffusion Policy with RGB features and robot state as global conditioning, and compared U-Net and ViT configurations.",
        ],
        "outcome": "In a fixed lab, across 1,000 trials, success was 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The work was exhibited at CES 2025.",
        "stack": "UMI, GoPro, IMU, ORB-SLAM3, Diffusion Policy, U-Net, and ViT.",
    },
    "cad-free-assembly": {
        "title": "CAD-free assembly",
        "result": "93% task success across 1,000 in-house trials, with no CAD model of the part.",
        "desc": "6D tool poses for assembly from a 2D camera, with no CAD model of the part. 93% task success across 1,000 in-house trials.",
        "video": "cad",
        "problem": "Assembly needs a target 6D tool pose when the part has no CAD model. At run time the sensor is a 2D camera.",
        "role": "I prototyped a two-view baseline and built the final pose pipeline.",
        "method": [
            "I prototyped a two-view RGB baseline: learned feature matching between a reference image and a target image, USAC essential-matrix estimation, relative pose recovery, and triangulation.",
            "In the final pipeline, LightGlue matches the live 2D image to a stored reference RGB-D capture, so each match carries depth. Matches with no depth are removed.",
            "solvePnP and RANSAC estimate the camera pose from the 3D-2D matches. That pose is chained with the hand-eye calibration and the stored reference pose. The result is the target 6D tool pose.",
        ],
        "outcome": "Task success was 93% across 1,000 in-house trials. This work is the basis of Korean Patent 10-2694987.",
        "stack": "LightGlue, USAC, solvePnP, RANSAC, and hand-eye calibration.",
    },
    "bin-picking": {
        "title": "CAD-based bin picking",
        "result": "89% task success across 1,000 in-house trials on five object types.",
        "desc": "Picking poses from RGB-D images and known CAD geometry. 89% task success in 1,000 in-house, fixed-environment trials.",
        "video": "bin",
        "problem": "Picking poses were needed for objects with known CAD geometry. The source is RGB-D images of a bin.",
        "role": "I trained the segmenter and fit visible-surface CAD templates to the segmented points.",
        "method": [
            "I trained Mask R-CNN (ResNet-101) with separate unoccluded and hole classes. Hole masks are subtracted from object masks. The remaining instance masks segment the point cloud.",
            "Visible-surface CAD templates for each pick pose are built by hidden-point removal, then fit to the segmented points with PCA initialization and point-to-point ICP.",
            "Each fit is checked model-to-scene and scene-to-model. Poses are filtered by registration fitness, inlier RMSE, and a combined score. Candidates are ranked and transformed into the robot base with the camera extrinsics.",
        ],
        "outcome": "Task success was 89% in 1,000 in-house, fixed-environment trials, moving five object types into an empty container.",
        "stack": "Mask R-CNN, ResNet-101, PCA, and point-to-point ICP.",
    },
    "ros-6d-vision": {
        "title": "ROS 6D vision server",
        "result": "A ROS action server returns robot-base and camera-frame poses, with eye-to-hand calibration tools.",
        "desc": "A ROS action server for capture, segmentation, and 6D pose, plus eye-to-hand calibration tools.",
        "video": None,
        "problem": "A caller needs the object pose in the robot base frame and in the camera frame. The camera also has to be calibrated to the robot.",
        "role": "I wrote the ROS action server and the eye-to-hand calibration tools.",
        "method": [
            "The server runs capture, segmentation, and pose estimation per request, and returns robot-base and camera-frame poses with matching scores.",
            "A configuration file selects the camera (Zivid, RealSense, or recorded data), the model, and the pipeline.",
            "Eye-to-hand calibration uses ArUco board pose estimation, the OpenCV Park method, and a batch AX = YB solver that reports residual error. A validation tool checks the calibration. Runtime parameters use ROS dynamic_reconfigure.",
        ],
        "outcome": "Each request returns the object pose in the robot base frame and in the camera frame, with a matching score.",
        "stack": "ROS, Zivid, RealSense, ArUco, OpenCV, and dynamic_reconfigure.",
    },
    "license-plate": {
        "title": "License plate recognition",
        "result": "Object detection finds the plate and OCR reads the letters and digits.",
        "desc": "A license-plate pipeline: object detection finds the plate, and OCR reads the letters and digits.",
        "video": None,
        "problem": "The letters and digits on a car license plate had to be read.",
        "role": "I built the recognition pipeline.",
        "method": [
            "Object detection finds the plate.",
            "OCR reads the letters and digits.",
        ],
        "outcome": "The pipeline finds the plate and reads its letters and digits.",
        "stack": "Object detection and OCR.",
    },
}

CLIPS = {
    "strawberry": {
        "home": "/assets/video/home/strawberry.mp4",
        "full": "/assets/video/strawberry-ces2025.mp4",
        "poster": "/assets/frames/strawberry-booth.jpg",
        "home_w": 720,
        "home_h": 404,
        "full_w": 540,
        "full_h": 960,
        "orient": "portrait",
        "label": "Flower thinning at the CES 2025 booth.",
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
        "label": "UR arm with a gripper and wrist camera, assembling a part on a fixture.",
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
        "label": "A Doosan cobot during CAD-based bin picking.",
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
        return '<div class="slot slot-empty" aria-hidden="true"></div>'
    clip = CLIPS[video]
    label = esc(clip["label"])
    return (
        '<div class="slot">'
        f'<img src="{clip["poster"]}" alt="{label}" width="{clip["home_w"]}" height="{clip["home_h"]}">'
        f'<video width="{clip["home_w"]}" height="{clip["home_h"]}" muted loop playsinline autoplay preload="metadata" poster="{clip["poster"]}" aria-label="{label}">'
        f'<source src="{clip["home"]}" type="video/mp4">'
        "</video></div>"
    )


def home_page():
    rows = []
    for project in PROJECTS:
        page = PAGES[project["slug"]]
        href = project_href("en", project["slug"])
        rows.append(
            f'<article class="proj" id="{esc(project["slug"])}">'
            f"{slot(page)}"
            '<div class="proj-copy">'
            f'<h2><a href="{href}">{esc(page["title"])}</a></h2>'
            f'<p>{esc(page["result"])} <a href="{href}">details</a></p>'
            "</div></article>"
        )
    body = f"""{head("Jaewoo Choi", "Senior AI Researcher at Daedong AILab. Perception for real robots, toward vision-language-action models.", "/")}
<body>
{nav(True)}
<main class="wrap glance" id="glance">
<div class="who">
<h1>Jaewoo Choi</h1>
<p class="role">Senior AI Researcher, Daedong AILab</p>
<p class="interest">I work on perception for real robots and want to extend it toward vision-language-action models that connect what a robot sees with how it acts.</p>
<p class="contacts"><a href="mailto:{esc(EMAIL)}">Email</a><a href="{esc(GITHUB)}" rel="me">GitHub</a><a href="{esc(KAGGLE)}" rel="me">Kaggle</a><a href="{esc(LINKEDIN)}" rel="me">LinkedIn</a></p>
</div>
<p class="evidence">Production RT100. 1,000-trial robot evaluations. Patent 10-2694987. 3 Kaggle medals.</p>
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
            f'{esc(PAGES[item["slug"]]["title"])}</a>'
        )
    if idx + 1 < len(PROJECTS):
        item = PROJECTS[idx + 1]
        nxt = (
            f'<a href="{project_href("en", item["slug"])}">'
            '<span class="dir quiet">Next</span>'
            f'{esc(PAGES[item["slug"]]["title"])}</a>'
        )
    return (
        '<nav class="pager" aria-label="Adjacent projects">'
        f"{prev}"
        '<a href="/#work">All work</a>'
        f"{nxt}"
        "</nav>"
    )


def project_page(project):
    page = PAGES[project["slug"]]
    method = page["method"]
    if method and isinstance(method[0], tuple):
        steps = "\n".join(
            f"<h3>{esc(label)}</h3>\n<p>{esc(text)}</p>" for label, text in method
        )
    else:
        items = "\n".join(f"<li>{esc(step)}</li>" for step in method)
        steps = f"<ol>\n{items}\n</ol>"
    title = f"{page['title']}, Jaewoo Choi"
    path = project_href("en", project["slug"])
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
{steps}
</section>
<section>
<h2>Result</h2>
<p>{esc(page["outcome"])}</p>
</section>
<section>
<h2>Stack</h2>
<p>{esc(page["stack"])}</p>
</section>
{pager(project)}
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
