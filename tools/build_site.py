#!/usr/bin/env python3
"""Facts for the personal site, from the CV.

`python3 tools/build_site.py` writes the HTML through renew.write_all.
The published design is the faculty skim (prototype A): Source Serif 4,
white page, project rows with a clip or an empty slot.
Korean copy stays in this file. PUBLISH_KO is false, so ko/ is not written.
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Korean copy stays in this file. While this is false the build does not
# write ko/. .nojekyll makes GitHub Pages publish every committed path, so
# a side folder would still be served. Set this true and rebuild to restore
# /ko/ and the language switch.
PUBLISH_KO = False
SITE = "https://imjaewoochoi.github.io"
EMAIL = "iam.jaewoochoi@gmail.com"
GITHUB = "https://github.com/ImJaewooChoi"
KAGGLE = "https://www.kaggle.com/loveacaji"
LINKEDIN = "https://www.linkedin.com/in/jaewoo-choi-955340356"
WHALE = "https://github.com/ImJaewooChoi/kaggle_happy_whale"
MATCH = "https://github.com/ImJaewooChoi/kaggle_image_matching2022"

# wide=True links stay on desktop and hide when the row would wrap.
NAV = {
    "en": [
        ("Projects", "projects", False),
        ("Experience", "experience", False),
        ("Patent", "patent", True),
        ("Awards", "awards", True),
    ],
    "ko": [
        ("프로젝트", "projects", False),
        ("경력", "experience", False),
        ("특허", "patent", True),
        ("수상", "awards", True),
    ],
}

UI = {
    "en": {
        "skip": "Skip to content",
        "cv": "CV",
        "updated": "Updated 21 Oct 2026",
        "projects_back": "Projects",
        "no_media": "No media yet",
        "media_comment": "Media can be added later.",
        "cv_comment": "CV PDF will be added later at /cv.pdf",
        "watch": "Watch the MP4",
        "prev": "Previous",
        "next": "Next",
        "pager": "Adjacent projects",
        "missing": "Page not found",
        "missing_body": "This address is not on the site.",
        "research": "Research interests",
        "work": "Selected work",
        "other": "Other projects",
        "details": "Details",
        "experience": "Experience",
        "education": "Education",
        "patent": "Patent",
        "awards": "Awards",
    },
    "ko": {
        "skip": "본문으로",
        "cv": "CV",
        "updated": "2026년 10월 21일 업데이트",
        "projects_back": "프로젝트",
        "no_media": "미디어 없음",
        "media_comment": "미디어는 나중에 넣습니다.",
        "cv_comment": "CV PDF는 나중에 /cv.pdf 에 넣습니다.",
        "watch": "MP4 보기",
        "prev": "이전",
        "next": "다음",
        "pager": "인접 프로젝트",
        "missing": "페이지 없음",
        "missing_body": "이 주소는 사이트에 없습니다.",
        "research": "연구 관심사",
        "work": "주요 작업",
        "other": "다른 프로젝트",
        "details": "자세히",
        "experience": "경력",
        "education": "학력",
        "patent": "특허",
        "awards": "수상",
    },
}

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

VIDEOS = {
    "cad": {
        "file": "cad-free-assembly",
        "orient": "landscape",
        "w": 1280,
        "h": 720,
        "label": {
            "en": "Silent. CAD-free auto assembly on a UR arm",
            "ko": "무음. UR arm의 CAD-free auto assembly",
        },
        "cap": {
            "en": "UR arm with a gripper and wrist camera, assembling a part on a fixture.",
            "ko": "Gripper와 wrist camera가 달린 UR arm이 fixture 위 부품을 조립합니다.",
        },
    },
    "bin": {
        "file": "bin-picking",
        "orient": "landscape",
        "w": 1280,
        "h": 720,
        "label": {
            "en": "Silent. CAD-based bin picking",
            "ko": "무음. CAD-based bin picking",
        },
        "cap": {
            "en": "A ring-scan close-up, then a cobot picking, then a green-bin close-up.",
            "ko": "세 장면입니다. Ring-scan close-up, cobot picking, green-bin close-up.",
        },
    },
    "strawberry": {
        "file": "strawberry-ces2025",
        "orient": "portrait",
        "w": 540,
        "h": 960,
        "label": {
            "en": "Silent. Flower thinning at the CES 2025 booth",
            "ko": "무음. CES 2025 부스의 flower thinning",
        },
        "cap": {
            "en": "Flower thinning at the CES 2025 booth.",
            "ko": "CES 2025 부스에서 flower thinning을 합니다.",
        },
    },
}


def P(*paragraphs):
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


PROJECTS = [
    {
        "slug": "language-distilled-segmentation",
        "group": "daedong",
        "video": None,
        "title": {
            "en": "Open-vocabulary segmentation and mapping",
            "ko": "RT100 open-vocabulary segmentation and occupancy mapping",
        },
        "line": {
            "en": "Built two versions of an open-vocabulary segmenter and the obstacle-mapping step. Version 1 runs on production RT100 robots with TensorRT on Jetson Orin Nano.",
            "ko": "RT100용 open-vocabulary segmenter(Version 1), open-vocabulary DETR 계열 instance segmentation 모델(Version 2), mask로 만드는 occupancy grid입니다. Production RT100에서는 Version 1이 TensorRT, Jetson Orin Nano로 돌아갑니다.",
        },
        "tools": {
            "en": "Open-vocabulary segmentation, DETR, DINOv3, SigLIP2, TensorRT",
            "ko": "Open-vocabulary segmentation, DETR, DINOv3, SigLIP2, TensorRT",
        },
        "desc": {
            "en": "Two versions of an open-vocabulary segmenter for RT100, and the occupancy-grid mapping that uses the masks. Version 1 is deployed on production RT100.",
            "ko": "RT100용 open-vocabulary segmenter 두 버전과 occupancy grid. Production RT100에는 Version 1을 배포했습니다.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set.",
                )),
                ("Approach", P(
                    "Version 2 is a DETR-style open-vocabulary instance segmentation model. The backbone is a frozen DINOv3. A MiniLM text encoder trains.",
                    "A multi-scale feature projector feeds a three-layer decoder. The decoder predicts masks from dot products between queries and refined spatial features.",
                    "During training only, object queries and pooled image features are matched to precomputed language-teacher embeddings of object and image captions. Semantically related negatives are reweighted so they are not pushed apart.",
                )),
                ("Results", P(
                    "Instance masks feed point-cloud projection and occupancy-grid mapping. Version 1 is in the production RT100 perception pipeline.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "RT100 자율 과수원 플랫폼은 고정된 label set 밖의 물체에도 instance mask가 필요합니다. 학습 중에만 language teacher를 써서 추론 비용을 늘리지 않습니다.",
                )),
                ("방법", P(
                    "Version 2는 DETR 계열 open-vocabulary instance segmentation 모델입니다. Backbone은 frozen DINOv3이고, lightweight text encoder는 학습합니다. Multi-scale feature projector 뒤에 three-layer decoder가 있고, decoder는 query와 refined spatial feature의 dot product로 mask를 예측합니다.",
                    "학습 중에만 object query와 pooled image feature를 language-teacher embedding에 맞춥니다. Embedding은 물체 caption과 이미지 caption입니다. 의미가 가까운 negative는 서로 밀리지 않게 가중치를 조정합니다.",
                )),
                ("결과", P(
                    "Instance mask는 point cloud projection과 occupancy grid mapping으로 넘어갑니다. Production RT100 perception pipeline에는 Version 1이 들어가 있습니다.",
                )),
                ("기술", P(
                    "DETR, frozen DINOv3, lightweight text encoder, multi-scale feature projector, three-layer decoder.",
                )),
            ],
        },
    },
    {
        "slug": "auto-labeling",
        "group": "daedong",
        "video": None,
        "title": {
            "en": "Auto-Labeling and Data Captioning System",
            "ko": "Auto-Labeling과 Data Captioning 시스템",
        },
        "line": {
            "en": "Point prompts and mask corrections become tracked masks. Qwen-series models write region-grounded captions. Per-image labeling cost fell from about USD 1.05 to about USD 0.036.",
            "ko": "Point prompt와 mask correction을 tracked mask로 바꿉니다. Qwen 계열 모델이 region caption을 답니다. 이미지당 비용은 약 USD 1.05에서 약 USD 0.036입니다.",
        },
        "tools": {
            "en": "Auto-labeling, TensorRT, Qwen",
            "ko": "Auto-labeling, TensorRT, Qwen",
        },
        "desc": {
            "en": "Video auto-labeling and region-grounded captioning. Per-image labeling cost fell from about USD 1.05 to about USD 0.036.",
            "ko": "Video auto-labeling과 region caption. 이미지당 labeling 비용이 약 USD 1.05에서 약 USD 0.036으로 줄었습니다.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "Manual annotation cost limits the supply of segmentation and region-grounded vision-language training data.",
                    "I built a video auto-labeling pipeline. Point prompts and mask corrections become tracked masks with consistent IDs across frames.",
                )),
                ("Approach", P(
                    "Qwen-series vision-language models generate region-grounded object captions and check them.",
                    "Uncertain cases go to a second review. Verified captions are linked to the instance annotations.",
                    "I set the label taxonomy and the annotation guidelines, and built COCO-format training datasets.",
                )),
                ("Results", P(
                    "Cost per image was about USD 1.05.",
                    "It fell to about USD 0.036.",
                    "That is a 96.6% reduction.",
                )),
                ("Stack", P(
                    "TensorRT, Qwen-series vision-language models, COCO.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "수작업 annotation 비용 때문에 segmentation 학습 데이터와 region-grounded vision-language 학습 데이터가 부족합니다.",
                )),
                ("방법", P(
                    "Video auto-labeling pipeline을 만들었습니다. Point prompt와 mask correction은 frame 사이에서 ID가 유지되는 tracked mask가 되고, image 입력과 video 입력은 TensorRT engine을 공유합니다. 같은 연산을 두 번 하지 않습니다.",
                    "Qwen 계열 vision-language model이 region-grounded object caption을 만들고 검증합니다. 불확실한 경우는 두 번째 검토로 보내고, 검증된 caption은 instance annotation에 연결합니다.",
                    "Label taxonomy와 annotation guideline을 정하고 COCO format 학습 데이터셋을 만들었습니다.",
                )),
                ("결과", P(
                    "이미지당 labeling 비용은 약 USD 1.05였습니다. 약 USD 0.036으로 줄었고, 감소율은 96.6%입니다.",
                )),
                ("기술", P(
                    "TensorRT, Qwen 계열 vision-language model, COCO.",
                )),
            ],
        },
    },
    {
        "slug": "strawberry-cultivation",
        "group": "daedong",
        "video": "strawberry",
        "title": {
            "en": "Strawberry Cultivation-Task Robot with UMI and Diffusion Policy",
            "ko": "UMI와 Diffusion Policy를 쓴 딸기 재배 작업 로봇",
        },
        "line": {
            "en": "Diffusion Policy trained on UMI demonstrations.||Fixed lab, 1,000 trials.||93.8% transplanting, 87.5% flower thinning, 65% runner handling.||Exhibited at CES 2025.",
            "ko": "UMI 시연으로 Diffusion Policy를 학습했습니다. 고정 실험실, 1,000회 시험의 성공률은 transplanting 93.8%, flower thinning 87.5%, runner handling 65%입니다. CES 2025에 전시했습니다.",
        },
        "tools": {
            "en": "Imitation learning, UMI, Diffusion Policy",
            "ko": "Imitation learning, UMI, Diffusion Policy",
        },
        "desc": {
            "en": "UMI demonstrations and Diffusion Policy for three strawberry tasks. Fixed lab, 1,000 trials: 93.8% transplanting, 87.5% flower thinning, 65% runner handling. Exhibited at CES 2025.",
            "ko": "딸기 재배 세 작업의 UMI 시연과 Diffusion Policy. 고정 실험실 1,000회: transplanting 93.8%, flower thinning 87.5%, runner handling 65%. CES 2025 전시.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "Three strawberry cultivation tasks were learned from human demonstrations: transplanting, flower thinning, and runner handling. I built everything except the robot-side post-processing.",
                )),
                ("Approach", P(
                    "Demonstrations were collected with a Universal Manipulation Interface (UMI). I led the data pipeline and the policy training for all three tasks.",
                    "I collected GoPro RGB and IMU data, calibrated the camera to the IMU, and turned ORB-SLAM3 visual-inertial SLAM trajectories into training sets.",
                    "Diffusion Policy was trained with RGB features and robot state as global conditioning.",
                )),
                ("Results", P(
                    "In a fixed lab environment, across 1,000 trials, success was 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. The robot was exhibited at CES 2025.",
                )),
                ("Stack", P(
                    "UMI, GoPro, IMU, ORB-SLAM3, Diffusion Policy, U-Net, ViT.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "사람 시연으로 딸기 재배 세 작업을 학습했습니다. Transplanting, flower thinning, runner handling입니다. 시연은 Universal Manipulation Interface(UMI)로 모았고, 세 작업 모두 data pipeline과 policy 학습을 맡았습니다.",
                )),
                ("방법", P(
                    "GoPro RGB와 IMU 데이터를 수집한 뒤 camera-IMU calibration을 했고, ORB-SLAM3 visual-inertial SLAM trajectory를 학습 데이터로 만들었습니다. RGB feature와 robot state를 global conditioning으로 Diffusion Policy를 학습했고, U-Net과 ViT 구성을 비교했습니다.",
                )),
                ("결과", P(
                    "고정된 실험실에서 1,000회 시험했습니다. 성공률은 transplanting 93.8%, flower thinning 87.5%, runner handling 65%입니다. CES 2025에 전시했습니다.",
                )),
                ("기술", P(
                    "UMI, GoPro, IMU, ORB-SLAM3, Diffusion Policy, U-Net, ViT.",
                )),
            ],
        },
    },
    {
        "slug": "cad-free-assembly",
        "group": "plaif",
        "video": "cad",
        "title": {
            "en": "CAD-free Auto Assembly",
            "ko": "CAD-free Auto Assembly",
        },
        "line": {
            "en": "6D tool poses for assembly from a 2D camera, with no CAD model of the part. 93% task success across 1,000 in-house trials. Basis of Korean Patent 10-2694987.",
            "ko": "부품 CAD 없이 2D camera로 조립용 6D tool pose를 구합니다. 사내 1,000회 시험의 task success는 93%입니다. 한국 특허 10-2694987의 기반입니다.",
        },
        "tools": {
            "en": "6D pose, LightGlue, RANSAC",
            "ko": "6D pose, LightGlue, RANSAC",
        },
        "desc": {
            "en": "6D tool poses for assembly without a part CAD model, from a 2D camera. 93% task success across 1,000 in-house trials. Basis of Korean Patent 10-2694987.",
            "ko": "부품 CAD 없이 2D camera로 6D tool pose. 사내 1,000회 task success 93%. 한국 특허 10-2694987의 기반.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "Assembly needs a target 6D tool pose when the part has no CAD model. At run time the sensor is a 2D camera, not a 3D camera.",
                )),
                ("Approach", P(
                    "In the final pipeline, LightGlue matches the live 2D image to a stored reference RGB-D capture, so each match carries depth.",
                    "solvePnP and RANSAC estimate the camera pose from the 3D-2D matches. That pose is chained with the hand-eye calibration and the stored reference pose. The result is the target 6D tool pose.",
                    "Task success was 93% across 1,000 in-house trials. This work is the basis of Korean Patent 10-2694987.",
                )),
                ("Stack", P(
                    "LightGlue, USAC, solvePnP, RANSAC, hand-eye calibration.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "부품 CAD model이 없을 때 조립용 target 6D tool pose가 필요합니다. 실행 시점의 센서는 3D camera가 아니라 2D camera입니다.",
                )),
                ("방법", P(
                    "먼저 two-view RGB baseline을 만들었습니다. Reference 이미지와 target 이미지 사이에서 learned feature matching, USAC essential-matrix estimation, relative pose recovery, triangulation을 썼습니다.",
                    '최종 pipeline은 LightGlue로 live 2D image와 저장된 reference RGB-D capture를 맞춥니다. Match마다 depth가 붙고, depth가 없는 match는 제거합니다. 3D-2D match에 solvePnP와 RANSAC으로 camera pose를 구한 뒤, hand-eye calibration과 저장된 reference pose를 이어 target 6D tool pose를 얻습니다. 사내 시험 1,000회에서 task success 93%를 기록했습니다. 이 작업이 <a href="/ko/#patent">한국 특허 10-2694987</a>의 기반입니다.',
                )),
                ("기술", P(
                    "LightGlue, USAC, solvePnP, RANSAC, hand-eye calibration.",
                )),
            ],
        },
    },
    {
        "slug": "bin-picking",
        "group": "plaif",
        "video": "bin",
        "title": {
            "en": "CAD-based Auto Bin Picking",
            "ko": "CAD-based Auto Bin Picking",
        },
        "line": {
            "en": "Picking poses from RGB-D images and known CAD geometry. 89% task success in 1,000 in-house, fixed-environment trials, moving five object types into an empty container.",
            "ko": "RGB-D와 CAD geometry로 picking pose를 구합니다. 사내 고정 환경에서 object type 5종을 빈 용기로 옮긴 1,000회 시험의 task success는 89%입니다.",
        },
        "tools": {
            "en": "6D pose, bin picking, instance segmentation model",
            "ko": "6D pose, bin picking, instance segmentation model",
        },
        "desc": {
            "en": "Picking poses from RGB-D and CAD geometry. 89% task success in 1,000 in-house, fixed-environment trials on five object types.",
            "ko": "RGB-D와 CAD로 picking pose. 사내 고정 환경 1,000회, object type 5종, task success 89%.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "I needed picking poses for objects with known CAD geometry.",
                    "The source is RGB-D images of a bin.",
                )),
                ("Approach", P(
                    'I trained an instance segmentation model with separate "unoccluded" and "hole" classes. Hole masks are subtracted from object masks. The remaining instance masks segment the point cloud.',
                    "Visible-surface CAD templates for each pick pose are built by hidden-point removal, then fit to the segmented points with PCA initialization and point-to-point ICP.",
                    "Poses are filtered by registration fitness and inlier RMSE, then ranked and transformed into the robot base with the camera extrinsics.",
                )),
                ("Results", P(
                    "Task success was 89% in 1,000 in-house, fixed-environment trials, moving five object types into an empty container.",
                )),
                ("Stack", P(
                    "Instance segmentation model, PCA, point-to-point ICP.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "CAD geometry를 아는 물체는 bin의 RGB-D image에서 picking pose를 추정합니다.",
                )),
                ("방법", P(
                    'Instance segmentation model을 class "unoccluded"와 "hole"로 나눠 학습했습니다. Object mask에서 hole mask를 빼고, 남은 instance mask로 point cloud를 나눕니다.',
                    "각 pick pose의 visible-surface CAD template은 hidden-point removal로 만들고, PCA initialization 다음 point-to-point ICP로 segmented point에 맞춥니다. Fit은 model-to-scene과 scene-to-model 양쪽을 보고, registration fitness, inlier RMSE, combined score로 pose를 거릅니다. Candidate를 순위화한 뒤 camera extrinsic으로 pose를 robot base에 옮깁니다. 빈 용기로 object type 5종을 옮기는 사내 고정 환경 시험 1,000회에서 task success 89%를 기록했습니다.",
                )),
                ("기술", P(
                    "Instance segmentation model, PCA, point-to-point ICP.",
                )),
            ],
        },
    },
    {
        "slug": "ros-6d-vision",
        "group": "plaif",
        "video": None,
        "title": {
            "en": "ROS 6D Vision Server and Hand-Eye Calibration Tools",
            "ko": "ROS 6D Vision Server와 Hand-Eye Calibration 도구",
        },
        "line": {
            "en": "Wrote the ROS server that returns camera and robot-base poses on each request, plus eye-to-hand calibration tools that report residual error.",
            "ko": "요청마다 capture, segmentation, pose estimation을 실행하는 ROS action server입니다. Eye-to-hand calibration 도구를 같이 만들었습니다.",
        },
        "tools": {
            "en": "6D pose, ROS, hand-eye calibration",
            "ko": "6D pose, ROS, hand-eye calibration",
        },
        "desc": {
            "en": "ROS action server for capture, segmentation, and 6D pose, plus eye-to-hand calibration tools for Zivid and RealSense.",
            "ko": "Capture, segmentation, 6D pose용 ROS action server와 eye-to-hand calibration 도구. Camera는 Zivid, RealSense, recorded data.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "A caller needs the object pose in the robot base frame. The camera also has to be calibrated to the robot.",
                )),
                ("Approach", P(
                    "I wrote a ROS action server that runs capture, segmentation, and pose estimation per request. It returns robot-base and camera-frame poses with matching scores.",
                    "A configuration file selects the camera (Zivid, RealSense, or recorded data), the model, and the pipeline.",
                    "Eye-to-hand calibration uses ArUco board pose estimation, the OpenCV Park method, and a batch AX = YB solver that reports residual error. I added a calibration validation tool. Runtime parameters use ROS dynamic_reconfigure.",
                )),
                ("Stack", P(
                    "ROS, Zivid, RealSense, ArUco, OpenCV, dynamic_reconfigure.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "Robot-base frame과 camera frame의 object pose가 둘 다 필요하고, camera와 robot 사이 eye-to-hand calibration도 필요합니다.",
                )),
                ("방법", P(
                    "ROS action server를 작성했습니다. 요청마다 capture, segmentation, pose estimation을 실행하고, matching score와 함께 robot-base pose와 camera-frame pose를 반환합니다. Configuration file에서 camera(Zivid, RealSense, recorded data), model, pipeline을 고릅니다.",
                    "Eye-to-hand calibration은 ArUco board pose estimation과 OpenCV Park method를 씁니다. Residual error를 보고하는 batch AX = YB solver가 있고, calibration validation tool을 추가했습니다. 실행 중 parameter는 ROS dynamic_reconfigure로 바꿉니다.",
                )),
                ("기술", P(
                    "ROS, Zivid, RealSense, ArUco, OpenCV, dynamic_reconfigure.",
                )),
            ],
        },
    },
    {
        "slug": "license-plate",
        "group": "fs",
        "video": None,
        "title": {
            "en": "Car License Plate Recognition",
            "ko": "차량 번호판 인식",
        },
        "line": {
            "en": "Built the plate recognition pipeline end to end.",
            "ko": "Object detection으로 번호판 위치를 찾습니다. OCR로 문자와 숫자를 읽습니다.",
        },
        "tools": {
            "en": "Detection, OCR",
            "ko": "Detection, OCR",
        },
        "desc": {
            "en": "Object detection locates a car license plate, and OCR reads the letters and digits.",
            "ko": "번호판 pipeline. Object detection으로 위치를 찾고 OCR로 문자와 숫자를 읽습니다.",
        },
        "sections": {
            "en": [
                ("Approach", P(
                    "Read the letters and digits on a car license plate. I built a recognition pipeline. Object detection locates the plate. OCR reads the letters and digits.",
                )),
                ("Stack", P(
                    "Object detection, OCR.",
                )),
            ],
            "ko": [
                ("방법", P(
                    "차량 번호판의 문자와 숫자를 읽습니다. 인식 pipeline을 만들었습니다. Object detection으로 번호판 위치를 찾고, OCR로 문자와 숫자를 인식합니다.",
                )),
                ("기술", P(
                    "Object detection, OCR.",
                )),
            ],
        },
    },
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


def contact_html():
    profiles = "".join(
        f'<a href="{esc(href)}" rel="me">{esc(label)}</a>'
        for href, label in (
            (GITHUB, "GitHub"),
            (KAGGLE, "Kaggle"),
            (LINKEDIN, "LinkedIn"),
        )
    )
    return (
        '<ul class="contact">\n'
        f'<li><a class="mail" href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></li>\n'
        f'<li class="profiles">{profiles}</li>\n'
        "</ul>"
    )


def langs_html(lang, en_path, ko_path):
    if not PUBLISH_KO:
        return ""
    en_cur = ' aria-current="page"' if lang == "en" else ""
    ko_cur = ' aria-current="page"' if lang == "ko" else ""
    return (
        f'<p class="langs">'
        f'<a href="{esc(en_path)}" hreflang="en" lang="en"{en_cur}>EN</a>'
        f'<span class="sep">|</span>'
        f'<a href="{esc(ko_path)}" hreflang="ko" lang="ko"{ko_cur}>한국어</a>'
        f"</p>"
    )


NAV_LINKS = {
    "en": [
        ("Work", "work"),
        ("Patent", "patent"),
        ("Code", "code"),
        ("Experience", "experience"),
        ("Awards", "awards"),
    ],
    "ko": [
        ("작업", "work"),
        ("특허", "patent"),
        ("코드", "code"),
        ("경력", "experience"),
        ("수상", "awards"),
    ],
}

WATCH = {"en": "Watch the demo", "ko": "데모 보기"}
EMAIL_LABEL = {"en": "Email", "ko": "이메일"}

# Home and project-page presentation. Numbers are the CV figures.
# The strawberry post-processing line is the one fact the owner added.
DISPLAY = {
    "strawberry-cultivation": {
        "nav": "Strawberry tasks",
        "pitch": "Teaching a robot three strawberry tasks.",
        "dek": "UMI demonstrations and Diffusion Policy.",
        "notes": [
            "I built the data pipeline and trained Diffusion Policy for three tasks from UMI demonstrations: transplanting, flower thinning, and runner handling.",
            "I built everything except the robot-side post-processing.",
        ],
        "blurb": "I built the data pipeline and trained Diffusion Policy on UMI demonstrations. I built everything except the robot-side post-processing.",
        "results": [
            ("Trials", "1,000, fixed lab"),
            ("Transplanting", "93.8%"),
            ("Flower thinning", "87.5%"),
            ("Runner handling", "65%"),
            ("Shown", "CES 2025"),
        ],
        "stack": ["UMI", "GoPro", "IMU", "ORB-SLAM3", "Diffusion Policy", "U-Net", "ViT"],
    },
    "cad-free-assembly": {
        "nav": "CAD-free assembly",
        "pitch": "Estimating 6D tool poses for assembly, at 93% task success.",
        "dek": "A 2D camera, and no CAD model of the part.",
        "notes": [
            "I matched a live 2D image to a stored RGB-D reference. There is no CAD model of the part.",
            "Across 1,000 in-house trials, task success was 93%. This work is the basis of Korean Patent 10-2694987.",
        ],
        "blurb": "I matched a live 2D image to a stored RGB-D reference, with no CAD model of the part. Task success was 93% across 1,000 in-house trials.",
        "results": [
            ("Task success", "93%"),
            ("Trials", "1,000, in-house"),
            ("Sensor", "2D camera at run time"),
            ("Patent", "Korean Patent 10-2694987"),
        ],
        "stack": ["LightGlue", "USAC", "solvePnP", "RANSAC", "hand-eye calibration"],
    },
    "bin-picking": {
        "nav": "Bin picking",
        "pitch": "Estimating picking poses from RGB-D, at 89% task success.",
        "dek": "RGB-D images and known CAD geometry.",
        "notes": [
            "I fit visible-surface CAD templates to segmented points.",
            "Task success was 89% in 1,000 in-house trials, in a fixed environment, moving five object types into an empty container.",
        ],
        "blurb": "I fit visible-surface CAD templates to segmented points. Task success was 89% in 1,000 in-house trials, fixed environment, five object types.",
        "results": [
            ("Task success", "89%"),
            ("Trials", "1,000, in-house, fixed environment"),
            ("Objects", "Five types, into an empty container"),
        ],
        "stack": ["Instance segmentation model", "PCA", "point-to-point ICP"],
    },
    "language-distilled-segmentation": {
        "nav": "RT100 segmentation",
        "pitch": "Segmenting orchard objects on RT100 and mapping the masks.",
        "dek": "Two segmenter versions, then an occupancy grid.",
        "notes": [],
        "blurb": "I built two versions of an open-vocabulary segmenter for RT100 and the occupancy-grid mapping that uses the masks.",
        "results": [
            ("Where it runs", "Version 1: production RT100 perception pipeline"),
            ("Deployment", "Version 1: production RT100, TensorRT on Jetson Orin Nano"),
        ],
        "stack": ["DINOv3", "SigLIP2", "DETR", "lightweight text encoder", "TensorRT", "Jetson Orin Nano"],
    },
    "auto-labeling": {
        "nav": "Auto-labeling",
        "pitch": "Cutting labeling cost from about USD 1.05 to about USD 0.036.",
        "dek": "Tracked masks, then region-grounded captions.",
        "notes": [],
        "blurb": "Point prompts become tracked masks. Per-image cost fell from about USD 1.05 to about USD 0.036, a 96.6% reduction.",
        "results": [
            ("Cost before", "about USD 1.05 per image"),
            ("Cost after", "about USD 0.036 per image"),
            ("Reduction", "96.6%"),
        ],
        "stack": ["TensorRT", "Qwen-series vision-language models", "COCO"],
    },
    "ros-6d-vision": {
        "nav": "ROS 6D vision",
        "pitch": "Serving 6D poses over ROS, with eye-to-hand calibration tools.",
        "dek": "Robot-base poses and camera-frame poses.",
        "notes": [],
        "blurb": "A ROS action server runs capture, segmentation, and pose estimation per request. I also wrote eye-to-hand calibration tools.",
        "results": [
            ("Request", "Capture, segmentation, and pose estimation"),
            ("Returns", "Robot-base and camera-frame poses, with matching scores"),
            ("Cameras", "Zivid, RealSense, or recorded data"),
            ("Calibration", "Eye-to-hand: ArUco, OpenCV Park, AX = YB"),
        ],
        "stack": ["ROS", "Zivid", "RealSense", "ArUco", "OpenCV", "dynamic_reconfigure"],
    },
    "license-plate": {
        "nav": "License plates",
        "pitch": "Locating a plate with detection and reading it with OCR.",
        "dek": "Detection finds the plate. OCR reads it.",
        "notes": [],
        "blurb": "Object detection locates the plate. OCR reads the letters and digits.",
        "results": [
            ("Locate", "Object detection"),
            ("Read", "OCR, letters and digits"),
        ],
        "stack": ["Object detection", "OCR"],
    },
}

PATENT_TITLE = (
    "Pose estimating device and method using artificial intelligence to "
    "estimate pose of robot's end effector for object and robot control "
    "system including the same."
)


def tail(text):
    parts = text.rsplit(" ", 1)
    if len(parts) == 2 and parts[0] and parts[1]:
        return parts[0] + "\u00a0" + parts[1]
    return text


def plain_title(text):
    return re.sub(r"<[^>]+>", "", text)


def show(project, lang):
    if lang == "en":
        return DISPLAY[project["slug"]]
    line = project["line"][lang].split("||")[0]
    return {
        "nav": project["title"][lang],
        "pitch": project["title"][lang],
        "dek": line,
        "notes": [project["desc"][lang]],
        "blurb": project["desc"][lang],
        "results": [],
        "stack": [part.strip() for part in project["tools"][lang].split(",")],
    }


def h(tag, text, attrs=""):
    attr = f" {attrs}" if attrs else ""
    return f"<{tag}{attr}>{esc(tail(text))}</{tag}>"


def h_link(tag, text, href, label):
    return (
        f'<{tag}><a href="{esc(href)}" aria-label="{esc(label)}">'
        f"{esc(tail(text))}</a></{tag}>"
    )


def nav_html(lang):
    base = home_href(lang)
    links = "\n".join(
        f'<a href="{base}#{anchor}">{esc(label)}</a>'
        for label, anchor in NAV_LINKS[lang]
    )
    return f"""<header class="nav">
