---
id: multi-account-cookie-session
name: 멀티 계정 쿠키 세션 관리
description: 같은 브라우저에서 두 계정을 동시에 유지할 수 없는 문제 - 브라우저 분리 + sessionKey만 갱신하는 패턴
source: learned
triggers:
  - 두 계정 403
  - 멀티 계정 쿠키
  - 계정 세션 만료
  - sessionKey 갱신
  - 브라우저 계정 분리
quality: high
---

# 멀티 계정 쿠키 세션 관리

## The Insight

같은 브라우저는 하나의 계정만 유지한다. 두 계정을 자동화 모니터링할 때는 **브라우저를 분리**해야 한다. 세션 만료 시 전체 쿠키를 다시 긁을 필요 없이 **sessionKey 하나만 교체**하면 된다.

## Why This Matters

- Chrome에서 account2로 로그인하면 account1 sessionKey가 무효화됨
- `document.cookie`는 httpOnly 쿠키(sessionKey 등)를 반환하지 않음
- Cloudflare 토큰(`cf_clearance`, `__cf_bm`)은 브라우저/IP 바인딩 → 공유 불가
- 두 계정이 같은 Cloudflare 토큰을 순차 사용하면 교대로 403 발생

## Recognition Pattern

- 두 계정 중 항상 하나만 403 → 브라우저 공유 문제
- `document.cookie` 결과가 비어있거나 sessionKey 없음 → httpOnly 쿠키
- 쿠키를 새로 넣어도 몇 분 후 다시 403 → routingHint JWT 만료 (~10-15분)

## The Approach

### 브라우저 분리
- **account1** → Chrome (또는 주 브라우저)
- **account2** → Safari (또는 Firefox)

### 세션 만료 시 최소 갱신
1. 해당 브라우저에서 claude.ai 열기
2. **Safari/Firefox**: DevTools → Storage 탭 → Cookies → `sessionKey` 값만 복사
3. 세션 파일의 sessionKey만 교체:
```python
import json
d = json.load(open('sessions/accountN.json'))
for c in d['cookies']:
    if c['name'] == 'sessionKey':
        c['value'] = '새로운 sessionKey 값'
with open('sessions/accountN.json', 'w') as f:
    json.dump(d, f, indent=2)
```

### 전체 쿠키 갱신이 필요한 경우
- 계정이 완전히 로그아웃된 경우
- Chrome: Network 탭 → 요청 클릭 → Request Headers → `cookie:` 전체 복사
- Safari: `document.cookie`는 httpOnly 제외 → Storage 탭에서 수동 확인
