"""Korean copy for /ko/. Same keys as the English data in renew.py.

Numbers are not typed here. Every figure comes from build_site.FACTS through
{placeholders}, and renew.write_all() fails the build if a Korean page and its
English pair do not carry the same numbers.
"""

from build_site import FACTS


def F(text):
    return text.format_map(FACTS)


G1 = "첫 배포: class-name text prompt"
G2 = "업그레이드: caption으로 학습한 detector"

UI = {
    "skip": "본문으로 건너뛰기",
    "work": "작업",
    "record": "특허와 수상",
    "experience": "경력",
    "education": "학력",
    "details": "자세히",
    "problem": "문제",
    "role": "맡은 일",
    "role_line": "역할",
    "method": "방법",
    "result": "결과",
    "prev": "이전",
    "next": "다음",
    "all": "전체 작업",
    "pager": "인접 프로젝트",
    "code": "코드",
    "present": "현재",
    "missing": "페이지를 찾을 수 없습니다",
    "missing_body": "이 주소는 사이트에 없습니다.",
    "home_desc": "과수원 로봇과 robot arm을 위한 segmentation, point-cloud perception, pose estimation, manipulation learning을 만드는 perception engineer입니다.",
}

INTRO = (
    "로봇의 perception을 만듭니다. Image segmentation, point-cloud obstacle mapping, "
    "object pose estimation, manipulation을 위한 imitation learning을 다룹니다."
)

WHEN = {
    "daedong": "2024년 5월–현재",
    "plaif": "2023년 1월–2024년 4월",
    "fs": "2022년 5월–2022년 12월",
}

RECORD = [
    F("한국 특허 {patent}, 2024년 8월 등록. 출원인 PLAIF. 공동 발명자. {{title}} 제 {{link}} 작업이 이 특허의 기반입니다."),
    "Kaggle UBC-OCEAN: 동메달, 팀 순위 83/1,326, 2024년 1월.",
    "Kaggle Image Matching Challenge 2022: 은메달, 팀 순위 50/642, 2022년 6월. {code}",
    "Kaggle Happywhale (Whale and Dolphin Identification): 동메달, 팀 순위 127/1,588, 2022년 4월. {code}",
]

EXPERIENCE = [
    "Daedong AILab, Senior AI Researcher, 2024년 5월–현재.",
    "PLAIF, Computer Vision Engineer, 2023년 1월–2024년 4월.",
    "FS Solution Co., Ltd., Computer Vision Engineer, 2022년 5월–2022년 12월.",
]

EDUCATION = [
    F("서경대학교 산업경영시스템공학과 공학사, 서울, 2016년 3월–2022년 8월. 학점 {gpa}. 복수전공: Big Data."),
]

CLIP_LABELS = {
    "auto": "Labeling 도구에 띄운 과수원 video. Mask가 다음 frame으로 이어집니다.",
    "strawberry": "CES 2025 부스의 딸기 재배 작업.",
    "cad": "Gripper와 wrist camera를 단 robot arm이 fixture 위에서 부품을 조립합니다.",
    "bin": "CAD-based bin picking 중인 cobot arm.",
}