<div class="nav-glass">
<div class="nav-bar">
<a class="wordmark" href="{base}">Jaewoo Choi</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span class="nav-toggle-icon"></span></button>
</div>
</div>
<nav class="nav-links" id="site-nav">
{links}
</nav>
</header>"""


def head(lang, title, desc, path, en_path, ko_path):
    canonical = abs_url(path)
    ko_alt = ""
    if PUBLISH_KO:
        ko_alt = f'<link rel="alternate" hreflang="ko" href="{esc(abs_url(ko_path))}">\n'
    kr = ""
    if lang == "ko":
        kr = '<link rel="preload" href="/assets/fonts/ibm-plex-sans-kr-400.woff2" as="font" type="font/woff2" crossorigin>\n'
    safe_title = esc(plain_title(title))
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
<meta name="description" content="{esc(plain_title(desc))}">
<meta name="author" content="Jaewoo Choi">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f5f5f7">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(abs_url(en_path))}">
{ko_alt}<link rel="alternate" hreflang="x-default" href="{esc(abs_url(en_path))}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{kr}<link rel="stylesheet" href="/assets/css/site.css">
</head>"""


def profile_links(lang):
    items = [
        (f"mailto:{EMAIL}", EMAIL_LABEL[lang], ""),
        (GITHUB, "GitHub", ' rel="me"'),
        (KAGGLE, "Kaggle", ' rel="me"'),
        (LINKEDIN, "LinkedIn", ' rel="me"'),
    ]
    return "".join(
        f'<a href="{esc(href)}"{extra}>{esc(label)}</a>'
        for href, label, extra in items
    )


