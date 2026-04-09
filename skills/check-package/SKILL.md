---
name: check-package
description: 폰케이스 패키지 적합성 자동 검토. 디바이스 STP 파일을 받아 트레이/블리스터 기준과 비교하고 OK/NG 결과와 3D HTML 뷰어를 생성한다.
triggers:
  - /check-package
  - 패키지 검토
  - 케이스 검토
  - package check
---

# check-package 스킬

디바이스 STP 파일을 받아 기존 패키지(트레이 + 블리스터) 적합성을 자동 검토한다.

## 스크립트 위치

```
/Users/mac/Library/Mobile Documents/com~apple~CloudDocs/0.work/1. 진행중/26.04 디바이스 검토용/check_package.py
```

## 사용법

```
/check-package <device.stp> [--side <mm>] [--back <mm>]
```

### 인수

| 인수 | 기본값 | 설명 |
|------|--------|------|
| `device.stp` | 필수 | 디바이스 STP 파일 경로 |
| `--side` | 1.5mm | 케이스 측면 두께 오프셋 |
| `--back` | 1.2mm | 케이스 뒷면 두께 오프셋 |
| `--no-browser` | false | HTML 자동 오픈 끄기 |

### 예시

```
/check-package "iPhone16Pro.stp"
/check-package "GalaxyS25.stp" --side 2.0 --back 1.5
/check-package "/path/to/device.stp" --side 1.8
```

## 실행 절차

이 스킬이 호출되면 아래 순서대로 실행한다.

### Step 1: 인수 파싱

사용자 입력에서 STP 파일 경로와 옵션을 추출한다.

- 파일 경로가 없으면: "디바이스 STP 파일 경로를 알려주세요." 요청
- 경로가 절대경로가 아니면: 현재 작업 디렉토리 기준으로 해석
- --side, --back 미입력 시: 기본값(1.5, 1.2) 사용

### Step 2: 스크립트 실행

```bash
python3 "/Users/mac/Library/Mobile Documents/com~apple~CloudDocs/0.work/1. 진행중/26.04 디바이스 검토용/check_package.py" \
  "<device_stp_path>" \
  --side <side_thickness> \
  --back <back_thickness>
```

Bash 도구로 실행한다.

### Step 3: 결과 요약 출력

스크립트 터미널 출력을 그대로 사용자에게 보여준다.

결과 HTML 경로를 확인하고:
```
📄 3D 뷰어: [결과 파일 경로]
브라우저에서 자동으로 열렸어요. 마우스로 돌려보세요.
```

### Step 4: NG 항목 해설 (NG인 경우)

NG 항목이 있으면 원인과 대응 방안을 한국어로 간단히 설명한다.

예시:
```
❌ 외측 폭 초과 (+2.3mm)
  → 케이스 외곽이 트레이 홈보다 2.3mm 넓어요.
    측면 두께를 1.5mm → 0.3mm 줄이면 통과 가능해요.
```

## 검토 기준 (참고)

### 트레이 (무림 STP 기준)

| 항목 | 기준값 | 조건 |
|------|--------|------|
| 내측 폭 (돌출 플랫폼) | 64.6mm | 케이스 내경 > 기준값 |
| 내측 높이 (돌출 플랫폼) | 141.6mm | 케이스 내경 > 기준값 |
| 외측 폭 (홈 내측선) | 92.4mm | 케이스 외곽 < 기준값 |
| 외측 높이 (홈 내측선) | 175.4mm | 케이스 외곽 < 기준값 |
| 트레이 깊이 | 6.0mm | 케이스 두께 < 기준값 |

### 블리스터 (3BR199750)

내측 칼선 치수 미확정 — check_package.py의 BLISTER 값 업데이트 후 활성화됨.

## 오류 대응

| 오류 | 원인 | 해결 |
|------|------|------|
| 파일을 찾을 수 없습니다 | 경로 오류 | 절대경로로 다시 시도 |
| 좌표를 찾을 수 없습니다 | STP 포맷 문제 | CARTESIAN_POINT 없는 파일 |
| plotly ImportError | plotly 미설치 | `pip3 install plotly` |
| permission denied | 결과 폴더 권한 | results/ 폴더 수동 생성 |

## 블리스터 치수 업데이트 방법

AI(일러스트레이터) 원본에서 내측 칼선 둥근 사각형 치수 확인 후:

```python
# check_package.py 상단 BLISTER 딕셔너리 수정
BLISTER = {
    "inner_w": 95.0,   # ← 실제 측정값으로 변경
    "inner_h": 172.0,  # ← 실제 측정값으로 변경
}
```
