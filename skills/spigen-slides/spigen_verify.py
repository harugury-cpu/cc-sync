#!/usr/bin/env python3
"""
spigen_verify.py — Google Slides 생성 결과를 template_spec.json 기준으로 검증.

사용법:
    python3 spigen_verify.py <PRESENTATION_ID> [slide_index]

    slide_index 생략 시 전체 슬라이드 검사.

종료 코드:
    0 = 모든 검증 통과 (완료 보고 가능)
    1 = FAIL 또는 MISS 존재 (spigen_lib.py 수정 후 재생성 필요)
"""

import json
import os
import subprocess
import sys

GWS = "/Users/harugury/.nvm/versions/node/v24.12.0/bin/gws"
SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template_spec.json")
EMU = 12700


# ── 유틸 ──────────────────────────────────────────────────────────────

def emu_pt(v):
    return v / EMU


def load_spec():
    with open(SPEC_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_presentation(pres_id):
    cmd = [GWS, "slides", "presentations", "get",
           "--params", json.dumps({"presentationId": pres_id})]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gws 오류:\n{r.stderr.strip()}")
    # keyring 경고 등 JSON 앞 불필요한 출력 제거
    stdout = r.stdout
    idx = stdout.find("{")
    if idx > 0:
        stdout = stdout[idx:]
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"gws 출력 파싱 실패: {e}\n출력(앞 300자): {r.stdout[:300]}")


def parse_el(el):
    """pageElement → {x, y, w, h, font_size, font_family, bold}

    Google Slides API는 크기를 size × scaleX/scaleY 로 인코딩한다.
    실제 렌더 크기 = size.width * scaleX (EMU) / 12700 (pt)
    """
    t = el.get("transform", {})
    sz = el.get("size", {})
    x = emu_pt(t.get("translateX", 0))
    y = emu_pt(t.get("translateY", 0))
    w = emu_pt(sz.get("width", {}).get("magnitude", 0) * t.get("scaleX", 1.0))
    h = emu_pt(sz.get("height", {}).get("magnitude", 0) * t.get("scaleY", 1.0))

    # 빈 run / paragraphMarker 건너뛰고 실제 내용 있는 첫 textRun 사용
    style = {}
    for te in el.get("shape", {}).get("text", {}).get("textElements", []):
        run = te.get("textRun", {})
        if not run or not run.get("content", "").strip():
            continue
        s = run.get("style", {})
        fs = s.get("fontSize", {}).get("magnitude")
        ff = s.get("fontFamily")
        if fs is not None or ff:
            style = {"font_size": fs, "font_family": ff, "bold": s.get("bold")}
            break

    return {
        "x": round(x, 1), "y": round(y, 1),
        "w": round(w, 1), "h": round(h, 1),
        **style,
    }


def build_elmap(slide):
    return {el["objectId"]: parse_el(el) for el in slide.get("pageElements", [])}


# ── 체크 헬퍼 ────────────────────────────────────────────────────────

def _chk(results, label, actual, expected, tol=2.5):
    if actual is None:
        results.append(("SKIP", f"{label}: 값 없음"))
        return
    diff = abs(actual - expected)
    if diff <= tol:
        results.append(("PASS", f"{label}: {actual:.1f} ≈ {expected:.1f}"))
    else:
        results.append(("FAIL",
            f"{label}: got {actual:.1f}, expected {expected:.1f}  (차이 {diff:.1f}pt)"))


def _chk_str(results, label, actual, expected):
    if actual is None:
        results.append(("SKIP", f"{label}: 값 없음"))
        return
    if actual == expected:
        results.append(("PASS", f"{label}: '{actual}'"))
    else:
        results.append(("FAIL", f"{label}: got '{actual}', expected '{expected}'"))


def _check_element(results, el, sp, prefix, tol=2.5):
    """공통: sp 딕셔너리의 x/y/w/h/font_size/font_family/bold를 el에서 검증."""
    for dim in ("x", "y", "w", "h"):
        if dim in sp:
            _chk(results, f"{prefix}.{dim}", el.get(dim), sp[dim], tol)
    if "font_size" in sp:
        _chk(results, f"{prefix}.font_size", el.get("font_size"), sp["font_size"], tol=0.6)
    if "font_family" in sp:
        _chk_str(results, f"{prefix}.font_family", el.get("font_family"), sp["font_family"])
    if "bold" in sp and sp["bold"] is not None:
        actual_bold = el.get("bold")
        if actual_bold is None:
            results.append(("SKIP", f"{prefix}.bold: 값 없음"))
        elif actual_bold == sp["bold"]:
            results.append(("PASS", f"{prefix}.bold: {actual_bold}"))
        else:
            results.append(("FAIL", f"{prefix}.bold: got {actual_bold}, expected {sp['bold']}"))


# ── 컴포넌트 감지 ────────────────────────────────────────────────────