def footer(lang):
    base = home_href(lang)
    pages = [
        ("Work", "work"),
        ("Experience", "experience"),
        ("Patent", "patent"),
        ("Awards", "awards"),
    ]
    if lang == "ko":
        pages = [
            ("작업", "work"),
            ("경력", "experience"),
            ("특허", "patent"),
            ("수상", "awards"),
        ]
    directory = "".join(
        f'<a href="{base}#{anchor}">{esc(label)}</a>' for label, anchor in pages
    )
    contact = profile_links(lang)
    return f"""<footer class="colophon">
<div class="colophon-inner">
<nav class="dir" aria-label="Directory">{directory}</nav>
<nav class="dir" aria-label="Contact">{contact}</nav>
<hr class="dir-rule">
<p>© Jaewoo Choi</p>
</div>
</footer>"""


def script():
    return """<script>
(function () {
  var header = document.querySelector(".nav");
  var btn = document.querySelector(".nav-toggle");
  if (header && btn) {
    btn.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      document.body.classList.toggle("nav-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close" : "Menu");
    });
    header.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () {
        header.classList.remove("is-open");
        document.body.classList.remove("nav-open");
        btn.setAttribute("aria-expanded", "false");
        btn.setAttribute("aria-label", "Menu");
      });
    });
  }
  var videos = document.querySelectorAll("video");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  videos.forEach(function (v) {
    v.removeAttribute("autoplay");
    v.muted = true;
    v.pause();
    if (reduce) v.controls = true;
  });
  if (reduce || !("IntersectionObserver" in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var v = entry.target;
      if (entry.isIntersecting && entry.intersectionRatio >= 0.25) {
        var pending = v.play();
        if (pending && pending.catch) pending.catch(function () {});
      } else {
        v.pause();
      }
    });
  }, { threshold: [0, 0.25, 0.5, 0.75] });
  videos.forEach(function (v) { io.observe(v); });
})();
</script>"""


