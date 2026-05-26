#!/usr/bin/env python3
"""
LanceDB 기반 에이전트 메모리 인프라.
- ollama nomic-embed-text로 로컬 임베딩
- ~/.claude/lancedb/에 저장
- 모든 에이전트(Claude, Codex 등) 공유
"""

import os
import sys
import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

DB_PATH = str(Path.home() / ".claude" / "lancedb")
TABLE_NAME = "memories"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768


def embed(text: str) -> list[float]:
    """ollama nomic-embed-text로 벡터 생성."""
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["embedding"]
    except Exception as e:
        print(f"[mem_db] 임베딩 실패: {e}", file=sys.stderr)
        return [0.0] * EMBED_DIM


def get_table():
    """LanceDB 테이블 반환 (없으면 생성)."""
    import lancedb
    import pyarrow as pa

    db = lancedb.connect(DB_PATH)
    if TABLE_NAME in db.table_names():
        return db.open_table(TABLE_NAME)

    schema = pa.schema([
        pa.field("id", pa.string()),
        pa.field("source", pa.string()),
        pa.field("date", pa.string()),
        pa.field("content", pa.string()),
        pa.field("agent", pa.string()),
        pa.field("vector", pa.list_(pa.float32(), EMBED_DIM)),
    ])
    return db.create_table(TABLE_NAME, schema=schema)


def add(content: str, source: str = "manual", agent: str = "claude") -> str:
    """메모리 추가. 중복 ID면 건너뜀."""
    doc_id = hashlib.md5(content.encode()).hexdigest()[:12]
    tbl = get_table()

    # 중복 확인
    try:
        existing = tbl.search().where(f"id = '{doc_id}'").limit(1).to_list()
        if existing:
            return doc_id
    except Exception:
        pass

    vector = embed(content)
    row = {
        "id": doc_id,
        "source": source,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": content,
        "agent": agent,
        "vector": vector,
    }
    import pyarrow as pa
    tbl.add([row])
    return doc_id


def search(query: str, limit: int = 5) -> list[dict]:
    """의미 검색. 가장 관련 있는 메모리 반환."""
    tbl = get_table()
    vec = embed(query)
    results = (
        tbl.search(vec)
        .limit(limit)
        .to_list()
    )
    return [{"content": r["content"], "source": r["source"],
             "date": r["date"], "score": r.get("_distance", 0)} for r in results]


def count() -> int:
    return get_table().count_rows()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "add":
        content = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
        source = sys.argv[3] if len(sys.argv) > 3 else "cli"
        doc_id = add(content, source)
        print(f"저장: {doc_id}")

    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read().strip()
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        results = search(query, limit)
        for r in results:
            print(f"[{r['date']} | {r['source']}]")
            print(r["content"][:300])
            print("---")

    elif cmd == "count":
        print(f"총 메모리: {count()}개")

    else:
        print("사용법: mem_db.py [add|search|count] [인자...]")
