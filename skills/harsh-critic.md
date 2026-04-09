---
name: harsh-critic
description: Claude 응답 완료 전 분노 트리거 자동 검사 및 수정. Stop Hook 또는 /harsh-critic으로 실행. "응답 검토", "자기검토", "harsh-critic" 키워드에 반응.
---

# Harsh Critic

## 역할
이 스킬은 Claude가 응답 제출 직전에 실행하는 자기검토 절차다. `$HOME/.claude/data/harsh-critic-triggers.json`의 트리거 목록으로 현재 응답을 검사한다.

## 검사 절차
### Step 1 - EXTREME 검사
`triggers.json`의 `EXTREME` 항목을 순서대로 확인한다. 하나라도 발견되면 즉시 현재 응답을 취소하고, 항목명과 이유를 짧게 밝힌 뒤 응답 전체를 다시 쓴다.

### Step 2 - HIGH 검사
`HIGH` 항목을 검사한다. 발견되면 해당 부분을 수정하고 응답을 정리한 뒤 Step 1부터 다시 검사한다.

### Step 3 - MEDIUM 검사
`MEDIUM` 항목은 차단하지 않는다. 발견 시 응답 말미에 `💡 개선 포인트: {항목}` 형식으로만 남긴다.

### Step 4 - PASS
모든 검사를 통과하면 `✅ Harsh Critic PASS`를 출력한 뒤 최종 응답을 전달한다.

## 자동 수정 루프
`EXTREME` 또는 `HIGH`가 보이면 수정 후 재검사한다. 이 루프는 최대 3회 반복한다. 3회 후에도 `EXTREME`가 남아 있으면 사용자에게 남은 항목과 문제 이유를 명시한다.

## 주의사항
`triggers.json`이 없으면 조용히 PASS 처리한다. `MEDIUM`만 발견됐다는 이유로 응답을 막으면 안 된다.
