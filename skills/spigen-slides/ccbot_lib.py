"""
ccbot_lib.py — CrossCheck Bot 슬라이드 컴포넌트
캔버스 : 720 × 405pt  (16:9)
참조   : https://docs.google.com/presentation/d/1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo/edit
         slide 6 = PAGE 01, slide 7 = PAGE 03, slide 8 = PAGE 02
"""
import sys
sys.path.insert(0, '/tmp')
from spigen_lib import pt, c255, shape, txt, txtstyle, clr

BG   = {"red": 0, "green": 0, "blue": 0}      # #000000
DARK = c255(14, 14, 14)                         # #0E0E0E
ORNG = c255(255, 107, 26)                       # #FF6B1A
WHT  = {"red": 1, "green": 1, "blue": 1}       # #FFFFFF
RED  = c255(255, 0, 0)                          # #FF0000 (현행값)
GRAY = c255(217, 217, 217)                      # #D9D9D9 (항목명)

W, H, M = 720, 405, 36   # 캔버스 너비·높이·마진 (pt)


# ── 내부 헬퍼 ────────────────────────────────────────────────────────

def _fill(oid, color, alpha=1.0):
    return {"updateShapeProperties": {"objectId": oid, "fields": "shapeBackgroundFill",
        "shapeProperties": {"shapeBackgroundFill": {"solidFill": {
            "alpha": alpha, "color": {"rgbColor": color}}}}}}

def _border(oid, color, alpha=1.0, wt=0.75):
    return {"updateShapeProperties": {"objectId": oid, "fields": "outline",
        "shapeProperties": {"outline": {"outlineFill": {"solidFill": {
            "alpha": alpha, "color": {"rgbColor": color}}},
            "weight": {"magnitude": pt(wt), "unit": "EMU"}}}}}

def _ghost(oid):
    return {"updateShapeProperties": {"objectId": oid,
        "fields": "shapeBackgroundFill,outline",
        "shapeProperties": {
            "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
            "outline": {"propertyState": "NOT_RENDERED"}}}}

def _no_fill_border(oid, color, alpha=0.549, wt=0.75):
    return {"updateShapeProperties": {"objectId": oid,
        "fields": "shapeBackgroundFill,outline",
        "shapeProperties": {
            "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
            "outline": {"outlineFill": {"solidFill": {
                "alpha": alpha, "color": {"rgbColor": color}}},
                "weight": {"magnitude": pt(wt), "unit": "EMU"}}}}}

def _center(oid):
    return {"updateParagraphStyle": {"objectId": oid, "textRange": {"type": "ALL"},
        "style": {"alignment": "CENTER"}, "fields": "alignment"}}

def _mid_v(oid):
    return {"updateShapeProperties": {"objectId": oid, "fields": "contentAlignment",
        "shapeProperties": {"contentAlignment": "MIDDLE"}}}

def _style(oid, color, size, bold=False):
    return {"updateTextStyle": {"objectId": oid, "textRange": {"type": "ALL"},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": color}},
                  "fontSize": {"magnitude": size, "unit": "PT"},
                  "fontFamily": "Noto Sans", "bold": bold},
        "fields": "foregroundColor,fontSize,fontFamily,bold"}}

def _page_bg(sid, reqs):
    reqs.append({"updatePageProperties": {"objectId": sid, "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": BG}}}}}})


def _header(sid, page_no, total, section, title, footer, reqs):
    for oid, x, y, w2, h2, text, color, size, bold in [
        (f"{sid}_sec",   M,      M,    192, 12, f"PAGE {page_no:02d} · {section}", ORNG, 7,  True),
        (f"{sid}_ttl",   M,      54,   W-M*2, 40, title,                            WHT,  22, True),
        (f"{sid}_pname", W-M-95, 69,    36,  11, "크로스체크봇",                   WHT,  6,  False),
        (f"{sid}_pdot",  W-M-59, 69,     4,  10, "·",                               WHT,  6,  False),
        (f"{sid}_pg",    W-M-55, 69,    23,  10, f"{page_no:02d} / {total:02d}",   WHT,  6,  False),
        (f"{sid}_fl",    M,     379,   110,  10, f"CrossCheck Bot · {footer}",      WHT,  5,  False),
        (f"{sid}_fr",    W-M-17,379,    17,   9, "2026",                            WHT,  5,  False),
    ]:
        reqs += [shape(oid, sid, "TEXT_BOX", x, y, w2, h2),
                 txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]

    bar = f"{sid}_bar"
    reqs += [shape(bar, sid, "RECTANGLE", M, 99, 21, 1.5), _fill(bar, ORNG)]


