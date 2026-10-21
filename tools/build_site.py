#!/usr/bin/env python3
"""Write the static HTML for the personal site. Facts come from the CV."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
            "en": "CAD-free auto assembly on a UR arm",
            "ko": "UR arm의 CAD-free auto assembly",
        },
        "cap": {
            "en": "Silent. UR arm with a gripper and wrist camera, assembling a part on a fixture.",
            "ko": "무음. Gripper와 wrist camera가 달린 UR arm이 fixture 위 부품을 조립합니다.",
        },
    },
    "bin": {
        "file": "bin-picking",
        "orient": "landscape",
        "w": 1280,
        "h": 720,
        "label": {
            "en": "CAD-based bin picking",
            "ko": "CAD-based bin picking",
        },
        "cap": {
            "en": "Silent. A ring-scan close-up, then a Doosan cobot picking, then a green-bin close-up.",
            "ko": "무음. 세 장면입니다. Ring-scan close-up, Doosan cobot picking, green-bin close-up.",
        },
    },
    "strawberry": {
        "file": "strawberry-ces2025",
        "orient": "portrait",
        "w": 540,
        "h": 960,
        "label": {
            "en": "Flower thinning at the CES 2025 booth",
            "ko": "CES 2025 부스의 flower thinning",
        },
        "cap": {
            "en": "Silent. Flower thinning at the CES 2025 booth.",
            "ko": "무음. CES 2025 부스에서 flower thinning을 합니다.",
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
            "en": "Language-Distilled Open-Vocabulary Instance Segmentation for Orchard Robots",
            "ko": "과수원 로봇용 Language-Distilled Open-Vocabulary Instance Segmentation",
        },
        "line": {
            "en": "Open-vocabulary instance segmenter for the RT100 orchard platform. Language-teacher supervision is used in training only, so inference cost does not go up.",
            "ko": "RT100용 open-vocabulary instance segmenter입니다. 학습에만 language-teacher supervision을 써서 추론 비용은 그대로 둡니다.",
        },
        "tools": {
            "en": "Open-vocabulary segmentation, DETR, DINOv3",
            "ko": "Open-vocabulary segmentation, DETR, DINOv3",
        },
        "desc": {
            "en": "Open-vocabulary instance segmenter for the RT100 orchard platform, trained with a language teacher and no added inference cost.",
            "ko": "RT100용 open-vocabulary instance segmenter. 학습에 language teacher를 쓰고 추론 비용은 그대로입니다.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "RT100, an autonomous orchard platform, needs instance masks for objects outside a fixed label set. A language teacher is available while training. The deployed model does not add inference cost.",
                )),
                ("Approach", P(
                    "I adapted a DETR-based segmenter for RT100. The backbone is a frozen DINOv3. A lightweight text encoder trains. A multi-scale feature projector feeds a three-layer decoder. The decoder predicts masks from dot products between queries and refined spatial features.",
                    "During training only, object queries and pooled image features are matched to precomputed language-teacher embeddings of object and image descriptions. Semantically related negatives are reweighted so they are not pushed apart.",
                )),
                ("Results", P(
                    "Instance masks feed point-cloud projection and occupancy-grid mapping. The model is in the production RT100 perception pipeline.",
                )),
                ("Stack", P(
                    "DETR, frozen DINOv3, a trainable lightweight text encoder, a multi-scale feature projector, a three-layer decoder.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "RT100 자율 과수원 플랫폼은 고정된 label set 밖의 물체에도 instance mask가 필요합니다. 학습 중에는 language teacher를 쓸 수 있고, 배포 모델의 추론 비용은 늘리지 않습니다.",
                )),
                ("방법", P(
                    "구조는 DETR 기반입니다. Backbone은 frozen DINOv3이고, lightweight text encoder는 학습합니다. Multi-scale feature projector 뒤에 three-layer decoder가 있고, decoder는 query와 refined spatial feature의 dot product로 mask를 예측합니다.",
                    "학습 중에만 object query와 pooled image feature를 language-teacher embedding에 맞춥니다. Embedding은 물체 설명과 이미지 설명입니다. 의미가 가까운 negative는 서로 밀리지 않게 가중치를 조정합니다.",
                )),
                ("결과", P(
                    "Instance mask는 point cloud projection과 occupancy grid mapping으로 넘어갑니다. 모델은 production RT100 perception pipeline에 들어가 있습니다.",
                )),
                ("기술", P(
                    "DETR, frozen DINOv3, lightweight text encoder, multi-scale feature projector, three-layer decoder.",
                )),
            ],
        },
    },
    {
        "slug": "orchard-obstacle-mapping",
        "group": "daedong",
        "video": None,
        "title": {
            "en": "Open-Vocabulary 3D Obstacle Perception and Occupancy Mapping for Autonomous Orchard Robots",
            "ko": "자율 과수원 로봇의 Open-Vocabulary 3D Obstacle Perception과 Occupancy Mapping",
        },
        "line": {
            "en": "Open-set obstacles are segmented and written into an occupancy grid. The pipeline runs on production RT100 robots with TensorRT on Jetson Nano.",
            "ko": "과수원 로봇은 open-set 장애물을 인식해 occupancy grid로 만들고, production RT100에서 TensorRT와 Jetson Nano로 돌립니다.",
        },
        "tools": {
            "en": "3D perception, TensorRT, Jetson Nano",
            "ko": "3D perception, TensorRT, Jetson Nano",
        },
        "desc": {
            "en": "Open-set obstacle perception for orchard robots, mapped to an occupancy grid and deployed on RT100 with TensorRT on Jetson Nano.",
            "ko": "과수원 로봇의 open-set 장애물 perception. Occupancy grid로 만들고 RT100에 TensorRT, Jetson Nano로 배포했습니다.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "Orchard robots must recognize open-set obstacles and turn them into a navigable map under embedded compute limits.",
                )),
                ("Approach", P(
                    "I pre-trained the adapter, neck, and segmentation head on multiple datasets over frozen DINOv2 and SigLIP2 encoders, with region-text alignment for instance and semantic segmentation.",
                    "The model takes text prompts at inference and can run with a fixed vocabulary. I adapted it to the orchard domain.",
                    "Point-cloud voxel centers are projected into the image and tied to instance masks. Virtual voxels are added from valid anchor depths. Obstacles go into an occupancy grid with decay, hysteresis, and cost inflation.",
                )),
                ("Results", P(
                    "The complete pipeline is deployed on production RT100 platforms and optimized with TensorRT on Jetson Nano.",
                )),
                ("Stack", P(
                    "DINOv2, SigLIP2, TensorRT, Jetson Nano.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "과수원 로봇은 open-set 장애물을 인식하고, embedded compute 한계 안에서 주행에 쓸 지도로 바꿔야 합니다. Frozen DINOv2와 SigLIP2 encoder 위에 adapter, neck, segmentation head를 여러 데이터셋으로 pre-train했습니다. Instance segmentation과 semantic segmentation에 region-text alignment를 썼습니다. Text-prompt inference와 fixed-vocabulary conversion이 있고, 과수원 도메인에 맞췄습니다.",
                )),
                ("방법", P(
                    "Point cloud voxel center를 이미지에 projection해서 instance mask와 연결합니다. 유효한 anchor depth로 virtual voxel을 더한 뒤, 장애물은 decay, hysteresis, cost inflation이 있는 occupancy grid에 기록합니다. 전체 pipeline은 production RT100에 올라가 있습니다. Jetson Nano에서 TensorRT로 최적화했습니다.",
                )),
                ("기술", P(
                    "DINOv2, SigLIP2, TensorRT, Jetson Nano.",
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
                    "Manual annotation cost limits the supply of segmentation and region-grounded vision-language training data. I built a video auto-labeling pipeline. Point prompts and mask corrections become tracked masks with consistent IDs across frames. Image and video inputs share TensorRT engines, so the same computation is not duplicated.",
                )),
                ("Approach", P(
                    "Qwen-series vision-language models generate region-grounded object descriptions and check them. Uncertain cases go to a second review. Verified descriptions are linked to the instance annotations. I set the label taxonomy and the annotation guidelines, and built COCO-format training datasets.",
                )),
                ("Results", P(
                    "Per-image labeling cost was about USD 1.05. It fell to about USD 0.036, a 96.6% reduction.",
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
                    "Qwen 계열 vision-language model이 region-grounded object description을 만들고 검증합니다. 불확실한 경우는 두 번째 검토로 보내고, 검증된 description은 instance annotation에 연결합니다.",
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
            "en": "Diffusion Policy trained on UMI demonstrations. In a fixed lab, across 1,000 trials, success was 93.8% for transplanting, 87.5% for flower thinning, and 65% for runner handling. Exhibited at CES 2025.",
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
                    "Three strawberry cultivation tasks were learned from human demonstrations: transplanting, flower thinning, and runner handling.",
                )),
                ("Approach", P(
                    "Demonstrations were collected with a Universal Manipulation Interface (UMI). I led the data pipeline and the policy training for all three tasks.",
                    "I collected GoPro RGB and IMU data, calibrated the camera to the IMU, and turned ORB-SLAM3 visual-inertial SLAM trajectories into training sets.",
                    "Diffusion Policy was trained with RGB features and robot state as global conditioning. I compared U-Net and ViT configurations.",
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
                    "I prototyped a two-view RGB baseline first: learned feature matching between a reference image and a target image, USAC essential-matrix estimation, relative pose recovery, and triangulation.",
                    "In the final pipeline, LightGlue matches the live 2D image to a stored reference RGB-D capture, so each match carries depth. Matches with no depth are removed.",
                    'solvePnP and RANSAC estimate the camera pose from the 3D-2D matches. That pose is chained with the hand-eye calibration and the stored reference pose. The result is the target 6D tool pose. Task success was 93% across 1,000 in-house trials. This work is the basis of <a href="/#patent">Korean Patent 10-2694987</a>.',
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
            "en": "6D pose, bin picking, Mask R-CNN",
            "ko": "6D pose, bin picking, Mask R-CNN",
        },
        "desc": {
            "en": "Picking poses from RGB-D and CAD geometry. 89% task success in 1,000 in-house, fixed-environment trials on five object types.",
            "ko": "RGB-D와 CAD로 picking pose. 사내 고정 환경 1,000회, object type 5종, task success 89%.",
        },
        "sections": {
            "en": [
                ("Problem", P(
                    "Estimate picking poses from RGB-D images of a bin for objects with known CAD geometry.",
                )),
                ("Approach", P(
                    'I trained Mask R-CNN (ResNet-101) with separate "unoccluded" and "hole" classes. Hole masks are subtracted from object masks. The remaining instance masks segment the point cloud.',
                    "Visible-surface CAD templates for each pick pose are built by hidden-point removal, then fit to the segmented points with PCA initialization and point-to-point ICP.",
                    "Each fit is checked model-to-scene and scene-to-model. Poses are filtered by registration fitness, inlier RMSE, and a combined score. Candidates are ranked. Poses are transformed into the robot base with the camera extrinsics.",
                )),
                ("Results", P(
                    "Task success was 89% in 1,000 in-house, fixed-environment trials, moving five object types into an empty container.",
                )),
                ("Stack", P(
                    "Mask R-CNN, ResNet-101, PCA, point-to-point ICP.",
                )),
            ],
            "ko": [
                ("문제", P(
                    "CAD geometry를 아는 물체는 bin의 RGB-D image에서 picking pose를 추정합니다.",
                )),
                ("방법", P(
                    'Mask R-CNN(ResNet-101)을 class "unoccluded"와 "hole"로 나눠 학습했습니다. Object mask에서 hole mask를 빼고, 남은 instance mask로 point cloud를 나눕니다.',
                    "각 pick pose의 visible-surface CAD template은 hidden-point removal로 만들고, PCA initialization 다음 point-to-point ICP로 segmented point에 맞춥니다. Fit은 model-to-scene과 scene-to-model 양쪽을 보고, registration fitness, inlier RMSE, combined score로 pose를 거릅니다. Candidate를 순위화한 뒤 camera extrinsic으로 pose를 robot base에 옮깁니다. 빈 용기로 object type 5종을 옮기는 사내 고정 환경 시험 1,000회에서 task success 89%를 기록했습니다.",
                )),
                ("기술", P(
                    "Mask R-CNN, ResNet-101, PCA, point-to-point ICP.",
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
            "en": "A ROS action server runs capture, segmentation, and pose estimation per request, and returns robot-base and camera-frame poses. Eye-to-hand calibration tools sit beside it.",
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
                    "A caller needs the object pose in the robot base frame and in the camera frame. The camera also has to be calibrated to the robot.",
                )),
                ("Approach", P(
                    "I wrote a ROS action server that runs capture, segmentation, and pose estimation per request. It returns robot-base and camera-frame poses with matching scores. A configuration file selects the camera (Zivid, RealSense, or recorded data), the model, and the pipeline.",
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
            "en": "Object detection locates the plate. OCR reads the letters and digits.",
            "ko": "Object detection으로 번호판 위치를 찾습니다. OCR로 문자와 숫자를 읽습니다.",
        },
        "tools": {
            "en": "Detection, OCR",
            "ko": "Detection, OCR",
        },
        "desc": {
            "en": "License plate pipeline: object detection locates the plate, OCR reads the letters and digits.",
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
    en_cur = ' aria-current="page"' if lang == "en" else ""
    ko_cur = ' aria-current="page"' if lang == "ko" else ""
    return (
        f'<p class="langs">'
        f'<a href="{esc(en_path)}" hreflang="en" lang="en"{en_cur}>EN</a>'
        f'<span class="sep">|</span>'
        f'<a href="{esc(ko_path)}" hreflang="ko" lang="ko"{ko_cur}>한국어</a>'
        f"</p>"
    )


def nav_html(lang):
    base = home_href(lang)
    links = []
    for label, anchor, wide in NAV[lang]:
        cls = ' class="nav-wide"' if wide else ""
        links.append(f'<a href="{base}#{anchor}"{cls}>{esc(label)}</a>')
    ui = UI[lang]
    links.append(f'<!-- {ui["cv_comment"]} -->\n<a href="/cv.pdf">{esc(ui["cv"])}</a>')
    return "<nav>\n" + "\n".join(links) + "\n</nav>"


def head(lang, title, desc, path, en_path, ko_path):
    canonical = abs_url(path)
    kr = ""
    if lang == "ko":
        kr = '<link rel="preload" href="/assets/fonts/ibm-plex-sans-kr-400.woff2" as="font" type="font/woff2" crossorigin>\n'
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Jaewoo Choi">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#eef1f3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141a1e" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(abs_url(en_path))}">
<link rel="alternate" hreflang="ko" href="{esc(abs_url(ko_path))}">
<link rel="alternate" hreflang="x-default" href="{esc(abs_url(en_path))}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400.woff2" as="font" type="font/woff2" crossorigin>
{kr}<link rel="stylesheet" href="/assets/css/site.css">
</head>"""


