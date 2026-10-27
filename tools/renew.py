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
        "result": "Built two versions of an open-vocabulary segmenter and the obstacle-mapping step after it. Deployed on production RT100 robots with TensorRT on Jetson Nano.",
        "desc": "Two versions of an open-vocabulary segmenter for the RT100 orchard platform, and the occupancy grid built from the masks. The pipeline runs on production RT100 with TensorRT on Jetson Nano.",
        "video": None,
        "problem": "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set, and those masks have to become a navigable map under embedded compute limits. A language teacher is available during training. The deployed model does not add inference cost.",
        "role": "I pre-trained a DINOv3 and SigLIP2 segmenter and adapted a DETR-based segmenter for the RT100 orchard platform. The occupancy-grid mapping built from the instance masks is also my work.",
        "method": [
            (
                "Version 1",
                "With the DINOv3 and SigLIP2 encoders frozen, I pre-trained the adapter, neck, and segmentation head on multiple datasets, with region-text alignment for instance and semantic segmentation. On top of that model I added text-prompt inference and fixed-vocabulary conversion, and adapted it to the orchard domain.",
            ),
            (
                "Version 2",
                "The second segmenter is a DETR-based model I adapted, with a frozen DINOv3 backbone, a trainable lightweight text encoder, a multi-scale feature projector, and a three-layer decoder that predicts masks from dot products of queries and refined spatial features. During training only, object queries and pooled image features are aligned with precomputed language-teacher embeddings of object and image descriptions, and semantically related negatives are reweighted so they are not pushed apart.",
            ),
            (
                "Post-processing",
                "Point-cloud voxel centers were projected into the image and associated with the instance masks. I added virtual voxels from valid anchor depths, and obstacles were mapped into a navigable occupancy grid with decay, hysteresis, and cost inflation.",
            ),
        ],
        "outcome": "The model is integrated into the production RT100 perception pipeline. I deployed the pipeline on production RT100 platforms and optimized it with TensorRT on Jetson Nano.",
        "stack": "DINOv3, SigLIP2, DETR, a lightweight text encoder, a multi-scale feature projector, a three-layer decoder, TensorRT, and Jetson Nano.",
    },
    "auto-labeling": {
        "title": "Auto-labeling pipeline",
        "result": "Per-image labeling cost fell from about USD 1.05 to about USD 0.036 (96.6%).",
        "desc": "A video auto-labeling pipeline I built writes region-grounded captions and reduced the cost of labeling one image by 96.6%, from about USD 1.05 to about USD 0.036.",
        "video": "auto",
        "problem": "Segmentation data and region-grounded vision-language data were labeled by hand.",
        "role": "Besides building the video auto-labeling pipeline, I set the label taxonomy and the annotation guidelines and compiled the COCO-format training datasets.",
        "method": [
            "Point prompts and mask corrections were turned into tracked masks with consistent IDs across frames.",
            "Image and video inputs share TensorRT engines, so the same computation is not run twice.",
            "Qwen-series vision-language models wrote the region-grounded object descriptions and checked them. I sent uncertain cases to a second review and linked the verified descriptions to the instance annotations.",
        ],
        "outcome": "Labeling one image cost about USD 1.05 before this pipeline and about USD 0.036 after it, a 96.6% reduction.",
        "stack": "TensorRT, Qwen-series vision-language models, and COCO.",
    },
    "strawberry-cultivation": {
        "title": "Strawberry cultivation tasks",
        "result": "Transplanting 93.8%, flower thinning 87.5%, and runner handling 65% across 1,000 fixed-lab trials. Shown at CES 2025.",
        "desc": "I trained Diffusion Policy on UMI demonstrations for transplanting, flower thinning, and runner handling. In 1,000 fixed-lab trials, success was 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The work was exhibited at CES 2025.",
        "video": "strawberry",
        "problem": "Transplanting, flower thinning, and runner handling are learned from human demonstrations collected with a Universal Manipulation Interface (UMI).",
        "role": "I led the data pipeline and the policy training for all three tasks, and built everything except the robot-side post-processing.",
        "method": [
            "GoPro RGB and IMU data were collected, and I calibrated the camera to the IMU.",
            "ORB-SLAM3 visual-inertial SLAM trajectories were turned into training sets.",
            "Diffusion Policy was trained with RGB features and robot state as global conditioning, and I compared U-Net and ViT configurations.",
        ],
        "outcome": "Across 1,000 trials in a fixed lab, transplanting succeeded 93.8% of the time, flower thinning 87.5%, and runner handling 65%. The work was exhibited at CES 2025.",
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
            "A two-view RGB baseline came first. It matched a reference image to a target image with learned features, estimated the essential matrix with USAC, recovered the relative pose, and ran triangulation.",
            "The final pipeline matches the live 2D image to a stored reference RGB-D capture with LightGlue, so each match carries depth. Matches with no depth are removed.",
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
            "The segmenter was an instance segmentation model, trained with separate unoccluded and hole classes. Hole masks were subtracted from object masks, and the remaining instance masks segmented the point cloud.",
            "For each pick pose, I built a visible-surface CAD template by hidden-point removal and aligned it to the segmented points with PCA initialization and point-to-point ICP.",
            "Each fit was checked model-to-scene and scene-to-model, and poses were filtered by registration fitness, inlier RMSE, and a combined score. The remaining candidates were ranked, and their poses were transformed into the robot base with the camera extrinsics.",
        ],
        "outcome": "In 1,000 in-house, fixed-environment trials, the robot moved five object types into an empty container with 89% task success.",
        "stack": "An instance segmentation model, PCA, and point-to-point ICP.",
    },
    "ros-6d-vision": {
        "title": "ROS 6D vision server",
        "result": "Wrote the ROS server that returns camera and robot-base poses on each request from Zivid, RealSense, or recorded data, plus eye-to-hand calibration tools that report residual error.",
        "desc": "Capture, segmentation, and pose estimation run on each request and return poses with matching scores. The eye-to-hand tools report residual error.",
        "video": None,
        "problem": "Each request returns an object pose in the robot base frame and in the camera frame, so the camera has to be calibrated to the robot.",
        "role": "I wrote the ROS action server and the eye-to-hand calibration tools.",
        "method": [
            "On each request, the server runs capture, segmentation, and pose estimation.",
            "A configuration file selects the camera (Zivid, RealSense, or recorded data), the model, and the pipeline.",
            "The eye-to-hand transform is computed from ArUco board poses with the OpenCV Park method and a batch AX = YB solver that reports residual error. I also added a validation tool and ROS dynamic_reconfigure for runtime parameters.",
        ],
        "outcome": "Each request returns the pose in the camera frame and in the robot base, with a matching score.",
        "stack": "ROS, Zivid, RealSense, ArUco, OpenCV, and dynamic_reconfigure.",
    },
    "license-plate": {
        "title": "License plate recognition",
        "result": "Built the plate recognition pipeline end to end: detection finds the plate, OCR reads it.",
        "desc": "Object detection locates a car license plate, and OCR reads the letters and digits.",
        "video": None,
        "problem": "Reading the letters and digits on a car license plate meant first finding the plate in the image.",
        "role": "I built the recognition pipeline.",
        "method": [
            "A detection model finds the plate.",
            "OCR reads the letters and digits.",
        ],
        "outcome": "The output is the plate's letters and digits.",
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
    body = f"""{head("Jaewoo Choi", "Senior AI Researcher at Daedong AILab, with work on open-vocabulary segmentation, obstacle mapping, 6D pose, and imitation learning for orchard and manipulation robots.", "/")}
<body>
{nav(True)}
<main class="wrap glance" id="glance">
<div class="who">
<h1>Jaewoo Choi</h1>
<p class="role">Senior AI Researcher, Daedong AILab</p>
<p class="interest">I work on perception for real robots: open-vocabulary RGB-D segmentation, point-cloud-image fusion for obstacle mapping, 6D pose estimation, and imitation learning for manipulation. This work was developed and tested on deployed orchard robots and on manipulation robots. Next, I want to extend it toward vision-language-action models that connect what a robot sees with how it acts.</p>
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


DIAGRAMS = {
    "language-distilled-segmentation": """<figure class="flow">
<div class="flow-step">
<p class="flow-k">RGB-D input</p>
</div>
<div class="flow-step">
<p class="flow-k">Open-vocabulary instance segmentation</p>
</div>
<div class="flow-fork">
<div>
<p class="flow-k">Version 1</p>
<p>Frozen DINOv3 + SigLIP2 encoders, trained adapter, neck, segmentation head.</p>
</div>
<div>
<p class="flow-k">Version 2</p>
<p>DETR-based, frozen DINOv3 backbone, lightweight text encoder, language-teacher supervision during training only.</p>
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
<figcaption>Both versions write instance masks. The occupancy grid is built from those masks.</figcaption>
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
        "alt": "Version 1: a frozen image encoder, an adapter, a PAN-FPN neck, instance and semantic heads, and a text encoder.",
        "caption": "Version 1. Frozen image and text encoders, a trained adapter and neck, and instance and semantic heads.",
    },
    ("language-distilled-segmentation", "Version 2"): {
        "src": "/assets/figures/open-vocab-v2.png",
        "w": 1920,
        "h": 860,
        "alt": "Version 2: a multi-scale projector, a three-layer decoder, and a teacher-alignment branch that runs only during training.",
        "caption": "Version 2. Multi-scale features and a three-layer decoder. The teacher branch runs only during training.",
    },
}


