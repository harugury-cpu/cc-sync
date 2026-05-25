#!/bin/bash
# UserPromptSubmit hook: 이전 세션 메모리 + 프로젝트 메모리 + MCP 지식 그래프를 컨텍스트에 주입

OUTPUT=""

# 1. 프로젝트 메모리 (사용자 프로필, 설정, 피드백)
PROJECT_MEM_DIR="$HOME/.claude/projects/-Users-harugury--cokacdir-workspace-yizd0re4/memory"
for f in user_profile.md project_setup.md feedback.md; do
    FPATH="$PROJECT_MEM_DIR/$f"
    [ -f "$FPATH" ] || continue
    BODY=$(grep -v '^---' "$FPATH" | grep -v '^name:' | grep -v '^description:' | grep -v '^metadata:' | grep -v 'node_type:' | grep -v 'type:' | grep -v 'originSessionId:' | sed '/^$/N;/^\n$/d')
    [ -n "$BODY" ] && OUTPUT="${OUTPUT}${BODY}

"
done

# 2. MCP 지식 그래프 엔티티
MCP_MEM="$HOME/.claude/mcp-memory.json"
if [ -f "$MCP_MEM" ]; then
    MCP_CONTENT=$(python3 -c "
import json, sys
try:
    with open('$MCP_MEM', encoding='utf-8') as f:
        data = json.load(f)
    entities = data.get('entities', [])
    if not entities:
        sys.exit(0)
    print('## MCP 지식 그래프')
    for e in entities:
        name = e.get('name', '')
        etype = e.get('entityType', '')
        obs = e.get('observations', [])
        print(f'### {name} ({etype})')
        for o in obs:
            print(f'- {o}')
except:
    pass
" 2>/dev/null || echo "")
    [ -n "$MCP_CONTENT" ] && OUTPUT="${OUTPUT}${MCP_CONTENT}

"
fi

# 3. 직전 세션 메모리
LATEST="$HOME/.claude/memory/LATEST.md"
if [ -f "$LATEST" ]; then
    LATEST_CONTENT=$(head -60 "$LATEST" 2>/dev/null || echo "")
    [ -n "$LATEST_CONTENT" ] && OUTPUT="${OUTPUT}${LATEST_CONTENT}"
fi

[ -n "$OUTPUT" ] || exit 0

printf '<previous-session-memory>\n%s\n</previous-session-memory>\n' "$OUTPUT"
exit 0