def footer(lang):
    ui = UI[lang]
    return f"""<footer class="colophon">
<p>{esc(ui["updated"])}</p>
{contact_html()}
</footer>"""


def script():
    return """<script>
(function () {
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


def mast(lang, en_path, ko_path, show_name):
    name = f'<a class="name" href="{home_href(lang)}">Jaewoo Choi</a>\n' if show_name else ""
    klass = "mast mast-named" if show_name else "mast"
    return f"""<header class="{klass}">
{name}{nav_html(lang)}
{langs_html(lang, en_path, ko_path)}
</header>"""


def video_html(key, lang, caption=True):
    v = VIDEOS[key]
    portrait = v["orient"] == "portrait"
    cls = "portrait" if portrait else "landscape"
    fig = "portrait" if portrait else "landscape"
    src = f"/assets/video/{v['file']}.mp4"
    poster = f"/assets/video/{v['file']}.jpg"
    cap = f"\n<figcaption>{v['cap'][lang]}</figcaption>" if caption else ""
    return f"""<figure class="{fig}">
<video class="{cls}" width="{v['w']}" height="{v['h']}" muted loop playsinline preload="none" poster="{poster}" aria-label="{esc(v['label'][lang])}">
<source src="{src}" type="video/mp4">
<a href="{src}">{esc(UI[lang]['watch'])}</a>
</video>{cap}
</figure>"""


def slot_html(lang):
    return f"<!-- {UI[lang]['media_comment']} -->"


def entry_html(project, lang):
    href = project_href(lang, project["slug"])
    title = esc(project["title"][lang])
    if project["video"]:
        klass = "entry has-video"
        media = "\n" + video_html(project["video"], lang)
    else:
        klass = "entry"
        media = "\n" + slot_html(lang)
    return f"""<article class="{klass}">