# ─────────────────────────────────────────────────────────────────────
# A: 현황 비교
# ─────────────────────────────────────────────────────────────────────
def ccbot_compare(sid, rows, callout, insert_index, reqs, page_no=1, total=3, layout_id=None):
    """
    rows = [{"item":"인력 투입","before":"크로스체크 2인","after":"봇 자동 대조"}, ...]
    callout = "요약 메시지"
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "현황 분석", "현행 vs 크로스체크봇", "현행 vs 도입 후 비교", reqs)

    # 열 헤더
    for oid, x, text, color, bold in [
        (f"{sid}_chb", M,     "현재",  RED,  False),
        (f"{sid}_cha", 370.5, "도입 후", ORNG, True),
    ]:
        reqs += [shape(oid, sid, "TEXT_BOX", x, 109, 300, 10),
                 txt(oid, text), _style(oid, color, 5, bold=bold), clr(oid)]

    ROW_Y0, ROW_H, ROW_GAP = 125.2, 40, 5
    for i, row in enumerate(rows):
        ry = ROW_Y0 + i * (ROW_H + ROW_GAP)

        reqs += [shape(f"{sid}_lb{i}", sid, "RECTANGLE", M,     ry, 313.5, ROW_H), _fill(f"{sid}_lb{i}", DARK)]
        reqs += [shape(f"{sid}_ga{i}", sid, "RECTANGLE", 349.5, ry, 21,    ROW_H), _fill(f"{sid}_ga{i}", DARK)]
        reqs += [shape(f"{sid}_rb{i}", sid, "RECTANGLE", 370.5, ry, 313.5, ROW_H), _fill(f"{sid}_rb{i}", ORNG)]

        ar = f"{sid}_ar{i}"
        reqs += [shape(ar, sid, "TEXT_BOX", 356, ry+17, 10, 10),
                 txt(ar, "›"), _style(ar, ORNG, 5), _ghost(ar), _center(ar)]

        # 좌: 항목명 + 현행값(RED)
        reqs += [shape(f"{sid}_ll{i}", sid, "TEXT_BOX", M+11, ry+8,  297, 9),
                 txt(f"{sid}_ll{i}", row["item"]),   _style(f"{sid}_ll{i}", GRAY, 5), clr(f"{sid}_ll{i}")]
        reqs += [shape(f"{sid}_lv{i}", sid, "TEXT_BOX", M+11, ry+18, 297, 14),
                 txt(f"{sid}_lv{i}", row["before"]), _style(f"{sid}_lv{i}", RED,  8), clr(f"{sid}_lv{i}")]

        # 우: "개선" + 도입후값
        reqs += [shape(f"{sid}_rl{i}", sid, "TEXT_BOX", 382, ry+8,  297, 9),
                 txt(f"{sid}_rl{i}", "개선"),        _style(f"{sid}_rl{i}", ORNG, 5, bold=True), clr(f"{sid}_rl{i}")]
        reqs += [shape(f"{sid}_rv{i}", sid, "TEXT_BOX", 382, ry+18, 297, 14),
                 txt(f"{sid}_rv{i}", row["after"]),  _style(f"{sid}_rv{i}", WHT,  8), clr(f"{sid}_rv{i}")]

    # 하단 callout
    cy = ROW_Y0 + len(rows) * (ROW_H + ROW_GAP) - ROW_GAP + 14
    reqs += [shape(f"{sid}_cbar", sid, "RECTANGLE", M, cy, 1, 26), _fill(f"{sid}_cbar", ORNG)]
    reqs += [shape(f"{sid}_ct", sid, "TEXT_BOX", M+12, cy+7, W-M*2-13, 13),
             txt(f"{sid}_ct", callout), _style(f"{sid}_ct", WHT, 7), _ghost(f"{sid}_ct")]


# ─────────────────────────────────────────────────────────────────────
# B: 프로세스 & 비용 흐름도
# ─────────────────────────────────────────────────────────────────────
def ccbot_flow(sid, steps, table_rows, summary, insert_index, reqs, page_no=2, total=3, layout_id=None):
    """
    steps = [{"num":"01","name":"이미지 업로드","service":"Google Chat API",
              "desc":"라벨 이미지 업로드","cost":"무료","paid":False}, ...]
    table_rows = [("인프라","과금 기준","사용량","월 비용"), ...]  ← 첫 행=헤더
    summary = {"label":"장당 발생 비용","price":"≈ ₩133",
               "subtitle":"월 75장 기준 · 월 ₩10,000 이하","note":"..."}
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "프로세스 & 비용", "동작 흐름과 단계별 발생 비용",
            "프로세스 & 비용 구조", reqs)

    # ── Step 카드 ────────────────────────────────────────────────
    CW, CH, CX0, CY = 103, 84, M, 111.1
    STEP_GAP = 6
    for i, s in enumerate(steps):
        cx = CX0 + i * (CW + STEP_GAP)
        pd = s.get("paid", False)
        bid = f"{sid}_sb{i}"
        reqs += [shape(bid, sid, "RECTANGLE", cx, CY, CW, CH),
                 _fill(bid, ORNG, 0.1) if pd else _fill(bid, DARK)]
        ix = cx + 9
        for oid, dy, text, color, size, bold in [
            (f"{sid}_stn{i}", CY+8.6,  f"STEP {s['num']}",  ORNG if pd else WHT,  5,   False),
            (f"{sid}_snm{i}", CY+18.2, s["name"],            WHT,                  8,   True),
            (f"{sid}_spr{i}", CY+29.9, s["service"],         ORNG if pd else WHT,  5,   False),
            (f"{sid}_sdc{i}", CY+40.3, s["desc"],            WHT,                  5,   False),
            (f"{sid}_slb{i}", CY+56.5, "월 예상 비용",       WHT,                  4,   False),
            (f"{sid}_scv{i}", CY+64.5, s["cost"],
             ORNG if pd else WHT, 8 if pd else 7, True),
        ]:
            reqs += [shape(oid, sid, "TEXT_BOX", ix, dy, 89, 10),
                     txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]

        sep = f"{sid}_ssep{i}"
        reqs += [shape(sep, sid, "RECTANGLE", ix, CY+52.4, 86, 0.5),
                 _fill(sep, ORNG if pd else WHT, 0.5 if pd else 0.1)]

        if i < len(steps) - 1:
            ar = f"{sid}_sar{i}"
            reqs += [shape(ar, sid, "TEXT_BOX", cx+CW-5, CY+39.3, 10, 7),
                     txt(ar, "›"), _style(ar, ORNG, 5), _ghost(ar), _center(ar)]

    # ── 비용 테이블 ──────────────────────────────────────────────
    TX, TY = M, 210
    reqs += [shape(f"{sid}_tlbl", sid, "TEXT_BOX", TX, TY, 384, 8),
             txt(f"{sid}_tlbl", "인프라별 비용 세부"),
             _style(f"{sid}_tlbl", WHT, 5, bold=True), clr(f"{sid}_tlbl")]

    COL_XS = [43, 123, 225, 338]
    COL_WS = [80, 102, 113, 90]

    def _paid(row):
        c = row[3] if len(row) > 3 else ""
        return ("₩" in c or "$" in c) and "무료" not in c

    # 헤더 행
    HEADER_Y = TY + 12
    rh = f"{sid}_trhdr"
    reqs += [shape(rh, sid, "RECTANGLE", TX+1, HEADER_Y, 383, 16), _fill(rh, DARK)]
    for ci, cell in enumerate(table_rows[0]):
        cid = f"{sid}_tc0_{ci}"
        reqs += [shape(cid, sid, "TEXT_BOX", COL_XS[ci], HEADER_Y+4.5, COL_WS[ci], 10),
                 txt(cid, cell), _style(cid, WHT, 4), clr(cid)]
    reqs += [shape(f"{sid}_tln0", sid, "RECTANGLE", TX+1, HEADER_Y+16, 383, 0.5),
             _fill(f"{sid}_tln0", WHT, 0.1)]

    # 데이터 행
    for ri, row in enumerate(table_rows[1:], start=1):
        is_pd = _paid(row)
        text_y = TY + 31.6 + (ri - 1) * 15.4
        sep_y  = text_y + 11.3
        if is_pd:
            rp = f"{sid}_trpd{ri}"
            reqs += [shape(rp, sid, "RECTANGLE", TX+1, sep_y-11.3, 383, 15), _fill(rp, ORNG, 0.1)]
        for ci, cell in enumerate(row):
            cid = f"{sid}_tc{ri}_{ci}"
            color = WHT
            bold  = (ci == 0 or ci == 3)
            if is_pd and (ci == 0 or ci == 3): color = ORNG
            reqs += [shape(cid, sid, "TEXT_BOX", COL_XS[ci], text_y, COL_WS[ci], 10),
                     txt(cid, cell), _style(cid, color, 5, bold=bold), clr(cid)]
        if ri < len(table_rows) - 1:
            ln = f"{sid}_tln{ri}"
            reqs += [shape(ln, sid, "RECTANGLE", TX+1, sep_y, 383, 0.5),
                     _fill(ln, WHT, 0.1)]

    # ── Callout 박스 ─────────────────────────────────────────────
    CLX, CLY, CLW, CLH = 428, 210, 256, 167
    reqs += [shape(f"{sid}_cbox", sid, "RECTANGLE", CLX, CLY, CLW, CLH),
             _fill(f"{sid}_cbox", ORNG, 0.1)]
    for oid, dy, text, color, size, bold in [
        (f"{sid}_clbl", CLY+50.4, summary["label"],       ORNG, 5,  True),
        (f"{sid}_cpr",  CLY+61.8, summary["price"],       ORNG, 24, True),
        (f"{sid}_cst",  CLY+88.8, summary["subtitle"],    WHT,  6,  False),
        (f"{sid}_cnt",  CLY+102.7, summary.get("note",""), WHT,  5,  False),
    ]:
        reqs += [shape(oid, sid, "TEXT_BOX", CLX+12, dy, 238, 25),
                 txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]


