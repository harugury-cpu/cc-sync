#!/bin/bash
# auto-validate.sh
# PostToolUse(Edit|Write|MultiEdit) 트리거 - 파일 수정 후 자동 문법 검증

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    ti = d.get('tool_input', {})
    print(ti.get('file_path', ti.get('path', '')))
except:
    print('')
" 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

EXT="${FILE_PATH##*.}"
ERROR_LOG="/tmp/claude-validation-error.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

case "$EXT" in
    py)
        OUTPUT=$(python3 -m py_compile "$FILE_PATH" 2>&1)
        EXIT=$?
        ;;
    js|mjs|cjs)
        OUTPUT=$(node --check "$FILE_PATH" 2>&1)
        EXIT=$?
        ;;
    ts|tsx)
        if command -v tsc > /dev/null 2>&1; then
            OUTPUT=$(tsc --noEmit --skipLibCheck "$FILE_PATH" 2>&1)
        else
            OUTPUT=$(node --check "$FILE_PATH" 2>&1)
        fi
        EXIT=$?
        ;;
    sh|bash)
        OUTPUT=$(bash -n "$FILE_PATH" 2>&1)
        EXIT=$?
        ;;
    *)
        exit 0
        ;;
esac

if [ $EXIT -ne 0 ]; then
    echo "[$TIMESTAMP] $FILE_PATH" >> "$ERROR_LOG"
    echo "$OUTPUT" >> "$ERROR_LOG"
    echo "---" >> "$ERROR_LOG"
    echo "⚠️ 검증 실패: $(basename "$FILE_PATH")"
    echo "$OUTPUT"
fi

exit 0
