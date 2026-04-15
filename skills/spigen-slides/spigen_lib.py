# spigen_lib.py — Spigen Slides 컴포넌트 라이브러리
# SKILL.md의 Step 3-5에서 분리된 Google Slides API 헬퍼 및 컴포넌트 코드
# 사용: import 후 reqs 리스트에 append하고 batchUpdate로 한 번에 실행

def pt(v): return int(v * 12700)
def c255(r, g, b): return {"red": r/255, "green": g/255, "blue": b/255}

ORANGE = c255(255, 105,   0)   # #FF6900 (테마 불문 고정)
WHITE  = {"red": 1, "green": 1, "blue": 1}
BLACK  = c255(26, 26, 26)

# 테마별 색상 토큰 — 배경이 검정(dark)이면 텍스트·카드가 밝게, 흰(light)이면 어둡게
THEMES = {
    'dark': {
        'SLIDE_BG':    {"red": 0,        "green": 0,        "blue": 0},        # #000000
        'TITLE_COLOR': c255(249, 250, 251),   # #F9FAFB
        'BODY_COLOR':  c255(107, 114, 128),   # #6B7280
        'CARD_BG':     c255( 10,  10,  10),   # #0A0A0A
        'CARD_BORDER': c255( 20,  20,  20),   # #141414
    },
    'light': {
        'SLIDE_BG':    {"red": 1,        "green": 1,        "blue": 1},        # #FFFFFF
        'TITLE_COLOR': c255( 26,  26,  26),   # #1A1A1A
        'BODY_COLOR':  c255( 74,  74,  74),   # #4A4A4A
        'CARD_BG':     c255(245, 245, 245),   # #F5F5F5
        'CARD_BORDER': c255(229, 229, 229),   # #E5E5E5
    },
    'warm': {
        'SLIDE_BG':    c255(245, 240, 232),   # #F5F0E8 베이지
        'TITLE_COLOR': c255( 26,  26,  26),   # #1A1A1A
        'BODY_COLOR':  c255( 74,  74,  74),   # #4A4A4A
        'CARD_BG':     {"red": 1, "green": 1, "blue": 1},  # #FFFFFF
        'CARD_BORDER': c255(200, 196, 190),   # #C8C4BE
    },
}

def shape(oid, page, stype, x, y, w, h):
    return {"createShape": {"objectId": oid, "shapeType": stype,
        "elementProperties": {"pageObjectId": page,
            "size": {"width":  {"magnitude": pt(w), "unit": "EMU"},
                     "height": {"magnitude": pt(h), "unit": "EMU"}},
            "transform": {"scaleX":1,"scaleY":1,
                "translateX": pt(x),"translateY": pt(y),"unit":"EMU"}}}}

def fill(oid, fg, bg=None, wt=0.6):
    bg = bg or fg
    return {"updateShapeProperties": {"objectId": oid,
        "fields": "shapeBackgroundFill,outline",
        "shapeProperties": {
            "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": fg}}},
            "outline": {"outlineFill": {"solidFill": {"color": {"rgbColor": bg}}},
                        "weight": {"magnitude": pt(wt), "unit": "EMU"}}}}}

def txtstyle(oid, color, size, bold=False):
    return {"updateTextStyle": {"objectId": oid,
        "textRange": {"type": "ALL"},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": color}},
                  "fontSize": {"magnitude": size, "unit": "PT"},
                  "fontFamily": "Noto Sans", "bold": bold},
        "fields": "foregroundColor,fontSize,fontFamily,bold"}}

def txt(oid, text):
    return {"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}}


def slide_base(slide_oid, title_text, insert_index, reqs, theme='dark'):
    T = THEMES[theme]
    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    # 배경색 (테마에 따라 결정)
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})
    # 상단 오렌지 바 (테마 불문 고정)
    bar = f"{slide_oid}_bar"
    reqs += [shape(bar, slide_oid, "RECTANGLE", 0, 0, 720, 3), fill(bar, ORANGE)]
    # 제목 (테마에 따라 글자색 결정)
    ttl = f"{slide_oid}_ttl"
    reqs += [shape(ttl, slide_oid, "TEXT_BOX", 56, 44, 500, 22),
             txt(ttl, title_text), txtstyle(ttl, T['TITLE_COLOR'], 17, bold=True)]