# ─────────────────────────────────────────────────────────────────────
# C: 로드맵 (Phase 카드 + Schedule/KPI)
# ─────────────────────────────────────────────────────────────────────
def ccbot_roadmap(sid, phases, schedule, kpi, insert_index, reqs, page_no=3, total=3, layout_id=None):
    """
    phases = [
        {"label":"Phase 1 · 개발","period":"~ 2026. 08","title":"봇 개발 완료",
         "bullets":[...], "current":True, "note":"← 현재 지점", "note_body":"..."},
        ...
    ]
    schedule = [{"num":"1","title":"봇 개발 완료","when":"~ 8월"}, ...]  (미사용, 원본과 레이아웃 통일)
    kpi = {"label":"파일럿 목표 · 연말 리뷰 지표", "text":"..."}
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "NEXT STEPS", "일정 · 목표 · 확장 계획", "일정 · 목표 · 확장 계획", reqs)

    # ROADMAP 라벨
    reqs += [shape(f"{sid}_rmlbl", sid, "TEXT_BOX", M, 121, 60, 8),
             txt(f"{sid}_rmlbl", "ROADMAP"), _style(f"{sid}_rmlbl", WHT, 5, bold=True), clr(f"{sid}_rmlbl")]

    # Phase 카드 배치 (원본: x=36, 186, 554 / 중간에 Schedule+KPI)
    PY = 146
    PH = 130
    PHASE_LAYOUT = [
        (36,  150),   # Phase 1
        (186, 181),   # Phase 2
        (554, 130),   # Phase 3
    ]

    for pi, ph in enumerate(phases[:3]):
        px, PW = PHASE_LAYOUT[pi]
        cur = ph.get("current", False)

        bg = f"{sid}_phbg{pi}"
        reqs += [shape(bg, sid, "RECTANGLE", px, PY, PW, PH),
                 _fill(bg, ORNG if cur else DARK, 0.1)]
        ix = px + 10

        reqs += [shape(f"{sid}_phl{pi}", sid, "TEXT_BOX", ix, PY+13, PW-15, 9),
                 txt(f"{sid}_phl{pi}", ph["label"]),
                 _style(f"{sid}_phl{pi}", ORNG if cur else WHT, 4.5), clr(f"{sid}_phl{pi}")]
        reqs += [shape(f"{sid}_php{pi}", sid, "TEXT_BOX", ix, PY+24, PW-15, 9),
                 txt(f"{sid}_php{pi}", ph["period"]),
                 _style(f"{sid}_php{pi}", WHT, 5), clr(f"{sid}_php{pi}")]
        reqs += [shape(f"{sid}_pht{pi}", sid, "TEXT_BOX", ix, PY+34, PW-15, 12),
                 txt(f"{sid}_pht{pi}", ph["title"]),
                 _style(f"{sid}_pht{pi}", WHT, 8, bold=True), clr(f"{sid}_pht{pi}")]

        for bi, b in enumerate(ph.get("bullets", [])[:3]):
            dot = f"{sid}_dot{pi}_{bi}"
            reqs += [shape(dot, sid, "RECTANGLE", ix, PY+47+bi*14, 1.5, 1.5),
                     _fill(dot, ORNG if cur else WHT, 1.0 if cur else 0.4)]
            reqs += [shape(f"{sid}_bt{pi}_{bi}", sid, "TEXT_BOX", ix+6, PY+43+bi*14, PW-22, 9),
                     txt(f"{sid}_bt{pi}_{bi}", b),
                     _style(f"{sid}_bt{pi}_{bi}", WHT, 5), clr(f"{sid}_bt{pi}_{bi}")]

        if cur:
            reqs += [shape(f"{sid}_phsp{pi}", sid, "RECTANGLE", ix, PY+102, PW-15, 0.5),
                     _fill(f"{sid}_phsp{pi}", ORNG, 0.5)]
            reqs += [shape(f"{sid}_phnt{pi}", sid, "TEXT_BOX", ix, PY+108, PW-15, 9),
                     txt(f"{sid}_phnt{pi}", ph.get("note", "← 현재 지점")),
                     _style(f"{sid}_phnt{pi}", ORNG, 5, bold=True), clr(f"{sid}_phnt{pi}")]
            if ph.get("note_body"):
                reqs += [shape(f"{sid}_phnb{pi}", sid, "TEXT_BOX", ix, PY+121, PW-15, 18),
                         txt(f"{sid}_phnb{pi}", ph["note_body"]),
                         _style(f"{sid}_phnb{pi}", WHT, 5, bold=True), clr(f"{sid}_phnb{pi}")]

    # Schedule+KPI 박스 (원본: x=366.8, y=146)
    SC_X, SC_Y, SC_W = 367, PY, 187
    reqs += [shape(f"{sid}_scbox", sid, "RECTANGLE", SC_X, SC_Y, SC_W, PH), _fill(f"{sid}_scbox", DARK)]

    reqs += [shape(f"{sid}_klbl", sid, "TEXT_BOX", SC_X+11, SC_Y+21, SC_W-22, 9),
             txt(f"{sid}_klbl", kpi["label"]),
             _style(f"{sid}_klbl", ORNG, 5, bold=True), clr(f"{sid}_klbl")]
    reqs += [shape(f"{sid}_ktxt", sid, "TEXT_BOX", SC_X+11, SC_Y+41, SC_W-22, 50),
             txt(f"{sid}_ktxt", kpi["text"]),
             _style(f"{sid}_ktxt", WHT, 6, bold=True), clr(f"{sid}_ktxt")]
