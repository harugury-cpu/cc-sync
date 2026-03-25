#!/bin/bash

# cc-sync 프로젝트에서 로컬로 memory-bank sync 데이터를 가져오는 스크립트
# 다른 디바이스에서 git pull 후 실행

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SYNC_TARGET="$HOME/.config/superpowers/conversation-index/sync"
SYNC_SOURCE="$SCRIPT_DIR/memory-bank-sync"

if [ ! -d "$SYNC_SOURCE" ]; then
    echo "⚠️  memory-bank-sync 폴더가 없습니다. 먼저 git pull 하세요."
    exit 1
fi

echo "🔄 memory-bank sync 데이터 가져오기..."
echo "Source: $SYNC_SOURCE"
echo "Target: $SYNC_TARGET"
echo ""

mkdir -p "$SYNC_TARGET"
cp "$SYNC_SOURCE"/* "$SYNC_TARGET/" 2>/dev/null

echo "✅ memory-bank sync import 완료!"
echo "   다음 세션 시작 시 sync-import-hook.js가 자동으로 local DB에 병합합니다."
