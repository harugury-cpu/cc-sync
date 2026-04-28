#!/usr/bin/env python3
"""
spigen_preview.py — 슬라이드 내용 → HTML 프리뷰 생성기

파이프라인:
    HTML 생성 → Telegram 전송 → 눈으로 확인 → OK → Google Slides API 생성

사용법 (개별 덱 스크립트에서):
    import spigen_preview as prev
    slides = [
        prev.Slide("SLIDE 02 — OVERVIEW", "OVERVIEW", "전체 흐름 한 눈에",
                   prev.html_decision_tree({...})),
        prev.Slide("SLIDE 03 — 개발팀", "개발팀", "개발팀 역할",
                   prev.html_split(left={...}, right={...})),
    ]
    prev.send("/tmp/preview_jangtal.html", slides)
"""
import subprocess, json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from spigen_models import ComponentSpec, SlideSpec

# ── 캔버스 상수 (Google Slides pt → px 1:1) ──
W, H = 720, 405
M = 36
CONTENT_TOP = 88

# ── 다크 테마 토큰 ──
T = {
    "BG":         "#000000",
    "SURFACE":    "#0E0E0E",
    "SURFACE_HI": "#161616",
    "BORDER":     "#202020",
    "BORDER_HI":  "#303030",
    "ORANGE":     "#FF6B1A",
    "ORANGE_DIM": "#3D1A05",
    "TEXT":       "#F0F0F0",
    "TEXT_DIM":   "#AAAAAA",
    "TEXT_FAINT": "#6E6E6E",
    "WHITE":      "#FFFFFF",
}


@dataclass
class Slide:
    label: str
    eyebrow: str
    title: str
    content_html: str
    page_no: Optional[int] = None


# ─────────────────────────────────────────────
# 공통 헬퍼
# ─────────────────────────────────────────────

def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")


def _abs(left=0, top=0, width=None, height=None, extra_style="") -> str:
    s = f"position:absolute;left:{left}px;top:{top}px;"
    if width is not None:
        s += f"width:{width}px;"
    if height is not None:
        s += f"height:{height}px;"
    return s + extra_style


def _box(x, y, w, h, bg, border, children="", border_w=0.5) -> str:
    return (
        f'<div style="{_abs(x,y,w,h)}'
        f'background:{bg};border:{border_w}px solid {border};overflow:hidden;">'
        f'{children}</div>'
    )


def _txt(x, y, w, h, text, color, size, bold=False, center=False, pre=False) -> str:
    fw = "700" if bold else "400"
    ta = "center" if center else "left"
    ws = "pre-line" if pre else "normal"
    return (
        f'<div style="{_abs(x,y,w,h)}'
        f'color:{color};font-size:{size}px;font-weight:{fw};'
        f'line-height:1.4;text-align:{ta};white-space:{ws};'
        f'font-family:\'Noto Sans KR\',system-ui;">'
        f'{_esc(text)}</div>'
    )


def _mono(x, y, w, h, text, color, size, bold=False, center=False) -> str:
    """영문/숫자 전용 — Proxima Nova 대체 폰트 사용."""
    fw = "700" if bold else "400"
    ta = "center" if center else "left"
    return (
        f'<div style="{_abs(x,y,w,h)}'
        f'color:{color};font-size:{size}px;font-weight:{fw};'
        f'line-height:1.4;text-align:{ta};letter-spacing:0.04em;'
        f'font-family:\'DM Sans\',system-ui,sans-serif;">'
        f'{_esc(text)}</div>'
    )


def _hline(x, y, w, color, h=0.5) -> str:
    return f'<div style="{_abs(x,y,w,h)}background:{color};"></div>'


# ─────────────────────────────────────────────
# 헤더 (eyebrow + 구분선 + 타이틀)
# ─────────────────────────────────────────────

def html_header(eyebrow="", title="") -> str:
    parts = []
    if eyebrow:
        parts.append(_mono(M, 30, 200, 10, eyebrow.upper(), T["TEXT_FAINT"], 7, bold=True))
        parts.append(_hline(M, 46, 36, T["ORANGE"], h=1.5))
    if title:
        parts.append(_txt(M, 52, W - M * 2, 24, title, T["TEXT"], 14, bold=True))
    return "\n".join(parts)