# 열 색상 설정 — 테마별로 구분 (라벨 색·왼쪽 바 색)
COL_STYLES = {
    'dark': {
        "현재":             {"lbl": c255(107,114,128), "bar": c255( 20, 20, 20)},
        "문제점":           {"lbl": c255(239, 68, 68), "bar": c255(127, 29, 29)},
        "도입 시 기대효과": {"lbl": c255( 52,211,153), "bar": c255(  6, 78, 59)},
    },
    'light': {
        "현재":             {"lbl": c255(107,114,128), "bar": c255(229,231,235)},
        "문제점":           {"lbl": c255(220, 38, 38), "bar": c255(254,226,226)},
        "도입 시 기대효과": {"lbl": c255(  5,150,105), "bar": c255(209,250,229)},
    },
}
PAD, COL_W, ARW_W = 56, 189, 20
COL_Y, LBL_H, ITEM_H, ITEM_GAP = 83, 11, 24, 5

def mk_3col(sid, cols, reqs, theme='light'):
    """cols = [{"label":"현재", "items":["항목1","항목2",...]}, ...]
    theme: 'dark' (검정 배경) | 'light' (흰 배경, 기본값)
    """
    T = THEMES[theme]
    sty_map = COL_STYLES[theme]
    CX = [PAD, PAD+COL_W+ARW_W, PAD+COL_W*2+ARW_W*2]
    AX = [PAD+COL_W, PAD+COL_W*2+ARW_W]

    for ci, col in enumerate(cols):
        cx  = CX[ci]
        sty = sty_map.get(col["label"], {"lbl": T['BODY_COLOR'], "bar": T['CARD_BORDER']})
        IY0 = COL_Y + LBL_H + 8

        lid = f"{sid}_lbl{ci}"
        reqs += [shape(lid, sid, "TEXT_BOX", cx, COL_Y, COL_W, LBL_H),
                 txt(lid, col["label"].upper()),
                 txtstyle(lid, sty["lbl"], 6.5, bold=True)]

        for ii, item in enumerate(col["items"]):
            iy = IY0 + ii*(ITEM_H+ITEM_GAP)
            bid, cid = f"{sid}_b{ci}{ii}", f"{sid}_c{ci}{ii}"
            reqs += [
                shape(bid, sid, "RECTANGLE", cx, iy, 2, ITEM_H),
                fill(bid, sty["bar"]),
                shape(cid, sid, "ROUND_RECTANGLE", cx+2, iy, COL_W-2, ITEM_H),
                fill(cid, T['CARD_BG'], T['CARD_BORDER']),
                txt(cid, item),
                txtstyle(cid, T['BODY_COLOR'], 7.5),
            ]

    for ai, ax in enumerate(AX):
        aid = f"{sid}_arw{ai}"
        reqs += [shape(aid, sid, "TEXT_BOX", ax, COL_Y+26, ARW_W, 18),
                 txt(aid, "›"), txtstyle(aid, ORANGE, 13, bold=True),
                 {"updateParagraphStyle": {"objectId": aid,
                   "textRange":{"type":"ALL"},
                   "style":{"alignment":"CENTER"},"fields":"alignment"}}]