def video_html(key, lang):
    v = VIDEOS[key]
    cls = "portrait" if v["orient"] == "portrait" else "landscape"
    src = f"/assets/video/{v['file']}.mp4"
    poster = f"/assets/video/{v['file']}.jpg"
    return f"""<figure class="{cls}">
<video class="{cls}" width="{v['w']}" height="{v['h']}" muted loop playsinline preload="none" poster="{poster}" aria-label="{esc(v['label'][lang])}">
<source src="{src}" type="video/mp4">
<a href="{src}">{esc(UI[lang]['watch'])}</a>
</video>
<figcaption>{esc(v['cap'][lang])}</figcaption>
</figure>"""


def page(lang, title, desc, path, en_path, ko_path, body):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, title, desc, path, en_path, ko_path)}
<body>
<a class="skip" href="#content">{esc(UI[lang]['skip'])}</a>
{nav_html(lang)}
{body}
{footer(lang)}
{script()}
</body>
</html>
"""


def spec_table(rows, wide=False):
    lines = []
    for row in rows:
        rid = f' id="{esc(row[2])}"' if len(row) == 3 else ""
        label, value = row[0], row[1]
        lines.append(f'<tr{rid}><th scope="row">{label}</th><td>{value}</td></tr>')
    klass = "spec spec-wide" if wide else "spec"
    return f'<table class="{klass}">\n' + "\n".join(lines) + "\n</table>"


def hero_html(lang):
    project = next(p for p in PROJECTS if p["slug"] == "strawberry-cultivation")
    info = show(project, lang)
    href = project_href(lang, project["slug"])
    src = f"/assets/video/{VIDEOS['strawberry']['file']}.mp4"
    if lang == "en":
        first = "I build perception for robots that work outside the lab, on orchard platforms and factory arms."
        second = "Next, I want to connect what a robot sees with how it acts."
    else:
        first = "실험실 밖에서 일하는 로봇의 perception을 만듭니다. 과수원 플랫폼과 공장 팔입니다."
        second = "다음에는 로봇이 본 것과 행동을 잇고 싶습니다."
    return f"""<section class="hero" id="work">
{h("h1", "Jaewoo Choi")}
<div class="lede-wrap">
<p class="lede">{esc(first)}</p>
<p class="lede">{esc(second)}</p>
<p class="contact-row">{profile_links(lang)}</p>
</div>
{h_link("h2", info["pitch"], href, project["title"][lang])}
{video_html("strawberry", lang)}
<p class="links"><a class="pill" href="{src}">{esc(WATCH[lang])}</a></p>
</section>"""


def featured_html(project, lang, theme):
    info = show(project, lang)
    href = project_href(lang, project["slug"])
    src = f"/assets/video/{VIDEOS[project['video']]['file']}.mp4"
    paras = "\n".join(f"<p>{esc(part)}</p>" for part in info["notes"])
    return f"""<section class="band band-{theme}">
{h_link("h2", info["pitch"], href, project["title"][lang])}
{video_html(project["video"], lang)}
<div class="copy">
{paras}
</div>
<p class="links"><a class="pill" href="{src}">{esc(WATCH[lang])}</a><a class="pill pill-ghost" href="{href}" aria-label="{esc(project['title'][lang])}">{esc(info["nav"])}</a></p>
</section>"""


def tile_html(project, lang, ink):
    info = show(project, lang)
    group = next(g for g in GROUPS if g["id"] == project["group"])
    href = project_href(lang, project["slug"])
    klass = "tile tile-ink" if ink else "tile"
    return f"""<article class="{klass}">
{h_link("h3", info["pitch"], href, project["title"][lang])}
<div class="copy"><p>{esc(info["blurb"])}</p></div>
<p class="quiet">{esc(group["org"])}, {esc(group["when"][lang])}</p>
</article>"""


def evidence_html(lang):
    cad = project_href(lang, "cad-free-assembly")
    if lang != "en":
        return f'<section class="section section-paper" id="patent"></section>'
    rows = [
        (
            "Patent",
            f'Korean Patent 10-2694987. Registered Aug 2024. Applicant PLAIF. Co-inventor. Basis: <a href="{cad}">CAD-free auto assembly</a>.',
            "patent",
        ),
        ("UBC-OCEAN", "Bronze, team rank 83/1,326. Jan 2024."),
        (
            "Image Matching Challenge 2022",
            f'Silver, team rank 50/642. Jun 2022. <a href="{MATCH}">kaggle_image_matching2022</a>.',
        ),
        (
            "Happywhale",
            f'Whale and Dolphin Identification. Bronze, team rank 127/1,588. Apr 2022. <a href="{WHALE}">kaggle_happy_whale</a>.',
        ),
        (
            "Code",
            f'<a href="{GITHUB}" rel="me">GitHub</a>, <a href="{MATCH}">kaggle_image_matching2022</a>, <a href="{WHALE}">kaggle_happy_whale</a>.',
            "code",
        ),
    ]
    return f"""<section class="section section-paper" id="record">
{h("h2", "Patent, Kaggle, and code", 'class="section-title"')}
{spec_table(rows, wide=True)}
</section>"""


def research_html(lang):
    if lang == "en":
        parts = [
            "I work on open-vocabulary RGB-D segmentation, point-cloud and image fusion for obstacle mapping, 6D pose estimation, and imitation learning for manipulation.",
            "I tested this on deployed orchard robots.",
            "I also tested it on manipulation robots.",
        ]
        heading = "Research interests"
    else:
        parts = [
            "실제 로봇의 perception을 다룹니다. 주제는 open-vocabulary RGB-D segmentation, 장애물 매핑을 위한 point cloud와 image의 fusion, 6D pose estimation, manipulation을 위한 imitation learning입니다.",
            "배치된 과수원 로봇과 manipulation 로봇에서 이 작업을 개발하고 시험했습니다.",
        ]
        heading = UI[lang]["research"]
    body = "\n".join(f'<p class="measure">{esc(part)}</p>' for part in parts)
    return f"""<section class="section section-paper" id="research">
{h("h2", heading, 'class="section-title"')}
<div class="measure-wrap">
{body}
</div>
</section>"""


def experience_html(lang):
    rows = []
    for group in GROUPS:
        items = [p for p in PROJECTS if p["group"] == group["id"]]
        lis = "\n".join(
            f'<li><a href="{project_href(lang, p["slug"])}" aria-label="{esc(p["title"][lang])}">{esc(show(p, lang)["pitch"])}</a></li>'
            for p in items
        )
        rows.append(
            f"""<article class="exp-row">
