"""
ccbot_lib.py — CrossCheck Bot 슬라이드 컴포넌트
캔버스 : 1440 × 810pt  (1920 × 1080px, 16:9)
참조   : https://docs.google.com/presentation/d/1aVvlg0jQyZkcp-jbRqxQ1tQE4Zp0Pn6HsIcvfOY0hpk
"""
import sys
sys.path.insert(0, '/tmp')
from spigen_lib import pt, c255, shape, txt, txtstyle, clr

BG   = {"red": 0, "green": 0, "blue": 0}     # #000000
DARK = c255(14, 14, 14)                        # #0E0E0E
ORNG = c255(255, 107, 26)                      # #FF6B1A
WHT  = {"red": 1, "green": 1, "blue": 1}      # #FFFFFF

W, H, M = 1440, 810, 72   # 캔버스 너비·높이·마진 (pt)


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
    """배경·테두리 완전 제거"""
    return {"updateShapeProperties": {"objectId": oid,
        "fields": "shapeBackgroundFill,outline",
        "shapeProperties": {
            "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
            "outline": {"propertyState": "NOT_RENDERED"}}}}

def _no_fill_border(oid, color, alpha=0.549, wt=0.75):
    """투명 배경 + 반투명 테두리 (원·배지용)"""
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

def _style(oid, color, size, bold=False, strike=False):
    s = {"foregroundColor": {"opaqueColor": {"rgbColor": color}},
         "fontSize": {"magnitude": size, "unit": "PT"},
         "fontFamily": "Noto Sans", "bold": bold}
    f = "foregroundColor,fontSize,fontFamily,bold"
    if strike:
        s["strikethrough"] = True; f += ",strikethrough"
    return {"updateTextStyle": {"objectId": oid, "textRange": {"type": "ALL"},
        "style": s, "fields": f}}

