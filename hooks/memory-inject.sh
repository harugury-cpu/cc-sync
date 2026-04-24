#!/bin/bash
# UserPromptSubmit hook: 이전 세션 메모리를 컨텍스트에 주입

LATEST="$HOME/.claude/memory/LATEST.md"
[ -f "$LATEST" ] || exit 0

CONTENT=$(head -60 "$LATEST" 2>/dev/null || echo "")
[ -n "$CONTENT" ] || exit 0

printf '<previous-session-memory>\n%s\n</previous-session-memory>\n' "$CONTENT"
exit 0
