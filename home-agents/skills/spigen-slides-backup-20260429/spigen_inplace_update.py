#!/usr/bin/env python3
"""
spigen_inplace_update.py

같은 Google Slides 프레젠테이션 ID를 유지한 채,
우리가 생성한 슬라이드(prefix 기준)만 삭제 후 새 요청을 다시 적용한다.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return r.stdout


def fetch_slides(presentation_id: str) -> list[dict]:
    data = json.loads(
        run(
            [
                "gws",
                "slides",
                "presentations",
                "get",
                "--params",
                json.dumps({"presentationId": presentation_id}),
            ]
        )
    )
    return data.get("slides", [])


def delete_owned_slides(presentation_id: str, prefixes: tuple[str, ...]) -> list[str]:
    slides = fetch_slides(presentation_id)
    owned = [
        s["objectId"]
        for s in slides
        if any(s["objectId"].startswith(prefix) for prefix in prefixes)
    ]
    if owned:
        run(
            [
                "gws",
                "slides",
                "presentations",
                "batchUpdate",
                "--params",
                json.dumps({"presentationId": presentation_id}),
                "--json",
                json.dumps({"requests": [{"deleteObject": {"objectId": oid}} for oid in owned]}, ensure_ascii=False),
            ]
        )
    return owned


def apply_requests(presentation_id: str, requests_path: Path) -> None:
    payload = json.loads(requests_path.read_text())
    run(
        [
            "gws",
            "slides",
            "presentations",
            "batchUpdate",
            "--params",
            json.dumps({"presentationId": presentation_id}),
            "--json",
            json.dumps(payload, ensure_ascii=False),
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("presentation_id")
    ap.add_argument("requests_json")
    ap.add_argument("--prefix", action="append", default=["slide_"])
    args = ap.parse_args()

    deleted = delete_owned_slides(args.presentation_id, tuple(args.prefix))
    apply_requests(args.presentation_id, Path(args.requests_json))
    print(
        json.dumps(
            {
                "status": "ok",
                "presentationId": args.presentation_id,
                "deleted_slide_count": len(deleted),
                "deleted_slide_ids": deleted,
                "requests_json": args.requests_json,
                "url": f"https://docs.google.com/presentation/d/{args.presentation_id}/edit",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
