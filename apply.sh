#!/bin/bash

# cc-sync 프로젝트의 설정을 ~/.claude/로 적용하는 스크립트
# 방향: cc-sync (Git) → ~/.claude/

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_DIR="$HOME/.claude"

sync_dir() {
    local src="$1" dst="$2"
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        rsync -a --delete "$src"/ "$dst"/
        rm -rf "$dst/.git" 2>/dev/null
    fi
}

echo "📦 Claude Code 설정 적용 중..."
echo "Source: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"
echo ""

mkdir -p "$TARGET_DIR"

# 디렉토리 복사
for dir in agents hooks skills memory plugins commands scripts rules teams; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        echo "✓ $dir 복사 중..."
        sync_dir "$SCRIPT_DIR/$dir" "$TARGET_DIR/$dir"
    fi
done

# .opencode 복사 (선택)
if [ -d "$SCRIPT_DIR/.opencode" ]; then
    echo "✓ .opencode 복사 중..."
    sync_dir "$SCRIPT_DIR/.opencode" "$HOME/.opencode"
fi

# 단일 파일 복사
for file in settings.json CLAUDE.md keybindings.json claude_desktop_config.json settings.local.json claude_code_config.json MANAGER_ORCHESTRATOR_ROLES.md; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "✓ $file 복사 중..."
        cp "$SCRIPT_DIR/$file" "$TARGET_DIR/"
    fi
done

# memory-bank sync 데이터 (멀티 디바이스 동기화)
SYNC_TARGET="$HOME/.config/superpowers/conversation-index/sync"
if [ -d "$SCRIPT_DIR/memory-bank-sync" ]; then
    echo "✓ memory-bank sync 복사 중..."
    mkdir -p "$SYNC_TARGET"
    cp "$SCRIPT_DIR/memory-bank-sync"/* "$SYNC_TARGET/" 2>/dev/null
fi

# settings.json 경로 치환 ($HOME 기준으로 자동 보정)
if [ -f "$TARGET_DIR/settings.json" ]; then
    echo "✓ settings.json 경로 치환 중 ($HOME)..."
    sed -i '' "s|/Users/[^/\"']*/|$HOME/|g" "$TARGET_DIR/settings.json"
fi

# hooks, scripts 실행 권한 부여
echo "✓ 실행 권한 설정 중..."
chmod +x "$TARGET_DIR/hooks"/*.sh 2>/dev/null
chmod +x "$TARGET_DIR/scripts"/*.sh 2>/dev/null

echo ""
echo "✅ 설정 적용 완료!"
echo ""
echo "💡 Claude Code를 재시작하세요: claude restart"
