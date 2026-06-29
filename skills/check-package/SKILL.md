---
name: check-package
description: 폰케이스 패키지 적합성 자동 검토. 디바이스 STP 파일을 받아 케이스 치수를 추정하고, 트레이/블리스터 기준과 비교해 OK/NG 결과와 3D HTML 뷰어를 생성한다.
triggers:
  - /check-package
  - 패키지 검토
  - 케이스 검토
  - package check
---

# check-package 스킬

## 목적

**케이스 단품 포장 적합성 검토.**
폰 STP 파일에서 디바이스 치수를 추정 → 케이스 치수 계산 → 트레이/블리스터 기준과 비교.
검토 대상은 폰+케이스 조합이 아니라 **빈 케이스 단품**을 트레이에 뒤집어 얹는 포장 형태다.

## 스크립트 위치

```
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/0.work/1. 진행중/26.04 디바이스 검토용/check_package.py
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

### Step 1: 인수 파싱

사용자 입력에서 STP 파일 경로와 옵션을 추출한다.

- 파일 경로가 없으면: "디바이스 STP 파일 경로를 알려주세요." 요청
- 경로가 절대경로가 아니면: 현재 작업 디렉토리 기준으로 해석
- iCloud 경로일 경우 `brctl download "<path>" && sleep 2` 로 먼저 동기화
- `--side`, `--back` 미입력 시: 기본값(1.5, 1.2) 사용

### Step 2: cadquery 환경 확인 및 실행

아래 순서대로 시도한다.

**방법 A — conda cq 환경 (있는 경우):**
```bash
# conda 위치 탐색
CONDA=$(which conda 2>/dev/null || find /opt /usr/local /Users/harugury -name "conda" -type f 2>/dev/null | head -1)
$CONDA run -n cq python \
  "/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/0.work/1. 진행중/26.04 디바이스 검토용/check_package.py" \
  "<device_stp_path>" --side <side> --back <back> --no-browser
```

**방법 B — venv 설치 (conda 없는 경우):**
```bash
# 최초 1회 venv 생성 및 cadquery 설치
python3 -m venv /tmp/cq-venv
/tmp/cq-venv/bin/pip install cadquery plotly --quiet

/tmp/cq-venv/bin/python \
  "/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/0.work/1. 진행중/26.04 디바이스 검토용/check_package.py" \
  "<device_stp_path>" --side <side> --back <back> --no-browser
```

방법 A 실패 시 방법 B로 자동 전환한다.

### Step 3: 결과 요약 출력

스크립트 터미널 출력을 그대로 사용자에게 보여준다.

결과 HTML이 생성된 경우:
```
📄 3D 뷰어 생성됨: [결과 파일 경로]
cokacdir --sendfile 로 파일을 전송합니다.
```
HTML 파일을 `cokacdir --sendfile`로 사용자에게 전송한다.

### Step 4: NG 항목 해설

NG 항목이 있으면 원인과 대응 방안을 한국어로 설명한다.

```
❌ 외측 폭 초과 (+2.3mm)
  → 케이스 외곽이 트레이 홈보다 2.3mm 넓습니다.
    측면 두께를 1.5mm → 0.3mm 줄이면 통과 가능합니다.
```

두께 항목이 NG인 경우 별도 안내:
```
⚠️ 두께 초과는 폰 자체 두께에서 기인합니다.
   트레이 깊이(6.0mm)가 케이스 두께보다 얕은 경우,
   케이스가 트레이 위로 돌출됩니다.
   포장 상자 내부 공간이 충분하면 실사용상 문제없을 수 있습니다.
```

## 검토 기준

### 트레이 (무림 STP 기준)

케이스를 뒤집어 트레이 홈에 얹는 형태 기준:

| 항목 | 기준값 | 조건 | 설명 |
|------|--------|------|------|
| 내측 폭 (보스) | 64.6mm | 케이스 내경 > 기준값 | 보스가 케이스 개구부 안으로 들어가야 함 |
| 내측 높이 (보스) | 141.6mm | 케이스 내경 > 기준값 | 동일 |
| 외측 폭 (홈) | 92.4mm | 케이스 외곽 < 기준값 | 케이스 외곽이 홈 안에 들어가야 함 |
| 외측 높이 (홈) | 175.4mm | 케이스 외곽 < 기준값 | 동일 |
| 트레이 깊이 | 6.0mm | 케이스 두께 < 기준값 | 초과 시 케이스가 트레이 위로 돌출 |

### 블리스터 (3BR199750 기준)

| 항목 | 기준값 | 조건 |
|------|--------|------|
| 내측 폭 | 85.5mm | 케이스 외곽 < 기준값 |
| 내측 높이 | 148.0mm | 케이스 외곽 < 기준값 |
| 깊이 | 15.0mm | 케이스 두께 < 기준값 |

## 오류 대응

| 오류 | 원인 | 해결 |
|------|------|------|
| 파일 없음 | 경로 오류 또는 iCloud 미동기화 | `brctl download` 후 재시도 |
| ModuleNotFoundError: cadquery | 환경 없음 | 방법 B(venv) 사용 |
| plotly ImportError | plotly 미설치 | venv에 `pip install plotly` |
| 치수가 비정상 (너무 크거나 작음) | 어셈블리 STP — 여러 컴포넌트 좌표 혼재 | 단품 STP 파일 사용 권장 |
| permission denied | 결과 폴더 권한 | `mkdir -p results` 후 재시도 |