<h3><a href="{href}">{title}</a></h3>
<p>{project['line'][lang]}</p>
<p class="tools">{project['tools'][lang]}</p>{media}
</article>"""


FEATURED = [
    {
        "slug": "strawberry-cultivation",
        "tall": True,
        "result": {
            "en": "Fixed lab, 1,000 trials: 93.8% transplanting, 87.5% flower thinning, 65% runner handling.",
            "ko": "고정 실험실, 1,000회: transplanting 93.8%, flower thinning 87.5%, runner handling 65%.",
        },
        "did": {
            "en": "I led the data pipeline and the policy training on UMI demonstrations. Exhibited at CES 2025.",
            "ko": "세 작업의 data pipeline과 policy 학습을 맡았습니다. CES 2025에 전시했습니다.",
        },
    },
    {
        "slug": "cad-free-assembly",
        "tall": False,
        "result": {
            "en": "93% task success across 1,000 in-house trials. Basis of Korean Patent 10-2694987.",
            "ko": '사내 1,000회 시험, task success 93%. <span class="nobr">한국 특허 10-2694987</span>의 기반.',
        },
        "did": {
            "en": "6D tool poses for assembly from a 2D camera, with no CAD model of the part.",
            "ko": "부품 CAD 없이 2D camera로 조립용 6D tool pose를 구합니다.",
        },
    },
    {
        "slug": "bin-picking",
        "tall": False,
        "result": {
            "en": "89% task success across 1,000 in-house trials. Fixed environment, five object types moved into an empty container.",
            "ko": "사내 고정 환경, object type 5종을 빈 용기로 옮긴 1,000회. task success 89%.",
        },
        "did": {
            "en": "Picking poses from RGB-D images and known CAD geometry.",
            "ko": "RGB-D와 CAD geometry로 picking pose를 구합니다.",
        },
    },
]


def feature_html(spec, lang):
    ui = UI[lang]
    project = next(p for p in PROJECTS if p["slug"] == spec["slug"])
    href = project_href(lang, project["slug"])
    tall = " feature-tall" if spec["tall"] else ""
    return f"""<article class="feature{tall}">
{video_html(project["video"], lang, caption=False)}
<div class="feature-copy">
<h3><a href="{href}">{esc(project["title"][lang])}</a></h3>
<p class="result">{spec["result"][lang]}</p>
<p class="did">{spec["did"][lang]}</p>
<p class="more"><a href="{href}">{esc(ui["details"])}</a></p>
</div>
</article>"""


def roster_html(lang):
    featured = {spec["slug"] for spec in FEATURED}
    items = []
    for project in PROJECTS:
        if project["slug"] in featured:
            continue
        group = next(g for g in GROUPS if g["id"] == project["group"])
        href = project_href(lang, project["slug"])
        items.append(
            f"""<li>
