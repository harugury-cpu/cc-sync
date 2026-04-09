#!/bin/bash
# PreToolUse: git commit / clasp push 전 기획 플로우 검증 체크리스트

COMMAND=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('command',''))
except:
    print('')
" 2>/dev/null)

echo "$COMMAND" | grep -qE '(git\s+commit|clasp\s+push)' || exit 0

# 대상 파일 결정: git commit이면 staged, clasp push면 현재 디렉토리 .gs 파일
if echo "$COMMAND" | grep -qE 'git\s+commit'; then
    STAGED=$(git diff --cached --name-only 2>/dev/null)
else
    # clasp push: 현재 디렉토리의 .gs 파일
    STAGED=$(find . -maxdepth 1 -name "*.gs" 2>/dev/null)
fi

echo "$STAGED" | grep -qiE '\.(js|ts|gs)$' || exit 0

HAS_AUTOMATION=0
while IFS= read -r file; do
    if [ -f "$file" ] && grep -qiE '(filter|trigger|doPost|processWebhook|\.update|mapping|findIndex|getDataRange)' "$file" 2>/dev/null; then
        HAS_AUTOMATION=1
        break
    fi
done <<< "$STAGED"

[ $HAS_AUTOMATION -eq 0 ] && exit 0

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 기획 플로우 검증 — 배포 전 확인 필요"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "[ 조건 검증 ]"
echo "  1. 기획에서 데이터를 식별하는 조건이 몇 개인가요?"
echo "     코드에서 그 조건을 모두 사용했나요?"
echo "     예) A열(기종) + B열(라인업) → 코드에 두 조건 모두 있나?"
echo ""
echo "[ 분기 검증 ]"
echo "  2. 플로우의 분기(if/else) 개수와 코드의 분기가 일치하나요?"
echo "  3. 각 분기의 결과(업데이트/알림/skip)가 기획과 같나요?"
echo ""
echo "[ 테스트 ]"
echo "  4. 각 분기를 실제 데이터로 모두 테스트했나요?"
echo "  5. 값이 없거나 매핑 실패하는 케이스도 확인했나요?"
echo ""
echo "  ✅ 위 항목 모두 확인 후 다시 실행하세요."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "BLOCK"
exit 1
