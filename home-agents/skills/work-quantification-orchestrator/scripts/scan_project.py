#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


KEYWORDS = {
    "PRD": ["prd", "요구", "기획"],
    "Apps Script": [".gs"],
    "HTML": [".html"],
    "Mermaid": [".mmd", "mermaid"],
    "Draw.io": [".drawio"],
    "Markdown": [".md"],
    "Spreadsheet": [".xlsx", ".csv", ".tsv"],
}


def classify(path: Path) -> list[str]:
    name = path.name.lower()
    hits = []
    for label, keys in KEYWORDS.items():
        if any(k in name for k in keys):
            hits.append(label)
    return hits or ["기타"]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: scan_project.py <PROJECT_DIR>")
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.exists():
        print(f"not found: {root}")
        return 1

    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    grouped: dict[str, list[Path]] = {}
    for p in files:
        rel = p.relative_to(root)
        for label in classify(p):
            grouped.setdefault(label, []).append(rel)

    print(f"# 프로젝트 스캔 결과\n")
    print(f"- root: {root}")
    print(f"- files: {len(files)}\n")

    for label in ["PRD", "Apps Script", "HTML", "Markdown", "Mermaid", "Draw.io", "Spreadsheet", "기타"]:
        items = grouped.get(label, [])
        if not items:
            continue
        print(f"## {label}")
        for rel in sorted(items)[:30]:
            print(f"- {rel}")
        if len(items) > 30:
            print(f"- ... +{len(items) - 30} more")
        print()

    print("## 구현 점검 질문")
    checks = [
        "완료 이벤트를 append-only로 저장하는 탭/함수가 있는가?",
        "원래 업무 item ID + 담당자로 업무로그를 찾는 함수가 있는가?",
        "라인업코드 기준 설문 배치 생성 함수가 있는가?",
        "설문응답원본 append와 업무로그 최신값 갱신이 분리되어 있는가?",
        "계산결과를 룰 탭 기준으로 재생성할 수 있는가?",
        "관리자 재설문이 기존 업무를 덮어쓰는가?",
        "지원파트 시간이 설문 응답과 분리되어 저장되는가?",
    ]
    for check in checks:
        print(f"- [ ] {check}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