<a href="{href}">
<span class="roster-title">{esc(project["title"][lang])}</span>
<span class="roster-when">{esc(group["org"])}, {esc(group["when"][lang])}</span>
<span class="roster-sum">{esc(project["desc"][lang])}</span>
</a>
</li>"""
        )
    return '<ul class="roster">\n' + "\n".join(items) + "\n</ul>"


def home_page(lang):
    ui = UI[lang]
    path = home_href(lang)
    en_path, ko_path = "/", "/ko/"
    if lang == "en":
        title = "Jaewoo Choi, Senior AI Researcher"
        desc = "Senior AI Researcher at Daedong AILab. Open-vocabulary perception, 6D pose, and imitation learning for orchard and manipulation robots."
        focus = """<p class="focus">Open-vocabulary perception, 6D pose, and imitation learning for orchard and manipulation robots.</p>"""
        research = """<p class="measure">I work on perception for real robots: open-vocabulary RGB-D segmentation, point-cloud and image fusion for obstacle mapping, 6D pose estimation, and imitation learning for manipulation. I have developed and tested this work on deployed orchard robots and on manipulation robots. I want to extend it toward vision-language-action models that connect what a robot sees with how it acts.</p>"""
        edu = """<article>
<h3>Seokyeong University</h3>
<p class="when">Mar 2016 to Aug 2022</p>
<p>Seoul, South Korea</p>
<p>Bachelor of Engineering, Industrial Management Systems Engineering. Multidisciplinary major: Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies).</p>
</article>"""
        patent = f"""<article>