<div>{h("h3", group["org"])}</div>
<div><p>{esc(group["role"][lang])}</p><p class="quiet">{esc(group["when"][lang])}</p></div>
<ul>
{lis}
</ul>
</article>"""
        )
    return f"""<section class="section" id="experience">
{h("h2", UI[lang]["experience"], 'class="section-title"')}
<div class="exp">
{''.join(rows)}
</div>
</section>"""


def education_html(lang):
    cad = project_href(lang, "cad-free-assembly")
    if lang == "en":
        rows = [
            ("School", "Seokyeong University"),
            ("Dates", "Mar 2016 to Aug 2022"),
            ("Place", "Seoul, South Korea"),
            (
                "Degree",
                "Bachelor of Engineering, Industrial Management Systems Engineering. Multidisciplinary major: Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies).",
            ),
            (
                "Patent",
                "Korean Patent 10-2694987. Registered Aug 2024. Applicant PLAIF. Co-inventor.",
            ),
            ("Title", esc(PATENT_TITLE)),
            (
                "Basis",
                f'<a href="{cad}">CAD-free auto assembly</a>',
            ),
        ]
        heading = "Education and patent"
    else:
        rows = [
            ("학교", "Seokyeong University"),
            ("기간", "2016년 3월부터 2022년 8월"),
            ("장소", "서울, 대한민국"),
            (
                "학위",
                "Bachelor of Engineering, Industrial Management Systems Engineering. 융합전공은 Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies)입니다.",
            ),
            ("특허", "한국 특허 10-2694987. 2024년 8월 등록. 출원인은 PLAIF입니다. 공동 발명자입니다."),
            ("명칭", f'<span lang="en">{esc(PATENT_TITLE)}</span>'),
            ("기반", f'<a href="{cad}">CAD-free auto assembly</a>'),
        ]
        heading = "학력과 특허"
    return f"""<section class="section section-paper" id="education">
{h("h2", heading, 'class="section-title"')}
{spec_table(rows, wide=True)}
</section>"""


def awards_html(lang):
    if lang == "en":
        rows = [
            ("UBC-OCEAN", "Bronze, team rank 83/1,326. Jan 2024."),
            (
                "Image Matching Challenge 2022",
                f'Silver, team rank 50/642. Jun 2022. <a href="{MATCH}">kaggle_image_matching2022</a>.',
            ),
            (
                "Happywhale",
                f'Whale and Dolphin Identification. Bronze, team rank 127/1,588. Apr 2022. <a href="{WHALE}">kaggle_happy_whale</a>.',
            ),
        ]
        heading = "Awards"
    else:
        rows = [
            ("UBC-OCEAN", "동메달, 팀 순위 83/1,326. 2024년 1월."),
            (
                "Image Matching Challenge 2022",
                f'은메달, 팀 순위 50/642. 2022년 6월. <a href="{MATCH}">kaggle_image_matching2022</a>.',
            ),
            (
                "Happywhale",
                f'Whale and Dolphin Identification. 동메달, 팀 순위 127/1,588. 2022년 4월. <a href="{WHALE}">kaggle_happy_whale</a>.',
            ),
        ]
        heading = "수상"
    return f"""<section class="section" id="awards">
{h("h2", heading, 'class="section-title"')}
{spec_table(rows, wide=True)}
</section>"""


def home_page(lang):
    path = home_href(lang)
    en_path, ko_path = "/", "/ko/"
    if lang == "en":
        title = "Jaewoo Choi, Senior AI Researcher"
        desc = "I build perception for robots that work outside the lab, on orchard platforms and factory arms."
    else:
        title = "Jaewoo Choi, Senior AI Researcher"
        desc = "실험실 밖에서 일하는 로봇의 perception."
    featured_slugs = ["cad-free-assembly", "bin-picking"]
    themes = {"cad-free-assembly": "ink", "bin-picking": "white"}
    bands = []
    for slug in featured_slugs:
        project = next(p for p in PROJECTS if p["slug"] == slug)
        bands.append(featured_html(project, lang, themes[slug]))
    strawberry = next(p for p in PROJECTS if p["slug"] == "strawberry-cultivation")
    sinfo = show(strawberry, lang)
    snotes = "\n".join(f"<p>{esc(part)}</p>" for part in sinfo["notes"])
    srows = [(esc(label), esc(value)) for label, value in sinfo["results"]]
    notes = f"""<section class="band band-white" id="strawberry-notes">
