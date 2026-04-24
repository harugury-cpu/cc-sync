#!/bin/bash

# ~/.claude 설정을 cc-sync 프로젝트로 동기화하는 스크립트
# 방향: ~/.claude/ → cc-sync (Git)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$HOME/.claude"

sync_dir() {
    local src="$1" dst="$2"
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        cp -r "$src"/* "$dst"/ 2>/dev/null
        find "$dst" -type d -name .git -prune -exec rm -rf {} + 2>/dev/null
    fi
}

echo "🔄 Claude Code 설정 동기화 중..."
echo "Source: $SOURCE_DIR"
echo "Target: $SCRIPT_DIR"
echo ""

# 디렉토리 동기화
for dir in agents hooks skills memory plugins commands scripts rules teams data; do
    if [ -d "$SOURCE_DIR/$dir" ]; then
        echo "✓ $dir 동기화 중..."
        sync_dir "$SOURCE_DIR/$dir" "$SCRIPT_DIR/$dir"
    fi
done

# ~/.agents 동기화 → home-agents/
if [ -d "$HOME/.agents" ]; then
    echo "✓ ~/.agents 동기화 중..."
    sync_dir "$HOME/.agents" "$SCRIPT_DIR/home-agents"
fi

# .opencode 동기화 (선택)
if [ -d "$HOME/.opencode" ]; then
    echo "✓ .opencode 동기화 중..."
    sync_dir "$HOME/.opencode" "$SCRIPT_DIR/.opencode"
fi

# 단일 파일 동기화
for file in settings.json CLAUDE.md keybindings.json claude_desktop_config.json settings.local.json claude_code_config.json MANAGER_ORCHESTRATOR_ROLES.md; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        echo "✓ $file 동기화 중..."
        cp "$SOURCE_DIR/$file" "$SCRIPT_DIR/"
    fi
done

# memory-bank sync 데이터 (멀티 디바이스 동기화)
SYNC_SOURCE="$HOME/.config/superpowers/conversation-index/sync"
if [ -d "$SYNC_SOURCE" ]; then
    echo "✓ memory-bank sync 동기화 중..."
    mkdir -p "$SCRIPT_DIR/memory-bank-sync"
    cp "$SYNC_SOURCE"/* "$SCRIPT_DIR/memory-bank-sync/" 2>/dev/null
fi

echo ""
echo "✅ 동기화 완료!"

# --auto 플래그: 자동 커밋 + push
if [[ "$1" == "--auto" ]]; then
    cd "$SCRIPT_DIR"
    rm -f .git/index.lock 2>/dev/null
    if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "cc-sync: 자동 동기화 $(date '+%Y-%m-%d %H:%M')"
        git push 2>/dev/null
        echo "✅ 자동 커밋 & Push 완료!"
    else
        echo "ℹ️  변경사항 없음"
    fi
    exit 0
fi

echo ""
echo "Git에 커밋하시겠습니까? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    cd "$SCRIPT_DIR"
    git add .
    git status
    echo ""
    echo "커밋 메시지를 입력하세요:"
    read -r commit_msg
    git commit -m "$commit_msg"
    echo ""
    echo "원격 저장소에 push하시겠습니까? (y/n)"
    read -r push_response
    if [[ "$push_response" =~ ^[Yy]$ ]]; then
        git push
        echo "✅ Push 완료!"
    fi
fi