<h3>Korean Patent 10-2694987</h3>
<p class="when">Registered Aug 2024</p>
<p>Applicant: PLAIF. Co-inventor.</p>
<p class="patent-title">Pose estimating device and method using artificial intelligence to estimate pose of robot's end effector for object and robot control system including the same.</p>
<p>The <a href="{project_href('en', 'cad-free-assembly')}">CAD-free auto assembly</a> work is the basis of this patent.</p>
</article>"""
        awards = f"""<article>
<h3>Kaggle UBC-OCEAN</h3>
<p class="when">Jan 2024</p>
<p>Bronze medal, team rank 83/1,326.</p>
</article>
<article>
<h3>Kaggle Image Matching Challenge 2022</h3>
<p class="when">Jun 2022</p>
<p>Silver medal, team rank 50/642.</p>
<p><a href="{MATCH}">kaggle_image_matching2022</a></p>
</article>
<article>
<h3>Kaggle Happywhale</h3>
<p class="when">Apr 2022</p>
<p>Whale and Dolphin Identification. Bronze medal, team rank 127/1,588.</p>
<p><a href="{WHALE}">kaggle_happy_whale</a></p>
</article>"""
    else:
        title = "Jaewoo Choi, Senior AI Researcher"
        desc = "Daedong AILab Senior AI Researcher. 과수원 로봇과 manipulation 로봇의 open-vocabulary perception, 6D pose, imitation learning."
        focus = """<p class="focus">과수원 로봇과 manipulation 로봇의 open-vocabulary perception, 6D pose, imitation learning을 연구합니다.</p>"""
        research = """<p class="measure">실제 로봇의 perception을 다룹니다. 주제는 open-vocabulary RGB-D segmentation, 장애물 매핑을 위한 point cloud와 image의 fusion, 6D pose estimation, manipulation을 위한 imitation learning입니다. 배치된 과수원 로봇과 manipulation 로봇에서 이 작업을 개발하고 시험했습니다. 로봇이 본 것과 행동을 잇는 vision-language-action model로 확장하고 싶습니다.</p>"""
        edu = """<article>