# ─────────────────────────────────────────────
# mk_flow HTML 렌더러
# ─────────────────────────────────────────────

def html_flow(steps: list, x0=54, y0=132) -> str:
    visible = steps[:6]
    n = len(visible)
    gap = 12 if n <= 4 else 8
    total_w = 612
    cw = (total_w - gap * max(0, n - 1)) / max(1, n)

    # primary: 마지막 hot 카드
    primary = -1
    for i, s in enumerate(visible):
        if isinstance(s, dict) and (s.get("hot") or s.get("primary") or s.get("accent")):
            primary = i

    # 카드 높이: desc 있으면 더 넓게
    has_desc = any(s.get("desc") or s.get("detail") for s in visible if isinstance(s, dict))
    ch = 230 if has_desc else 150

    parts = []
    for i, step in enumerate(visible):
        name = step.get("name", step.get("title", ""))
        svc  = step.get("service", step.get("infra", ""))
        desc = step.get("desc",  step.get("detail", ""))
        num  = step.get("num", f"{i+1:02d}")
        is_primary = (i == primary)
        marked = bool(step.get("hot") or step.get("primary") or step.get("accent"))
        dim_hot = marked and not is_primary

        if is_primary:
            bg, brd = T["ORANGE"], T["ORANGE"]
            c_sn, c_st, c_sv, c_sd, c_sep = T["WHITE"], T["WHITE"], T["WHITE"], T["WHITE"], T["WHITE"]
        elif dim_hot:
            bg, brd = T["ORANGE_DIM"], T["ORANGE"]
            c_sn, c_st, c_sv, c_sd, c_sep = T["ORANGE"], T["TEXT"], T["TEXT_DIM"], T["TEXT_DIM"], T["ORANGE"]
        else:
            bg, brd = T["SURFACE"], T["BORDER"]
            c_sn, c_st, c_sv, c_sd, c_sep = T["TEXT_FAINT"], T["TEXT"], T["TEXT_DIM"], T["TEXT_DIM"], T["BORDER_HI"]

        x = x0 + i * (cw + gap)

        inner = (
            _mono(x+8, y0+8, cw-16, 10, f"STEP {num}", c_sn, 5, bold=True)
            + _txt(x+8, y0+18, cw-16, 28, name, c_st, 9, bold=True)
            + _txt(x+8, y0+44, cw-16, 14, svc,  c_sv, 7)
        )
        if desc:
            inner += _hline(x+8, y0+62, cw-16, c_sep)
            inner += _txt(x+8, y0+68, cw-16, ch-76, desc, c_sd, 7, pre=True)

        parts.append(_box(x, y0, cw, ch, bg, brd, inner))

        if i < n - 1:
            arr_x = x + cw + (gap / 2) - 4
            arr_y = y0 + ch / 2 - 5
            parts.append(
                f'<div style="position:absolute;left:{arr_x:.1f}px;top:{arr_y:.1f}px;'
                f'color:{T["TEXT_FAINT"]};font-size:10px;line-height:1;">›</div>'
            )

    return "\n".join(parts)


# ─────────────────────────────────────────────
# mk_decision_tree HTML 렌더러
# ─────────────────────────────────────────────

