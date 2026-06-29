#!/bin/bash
# harsh-critic-learn.sh
# Stop 훅: !!! 이벤트 발생 후 Claude 응답에서 NEVER DO 규칙 자동 추출
set -euo pipefail

LEARN_FILE="/tmp/harsh_learn_latest.json"
HARSH_CRITIC_HOME="${HARSH_CRITIC_HOME:-$HOME/.ai-feedback/harsh-critic}"
TRIGGERS_FILE="${HARSH_CRITIC_TRIGGERS_FILE:-$HARSH_CRITIC_HOME/triggers.json}"
LOCK_DIR="/tmp/harsh_critic_learn.lock"
MAX_SECONDS=45

# nested `claude -p` also fires Claude hooks. If this env var is inherited by
# that child Claude process, skip this hook to prevent recursive Stop-hook loops.
[ "${HARSH_CRITIC_LEARN_DISABLE:-}" = "1" ] && exit 0

# !!! 학습 파일 없으면 종료
[ -f "$LEARN_FILE" ] || exit 0

# 중복 실행 방지. 오래된 lock은 비정상 종료 흔적으로 보고 회수.
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  if [ -d "$LOCK_DIR" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0) ))
    if [ "$LOCK_AGE" -gt 300 ]; then
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null || exit 0
    else
      exit 0
    fi
  else
    exit 0
  fi
fi

TMP_INPUT="/tmp/harsh_learn_processing_$$.json"
TMP_OUT="/tmp/harsh_learn_claude_$$.out"
cleanup() {
  rm -f "$TMP_INPUT" "$TMP_OUT"
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT

# 재진입 방지를 위해 latest marker를 먼저 제거하고 현재 입력을 별도 파일로 복사한다.
# claude -p가 nested Stop hook을 발생시켜도 latest가 없으므로 바로 종료된다.
if ! cp "$LEARN_FILE" "$TMP_INPUT" 2>/dev/null; then
  rm -f "$LEARN_FILE"
  exit 0
fi
REAL_LEARN_FILE="$(readlink "$LEARN_FILE" 2>/dev/null || true)"
rm -f "$LEARN_FILE"
[ -n "$REAL_LEARN_FILE" ] && rm -f "$REAL_LEARN_FILE" 2>/dev/null || true

# 의존성 확인
command -v claude >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

# Stop 훅 입력 읽기
cat > /dev/null  # stdin 비움 (응답 데이터 불필요)

# 사용자 프롬프트 추출
USER_PROMPT=$(jq -r '.prompt // empty' "$TMP_INPUT" 2>/dev/null || echo "")
if [ -z "$USER_PROMPT" ]; then
  exit 0
fi

# triggers 파일이 비었거나 깨졌으면 기본 구조로 복구
mkdir -p "$(dirname "$TRIGGERS_FILE")"
if ! jq -e 'type == "object"' "$TRIGGERS_FILE" >/dev/null 2>&1; then
  echo '{"triggers":{"EXTREME":[],"HIGH":[],"MEDIUM":[]},"auto_rules":[]}' > "$TRIGGERS_FILE"
elif ! jq -e 'has("auto_rules")' "$TRIGGERS_FILE" >/dev/null 2>&1; then
  tmp_init="/tmp/harsh_triggers_init_$$.json"
  jq '.auto_rules = []' "$TRIGGERS_FILE" > "$tmp_init" && mv "$tmp_init" "$TRIGGERS_FILE"
fi

# Claude로 규칙 추출
EXTRACT_PROMPT="다음은 사용자가 !!!를 사용해 강한 불만을 표현한 메시지다.

사용자 메시지: ${USER_PROMPT}

이 상황에서 Claude가 앞으로 피해야 할 NEVER DO 규칙 하나를 JSON으로만 반환하라.
규칙은 구체적이고 행동 가능해야 한다.
형식 (JSON만, 다른 텍스트 없음):
{\"id\":\"auto_\",\"description\":\"한 줄 설명\",\"keywords\":[\"응답에서감지할키워드1\",\"키워드2\"],\"context\":\"원인 요약 한 줄\"}"

# claude -p가 멈추거나 hook 재귀를 만들지 않도록:
# 1) HARSH_CRITIC_LEARN_DISABLE=1 상속
# 2) 직접 타임아웃 감시
(
  printf '%s\n' "$EXTRACT_PROMPT" | HARSH_CRITIC_LEARN_DISABLE=1 claude -p > "$TMP_OUT" 2>/dev/null
) &
CLAUDE_PID=$!

elapsed=0
while kill -0 "$CLAUDE_PID" 2>/dev/null; do
  if [ "$elapsed" -ge "$MAX_SECONDS" ]; then
    kill -TERM "$CLAUDE_PID" 2>/dev/null || true
    sleep 2
    kill -KILL "$CLAUDE_PID" 2>/dev/null || true
    exit 0
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done
wait "$CLAUDE_PID" 2>/dev/null || true

RULE_JSON=$(tr -d '\n' < "$TMP_OUT" | grep -o '{[^{}]*}' | head -1 || echo "")

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  exit 0
fi

# ID에 타임스탬프 붙여 고유화, 메타데이터 추가
TIMESTAMP=$(date +%s)
RULE_JSON=$(echo "$RULE_JSON" | jq \
  --arg ts "$TIMESTAMP" \
  --arg src "user_frustration" \
  '.id = ("auto_" + $ts) | .level = "SOFT" | .hit_count = 0 | .source = $src | .created_at = (now | todate)')

if [ -z "$RULE_JSON" ] || ! echo "$RULE_JSON" | jq . >/dev/null 2>&1; then
  exit 0
fi

# triggers.json에 append
UPDATED=$(jq --argjson rule "$RULE_JSON" '.auto_rules += [$rule]' "$TRIGGERS_FILE")
echo "$UPDATED" > "$TRIGGERS_FILE"

DESCRIPTION=$(echo "$RULE_JSON" | jq -r '.description // "새 규칙"')
echo "💡 [HARSH-LEARN] 새 규칙 추가: ${DESCRIPTION}" >&2

exit 0
