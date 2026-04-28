#!/usr/bin/env python3
"""
서브에이전트 검수 결과를 manifest에 기록하고,
3개가 모두 PASS일 때만 completion_status=COMPLETED 로 바꾼다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest_json")
    ap.add_argument("--planner", required=True, choices=["PASS", "FAIL"])
    ap.add_argument("--designer", required=True, choices=["PASS", "FAIL"])
    ap.add_argument("--audience-feedback", default="")
    args = ap.parse_args()

    path = Path(args.manifest_json)
    data = json.loads(path.read_text())
    data["subagent_reviews"] = {
        "planner": args.planner,
        "designer": args.designer,
    }
    data["audience_feedback"] = {
        "status": "RECORDED" if args.audience_feedback else "SKIPPED",
        "summary": args.audience_feedback,
    }
    all_pass = all(v == "PASS" for v in data["subagent_reviews"].values())
    data["completion_status"] = "COMPLETED" if all_pass else "BLOCKED"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    print(json.dumps({
        "status": data["completion_status"],
        "subagent_reviews": data["subagent_reviews"],
        "manifest": str(path),
    }, ensure_ascii=False, indent=2))
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main())