def html_decision_tree(nodes: dict, x=54, y=170) -> str:
    input_text    = nodes.get("input", "")
    decision_text = nodes.get("decision", "")
    yes_text      = nodes.get("yes", "")
    no_text       = nodes.get("no", "")
    output_text   = nodes.get("output", "")
    yes_label     = nodes.get("yes_label", "YES")
    no_label      = nodes.get("no_label", "NO")

    def centered_box(bx, by, bw, bh, bg, border, text, color=T["TEXT"], size=8, caption=""):
        cap_html = (
            f'<div style="font-size:5px;font-weight:700;color:{T["TEXT_FAINT"]};'
            f'letter-spacing:0.08em;margin-bottom:6px;font-family:\'DM Sans\',system-ui;">'
            f'{caption}</div>'
        ) if caption else ""
        return (
            f'<div style="{_abs(bx,by,bw,bh)}'
            f'background:{bg};border:0.5px solid {border};'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">'
            f'{cap_html}'
            f'<span style="color:{color};font-size:{size}px;font-weight:700;'
            f'font-family:\'Noto Sans KR\',system-ui;white-space:pre-line;">{_esc(text)}</span>'
            f'</div>'
        )

    # 박스들
    b_input    = centered_box(x,      y+38,  110, 44, T["SURFACE"],    T["BORDER"], input_text)
    b_decision = centered_box(x+188,  y+22,  126, 76, T["SURFACE_HI"], T["ORANGE"], decision_text, caption="판단")
    b_yes      = centered_box(x+396,  y,     150, 44, T["ORANGE_DIM"], T["ORANGE"], yes_text)
    b_no       = centered_box(x+396,  y+96,  150, 44, T["SURFACE"],    T["BORDER"], no_text)
    b_output   = centered_box(x+574,  y+38,   74, 44, T["SURFACE_HI"], T["BORDER"], output_text, size=7)

    # 라벨
    lbl_yes = _mono(x+336, y+20,  34, 10, yes_label, T["ORANGE"],     5, center=True)
    lbl_no  = _mono(x+336, y+106, 34, 10, no_label,  T["TEXT_FAINT"], 5, center=True)

    # SVG 커넥터 (픽셀 좌표 = pt 좌표 그대로)
    svg = f"""<svg style="position:absolute;top:0;left:0;width:{W}px;height:{H}px;pointer-events:none;overflow:visible;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr-o" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6" fill="none" stroke="{T["ORANGE"]}" stroke-width="1"/>
    </marker>
    <marker id="arr-g" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6" fill="none" stroke="{T["BORDER_HI"]}" stroke-width="1"/>
    </marker>
  </defs>
  <line x1="{x+110}" y1="{y+60}" x2="{x+186}" y2="{y+60}" stroke="{T["BORDER_HI"]}" stroke-width="1" marker-end="url(#arr-g)"/>
  <line x1="{x+314}" y1="{y+40}" x2="{x+394}" y2="{y+22}" stroke="{T["ORANGE"]}"     stroke-width="1" marker-end="url(#arr-o)"/>
  <line x1="{x+314}" y1="{y+80}" x2="{x+394}" y2="{y+118}" stroke="{T["BORDER_HI"]}" stroke-width="1" marker-end="url(#arr-g)"/>
  <line x1="{x+546}" y1="{y+22}" x2="{x+572}" y2="{y+58}" stroke="{T["ORANGE"]}"     stroke-width="1" marker-end="url(#arr-o)"/>
  <line x1="{x+546}" y1="{y+118}" x2="{x+572}" y2="{y+62}" stroke="{T["BORDER_HI"]}" stroke-width="1" marker-end="url(#arr-g)"/>
</svg>"""

    return svg + b_input + b_decision + b_yes + b_no + b_output + lbl_yes + lbl_no


# ─────────────────────────────────────────────
# mk_split HTML 렌더러
# ─────────────────────────────────────────────

def html_split(left: dict, right: dict, arrow=True) -> str:
    left_x = 54
    top_y = 120
    card_w = 278
    card_h = 236
    right_x = 388
    body_w = 242
    left_body  = left.get("body", "")
    right_body = right.get("body", "")

    l_inner = (
        _txt(left_x + 18, top_y + 24, body_w, 24, left.get("title", ""),  T["TEXT"], 14, bold=True)
        + _txt(left_x + 18, top_y + 66, body_w, 136, left_body, T["TEXT_DIM"], 8, pre=True)
    )
    r_inner = (
        _txt(right_x + 18, top_y + 24, body_w, 24, right.get("title", ""), T["TEXT"], 14, bold=True)
        + _txt(right_x + 18, top_y + 66, body_w, 136, right_body, T["TEXT_DIM"], 8, pre=True)
    )

    l_box = _box(left_x, top_y, card_w, card_h, T["SURFACE"], T["BORDER"], l_inner)
    r_box = _box(right_x, top_y, card_w, card_h, T["ORANGE_DIM"], T["ORANGE"], r_inner)
    arr   = (
        f'<div style="position:absolute;left:348px;top:228px;'
        f'width:16px;height:16px;color:{T["ORANGE"]};'
        f'font-size:13px;font-weight:700;text-align:center;line-height:16px;">›</div>'
    ) if arrow else ""

    return l_box + r_box + arr