def detect_components(elmap, oid):
    comps = []
    if f"{oid}_num" in elmap and f"{oid}_label" in elmap:
        comps.append("section_divider")
    if f"{oid}_step0" in elmap:
        comps.append("flow")
    if f"{oid}_col0" in elmap:
        comps.append("3col")
    if f"{oid}_kpi_bg0" in elmap:
        comps.append("kpi_dashboard")
    if f"{oid}_quote_mark" in elmap:
        comps.append("quote")
    if f"{oid}_eyebrow" in elmap:
        comps.append("slide_base")
    elif f"{oid}_title" in elmap and "section_divider" not in comps:
        comps.append("slide_base")
    return comps


# ── 컴포넌트별 검증 함수 ──────────────────────────────────────────────

def verify_slide_base(elmap, oid, spec, tol):
    results = []
    s = spec.get("slide_base", {})
    for suffix, key in [("_eyebrow", "eyebrow"), ("_title", "title")]:
        sp = s.get(key, {})
        el = elmap.get(oid + suffix)
        if el and sp:
            _check_element(results, el, sp, f"slide_base.{key}", tol)
    return results


def verify_section_divider(elmap, oid, spec, tol):
    results = []
    s = spec.get("section_divider", {})
    for suffix, key in [("_num", "num"), ("_vline", "vline"), ("_label", "label"), ("_title", "title")]:
        sp = s.get(key, {})
        el = elmap.get(oid + suffix)
        if not sp:
            continue
        if not el:
            results.append(("MISS", f"section_divider{suffix} 요소 없음"))
            continue
        _check_element(results, el, sp, f"section_divider.{key}", tol)
    return results


def verify_flow(elmap, oid, spec, tol):
    results = []
    layout = spec.get("flow", {}).get("_layout", {})
    x0 = layout.get("x0", 54)
    y0 = layout.get("y0", 132)
    total_w = layout.get("total_w", 612)
    ch = layout.get("ch", 96)

    n = sum(1 for i in range(10) if f"{oid}_step{i}" in elmap)
    if n == 0:
        return results

    gap = layout.get("gap_le4", 12) if n <= 4 else layout.get("gap_gt4", 8)
    cw = (total_w - gap * (n - 1)) / n

    s = spec.get("flow", {})

    for i in range(n):
        x = x0 + i * (cw + gap)
        pfx = f"flow.step{i}"

        # 카드 박스
        card = elmap.get(f"{oid}_step{i}")
        if card:
            _chk(results, f"{pfx}.x", card.get("x"), round(x, 1), tol)
            _chk(results, f"{pfx}.y", card.get("y"), y0, tol)
            _chk(results, f"{pfx}.w", card.get("w"), round(cw, 1), tol)
            _chk(results, f"{pfx}.h", card.get("h"), ch, tol)
        else:
            results.append(("MISS", f"{pfx} 카드 요소 없음"))

        # 텍스트 서브요소
        for suffix, key in [("_sn", "sn"), ("_st", "st"), ("_sv", "sv")]:
            sp = s.get(key, {})
            el = elmap.get(f"{oid}{suffix}{i}")
            if not el or not sp:
                continue
            _chk(results, f"{pfx}{suffix}.x", el.get("x"), round(x + sp.get("rel_x", 0), 1), tol)
            _chk(results, f"{pfx}{suffix}.y", el.get("y"), y0 + sp.get("rel_y", 0), tol)
            _chk(results, f"{pfx}{suffix}.w", el.get("w"), round(cw - sp.get("w_shrink", 0), 1), tol)
            if "font_size" in sp:
                _chk(results, f"{pfx}{suffix}.font_size", el.get("font_size"), sp["font_size"], tol=0.6)
            if "font_family" in sp:
                _chk_str(results, f"{pfx}{suffix}.font_family", el.get("font_family"), sp["font_family"])

    return results


def verify_3col(elmap, oid, spec, tol):
    results = []
    layout = spec.get("3col", {}).get("_layout", {})
    x0 = layout.get("x0", 36)
    y0 = layout.get("y0", 128)
    cw = layout.get("card_w", 206)
    gap = layout.get("gap", 12)
    s = spec.get("3col", {})

    n = sum(1 for i in range(5) if f"{oid}_col{i}" in elmap)
    for i in range(n):
        x = x0 + i * (cw + gap)
        pfx = f"3col.col{i}"

        card = elmap.get(f"{oid}_col{i}")
        if card:
            _chk(results, f"{pfx}.x", card.get("x"), x, tol)
            _chk(results, f"{pfx}.y", card.get("y"), y0, tol)
            _chk(results, f"{pfx}.w", card.get("w"), cw, tol)

        for suffix, key in [("_cl", "cl"), ("_ct", "ct")]:
            sp = s.get(key, {})
            el = elmap.get(f"{oid}{suffix}{i}")
            if not el or not sp:
                continue
            _chk(results, f"{pfx}{suffix}.x", el.get("x"), x + sp.get("rel_x", 0), tol)
            _chk(results, f"{pfx}{suffix}.y", el.get("y"), y0 + sp.get("rel_y", 0), tol)
            if "font_size" in sp:
                _chk(results, f"{pfx}{suffix}.font_size", el.get("font_size"), sp["font_size"], tol=0.6)
            if "font_family" in sp:
                _chk_str(results, f"{pfx}{suffix}.font_family", el.get("font_family"), sp["font_family"])

    return results


