#!/bin/bash
# harsh-critic-learn.sh
# Stop 훅: !!! 이벤트 발생 후 Claude 응답에서 NEVER DO 규칙 자동 추출
set -euo pipefail

LEARN_FILE="/tmp/harsh_learn_latest.json"
TRIGGERS_FILE="$HOME/.claude/data/harsh-critic-triggers.json"

# !!! 학습 파일 없으면 종료
[ -f "$LEARN_FILE" ] || exit 0

# 의존성 확인
command -v claude >/dev/null 2>&1 || { rm -f "$LEARN_FILE"; exit 0; }
command -v jq >/dev/null 2>&1 || { rm -f "$LEARN_FILE"; exit 0; }

# Stop 훅 입력 읽기
cat > /dev/null  # stdin 비움 (응답 데이터 불필요)

# 사용자 프롬프트 추출
USER_PROMPT=$(jq -r '.prompt // empty' "$LEARN_FILE" 2>/dev/null || echo "")
if [ -z "$USER_PROMPT" ]; then
  rm -f "$LEARN_FILE"
  exit 0
fi

# Claude로 규칙 추출
EXTRACT_PROMPT="다음은 사용자가 !!!를 사용해 강한 불만을 표현한 메시지다.

사용자 메시지: ${USER_PROMPT}

이 상황에서 Claude가 앞으로 피해야 할 NEVER DO 규칙 하나를 JSON으로만 반환하라.
규칙은 구체적이고 행동 가능해야 한다.
형식 (JSON만, 다른 텍스트 없음):
{\"id\":\"auto_\",\"description\":\"한 줄 설명\",\"keywords\":[\"응답에서감지할키워드1\",\"키워드2\"],\"context\":\"원인 요약 한 줄\"}"

RULE_JSON=$(echo "$EXTRACT_PROMPT" | claude -p 2>/dev/null | tr -d '\n' | grep -o '{[^{}]*}' | head -1 || echo "")

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  rm -f "$LEARN_FILE"
  exit 0
fi

# ID에 타임스탬프 붙여 고유화, 메타데이터 추가
TIMESTAMP=$(date +%s)
RULE_JSON=$(echo "$RULE_JSON" | jq \
  --arg ts "$TIMESTAMP" \
  --arg src "user_frustration" \
  '.id = ("auto_" + $ts) | .level = "SOFT" | .hit_count = 0 | .source = $src | .created_at = (now | todate)')

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  rm -f "$LEARN_FILE"
  exit 0
fi

# triggers.json에 append
UPDATED=$(jq --argjson rule "$RULE_JSON" '.auto_rules += [$rule]' "$TRIGGERS_FILE")
echo "$UPDATED" > "$TRIGGERS_FILE"

DESCRIPTION=$(echo "$RULE_JSON" | jq -r '.description // "새 규칙"')
echo "💡 [HARSH-LEARN] 새 규칙 추가: ${DESCRIPTION}" >&2

rm -f "$LEARN_FILE"
exit 0