def html_text_block(body_text: str, x=M, y=128, w=648, h=220) -> str:
    inner = _txt(x + 20, y + 20, w - 40, h - 40, body_text, T["TEXT_DIM"], 9, pre=True)
    return _box(x, y, w, h, T["SURFACE"], T["BORDER"], inner)


def html_3col_cards(cards: list, x=36, y=128, card_w=206, gap=12, card_h=190) -> str:
    parts = []
    for i, card in enumerate(cards[:3]):
        bx = x + i * (card_w + gap)
        items = card.get("items", [])
        inner = (
            _mono(bx + 18, y + 20, 170, 12, card.get("label", ""), T["TEXT_FAINT"], 7, bold=True)
            + _txt(bx + 18, y + 43, 170, 28, card.get("title", ""), T["TEXT"], 14.5, bold=True)
        )
        for j, item in enumerate(items[:5]):
            inner += _txt(bx + 28, y + 82 + j * 19, 162, 13, f"• {item}", T["TEXT_DIM"], 7)
        parts.append(_box(bx, y, card_w, card_h, T["ORANGE_DIM"] if card.get("hot") else T["SURFACE"], T["ORANGE"] if card.get("hot") else T["BORDER"], inner))
    return "\n".join(parts)


def html_cover(title: str, subtitle="", department="디자인부문ㅣ패키지디자인팀",
               owner="한원진 담당", date_text="", version="V1.0") -> str:
    title_text = title if not subtitle else f"{title}\n{subtitle}"
    team_text = department if not owner else f"{department}\n{owner}"
    meta_text = version if not date_text else f"{date_text}\n{version}"
    return "\n".join([
        _txt(28, 34, 595, 100, title_text, T["TEXT"], 36, pre=True),
        _txt(28, 319, 561, 50, team_text, T["TEXT"], 12, pre=True),
        _txt(508, 319, 177, 50, meta_text, T["TEXT"], 12, pre=True),
    ])


def html_section_divider(num: str, title: str, label="SECTION") -> str:
    return "\n".join([
        _mono(51, 103, 120, 82, num, T["ORANGE"], 100, bold=True),
        _mono(172, 158, 100, 16, label, T["TEXT_DIM"], 14.5),
        _txt(165, 174, 380, 64, title, T["TEXT"], 28, bold=True),
    ])


def html_compare_rows(rows: list, left_label="현재", right_label="도입 후", callout="") -> str:
    parts = [
        _mono(36, 109, 120, 10, left_label, "#FF0000", 5),
        _mono(370.5, 109, 120, 10, right_label, T["ORANGE"], 5, bold=True),
    ]
    row_y0, row_h, row_gap = 125.2, 40, 5
    for i, row in enumerate(rows[:5]):
        ry = row_y0 + i * (row_h + row_gap)
        parts.append(_box(36, ry, 313.5, row_h, T["SURFACE"], T["BORDER"], ""))
        parts.append(_box(349.5, ry, 21, row_h, T["SURFACE"], T["BORDER"], ""))
        parts.append(_box(370.5, ry, 313.5, row_h, T["ORANGE_DIM"], T["ORANGE"], ""))
        parts.append(_mono(356, ry + 17, 10, 10, "›", T["ORANGE"], 5, center=True))
        parts.append(_txt(47, ry + 8, 280, 9, row.get("item", ""), T["TEXT_FAINT"], 5))
        parts.append(_txt(47, ry + 18, 280, 14, row.get("before", ""), "#FF0000", 8))
        parts.append(_txt(382, ry + 8, 280, 9, row.get("after_label", "개선"), T["ORANGE"], 5, bold=True))
        parts.append(_txt(382, ry + 18, 280, 14, row.get("after", ""), T["TEXT"], 8))
    if callout:
        cy = row_y0 + min(len(rows), 5) * (row_h + row_gap) - row_gap + 14
        parts.append(_box(36, cy, 1, 26, T["ORANGE"], T["ORANGE"], "", border_w=0))
        parts.append(_txt(48, cy + 7, 636, 13, callout, T["TEXT"], 7))
    return "\n".join(parts)


