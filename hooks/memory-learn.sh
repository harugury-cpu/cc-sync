#!/bin/bash
# Stop hook: 세션 종료 시 핵심 내용 자동 추출 → ~/.claude/memory/ 저장

set -uo pipefail

# 재귀 방지: memory-learn이 spawning한 claude -p 서브세션이면 스킵
[ -z "${CLAUDE_SKIP_MEMORY_LEARN:-}" ] || exit 0

MEM_DIR="$HOME/.claude/memory"
mkdir -p "$MEM_DIR"

INPUT=$(cat 2>/dev/null || echo "")
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")
[ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ] || exit 0

# JSONL 파싱: 사용자/어시스턴트 메시지만 추출
TURNS=$(python3 -c "
import json, sys
msgs = []
try:
    with open(sys.argv[1], encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line.strip())
                t = d.get('type', '')
                if t not in ('user', 'assistant'):
                    continue
                c = d.get('message', {}).get('content', '')
                if isinstance(c, list):
                    c = ' '.join(x.get('text','') for x in c if isinstance(x, dict) and x.get('type')=='text')
                c = str(c).strip()
                if not c or c.startswith('<local-command') or c.startswith('<system'):
                    continue
                msgs.append(('U' if t=='user' else 'A') + ': ' + c[:400])
            except:
                pass
except:
    pass
print('\n'.join(msgs[-20:]))
" "$TRANSCRIPT_PATH" 2>/dev/null || echo "")

# 5턴 미만 세션 스킵
TURN_COUNT=$(echo "$TURNS" | grep -c '^[UA]:' 2>/dev/null || echo 0)
[ "$TURN_COUNT" -ge 5 ] || exit 0

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
SESSION_FILE="$MEM_DIR/session_${DATE}_${TIME}.md"
TURNS_COPY="$TURNS"

# 완전 분리된 백그라운드 프로세스 (부모 쉘 즉시 종료)
(
    setsid bash -c "
        PROMPT='다음 AI 대화에서 다음 세션에 유용한 정보를 추출하라. 없는 항목은 완전히 생략.

대화:
${TURNS_COPY}

형식 (없는 항목 생략):
## 사용자 선호/패턴
-

## 내린 결정
-

## 진행 중 작업
-

## 주의사항
- '

        EXTRACT=\$(echo \"\$PROMPT\" | CLAUDE_SKIP_MEMORY_LEARN=1 timeout 90 claude -p 2>/dev/null | head -30 || echo '')
        [ -n \"\$EXTRACT\" ] || exit 0

        {
            echo '# 세션: ${DATE} ${TIME}'
            echo ''
            echo \"\$EXTRACT\"
            echo ''
        } > '${SESSION_FILE}'

        {
            echo '# 이전 세션 메모리'
            echo ''
            ls -t '${MEM_DIR}'/session_*.md 2>/dev/null | head -3 | while IFS= read -r f; do
                cat \"\$f\"
                echo '---'
            done
        } > '${MEM_DIR}/LATEST.md'

        echo '💾 [MEMORY-LEARN] 저장: ${SESSION_FILE}' >&2
    " > /dev/null 2>&1
) &
disown $!

exit 0