PAGES = {
    "language-distilled-segmentation": {
        "title": "RT100용 open-vocabulary perception과 mapping",
        "nav_title": "RT100 open-vocabulary perception",
        "result": "RT100 과수원 차량의 자율주행 vision stack에 vision perception model로 배포되어, Jetson Orin Nano에서 TensorRT로 돌아갑니다. Caption으로 학습한 업그레이드가 첫 배포 모델을 대체했습니다.",
        "role_line": "첫 배포 모델과 업그레이드를 학습해 RT100에 배포했고, occupancy grid mapping을 구현했습니다.",
        "desc": "RT100 자율주행 vision stack의 open-vocabulary vision perception model입니다. 첫 배포부터 caption 학습 업그레이드까지의 과정과, instance mask로 만든 occupancy grid를 다룹니다. Jetson Orin Nano에서 TensorRT로 돌아갑니다.",
        "thumb_alt": "업그레이드한 모델(caption으로 학습한 open-vocabulary detector)의 구조도.",
        "problem": "자율주행 과수원 차량 RT100은 고정된 label 목록에 없는 물체도 instance mask로 잡아야 합니다. 그 mask는 차량 위에서 주행 가능한 map이 되어야 합니다.",
        "role": "첫 배포 모델은 class-name text prompt 방식으로 pre-training했습니다. 이어서 caption으로 학습한 open-vocabulary detector로 업그레이드했고, 이 모델이 RT100 vision stack에서 첫 배포 모델을 대체했습니다. 두 모델 모두 제 auto-labeling pipeline이 만든 label로 학습했습니다.",
        "method": [
            (
                G1,
                "DINOv3와 SigLIP2 encoder는 고정하고, image adapter, PAN-FPN neck, text adapter, instance head, semantic head를 여러 dataset으로 pre-training했습니다. 두 head는 batch를 번갈아 가며 함께 학습했습니다. Box와 instance mask를 내는 instance head에는 region-text alignment loss를 걸었습니다. Semantic head는 pixel마다 class-name text embedding과 비교해 class를 고릅니다. Text-prompt inference와 fixed-vocabulary 변환을 넣었고, 모델을 과수원 domain에 맞췄습니다.",
            ),
            (
                "업그레이드가 필요했던 이유",
                "첫 배포 모델은 class name만 보고 학습했고, SigLIP2 text encoder도 고정돼 있었습니다. Validation subset에서는 가로등 같은 가는 구조물과 책 같은 작은 물체를 놓쳤습니다. 비슷한 class끼리 헷갈리기도 했습니다. Semantic head는 정해진 목록에서 가장 가까운 class를 고를 뿐, 모르는 물체를 거부하지 못합니다. 그래서 RT100 이미지에서 흰 반사판 일부가 snow로 분류됐습니다. 업그레이드한 모델은 class name보다 풍부한 text로 학습합니다. Compact text encoder를 object caption과 image caption으로 학습합니다. Caption은 학습 때만 쓰므로 inference 비용이 늘지 않습니다. Occupancy grid에는 instance mask가 필요해서, detector에 mask head를 달아 box와 함께 mask를 내게 했습니다.",
            ),
            (
                G2,
                "업그레이드한 모델은 query-based transformer detector입니다. Frozen DINOv3 backbone 뒤에 multi-scale projector와 three-layer decoder가 붙습니다. 학습 가능한 compact text encoder가 category name을 embedding합니다. Inference 때는 어떤 category name 목록이든 받습니다. 그 embedding으로 decoder query를 고르고 class마다 점수를 매깁니다. Mask head는 가장 해상도가 높은 feature를 decoder query와 함께 읽고, mask를 원본 이미지 해상도로 돌려줍니다. 학습에는 category name, object caption, image caption을 씁니다. 미리 계산해 둔 language teacher가 caption을 matched query, pooled image feature와 정렬하고, 관련 있는 negative의 가중치를 다시 매깁니다. Mask는 matching을 거쳐 BCE/Dice loss로 학습합니다.",
            ),
            (
                "Mask를 occupancy grid로",
                "Point cloud를 voxel로 줄이고, 각 voxel 중심을 camera image에 투영합니다. Instance mask 안에 떨어진 voxel은 그 mask의 object와 class를 받습니다. 유효한 anchor depth에서 virtual voxel을 더했습니다. Label이 붙은 voxel은 주행 가능한 occupancy grid에 기록됩니다. 더 이상 관측되지 않는 cell은 decay로 서서히 지워집니다. Hysteresis는 cell이 free와 occupied 사이에서 뒤집히지 않게 잡아 줍니다. Cost inflation은 계획 경로가 장애물 가장자리에서 떨어지게 합니다. Navigation은 이 grid를 읽습니다.",
            ),
        ],
        "outcome": "업그레이드한 모델은 ONNX와 TensorRT로 export되며, PyTorch, ONNX Runtime과 parity check를 거칩니다. 남은 과제는 두 가지입니다. 작은 물체, 그리고 주어진 category name 어디에도 맞지 않는 물체를 거부하는 일입니다.",
    },
    "auto-labeling": {
        "title": "Prompt 기반 image·video auto-labeling",
        "nav_title": "Auto-labeling pipeline",
        "result": F("이미지당 labeling 비용이 Prolific 대비 {cost_before}에서 {cost_after}으로 {cost_cut} 줄었습니다."),
        "role_line": "기존 video segmentation 모델 위에 prompting, serving, post-processing 계층을 만들었습니다.",
        "desc": F("Daedong AILab에 배포한 image·video용 prompt 기반 auto-labeling pipeline입니다. 이미지당 labeling 비용이 Prolific 대비 {cost_before}에서 {cost_after}으로 {cost_cut} 줄었습니다."),
        "problem": "이 pipeline 전에는 segmentation data와 region-grounded vision-language data를 사람이 직접 label했습니다.",
        "role": "Labeling 도구 밖에서는 label taxonomy를 정하고 annotation guideline을 썼습니다. COCO 형식의 training dataset도 만들었습니다. Labeling 뒤에 이어지는 세 단계 captioning pipeline 역시 제 작업입니다.",
        "method": [
            "Click과 mask 수정은 frame이 바뀌어도 같은 ID를 유지하는 tracked mask가 됩니다.",
            "Labeling이 끝나면 open-weight vision-language model이 label된 data에 caption을 답니다.",
        ],
        "outcome": "Pipeline은 Daedong AILab에 배포되어 있습니다. 이 label로 open-vocabulary perception model과 그 업그레이드를 학습했습니다.",
    },
    "strawberry-cultivation": {
        "title": "딸기 재배 작업",
        "result": F("고정된 실험실 환경에서 {cycles} work cycles 동안 측정한 task success는 transplanting {transplant}, flower thinning {thinning}, runner handling {runner}입니다. {ces}에 전시했습니다."),
        "role_line": "세 작업 모두 data pipeline과 Diffusion Policy 학습을 이끌었습니다.",
        "desc": F("UMI 시연으로 학습한 딸기 재배 작업 세 가지의 Diffusion Policy입니다. 고정된 실험실 환경에서 {cycles} work cycles 동안 측정한 task success는 transplanting {transplant}, flower thinning {thinning}, runner handling {runner}입니다. {ces}에 전시했습니다."),
        "problem": "딸기 재배 로봇은 모종 이식(transplanting), 꽃 솎기(flower thinning), 런너 정리(runner handling)를 해야 합니다. 작업별 policy는 Universal Manipulation Interface(UMI)로 모은 사람의 시연에서 학습합니다.",
        "role": "로봇 쪽 post-processing을 뺀 나머지는 모두 제가 만들었습니다.",
        "method": [],
        "outcome": "세 작업 policy는 재배 로봇에서 돌아갑니다.",
    },
    "cad-free-assembly": {
        "title": "CAD-free assembly",
        "result": F("사내 시험 {trials}회에서 task success {cad_success}를 기록했습니다."),
        "role_line": "2D camera image에서 목표 6D tool pose를 구하는 pose pipeline을 만들었습니다.",
        "desc": F("부품 CAD model 없이 2D camera로 robot assembly용 6D tool pose를 추정합니다. 사내 시험 {trials}회에서 task success {cad_success}를 기록했고, 한국 특허 {patent}의 기반이 됐습니다."),
        "problem": "CAD model이 없는 부품을 로봇이 조립해야 합니다. 실행 중에는 2D camera만 쓸 수 있으므로, 그 image에서 목표 6D tool pose를 구해야 합니다.",
        "role": F("이 작업은 한국 특허 {patent}의 기반이며, 저는 이 특허의 공동 발명자입니다."),
        "method": [
            "LightGlue가 실시간 2D image를 미리 저장한 reference RGB-D capture와 matching합니다. 그래서 match마다 depth가 붙습니다.",
            "solvePnP와 RANSAC이 3D-2D match에서 camera pose를 복원합니다. 이 pose를 eye-to-hand calibration, 저장된 reference pose와 이어 목표 6D tool pose를 얻습니다.",
        ],
        "outcome": "",
    },
    "bin-picking": {
        "title": "CAD-based bin picking",
        "result": F("사내 고정 환경 시험 {trials}회에서 object type 다섯 종류를 빈 용기로 옮겨 task success {bin_success}를 기록했습니다."),
        "role_line": "Instance segmentation model을 학습했고, CAD template 정렬 단계를 만들었습니다.",
        "desc": F("CAD geometry를 아는 물체를 위한 RGB-D bin picking입니다. Object type 다섯 종류, 사내 고정 환경 시험 {trials}회에서 task success {bin_success}를 기록했습니다."),
        "problem": "로봇이 CAD geometry를 아는 물체를 bin에서 꺼내야 합니다. 그러려면 bin을 찍은 RGB-D image에서 물체마다 pick pose를 구해야 합니다.",
        "role": "",
        "method": [
            "Instance segmentation model은 가려지지 않은 물체 class와 hole class를 나눠 학습했습니다. Object mask에서 hole mask를 빼고, 남은 instance mask로 point cloud를 나눴습니다.",
            "Pick pose마다 hidden-point removal로 visible-surface CAD template을 만들었습니다. PCA 초기화와 point-to-point ICP로 이 template을 segment된 point에 정렬했습니다.",
            "Registration fitness가 낮거나 inlier RMSE가 높은 pose는 버렸습니다. 남은 pose는 순위를 매긴 뒤 camera extrinsics로 robot base frame에 옮겼습니다.",
        ],
        "outcome": "",
    },
    "ros-6d-vision": {
        "title": "Eye-to-hand calibration 자동화",
        "result": "ROS trigger로 calibration을 돌리고, capture마다 residual error를 보고합니다. 별도 검증 단계는 robot base frame 기준 marker pose를 출력합니다.",
        "role_line": "Eye-to-hand calibration 자동화와 검증 단계를 만들었습니다.",
        "desc": "로봇 밖에 고정한 Zivid camera의 eye-to-hand calibration 자동화입니다. ArUco board capture, residual error를 보고하는 eye-to-hand solve, 검증 단계로 이뤄집니다.",
        "problem": "로봇 밖에 고정한 camera(eye-to-hand)는 pose를 camera frame 기준으로 측정합니다. 로봇은 robot base frame 기준 pose가 필요하므로, camera와 로봇 사이 transform을 calibration하고 검증해야 합니다.",
        "role": "",
        "method": [
            "ROS trigger가 들어올 때마다 ArUco board를 Zivid로 찍고, robot tool pose를 읽고, point cloud를 함께 써서 marker pose를 추정합니다.",
            "새 pose 쌍이 들어올 때마다 해를 다시 구합니다. Batch AX = YB solver와 OpenCV Park method가 camera-to-robot transform을 추정하고, capture마다 residual error의 평균과 표준편차를 publish합니다.",
            "Capture와 pose 쌍을 저장하므로, 중단된 session을 이어서 진행할 수 있습니다. 종료 요청이 오면 최종 calibration matrix를 저장합니다.",
            "별도 validation node가 저장된 matrix를 불러와, marker마다 robot base frame 기준 위치와 자세를 보고합니다.",
        ],
        "outcome": "",
    },
    "license-plate": {
        "title": "차량 번호판 인식",
        "result": "인식 pipeline은 배포되어 쓰이고 있습니다.",
        "role_line": "번호판 인식 pipeline을 만들었습니다.",
        "desc": "차량 번호판 인식입니다. Object detection이 번호판 위치를 찾고, OCR이 문자와 숫자를 읽습니다.",
        "problem": "번호판을 읽으려면 먼저 image에서 번호판을 찾아야 합니다.",
        "role": "",
        "method": [
            "Detection model이 번호판을 찾습니다.",
            "OCR이 문자와 숫자를 읽습니다.",
        ],
        "outcome": "",
    },
}