def html_split_cards(text_lines: list, cards: list) -> str:
    left_text = "\n".join(text_lines[:8])
    parts = [
        _box(36, 128, 312, 220, T["SURFACE"], T["BORDER"], _txt(56, 152, 272, 172, left_text, T["TEXT_DIM"], 9, pre=True))
    ]
    for i, card in enumerate(cards[:3]):
        by = 128 + i * 76
        parts.append(_box(372, by, 312, 64, T["ORANGE_DIM"] if card.get("primary") else T["SURFACE"], T["ORANGE"] if card.get("primary") else T["BORDER"], ""))
        parts.append(_mono(392, by + 14, 120, 10, card.get("label", ""), T["ORANGE"] if card.get("primary") else T["TEXT_FAINT"], 7, bold=True))
        parts.append(_txt(392, by + 28, 268, 20, card.get("body", ""), T["TEXT"], 8, bold=True))
    return "\n".join(parts)


def html_arch_layers(layers: list, x=54, y=148, w=612, spine_w=72, gap=20) -> str:
    visible = layers[:4]
    if not visible:
        return ""
    total_h = 200 if not any((row.get("desc", "") if isinstance(row, dict) else "") for row in visible) else 230
    row_gap = 10
    row_h = (total_h - row_gap * (len(visible) - 1)) / len(visible)
    box_x = x + spine_w + gap
    box_w = w - spine_w - gap
    parts = [_box(x, y, spine_w, total_h, T["SURFACE_HI"], T["BORDER"], "")]
    for i, row in enumerate(visible):
        yy = y + i * (row_h + row_gap)
        hot = bool(row.get("primary") or row.get("accent") or row.get("hot"))
        bg = T["ORANGE"] if hot else T["SURFACE"]
        br = T["ORANGE"] if hot else T["BORDER"]
        fg = T["BG"] if hot else T["TEXT"]
        parts.append(_mono(x + 8, yy + row_h / 2 - 5, spine_w - 16, 10, row.get("label", f"{i+1:02d}"), T["ORANGE"] if hot else T["TEXT_FAINT"], 7, bold=True, center=True))
        parts.append(_box(box_x, yy, box_w, row_h, bg, br, ""))
        parts.append(_txt(box_x + 18, yy + 12, box_w - 36, 16, row.get("title", row.get("name", "")), fg, 10, bold=True))
        if row.get("desc"):
            parts.append(_txt(box_x + 18, yy + 32, box_w - 36, row_h - 40, row.get("desc", ""), T["TEXT_DIM"] if not hot else T["BG"], 7, pre=True))
    return "\n".join(parts)


def html_arch_orchestrator(nodes: dict, x=54, y=146) -> str:
    input_text = nodes.get("input", "입력")
    main_text = nodes.get("main", "run.jsx")
    engine_text = nodes.get("engine", "engine.jsx")
    output_text = nodes.get("output", "출력")
    right_nodes = nodes.get("right_nodes", [])[:3]

    parts = []
    parts.append(_box(x, y + 40, 120, 44, T["SURFACE"], T["BORDER"],
                      _mono(x, y + 50, 120, 10, "입력", T["TEXT_FAINT"], 7, bold=True, center=True)
                      + _txt(x, y + 62, 120, 12, input_text, T["TEXT"], 8, bold=True, center=True)))
    parts.append(_box(x + 200, y + 30, 160, 64, T["ORANGE_DIM"], T["ORANGE"],
                      _mono(x + 200, y + 45, 160, 10, "ORCHESTRATOR", T["ORANGE"], 7, bold=True, center=True)
                      + _txt(x + 200, y + 61, 160, 16, main_text, T["TEXT"], 13, bold=True, center=True)))
    for i, item in enumerate(right_nodes):
        yy = y + i * 54
        br = T["ORANGE"] if item.get("accent") or item.get("primary") else T["BORDER"]
        parts.append(_box(x + 428, yy, 184, 36, T["SURFACE"], br,
                          _txt(x + 444, yy + 12, 152, 12, item.get("label", ""), T["TEXT"], 7.5, bold=True)))
    parts.append(_box(x + 200, y + 128, 160, 40, T["SURFACE"], T["BORDER"],
                      _txt(x + 200, y + 142, 160, 12, engine_text, T["TEXT"], 9, bold=True, center=True)))
    parts.append(_box(x + 428, y + 172, 184, 36, T["SURFACE"], T["BORDER"],
                      _txt(x + 444, y + 184, 152, 12, output_text, T["TEXT"], 7.5, bold=True)))
    return "\n".join(parts)


