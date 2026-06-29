#!/bin/bash
set -euo pipefail

# hook이 띄운 중첩 claude -p 세션에서는 발화하지 않는다 — 인용된 "!!!"에
# 반응해 학습 파일을 또 만들면 learn hook과 무한 재귀 루프가 된다.
[ "${HARSH_CRITIC_LEARN_DISABLE:-}" = "1" ] && exit 0
[ -n "${CLAUDE_SKIP_MEMORY_LEARN:-}" ] && exit 0

input=$(cat)
prompt=$(echo "$input" | jq -r '.prompt // empty' 2>/dev/null || true)

if echo "$prompt" | grep -qE '!{3,}|멍청|^[[:space:]]*--[[:space:]]*$'; then
  # 학습용 컨텍스트 저장
  TIMESTAMP=$(date +%s)
  LEARN_FILE="/tmp/harsh_learn_${TIMESTAMP}.json"
  echo "$input" > "$LEARN_FILE"
  ln -sf "$LEARN_FILE" /tmp/harsh_learn_latest.json

  printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"⚡ HARSH-CRITIC 모드 활성화: 이 응답 전에 반드시 harsh-critic 스킬을 실행하고 자기검토를 완료하세요. EXTREME/HIGH 트리거가 없을 때만 응답을 제출하세요."}}'
fi
exit 0
