"""
spigen_build.py — Spigen Slides v5

표지/마지막 슬라이드: 템플릿 복사 후 텍스트 교체 (고정)
중간 콘텐츠 슬라이드: createSlide로 직접 생성
"""
import subprocess, json, uuid

TEMPLATE_ID     = "1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk"
COVER_TITLE_OID = "g3e66e3c2180_1_2"   # 제목
COVER_META_OID  = "g3e66e3c2180_1_3"   # 부서 | 담당자
COVER_DATE_OID  = "g3e66e3c2180_1_4"   # 날짜


def _uid():
    return "ob_" + uuid.uuid4().hex[:12]


COLORS = {
    "dark": {
        "bg":     {"red": 0.110, "green": 0.110, "blue": 0.118},  # #1C1C1E
        "fg":     {"red": 1.000, "green": 1.000, "blue": 1.000},
        "dim":    {"red": 0.650, "green": 0.650, "blue": 0.660},
        "accent": {"red": 1.000, "green": 0.420, "blue": 0.102},  # #FF6B1A
    },
    "light": {
        "bg":     {"red": 1.000, "green": 1.000, "blue": 1.000},
        "fg":     {"red": 0.110, "green": 0.110, "blue": 0.118},
        "dim":    {"red": 0.430, "green": 0.430, "blue": 0.450},
        "accent": {"red": 1.000, "green": 0.420, "blue": 0.102},
    },
}


def _pt(v):
    return {"magnitude": v, "unit": "PT"}


def _emu(pt):
    return int(pt * 12700)


def _transform(x, y):
    return {
        "scaleX": 1, "scaleY": 1,
        "translateX": _emu(x), "translateY": _emu(y),
        "unit": "EMU",
    }


def _size(w, h):
    return {
        "width":  {"magnitude": _emu(w), "unit": "EMU"},
        "height": {"magnitude": _emu(h), "unit": "EMU"},
    }


def _rgb(c):
    return {"rgbColor": c}