<h3>Seokyeong University</h3>
<p class="when">2016년 3월부터 2022년 8월</p>
<p>서울, 대한민국</p>
<p>Bachelor of Engineering, Industrial Management Systems Engineering. 융합전공은 Bigdata Business Intelligence (Bachelor of Multidisciplinary Studies)입니다.</p>
</article>"""
        patent = f"""<article>
<h3>한국 특허 10-2694987</h3>
<p class="when">2024년 8월 등록</p>
<p>출원인은 PLAIF입니다. 공동 발명자입니다.</p>
<p class="patent-title" lang="en">Pose estimating device and method using artificial intelligence to estimate pose of robot's end effector for object and robot control system including the same.</p>
<p><a href="{project_href('ko', 'cad-free-assembly')}">CAD-free auto assembly</a>가 이 특허의 기반입니다.</p>
</article>"""
        awards = f"""<article>
<h3>Kaggle UBC-OCEAN</h3>
<p class="when">2024년 1월</p>
<p>동메달, 팀 순위 83/1,326.</p>
</article>
<article>
<h3>Kaggle Image Matching Challenge 2022</h3>
<p class="when">2022년 6월</p>
<p>은메달, 팀 순위 50/642.</p>
<p><a href="{MATCH}">kaggle_image_matching2022</a></p>
</article>
<article>
<h3>Kaggle Happywhale</h3>
<p class="when">2022년 4월</p>
<p>Whale and Dolphin Identification. 동메달, 팀 순위 127/1,588.</p>
<p><a href="{WHALE}">kaggle_happy_whale</a></p>
</article>"""

    features = "\n".join(feature_html(spec, lang) for spec in FEATURED)
    roster = roster_html(lang)

    exp_blocks = []
    for group in GROUPS:
        items = [p for p in PROJECTS if p["group"] == group["id"]]
        lis = "\n".join(
            f'<li><a href="{project_href(lang, p["slug"])}">{esc(p["title"][lang])}</a></li>'
            for p in items
        )
        exp_blocks.append(
            f"""<article>
