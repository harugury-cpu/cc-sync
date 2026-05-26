#!/usr/bin/env python3
"""
LLM Wiki 자동 축적 (Layer 2).
LanceDB에 저장된 메모리를 주제별 마크다운 wiki로 정리.
~/.claude/wiki/ 에 저장.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.home() / ".claude" / "bin"))
import mem_db

WIKI_DIR = Path.home() / ".claude" / "wiki"
WIKI_DIR.mkdir(exist_ok=True)

TOPICS = {
    "성향_말투": ["성향", "말투", "반응", "유머", "직접성", "짜증"],
    "관심사_고민": ["관심사", "고민", "커리어", "이직", "인생"],
    "작업_프로젝트": ["작업", "프로젝트", "구현", "개발", "설치", "구축"],
    "도구_환경": ["LanceDB", "ollama", "Python", "Claude", "Codex", "brew", "도구"],
    "보안_제약": ["보안", "외부 전송", "iCloud", "제약", "정책"],
}

def build():
    print(f"Wiki 빌드 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    for topic, keywords in TOPICS.items():
        wiki_file = WIKI_DIR / f"{topic}.md"
        results = []
        
        for kw in keywords:
            hits = mem_db.search(kw, limit=3)
            for h in hits:
                # 중복 제거 (content 앞 100자 기준)
                key = h["content"][:100]
                if not any(key == r["content"][:100] for r in results):
                    results.append(h)
        
        if not results:
            continue
        
        with open(wiki_file, "w", encoding="utf-8") as f:
            f.write(f"# {topic.replace('_', ' ')}\n")
            f.write(f"*마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            
            for r in results[:10]:
                f.write(f"## [{r['date']} | {r['source']}]\n")
                f.write(r["content"][:400] + "\n\n---\n\n")
        
        print(f"  ✅ {topic}.md ({len(results[:10])}개 항목)")
    
    # 인덱스 파일
    index_file = WIKI_DIR / "INDEX.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("# 에이전트 메모리 Wiki\n\n")
        f.write(f"*빌드: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write(f"DB 총 메모리: {mem_db.count()}개\n\n")
        for topic in TOPICS:
            wiki_file = WIKI_DIR / f"{topic}.md"
            if wiki_file.exists():
                f.write(f"- [[{topic}]]\n")
    
    print(f"\n✅ Wiki 빌드 완료: {WIKI_DIR}")
    print(f"   파일: {list(WIKI_DIR.glob('*.md'))}")

if __name__ == "__main__":
    build()