<div class="copy">
{snotes}
</div>
{spec_table(srows)}
</section>"""
    tiles = []
    n = 0
    skip = {"strawberry-cultivation", *featured_slugs}
    for project in PROJECTS:
        if project["slug"] in skip:
            continue
        tiles.append(tile_html(project, lang, ink=(n % 2 == 1)))
        n += 1
    body = f"""<main id="content">
<div class="page">
{hero_html(lang)}
{notes}
{evidence_html(lang)}
{''.join(bands)}
<section class="tile-grid" aria-label="{esc(UI[lang]['other'])}">
{''.join(tiles)}
</section>
{research_html(lang)}
{experience_html(lang)}
{education_html(lang)}
{awards_html(lang)}
</div>
</main>"""
    return page(lang, title, desc, path, en_path, ko_path, body)


def approach_paragraphs(project, lang):
    found = []
    for heading, body in project["sections"][lang]:
        if heading in ("Problem", "Approach", "문제", "방법"):
            found.extend(re.findall(r"<p>(.*?)</p>", body, flags=re.S))
    return found


def approach_html(paragraphs):
    if not paragraphs:
        return ""
    limit = 3
    if len(paragraphs) <= limit:
        groups = [[p] for p in paragraphs]
    else:
        groups = [[p] for p in paragraphs[: limit - 1]]
        groups.append(paragraphs[limit - 1 :])
    blocks = []
    for group in groups:
        inner = "\n".join(f"<p>{part}</p>" for part in group)
        blocks.append(f'<div class="approach-block">\n{inner}\n</div>')
    return "\n".join(blocks)


def local_nav(project, lang, anchors):
    info = show(project, lang)
    base = project_href(lang, project["slug"])
    labels = {
        "en": {"overview": "Overview", "approach": "Approach", "results": "Results", "stack": "Stack"},
        "ko": {"overview": "개요", "approach": "방법", "results": "결과", "stack": "기술"},
    }[lang]
    links = "\n".join(
        f'<a href="{base}#{key}">{esc(labels[key])}</a>' for key in anchors
    )
    name = esc(info["nav"])
    return f"""<div class="local">