def verify_kpi(elmap, oid, spec, tol):
    results = []
    layout = spec.get("kpi_dashboard", {}).get("_layout", {})
    x0 = layout.get("x0", 36)
    y0 = layout.get("y0", 128)
    gap = layout.get("gap", 12)
    card_h = layout.get("card_h", 128)
    s = spec.get("kpi_dashboard", {})

    n = sum(1 for i in range(5) if f"{oid}_kpi_bg{i}" in elmap)
    canvas_w = 720
    margin = 36
    card_w = (canvas_w - margin * 2 - gap * (n - 1)) / max(1, n)

    for i in range(n):
        x = x0 + i * (card_w + gap)
        pfx = f"kpi.{i}"
        for suffix, key in [("_kpi_label", "kpi_label"), ("_kpi_value", "kpi_value"), ("_kpi_sub", "kpi_sub")]:
            sp = s.get(key, {})
            el = elmap.get(f"{oid}{suffix}{i}")
            if not el or not sp:
                continue
            _chk(results, f"{pfx}{suffix}.x", el.get("x"), round(x + sp.get("rel_x", 0), 1), tol)
            _chk(results, f"{pfx}{suffix}.y", el.get("y"), y0 + sp.get("rel_y", 0), tol)
            if "font_size" in sp:
                _chk(results, f"{pfx}{suffix}.font_size", el.get("font_size"), sp["font_size"], tol=0.6)
            if "font_family" in sp:
                _chk_str(results, f"{pfx}{suffix}.font_family", el.get("font_family"), sp["font_family"])

    return results


def verify_quote(elmap, oid, spec, tol):
    results = []
    s = spec.get("quote", {})
    for suffix, key in [("_quote_mark", "quote_mark"), ("_quote", "quote")]:
        sp = s.get(key, {})
        el = elmap.get(oid + suffix)
        if el and sp:
            _check_element(results, el, sp, f"quote.{key}", tol)
    return results


# ── 출력 ─────────────────────────────────────────────────────────────

ICONS = {"PASS": "✓", "FAIL": "✗", "SKIP": "·", "MISS": "?"}


def print_results(results):
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0, "MISS": 0}
    for status, msg in results:
        counts[status] = counts.get(status, 0) + 1
        icon = ICONS.get(status, " ")
        print(f"    {icon} [{status}] {msg}")
    return counts


# ── 메인 ─────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 spigen_verify.py <PRESENTATION_ID> [slide_index]")
        sys.exit(1)

    pres_id = sys.argv[1]
    target = None
    if len(sys.argv) > 2:
        try:
            target = int(sys.argv[2])
        except ValueError:
            print(f"오류: slide_index는 정수여야 합니다 (got '{sys.argv[2]}')")
            sys.exit(1)

    spec = load_spec()
    tol = spec.get("_meta", {}).get("tolerance_pt", 2.5)

    print(f"프레젠테이션 로드 중: {pres_id}")
    data = get_presentation(pres_id)
    slides = data.get("slides", [])
    print(f"슬라이드 {len(slides)}장 확인\n")

    total = {"PASS": 0, "FAIL": 0, "SKIP": 0, "MISS": 0}

    for idx, slide in enumerate(slides):
        if target is not None and idx != target:
            continue

        oid = slide.get("objectId", f"slide_{idx}")
        elmap = build_elmap(slide)
        comps = detect_components(elmap, oid)

        print(f"── Slide {idx}  ({oid})")
        if not comps:
            print("    (인식된 컴포넌트 없음 — 건너뜀)\n")
            continue
        print(f"    컴포넌트: {', '.join(comps)}")

        results = []
        if "slide_base" in comps:
            results += verify_slide_base(elmap, oid, spec, tol)
        if "section_divider" in comps:
            results += verify_section_divider(elmap, oid, spec, tol)
        if "flow" in comps:
            results += verify_flow(elmap, oid, spec, tol)
        if "3col" in comps:
            results += verify_3col(elmap, oid, spec, tol)
        if "kpi_dashboard" in comps:
            results += verify_kpi(elmap, oid, spec, tol)
        if "quote" in comps:
            results += verify_quote(elmap, oid, spec, tol)

        counts = print_results(results)
        print(f"    → PASS:{counts['PASS']} FAIL:{counts['FAIL']} SKIP:{counts['SKIP']} MISS:{counts['MISS']}\n")
        for k, v in counts.items():
            total[k] = total.get(k, 0) + v

    print("══════════════════════════════════════════════")
    print(f"최종: PASS={total['PASS']}  FAIL={total['FAIL']}  SKIP={total['SKIP']}  MISS={total['MISS']}")

    if total["FAIL"] > 0 or total["MISS"] > 0:
        print("❌ 검증 실패 — spigen_lib.py 수정 후 슬라이드 재생성 필요")
        sys.exit(1)
    elif total["PASS"] == 0:
        print("⚠  검증 대상 없음 — objectId 패턴 확인 필요")
        sys.exit(0)
    else:
        print("✓  모든 검증 통과 — 완료 보고 가능")
        sys.exit(0)


if __name__ == "__main__":
    main()
