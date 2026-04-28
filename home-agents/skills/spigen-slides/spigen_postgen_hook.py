#!/usr/bin/env python3
"""
spigen_postgen_hook.py

Spigen Slides 생성 직후 반드시 실행하는 강제 검수 훅.

역할:
1. preview HTML verify 강제 (선택 입력이지만 strict 기준에서는 사실상 필수)
2. spigen_verify.py 수치 검증 강제
3. 전체 슬라이드 썸네일 수집 강제
4. 서브에이전트 검수 입력 번들(manifest) 생성
5. strict 모드에서는 "검수 전 완료 보고 금지" 상태코드로 종료
"""

from __future__ import annotations

import argparse
import json
import ssl
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFY = HERE / "spigen_verify.py"
PREVIEW_VERIFY = HERE / "spigen_preview_verify.py"
PROMPTS = HERE / "spigen_subagent_prompts.md"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def pick_python(required_module: str = "") -> str:
    candidates = [
        sys.executable,
        "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3",
        "/usr/local/bin/python3",
        "/usr/bin/python3",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if not required_module:
            return candidate
        probe = subprocess.run(
            [
                candidate,
                "-c",
                f"import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('{required_module}') else 1)",
            ],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            return candidate
    return sys.executable


def fetch_presentation(presentation_id: str) -> dict:
    res = run(
        [
            "gws",
            "slides",
            "presentations",
            "get",
            "--params",
            json.dumps({"presentationId": presentation_id}),
        ]
    )
    return json.loads(res.stdout)


def run_verify(presentation_id: str) -> subprocess.CompletedProcess:
    return run([pick_python(), str(VERIFY), presentation_id], check=False)


def run_preview_verify(preview_html: str, slides: int, out_dir: Path) -> subprocess.CompletedProcess:
    return run(
        [
            pick_python("playwright"),
            str(PREVIEW_VERIFY),
            preview_html,
            "--slides",
            str(slides),
            "--output",
            str(out_dir),
        ],
        check=False,
    )


def download_thumbnails(presentation_id: str, slides: list[dict], out_dir: Path) -> list[dict]:
    out = []
    thumbs_dir = out_dir / "thumbnails"
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    ssl_context = ssl._create_unverified_context()
    for idx, slide in enumerate(slides):
        slide_id = slide["objectId"]
        thumb = run(
            [
                "gws",
                "slides",
                "presentations",
                "pages",
                "getThumbnail",
                "--params",
                json.dumps({"presentationId": presentation_id, "pageObjectId": slide_id}),
            ]
        )
        url = json.loads(thumb.stdout).get("contentUrl", "")
        path = thumbs_dir / f"{idx:02d}_{slide_id}.png"
        with urllib.request.urlopen(url, context=ssl_context) as resp:
            path.write_bytes(resp.read())
        out.append(
            {
                "index": idx,
                "slide_id": slide_id,
                "thumbnail_path": str(path),
                "thumbnail_url": url,
            }
        )
    return out


def build_manifest(
    presentation_id: str,
    verify_res: subprocess.CompletedProcess,
    preview_verify: dict,
    slide_entries: list[dict],
    audience: str,
    purpose: str,
) -> dict:
    verify_ok = verify_res.returncode == 0
    preview_ok = preview_verify.get("ok", False)
    return {
        "status": "SUBAGENT_REVIEW_REQUIRED" if (verify_ok and preview_ok) else "VERIFY_FAILED",
        "presentation_id": presentation_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "preview_verify": preview_verify,
        "verify": {
            "ok": verify_ok,
            "returncode": verify_res.returncode,
            "stdout_path": "verify.txt",
        },
        "inputs": {
            "audience": audience,
            "purpose": purpose,
        },
        "review_sequence": [
            "planner_subagent_required",
            "designer_subagent_required",
            "audience_subagent_feedback_only",
        ],
        "subagent_reviews": {
            "planner": "PENDING",
            "designer": "PENDING",
        },
        "audience_feedback": {
            "status": "PENDING",
            "summary": "",
        },
        "completion_status": "BLOCKED",
        "required_files": {
            "subagent_prompts": str(PROMPTS),
            "design_spec": str(HERE / "spigen_design_spec.md"),
            "review_checklist": str(HERE / "spigen_review_checklist.md"),
        },
        "slides": slide_entries,
        "hard_gate": [
            "이 manifest가 생성되지 않으면 완료로 보고 금지",
            "preview verify FAIL이면 Slides 생성 성공이어도 완료로 보고 금지",
            "verify FAIL/MISS가 있으면 수정 후 재생성/재반영",
            "thumbnail 확인 없이 완료로 보고 금지",
            "planner PASS 없이 완료로 보고 금지",
            "designer PASS 없이 완료로 보고 금지",
            "audience는 PASS/FAIL 대상이 아니라 feedback 수집 대상이다",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("presentation_id")
    ap.add_argument("--audience", default="")
    ap.add_argument("--purpose", default="")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--preview-html", default="")
    ap.add_argument("--preview-slides", type=int, default=0)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    bundle_dir = (
        Path(args.out_dir).expanduser()
        if args.out_dir
        else Path("/tmp") / f"spigen_review_{args.presentation_id}"
    )
    bundle_dir.mkdir(parents=True, exist_ok=True)

    preview_verify_info = {
        "ok": False,
        "skipped": not bool(args.preview_html),
        "returncode": None,
        "stdout_path": "",
        "report_path": "",
    }
    if args.preview_html:
        preview_dir = bundle_dir / "preview_verify"
        preview_dir.mkdir(parents=True, exist_ok=True)
        preview_res = run_preview_verify(args.preview_html, args.preview_slides or 0, preview_dir)
        (preview_dir / "stdout.txt").write_text(
            preview_res.stdout + ("\n" + preview_res.stderr if preview_res.stderr else ""),
            encoding="utf-8",
        )
        preview_verify_info = {
            "ok": preview_res.returncode == 0,
            "skipped": False,
            "returncode": preview_res.returncode,
            "stdout_path": str(preview_dir / "stdout.txt"),
            "report_path": str(preview_dir / "preview_verify_report.json"),
        }

    verify_res = run_verify(args.presentation_id)
    (bundle_dir / "verify.txt").write_text(
        verify_res.stdout + ("\n" + verify_res.stderr if verify_res.stderr else ""),
        encoding="utf-8",
    )

    if verify_res.returncode != 0 or (args.preview_html and not preview_verify_info["ok"]):
        manifest = build_manifest(
            args.presentation_id,
            verify_res,
            preview_verify_info,
            [],
            args.audience,
            args.purpose,
        )
        (bundle_dir / "review_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": "VERIFY_FAILED",
                    "bundle_dir": str(bundle_dir),
                    "preview_verify": preview_verify_info,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    prs = fetch_presentation(args.presentation_id)
    slide_entries = download_thumbnails(args.presentation_id, prs.get("slides", []), bundle_dir)
    manifest = build_manifest(
        args.presentation_id,
        verify_res,
        preview_verify_info,
        slide_entries,
        args.audience,
        args.purpose,
    )
    (bundle_dir / "review_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": manifest["status"],
                "bundle_dir": str(bundle_dir),
                "manifest": str(bundle_dir / "review_manifest.json"),
                "verify": str(bundle_dir / "verify.txt"),
                "preview_verify": preview_verify_info,
                "completion_status": "BLOCKED",
                "thumbnail_count": len(slide_entries),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    if args.strict:
        print("SUBAGENT_REVIEWS_PENDING")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