DIAGRAMS = {
    "language-distilled-segmentation": f"""<figure class="flow">
<p class="flow-k">RT100의 system flow</p>
<div class="flow-step">
<p class="flow-k">입력</p>
<p>RGB image, 그리고 같은 장면의 point cloud.</p>
</div>
<div class="flow-step">
<p class="flow-k">Open-vocabulary segmentation</p>
<p>Category name을 text로 주므로 다시 학습하지 않고 class 목록을 바꿀 수 있습니다.</p>
</div>
<div class="flow-fork">
<div>
<p class="flow-k">{G1}</p>
<p>Frozen DINOv3와 SigLIP2 encoder. 학습하는 부분은 image adapter와 text adapter, PAN-FPN neck, instance head와 semantic head입니다.</p>
</div>
<div>
<p class="flow-k">{G2} (첫 배포 모델 대체)</p>
<p>Frozen DINOv3 backbone, multi-scale projector, three-layer decoder, 학습 가능한 compact text encoder, mask head.</p>
</div>
</div>
<div class="flow-step">
<p class="flow-k">Box와 instance mask</p>
<p>두 모델 모두 냅니다. 첫 배포 모델은 semantic mask도 냈습니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Voxel에서 mask로</p>
<p>Image에 투영한 voxel 중심이 자신이 떨어진 mask의 object와 class를 받습니다. 유효한 anchor depth에서 virtual voxel을 더합니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Occupancy grid</p>
<p>Label이 붙은 voxel을 decay, hysteresis, cost inflation과 함께 grid에 기록합니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Navigation</p>
<p>Occupancy grid를 읽습니다.</p>
</div>
<figcaption>업그레이드 뒤에도 같은 mapping 단계를 씁니다.</figcaption>
</figure>
""",
    "strawberry-cultivation": F("""<figure class="flow">
<p class="flow-k">작업별 전체 시스템</p>
<div class="flow-step">
<p class="flow-k">시연</p>
<p>사람이 손에 든 UMI gripper로 작업을 합니다. Gripper에 달린 GoPro가 RGB video와 IMU data를 기록합니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Calibration</p>
<p>Camera를 IMU에 맞춰 calibration합니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Trajectory</p>
<p>ORB-SLAM3 visual-inertial SLAM이 video와 IMU data에서 gripper trajectory를 복원합니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Training set</p>
<p>Trajectory와 video frame을 training set으로 만듭니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">Policy</p>
<p>Diffusion Policy가 action sequence를 냅니다.</p>
</div>
<div class="flow-step">
<p class="flow-k">로봇 쪽</p>
<p>로봇 쪽 post-processing이 action을 robot control로 넘깁니다.</p>
</div>
<figcaption>같은 pipeline을 작업마다 한 번씩 돌리며, 작업마다 policy가 따로 있습니다.</figcaption>
</figure>
"""),
}

