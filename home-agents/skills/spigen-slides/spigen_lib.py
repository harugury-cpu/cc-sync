"""
spigen_lib.py — Spigen / CrossCheck Bot Google Slides component library

Design source:
    https://docs.google.com/presentation/d/1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo/edit

Design direction:
    - 720 × 405pt Google Slides 16:9 canvas
    - dark background (#000000)
    - orange accent (#FF6B1A)
    - surface cards (#0E0E0E)
    - native Google Slides shapes/text only

Compatibility:
    Existing public helper/function names are preserved so older execution snippets
    still run, but all visual output now follows the user's current template.
"""


# ─────────────────────────────────────────────────────────────────────
# Tokens / primitives
# ─────────────────────────────────────────────────────────────────────

def pt(v):
    return int(v * 12700)


def _has_korean(text):
    s = str(text or "")
    return any(
        ("\uac00" <= ch <= "\ud7a3")
        or ("\u1100" <= ch <= "\u11ff")
        or ("\u3130" <= ch <= "\u318f")
        for ch in s
    )


def _font_for(text, ff=None):
    """
    Font policy:
      - Korean-containing text -> Noto Sans
      - Everything else        -> Proxima Nova

    Explicit fontFamily still wins unless ff is None / AUTO.
    """
    if ff not in (None, "AUTO"):
        return ff
    return "Noto Sans" if _has_korean(text) else "Proxima Nova"


def c255(r, g, b):
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


BG = {"red": 0, "green": 0, "blue": 0}
SURFACE = c255(14, 14, 14)
SURFACE_HI = c255(22, 22, 22)
BORDER = c255(32, 32, 32)
BORDER_HI = c255(48, 48, 48)
ORANGE = c255(255, 107, 26)
ORANGE_DIM = c255(61, 26, 5)
WHITE = {"red": 1, "green": 1, "blue": 1}
TEXT = c255(240, 240, 240)
TEXT_DIM = c255(170, 170, 170)
TEXT_FAINT = c255(110, 110, 110)
GOOD = c255(156, 227, 125)
BAD = c255(255, 122, 122)
BLACK = c255(0, 0, 0)

W, H, M = 720, 405, 36
CONTENT_TOP = 112
CONTENT_BOTTOM = 381

# 모든 출력은 dark 단일 테마. theme= 인자는 API 호환용으로만 남겨둔다.
THEMES = {
    "dark": {
        "SLIDE_BG": BG,
        "TITLE_COLOR": TEXT,
        "BODY_COLOR": TEXT_DIM,
        "CARD_BG": SURFACE,
        "CARD_BORDER": BORDER,
    },
}


def _same_rgb(a, b, eps=1e-6):
    if not a or not b:
        return False
    return (
        abs(a.get("red", 0) - b.get("red", 0)) < eps
        and abs(a.get("green", 0) - b.get("green", 0)) < eps
        and abs(a.get("blue", 0) - b.get("blue", 0)) < eps
    )


def _normalize_visible_fill(fg, bg):
    """
    Prevent boxes/lines from disappearing into the slide background.
    If both fill and outline match BG, promote them to visible neutral tokens.
    """
    if _same_rgb(fg, BG) and _same_rgb(bg, BG):
        return SURFACE, BORDER
    if _same_rgb(fg, BG) and not _same_rgb(bg, BG):
        return SURFACE, bg
    return fg, bg


def _clamp_rect_to_canvas(x, y, w, h, left=0, top=0, right=W, bottom=H):
    """
    Hard safety rail:
      no shape/text box may extend beyond the slide canvas.

    Returns a clamped rect that always remains visible inside the canvas.
    """
    x = max(left, min(x, right - 1))
    y = max(top, min(y, bottom - 1))
    w = max(1, min(w, right - x))
    h = max(1, min(h, bottom - y))
    return x, y, w, h


def _fit_height_to_content(y, desired_h, min_h=12, bottom=CONTENT_BOTTOM):
    """
    Fit a vertical block into the content area.
    Use before laying out stacks/tables/diagrams that can grow downward.
    """
    return max(min_h, min(desired_h, bottom - y))


def _stack_group_height(item_heights, gap=0):
    if not item_heights:
        return 0
    return sum(item_heights) + gap * max(0, len(item_heights) - 1)


def shape(oid, page, stype, x, y, w, h):
    x, y, w, h = _clamp_rect_to_canvas(x, y, w, h)
    return {
        "createShape": {
            "objectId": oid,
            "shapeType": stype,
            "elementProperties": {
                "pageObjectId": page,
                "size": {
                    "width": {"magnitude": pt(w), "unit": "EMU"},
                    "height": {"magnitude": pt(h), "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1,
                    "scaleY": 1,
                    "translateX": pt(x),
                    "translateY": pt(y),
                    "unit": "EMU",
                },
            },
        }
    }


def line(oid, page, x1, y1, x2, y2, category="STRAIGHT"):
    """
    Native Google Slides line / connector primitive.

    Use for:
        - process arrows
        - branch / fallback connectors
        - module relation lines

    Do not use for:
        - table separators
        - card dividers
        - decorative underlines

    Notes:
        Google Slides may normalize the created element's internal size/transform
        while preserving the visual endpoints. This is expected API behavior.
    """
    w = max(abs(x2 - x1), 0.1)
    h = max(abs(y2 - y1), 0.1)
    return {
        "createLine": {
            "objectId": oid,
            "category": category,
            "elementProperties": {
                "pageObjectId": page,
                "size": {
                    "width": {"magnitude": pt(w), "unit": "EMU"},
                    "height": {"magnitude": pt(h), "unit": "EMU"},
                },
                "transform": {
                    "scaleX": 1 if x2 >= x1 else -1,
                    "scaleY": 1 if y2 >= y1 else -1,
                    "translateX": pt(min(x1, x2)),
                    "translateY": pt(min(y1, y2)),
                    "unit": "EMU",
                },
            },
        }
    }


def linestyle(oid, color=ORANGE, weight=1.0, start_arrow="NONE", end_arrow="NONE", dash_style="SOLID"):
    return {
        "updateLineProperties": {
            "objectId": oid,
            "lineProperties": {
                "lineFill": {"solidFill": {"color": {"rgbColor": color}}},
                "weight": {"magnitude": weight, "unit": "PT"},
                "dashStyle": dash_style,
                "startArrow": start_arrow,
                "endArrow": end_arrow,
            },
            "fields": "lineFill.solidFill.color,weight,dashStyle,startArrow,endArrow",
        }
    }


def connector(reqs, sid, oid, x1, y1, x2, y2, color=ORANGE, weight=1.0,
              start_arrow="NONE", end_arrow="FILL_ARROW", category="STRAIGHT"):
    """
    Semantic relationship / flow line.

    Preferred for:
        - flow direction
        - branch yes/no routes
        - module-to-module relationships

    Avoid for:
        - table grid lines
        - card separators
        - static layout dividers
    """
    reqs += [
        line(oid, sid, x1, y1, x2, y2, category=category),
        linestyle(oid, color=color, weight=weight, start_arrow=start_arrow, end_arrow=end_arrow),
    ]


def fill(oid, fg, bg=None, wt=0.4):
    bg = bg or fg
    fg, bg = _normalize_visible_fill(fg, bg)
    props = {
        "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": fg}}},
    }
    if wt and wt > 0:
        props["outline"] = {
            "outlineFill": {"solidFill": {"color": {"rgbColor": bg}}},
            "weight": {"magnitude": pt(wt), "unit": "EMU"},
        }
    else:
        props["outline"] = {"propertyState": "NOT_RENDERED"}
    return {
        "updateShapeProperties": {
            "objectId": oid,
            "fields": "shapeBackgroundFill,outline",
            "shapeProperties": props,
        }
    }


def clr(oid):
    return {
        "updateShapeProperties": {
            "objectId": oid,
            "fields": "outline,shapeBackgroundFill",
            "shapeProperties": {
                "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
                "outline": {"propertyState": "NOT_RENDERED"},
            },
        }
    }


def txt(oid, text):
    return {"insertText": {"objectId": oid, "insertionIndex": 0, "text": str(text)}}


def paragraph_bullets(oid, preset="BULLET_DISC_CIRCLE_SQUARE"):
    return {
        "createParagraphBullets": {
            "objectId": oid,
            "textRange": {"type": "ALL"},
            "bulletPreset": preset,
        }
    }


def _type_scale(size):
    """
    Remap small / mid typography tiers so the minimum readable size becomes 7pt
    while preserving relative hierarchy.

    Display titles are kept mostly stable; body / caption / label tiers are
    proportionally lifted.
    """
    if size <= 5.5:
        return 7
    if size <= 6:
        return 7.5
    if size <= 6.5:
        return 8
    if size <= 7:
        return 7.5
    if size <= 8:
        return 9.5
    if size <= 8.5:
        return 10
    if size <= 9:
        return 10.5
    if size <= 11:
        return 12.5
    if size <= 13:
        return 14.5
    return size


