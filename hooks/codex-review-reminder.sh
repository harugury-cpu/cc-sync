#!/bin/bash
# codex-review-reminder.sh
# 코드 파일 수정 후 완료 선언 전 codex 리뷰 촉구

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

if [ -z "$FILE" ]; then exit 0; fi

if echo "$FILE" | grep -qE '\.(ts|tsx|js|jsx|mjs|cjs|py|go|rs|java|kt|swift|c|cpp|h|cs|rb|php|sh|bash|zsh)$'; then
    printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"⚠️ [codex 리뷰 의무] 코드 파일이 수정되었습니다. 완료를 선언하기 전에 반드시 Skill 도구로 codex 스킬을 호출하여 리뷰를 받아야 합니다."}}\n'
fi