# Same images as English. Keyed by the English method label so the figure lands in the same place.
ARCH = {
    ("language-distilled-segmentation", "Initial release: class-name text prompts"): {
        "alt": "첫 배포 모델(class-name text prompt): frozen DINOv3 image encoder와 SigLIP2 text encoder, 학습하는 image adapter, PAN-FPN neck, text adapter, instance head와 semantic head.",
        "caption": "첫 배포 모델의 구조.",
    },
    ("language-distilled-segmentation", "Upgrade: caption-trained detector"): {
        "alt": F("업그레이드한 모델(caption으로 학습한 open-vocabulary detector)의 구조도. Frozen image encoder 뒤에 multi-scale projector와 {queries}개 query를 쓰는 three-layer decoder가 붙고, 이 query가 mask head, box head, class head로 이어집니다. Category name은 학습 가능한 text encoder를 거쳐 query를 고르고 class 점수를 매깁니다. 학습 때만 쓰는 branch에서는 object caption과 image caption이 frozen teacher text encoder를 거쳐 matched query, pooled image feature와 정렬됩니다."),
        "caption": "업그레이드한 모델. Category name(청록색)은 inference에 씁니다. Object caption(자홍색)과 image caption(금색)은 학습 때만 씁니다.",
    },
}

EXTRA_SECTIONS = {
    "cad-free-assembly": """<section>
<h2>시스템 구성도</h2>
<p>Reference RGB-D capture는 한 번만 찍습니다. 실행 중에는 2D camera image를 crop하고 grayscale로 바꾼 뒤 matching합니다.</p>
<figure class="arch"><img src="/assets/figures/cad-free-system.png" width="2040" height="760" alt="CAD-free assembly 시스템. Reference RGB-D capture는 한 번만 찍습니다. 실행 중에는 2D camera image를 crop하고 grayscale로 바꾸며, LightGlue가 그 keypoint를 reference RGB image와 matching합니다. Reference depth가 match를 2D-3D match로 바꾸고, solvePnP와 RANSAC이 camera pose를 구합니다. Eye-to-hand calibration과 저장된 reference tool pose로 이어지는 transform chain이 robot motion에 쓸 목표 6D tool pose를 줍니다."><figcaption>점선 상자는 특허에 적힌 단계입니다.</figcaption></figure>
</section>
""",
    "bin-picking": """<section>
<h2>시스템 구성도</h2>
<p>요청마다 color, point, normal이 담긴 RGB-D frame 하나에서 시작합니다. Mask 안의 point는 downsampling하고 normal 방향으로 거른 뒤 PCA에 넣습니다. Reverse check가 각 fit을 양방향으로 평가합니다. 남긴 pose는 ROS action result로 돌아가고, robot motion은 로봇 쪽에서 처리합니다.</p>
<figure class="arch"><img src="/assets/figures/bin-picking-system.png" width="1900" height="1090" alt="CAD-based bin picking 시스템. RGB-D frame이 instance segmentation model로 들어가 object와 hole을 segment합니다. Hole mask를 지운 뒤 object마다 mask 안의 point로 PCA 초기 pose를 구합니다. CAD mesh에서 hidden-point removal로 미리 만든 visible-surface template을 point-to-point ICP로 정렬하고, fit check로 pose 순위를 매깁니다. 남긴 pose는 eye-to-hand calibration으로 camera frame에서 robot base로 옮겨, robot motion에 쓸 ROS action result로 돌려줍니다."><figcaption>학습하는 것은 instance segmentation model 하나뿐입니다. Template은 object마다 offline으로 한 번 만듭니다.</figcaption></figure>
</section>
""",
    "strawberry-cultivation": """<section>
<h2>모델 구조</h2>
<p>Policy는 Diffusion Policy입니다. Image encoder가 RGB frame을 feature로 바꿉니다. 그 feature와 robot state가 global conditioning이 됩니다. Denoising network는 noise가 섞인 action sequence에서 출발해 단계를 반복하며 noise를 걷어 내고, 로봇 쪽에 넘길 action sequence를 돌려줍니다.</p>
<figure class="arch"><img src="/assets/figures/strawberry-policy.png" width="2040" height="700" alt="딸기 작업용 Diffusion Policy. RGB frame이 image encoder를 거쳐 RGB feature가 됩니다. RGB feature와 robot state가 학습된 denoising network의 global conditioning이 되고, network는 denoising 단계를 반복해 noise 섞인 action sequence를 action sequence로 바꿉니다. Action sequence는 로봇 쪽으로 넘어갑니다."></figure>
</section>
""",
    "auto-labeling": f"""<section>
<h2>모델 구조</h2>
<p>Pipeline은 기존 prompt 기반 video segmentation 모델을 씁니다. Image encoder와 neck이 frame마다 feature를 만들고, mask decoder가 point prompt나 mask prompt를 mask logit으로 바꿉니다. Video에서는 memory 경로가 추적 중인 mask를 저장해 이후 frame으로 넘깁니다.</p>
<figure class="arch"><img src="/assets/figures/auto-labeling-system.png" width="2040" height="1500" alt="Auto-labeling 시스템. 위쪽에서는 image encoder와 neck이 point-prompt decoding과 mask-prompt decoding으로 이어지고, memory bank를 쓰는 memory attention이 frame 사이로 추적 대상을 넘깁니다. Mask logit은 COCO polygon과 RLE mask를 쓰는 CPU service로 갑니다. 아래쪽에서는 완성된 label에 세 단계로 caption을 답니다. Mask마다 object caption, image 안에서 각 mask가 맺는 relation caption, 그리고 image caption입니다. Caption은 검토를 거치고 확신이 낮은 경우는 다시 검토한 뒤 instance annotation에 연결합니다. Object caption과 image caption은 open-vocabulary detector 업그레이드의 학습에 쓰입니다. Relation caption은 label과 함께 저장하고 그 학습에는 쓰지 않습니다."><figcaption>GPU service가 모델을 돌리고, CPU service가 mask logit을 COCO polygon과 RLE mask로 바꿉니다.</figcaption></figure>
<p>모델은 공개된 기존 open-source TensorRT export 위에서 돌아갑니다. 그 export가 모델을 여러 graph로 나누고 memory attention을 sparse하게 바꿨습니다. 이 변경은 export 작성자의 작업입니다. 제 변경은 model weight를 바꾸지 않습니다.</p>
</section>
<section>
<h2>Image labeling</h2>
<p>정지 image에는 이전 frame이 없으므로 memory encoder와 object pointer를 쓰지 않습니다. Point-prompt decoder에서 mask, object score, IoU 출력만 남긴 subgraph를 뽑았습니다. Operator와 weight는 video graph와 같습니다. Encoder와 neck은 image마다 한 번 돕니다. 첫 click은 first-click decoder로 갑니다. 그다음 click부터는 앞선 click 전부, 그리고 mask prompt 역할을 하는 직전 mask logit과 함께 refine decoder로 들어갑니다.</p>
</section>
<section>
<h2>Video labeling</h2>
<p>첫 frame에 이미 있는 label은 model input 크기로 바꾸고 mask logit으로 만들어 conditioning frame으로 넣습니다. Ground 같은 region class는 먼저 object mask의 합집합만큼 잘라 내므로, 겹친 label에서 tracking이 시작되는 일은 없습니다. Click은 그 위에 point prompt로 얹으며, 새 object는 반드시 positive click으로 시작합니다. Annotator가 한 frame을 아직 click하는 동안에는 중간 mask를 memory에 쓰지 않습니다. 최종 mask만 encoding해 저장합니다. 뒤쪽 frame에서 고친 내용도 같은 방식으로, 같은 track ID를 가진 새 conditioning frame으로 더합니다.</p>
</section>
<section>
<h2>출력</h2>
<p>Mask logit은 낮은 해상도로 채운 뒤 upsampling해 binary mask로 바꿉니다. Cleanup 단계는 object와 region class가 겹치지 않게 하고, region class의 작은 조각은 이웃 영역에 넘깁니다. 같은 object class끼리 겹친 중복도 지웁니다. 어떤 positive click과도 이어지지 않은 조각은 버립니다. Object는 COCO polygon으로, region class는 mask로 저장합니다.</p>
</section>
<section>
<h2>Serving</h2>
<p>Image 경로와 video 경로는 GPU 위의 encoder와 neck 하나를 함께 씁니다. Image feature는 click 사이에 GPU에 남겨 두고, 직전 mask도 마찬가지입니다. FP16 build가 mask IoU check를 통과하지 못해서 point-prompt decoder는 FP32로 build했습니다. GPU inference와 CPU post-processing은 별도 service 두 개로 나눠 돌립니다.</p>
</section>
<section>
<h2>Labeling 이후 captioning</h2>
<p>Caption은 세 단계로 나뉩니다.</p>
<ul>
<li>Mask마다 그 mask가 덮는 object의 caption을 달았습니다.</li>
<li>Mask마다 image와의 관계를 설명하는 caption도 달았습니다.</li>
<li>Image 전체에도 따로 caption을 달았습니다.</li>
</ul>
<p>Caption은 검토를 거치며, 확신이 낮은 경우는 두 번째 검토로 넘깁니다. 검증된 caption은 instance annotation에 연결합니다.</p>
<p><a href="/ko/projects/language-distilled-segmentation.html">Open-vocabulary 모델</a>의 caption 학습 업그레이드는 object caption과 image caption으로 학습합니다. Relationship caption은 label과 함께 저장해 두고, 이 학습에는 쓰지 않습니다.</p>
</section>
""",
}
