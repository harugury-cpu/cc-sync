#!/usr/bin/env python3
"""
spigen_spec_example.py — shared spec pipeline example.

Preview HTML and Google Slides API both consume the same component specs.
"""

import json

import spigen_lib as lib
import spigen_preview as prev
from spigen_models import ComponentSpec, SlideSpec


def build_example_specs():
    return [
        SlideSpec(
            slide_id="slide_cover",
            label="SLIDE 00 — COVER",
            title="",
            components=[
                ComponentSpec(
                    type="cover",
                    props={
                        "title": "Spigen Slides\nShared Spec Example",
                        "subtitle": "Preview / Google Slides 동시 렌더",
                        "department": "디자인부문ㅣ패키지디자인팀",
                        "owner": "한원진 담당",
                        "date_text": "2026.04.28",
                        "version": "V2.0",
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_section",
            label="SLIDE 01 — SECTION",
            title="",
            components=[
                ComponentSpec(
                    type="section-divider",
                    props={"num": "01", "title": "Shared Spec Samples", "label": "EXAMPLE"},
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_cards",
            label="SLIDE 02 — 3COL",
            eyebrow="OVERVIEW",
            title="핵심 샘플 컴포넌트",
            page_no=1,
            components=[
                ComponentSpec(
                    type="3col-cards",
                    props={
                        "cards": [
                            {"label": "SPEC", "title": "공통 데이터", "items": ["SlideSpec", "ComponentSpec", "단일 입력"], "hot": True},
                            {"label": "PREVIEW", "title": "HTML 미리보기", "items": ["같은 spec 소비", "브라우저 확인", "빠른 반복"]},
                            {"label": "SLIDES", "title": "실제 납품", "items": ["Google Slides API", "native shape", "editable text"]},
                        ]
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_compare",
            label="SLIDE 03 — COMPARE",
            eyebrow="COMPARE",
            title="기존 방식 vs 새 방식",
            page_no=2,
            components=[
                ComponentSpec(
                    type="compare-rows",
                    props={
                        "rows": [
                            {"item": "source of truth", "before": "HTML 결과물", "after": "공통 SlideSpec / ComponentSpec"},
                            {"item": "렌더 방향", "before": "HTML → Slides 변환", "after": "preview / Slides 개별 렌더"},
                            {"item": "결과 안정성", "before": "비율 드리프트 발생", "after": "같은 데이터 소비"},
                        ],
                        "callout": "비교는 앞으로 카드형 2분할이 아니라 행 기반 compare layout을 우선 사용한다.",
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_flow",
            label="SLIDE 04 — FLOW",
            eyebrow="PROCESS",
            title="렌더링 파이프라인",
            page_no=3,
            components=[
                ComponentSpec(
                    type="flow-focus",
                    props={
                        "steps": [
                            {"num": "01", "name": "PLAN", "service": "내용 구조화", "desc": "청중/목적/메시지 정리"},
                            {"num": "02", "name": "SPEC", "service": "공통 데이터", "desc": "SlideSpec / ComponentSpec", "primary": True},
                            {"num": "03", "name": "RENDER", "service": "미리보기 + 납품", "desc": "HTML / Google Slides"},
                        ],
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_decision",
            label="SLIDE 05 — DECISION",
            eyebrow="PROCESS",
            title="자동 선택 실패 시 수동 폴백",
            page_no=4,
            audience="internal",
            purpose="explain",
            detail_mode="detail",
            components=[
                ComponentSpec(
                    type="decision-tree",
                    props={
                        "nodes": {
                            "input": "CSV 입력",
                            "decision": "자동 선택 가능?",
                            "yes": "project.json 자동 선택",
                            "no": "리스트박스 수동 폴백",
                            "output": "PDF 출력",
                            "yes_label": "자동",
                            "no_label": "수동",
                        }
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_layers",
            label="SLIDE 06 — LAYERS",
            eyebrow="ARCH",
            title="입력부터 출력까지 4계층",
            page_no=5,
            components=[
                ComponentSpec(
                    type="arch-layers",
                    props={
                        "layers": [
                            {"label": "입력", "title": "CSV / 제품번호 / 사용자 입력"},
                            {"label": "선택", "title": "resolver + config", "desc": "선택 규칙과 매핑 판단", "accent": True},
                            {"label": "렌더링", "title": "engine.jsx + spec"},
                            {"label": "출력", "title": "Google Slides / Preview HTML"},
                        ]
                    },
                )
            ],
        ),
        SlideSpec(
            slide_id="slide_mapping",
            label="SLIDE 07 — MAPPING",
            eyebrow="ARCH",
            title="실행 모듈과 설정 파일 관계",
            page_no=6,
            audience="internal",
            purpose="explain",
            components=[
                ComponentSpec(
                    type="swimlane-mapping",
                    props={
                        "rows": [
                            {"left": "run.jsx", "middle": "입력", "right": "CSV"},
                            {"left": "monday_resolver.py", "middle": "선택 기준", "right": "monday_config.json"},
                            {"left": "engine.jsx", "middle": "템플릿 차이", "right": "{ID}_BSspec.json", "accent": True},
                        ]
                    },
                )
            ],
        ),
    ]


def build_preview(path="/tmp/spigen_spec_preview.html"):
    specs = build_example_specs()
    prev.send_specs(path, specs)
    return path


def build_requests():
    specs = build_example_specs()
    reqs = []
    total_pages = max((slide.page_no or 0) for slide in specs)
    for idx, slide in enumerate(specs):
        lib.render_slide_spec(slide, idx, reqs, total=total_pages)
    return {"requests": reqs}


if __name__ == "__main__":
    preview_path = build_preview()
    payload = build_requests()
    print("preview:", preview_path)
    print(json.dumps(payload, ensure_ascii=False)[:1200])
