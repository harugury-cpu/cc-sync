#!/usr/bin/env python3
"""기존 ~/.claude/memory/*.md 파일을 LanceDB로 마이그레이션."""

import sys
import os
from pathlib import Path

# mem_db 임포트
sys.path.insert(0, str(Path.home() / ".claude" / "bin"))
import mem_db

MEM_DIR = Path.home() / ".claude" / "memory"

def migrate():
    md_files = sorted(MEM_DIR.glob("*.md"))
    total = len(md_files)
    print(f"마이그레이션 대상: {total}개 파일")

    added = 0
    skipped = 0
    for i, fpath in enumerate(md_files, 1):
        content = fpath.read_text(encoding="utf-8").strip()
        if not content or len(content) < 20:
            skipped += 1
            continue

        # 파일을 청크로 분할 (최대 800자)
        chunks = [content[j:j+800] for j in range(0, len(content), 800)]
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            mem_db.add(chunk, source=fpath.name, agent="migrate")
            added += 1

        if i % 10 == 0:
            print(f"  진행: {i}/{total}...")

    print(f"\n완료: {added}개 청크 저장, {skipped}개 파일 스킵")
    print(f"DB 총 메모리: {mem_db.count()}개")

if __name__ == "__main__":
    migrate()
