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

# 1. LLM Wiki 요약 (vault 정본) — 항상 필요한 사용자 맥락(목차+성향)만 고정 주입.
#    나머지 칸(관심사·작업·도구·보안)은 vault-search.sh가 키워드 매칭 시 자동 주입.
WIKI_DIR="/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/_wiki"
for f in INDEX.md 성향_말투.md; do
    FPATH="$WIKI_DIR/$f"
    [ -f "$FPATH" ] || continue
    BODY=$(grep -v '^---$' "$FPATH")
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
        LATEST_CONTENT=$(head -20 "$LATEST" 2>/dev/null || echo "")
        [ -n "$LATEST_CONTENT" ] && OUTPUT="${OUTPUT}${LATEST_CONTENT}"
    fi
fi

[ -n "$OUTPUT" ] || exit 0
printf '<previous-session-memory>\n%s\n</previous-session-memory>\n' "$OUTPUT"
exit 0
