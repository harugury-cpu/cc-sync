#!/bin/bash
set -euo pipefail

check_auto_rules() {
  local auto_rules
  auto_rules="$(jq -c '.auto_rules[]?' "$TRIGGERS_FILE" 2>/dev/null || true)"
  [ -n "$auto_rules" ] || return 0

  while IFS= read -r rule; do
    [ -n "$rule" ] || continue

    local id level hit_count matched
    id="$(echo "$rule" | jq -r '.id // empty')"
    level="$(echo "$rule" | jq -r '.level // "SOFT"')"
    hit_count="$(echo "$rule" | jq -r '.hit_count // 0')"
    matched=0

    while IFS= read -r kw; do
      [ -n "$kw" ] || continue
      if grep -qiF "$kw" "$TMP_FILE" 2>/dev/null; then
        matched=1
        break
      fi
    done < <(echo "$rule" | jq -r '.keywords[]? // empty')

    [ "$matched" -eq 1 ] || continue

    hit_count=$((hit_count + 1))
    jq --arg rid "$id" --argjson hc "$hit_count" \
      '(.auto_rules[] | select(.id == $rid) | .hit_count) |= $hc' \
      "$TRIGGERS_FILE" > /tmp/harsh_triggers_update.json \
      && mv /tmp/harsh_triggers_update.json "$TRIGGERS_FILE"

    # 자동 SOFT→HARD 승격 폐기: 자동학습 규칙은 절대 응답을 차단하지 않는다.
    # (광범위 키워드일수록 hit이 빨리 쌓여 차단으로 승격되는 역설을 제거)
    local desc
    desc="$(echo "$rule" | jq -r '.description // .id')"
    case "$level" in
      HARD)
        echo "⚠️ [HARD] ${desc} — 자기검토 권고(비차단)" >&2
        ;;
      SOFT)
        echo "💡 [SOFT] ${desc}" >&2
        ;;
    esac
  done <<< "$auto_rules"
}

check_triggers() {
  local level="$1"
  local matches

  # 수정: .triggers[$level][]? — 올바른 객체 구조 접근
  matches="$(jq -c --arg level "$level" '.triggers[$level][]?' "$TRIGGERS_FILE" 2>/dev/null || true)"
  [ -n "$matches" ] || return 0

  while IFS= read -r trigger; do
    [ -n "$trigger" ] || continue

    local id description matched
    id="$(printf '%s\n' "$trigger" | jq -r '.id // empty')"
    [ -n "$id" ] || continue
    matched=0

    # 수정: id grep → keywords[] 매칭
    while IFS= read -r kw; do
      [ -n "$kw" ] || continue
      if grep -qiF "$kw" "$TMP_FILE" 2>/dev/null; then
        matched=1
        break
      fi
    done < <(printf '%s\n' "$trigger" | jq -r '.keywords[]? // empty')

    [ "$matched" -eq 1 ] || continue

    description="$(printf '%s\n' "$trigger" | jq -r '.description // .id // "trigger matched"')"

    case "$level" in
      EXTREME)
        echo "🚫 [EXTREME] ${description} — 응답 차단" >&2
        return 2
        ;;
      HIGH)
        echo "⚠️ [HIGH] ${description}" >&2
        ;;
      MEDIUM)
        echo "💡 [MEDIUM] ${description}" >&2
        ;;
    esac
  done <<< "$matches"
}

main() {
  HARSH_CRITIC_HOME="${HARSH_CRITIC_HOME:-$HOME/.ai-feedback/harsh-critic}"
  TRIGGERS_FILE="${HARSH_CRITIC_TRIGGERS_FILE:-$HARSH_CRITIC_HOME/triggers.json}"

  if [ ! -f "$TRIGGERS_FILE" ]; then
    exit 0
  fi

  if ! command -v jq >/dev/null 2>&1; then
    exit 0
  fi

  TMP_FILE="/tmp/harsh_critic_$$.json"
  trap 'rm -f "$TMP_FILE"' EXIT

  if ! cat >"$TMP_FILE"; then
    : >"$TMP_FILE"
  fi

  if [ ! -s "$TMP_FILE" ]; then
    exit 0
  fi

  if ! check_triggers EXTREME; then
    exit 2
  fi

  check_triggers HIGH
  check_triggers MEDIUM

  if ! check_auto_rules; then
    exit 2
  fi
}

main "$@"
