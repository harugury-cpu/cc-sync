#!/bin/bash
# UserPromptSubmit hook: Obsidian vault를 ripgrep으로 검색해 관련 노트를 컨텍스트로 주입
# 주력 검색 = ripgrep (Tier 4). GraphRAG/온톨로지는 보조.
set -o pipefail

VAULT="/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault"
[ -d "$VAULT" ] || exit 0
command -v rg >/dev/null 2>&1 || exit 0

INPUT=$(cat 2>/dev/null || echo "")

# 1. user prompt 추출
QUERY=$(printf '%s' "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    p = d.get('prompt', '')
    if isinstance(p, list):
        p = ' '.join(x.get('text','') for x in p if isinstance(x, dict))
    print(str(p)[:400])
except Exception:
    pass
" 2>/dev/null)
[ -z "$QUERY" ] && exit 0

# 2. 키워드 토큰 추출 (2자+ 한글 / 3자+ 영숫자, 불용어 제외)
TOKENS=$(printf '%s' "$QUERY" | python3 -c "
import re, sys
t = sys.stdin.read()
stop = set('그래서 그리고 하지만 그런데 그러면 해줘 해줭 확인 알려 보여 이거 저거 그거 무엇 뭐가 뭔지 어디 언제 어떻게 그럼 일단 지금 우리 너의 나의 에서 으로 그게 이게 저게 하자 하는 한거 인거 이런 저런 그런 되는 된거 으로 처럼 까지 부터 마저 그리 정도 관련 진행 확인해'.split())
toks = re.findall(r'[가-힣]{2,}|[A-Za-z0-9]{3,}', t)
seen = []
for w in toks:
    if w in stop or w in seen:
        continue
    seen.append(w)
print('\n'.join(seen[:12]))
" 2>/dev/null)
[ -z "$TOKENS" ] && exit 0

# 3. OR 패턴으로 rg, 파일별 매칭수 상위 4개
PATTERN=$(printf '%s' "$TOKENS" | paste -sd '|' -)
TOPFILES=$(rg -c -i -e "$PATTERN" "$VAULT" --glob '*.md' --glob '!**/.venv/**' --glob '!**/node_modules/**' 2>/dev/null \
  | sort -t: -k2 -rn | head -4 | cut -d: -f1)
[ -z "$TOPFILES" ] && exit 0

# 4. 각 노트에서 대표 매칭 라인 1개 + 상대경로 출력
echo "## 관련 vault 노트 (ripgrep 자동검색)"
echo "_아래는 사용자의 Obsidian vault에서 이번 질문 키워드로 자동 검색된 노트입니다. 관련 있으면 근거로 쓰고, 없으면 무시하세요._"
echo
while IFS= read -r f; do
    [ -z "$f" ] && continue
    rel="${f#$VAULT/}"
    snippet=$(rg -i -m1 -e "$PATTERN" "$f" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' | cut -c1-160)
    echo "- ${rel}"
    [ -n "$snippet" ] && echo "  > ${snippet}"
done <<< "$TOPFILES"

exit 0