def _page_bg(sid, reqs):
    reqs.append({"updatePageProperties": {"objectId": sid, "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {"solidFill": {"color": {"rgbColor": BG}}}}}})


def _header(sid, page_no, total, section, title, footer, reqs):
    """PAGE XX 태그 / 대형 타이틀 / 오렌지 바 / 페이지 카운터 / 푸터"""
    for oid, x, y, w2, h2, text, color, size, bold in [
        (f"{sid}_sec",   M,         M,   384, 24, f"PAGE {page_no:02d} · {section}", ORNG, 13.5, True),
        (f"{sid}_ttl",   M,       108,   W-M*2, 80, title,                            WHT,  43.5, True),
        (f"{sid}_pname", W-M-190, 138,    72,  22, "크로스체크봇",                   WHT,  12,   False),
        (f"{sid}_pdot",  W-M-118, 138,     9,  21, "·",                               WHT,  12,   False),
        (f"{sid}_pg",    W-M-109, 138,    46,  21, f"{page_no:02d} / {total:02d}",   WHT,  12,   False),
        (f"{sid}_fl",    M,       758,   220,  20, f"CrossCheck Bot · {footer}",      WHT,  10.5, False),
        (f"{sid}_fr",    W-M-33,  758,    33,  19, "2026",                            WHT,  10.5, False),
    ]:
        reqs += [shape(oid, sid, "TEXT_BOX", x, y, w2, h2),
                 txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]

    bar = f"{sid}_bar"
    reqs += [shape(bar, sid, "RECTANGLE", M, 198, 42, 3), _fill(bar, ORNG)]


# ─────────────────────────────────────────────────────────────────────
# A: 현황 비교
# ─────────────────────────────────────────────────────────────────────
def ccbot_compare(sid, rows, callout, insert_index, reqs, page_no=1, total=3, layout_id=None):
    """
    rows = [{"item":"인력 투입","before":"크로스체크 2인","after":"크로스체크 1인 + 봇 체크 1"}, ...]
    callout = "기존 2인 육안 대조를 1인 + 봇으로 전환, 건당 약 100초 · 월 ₩10,000 이하"
    layout_id: 커스텀 마스터 레이아웃 objectId (None이면 predefinedLayout BLANK 사용)
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "현황 분석", "현행 vs 크로스체크봇", "현행 vs 도입 후 비교", reqs)

    # 열 헤더
    for oid, x, text, color in [(f"{sid}_chb", M, "현재", WHT), (f"{sid}_cha", 741, "도입 후", ORNG)]:
        reqs += [shape(oid, sid, "TEXT_BOX", x, 198, 646, 20),
                 txt(oid, text), _style(oid, color, 10.5, bold=True), clr(oid)]

    ROW_Y0, ROW_H, ROW_GAP = 230, 80, 9
    for i, row in enumerate(rows):
        ry = ROW_Y0 + i * (ROW_H + ROW_GAP)

        reqs += [shape(f"{sid}_lb{i}", sid, "RECTANGLE", M, ry, 627, ROW_H), _fill(f"{sid}_lb{i}", DARK)]
        reqs += [shape(f"{sid}_ga{i}", sid, "RECTANGLE", 699, ry, 42, ROW_H), _fill(f"{sid}_ga{i}", DARK)]

        ar = f"{sid}_ar{i}"
        reqs += [shape(ar, sid, "TEXT_BOX", 712, ry+34, 19, 19),
                 txt(ar, "›"), _style(ar, ORNG, 10.5), _ghost(ar), _center(ar)]

        reqs += [shape(f"{sid}_rb{i}", sid, "RECTANGLE", 741, ry, 627, ROW_H), _fill(f"{sid}_rb{i}", ORNG)]

        # 좌: 항목명 + 현행값(취소선)
        reqs += [shape(f"{sid}_ll{i}", sid, "TEXT_BOX", M+22, ry+17, 602, 18),
                 txt(f"{sid}_ll{i}", row["item"]), _style(f"{sid}_ll{i}", WHT, 9.75), clr(f"{sid}_ll{i}")]
        reqs += [shape(f"{sid}_lv{i}", sid, "TEXT_BOX", M+22, ry+37, 602, 28),
                 txt(f"{sid}_lv{i}", row["before"]), _style(f"{sid}_lv{i}", WHT, 16.5, strike=True), clr(f"{sid}_lv{i}")]

        # 우: "개선" + 도입후값
        reqs += [shape(f"{sid}_rl{i}", sid, "TEXT_BOX", 763, ry+17, 601, 18),
                 txt(f"{sid}_rl{i}", "개선"), _style(f"{sid}_rl{i}", ORNG, 9.75, bold=True), clr(f"{sid}_rl{i}")]
        reqs += [shape(f"{sid}_rv{i}", sid, "TEXT_BOX", 763, ry+37, 601, 28),
                 txt(f"{sid}_rv{i}", row["after"]), _style(f"{sid}_rv{i}", WHT, 16.5), clr(f"{sid}_rv{i}")]

    # 하단 callout
    cy = ROW_Y0 + len(rows) * (ROW_H + ROW_GAP) - ROW_GAP + 27
    reqs += [shape(f"{sid}_cbar", sid, "RECTANGLE", M, cy, 2, 53), _fill(f"{sid}_cbar", ORNG)]
    reqs += [shape(f"{sid}_ct", sid, "TEXT_BOX", M+23, cy+15, W-M*2-25, 26),
             txt(f"{sid}_ct", callout), _style(f"{sid}_ct", WHT, 15), _ghost(f"{sid}_ct")]


# ─────────────────────────────────────────────────────────────────────
# B: 프로세스 & 비용 흐름도
# ─────────────────────────────────────────────────────────────────────
def ccbot_flow(sid, steps, table_rows, summary, insert_index, reqs, page_no=2, total=3, layout_id=None):
    """
    steps = [{"num":"01","name":"이미지 업로드","service":"Google Chat API",
              "desc":"라벨 이미지 업로드","cost":"무료","paid":False}, ...]
    table_rows = [("인프라","과금 기준","사용량","월 비용"), ...]  ← 첫 행=헤더
    summary = {"label":"장당 발생 비용","price":"≈ ₩133",
               "subtitle":"월 75장 기준 · 월 ₩10,000 이하","note":"배포시에만 발생"}
    layout_id: 커스텀 마스터 레이아웃 objectId (None이면 predefinedLayout BLANK 사용)
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "프로세스 & 비용", "동작 흐름과 단계별 발생 비용",
            "프로세스 & 비용 구조", reqs)

    # ── Step 카드 ────────────────────────────────────────────────
    CW, CH, CX0, CY = 206, 168, M, 222
    for i, s in enumerate(steps):
        cx, pd = CX0 + i * (CW + 12), s.get("paid", False)
        bid = f"{sid}_sb{i}"
        reqs += [shape(bid, sid, "RECTANGLE", cx, CY, CW, CH),
                 _fill(bid, ORNG, 0.1) if pd else _fill(bid, DARK)]
        ix = cx + 17
        for oid, dy, text, color, size, bold in [
            (f"{sid}_stn{i}", CY+18,  f"STEP {s['num']}",  ORNG if pd else WHT,  9,    False),
            (f"{sid}_snm{i}", CY+37,  s["name"],           WHT,                  16.5, True),
            (f"{sid}_spr{i}", CY+60,  s["service"],        ORNG if pd else WHT,  9.75, False),
            (f"{sid}_sdc{i}", CY+81,  s["desc"],           WHT,                  9.38, False),
            (f"{sid}_slb{i}", CY+113, "월 예상 비용",      WHT,                  8.25, False),
            (f"{sid}_scv{i}", CY+129, s["cost"],
             ORNG if pd else WHT, 15 if pd else 13.5, True),
        ]:
            reqs += [shape(oid, sid, "TEXT_BOX", ix, dy, 178, 26),
                     txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]

        sep = f"{sid}_ssep{i}"
        reqs += [shape(sep, sid, "RECTANGLE", ix, CY+105, 172, 1),
                 _fill(sep, ORNG if pd else WHT, 0.5 if pd else 0.1)]

        if i < len(steps) - 1:
            ar = f"{sid}_sar{i}"
            reqs += [shape(ar, sid, "TEXT_BOX", cx+CW-10, CY+79, 21, 14),
                     txt(ar, "›"), _style(ar, ORNG, 10.5), _ghost(ar), _center(ar)]

    # ── 비용 테이블 ──────────────────────────────────────────────
    TX, TY = M, 420
    reqs += [shape(f"{sid}_tlbl", sid, "TEXT_BOX", TX, TY, 768, 17),
             txt(f"{sid}_tlbl", "인프라별 비용 세부"),
             _style(f"{sid}_tlbl", WHT, 9, bold=True), clr(f"{sid}_tlbl")]

    COL_XS = [TX+14, TX+174, TX+377, TX+603]
    COL_WS = [166, 209, 239, 151]

    def _paid(row): c = row[3] if len(row) > 3 else ""; return ("₩" in c or "$" in c) and "무료" not in c

    for ri, row in enumerate(table_rows):
        is_hdr = ri == 0; is_pd = not is_hdr and _paid(row)
        ry = TY + 23 + ri * 30
        if is_hdr:
            rh = f"{sid}_trhdr"
            reqs += [shape(rh, sid, "RECTANGLE", TX+1, ry, 766, 32), _fill(rh, DARK)]
        elif is_pd:
            rp = f"{sid}_trpd{ri}"
            reqs += [shape(rp, sid, "RECTANGLE", TX+1, ry, 766, 30), _fill(rp, ORNG, 0.1)]

        for ci, cell in enumerate(row):
            cid = f"{sid}_tc{ri}_{ci}"
            color = WHT
            size  = 8.25 if is_hdr else (9.75 if (ci==0 or ci==3) else 9)
            bold  = is_hdr or (not is_hdr and (ci==0 or ci==3))
            if not is_hdr and is_pd and (ci==0 or ci==3): color = ORNG
            reqs += [shape(cid, sid, "TEXT_BOX", COL_XS[ci], ry+(8 if is_hdr else 6), COL_WS[ci], 20),
                     txt(cid, cell), _style(cid, color, size, bold=bold), clr(cid)]

        if ri < len(table_rows)-1:
            ln = f"{sid}_tln{ri}"
            reqs += [shape(ln, sid, "RECTANGLE", TX+1, ry+(32 if is_hdr else 30), 766, 1),
                     _fill(ln, WHT, 0.1)]

    # ── Callout 박스 ─────────────────────────────────────────────
    CLX, CLY, CLW, CLH = 856, 420, 512, 333
    reqs += [shape(f"{sid}_cbox", sid, "RECTANGLE", CLX, CLY, CLW, CLH),
             _fill(f"{sid}_cbox", ORNG, 0.1)]
    for oid, dy, text, color, size, bold in [
        (f"{sid}_clbl", CLY+101, summary["label"],    ORNG, 9,  True),
        (f"{sid}_cpr",  CLY+124, summary["price"],    ORNG, 48, True),
        (f"{sid}_cst",  CLY+178, summary["subtitle"], WHT,  12, False),
        (f"{sid}_cnt",  CLY+205, summary.get("note",""), WHT, 9, False),
    ]:
        reqs += [shape(oid, sid, "TEXT_BOX", CLX+24, dy, 477, 50),
                 txt(oid, text), _style(oid, color, size, bold=bold), clr(oid)]


# ─────────────────────────────────────────────────────────────────────
# C: 로드맵 (Phase 카드 + Schedule + KPI)
# ─────────────────────────────────────────────────────────────────────
def ccbot_roadmap(sid, phases, schedule, kpi, insert_index, reqs, page_no=3, total=3, layout_id=None):
    """
    phases = [
        {"label":"Phase 1 · 개발","period":"~ 2026. 08","title":"봇 개발 완료",
         "bullets":["9개 항목 자동 대조 로직 개발",...],
         "current":True,
         "note":"← 현재 지점",
         "note_body":"개발 기간 동안 월 최대 5만 원 발생 가능"},
        ...
    ]
    schedule = [{"num":"1","title":"봇 개발 완료","when":"~ 8월"}, ...]
    kpi = {"label":"파일럿 목표 · 연말 리뷰 지표",
           "text":"OCR 정확도 95% 이상 · 월 실사용 비용 정확 산출 · 팀원 사용 만족도 90% 이상"}
    layout_id: 커스텀 마스터 레이아웃 objectId (None이면 predefinedLayout BLANK 사용)
    """
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({"createSlide": {"objectId": sid, "insertionIndex": insert_index,
        "slideLayoutReference": layout_ref}})
    _page_bg(sid, reqs)
    _header(sid, page_no, total, "NEXT STEPS", "일정 · 목표 · 확장 계획", "일정 · 목표 · 확장 계획", reqs)

    # ROADMAP 라벨
    reqs += [shape(f"{sid}_rmlbl", sid, "TEXT_BOX", M, 292, 120, 16),
             txt(f"{sid}_rmlbl", "ROADMAP"), _style(f"{sid}_rmlbl", WHT, 9, bold=True), clr(f"{sid}_rmlbl")]

    # Phase 카드
    PW, PH, PX0, PY = 245, 270, M, 320
    for pi, ph in enumerate(phases):
        px, cur = PX0 + pi * (PW + 12), ph.get("current", False)
        bg = f"{sid}_phbg{pi}"
        reqs += [shape(bg, sid, "RECTANGLE", px, PY, PW, PH),
                 _fill(bg, ORNG if cur else DARK, 0.1)]
        ix = px + 17

        reqs += [shape(f"{sid}_phl{pi}", sid, "TEXT_BOX", ix, PY+19, 217, 14),
                 txt(f"{sid}_phl{pi}", ph["label"]),
                 _style(f"{sid}_phl{pi}", ORNG if cur else WHT, 8.25), clr(f"{sid}_phl{pi}")]
        reqs += [shape(f"{sid}_php{pi}", sid, "TEXT_BOX", ix, PY+38, 217, 18),
                 txt(f"{sid}_php{pi}", ph["period"]),
                 _style(f"{sid}_php{pi}", WHT, 9.75), clr(f"{sid}_php{pi}")]
        reqs += [shape(f"{sid}_pht{pi}", sid, "TEXT_BOX", ix, PY+55, 217, 23),
                 txt(f"{sid}_pht{pi}", ph["title"]),
                 _style(f"{sid}_pht{pi}", WHT, 16.5, bold=True), clr(f"{sid}_pht{pi}")]

        for bi, b in enumerate(ph.get("bullets", [])[:4]):
            dot = f"{sid}_dot{pi}_{bi}"
            reqs += [shape(dot, sid, "RECTANGLE", ix, PY+94+bi*24, 3, 3),
                     _fill(dot, ORNG if cur else WHT, 1.0 if cur else 0.4)]
            reqs += [shape(f"{sid}_bt{pi}_{bi}", sid, "TEXT_BOX", ix+11, PY+88+bi*24, 195, 18),
                     txt(f"{sid}_bt{pi}_{bi}", b),
                     _style(f"{sid}_bt{pi}_{bi}", WHT, 10.5), clr(f"{sid}_bt{pi}_{bi}")]

        if cur:
            reqs += [shape(f"{sid}_phsp{pi}", sid, "RECTANGLE", ix, PY+190, 211, 1),
                     _fill(f"{sid}_phsp{pi}", ORNG, 0.5)]
            reqs += [shape(f"{sid}_phnt{pi}", sid, "TEXT_BOX", ix, PY+200, 217, 17),
                     txt(f"{sid}_phnt{pi}", ph.get("note", "← 현재 지점")),
                     _style(f"{sid}_phnt{pi}", ORNG, 9, bold=True), clr(f"{sid}_phnt{pi}")]
            if ph.get("note_body"):
                reqs += [shape(f"{sid}_phnb{pi}", sid, "TEXT_BOX", ix, PY+221, 217, 33),
                         txt(f"{sid}_phnb{pi}", ph["note_body"]),
                         _style(f"{sid}_phnb{pi}", WHT, 10.5, bold=True), clr(f"{sid}_phnb{pi}")]

    # SCHEDULE 섹션
    SC_X, SC_Y, SC_W, SC_H = 862, 320, 506, 212
    reqs += [shape(f"{sid}_sclbl", sid, "TEXT_BOX", SC_X, 292, 120, 16),
             txt(f"{sid}_sclbl", "SCHEDULE"), _style(f"{sid}_sclbl", WHT, 9, bold=True), clr(f"{sid}_sclbl")]
    reqs += [shape(f"{sid}_scbox", sid, "ROUND_RECTANGLE", SC_X, SC_Y, SC_W, SC_H), _fill(f"{sid}_scbox", DARK)]

    for si2, sc in enumerate(schedule):
        ry = SC_Y + 20 + si2 * 51
        if si2 > 0:
            reqs += [shape(f"{sid}_scln{si2}", sid, "RECTANGLE", SC_X, ry-1, SC_W, 1),
                     _fill(f"{sid}_scln{si2}", WHT, 0.1)]

        # 숫자 원 (투명 배경 + 반투명 오렌지 테두리)
        reqs += [shape(f"{sid}_circ{si2}", sid, "RECTANGLE", SC_X+17, ry, 21, 21),
                 _no_fill_border(f"{sid}_circ{si2}", ORNG)]
        reqs += [shape(f"{sid}_cnum{si2}", sid, "TEXT_BOX", SC_X+15, ry+1, 26, 22),
                 txt(f"{sid}_cnum{si2}", str(sc["num"])),
                 _style(f"{sid}_cnum{si2}", ORNG, 9.75, bold=True),
                 _ghost(f"{sid}_cnum{si2}"), _center(f"{sid}_cnum{si2}"), _mid_v(f"{sid}_cnum{si2}")]

        reqs += [shape(f"{sid}_stask{si2}", sid, "TEXT_BOX", SC_X+54, ry+1, 390, 22),
                 txt(f"{sid}_stask{si2}", sc["title"]),
                 _style(f"{sid}_stask{si2}", WHT, 12, bold=True), clr(f"{sid}_stask{si2}")]

        bw = max(35, min(55, len(sc["when"]) * 9))
        bx = SC_X + SC_W - bw - 10
        reqs += [shape(f"{sid}_bdg{si2}", sid, "RECTANGLE", bx, ry-1, bw, 23),
                 _no_fill_border(f"{sid}_bdg{si2}", ORNG)]
        reqs += [shape(f"{sid}_bwt{si2}", sid, "TEXT_BOX", bx+4, ry+3, bw-8, 18),
                 txt(f"{sid}_bwt{si2}", sc["when"]),
                 _style(f"{sid}_bwt{si2}", ORNG, 9.75, bold=True),
                 _ghost(f"{sid}_bwt{si2}"), _center(f"{sid}_bwt{si2}")]

    # KPI 박스
    KY = SC_Y + SC_H + 16
    reqs += [shape(f"{sid}_kbox", sid, "RECTANGLE", SC_X, KY, SC_W, 77), _fill(f"{sid}_kbox", ORNG, 0.1)]
    reqs += [shape(f"{sid}_klbl", sid, "TEXT_BOX", SC_X+18, KY+17, 483, 17),
             txt(f"{sid}_klbl", kpi["label"]),
             _style(f"{sid}_klbl", ORNG, 9, bold=True), clr(f"{sid}_klbl")]
    reqs += [shape(f"{sid}_ktxt", sid, "TEXT_BOX", SC_X+18, KY+40, 483, 22),
             txt(f"{sid}_ktxt", kpi["text"]),
             _style(f"{sid}_ktxt", WHT, 12, bold=True), clr(f"{sid}_ktxt")]