<div class="local-bar">
<a class="local-name" href="{base}#overview">{name}</a>
<nav aria-label="{name}">
{links}
</nav>
</div>
</div>"""


def project_page(project, lang):
    ui = UI[lang]
    path = project_href(lang, project["slug"])
    en_path = project_href("en", project["slug"])
    ko_path = project_href("ko", project["slug"])
    info = show(project, lang)
    title = f"{plain_title(project['title'][lang])}, Jaewoo Choi"
    desc = project["desc"][lang]
    group = next(g for g in GROUPS if g["id"] == project["group"])
    anchors = ["overview", "approach"]
    if info["results"]:
        anchors.append("results")
    if info["stack"]:
        anchors.append("stack")
    if project["video"]:
        src = f"/assets/video/{VIDEOS[project['video']]['file']}.mp4"
        media = f'<div class="project-media">\n{video_html(project["video"], lang)}\n</div>'
        watch = f'<p class="links"><a class="pill" href="{src}">{esc(WATCH[lang])}</a></p>'
    else:
        media = f"<!-- {ui['media_comment']} -->"
        watch = ""
    kicker = f"{group['org']} · {group['role'][lang]} · {group['when'][lang]}"
    results = ""
    if info["results"]:
        label = "Results" if lang == "en" else "결과"
        rows = []
        for label_cell, value in info["results"]:
            if label_cell == "Patent":
                cell = f'<a href="{home_href(lang)}#patent">Korean Patent 10-2694987</a>'
            else:
                cell = esc(value)
            rows.append((esc(label_cell), cell))
        results = f"""<section class="section section-paper" id="results">
