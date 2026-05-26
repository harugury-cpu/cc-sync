#!/bin/bash
# UserPromptSubmit hook: LanceDB 의미 검색으로 관련 메모리 주입

INPUT=$(cat 2>/dev/null || echo "")
QUERY=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    # hook_event_name = UserPromptSubmit, prompt 필드 추출
    prompt = d.get('prompt', '')
    if isinstance(prompt, list):
        prompt = ' '.join(x.get('text','') for x in prompt if isinstance(x, dict))
    print(str(prompt)[:300])
except:
    pass
" 2>/dev/null || echo "")

OUTPUT=""

# 1. 프로젝트 메모리 (사용자 프로필, 설정, 피드백) — 기존 방식 유지
PROJECT_MEM_DIR="$HOME/.claude/projects/-Users-harugury--cokacdir-workspace-yizd0re4/memory"
for f in user_profile.md project_setup.md feedback.md; do
    FPATH="$PROJECT_MEM_DIR/$f"
    [ -f "$FPATH" ] || continue
    BODY=$(grep -v '^---' "$FPATH" | grep -v '^name:' | grep -v '^description:' | grep -v '^metadata:' | grep -v 'node_type:' | grep -v 'type:' | grep -v 'originSessionId:' | sed '/^$/N;/^\n$/d')
    [ -n "$BODY" ] && OUTPUT="${OUTPUT}${BODY}

"
done

# 2. LanceDB 의미 검색 (ollama가 실행 중인 경우)
if [ -n "$QUERY" ]; then
    SEMANTIC=$(python3 -c "
import sys
sys.path.insert(0, '$HOME/.claude/bin')
try:
    import mem_db
    results = mem_db.search('$QUERY', limit=4)
    if results:
        print('## 관련 기억 (의미 검색)')
        for r in results:
            print(f\"[{r['date']} | {r['source']}]\")
            print(r['content'][:250])
            print('---')
except Exception as e:
    pass
" 2>/dev/null || echo "")
    [ -n "$SEMANTIC" ] && OUTPUT="${OUTPUT}${SEMANTIC}

"
fi

# 3. 직전 세션 메모리 (fallback — LATEST.md)
if [ -z "$SEMANTIC" ]; then
    LATEST="$HOME/.claude/memory/LATEST.md"
    if [ -f "$LATEST" ]; then
        LATEST_CONTENT=$(head -60 "$LATEST" 2>/dev/null || echo "")
        [ -n "$LATEST_CONTENT" ] && OUTPUT="${OUTPUT}${LATEST_CONTENT}"
    fi
fi

[ -n "$OUTPUT" ] || exit 0
printf '<previous-session-memory>\n%s\n</previous-session-memory>\n' "$OUTPUT"
exit 0