class SpigenBuilder:
    def __init__(self, title, theme="light"):
        """템플릿을 복사해 새 프레젠테이션 생성. 템플릿은 cover(0) + closing(1) 2장 고정."""
        if theme not in COLORS:
            theme = "light"
        r = subprocess.run(
            ["gws", "drive", "files", "copy",
             "--params", json.dumps({"fileId": TEMPLATE_ID}),
             "--json", json.dumps({"name": title})],
            capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"템플릿 복사 실패: {r.stderr or r.stdout}")
        self.pid = json.loads(r.stdout)["id"]
        self.c = COLORS[theme]
        self.reqs = []
        self._n = 0  # 콘텐츠 슬라이드 카운터 (closing 앞에 삽입)

    def _next(self):
        """콘텐츠 슬라이드용 (oid, idx) 반환 후 카운터 증가."""
        oid = _uid()         # _uid()로 충돌 방지
        idx = 1 + self._n   # 커버(0) 뒤, closing 앞에 삽입
        self._n += 1
        return oid, idx

    # ── 기본 프리미티브 ────────────────────────────────────────────

    def _slide(self, oid, idx):
        self.reqs.append({
            "createSlide": {
                "objectId": oid,
                "insertionIndex": idx,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }
        })

    def _bg(self, oid):
        self.reqs.append({
            "updatePageProperties": {
                "objectId": oid,
                "pageProperties": {
                    "pageBackgroundFill": {
                        "solidFill": {"color": _rgb(self.c["bg"])}
                    }
                },
                "fields": "pageBackgroundFill",
            }
        })

    def _shape(self, page_oid, shape_oid, x, y, w, h):
        self.reqs.append({
            "createShape": {
                "objectId": shape_oid,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_oid,
                    "size": _size(w, h),
                    "transform": _transform(x, y),
                },
            }
        })

    def _text(self, oid, text):
        self.reqs.append({
            "insertText": {"objectId": oid, "insertionIndex": 0, "text": text}
        })

    def _style(self, oid, size, bold=False, color=None, italic=False, align="START"):
        if color is None:
            color = self.c["fg"]
        self.reqs += [
            {
                "updateTextStyle": {
                    "objectId": oid,
                    "style": {
                        "fontSize": _pt(size),
                        "bold": bold,
                        "italic": italic,
                        "foregroundColor": {"opaqueColor": _rgb(color)},
                        "fontFamily": "Noto Sans KR",
                    },
                    "textRange": {"type": "ALL"},
                    "fields": "fontSize,bold,italic,foregroundColor,fontFamily",
                }
            },
            {
                "updateParagraphStyle": {
                    "objectId": oid,
                    "style": {"alignment": align},
                    "textRange": {"type": "ALL"},
                    "fields": "alignment",
                }
            },
        ]

    def _hline(self, page_oid, x, y, w, weight=2, color=None):
        if color is None:
            color = self.c["accent"]
        oid = _uid()
        self.reqs.append({
            "createLine": {
                "objectId": oid,
                "lineCategory": "STRAIGHT",
                "elementProperties": {
                    "pageObjectId": page_oid,
                    "size": {"width": {"magnitude": _emu(w), "unit": "EMU"},
                             "height": {"magnitude": 0, "unit": "EMU"}},
                    "transform": _transform(x, y),
                },
            }
        })
        self.reqs.append({
            "updateLineProperties": {
                "objectId": oid,
                "lineProperties": {
                    "lineFill": {"solidFill": {"color": _rgb(color)}},
                    "weight": _pt(weight),
                },
                "fields": "lineFill,weight",
            }
        })

    def _vline(self, page_oid, x, y, h, weight=4, color=None):
        if color is None:
            color = self.c["accent"]
        oid = _uid()
        self.reqs.append({
            "createLine": {
                "objectId": oid,
                "lineCategory": "STRAIGHT",
                "elementProperties": {
                    "pageObjectId": page_oid,
                    "size": {"width": {"magnitude": 0, "unit": "EMU"},
                             "height": {"magnitude": _emu(h), "unit": "EMU"}},
                    "transform": _transform(x, y),
                },
            }
        })
        self.reqs.append({
            "updateLineProperties": {
                "objectId": oid,
                "lineProperties": {
                    "lineFill": {"solidFill": {"color": _rgb(color)}},
                    "weight": _pt(weight),
                },
                "fields": "lineFill,weight",
            }
        })

    # ── 슬라이드 타입 ──────────────────────────────────────────────

    def cover(self, title, subtitle="", dept="디자인부문ㅣ패키지디자인팀",
              name="한원진 담당", date="2026. 04."):
        """표지: 템플릿 커버 슬라이드의 텍스트를 교체. deleteText 후 insertText + 스타일 재적용."""
        title_text = f"{title}\n{subtitle}" if subtitle else title
        meta_text  = f"{dept}\n{name}"
        entries = [
            (COVER_TITLE_OID, title_text, 28, True),
            (COVER_META_OID,  meta_text,  11, False),
            (COVER_DATE_OID,  date,        11, False),
        ]
        for oid, text, size, bold in entries:
            self.reqs += [
                {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
                {"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}},
                {"updateTextStyle": {
                    "objectId": oid,
                    "style": {
                        "fontSize": _pt(size),
                        "bold": bold,
                        "fontFamily": "Noto Sans KR",
                        "foregroundColor": {"opaqueColor": _rgb(self.c["fg"])},
                    },
                    "textRange": {"type": "ALL"},
                    "fields": "fontSize,bold,fontFamily,foregroundColor",
                }},
            ]

    def closing(self, **kwargs):
        """마지막 슬라이드: 템플릿 슬라이드 그대로 유지. 아무것도 하지 않음."""
        pass

    def slide(self, heading, body, body_size=14):
        """본문: 헤더 + 오렌지 가로선 + 텍스트박스"""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        b = _uid()
        self._shape(oid, b, 40, 72, 640, 310)
        self._text(b, body)
        self._style(b, body_size)

    def two_col(self, heading, left_title, left_body, right_title, right_body):
        """2단 슬라이드: 헤더 + 왼쪽/오른쪽 패널"""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        lt = _uid()
        self._shape(oid, lt, 40, 76, 310, 28)
        self._text(lt, left_title)
        self._style(lt, 15, bold=True, color=self.c["accent"])

        lb = _uid()
        self._shape(oid, lb, 40, 108, 310, 274)
        self._text(lb, left_body)
        self._style(lb, 13)

        self._vline(oid, 365, 76, 300, weight=1, color=self.c["dim"])

        rt = _uid()
        self._shape(oid, rt, 375, 76, 310, 28)
        self._text(rt, right_title)
        self._style(rt, 15, bold=True, color=self.c["accent"])

        rb = _uid()
        self._shape(oid, rb, 375, 108, 310, 274)
        self._text(rb, right_body)
        self._style(rb, 13)

    def flow(self, heading, steps):
        """흐름 슬라이드: 헤더 + 번호 단계 목록. steps = [(label, desc), ...]"""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        step_h = max(16, min(60, 290 // max(len(steps), 1)))
        for i, (label, desc) in enumerate(steps):
            y = 72 + i * (step_h + 6)
            num = _uid()
            self._shape(oid, num, 40, y, 32, step_h)
            self._text(num, str(i + 1))
            self._style(num, 16, bold=True, color=self.c["accent"], align="CENTER")

            self._vline(oid, 80, y + 4, step_h - 8, weight=1, color=self.c["dim"])

            body = _uid()
            self._shape(oid, body, 90, y, 590, step_h)
            self._text(body, f"{label}\n{desc}" if desc else label)
            self._style(body, 13)

    def decision(self, heading, question, yes_label, yes_body, no_label, no_body):
        """분기 슬라이드: 헤더 + 질문 박스 + YES/NO 패널"""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        q = _uid()
        self._shape(oid, q, 160, 72, 400, 44)
        self._text(q, question)
        self._style(q, 15, bold=True, align="CENTER")
        self._hline(oid, 160, 118, 400, weight=1, color=self.c["dim"])

        yl = _uid()
        self._shape(oid, yl, 40, 130, 300, 28)
        self._text(yl, f"✓  {yes_label}")
        self._style(yl, 14, bold=True, color=self.c["accent"])

        yb = _uid()
        self._shape(oid, yb, 40, 162, 300, 210)
        self._text(yb, yes_body)
        self._style(yb, 13)

        self._vline(oid, 355, 130, 230, weight=1, color=self.c["dim"])

        nl = _uid()
        self._shape(oid, nl, 365, 130, 315, 28)
        self._text(nl, f"✗  {no_label}")
        self._style(nl, 14, bold=True, color=self.c["dim"])

        nb = _uid()
        self._shape(oid, nb, 365, 162, 315, 210)
        self._text(nb, no_body)
        self._style(nb, 13)

    def checklist(self, heading, items):
        """체크리스트 슬라이드: 헤더 + 항목 목록. items = [(label, done), ...]"""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        item_h = max(16, min(52, 300 // max(len(items), 1)))
        for i, (label, done) in enumerate(items):
            y = 72 + i * (item_h + 4)
            mark = _uid()
            self._shape(oid, mark, 40, y, 32, item_h)
            self._text(mark, "●" if done else "○")
            color = self.c["accent"] if done else self.c["dim"]
            self._style(mark, 16, color=color, align="CENTER")

            txt = _uid()
            self._shape(oid, txt, 82, y, 598, item_h)
            self._text(txt, label)
            self._style(txt, 13, color=self.c["dim"] if done else self.c["fg"])

    # ── API 플러시 ────────────────────────────────────────────────

    def flush(self):
        ok = True
        for i in range(0, len(self.reqs), 50):
            chunk = self.reqs[i:i + 50]
            r = subprocess.run(
                ["gws", "slides", "presentations", "batchUpdate",
                 "--params", json.dumps({"presentationId": self.pid}),
                 "--json",   json.dumps({"requests": chunk})],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                out = "\n".join(x for x in [r.stdout, r.stderr] if x).strip()[:400]
                print(f"[오류] 청크 {i // 50 + 1}: {out}")
                ok = False
        self.reqs = []
        return ok