def txtstyle(oid, color, size, bold=False, ff="Noto Sans"):
    size = _type_scale(size)
    return {
        "updateTextStyle": {
            "objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {
                "foregroundColor": {"opaqueColor": {"rgbColor": color}},
                "fontSize": {"magnitude": size, "unit": "PT"},
                "fontFamily": ff,
                "bold": bold,
            },
            "fields": "foregroundColor,fontSize,fontFamily,bold",
        }
    }


def align(oid, alignment="CENTER"):
    return {
        "updateParagraphStyle": {
            "objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {"alignment": alignment},
            "fields": "alignment",
        }
    }


def bring_to_front(oids):
    if isinstance(oids, str):
        oids = [oids]
    return {
        "updatePageElementsZOrder": {
            "pageElementObjectIds": oids,
            "operation": "BRING_TO_FRONT",
        }
    }


def middle(oid):
    return {
        "updateShapeProperties": {
            "objectId": oid,
            "fields": "contentAlignment",
            "shapeProperties": {"contentAlignment": "MIDDLE"},
        }
    }


def _page_bg(sid, reqs):
    reqs.append({
        "updatePageProperties": {
            "objectId": sid,
            "fields": "pageBackgroundFill",
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {"color": {"rgbColor": BG}}
                }
            },
        }
    })


def _new_slide(sid, insert_index, reqs, layout_id=None):
    layout_ref = {"layoutId": layout_id} if layout_id else {"predefinedLayout": "BLANK"}
    reqs.append({
        "createSlide": {
            "objectId": sid,
            "insertionIndex": insert_index,
            "slideLayoutReference": layout_ref,
        }
    })
    _page_bg(sid, reqs)


def _text(reqs, sid, oid, x, y, w, h, text, color=TEXT, size=8, bold=False,
          ff=None, center=False, valign=False):
    reqs += [
        shape(oid, sid, "TEXT_BOX", x, y, w, h),
        txt(oid, text),
        txtstyle(oid, color, size, bold=bold, ff=_font_for(text, ff)),
        clr(oid),
    ]
    if center:
        reqs.append(align(oid, "CENTER"))
    if valign:
        reqs.append(middle(oid))


def _rect(reqs, sid, oid, x, y, w, h, bg=SURFACE, border=BORDER, wt=0.5):
    reqs += [shape(oid, sid, "RECTANGLE", x, y, w, h), fill(oid, bg, border, wt)]


def _divider(reqs, sid, oid, x, y, w, h=0.5, color=BORDER_HI):
    """Static divider line rendered as a thin rectangle, not a connector."""
    reqs += [shape(oid, sid, "RECTANGLE", x, y, w, h), fill(oid, color, color, 0)]


def _bullet_line(reqs, sid, oid_prefix, x, y, w, text,
                 bullet_color=TEXT_FAINT, text_color=TEXT_DIM,
                 text_size=7, line_h=13, bullet_size=2.5,
                 bullet_gap=8, ff="Noto Sans", bold=False):
    """
    Bullet + text are treated as one logical row.
    The bullet is vertically centered against the first text line area,
    so it never floats too high/low relative to the copy.
    """
    bullet_y = y + max(0, (line_h - bullet_size) / 2)
    reqs += [
        shape(f"{oid_prefix}_dot", sid, "RECTANGLE", x, bullet_y, bullet_size, bullet_size),
        fill(f"{oid_prefix}_dot", bullet_color, bullet_color, 0),
    ]
    _text(
        reqs,
        sid,
        f"{oid_prefix}_text",
        x + bullet_size + bullet_gap,
        y,
        w - bullet_size - bullet_gap,
        line_h,
        text,
        text_color,
        text_size,
        bold,
        ff,
    )


def _bulleted_text_box(reqs, sid, oid, x, y, w, h, items,
                       color=TEXT_DIM, size=7, ff="Noto Sans",
                       bold=False, preset="BULLET_DISC_CIRCLE_SQUARE"):
    """
    Native paragraph bullets inside a single text box.
    Use when bullets are semantically needed and alignment stability matters more
    than custom square-glyph styling.
    """
    text = "\n".join(str(i) for i in items if str(i).strip())
    reqs += [
        shape(oid, sid, "TEXT_BOX", x, y, w, h),
        txt(oid, text),
        paragraph_bullets(oid, preset=preset),
        txtstyle(oid, color, size, bold=bold, ff=ff),
        clr(oid),
    ]


def _header(sid, reqs, eyebrow="", title="", page_no=None, total=None, footer=""):
    if eyebrow:
        _text(reqs, sid, f"{sid}_eyebrow", M, M, 240, 12, eyebrow.upper(),
              ORANGE, 7, True, "AUTO")
    if title:
        _text(reqs, sid, f"{sid}_title", M, 54, W - M * 2, 40, title,
              TEXT, 22, True, "AUTO")
    # Current template direction: no title underline bar, no top page indicator,
    # no bottom footer/year. Keep only eyebrow + title.


def _footer(sid, reqs, text):
    # Footer intentionally disabled for the current clean template.
    return


def _primary_index(items, predicate):
    """Return the single item explicitly allowed to use 100% orange."""
    for i, item in enumerate(items):
        if isinstance(item, dict) and item.get("primary"):
            return i
    for i, item in enumerate(items):
        if predicate(item):
            return i
    return None