def html_swimlane_mapping(rows: list, x=54, y=148) -> str:
    visible = rows[:3]
    if not visible:
        return ""
    left_w, mid_w, right_w = 220, 120, 236
    total_h = 180
    row_gap = 8
    row_h = (total_h - 28 - row_gap * (len(visible) - 1)) / len(visible)
    mid_x = x + left_w + 18
    right_x = mid_x + mid_w + 18
    parts = [
        _box(x, y, left_w, total_h, T["SURFACE"], T["BORDER"], ""),
        _box(mid_x, y, mid_w, total_h, T["SURFACE_HI"], T["BORDER"], ""),
        _box(right_x, y, right_w, total_h, T["SURFACE"], T["BORDER"], ""),
        _mono(x + 18, y + 16, 100, 10, "실행 모듈", T["ORANGE"], 7, bold=True),
        _mono(mid_x + 18, y + 16, 84, 10, "관계", T["TEXT_FAINT"], 7, bold=True),
        _mono(right_x + 18, y + 16, 120, 10, "설정 / 데이터", T["TEXT_FAINT"], 7, bold=True),
    ]
    for i, row in enumerate(visible):
        yy = y + 40 + i * (row_h + row_gap)
        accent = bool(row.get("accent") or row.get("primary"))
        parts.append(_box(x + 12, yy, left_w - 24, row_h, T["ORANGE_DIM"] if accent else T["SURFACE_HI"], T["ORANGE"] if accent else T["BORDER"], ""))
        parts.append(_txt(x + 26, yy + 10, left_w - 52, row_h - 20, row.get("left", ""), T["TEXT"], 8, bold=True))
        parts.append(_txt(mid_x + 10, yy + 10, mid_w - 20, row_h - 20, row.get("middle", ""), T["TEXT_DIM"], 7, center=True))
        parts.append(_box(right_x + 12, yy, right_w - 24, row_h, T["SURFACE_HI"], T["BORDER"], ""))
        parts.append(_txt(right_x + 26, yy + 10, right_w - 52, row_h - 20, row.get("right", ""), T["TEXT"], 8, bold=True))
    return "\n".join(parts)


def _component_html(component: ComponentSpec | dict) -> str:
    if isinstance(component, dict):
        component = ComponentSpec.from_dict(component)
    ctype = component.type
    props = component.props
    if ctype == "cover":
        return html_cover(
            props.get("title", ""),
            subtitle=props.get("subtitle", ""),
            department=props.get("department", "디자인부문ㅣ패키지디자인팀"),
            owner=props.get("owner", "한원진 담당"),
            date_text=props.get("date_text", ""),
            version=props.get("version", "V1.0"),
        )
    if ctype == "section-divider":
        return html_section_divider(props.get("num", "01"), props.get("title", ""), label=props.get("label", "SECTION"))
    if ctype == "compare-rows":
        return html_compare_rows(
            props.get("rows", []),
            left_label=props.get("left_label", "현재"),
            right_label=props.get("right_label", "도입 후"),
            callout=props.get("callout", ""),
        )
    if ctype in ("flow", "flow-focus"):
        return html_flow(props.get("steps", []), x0=props.get("x0", 54), y0=props.get("y0", 132))
    if ctype == "decision-tree":
        return html_decision_tree(props.get("nodes", {}), x=props.get("x", 54), y=props.get("y", 170))
    if ctype == "split-layout":
        return html_split(props.get("left", {}), props.get("right", {}), arrow=props.get("arrow", True))
    if ctype == "text-block":
        return html_text_block(props.get("body_text", ""))
    if ctype == "3col-cards":
        return html_3col_cards(props.get("cards", []))
    if ctype == "split-cards":
        return html_split_cards(props.get("text_lines", []), props.get("cards", []))
    if ctype == "arch-layers":
        return html_arch_layers(props.get("layers", []))
    if ctype == "arch-orchestrator":
        return html_arch_orchestrator(props.get("nodes", {}))
    if ctype == "swimlane-mapping":
        return html_swimlane_mapping(props.get("rows", []))
    raise ValueError(f"Unsupported preview component type: {ctype}")