<div class="prose">
{h("h2", label)}
{spec_table(rows)}
</div>
</section>"""
    stack = ""
    if info["stack"]:
        label = "Stack" if lang == "en" else "기술"
        items = "\n".join(f"<li>{esc(part)}</li>" for part in info["stack"])
        stack = f"""<section class="section" id="stack">
<div class="prose">
{h("h2", label)}
<ul class="tech">
{items}
</ul>
</div>
</section>"""
    back = home_href(lang) + "#work"
    body = f"""<main id="content">
{local_nav(project, lang, anchors)}
<header class="project-hero" id="overview">
<p class="kicker">{esc(kicker)}</p>
{h("h1", info["pitch"])}
<p class="dek">{esc(info["dek"])}</p>
{watch}
</header>
{media}
<section class="section" id="approach">
<div class="prose">
{h("h2", "Approach" if lang == "en" else "방법")}
{approach_html(approach_paragraphs(project, lang))}
</div>
</section>
{results}
{stack}
<section class="section section-paper">
{pager_html(project, lang)}
<p class="back"><a href="{back}">{esc(ui["work"])}</a></p>
</section>
</main>"""
    return page(lang, title, desc, path, en_path, ko_path, body)


def pager_html(project, lang):
    ui = UI[lang]
    idx = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    links = []
    if idx > 0:
        prev = PROJECTS[idx - 1]
        links.append(
            f'<a class="pager-prev" href="{project_href(lang, prev["slug"])}">'
            f'<span class="pager-label">{esc(ui["prev"])}</span>'
            f'<span class="pager-name">{esc(show(prev, lang)["pitch"])}</span></a>'
        )
    else:
        links.append("<span></span>")
    if idx + 1 < len(PROJECTS):
        nxt = PROJECTS[idx + 1]
        links.append(
            f'<a class="pager-next" href="{project_href(lang, nxt["slug"])}">'
            f'<span class="pager-label">{esc(ui["next"])}</span>'
            f'<span class="pager-name">{esc(show(nxt, lang)["pitch"])}</span></a>'
        )
    return (
        f'<nav class="pager" aria-label="{esc(ui["pager"])}">\n'
        + "\n".join(links)
        + "\n</nav>"
    )


def not_found_page():
    ui = UI["en"]
    ko_note = ""
    if PUBLISH_KO:
        ui_ko = UI["ko"]
        ko_note = f'<p class="lede" lang="ko">{esc(ui_ko["missing_body"])}</p>\n'
    body = f"""<main id="content">
<section class="band band-white">
{h("h1", ui["missing"])}
<p class="dek">{esc(ui["missing_body"])}</p>
{ko_note}<p class="links"><a class="pill" href="/">Jaewoo Choi</a></p>
</section>
</main>"""
    return page("en", ui["missing"], ui["missing_body"], "/404.html", "/", "/ko/", body)


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
    text = re.sub(r"\bSAM\s+3\b", "SAM\u00a03", text)
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
