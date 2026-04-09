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

    # hit_count 증가
    hit_count=$((hit_count + 1))
    jq --arg rid "$id" --argjson hc "$hit_count" \
      '(.auto_rules[] | select(.id == $rid) | .hit_count) |= $hc' \
      "$TRIGGERS_FILE" > /tmp/harsh_triggers_update.json \
      && mv /tmp/harsh_triggers_update.json "$TRIGGERS_FILE"

    # 2회 이상 재발 시 HARD 승격
    if [ "$hit_count" -ge 2 ] && [ "$level" = "SOFT" ]; then
      jq --arg rid "$id" \
        '(.auto_rules[] | select(.id == $rid) | .level) |= "HARD"' \
        "$TRIGGERS_FILE" > /tmp/harsh_triggers_update.json \
        && mv /tmp/harsh_triggers_update.json "$TRIGGERS_FILE"
      level="HARD"
      echo "⬆️ [PROMOTED] ${id} — SOFT → HARD" >&2
    fi

    local desc
    desc="$(echo "$rule" | jq -r '.description // .id')"
    case "$level" in
      HARD)
        echo "🚫 [HARD] ${desc} — 응답 차단" >&2
        return 2
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

  matches="$(jq -c --arg level "$level" '.triggers[]? | select(.level == $level)' "$TRIGGERS_FILE" 2>/dev/null || true)"
  [ -n "$matches" ] || return 0

  while IFS= read -r trigger; do
    [ -n "$trigger" ] || continue

    local id description
    id="$(printf '%s\n' "$trigger" | jq -r '.id // empty')"
    [ -n "$id" ] || continue

    if grep -Fq -- "$id" "$TMP_FILE"; then
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
    fi
  done <<< "$matches"
}

main() {
  TRIGGERS_FILE="$HOME/.claude/data/harsh-critic-triggers.json"

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