def mk_flow(sid, steps, cost_map, reqs, theme='dark'):
    """
    steps    = [("STEP 01","이름","서비스", is_paid), ...]
    cost_map = {step_index: "₩X,XXX~X,XXX"}
    theme: 'dark' (기본값) | 'light'
    """
    T = THEMES[theme]
    N = len(steps)
    BW, FH, AW = 108, 55, 14
    FY = 50
    SX = (720 - N*BW - (N-1)*AW) // 2

    for i, (step, name, svc, paid) in enumerate(steps):
        bx  = SX + i*(BW+AW)
        bid = f"{sid}_s{i}"
        # 유료 스텝: 오렌지 테두리 강조 / 일반 스텝: 테마 카드색
        fc  = c255(13,7,0) if paid else T['CARD_BG']
        bc  = ORANGE       if paid else T['CARD_BORDER']
        reqs += [shape(bid, sid, "ROUND_RECTANGLE", bx, FY, BW, FH),
                 fill(bid, fc, bc, 0.8),
                 txt(bid, f"{step}\n{name}\n{svc}"),
                 txtstyle(bid, T['BODY_COLOR'], 6.5)]

        if i < N-1:
            lid = f"{sid}_l{i}"
            reqs += [
                {"createLine": {"objectId": lid, "lineCategory": "STRAIGHT",
                    "elementProperties": {"pageObjectId": sid,
                        "size": {"width":{"magnitude":pt(AW),"unit":"EMU"},
                                 "height":{"magnitude":pt(1),"unit":"EMU"}},
                        "transform":{"scaleX":1,"scaleY":1,
                            "translateX":pt(bx+BW),"translateY":pt(FY+FH//2),
                            "unit":"EMU"}}}},
                {"updateLineProperties": {"objectId": lid,
                    "fields": "lineFill,weight,endArrow",
                    "lineProperties": {
                        "lineFill": {"solidFill": {"color": {"rgbColor": ORANGE}}},
                        "weight": {"magnitude": pt(1), "unit": "EMU"},
                        "endArrow": "OPEN_ARROW"}}},
            ]

        if i in cost_map:
            cid = f"{sid}_cost{i}"
            bx2 = SX + i*(BW+AW)
            reqs += [shape(cid, sid, "ROUND_RECTANGLE", bx2, FY+FH+18, BW, 40),
                     fill(cid, c255(13,7,0), ORANGE, 0.8),
                     txt(cid, f"월 예상\n{cost_map[i]}"),
                     txtstyle(cid, ORANGE, 7.5, bold=True)]


def mk_text_block(sid, body_text, reqs, y_start=83, font_size=8.5, theme='light'):
    """theme: 'light' (흰 배경, 기본값) | 'dark' (검정 배경)"""
    T = THEMES[theme]
    bid = f"{sid}_body"
    reqs += [shape(bid, sid, "TEXT_BOX", 56, y_start, 608, 280),
             txt(bid, body_text),
             txtstyle(bid, T['BODY_COLOR'], font_size)]


def mk_section_divider(slide_oid, num, title, insert_index, reqs):
    """num='01', title='디자인 원칙' — 다크 테마 고정"""
    T = THEMES['dark']
    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})
    bar = f"{slide_oid}_bar"
    reqs += [shape(bar, slide_oid, "RECTANGLE", 0, 0, 720, 3), fill(bar, ORANGE)]
    # 대형 번호 (120pt, 오렌지, 좌측)
    nid = f"{slide_oid}_num"
    reqs += [shape(nid, slide_oid, "TEXT_BOX", 56, 120, 300, 140),
             txt(nid, num),
             {"updateTextStyle": {"objectId": nid,
                 "textRange": {"type": "ALL"},
                 "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                           "fontSize": {"magnitude": 120, "unit": "PT"},
                           "fontFamily": "Proxima Nova", "bold": True},
                 "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
    # 섹션 제목 (36pt, 흰색)
    tid = f"{slide_oid}_ttl"
    reqs += [shape(tid, slide_oid, "TEXT_BOX", 56, 280, 600, 50),
             txt(tid, title),
             {"updateTextStyle": {"objectId": tid,
                 "textRange": {"type": "ALL"},
                 "style": {"foregroundColor": {"opaqueColor": {"rgbColor": T['TITLE_COLOR']}},
                           "fontSize": {"magnitude": 36, "unit": "PT"},
                           "fontFamily": "Noto Sans", "bold": False},
                 "fields": "foregroundColor,fontSize,fontFamily,bold"}}]


def mk_contents(slide_oid, sections, insert_index, reqs):
    """sections = [("01","디자인 원칙"), ("02","소재 규정"), ("03","적용 사례")]"""
    T = THEMES['dark']
    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})
    bar = f"{slide_oid}_bar"
    reqs += [shape(bar, slide_oid, "RECTANGLE", 0, 0, 720, 3), fill(bar, ORANGE)]
    # "CONTENTS" 타이틀
    cid = f"{slide_oid}_ctl"
    reqs += [shape(cid, slide_oid, "TEXT_BOX", 56, 44, 300, 30),
             txt(cid, "CONTENTS"),
             {"updateTextStyle": {"objectId": cid,
                 "textRange": {"type": "ALL"},
                 "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                           "fontSize": {"magnitude": 14, "unit": "PT"},
                           "fontFamily": "Proxima Nova", "bold": True},
                 "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
    Y0 = 120
    for i, (num, title) in enumerate(sections):
        y = Y0 + i * 72
        nid = f"{slide_oid}_n{i}"
        reqs += [shape(nid, slide_oid, "TEXT_BOX", 56, y, 80, 40),
                 txt(nid, num),
                 {"updateTextStyle": {"objectId": nid,
                     "textRange": {"type": "ALL"},
                     "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                               "fontSize": {"magnitude": 28, "unit": "PT"},
                               "fontFamily": "Proxima Nova", "bold": True},
                     "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
        tid = f"{slide_oid}_t{i}"
        reqs += [shape(tid, slide_oid, "TEXT_BOX", 140, y+4, 500, 36),
                 txt(tid, title),
                 {"updateTextStyle": {"objectId": tid,
                     "textRange": {"type": "ALL"},
                     "style": {"foregroundColor": {"opaqueColor": {"rgbColor": T['TITLE_COLOR']}},
                               "fontSize": {"magnitude": 20, "unit": "PT"},
                               "fontFamily": "Noto Sans", "bold": False},
                     "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
        if i < len(sections) - 1:
            lid = f"{slide_oid}_ln{i}"
            reqs += [shape(lid, slide_oid, "RECTANGLE", 56, y+60, 608, 1),
                     fill(lid, T['CARD_BORDER'])]


def mk_quote(slide_oid, quote_text, insert_index, reqs, attribution=""):
    """quote_text='성능이 30% 향상됐다', attribution='2026 Q1 리포트' (선택)"""
    T = THEMES['dark']
    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})
    # 오렌지 악센트 바 (인용 텍스트 위 중앙)
    bid = f"{slide_oid}_qbar"
    reqs += [shape(bid, slide_oid, "RECTANGLE", 335, 140, 50, 3), fill(bid, ORANGE)]
    # 인용 텍스트 (28pt, 중앙)
    qid = f"{slide_oid}_q"
    reqs += [shape(qid, slide_oid, "TEXT_BOX", 80, 160, 560, 80),
             txt(qid, quote_text),
             {"updateTextStyle": {"objectId": qid,
                 "textRange": {"type": "ALL"},
                 "style": {"foregroundColor": {"opaqueColor": {"rgbColor": T['TITLE_COLOR']}},
                           "fontSize": {"magnitude": 28, "unit": "PT"},
                           "fontFamily": "Noto Sans", "bold": True},
                 "fields": "foregroundColor,fontSize,fontFamily,bold"}},
             {"updateParagraphStyle": {"objectId": qid,
                 "textRange": {"type": "ALL"},
                 "style": {"alignment": "CENTER"}, "fields": "alignment"}}]
    if attribution:
        aid = f"{slide_oid}_attr"
        reqs += [shape(aid, slide_oid, "TEXT_BOX", 80, 260, 560, 24),
                 txt(aid, attribution),
                 txtstyle(aid, T['BODY_COLOR'], 10),
                 {"updateParagraphStyle": {"objectId": aid,
                     "textRange": {"type": "ALL"},
                     "style": {"alignment": "CENTER"}, "fields": "alignment"}}]


def mk_split(sid, left, right, reqs, theme='light'):
    """left={'title':'좌측 제목','body':'설명'}, right={...}
    theme: 'light' (기본) | 'dark'"""
    T = THEMES[theme]
    LX, RX = 56, 380
    COL_W = 280
    lt = f"{sid}_lt"
    reqs += [shape(lt, sid, "TEXT_BOX", LX, 83, COL_W, 24),
             txt(lt, left['title']),
             txtstyle(lt, T['TITLE_COLOR'], 14, bold=True)]
    lb = f"{sid}_lb"
    reqs += [shape(lb, sid, "TEXT_BOX", LX, 115, COL_W, 240),
             txt(lb, left['body']),
             txtstyle(lb, T['BODY_COLOR'], 8.5)]
    div = f"{sid}_div"
    reqs += [shape(div, sid, "RECTANGLE", 356, 83, 1, 280),
             fill(div, T['CARD_BORDER'])]
    rt = f"{sid}_rt"
    reqs += [shape(rt, sid, "TEXT_BOX", RX, 83, COL_W, 24),
             txt(rt, right['title']),
             txtstyle(rt, T['TITLE_COLOR'], 14, bold=True)]
    rb = f"{sid}_rb"
    reqs += [shape(rb, sid, "TEXT_BOX", RX, 115, COL_W, 240),
             txt(rb, right['body']),
             txtstyle(rb, T['BODY_COLOR'], 8.5)]


def mk_title_accent(sid, accent_part, rest_part, reqs, theme='light', subtitle="", y=44, font_size=22):
    """
    accent_part: 오렌지로 표시할 앞부분 ("What")
    rest_part:   나머지 텍스트 (" We Can Do")
    subtitle:    제목 아래 작은 설명 텍스트 (선택)
    """
    T = THEMES[theme]
    full = accent_part + rest_part
    hid = f"{sid}_hdr"
    reqs += [shape(hid, sid, "TEXT_BOX", 56, y, 608, font_size * 2),
             txt(hid, full)]
    reqs.append({"updateTextStyle": {"objectId": hid,
        "textRange": {"type": "ALL"},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": T['TITLE_COLOR']}},
                  "fontSize": {"magnitude": font_size, "unit": "PT"},
                  "fontFamily": "Proxima Nova", "bold": True},
        "fields": "foregroundColor,fontSize,fontFamily,bold"}})
    # accent 부분만 오렌지로 덮어쓰기
    reqs.append({"updateTextStyle": {"objectId": hid,
        "textRange": {"type": "FIXED_RANGE",
                      "startIndex": 0, "endIndex": len(accent_part)},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}}},
        "fields": "foregroundColor"}})
    if subtitle:
        subid = f"{sid}_sub"
        sub_y = y + font_size * 2 + 4
        reqs += [shape(subid, sid, "TEXT_BOX", 56, sub_y, 608, 18),
                 txt(subid, subtitle),
                 txtstyle(subid, T['BODY_COLOR'], 8)]


def mk_3col_cards(sid, cards, reqs, theme='light'):
    """
    cards = [
        {"num": "1", "title": "H&B Store Management", "body": "설명 텍스트"},
        {"num": "2", "title": "Marketing & Design",   "body": "설명 텍스트"},
        {"num": "3", "title": "Logistics",             "body": "설명 텍스트"},
    ]
    카드 스타일: 0→light, 1→dark, 2→accent(orange) 고정
    """
    CARD_STYLES = [
        {"bg": c255(245,245,245), "border": c255(229,229,229),
         "title": c255(26,26,26),   "body": c255(74,74,74),
         "badge_bg": ORANGE,        "badge_txt": WHITE},
        {"bg": c255(26,26,26),    "border": c255(26,26,26),
         "title": c255(249,250,251),"body": c255(156,163,175),
         "badge_bg": ORANGE,        "badge_txt": WHITE},
        {"bg": ORANGE,            "border": ORANGE,
         "title": WHITE,           "body": c255(255,220,190),
         "badge_bg": WHITE,         "badge_txt": ORANGE},
    ]
    PAD_X = 36
    CARD_W, CARD_H, GAP = 208, 220, 12
    CARD_Y = 128  # (405 - 70 - 220) / 2 + 70 ≈ 128 → 수직 중앙

    for ci, (card, sty) in enumerate(zip(cards, CARD_STYLES)):
        cx = PAD_X + ci * (CARD_W + GAP)
        cid = f"{sid}_card{ci}"
        reqs += [shape(cid, sid, "ROUND_RECTANGLE", cx, CARD_Y, CARD_W, CARD_H),
                 fill(cid, sty["bg"], sty["border"], 0)]
        # 원형 번호 배지
        bid = f"{sid}_badge{ci}"
        reqs += [shape(bid, sid, "ELLIPSE", cx+16, CARD_Y+16, 20, 20),
                 fill(bid, sty["badge_bg"], sty["badge_bg"], 0),
                 txt(bid, card["num"]),
                 txtstyle(bid, sty["badge_txt"], 8, bold=True),
                 {"updateParagraphStyle": {"objectId": bid,
                     "textRange": {"type": "ALL"},
                     "style": {"alignment": "CENTER"}, "fields": "alignment"}}]
        # 카드 제목
        ttid = f"{sid}_ctitle{ci}"
        reqs += [shape(ttid, sid, "TEXT_BOX", cx+16, CARD_Y+46, CARD_W-32, 40),
                 txt(ttid, card["title"]),
                 txtstyle(ttid, sty["title"], 11, bold=True)]
        # 카드 본문
        bdid = f"{sid}_cbody{ci}"
        reqs += [shape(bdid, sid, "TEXT_BOX", cx+16, CARD_Y+94, CARD_W-32, 112),
                 txt(bdid, card["body"]),
                 txtstyle(bdid, sty["body"], 7.5)]


def mk_toc(slide_oid, items, insert_index, reqs,
           category="", year="",
           title_accent="Table Of", title_rest=" Content",
           description=""):
    """
    items = [{"title": "Introduction", "desc": "설명"}, ...]  최대 6개 (2열 3행)
    category: 상단 왼쪽 오렌지 caps 라벨 (예: "PROJECT MANAGEMENT")
    year:     상단 오른쪽 텍스트 (예: "2026")
    title_accent: 오렌지로 표시할 제목 앞부분
    title_rest:   검정으로 표시할 나머지 제목
    description:  우측 상단 소형 설명 텍스트 (선택)
    """
    T = THEMES['warm']
    LINE_COLOR = c255(200, 196, 190)

    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})

    # 상단 메타 라벨 (좌: 카테고리, 우: 연도)
    if category:
        cid = f"{slide_oid}_cat"
        reqs += [shape(cid, slide_oid, "TEXT_BOX", 36, 20, 300, 12),
                 txt(cid, category.upper()),
                 {"updateTextStyle": {"objectId": cid, "textRange": {"type": "ALL"},
                     "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                               "fontSize": {"magnitude": 7, "unit": "PT"},
                               "fontFamily": "Proxima Nova", "bold": True},
                     "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
    if year:
        yid = f"{slide_oid}_yr"
        reqs += [shape(yid, slide_oid, "TEXT_BOX", 600, 20, 84, 12),
                 txt(yid, str(year)),
                 {"updateTextStyle": {"objectId": yid, "textRange": {"type": "ALL"},
                     "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                               "fontSize": {"magnitude": 7, "unit": "PT"},
                               "fontFamily": "Proxima Nova", "bold": False},
                     "fields": "foregroundColor,fontSize,fontFamily,bold"}},
                 {"updateParagraphStyle": {"objectId": yid,
                     "textRange": {"type": "ALL"},
                     "style": {"alignment": "END"}, "fields": "alignment"}}]

    # 2색 대형 제목
    full_title = title_accent + title_rest
    tid = f"{slide_oid}_ttl"
    reqs += [shape(tid, slide_oid, "TEXT_BOX", 36, 38, 460, 50), txt(tid, full_title)]
    reqs.append({"updateTextStyle": {"objectId": tid, "textRange": {"type": "ALL"},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": T['TITLE_COLOR']}},
                  "fontSize": {"magnitude": 32, "unit": "PT"},
                  "fontFamily": "Proxima Nova", "bold": True},
        "fields": "foregroundColor,fontSize,fontFamily,bold"}})
    reqs.append({"updateTextStyle": {"objectId": tid,
        "textRange": {"type": "FIXED_RANGE", "startIndex": 0, "endIndex": len(title_accent)},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}}},
        "fields": "foregroundColor"}})

    # 우측 설명 텍스트
    if description:
        did = f"{slide_oid}_desc"
        reqs += [shape(did, slide_oid, "TEXT_BOX", 510, 38, 174, 50),
                 txt(did, description),
                 txtstyle(did, T['BODY_COLOR'], 7.5)]

    # 2열 TOC 아이템
    COL1_X, COL2_X = 36, 392
    COL_W = 320
    ITEM_Y0, ITEM_H = 150, 46  # (405-68-138)/2 + 68+82 ≈ 150 → 수직 중앙
    mid = (len(items) + 1) // 2

    for col_idx, (col_items, col_x) in enumerate([(items[:mid], COL1_X), (items[mid:], COL2_X)]):
        for row, item in enumerate(col_items):
            iy = ITEM_Y0 + row * ITEM_H
            # 구분선
            lid = f"{slide_oid}_tl{col_idx}{row}"
            reqs += [shape(lid, slide_oid, "RECTANGLE", col_x, iy, COL_W, 1),
                     fill(lid, LINE_COLOR)]
            # → 화살표
            aid = f"{slide_oid}_arr{col_idx}{row}"
            reqs += [shape(aid, slide_oid, "TEXT_BOX", col_x, iy+8, 18, 14),
                     txt(aid, "→"),
                     {"updateTextStyle": {"objectId": aid, "textRange": {"type": "ALL"},
                         "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}},
                                   "fontSize": {"magnitude": 10, "unit": "PT"},
                                   "fontFamily": "Proxima Nova", "bold": True},
                         "fields": "foregroundColor,fontSize,fontFamily,bold"}}]
            # 섹션 제목
            stid = f"{slide_oid}_st{col_idx}{row}"
            reqs += [shape(stid, slide_oid, "TEXT_BOX", col_x+22, iy+6, 130, 14),
                     txt(stid, item["title"]),
                     txtstyle(stid, T['TITLE_COLOR'], 9, bold=True)]
            # 설명
            sdid = f"{slide_oid}_sd{col_idx}{row}"
            reqs += [shape(sdid, slide_oid, "TEXT_BOX", col_x+22, iy+20, 292, 20),
                     txt(sdid, item.get("desc", "")),
                     txtstyle(sdid, T['BODY_COLOR'], 7)]


