#!/bin/bash
# UserPromptSubmit hook: Obsidian vault를 ripgrep으로 검색해 관련 노트를 컨텍스트로 주입
# 주력 검색 = ripgrep (Tier 4). GraphRAG/온톨로지는 보조.
set -o pipefail

VAULT="/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault"
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

# 2-4. 키워드 추출 → AND 비율 필터링 → 출력
VAULT="$VAULT" QUERY="$QUERY" python3 << 'PYEOF'
import re, sys, subprocess, os

vault = os.environ['VAULT']
query = os.environ['QUERY']

# 키워드 추출 - 한글 4자+, 영문 5자+, 엄격한 불용어 제거
stop = set('''
그래서 그리고 하지만 그런데 그러면 해줘 해줭 확인 알려 보여 이거 저거 그거 무엇 뭐가 뭔지
어디 언제 어떻게 그럼 일단 지금 우리 너의 나의 에서 으로 그게 이게 저게 하자 하는 한거 인거
이런 저런 그런 되는 된거 처럼 까지 부터 마저 그리 정도 관련 진행 완료 진짜 사실 가능 아니
맞아 이제 그때 아직 있음 없음 있는 없는 되고 하고 이다 이라 해야 해도 되면 하면 이면
방법 결과 내용 항목 기능 작업 수정 변경 추가 제거 설명 의미 문제 원인 이유 해결 개선
대화 질문 대답 응답 다음 이전 현재 앞서 이후 부분 전체 모두 각각 여러 하나 두가지 세가지
이렇게 저렇게 어떻게 뭔가 뭐랄 이거 저거 그거 그게 이게 저게 거야 거지 거잖아 거야
'''.split())

toks = re.findall(r'[가-힣]{4,}|[A-Za-z]{5,}', query)
keywords = []
seen = set()
for w in toks:
    wl = w.lower()
    if wl not in stop and wl not in seen:
        keywords.append(w)
        seen.add(wl)
    if len(keywords) >= 8:
        break

if not keywords:
    sys.exit(0)

# 1차: OR 패턴으로 후보 파일 추출 (매칭 행 3줄 이상만)
pattern = '|'.join(re.escape(k) for k in keywords)
result = subprocess.run(
    ['rg', '-c', '-i', '-e', pattern, vault, '--glob', '*.md',
     '--glob', '!**/.venv/**', '--glob', '!**/node_modules/**'],
    capture_output=True, text=True
)

candidates = []
for line in result.stdout.splitlines():
    if ':' not in line:
        continue
    parts = line.rsplit(':', 1)
    try:
        count = int(parts[1])
        if count >= 3:
            candidates.append((count, parts[0]))
    except ValueError:
        continue

candidates.sort(reverse=True)
candidates = candidates[:20]

if not candidates:
    sys.exit(0)

# 2차: 파일 직접 읽어서 AND 비율 체크 (키워드 60% 이상 포함한 파일만)
threshold = max(2, int(len(keywords) * 0.6))
scored = []
for count, fpath in candidates:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        hits = sum(1 for kw in keywords if kw.lower() in content)
        if hits >= threshold:
            scored.append((hits, count, fpath))
    except Exception:
        continue

scored.sort(reverse=True)
top = scored[:3]

if not top:
    sys.exit(0)

print("## 관련 vault 노트 (ripgrep 자동검색)")
print("_아래는 사용자의 Obsidian vault에서 이번 질문 키워드로 자동 검색된 노트입니다. 관련 있으면 근거로 쓰고, 없으면 무시하세요._")
print()

for hits, count, fpath in top:
    rel = fpath[len(vault)+1:]
    r3 = subprocess.run(
        ['rg', '-i', '-m1', '-e', pattern, fpath],
        capture_output=True, text=True
    )
    snippet = (r3.stdout.strip()[:160]) if r3.returncode == 0 else ''
    print(f"- {rel}")
    if snippet:
        print(f"  > {snippet}")

PYEOF

exit 0
