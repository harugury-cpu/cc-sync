#!/usr/bin/env python3
"""
spigen_preview_verify.py

Spigen preview HTML을 Playwright로 열어 슬라이드별 스크린샷과
console/page error를 수집하는 preflight 검증기.
huashu-design/scripts/verify.py 구조를 spigen preview용으로 이식한 버전.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_viewport(s: str) -> dict:
    w, h = s.split("x")
    return {"width": int(w), "height": int(h)}


def verify_preview(
    html_path: str,
    viewports: list[dict] | None = None,
    slides: int = 0,
    output_dir: str | None = None,
    show: bool = False,
    wait: int = 1000,
) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright가 설치되지 않았습니다.")
        print("실행: pip install playwright && playwright install chromium")
        return 1

    html_file = Path(html_path).resolve()
    if not html_file.exists():
        print(f"ERROR: 파일이 없습니다: {html_file}")
        return 1

    if output_dir is None:
        output_dir = str(html_file.parent / f"{html_file.stem}_screenshots")
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if viewports is None:
        viewports = [{"width": 1440, "height": 900}]

    console_errors: list[str] = []
    page_errors: list[str] = []
    screenshots: list[str] = []
    file_url = html_file.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not show)
        for viewport in viewports:
            context = browser.new_context(viewport=viewport, device_scale_factor=2)
            page = context.new_page()
            page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)))

            page.goto(file_url, wait_until="networkidle")
            page.wait_for_timeout(wait)

            if slides > 0:
                for i in range(slides):
                    shot = out_dir / f"{html_file.stem}-slide-{str(i + 1).zfill(2)}.png"
                    page.screenshot(path=str(shot), full_page=False)
                    screenshots.append(str(shot))
                    if i < slides - 1:
                        page.keyboard.press("ArrowRight")
                        page.wait_for_timeout(300)
            else:
                suffix = f"-{viewport['width']}x{viewport['height']}" if len(viewports) > 1 else ""
                shot = out_dir / f"{html_file.stem}{suffix}.png"
                page.screenshot(path=str(shot), full_page=False)
                screenshots.append(str(shot))

            context.close()
        browser.close()

    report = {
        "html_path": str(html_file),
        "output_dir": str(out_dir),
        "console_errors": console_errors,
        "page_errors": page_errors,
        "screenshots": screenshots,
        "ok": not page_errors,
    }
    (out_dir / "preview_verify_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_path")
    ap.add_argument("--viewports", default="1440x900")
    ap.add_argument("--slides", type=int, default=0)
    ap.add_argument("--output", default=None)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--wait", type=int, default=1000)
    args = ap.parse_args()
    viewports = [parse_viewport(v) for v in args.viewports.split(",")]
    return verify_preview(
        html_path=args.html_path,
        viewports=viewports,
        slides=args.slides,
        output_dir=args.output,
        show=args.show,
        wait=args.wait,
    )


if __name__ == "__main__":
    sys.exit(main())
