# Keyescape Booking Skill

키이스케이프 메모리컴퍼니 방탈출 자동 예약 스킬.
빈자리 확인 + 즉시 예약까지 처리한다.

## When to use
- "키이스케이프 예약 잡아줘"
- "FILM BY EDDY 토요일 예약 해줘"
- 테마 / 날짜 / 우선순위 시간을 주면서 예약 요청하는 모든 경우
- 예약 오픈 시각에 자동 시도를 예약할 때

---

## Default User Info

메모리에서 불러온 기본값. 변경 요청이 있으면 먼저 확인한다.

- 이름: 한원진
- 전화번호: 010-4308-3436
- 인원: 3명
- 결제: 무통장입금 (payment=D)
- 1인 가격: 32,000원

---

## Known Themes (메모리컴퍼니, zizumNum=18)

| 테마 | themeNum | themeInfoNum |
|------|----------|--------------|
| FILM BY EDDY | 57 | 34 |
| FILM BY STEVE | 58 | 35 |
| FILM BY BOB | 59 | 36 |

예약 오픈: **매주 일요일 10:30** → 당일 **10:29:57**에 시도

---

## Inputs

| 항목 | 예시 | 필수 |
|------|------|------|
| 테마 | FILM BY EDDY | 필수 |
| 목표 날짜 (토요일) | 2026-05-09 | 필수 |
| 우선순위 시간 | 12:15 → 13:45 → 10:45 | 필수 |
| 실행 시각 | 10:29:57 기본값 | 선택 |

---

## Execution Flow

### Step 1 — 실행 시각 계산

목표 토요일 기준 6일 전(일요일) 10:29:57을 실행 시각으로 쓴다.

```python
from datetime import date, timedelta
target_sat = date(YYYY, MM, DD)
run_day = target_sat - timedelta(days=6)  # 전 주 일요일
run_at = f"{run_day} 10:29:57"
```

사용자가 "지금 바로" 또는 "오늘" 시도를 요청하면 --at "오늘 날짜 10:29:57" 또는 즉시 실행.

---

### Step 2 — cokacdir 스케줄 등록

아래 Python 코드를 cron prompt에 포함시켜 --once 스케줄로 등록한다.
변수(PRIORITY, TARGET_DATE, THEME_NUM, THEME_INFO_NUM)는 사용자 입력으로 채운다.

```python
import json
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar

BASE = 'https://www.keyescape.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
PRIORITY       = ['12:15', '13:45', '10:45']   # 사용자 입력으로 교체
TARGET_DATE    = '2026-05-09'                   # 사용자 입력으로 교체
THEME_NUM      = '57'                           # 사용자 입력으로 교체
THEME_INFO_NUM = '34'                           # 사용자 입력으로 교체
NAME           = '한원진'
MOBILE         = ('010', '4308', '3436')
PEOPLE         = 3
PRICE_PER      = 32000

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))

# 1. 세션 쿠키 수집
opener.open(Request(
    f'{BASE}/reservation1.php?zizum_num=18&theme_num={THEME_NUM}&theme_info_num={THEME_INFO_NUM}',
    headers=HEADERS
)).read()

# 2. 슬롯 조회
payload = urlencode({
    't': 'get_theme_time', 'date': TARGET_DATE,
    'zizumNum': '18', 'themeNum': THEME_NUM, 'endDay': '0'
}).encode()
req = Request(f'{BASE}/controller/run_proc.php', data=payload, headers={
    **HEADERS,
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': f'{BASE}/reservation1.php'
})
resp = json.loads(opener.open(req).read().decode())
slots = resp if isinstance(resp, list) else resp.get('data', [])

# 3. 우선순위 순서로 예약
for priority_time in PRIORITY:
    for slot in slots:
        if slot.get('enable', 'N') == 'N':
            continue
        slot_time = (slot.get('start_time') or slot.get('revTimes') or
                     slot.get('time') or '')
        if priority_time not in slot_time:
            continue
        ttn = (slot.get('theme_time_num') or slot.get('themeTimeNum') or
               slot.get('num'))
        book_payload = urlencode({
            'device': 'pc', 't': 'ins_rev',
            'theme_info_num': THEME_INFO_NUM,
            'zizum_num': '18', 'theme_num': THEME_NUM,
            'rev_days': TARGET_DATE, 'theme_time_num': str(ttn),
            'rev_price': str(PEOPLE * PRICE_PER),
            'person': str(PEOPLE), 'name': NAME,
            'mobile1': MOBILE[0], 'mobile2': MOBILE[1], 'mobile3': MOBILE[2],
            'payment': 'D',
            'agree_all': 'on', 'agree_1': 'on', 'agree_2': 'on', 'agree_3': 'on'
        }).encode()
        book_req = Request(f'{BASE}/reservation2.php', data=book_payload, headers={
            **HEADERS,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'{BASE}/reservation1.php'
        })
        result = opener.open(book_req).read().decode('utf-8', errors='ignore')
        print(f'예약 시도: {TARGET_DATE} {priority_time} (ttn={ttn})')
        print(result[:500])
        exit(0)

print('빈자리 없음: 우선순위 시간 모두 마감')
```

---

### Step 3 — 스케줄 등록 후 확인 메시지 출력

```
⏰ 키이스케이프 예약 스케줄 등록 완료

테마: FILM BY EDDY
목표: 2026-05-09 (토)
실행: 2026-05-03 (일) 10:29:57
우선순위: 12:15 → 13:45 → 10:45
예약자: 한원진 / 010-4308-3436 / 3명

결과는 예약 시도 직후 전송됩니다.
```

---

## Success / Failure Report Format

성공:
```
✅ 키이스케이프 예약 완료
테마: FILM BY EDDY
날짜: 2026-05-09 (토) 12:15
예약자: 한원진 3명
결제: 무통장입금 96,000원
```

실패:
```
❌ 예약 실패: [사유]
조회된 빈자리: [있으면 목록 / 없으면 없음]
```

---

## Notes

- 예약 오픈은 매주 일요일 10:30이므로 10:29:57에 시도
- 결제 방식이 무통장입금(payment=D)이므로 KCP 결제창 없이 바로 처리됨
- 취소표 상시 대기 조회는 escape-room-check 스킬로 별도 처리
- 인원/결제 방식 변경 시 사용자에게 확인 후 진행
- 오늘 당일 시도: --at "오늘 날짜 10:29:57" 또는 --at "Nm" (N분 후)
