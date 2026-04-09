#!/bin/bash
# fix-commit-learner.sh
# git post-commit hook: fix: 커밋 diff에서 NEVER DO 규칙 자동 추출
set -euo pipefail

TRIGGERS_FILE="$HOME/.claude/data/harsh-critic-triggers.json"

# 의존성 확인
command -v claude >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0
[ -f "$TRIGGERS_FILE" ] || exit 0

# 커밋 메시지가 fix:로 시작하는지 확인
COMMIT_MSG=$(git log -1 --pretty=%s 2>/dev/null || echo "")
echo "$COMMIT_MSG" | grep -qi '^fix:' || exit 0

# diff 추출 (최대 200줄)
DIFF=$(git show HEAD --stat --patch 2>/dev/null | head -200)
[ -n "$DIFF" ] || exit 0

EXTRACT_PROMPT="다음은 fix: 커밋의 diff다.

${DIFF}

이 수정에서 Claude가 앞으로 피해야 할 NEVER DO 규칙 하나를 JSON으로만 반환하라.
규칙은 구체적이고 행동 가능해야 한다.
형식 (JSON만, 다른 텍스트 없음):
{\"id\":\"auto_\",\"description\":\"한 줄 설명\",\"keywords\":[\"응답에서감지할키워드1\",\"키워드2\"],\"context\":\"원인 요약 한 줄\"}"

RULE_JSON=$(echo "$EXTRACT_PROMPT" | claude -p 2>/dev/null | tr -d '\n' | grep -o '{[^{}]*}' | head -1 || echo "")

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  exit 0
fi

TIMESTAMP=$(date +%s)
RULE_JSON=$(echo "$RULE_JSON" | jq \
  --arg ts "$TIMESTAMP" \
  --arg src "fix_commit" \
  '.id = ("auto_" + $ts) | .level = "SOFT" | .hit_count = 0 | .source = $src | .created_at = (now | todate)')

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  exit 0
fi

UPDATED=$(jq --argjson rule "$RULE_JSON" '.auto_rules += [$rule]' "$TRIGGERS_FILE")
echo "$UPDATED" > "$TRIGGERS_FILE"

DESCRIPTION=$(echo "$RULE_JSON" | jq -r '.description // "새 규칙"')
echo "💡 [FIX-LEARN] 새 규칙 추가: ${DESCRIPTION}"
exit 0
