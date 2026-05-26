#!/bin/bash

# ~/.claude 데이터를 iCloud로 내보내기
# 대상: lancedb, wiki, memory (.gitignore 제외 항목)
# 주의: iCloud 경로에서는 Bash 명령어만 사용 (Read/Write 도구 무한 대기)

ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
BACKUP_DIR="$ICLOUD_DIR/claude-backup"
CLAUDE_DIR="$HOME/.claude"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

echo "📤 Claude 데이터 iCloud 백업 시작..."
echo "대상: $BACKUP_DIR"
echo ""

mkdir -p "$BACKUP_DIR"

for target in lancedb wiki memory; do
    if [ -d "$CLAUDE_DIR/$target" ]; then
        echo "✓ $target 백업 중..."
        rm -rf "$BACKUP_DIR/$target"
        cp -r "$CLAUDE_DIR/$target" "$BACKUP_DIR/$target"
        echo "  완료 ($(du -sh "$CLAUDE_DIR/$target" | cut -f1))"
    else
        echo "  ↳ $target 없음, 건너뜀"
    fi
done

printf "%s\n백업 일시: %s\n" "$TIMESTAMP" "$TIMESTAMP" > "$BACKUP_DIR/backup_timestamp.txt"

echo ""
echo "✅ iCloud 백업 완료!"
echo "경로: $BACKUP_DIR"
echo ""
echo "⚠️  iCloud 동기화 완료까지 잠시 기다린 후 새 Mac으로 이동하세요."