def render_slide_spec(slide_spec: SlideSpec | dict) -> Slide:
    if isinstance(slide_spec, dict):
        slide_spec = SlideSpec.from_dict(slide_spec)
    content_html = "\n".join(_component_html(component) for component in slide_spec.components)
    special = bool(slide_spec.components and slide_spec.components[0].type in ("cover", "section-divider"))
    label = slide_spec.label or slide_spec.slide_id or slide_spec.title
    return Slide(
        label=label,
        eyebrow="" if special else slide_spec.eyebrow,
        title="" if special else slide_spec.title,
        content_html=content_html,
        page_no=slide_spec.page_no,
    )


def build_html_from_specs(slide_specs: list[SlideSpec | dict]) -> str:
    slides = [render_slide_spec(spec) for spec in slide_specs]
    return build_html(slides)


# ─────────────────────────────────────────────
# 슬라이드 래퍼 + 덱 빌더
# ─────────────────────────────────────────────

def _wrap_slide(slide: Slide) -> str:
    header = html_header(slide.eyebrow, slide.title)
    pg = ""
    if slide.page_no is not None:
        pg = _mono(W - M - 30, H - 18, 30, 10, str(slide.page_no), T["TEXT_FAINT"], 7)
    return f"""
<section class="spigen-slide-page" data-screen-label="{_esc(slide.label)}">
  <div class="slide-label">{_esc(slide.label)}</div>
  <div class="slide">
    {header}
    {slide.content_html}
    {pg}
  </div>
</section>"""


_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=DM+Sans:wght@400;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:100%;height:100%;}}
body{{background:#0a0a0a;font-family:'Noto Sans KR',system-ui,sans-serif;overflow:hidden;}}
.spigen-slide-page{{position:relative;width:{W}px;height:{H}px;background:{T["BG"]};overflow:hidden;}}
.slide-label{{
  position:absolute;left:16px;bottom:12px;z-index:2;
  color:{T["TEXT_FAINT"]};font-size:9px;letter-spacing:0.06em;
  font-family:'DM Sans',system-ui,sans-serif;
  opacity:0.8;
}}
.slide{{
  width:{W}px;height:{H}px;
  background:{T["BG"]};
  position:absolute;top:0;left:0;overflow:hidden;
}}
"""


def build_html(slides: list[Slide]) -> str:
    stage_script_path = Path(__file__).resolve().parent / "spigen_preview_stage.js"
    stage_script = stage_script_path.read_text(encoding="utf-8")
    body = "\n".join(_wrap_slide(s) for s in slides)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Spigen Slides Preview</title>
<style>{_CSS}</style>
</head>
<body>
<spigen-deck-stage width="{W}" height="{H}">
{body}
</spigen-deck-stage>
<script>{stage_script}</script>
</body>
</html>"""


def send(out_path: str, slides: list[Slide], chat="8603864803", key="14132e119c92a946"):
    html = build_html(slides)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 프리뷰 생성: {out_path}")

    r = subprocess.run(
        ["/usr/local/bin/cokacdir", "--sendfile", out_path, "--chat", chat, "--key", key],
        capture_output=True, text=True,
    )
    try:
        res = json.loads(r.stdout)
        if res.get("status") == "ok":
            print("✅ Telegram 전송 완료")
        else:
            print(f"  [FAIL] {res}")
    except Exception:
        print(f"  [RAW] {r.stdout.strip()} {r.stderr.strip()[:100]}")


def send_specs(out_path: str, slide_specs: list[SlideSpec | dict], chat="8603864803", key="14132e119c92a946"):
    slides = [render_slide_spec(spec) for spec in slide_specs]
    send(out_path, slides, chat=chat, key=key)
