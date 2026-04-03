#!/bin/bash
# context-enrichment.sh
# UserPromptSubmit 트리거 - 매 프롬프트마다 프로젝트 컨텍스트 자동 주입

PROJECT_ROOT=$(pwd)

# Git 레포인 경우에만 실행
if ! git -C "$PROJECT_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
    exit 0
fi

OUTPUT="<context-snapshot>\n"

# 최근 변경 파일
CHANGED=$(git -C "$PROJECT_ROOT" status --short 2>/dev/null | head -10)
if [ -n "$CHANGED" ]; then
    OUTPUT+="[변경된 파일]\n$CHANGED\n\n"
fi

# 최근 커밋 3개
COMMITS=$(git -C "$PROJECT_ROOT" log --oneline -3 2>/dev/null)
if [ -n "$COMMITS" ]; then
    OUTPUT+="[최근 커밋]\n$COMMITS\n\n"
fi

# 최근 검증 에러 (auto-validate에서 기록)
ERROR_LOG="/tmp/claude-validation-error.log"
if [ -f "$ERROR_LOG" ]; then
    RECENT_ERROR=$(tail -15 "$ERROR_LOG" 2>/dev/null)
    if [ -n "$RECENT_ERROR" ]; then
        OUTPUT+="[최근 검증 에러]\n$RECENT_ERROR\n\n"
    fi
fi

OUTPUT+="</context-snapshot>"
printf "%b" "$OUTPUT"
exit 0
