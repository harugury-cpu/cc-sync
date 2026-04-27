---
name: escape-room-check
description: 방탈출 카페 예약 페이지에서 특정 테마의 빈자리를 조회한다. URL과 테마명, 원하는 요일/시간대를 받아 현재 예약 가능 슬롯을 바로 보여준다. 알림이나 스케줄 없이 즉시 결과를 반환한다.
license: MIT
metadata:
  category: utility
  locale: ko-KR
  phase: v1
---

# Escape Room Availability Check

## What this skill does

방탈출 예약 사이트의 특정 테마에 대해 지정한 요일·시간대에 빈자리가 있는지 즉시 확인한다.
스케줄 등록이나 텔레그램 알림 없이 결과를 대화 안에서 바로 보여준다.

## When to use

- "제로월드 홍대 얼라이브 토요일 빈자리 있어?"
- "이 방탈출 예약 페이지에서 다음 주 금요일 저녁 자리 확인해줘"
- URL과 테마명을 주면서 빈자리 여부를 묻는 모든 경우

## Inputs

| 항목 | 예시 | 필수 |
|------|------|------|
| 예약 페이지 URL | https://zerohongdae.com/reservation/51 | 필수 |
| 테마명 | 얼라이브 | 필수 |
| 원하는 요일 | 토요일 | 필수 |
| 원하는 시간대 | 12시~20시 | 필수 |
| 조회 기간 | 2주 이내 (기본값) | 선택 |

## Investigation Process

URL을 처음 받으면 아래 순서로 API를 탐색한다.

### Step 1 — 페이지 fetch + 쿠키 수집

```bash
curl -s -c /tmp/er_cookies.txt "<URL>" -o /tmp/er_page.html
```

XSRF-TOKEN 또는 csrf_token 쿠키 확인:
```bash
grep -i "xsrf\|csrf\|token" /tmp/er_cookies.txt
```

### Step 2 — JS 파일에서 API 엔드포인트 탐색

페이지에서 script src 목록 추출:
```bash
grep -oP 'src="[^"]+\.js[^"]*"' /tmp/er_page.html
```

각 JS 파일에서 date/time/reservation 관련 POST 엔드포인트 탐색:
```bash
curl -s "<JS_URL>" | grep -oP '(?:url|fetch|ajax)[^"'\'']{0,30}["\'\'](\/[^"'\'']+)["'\'']' | head -20
```

### Step 3 — 테마 목록 API 호출 테스트

발견한 엔드포인트에 날짜를 POST로 전송:
```python
import json
from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode, unquote
from http.cookiejar import CookieJar

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))
opener.open(Request("<PAGE_URL>", headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read()
xsrf = next((unquote(c.value) for c in cj if "xsrf" in c.name.lower() or "csrf" in c.name.lower()), None)

payload = urlencode({"reservationDate": "<DATE>", "location": "1"}).encode()
req = Request("<API_URL>", data=payload, headers={
    "User-Agent": "Mozilla/5.0",
    "X-XSRF-TOKEN": xsrf,
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "<PAGE_URL>",
})
data = json.loads(opener.open(req, timeout=15).read().decode())
print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
```

### Step 4 — 응답 구조 해석

응답에서 아래 패턴을 찾는다:

**예약 가능 여부 필드 (사이트마다 다름)**:
- `reservation: false` → 빈자리 (zerohongdae 방식)
- `reservation: true` → 빈자리 (다른 사이트 방식)
- `available: true` → 빈자리
- `status: "available"` → 빈자리
- `is_reserved: false` → 빈자리

**테마 식별**:
- 응답의 `data` 또는 `themes` 배열에서 테마명으로 PK/ID 찾기
- 테마명이 title, name, theme_name 등으로 들어올 수 있음

### Step 5 — 예약 가능 범위 파악

달력 maxDate를 JS에서 확인:
```bash
curl -s "<JS_URL>" | grep -oP 'setDate[^;]{0,80}'
```
`setDate(getDate() + N)` 패턴 → N일이 최대 조회 가능 기간

### Step 6 — 결과 필터링 및 출력

- 지정 요일 + 지정 시간대에 해당하는 빈자리만 추출
- 날짜별로 묶어서 출력

## Known Sites

### 제로월드 홍대 (zerohongdae.com)
- API: `POST /reservation/theme`
- 파라미터: `reservationDate=YYYY-MM-DD&location=1`
- CSRF: XSRF-TOKEN 쿠키 → X-XSRF-TOKEN 헤더
- 예약 가능: `reservation: false`
- 최대 범위: today + 14일
- 얼라이브 테마 PK: 52


### 키이스케이프 메모리컴퍼니 (keyescape.com)
- API: `POST /controller/run_proc.php`
- 파라미터: `t=get_theme_time&date=YYYY-MM-DD&zizumNum=18&themeNum=<theme_num>&endDay=0`
- CSRF: 없음 (세션 쿠키만 필요 — 예약 페이지 먼저 GET 후 사용)
- 예약 가능: `enable != 'N'`
- 최대 범위: today + (doing-1)일 (doing=7이면 today+6)
- 예약 오픈: 매주 일요일 10:30에 다음 주 토요일분 오픈
- 테마 (zizum_num=18, 메모리컴퍼니 지점):
  - FILM BY EDDY:  theme_num=57, info_num=34, doing=7
  - FILM BY STEVE: theme_num=58, info_num=35, doing=7
  - FILM BY BOB:   theme_num=59, info_num=36, doing=7
- 예약 링크: `https://www.keyescape.com/reservation1.php?zizum_num=18&theme_num=<theme_num>&theme_info_num=<info_num>`

## Output Format

```
📋 [테마명] 빈자리 현황 (요일 HH시~HH시)

📅 MM/DD(요일)
  • HH시 MM분
  • HH시 MM분

📅 MM/DD(요일)
  • HH시 MM분

👉 [예약 링크]
```

빈자리 없으면:
```
❌ [테마명] 현재 조회 가능 기간 내 빈자리 없음
   (조회 범위: MM/DD ~ MM/DD, 요일, HH~HH시)
```

## Failure Modes

- **SPA/React 사이트**: 클라이언트 사이드 렌더링이면 curl로 API 탐색 불가. "브라우저 자동화가 필요한 구조입니다"라고 안내.
- **CSRF 토큰 불일치**: 세션 만료 시 재시도. 3회 실패 시 중단.
- **테마 PK 못 찾을 때**: 응답의 data 배열 전체를 출력해서 사용자가 확인하도록 안내.
- **API 엔드포인트 탐색 실패**: JS 파일에서 패턴 못 찾으면 reservation/theme, api/slots, api/times 등 일반적인 경로 순서로 시도.

## Notes

- 스케줄 등록이나 알림 설정은 이 스킬 범위 밖. 사용자가 원하면 cokacdir --cron으로 별도 등록.
- Known Sites 목록은 새 사이트 성공 시 업데이트.