# Extra sections placed after Method. Raw HTML; harden_html adds the text hyphen handling.
EXTRA_SECTIONS = {
    "auto-labeling": """<section>
<h2>Model: a tracker built on SAM3</h2>
<p>The labeling tracker is based on the SAM3 video tracker, compiled to TensorRT engines and driven by clicks and seed masks. Class names and track IDs come from the labeling backend, so the model only has to produce masks. The engines follow an open-source TensorRT build of that tracker. It keeps SAM3's weights and changes how the work is divided between engines and where memory lives on the GPU.</p>
</section>
<section>
<h2>Model structure</h2>
<p>The tracker runs as separate engines. A ViT image encoder runs once per frame, and a neck turns its output into multi-scale features. Two prompt paths can start an object. The point-prompt decoder predicts a mask from the first positive or negative click and refines it with each later click. The mask-prompt init takes a seed mask and writes it into the memory bank. On every later frame, a step engine runs memory attention over that bank of past mask memories and object pointers, predicts the object's mask and encodes the new memory. Each path returns mask logits with an IoU estimate and an object score.</p>
<figure class="arch"><img src="/assets/figures/video-tracker.png" width="2040" height="900" alt="SAM3 tracker path: a frozen image encoder and neck feed a point-prompt decoder, a mask-prompt init, and a memory-attention step that reads and writes a memory bank. Mask logits go to the CPU service that writes COCO polygons and RLE masks."><figcaption>The GPU service runs the tracker. A CPU service turns its mask logits into COCO polygons and RLE masks.</figcaption></figure>
<h3>What the TensorRT build changes</h3>
<p>Splitting the graph lets the costly part run once. The encoder's output buffer is bound directly as the neck's input, and the neck's three feature maps feed the init and step engines without any copy. A frame with many objects still pays for one encoder pass.</p>
<p>The step engine takes memory as a gathered list of key tokens with a valid-key count per object, not as a fixed stack of frames. Each key carries its own rotary position index and keeps its place in the frame when other keys are dropped. Object pointers sit before the memory keys, so the count mask never cuts a pointer in a mixed batch. With the full memory, the computation matches the original tracker. The difference is per-object key pruning: only keys near the object's last mask survive, plus a coarse background grid for global context. Attention cost follows the number of keys, so each object pays only for the keys around it.</p>
<p>Memory stays on the GPU as FP16 token rows in a reusable buffer pool. Before each step, the CPU writes a short table of row addresses and a small CUDA kernel gathers those rows into the step's input. Only address tables, key counts, scores and low-resolution mask logits cross the bus. History is bounded, with a few conditioning memories, a recent window and a capped pointer list per object. Several objects advance in one batched step, and the first layer's self-attention over the frame is computed once for all of them. The neck, init and step engines run in FP16, while the point-prompt decoders and, in this pipeline's mode, the encoder layers stay in FP32.</p>
</section>
<section>
<h2>How the pipeline uses it</h2>
<p>On top of SAM3, I built the prompting, serving and post-processing layer.</p>
<ol>
<li>Clicks on a video frame accumulate. Each new click refines the previous mask on the GPU, and the object's memory is committed only after the last click, so a half-finished mask never reaches the memory bank.</li>
<li>For single images, point heads are cut out of the video point-prompt graphs. They keep the mask, IoU and object-score outputs and drop the memory outputs.</li>
<li>Image and video requests share one image encoder and neck. Every engine is loaded once per process and shared by concurrent workers.</li>
<li>Token pruning for memory and query tokens is reimplemented. Parity tests confirm it picks the same tokens as the original selection.</li>
<li>A preview session snapshots its image features on the GPU. Later clicks on the same image restore that snapshot and skip the encoder.</li>
<li>GPU inference and CPU post-processing run as separate services. The GPU side returns raw mask logits; the CPU side fills holes, resizes the masks and writes COCO polygons or RLE masks.</li>
<li>A correction at a later frame enters as new clicks or a seed mask at that frame. The object keeps its track ID from there on.</li>
</ol>
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
    else:
        items = "\n".join(f"<li>{esc(step)}</li>" for step in method)
        steps = f"<ol>\n{items}\n</ol>"
    title = f"{page['title']}, Jaewoo Choi"
    path = project_href("en", project["slug"])
    extra = EXTRA_SECTIONS.get(project["slug"], "")
    if extra:
        extra = extra.strip() + "\n"
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
{extra}<section>
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