<h3>{esc(group['org'])}</h3>
<p class="when">{esc(group['when'][lang])}</p>
<p>{esc(group['role'][lang])}</p>
<ul class="role-projects">
{lis}
</ul>
</article>"""
        )

    role = "Senior AI Researcher, Daedong AILab"
    loc = "Seoul, South Korea" if lang == "en" else "서울, 대한민국"
    doc = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, title, desc, path, en_path, ko_path)}
<body>
<a class="skip" href="#content">{esc(ui['skip'])}</a>
<div class="wrap">
{mast(lang, en_path, ko_path, False)}
<main id="content">
<header class="intro">
<h1>Jaewoo Choi</h1>
<p class="role">{esc(role)}</p>
<p class="loc">{esc(loc)}</p>
{focus}
{contact_html()}
</header>
<section id="projects">
<h2>{esc(ui['work'])}</h2>
{features}
</section>
<section id="other">
<h2>{esc(ui['other'])}</h2>
{roster}
</section>
<section id="research">
<h2>{esc(ui['research'])}</h2>
{research}
</section>
<section id="experience">
<h2>{esc(ui['experience'])}</h2>
<div class="cv">
{''.join(exp_blocks)}
</div>
</section>
<section id="education">
<h2>{esc(ui['education'])}</h2>
<div class="cv">
{edu}
</div>
</section>
<section id="patent">
<h2>{esc(ui['patent'])}</h2>
<div class="cv">
{patent}
</div>
</section>
<section id="awards">
<h2>{esc(ui['awards'])}</h2>
<div class="cv">
{awards}
</div>
</section>
</main>
{footer(lang)}
</div>
{script()}
</body>
</html>
"""
    return doc


def sections_html(pairs):
    parts = []
    for heading, body in pairs:
        if heading in ("Stack", "기술"):
            body = body.replace("<p>", '<p class="stack">')
        parts.append(f"<h2>{esc(heading)}</h2>\n{body}")
    return "\n".join(parts)


def pager_html(project, lang):
    ui = UI[lang]
    idx = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    links = []
    if idx > 0:
        prev = PROJECTS[idx - 1]
        links.append(
            f'<a class="pager-prev" href="{project_href(lang, prev["slug"])}">'
            f'<span class="pager-label">{esc(ui["prev"])}</span> {esc(prev["title"][lang])}</a>'
        )
    if idx + 1 < len(PROJECTS):
        nxt = PROJECTS[idx + 1]
        links.append(
            f'<a class="pager-next" href="{project_href(lang, nxt["slug"])}">'
            f'<span class="pager-label">{esc(ui["next"])}</span> {esc(nxt["title"][lang])}</a>'
        )
    if not links:
        return ""
    return (
        f'<nav class="pager" aria-label="{esc(ui["pager"])}">\n'
        + "\n".join(links)
        + "\n</nav>"
    )


