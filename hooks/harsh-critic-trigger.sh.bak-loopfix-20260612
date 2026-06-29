#!/bin/bash
set -euo pipefail

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
