#!/bin/bash

# 새 Mac에서 Claude Code 환경 전체 복원
# 전제: iCloud가 동기화되어 있어야 함
# 실행 방법: bash ~/cc-sync/scripts/setup-new-mac.sh

set -euo pipefail

ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
BACKUP_DIR="$ICLOUD_DIR/claude-backup"
CLAUDE_DIR="$HOME/.claude"
CC_SYNC_DIR="$HOME/cc-sync"

echo "🚀 새 Mac Claude Code 환경 복원 시작"
echo "================================================"
echo ""

# 1. Homebrew
echo "1️⃣  Homebrew 확인..."
if ! command -v brew &>/dev/null; then
    echo "   Homebrew 설치 중..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Apple Silicon 경로 설정
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "   ✓ Homebrew 이미 설치됨 ($(brew --version | head -1))"
fi

# 2. ollama
echo ""
echo "2️⃣  ollama 설치 및 모델 준비..."
if ! command -v ollama &>/dev/null; then
    echo "   ollama 설치 중..."
    brew install ollama
fi
echo "   ✓ ollama $(ollama --version 2>/dev/null || echo '설치됨')"

brew services start ollama 2>/dev/null || true
echo "   ollama 서비스 기동 대기 중..."
sleep 5

echo "   nomic-embed-text:latest 모델 다운로드 중..."
ollama pull nomic-embed-text:latest
echo "   ✓ 모델 준비 완료"

# 3. Python 패키지
echo ""
echo "3️⃣  Python 패키지 설치 중..."
if command -v pip3 &>/dev/null; then
    pip3 install --quiet lancedb pyarrow
elif command -v pip &>/dev/null; then
    pip install --quiet lancedb pyarrow
else
    echo "   ⚠️  pip를 찾을 수 없습니다. Python3을 먼저 설치하세요."
    echo "      brew install python3"
    exit 1
fi
echo "   ✓ lancedb, pyarrow 설치 완료"

# 4. cc-sync 클론 + apply
echo ""
echo "4️⃣  cc-sync 설정 적용 중..."
if [ ! -d "$CC_SYNC_DIR" ]; then
    echo ""
    echo "   cc-sync 저장소 URL을 입력하세요 (예: https://github.com/yourname/cc-sync):"
    read -r CC_URL
    git clone "$CC_URL" "$CC_SYNC_DIR"
fi
bash "$CC_SYNC_DIR/apply.sh"

# 5. iCloud 데이터 복원
echo ""
echo "5️⃣  iCloud 데이터 복원 중..."

if [ ! -d "$BACKUP_DIR" ]; then
    echo "   ⚠️  iCloud 백업 폴더 없음: $BACKUP_DIR"
    echo "   이전 Mac에서 export.sh를 실행하고 iCloud 동기화를 기다린 후 이 단계를 다시 실행하세요:"
    echo "      bash $CC_SYNC_DIR/scripts/setup-new-mac.sh"
else
    for target in lancedb wiki memory; do
        if [ -d "$BACKUP_DIR/$target" ]; then
            echo "   ✓ $target 복원 중..."
            rm -rf "$CLAUDE_DIR/$target"
            cp -r "$BACKUP_DIR/$target" "$CLAUDE_DIR/$target"
        fi
    done

    if [ -f "$BACKUP_DIR/backup_timestamp.txt" ]; then
        echo ""
        echo "   백업 정보:"
        cat "$BACKUP_DIR/backup_timestamp.txt" | sed 's/^/   /'
    fi
fi

echo ""
echo "================================================"
echo "✅ 환경 복원 완료!"
echo ""
echo "💡 다음 단계:"
echo "   1. Claude Code 설치 (미설치 시):"
echo "      npm install -g @anthropic-ai/claude-code"
echo "   2. 메모리 DB 확인:"
echo "      python3 ~/.claude/bin/mem_db.py --stats"
echo "   3. Claude Code 시작:"
echo "      claude"