def mk_split_cards(sid, text_lines, cards, reqs, theme='light'):
    """
    text_lines: ["고객과 함께 성장하는 기업", "함께 꿈을 이룰 수 있는 기업", ...]
    cards: [{"label": "Professionalism", "style": "accent"},
            {"label": "Honesty",         "style": "dark"},
            {"label": "Responsibility",  "style": "light"}, ...]
    style 값: 'accent'(오렌지) | 'dark'(검정) | 'light'(밝은 회색)
    """
    T = THEMES[theme]
    CARD_STYLES_MAP = {
        'accent': {'bg': ORANGE,          'txt': WHITE},
        'dark':   {'bg': c255(26,26,26),  'txt': c255(249,250,251)},
        'light':  {'bg': c255(245,245,245),'txt': c255(26,26,26)},
    }
    # 좌측 텍스트
    for i, line in enumerate(text_lines):
        lid = f"{sid}_tl{i}"
        reqs += [shape(lid, sid, "TEXT_BOX", 36, 143 + i * 24, 300, 20),
                 txt(lid, line),
                 txtstyle(lid, T['BODY_COLOR'], 9)]

    # 우측 카드 스택
    CARD_X, CARD_W, CARD_H, CARD_GAP = 370, 314, 56, 8
    for i, card in enumerate(cards):
        cy = 143 + i * (CARD_H + CARD_GAP)
        sty = CARD_STYLES_MAP.get(card.get('style', 'light'))
        cid = f"{sid}_sc{i}"
        reqs += [shape(cid, sid, "ROUND_RECTANGLE", CARD_X, cy, CARD_W, CARD_H),
                 fill(cid, sty['bg'], sty['bg'], 0),
                 txt(cid, card['label']),
                 txtstyle(cid, sty['txt'], 11),
                 {"updateParagraphStyle": {"objectId": cid,
                     "textRange": {"type": "ALL"},
                     "style": {"alignment": "CENTER"}, "fields": "alignment"}}]