def _estimate_lines(text, card_w, chars_per_line_at_100=11):
    """
    Rough line estimator for Korean/English mixed short labels.
    We prefer expanding card height over shrinking font size.
    """
    if not text:
        return 1
    # Normalize by a ~100pt card width baseline.
    capacity = max(6, int(chars_per_line_at_100 * (card_w / 100.0)))
    return max(1, (len(str(text)) + capacity - 1) // capacity)


def _center_group_start(card_y, card_h, group_h, min_pad=8):
    """
    Center a text group vertically when the available padding is tight.
    This encodes the rule:
      "If text area is x, and top/bottom padding is smaller than x,
       keep top/bottom padding visually balanced."
    """
    pad = max(0, (card_h - group_h) / 2)
    if pad < group_h:
        return card_y + max(min_pad, pad)
    return card_y + min_pad


def _top_weighted_group_start(card_y, card_h, group_h, top_pad=14, bottom_bias=10):
    """
    For larger / hero-style cards:
      keep top padding smaller than bottom padding.
    Use when the card should read from the upper area downward.
    """
    max_start = card_y + max(0, card_h - group_h - bottom_bias)
    return min(card_y + top_pad, max_start)


def _face_center(x, y, w, h, side):
    """
    Return the center point of a card face.
    side: left | right | top | bottom
    """
    if side == "left":
        return x, y + h / 2
    if side == "right":
        return x + w, y + h / 2
    if side == "top":
        return x + w / 2, y
    if side == "bottom":
        return x + w / 2, y + h
    return x + w / 2, y + h / 2


def _face_pair_between(src, dst):
    """
    Pick source/destination faces so both endpoints land on face centers.

    src, dst: (x, y, w, h)
    Rule:
      - if horizontal delta dominates, connect left/right face centers
      - if vertical delta dominates, connect top/bottom face centers
    """
    sx, sy, sw, sh = src
    dx, dy, dw, dh = dst
    scx, scy = sx + sw / 2, sy + sh / 2
    dcx, dcy = dx + dw / 2, dy + dh / 2
    vx, vy = dcx - scx, dcy - scy

    if abs(vx) >= abs(vy):
        s_face = "right" if vx >= 0 else "left"
        d_face = "left" if vx >= 0 else "right"
    else:
        s_face = "bottom" if vy >= 0 else "top"
        d_face = "top" if vy >= 0 else "bottom"
    return _face_center(sx, sy, sw, sh, s_face), _face_center(dx, dy, dw, dh, d_face)


def connect_boxes(reqs, sid, oid, src, dst, color=ORANGE, weight=1.0,
                  start_arrow="NONE", end_arrow="FILL_ARROW", category="STRAIGHT"):
    (x1, y1), (x2, y2) = _face_pair_between(src, dst)
    connector(
        reqs, sid, oid,
        x1, y1, x2, y2,
        color=color, weight=weight,
        start_arrow=start_arrow, end_arrow=end_arrow, category=category,
    )


def orth_connector(reqs, sid, oid, x1, y1, x2, y2, color=ORANGE, weight=1.0,
                   lead=28, start_arrow="NONE", end_arrow="FILL_ARROW"):
    """
    Manual orthogonal connector composed from straight line segments.

    Use when Google Slides native BENT connectors visually detach from the
    exact face-center start/end points.
    """
    if abs(y2 - y1) < 0.5:
        connector(reqs, sid, oid, x1, y1, x2, y2,
                  color=color, weight=weight,
                  start_arrow=start_arrow, end_arrow=end_arrow,
                  category="STRAIGHT")
        return

    if x2 >= x1:
        elbow_x = min(x2 - 12, x1 + lead)
    else:
        elbow_x = max(x2 + 12, x1 - lead)

    connector(reqs, sid, f"{oid}_h1", x1, y1, elbow_x, y1,
              color=color, weight=weight,
              start_arrow=start_arrow, end_arrow="NONE",
              category="STRAIGHT")
    connector(reqs, sid, f"{oid}_v", elbow_x, y1, elbow_x, y2,
              color=color, weight=weight,
              start_arrow="NONE", end_arrow="NONE",
              category="STRAIGHT")
    connector(reqs, sid, f"{oid}_h2", elbow_x, y2, x2, y2,
              color=color, weight=weight,
              start_arrow="NONE", end_arrow=end_arrow,
              category="STRAIGHT")


# ─────────────────────────────────────────────────────────────────────
# Public components — current template direction
# ─────────────────────────────────────────────────────────────────────

def slide_base(slide_oid, title_text, insert_index, reqs, theme="dark",
               page_label="", page_no=None, total=None, footer=""):
    _new_slide(slide_oid, insert_index, reqs)
    _header(
        slide_oid,
        reqs,
        eyebrow=page_label or "",
        title=title_text,
        page_no=page_no,
        total=total,
        footer=footer or title_text,
    )


def mk_section_divider(slide_oid, num, title, insert_index, reqs):
    _new_slide(slide_oid, insert_index, reqs)
    _text(reqs, slide_oid, f"{slide_oid}_num", 51, 103, 120, 82, num,
          ORANGE, 100, True, "Proxima Nova")
    reqs += [shape(f"{slide_oid}_vline", slide_oid, "RECTANGLE", 154, 121, 0.7, 80),
             fill(f"{slide_oid}_vline", BORDER_HI, BORDER_HI, 0)]
    _text(reqs, slide_oid, f"{slide_oid}_label", 172, 163, 100, 12, "Section",
          TEXT_FAINT, 11.5, False, "Proxima Nova")
    _text(reqs, slide_oid, f"{slide_oid}_title", 165, 174, 380, 64, title,
          TEXT, 28, True, "Noto Sans")
    _footer(slide_oid, reqs, "Section Divider")


def mk_quote(slide_oid, quote_text, insert_index, reqs, attribution=""):
    _new_slide(slide_oid, insert_index, reqs)
    _text(reqs, slide_oid, f"{slide_oid}_quote_mark", 80, 112, 80, 60, "“",
          ORANGE, 80, True, "Proxima Nova")
    _text(reqs, slide_oid, f"{slide_oid}_quote", 80, 155, 560, 76, quote_text,
          TEXT, 24, True, "Noto Sans", center=True)
    if attribution:
        reqs += [shape(f"{slide_oid}_qbar", slide_oid, "RECTANGLE", 250, 259, 2, 20),
                 fill(f"{slide_oid}_qbar", ORANGE, ORANGE, 0)]
        _text(reqs, slide_oid, f"{slide_oid}_attr", 264, 250, 300, 24, attribution,
              TEXT_DIM, 10, False, "Noto Sans")
    _footer(slide_oid, reqs, "Quote · Callout")


def mk_contents(slide_oid, sections, insert_index, reqs):
    _new_slide(slide_oid, insert_index, reqs)
    _header(slide_oid, reqs, eyebrow="Contents", title="목차", footer="Contents")
    y0 = 132
    for i, sec in enumerate(sections[:5]):
        if isinstance(sec, dict):
            num = sec.get("num", f"{i+1:02d}")
            title = sec.get("title", "")
            desc = sec.get("desc", "")
        else:
            num, title = sec[0], sec[1]
            desc = sec[2] if len(sec) > 2 else ""
        y = y0 + i * 46
        reqs += [shape(f"{slide_oid}_line{i}", slide_oid, "RECTANGLE", M, y - 8, W - M * 2, 0.5),
                 fill(f"{slide_oid}_line{i}", BORDER, BORDER, 0)]
        _text(reqs, slide_oid, f"{slide_oid}_num{i}", M, y, 32, 18, num,
              ORANGE, 13, True, "Proxima Nova")
        _text(reqs, slide_oid, f"{slide_oid}_ttl{i}", M + 50, y, 220, 18, title,
              TEXT, 12, True, "Noto Sans")
        if desc:
            _text(reqs, slide_oid, f"{slide_oid}_desc{i}", M + 280, y + 1, 360, 16, desc,
                  TEXT_DIM, 8, False, "Noto Sans")


def mk_3col(sid, cols, reqs, theme="dark", align_mode="top_weighted"):
    """Template-style 3-column card grid."""
    card_w, gap, x0, y0 = 206, 12, M, 128
    visible_cols = cols[:3]
    primary = _primary_index(
        visible_cols,
        lambda c: isinstance(c, dict) and (
            c.get("role") in ("conclusion", "summary")
            or c.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for i, col in enumerate(visible_cols):
        x = x0 + i * (card_w + gap)
        marked = col.get("primary") or col.get("hot") or col.get("accent")
        hot = i == primary
        dim_hot = marked and not hot
        _rect(reqs, sid, f"{sid}_col{i}", x, y0, card_w, 190,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.5)
        label = col.get("label", f"0{i+1}")
        title = col.get("title", label)
        items = col.get("items", [])
        label_h = 12
        title_h = 28
        item_h = 12
        label_gap = 11
        title_gap = 12
        body_gap = 4
        outer_pad = 16
        group_h = label_h + label_gap + title_h
        if items:
            group_h += title_gap + item_h * min(5, len(items)) + body_gap * max(0, min(5, len(items)) - 1)
        if align_mode == "balanced":
            start_y = _center_group_start(y0, 190, group_h, min_pad=outer_pad)
        else:
            start_y = _top_weighted_group_start(y0, 190, group_h, top_pad=20, bottom_bias=16)
        cursor_y = start_y
        _text(reqs, sid, f"{sid}_cl{i}", x + 18, cursor_y, card_w - 36, label_h,
              str(label).upper(), BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), 7, True, "Proxima Nova", valign=True)
        cursor_y += label_h + label_gap
        _text(reqs, sid, f"{sid}_ct{i}", x + 18, cursor_y, card_w - 36, title_h,
              title, BLACK if hot else TEXT, 13, True, "Noto Sans", valign=True)
        cursor_y += title_h + title_gap
        if items:
            line_y = cursor_y
            for j, item in enumerate(items[:5]):
                _text(
                    reqs, sid, f"{sid}_items{i}_{j}",
                    x + 18, line_y, card_w - 36, item_h, item,
                    BLACK if hot else TEXT_DIM,
                    7, False, "Noto Sans", valign=True
                )
                line_y += item_h + body_gap


def mk_3col_cards(sid, cards, reqs, theme="dark"):
    normalized = []
    for i, c in enumerate(cards[:3]):
        normalized.append({
            "label": c.get("num", c.get("label", f"0{i+1}")),
            "title": c.get("title", c.get("label", "")),
            "items": (c["body"] if isinstance(c.get("body"), list) else ([c["body"]] if c.get("body") else c.get("items", []))),
            "hot": c.get("hot") or c.get("accent") or c.get("style") == "accent",
        })
    mk_3col(sid, normalized, reqs, theme=theme)


def mk_rule_grid(sid, cards, reqs, x=M, y=CONTENT_TOP, w=None, cols=2, gap_x=12, gap_y=12, card_h=96):
    """
    Equal-ratio rule/guide cards.

    Use when the page should remain simple:
      - repeated grid cards are okay
      - mixed 3-up + 1-wide patterns are not

    This helper applies:
      - equal card ratios
      - centered text-group padding in tight cards
      - bullet/text row alignment
    """
    visible = cards[: max(1, cols * 2)]
    if not visible:
        return
    w = w or (W - M * 2)
    rows = (len(visible) + cols - 1) // cols
    label_gap = 8
    title_gap = 10
    body_gap = 4
    outer_pad = 16
    max_group_h = 0
    for card in visible:
        label = card.get("label", "")
        title = card.get("title", "")
        lines = card.get("lines", [])[:3]
        label_h = 10 if label else 0
        title_h = 18 if title else 0
        line_h = 10
        group_h = 0
        if label:
            group_h += label_h
        if title:
            if group_h:
                group_h += label_gap
            group_h += title_h
        if lines:
            if group_h:
                group_h += title_gap
            group_h += line_h * len(lines) + body_gap * max(0, len(lines) - 1)
        max_group_h = max(max_group_h, group_h)
    # Keep top/bottom padding larger than inner gaps.
    card_h = max(card_h, max_group_h + outer_pad * 2)
    card_w = (w - gap_x * (cols - 1)) / cols
    total_h = rows * card_h + gap_y * (rows - 1)
    if y + total_h > CONTENT_BOTTOM:
        fitted = max(72, (CONTENT_BOTTOM - y - gap_y * max(0, rows - 1)) / rows)
        card_h = max(fitted, max_group_h + outer_pad * 2)
    for i, card in enumerate(visible):
        row = i // cols
        col = i % cols
        xx = x + col * (card_w + gap_x)
        yy = y + row * (card_h + gap_y)
        marked = bool(card.get("primary") or card.get("accent") or card.get("hot"))
        fill_color = ORANGE if card.get("primary") else (ORANGE_DIM if card.get("accent_bg") else SURFACE)
        border_color = ORANGE if marked or card.get("accent_bg") else BORDER
        _rect(reqs, sid, f"{sid}_rulegrid_box_{i}", xx, yy, card_w, card_h, fill_color, border_color, 0.5)

        label = card.get("label", "").upper()
        title = card.get("title", "")
        lines = card.get("lines", [])[:3]

        label_h = 10 if label else 0
        title_h = 18 if title else 0
        bullet_h = 10
        parts = ([label_h] if label else []) + ([title_h] if title else []) + ([bullet_h] * len(lines))
        group_h = _stack_group_height(parts, gap=8)
        start_y = _center_group_start(yy, card_h, group_h, min_pad=outer_pad)

        cursor_y = start_y
        if label:
            _text(
                reqs, sid, f"{sid}_rulegrid_label_{i}",
                xx + 16, cursor_y, card_w - 32, label_h, label,
                ORANGE if marked or card.get("accent_bg") else TEXT_FAINT,
                7, True, "Proxima Nova", valign=True
            )
            cursor_y += label_h + label_gap

        if title:
            _text(
                reqs, sid, f"{sid}_rulegrid_title_{i}",
                xx + 16, cursor_y, card_w - 32, title_h, title,
                BLACK if card.get("primary") else TEXT,
                11, True, "Noto Sans", valign=True
            )
            cursor_y += title_h + title_gap

        for j, line in enumerate(lines):
            _text(
                reqs, sid, f"{sid}_rulegrid_line_{i}_{j}",
                xx + 16, cursor_y, card_w - 32, bullet_h, line,
                BLACK if card.get("primary") else TEXT_DIM,
                7, False, "Noto Sans", valign=True
            )
            cursor_y += bullet_h + body_gap


def mk_flow(sid, steps, cost_map=None, reqs=None, theme="dark"):
    """Horizontal process flow. Compatible with old tuple input and new dict input."""
    if reqs is None:
        # Old signature was mk_flow(sid, steps, cost_map, reqs, theme)
        raise ValueError("reqs is required")
    cost_map = cost_map or {}
    visible_steps = steps[:6]
    n = len(visible_steps)
    gap = 12 if n <= 4 else 8
    x0, y0 = 54, 132
    total_w = 612
    cw = (total_w - gap * max(0, n - 1)) / max(1, n)
    ch = 96
    def _is_marked(step):
        if isinstance(step, dict):
            return (
                step.get("role") in ("conclusion", "summary")
                or step.get("style") in ("primary", "conclusion", "summary")
            )
        return False
    primary = _primary_index(visible_steps, _is_marked)
    for i, step in enumerate(visible_steps):
        if isinstance(step, dict):
            num = step.get("num", f"{i+1:02d}")
            name = step.get("name", step.get("title", ""))
            svc = step.get("service", step.get("infra", ""))
            desc = step.get("desc", step.get("detail", ""))
            cost = step.get("cost", cost_map.get(i, ""))
            paid = step.get("paid", step.get("hot", bool(cost and cost != "무료")))
            marked = step.get("primary") or step.get("hot") or step.get("accent") or paid
        else:
            raw_step, name, svc, paid = step[:4]
            num = str(raw_step).replace("STEP", "").strip() or f"{i+1:02d}"
            desc = ""
            cost = cost_map.get(i, "")
            marked = paid
        is_primary = i == primary
        dim_hot = marked and not is_primary
        x = x0 + i * (cw + gap)
        _rect(reqs, sid, f"{sid}_step{i}", x, y0, cw, ch,
              ORANGE if is_primary else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.5)
        _text(reqs, sid, f"{sid}_sn{i}", x + 8, y0 + 8, cw - 16, 9,
              f"STEP {num}", BLACK if is_primary else (ORANGE if dim_hot else TEXT_FAINT), 5, False, "Proxima Nova")
        _text(reqs, sid, f"{sid}_st{i}", x + 8, y0 + 18, cw - 16, 13,
              name, BLACK if is_primary else TEXT, 8, True, "Noto Sans")
        _text(reqs, sid, f"{sid}_sv{i}", x + 8, y0 + 31, cw - 16, 10,
              svc, BLACK if is_primary else TEXT_DIM, 5, False, "Noto Sans")
        if desc:
            _text(reqs, sid, f"{sid}_sd{i}", x + 8, y0 + 42, cw - 16, 17,
                  desc, BLACK if is_primary else TEXT_DIM, 5, False, "Noto Sans")
        reqs += [shape(f"{sid}_sep{i}", sid, "RECTANGLE", x + 8, y0 + 59, cw - 16, 0.5),
                 fill(f"{sid}_sep{i}", BLACK if is_primary else (ORANGE if dim_hot else BORDER_HI), BLACK if is_primary else (ORANGE if dim_hot else BORDER_HI), 0)]
        if cost:
            _text(reqs, sid, f"{sid}_costl{i}", x + 8, y0 + 63, cw - 16, 8,
                  "월 예상 비용", BLACK if is_primary else (ORANGE if dim_hot else TEXT_FAINT), 4, False, "Noto Sans")
            _text(reqs, sid, f"{sid}_cost{i}", x + 8, y0 + 71, cw - 16, 10,
                  cost, BLACK if is_primary else TEXT, 7, True, "Noto Sans")
        if i < min(len(steps), 6) - 1:
            _text(reqs, sid, f"{sid}_arr{i}", x + cw - 5, y0 + 39, 10, 8,
                  "›", ORANGE, 5, False, "Proxima Nova", center=True)


def mk_flow_focus(sid, steps, reqs, x=54, y=136, w=612, cols=3):
    """
    Larger, template-like flow layout for pages where process itself is the main message.

    Compared with mk_flow():
        - bigger cards
        - single-row horizontal flow
        - larger titles/body for proposal / overview decks
        - no lower cost/table area
    """
    visible_steps = steps[:6]
    if not visible_steps:
        return
    cols = len(visible_steps)
    gap_x = 8
    card_w = (w - gap_x * (cols - 1)) / cols
    max_group_h = 0
    for step in visible_steps:
        if isinstance(step, dict):
            name = step.get("name", step.get("title", ""))
            svc = step.get("service", step.get("infra", ""))
        else:
            name = step[1] if len(step) > 1 else ""
            svc = step[2] if len(step) > 2 else ""
        title_lines = _estimate_lines(name, card_w - 24, chars_per_line_at_100=8)
        svc_lines = _estimate_lines(svc, card_w - 24, chars_per_line_at_100=10) if svc else 0
        num_h = 18
        title_h = 16 * title_lines
        svc_h = 14 * svc_lines if svc else 0
        group_h = num_h + 8 + title_h + (8 + svc_h if svc else 0)
        max_group_h = max(max_group_h, group_h)
    card_h = max(96, max_group_h + 28)
    card_h = _fit_height_to_content(y, card_h, min_h=72)
    primary = _primary_index(
        visible_steps,
        lambda s: isinstance(s, dict) and (
            s.get("role") in ("conclusion", "summary")
            or s.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for i, step in enumerate(visible_steps):
        xx = x + i * (card_w + gap_x)
        yy = y
        if isinstance(step, dict):
            num = step.get("num", f"{i+1:02d}")
            name = step.get("name", step.get("title", ""))
            svc = step.get("service", step.get("infra", ""))
            marked = step.get("primary") or step.get("accent") or step.get("hot")
        else:
            raw_step, name, svc = step[:3]
            num = str(raw_step).replace("STEP", "").strip() or f"{i+1:02d}"
            marked = False
        hot = i == primary
        dim_hot = marked and not hot
        title_size = 10
        title_lines = _estimate_lines(name, card_w - 24, chars_per_line_at_100=8)
        title_h = 16 * title_lines
        svc_lines = _estimate_lines(svc, card_w - 24, chars_per_line_at_100=10) if svc else 0
        svc_h = 14 * svc_lines if svc else 0
        num_h = 18
        heights = [num_h, title_h] + ([svc_h] if svc else [])
        group_h = _stack_group_height(heights, gap=8)
        start_y = _top_weighted_group_start(yy, card_h, group_h, top_pad=14, bottom_bias=14)
        num_y = start_y
        title_y = num_y + num_h + 8
        svc_y = title_y + title_h + 8
        _rect(reqs, sid, f"{sid}_focus_bg{i}", xx, yy, card_w, card_h,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.5)
        _text(reqs, sid, f"{sid}_focus_num{i}", xx + 12, num_y, 56, num_h,
              f"STEP {num}", BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT),
              7, True, "Proxima Nova", valign=True)
        _text(reqs, sid, f"{sid}_focus_title{i}", xx + 12, title_y, card_w - 24, title_h,
              name, BLACK if hot else TEXT, title_size, True, "Noto Sans", valign=True)
        if svc:
            _text(reqs, sid, f"{sid}_focus_svc{i}", xx + 12, svc_y, card_w - 24, svc_h,
                  svc, BLACK if hot else TEXT_DIM, 7, False, "Noto Sans", valign=True)
        if i < len(visible_steps) - 1:
            nx = x + (i + 1) * (card_w + gap_x)
            x1, y1 = _face_center(xx, yy, card_w, card_h, "right")
            x2, y2 = _face_center(nx, yy, card_w, card_h, "left")
            connector(
                reqs, sid, f"{sid}_focus_arrow{i}",
                x1, y1, x2, y2,
                color=ORANGE if (marked or i + 1 == primary) else BORDER_HI,
                weight=1.0,
                start_arrow="NONE",
                end_arrow="FILL_ARROW",
            )


def mk_text_block(sid, body_text, reqs, y_start=128, font_size=10, theme="dark"):
    box_h = _fit_height_to_content(y_start, 170, min_h=72)
    _rect(reqs, sid, f"{sid}_bodybox", M, y_start, W - M * 2, box_h, SURFACE, BORDER, 0.5)
    _text(reqs, sid, f"{sid}_body", M + 20, y_start + 22, W - M * 2 - 40, max(18, box_h - 44),
          body_text, TEXT_DIM, font_size, False, "Noto Sans")


def mk_split(sid, left, right, reqs, theme="dark"):
    _rect(reqs, sid, f"{sid}_leftbox", M, 128, 313, 170, SURFACE, BORDER, 0.5)
    _rect(reqs, sid, f"{sid}_rightbox", 371, 128, 313, 170, ORANGE_DIM, ORANGE, 0.5)
    _text(reqs, sid, f"{sid}_lt", M + 18, 150, 280, 24, left.get("title", ""),
          TEXT, 14, True)
    _text(reqs, sid, f"{sid}_lb", M + 18, 184, 280, 80, left.get("body", ""),
          TEXT_DIM, 8, False)
    _text(reqs, sid, f"{sid}_rt", 389, 150, 280, 24, right.get("title", ""),
          TEXT, 14, True)
    _text(reqs, sid, f"{sid}_rb", 389, 184, 280, 80, right.get("body", ""),
          TEXT_DIM, 8, False)
    _text(reqs, sid, f"{sid}_arrow", 352, 198, 16, 16, "›", ORANGE, 11, True, center=True)


def mk_title_accent(sid, accent_part, rest_part, reqs, theme="dark",
                    subtitle="", y=54, font_size=22):
    full = accent_part + rest_part
    oid = f"{sid}_title_accent"
    reqs += [shape(oid, sid, "TEXT_BOX", M, y, W - M * 2, 42), txt(oid, full)]
    reqs.append(txtstyle(oid, TEXT, font_size, bold=True, ff="Noto Sans"))
    reqs.append({
        "updateTextStyle": {
            "objectId": oid,
            "textRange": {"type": "FIXED_RANGE", "startIndex": 0, "endIndex": len(accent_part)},
            "style": {"foregroundColor": {"opaqueColor": {"rgbColor": ORANGE}}},
            "fields": "foregroundColor",
        }
    })
    reqs.append(clr(oid))
    if subtitle:
        _text(reqs, sid, f"{sid}_title_sub", M, y + 45, W - M * 2, 18,
              subtitle, TEXT_DIM, 8, False)


def mk_toc(slide_oid, items, insert_index, reqs, category="", year="",
           title_accent="Table Of", title_rest=" Content", description=""):
    _new_slide(slide_oid, insert_index, reqs)
    if category:
        _text(reqs, slide_oid, f"{slide_oid}_cat", M, 30, 240, 10,
              category.upper(), ORANGE, 7, True, "Proxima Nova")
    if year:
        _text(reqs, slide_oid, f"{slide_oid}_year", W - M - 60, 30, 60, 10,
              str(year), TEXT_FAINT, 7, False, "Proxima Nova")
    mk_title_accent(slide_oid, title_accent, title_rest, reqs, y=54, font_size=24)
    if description:
        _text(reqs, slide_oid, f"{slide_oid}_desc", M, 92, W - M * 2, 16,
              description, TEXT_DIM, 7, False)
    y0 = 140
    for i, item in enumerate(items[:6]):
        col = 0 if i < 3 else 1
        row = i if i < 3 else i - 3
        x = M + col * 335
        y = y0 + row * 56
        title = item.get("title", "") if isinstance(item, dict) else item[0]
        desc = item.get("desc", "") if isinstance(item, dict) else (item[1] if len(item) > 1 else "")
        reqs += [shape(f"{slide_oid}_ln{i}", slide_oid, "RECTANGLE", x, y - 8, 300, 0.5),
                 fill(f"{slide_oid}_ln{i}", BORDER, BORDER, 0)]
        _text(reqs, slide_oid, f"{slide_oid}_arr{i}", x, y, 16, 14, "→",
              ORANGE, 9, True, "Proxima Nova")
        _text(reqs, slide_oid, f"{slide_oid}_it{i}", x + 24, y, 130, 14, title,
              TEXT, 9, True)
        _text(reqs, slide_oid, f"{slide_oid}_id{i}", x + 24, y + 16, 260, 20, desc,
              TEXT_DIM, 7, False)
    _footer(slide_oid, reqs, "Table Of Content")


def mk_split_cards(sid, text_lines, cards, reqs, theme="dark"):
    x0, y0 = M, 140
    for i, line in enumerate(text_lines[:5]):
        _text(reqs, sid, f"{sid}_tl{i}", x0, y0 + i * 24, 260, 18,
              line, TEXT_DIM, 9, False)
    card_x, card_w, card_h, gap = 370, 314, 44, 8
    visible_cards = cards[:4]
    primary = _primary_index(
        visible_cards,
        lambda c: isinstance(c, dict) and (
            c.get("role") in ("conclusion", "summary")
            or c.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for i, card in enumerate(visible_cards):
        y = y0 + i * (card_h + gap)
        style = card.get("style", "")
        marked = card.get("primary") or style == "accent" or card.get("hot") or card.get("accent")
        hot = i == primary
        dim_hot = marked and not hot
        _rect(reqs, sid, f"{sid}_sc{i}", card_x, y, card_w, card_h,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.5)
        _text(reqs, sid, f"{sid}_sct{i}", card_x + 18, y + 13, card_w - 36, 18,
              card.get("label", card.get("title", "")), BLACK if hot else TEXT, 10, True, center=True)


# Convenience aliases for template-like cases.
def mk_summary(slide_oid, message, insert_index, reqs, attribution=""):
    mk_quote(slide_oid, message, insert_index, reqs, attribution)


def mk_feature_grid(sid, cards, reqs, theme="dark"):
    mk_3col_cards(sid, cards, reqs, theme)


def mk_kpi_dashboard(sid, kpis, reqs, y=128):
    """
    kpis = [
        {"label": "처리 건수", "value": "1,248", "sub": "월 누적", "hot": True},
        ...
    ]
    """
    count = min(len(kpis), 4)
    if count <= 0:
        return
    gap = 12
    card_w = (W - M * 2 - gap * (count - 1)) / count
    card_h = _fit_height_to_content(y, 128, min_h=84)
    visible_kpis = kpis[:count]
    primary = _primary_index(
        visible_kpis,
        lambda k: isinstance(k, dict) and (
            k.get("role") in ("conclusion", "summary")
            or k.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for i, k in enumerate(visible_kpis):
        x = M + i * (card_w + gap)
        marked = k.get("primary") or k.get("hot") or k.get("accent")
        hot = i == primary
        dim_hot = marked and not hot
        _rect(reqs, sid, f"{sid}_kpi_bg{i}", x, y, card_w, card_h,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.5)
        _text(reqs, sid, f"{sid}_kpi_label{i}", x + 14, y + 18, card_w - 28, 12,
              k.get("label", ""), BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), 7, True, "AUTO")
        _text(reqs, sid, f"{sid}_kpi_value{i}", x + 14, y + 46, card_w - 28, 40,
              k.get("value", ""), BLACK if hot else TEXT, 26, True, "Proxima Nova")
        _text(reqs, sid, f"{sid}_kpi_sub{i}", x + 14, y + 91, card_w - 28, 20,
              k.get("sub", ""), BLACK if hot else TEXT_DIM, 7, False, "AUTO")


def mk_bar_chart(sid, bars, reqs, x=M, y=144, w=420, h=150,
                 title="성과 추이", value_suffix="", max_value=None, key="chart"):
    """
    bars = [
        {"label": "1월", "value": 72, "accent": False},
        {"label": "2월", "value": 88, "accent": True},
    ]
    """
    if not bars:
        return
    prefix = f"{sid}_{key}"
    max_v = max_value or max(float(b.get("value", 0)) for b in bars) or 1
    _text(reqs, sid, f"{prefix}_title", x, y - 28, w, 16,
          title, TEXT, 9, True, "Noto Sans")
    reqs += [shape(f"{prefix}_axis", sid, "RECTANGLE", x, y + h, w, 0.5),
             fill(f"{prefix}_axis", BORDER_HI, BORDER_HI, 0)]
    gap = 10
    bw = (w - gap * (len(bars) - 1)) / len(bars)
    for i, b in enumerate(bars):
        val = float(b.get("value", 0))
        bh = max(2, h * val / max_v)
        bx = x + i * (bw + gap)
        by = y + h - bh
        hot = b.get("accent", i == len(bars) - 1)
        _rect(reqs, sid, f"{prefix}_bar{i}", bx, by, bw, bh,
              ORANGE if hot else SURFACE_HI, ORANGE if hot else BORDER, 0.3)
        _text(reqs, sid, f"{prefix}_val{i}", bx - 6, by - 17, bw + 12, 12,
              f"{int(val) if val.is_integer() else val:g}{value_suffix}",
              ORANGE if hot else TEXT_DIM, 7, True, "Proxima Nova", center=True)
        _text(reqs, sid, f"{prefix}_lab{i}", bx - 6, y + h + 8, bw + 12, 12,
              b.get("label", ""), TEXT_FAINT, 7, False, "Noto Sans", center=True)


def mk_report_table(sid, rows, reqs, x=M, y=138, w=648):
    """
    rows = [
        {"metric": "처리 시간", "before": "수분~수십분", "after": "약 100초", "impact": "–90%", "hot": True},
        ...
    ]
    """
    col = [0.23, 0.27, 0.28, 0.22]
    xs = [x]
    for ratio in col[:-1]:
        xs.append(xs[-1] + w * ratio)
    ws = [w * r for r in col]
    header_h, row_h = 24, 36
    headers = ["지표", "도입 전", "도입 후", "성과"]
    max_rows = max(1, int((_fit_height_to_content(y, CONTENT_BOTTOM - y, min_h=60) - header_h) // row_h))
    rows = rows[:max_rows]
    _rect(reqs, sid, f"{sid}_tbl_head_bg", x, y, w, header_h, SURFACE_HI, BORDER_HI, 0.5)
    for i, head in enumerate(headers):
        _text(reqs, sid, f"{sid}_tbl_head{i}", xs[i] + 10, y + 7, ws[i] - 20, 10,
              head, TEXT_FAINT, 7, True, "Noto Sans", valign=True)
    visible_rows = rows[:5]
    primary = _primary_index(
        visible_rows,
        lambda row: isinstance(row, dict) and (
            row.get("role") in ("conclusion", "summary")
            or row.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for r, row in enumerate(visible_rows):
        ry = y + header_h + r * row_h
        marked = row.get("primary") or row.get("hot") or row.get("accent")
        hot = r == primary
        dim_hot = marked and not hot
        _rect(reqs, sid, f"{sid}_tbl_rowbg{r}", x, ry, w, row_h,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.4)
        vals = [row.get("metric", ""), row.get("before", ""), row.get("after", ""), row.get("impact", "")]
        for c, val in enumerate(vals):
            color = BLACK if hot else (TEXT if c in (0, 2, 3) else TEXT_DIM)
            bold = c in (0, 3)
            _text(reqs, sid, f"{sid}_tbl_{r}_{c}", xs[c] + 10, ry + 11, ws[c] - 20, 13,
                  val, color, 7, bold, "Noto Sans", valign=True)


def mk_callout_message(sid, message, reqs, sub="", x=84, y=148, w=552, h=126):
    """Large emphasized message block for conclusion / executive summary."""
    _rect(reqs, sid, f"{sid}_callout_bg", x, y, w, h, ORANGE_DIM, ORANGE, 0.6)
    bar_y = y + min(28, max(10, h * 0.22))
    bar_h = max(2, h - (bar_y - y) * 2)
    reqs += [shape(f"{sid}_callout_bar", sid, "RECTANGLE", x + 28, bar_y, 3, bar_h),
             fill(f"{sid}_callout_bar", ORANGE, ORANGE, 0)]
    has_sub = bool(sub)
    msg_y = y + min(30, max(10, h * 0.24))
    if has_sub:
        msg_h = 50 if h >= 88 else max(18, h * 0.45)
        msg_size = 20 if h >= 88 else (12 if h >= 60 else 9.5)
    else:
        msg_h = max(22, h - (msg_y - y) - 10)
        msg_size = 20 if h >= 110 else (15 if h >= 70 else 12)
    _text(reqs, sid, f"{sid}_callout_msg", x + 48, msg_y, w - 80, msg_h,
          message, TEXT, msg_size, True, "Noto Sans")
    if has_sub:
        sub_y = y + h - 28 if h >= 70 else y + h - 18
        sub_size = 8 if h >= 70 else 6
        _text(reqs, sid, f"{sid}_callout_sub", x + 48, sub_y, w - 80, 20,
              sub, TEXT_DIM, sub_size, False, "Noto Sans")


def mk_conclusion_detail(sid, conclusion, details, reqs, eyebrow="SUMMARY", title="요약",
                         accent_line=True):
    """
    Closing summary layout:
        left  = one large conclusion
        right = small supporting details

    Use when the final slide should read as "결론 → 세부 근거".
    100% orange card is intentionally not used here; orange is limited to
    keywords, small numbers, and a short accent line.
    """
    if eyebrow:
        _text(reqs, sid, f"{sid}_summary_eyebrow", M, 28, 120, 10,
              eyebrow.upper(), ORANGE, 7, True, "Proxima Nova")
    _text(reqs, sid, f"{sid}_summary_title", M, 50, 180, 28,
          title, TEXT, 22, True, "Noto Sans")
    if accent_line:
        reqs += [shape(f"{sid}_summary_line", sid, "RECTANGLE", M, 95, 22, 1.2),
                 fill(f"{sid}_summary_line", ORANGE, ORANGE, 0.1)]

    # Left conclusion block.
    lines = conclusion if isinstance(conclusion, (list, tuple)) else [conclusion]
    base_y = 130
    for i, line in enumerate(lines[:3]):
        color = ORANGE if i == len(lines[:3]) - 1 else TEXT
        _text(reqs, sid, f"{sid}_summary_conclusion_{i}", M, base_y + i * 28, 280, 28,
              line, color, 18, True, "Noto Sans")

    # Right supporting details.
    box_x, box_y, box_w, box_h, gap = 390, 128, 276, 46, 10
    max_detail_h = _fit_height_to_content(box_y, 3 * box_h + 2 * gap, min_h=70)
    detail_count = min(3, len(details))
    if detail_count:
        box_h = max(34, (max_detail_h - gap * (detail_count - 1)) / detail_count)
    for i, detail in enumerate(details[:3]):
        y = box_y + i * (box_h + gap)
        if isinstance(detail, dict):
            label = detail.get("label", f"{i+1:02d}")
            text = detail.get("text", detail.get("title", ""))
        else:
            label = f"{i+1:02d}"
            text = str(detail)
        _rect(reqs, sid, f"{sid}_summary_detail_bg{i}", box_x, y, box_w, box_h,
              SURFACE, BORDER, 0.4)
        _text(reqs, sid, f"{sid}_summary_detail_no{i}", box_x + 16, y + max(10, (box_h - 11) / 2), 24, 11,
              label, ORANGE, 7, True, "Proxima Nova")
        _text(reqs, sid, f"{sid}_summary_detail_text{i}", box_x + 50, y + max(8, (box_h - 20) / 2), box_w - 68, 20,
              text, TEXT, 9, True, "Noto Sans")


def mk_metric_bar_summary(sid, metric, bars, reqs,
                          x=54, y=130, w=612, h=140,
                          metric_w=210, gap=24):
    """
    One-row performance expression:
        left  = large metric card
        right = monthly bar chart

    metric = {
        "label": "6-MONTH AVG",
        "value": "72.7%",
        "caption": "지난 6개월 평균"
    }
    bars = [
        {"label": "1월", "value": 45},
        {"label": "6월", "value": 95, "accent": True},
    ]
    """
    chart_x = x + metric_w + gap
    chart_w = w - metric_w - gap

    # Left metric card
    _rect(reqs, sid, f"{sid}_metric_bg", x, y, metric_w, h, SURFACE, BORDER, 0.5)
    _text(reqs, sid, f"{sid}_metric_label", x + 18, y + 24, metric_w - 36, 12,
          metric.get("label", "").upper(), TEXT_FAINT, 7, True, "Proxima Nova", valign=True)
    _text(reqs, sid, f"{sid}_metric_value", x + 18, y + 50, metric_w - 36, 48,
          metric.get("value", ""), ORANGE, 30, True, "Proxima Nova", valign=True)
    if metric.get("caption"):
        _text(reqs, sid, f"{sid}_metric_caption", x + 18, y + 106, metric_w - 36, 14,
              metric.get("caption", ""), TEXT_DIM, 7, False, "Noto Sans", valign=True)

    # Right chart panel
    _rect(reqs, sid, f"{sid}_chart_bg", chart_x, y, chart_w, h, SURFACE, BORDER, 0.5)
    if not bars:
        return

    max_v = max(float(b.get("value", 0)) for b in bars) or 1
    inner_x = chart_x + 18
    inner_y = y + 26
    inner_w = chart_w - 36
    bar_area_h = h - 70
    bar_gap = 8
    bar_w = (inner_w - bar_gap * (len(bars) - 1)) / len(bars)

    for i, b in enumerate(bars):
        val = float(b.get("value", 0))
        bh = max(4, bar_area_h * val / max_v)
        bx = inner_x + i * (bar_w + bar_gap)
        by = inner_y + bar_area_h - bh
        hot = b.get("accent", i == len(bars) - 1)
        bar_color = ORANGE if hot else c255(53, 31, 23)
        border_color = ORANGE if hot else c255(86, 50, 36)
        _rect(reqs, sid, f"{sid}_metric_bar{i}", bx, by, bar_w, bh,
              bar_color, border_color, 0.4)
        _text(reqs, sid, f"{sid}_metric_bar_val{i}", bx - 4, by - 15, bar_w + 8, 10,
              f"{int(val) if val.is_integer() else val:g}",
              TEXT if not hot else WHITE, 7, True, "Proxima Nova", center=True, valign=True)
        _text(reqs, sid, f"{sid}_metric_bar_lab{i}", bx - 4, y + h - 24, bar_w + 8, 10,
              b.get("label", ""), TEXT_FAINT, 7, False, "Noto Sans", center=True, valign=True)


def mk_arch_layers(sid, layers, reqs, x=54, y=148, w=612, spine_w=72, gap=20,
                   eyebrow="", title=""):
    """
    Layered architecture diagram.

    layers = [
        {"label": "입력", "title": "CSV / 제품번호 / 사용자 입력"},
        {"label": "선택", "title": "monday_resolver.py + monday_config.json", "accent": True, "desc": "..."},
        {"label": "렌더링", "title": "engine.jsx + project.json + {ID}_BSspec.json"},
        {"label": "출력", "title": "PDF 생성 / 파일명 규칙 / 저장"},
    ]
    """
    if eyebrow or title:
        _header(sid, reqs, eyebrow=eyebrow, title=title)
    visible = layers[:4]
    if not visible:
        return
    has_desc = any((row.get("desc", "") if isinstance(row, dict) else "") for row in visible)
    total_h = _fit_height_to_content(y, 230 if has_desc else 200, min_h=120)
    row_gap = 10
    row_h = (total_h - row_gap * (len(visible) - 1)) / len(visible)
    box_x = x + spine_w + gap
    box_w = w - spine_w - gap
    _rect(reqs, sid, f"{sid}_layers_spine", x, y, spine_w, total_h, SURFACE_HI, BORDER, 0.4)
    primary = _primary_index(
        visible,
        lambda row: isinstance(row, dict) and (
            row.get("role") in ("conclusion", "summary")
            or row.get("style") in ("primary", "conclusion", "summary")
        ),
    )
    for i, row in enumerate(visible):
        yy = y + i * (row_h + row_gap)
        label = row.get("label", f"{i+1:02d}")
        title_text = row.get("title", row.get("name", ""))
        desc = row.get("desc", "")
        marked = row.get("primary") or row.get("accent") or row.get("hot")
        hot = i == primary
        dim_hot = marked and not hot
        _text(reqs, sid, f"{sid}_layers_label{i}", x + 8, yy + row_h / 2 - 5, spine_w - 16, 10,
              label, ORANGE if (hot or dim_hot) else TEXT_FAINT, 7, True, "Proxima Nova", center=True)
        _rect(reqs, sid, f"{sid}_layers_box{i}", box_x, yy, box_w, row_h,
              ORANGE if hot else (ORANGE_DIM if dim_hot else SURFACE),
              ORANGE if marked else BORDER, 0.4)
        group_h = _stack_group_height([16] + ([12] if desc else []), gap=2)
        title_y = _center_group_start(yy, row_h, group_h, min_pad=10)
        _text(reqs, sid, f"{sid}_layers_title{i}", box_x + 18, title_y, box_w - 36, 16,
              title_text, BLACK if hot else TEXT, 10, True, "Noto Sans")
        if desc:
            desc_y = title_y + 18
            _text(reqs, sid, f"{sid}_layers_desc{i}", box_x + 18, desc_y, box_w - 36, 12,
                  desc, BLACK if hot else TEXT_DIM, 7, False, "Noto Sans")


def mk_arch_orchestrator(sid, nodes, reqs, eyebrow="", title="", x=54, y=146):
    """
    Structure diagram for module relationships.

    Preferred over card stacks when the page explains ownership / calling
    relationships between modules.
    """
    if eyebrow or title:
        _header(sid, reqs, eyebrow=eyebrow, title=title)

    input_text = nodes.get("input", "입력")
    main_text = nodes.get("main", "run.jsx")
    engine_text = nodes.get("engine", "engine.jsx")
    output_text = nodes.get("output", "출력")
    right_nodes = nodes.get("right_nodes", [])

    total_h = _fit_height_to_content(y, 208, min_h=160)
    main_y = y + 30
    input_y = y + 40
    right0_y = y
    engine_y = y + 128
    output_y = y + 172
    if y + 208 > CONTENT_BOTTOM:
        delta = y + 208 - CONTENT_BOTTOM
        main_y -= delta
        input_y -= delta
        right0_y -= delta
        engine_y -= delta
        output_y -= delta

    _rect(reqs, sid, f"{sid}_orc_in", x, input_y, 120, 44, SURFACE, BORDER, 0.4)
    in_group_h = 10 + 2 + 12
    in_top = _center_group_start(input_y, 44, in_group_h, min_pad=8) - input_y
    _text(reqs, sid, f"{sid}_orc_in_cap", x, input_y + in_top, 120, 10, "입력",
          TEXT_FAINT, 7, True, "Proxima Nova", center=True, valign=True)
    _text(reqs, sid, f"{sid}_orc_in_txt", x, input_y + in_top + 12, 120, 12, input_text,
          TEXT, 8, True, "Noto Sans", center=True, valign=True)

    _rect(reqs, sid, f"{sid}_orc_main", x + 200, main_y, 160, 64, ORANGE_DIM, ORANGE, 0.5)
    _text(reqs, sid, f"{sid}_orc_main_cap", x + 200, main_y + 15, 160, 10, "ORCHESTRATOR",
          ORANGE, 7, True, "Proxima Nova", center=True, valign=True)
    _text(reqs, sid, f"{sid}_orc_main_txt", x + 200, main_y + 31, 160, 16, main_text,
          TEXT, 13, True, "Noto Sans", center=True, valign=True)

    for i, item in enumerate(right_nodes[:3]):
        yy = right0_y + i * 54
        accent = item.get("accent") or item.get("primary")
        _rect(reqs, sid, f"{sid}_orc_rbox{i}", x + 428, yy, 184, 36,
              SURFACE, ORANGE if accent else BORDER, 0.4)
        _text(reqs, sid, f"{sid}_orc_rtxt{i}", x + 444, yy + 12, 152, 12,
              item.get("label", ""), TEXT, 7.5, True, "AUTO", valign=True)

    _rect(reqs, sid, f"{sid}_orc_engine", x + 200, engine_y, 160, 40, SURFACE, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_orc_engine_txt", x + 200, engine_y + 14, 160, 12, engine_text,
          TEXT, 9, True, "Noto Sans", center=True, valign=True)

    _rect(reqs, sid, f"{sid}_orc_out", x + 428, output_y, 184, 36, SURFACE, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_orc_out_txt", x + 444, output_y + 12, 152, 12, output_text,
          TEXT, 7.5, True, "AUTO", valign=True)

    in_rect = (x, input_y, 120, 44)
    main_rect = (x + 200, main_y, 160, 64)
    r0_rect = (x + 428, right0_y, 184, 36)
    r1_rect = (x + 428, right0_y + 54, 184, 36)
    r2_rect = (x + 428, right0_y + 108, 184, 36)
    eng_rect = (x + 200, engine_y, 160, 40)
    out_rect = (x + 428, output_y, 184, 36)

    main_rx, main_ry = _face_center(*main_rect, "right")
    r0_lx, r0_ly = _face_center(*r0_rect, "left")
    r1_lx, r1_ly = _face_center(*r1_rect, "left")
    r2_lx, r2_ly = _face_center(*r2_rect, "left")
    eng_rx, eng_ry = _face_center(*eng_rect, "right")
    out_lx, out_ly = _face_center(*out_rect, "left")

    connect_boxes(reqs, sid, f"{sid}_orc_c0", in_rect, main_rect, color=BORDER_HI, weight=1.0)
    orth_connector(reqs, sid, f"{sid}_orc_c1", main_rx, main_ry, r0_lx, r0_ly, color=BORDER_HI, weight=1.0)
    orth_connector(reqs, sid, f"{sid}_orc_c2", main_rx, main_ry, r1_lx, r1_ly, color=ORANGE, weight=1.0)
    orth_connector(reqs, sid, f"{sid}_orc_c3", main_rx, main_ry, r2_lx, r2_ly, color=BORDER_HI, weight=1.0)
    connect_boxes(reqs, sid, f"{sid}_orc_c4", main_rect, eng_rect, color=BORDER_HI, weight=1.0)
    orth_connector(reqs, sid, f"{sid}_orc_c5", eng_rx, eng_ry, out_lx, out_ly, color=ORANGE, weight=1.0)


def mk_decision_tree(sid, nodes, reqs, eyebrow="", title="", x=54, y=170):
    """
    Decision tree with a checkpoint and two branches.

    nodes = {
        "input": "CSV 입력",
        "decision": "자동 선택 가능?",
        "yes": "project.json 자동 선택",
        "no": "리스트박스 수동 폴백",
        "output": "PDF 출력",
        "yes_label": "자동",
        "no_label": "수동",
    }
    """
    if eyebrow or title:
        _header(sid, reqs, eyebrow=eyebrow, title=title)
    input_text = nodes.get("input", "")
    decision_text = nodes.get("decision", "")
    yes_text = nodes.get("yes", "")
    no_text = nodes.get("no", "")
    output_text = nodes.get("output", "")
    yes_label = nodes.get("yes_label", "YES")
    no_label = nodes.get("no_label", "NO")

    total_h = _fit_height_to_content(y, 140, min_h=110)
    base_y = min(y, CONTENT_BOTTOM - total_h)

    _rect(reqs, sid, f"{sid}_tree_input", x, base_y + 38, 110, 44, SURFACE, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_tree_input_t", x, base_y + 51, 110, 14, input_text,
          TEXT, 8, True, "Noto Sans", center=True)

    _rect(reqs, sid, f"{sid}_tree_decision", x + 188, base_y + 22, 126, 76, SURFACE_HI, ORANGE, 0.5)
    _text(reqs, sid, f"{sid}_tree_decision_cap", x + 188, base_y + 36, 126, 10, "판단",
          TEXT_FAINT, 7, True, "Proxima Nova", center=True)
    _text(reqs, sid, f"{sid}_tree_decision_t", x + 202, base_y + 56, 98, 14, decision_text,
          TEXT, 8, True, "Noto Sans", center=True)

    _rect(reqs, sid, f"{sid}_tree_yes", x + 396, base_y, 150, 44, ORANGE_DIM, ORANGE, 0.5)
    _text(reqs, sid, f"{sid}_tree_yes_t", x + 396, base_y + 13, 150, 14, yes_text,
          TEXT, 8, True, "Noto Sans", center=True)

    _rect(reqs, sid, f"{sid}_tree_no", x + 396, base_y + 96, 150, 44, SURFACE, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_tree_no_t", x + 396, base_y + 109, 150, 14, no_text,
          TEXT, 8, True, "Noto Sans", center=True)

    _rect(reqs, sid, f"{sid}_tree_output", x + 574, base_y + 38, 74, 44, SURFACE_HI, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_tree_output_t", x + 574, base_y + 51, 74, 14, output_text,
          TEXT, 8, True, "Noto Sans", center=True)

    connector(reqs, sid, f"{sid}_tree_c0", x + 110, base_y + 60, x + 188, base_y + 60, color=BORDER_HI, weight=1.0)
    connector(reqs, sid, f"{sid}_tree_c1", x + 314, base_y + 40, x + 396, base_y + 22, color=ORANGE, weight=1.0)
    connector(reqs, sid, f"{sid}_tree_c2", x + 314, base_y + 80, x + 396, base_y + 118, color=BORDER_HI, weight=1.0)
    connector(reqs, sid, f"{sid}_tree_c3", x + 546, base_y + 22, x + 574, base_y + 60, color=ORANGE, weight=1.0)
    connector(reqs, sid, f"{sid}_tree_c4", x + 546, base_y + 118, x + 574, base_y + 60, color=BORDER_HI, weight=1.0)

    _text(reqs, sid, f"{sid}_tree_yes_lab", x + 336, base_y + 20, 34, 10, yes_label,
          ORANGE, 5, False, "Proxima Nova", center=True)
    _text(reqs, sid, f"{sid}_tree_no_lab", x + 336, base_y + 106, 34, 10, no_label,
          TEXT_FAINT, 5, False, "Proxima Nova", center=True)


def mk_swimlane_mapping(sid, rows, reqs, eyebrow="", title="", x=54, y=148):
    """
    Swimlane mapping for module ↔ data / config relationships.

    rows = [
        {"left": "run.jsx", "middle": "입력", "right": "CSV"},
        {"left": "monday_resolver.py", "middle": "선택 기준", "right": "monday_config.json"},
        {"left": "engine.jsx", "middle": "템플릿 차이", "right": "{ID}_BSspec.json", "accent": True},
    ]
    """
    if eyebrow or title:
        _header(sid, reqs, eyebrow=eyebrow, title=title)
    visible = rows[:3]
    left_w, mid_w, right_w = 220, 120, 236
    total_h = _fit_height_to_content(y, 180, min_h=110)
    row_gap = 8
    row_h = (total_h - 28 - row_gap * (len(visible) - 1)) / len(visible)
    mid_x = x + left_w + 18
    right_x = mid_x + mid_w + 18
    _rect(reqs, sid, f"{sid}_map_left_lane", x, y, left_w, total_h, SURFACE, BORDER, 0.4)
    _rect(reqs, sid, f"{sid}_map_mid_lane", mid_x, y, mid_w, total_h, SURFACE_HI, BORDER, 0.4)
    _rect(reqs, sid, f"{sid}_map_right_lane", right_x, y, right_w, total_h, SURFACE, BORDER, 0.4)
    _text(reqs, sid, f"{sid}_map_head_left", x + 18, y + 16, 100, 10, "실행 모듈",
          ORANGE, 7, True, "Proxima Nova", valign=True)
    _text(reqs, sid, f"{sid}_map_head_mid", mid_x + 16, y + 16, mid_w - 32, 10, "관계",
          TEXT_FAINT, 7, True, "Proxima Nova", center=True, valign=True)
    _text(reqs, sid, f"{sid}_map_head_right", right_x + 18, y + 16, 100, 10, "설정 / 데이터",
          ORANGE, 7, True, "Proxima Nova", valign=True)
    base_y = y + 40
    for i, row in enumerate(visible):
        yy = base_y + i * (row_h + row_gap)
        accent = bool(row.get("primary") or row.get("accent") or row.get("hot"))
        if i < len(visible):
            _divider(reqs, sid, f"{sid}_map_sep_l{i}", x + 14, yy + row_h + 4, left_w - 28)
            _divider(reqs, sid, f"{sid}_map_sep_m{i}", mid_x + 14, yy + row_h + 4, mid_w - 28)
            _divider(reqs, sid, f"{sid}_map_sep_r{i}", right_x + 14, yy + row_h + 4, right_w - 28)
        _text(reqs, sid, f"{sid}_map_left{i}", x + 18, yy + 8, left_w - 36, 16,
              row.get("left", ""), TEXT, 13, True, "Noto Sans", valign=True)
        _text(reqs, sid, f"{sid}_map_mid{i}", mid_x + 16, yy + 10, mid_w - 32, 12,
              row.get("middle", ""), ORANGE if accent else TEXT_DIM, 7, accent, "AUTO", center=True, valign=True)
        _text(reqs, sid, f"{sid}_map_right{i}", right_x + 18, yy + 8, right_w - 36, 16,
              row.get("right", ""), TEXT, 13, True, "Noto Sans", valign=True)