def project_page(project, lang):
    ui = UI[lang]
    path = project_href(lang, project["slug"])
    en_path = project_href("en", project["slug"])
    ko_path = project_href("ko", project["slug"])
    title = f"{project['title'][lang]}, Jaewoo Choi"
    desc = project["desc"][lang]
    group = next(g for g in GROUPS if g["id"] == project["group"])
    if project["video"]:
        media = video_html(project["video"], lang)
    else:
        media = slot_html(lang)
    sections = sections_html(project["sections"][lang])
    back = home_href(lang) + "#projects"
    doc = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, title, desc, path, en_path, ko_path)}
<body>
<a class="skip" href="#content">{esc(ui['skip'])}</a>
<div class="wrap">
{mast(lang, en_path, ko_path, True)}
<main id="content" class="project">
<p class="kicker">{esc(group['org'])}, {esc(group['role'][lang])}, {esc(group['when'][lang])}</p>
<h1>{esc(project['title'][lang])}</h1>
<p class="dek">{project['line'][lang]}</p>
{media}
<div class="prose">
{sections}
</div>
{pager_html(project, lang)}
<p class="back"><a href="{back}">{esc(ui['projects_back'])}</a></p>
</main>
{footer(lang)}
</div>
{script()}
</body>
</html>
"""
    return doc


def not_found_page():
    ui = UI["en"]
    ui_ko = UI["ko"]
    return f"""<!DOCTYPE html>
<html lang="en">
{head("en", ui["missing"], ui["missing_body"], "/404.html", "/", "/ko/")}
<body>
<a class="skip" href="#content">{esc(ui['skip'])}</a>
<div class="wrap">
{mast("en", "/", "/ko/", True)}
<main id="content">
<h1>{esc(ui['missing'])}</h1>
<p>{esc(ui['missing_body'])}</p>
<p><a href="/">Jaewoo Choi</a></p>
<p lang="ko">{esc(ui_ko['missing_body'])} <a href="/ko/" hreflang="ko" lang="ko">한국어</a></p>
</main>
{footer("en")}
</div>
</body>
</html>
"""


NBH = "\u2011"
PHRASES = (
    "Computer Vision Engineer로",
    "computer vision engineer",
    "Computer Vision Engineer",
    "딸기 재배 작업 로봇",
    "6D tool pose를 구합니다",
    "picking pose를 구합니다",
    "학습을 맡았습니다",
    "known CAD geometry",
    "65% runner handling",
    "runner handling 65%",
    "into an empty container",
    "five object types",
    "Daedong AILab",
    "FS Solution",
    "Jetson Nano",
    "Seokyeong University",
    "imitation learning",
    "flower thinning",
    "runner handling",
    "object types",
)


def harden_text(text):
    text = re.sub(r"(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])", NBH, text)
    for phrase in PHRASES:
        text = text.replace(phrase, f'<span class="nobr">{phrase}</span>')
    return text


def harden_html(doc):
    parts = re.split(r"(<[^>]*>)", doc)
    out = []
    skip = False
    for part in parts:
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<script") and not low.startswith("</"):
                skip = True
            elif low.startswith("<style") and not low.startswith("</"):
                skip = True
            out.append(part)
            if low.startswith("</script") or low.startswith("</style"):
                skip = False
            continue
        out.append(part if skip else harden_text(part))
    return "".join(out)


def main():
    pages = {
        "index.html": home_page("en"),
        "ko/index.html": home_page("ko"),
        "404.html": not_found_page(),
    }
    for project in PROJECTS:
        pages[f"projects/{project['slug']}.html"] = project_page(project, "en")
        pages[f"ko/projects/{project['slug']}.html"] = project_page(project, "ko")
    for rel, text in pages.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(harden_html(text), encoding="utf-8")
        print("wrote", rel)
    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        sitemap.unlink()
        print("removed sitemap.xml")


if __name__ == "__main__":
    main()
