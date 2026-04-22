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

# Kept for older snippets that import THEMES.
THEMES = {
    "dark": {
        "SLIDE_BG": BG,
        "TITLE_COLOR": TEXT,
        "BODY_COLOR": TEXT_DIM,
        "CARD_BG": SURFACE,
        "CARD_BORDER": BORDER,
    },
    "light": {
        # Compatibility only. Current template still uses dark output.
        "SLIDE_BG": BG,
        "TITLE_COLOR": TEXT,
        "BODY_COLOR": TEXT_DIM,
        "CARD_BG": SURFACE,
        "CARD_BORDER": BORDER,
    },
    "warm": {
        # Compatibility only. Current template still uses dark output.
        "SLIDE_BG": BG,
        "TITLE_COLOR": TEXT,
        "BODY_COLOR": TEXT_DIM,
        "CARD_BG": SURFACE,
        "CARD_BORDER": BORDER,
    },
}


def shape(oid, page, stype, x, y, w, h):
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


def fill(oid, fg, bg=None, wt=0.4):
    bg = bg or fg
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


def txtstyle(oid, color, size, bold=False, ff="Noto Sans"):
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
          ff="Noto Sans", center=False, valign=False):
    reqs += [
        shape(oid, sid, "TEXT_BOX", x, y, w, h),
        txt(oid, text),
        txtstyle(oid, color, size, bold=bold, ff=ff),
        clr(oid),
    ]
    if center:
        reqs.append(align(oid, "CENTER"))
    if valign:
        reqs.append(middle(oid))


def _rect(reqs, sid, oid, x, y, w, h, bg=SURFACE, border=BORDER, wt=0.5):
    reqs += [shape(oid, sid, "RECTANGLE", x, y, w, h), fill(oid, bg, border, wt)]


def _header(sid, reqs, eyebrow="", title="", page_no=None, total=None, footer=""):
    if eyebrow:
        _text(reqs, sid, f"{sid}_eyebrow", M, M, 240, 12, eyebrow.upper(),
              ORANGE, 7, True, "Noto Sans")
    if title:
        _text(reqs, sid, f"{sid}_title", M, 54, W - M * 2, 40, title,
              TEXT, 22, True, "Noto Sans")
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


def mk_3col(sid, cols, reqs, theme="dark"):
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
        _text(reqs, sid, f"{sid}_cl{i}", x + 18, y0 + 20, card_w - 36, 12,
              str(label).upper(), BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), 7, True, "Proxima Nova")
        _text(reqs, sid, f"{sid}_ct{i}", x + 18, y0 + 43, card_w - 36, 28,
              title, BLACK if hot else TEXT, 13, True, "Noto Sans")
        for j, item in enumerate(items[:5]):
            yy = y0 + 82 + j * 19
            reqs += [shape(f"{sid}_dot{i}_{j}", sid, "RECTANGLE", x + 18, yy + 5, 2.5, 2.5),
                     fill(f"{sid}_dot{i}_{j}", BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), 0)]
            _text(reqs, sid, f"{sid}_it{i}_{j}", x + 28, yy, card_w - 46, 13,
                  item, BLACK if hot else TEXT_DIM, 7, False, "Noto Sans")


def mk_3col_cards(sid, cards, reqs, theme="dark"):
    normalized = []
    for i, c in enumerate(cards[:3]):
        normalized.append({
            "label": c.get("num", c.get("label", f"0{i+1}")),
            "title": c.get("title", c.get("label", "")),
            "items": [c.get("body", "")] if c.get("body") else c.get("items", []),
            "hot": c.get("hot") or c.get("accent") or c.get("style") == "accent",
        })
    mk_3col(sid, normalized, reqs, theme=theme)


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
              f"STEP {num}", BLACK if is_primary else (ORANGE if dim_hot else TEXT_FAINT), 5, False, "JetBrains Mono")
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


def mk_text_block(sid, body_text, reqs, y_start=128, font_size=10, theme="dark"):
    _rect(reqs, sid, f"{sid}_bodybox", M, y_start, W - M * 2, 170, SURFACE, BORDER, 0.5)
    _text(reqs, sid, f"{sid}_body", M + 20, y_start + 22, W - M * 2 - 40, 120,
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
    card_h = 128
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
              k.get("label", ""), BLACK if hot else (ORANGE if dim_hot else TEXT_FAINT), 6, True, "Noto Sans")
        _text(reqs, sid, f"{sid}_kpi_value{i}", x + 14, y + 46, card_w - 28, 40,
              k.get("value", ""), BLACK if hot else TEXT, 26, True, "Proxima Nova")
        _text(reqs, sid, f"{sid}_kpi_sub{i}", x + 14, y + 91, card_w - 28, 20,
              k.get("sub", ""), BLACK if hot else TEXT_DIM, 7, False, "Noto Sans")


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
              ORANGE if hot else TEXT_DIM, 6, True, "Proxima Nova", center=True)
        _text(reqs, sid, f"{prefix}_lab{i}", bx - 6, y + h + 8, bw + 12, 12,
              b.get("label", ""), TEXT_FAINT, 5.5, False, "Noto Sans", center=True)


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
    _rect(reqs, sid, f"{sid}_tbl_head_bg", x, y, w, header_h, SURFACE_HI, BORDER_HI, 0.5)
    for i, head in enumerate(headers):
        _text(reqs, sid, f"{sid}_tbl_head{i}", xs[i] + 10, y + 7, ws[i] - 20, 10,
              head, TEXT_FAINT, 5.5, True, "Noto Sans")
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
                  val, color, 7, bold, "Noto Sans")


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
              eyebrow.upper(), ORANGE, 7, True, "JetBrains Mono")
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
        _text(reqs, sid, f"{sid}_summary_detail_no{i}", box_x + 16, y + 16, 24, 11,
              label, ORANGE, 6.5, True, "JetBrains Mono")
        _text(reqs, sid, f"{sid}_summary_detail_text{i}", box_x + 50, y + 13, box_w - 68, 20,
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
          metric.get("label", "").upper(), TEXT_FAINT, 5.5, True, "Proxima Nova")
    _text(reqs, sid, f"{sid}_metric_value", x + 18, y + 50, metric_w - 36, 48,
          metric.get("value", ""), ORANGE, 30, True, "Proxima Nova")
    if metric.get("caption"):
        _text(reqs, sid, f"{sid}_metric_caption", x + 18, y + 106, metric_w - 36, 14,
              metric.get("caption", ""), TEXT_DIM, 6.5, False, "Noto Sans")

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
              TEXT if not hot else WHITE, 5.5, True, "Proxima Nova", center=True)
        _text(reqs, sid, f"{sid}_metric_bar_lab{i}", bx - 4, y + h - 24, bar_w + 8, 10,
              b.get("label", ""), TEXT_FAINT, 5.5, False, "Noto Sans", center=True)
