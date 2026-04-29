"""
spigen_build.py — Spigen Slides v5 단순 빌더
createSlide + createShape + insertText + 스타일 적용
복잡한 컴포넌트 없음. 헤더 + 텍스트박스 구조만.
"""
import subprocess, json, uuid


def _uid():
    return "ob_" + uuid.uuid4().hex[:12]


COLORS = {
    "dark": {
        "bg":     {"red": 0.110, "green": 0.110, "blue": 0.118},  # #1C1C1E
        "fg":     {"red": 1.000, "green": 1.000, "blue": 1.000},  # #FFFFFF
        "dim":    {"red": 0.650, "green": 0.650, "blue": 0.660},  # muted
        "accent": {"red": 1.000, "green": 0.420, "blue": 0.102},  # #FF6B1A
    },
    "light": {
        "bg":     {"red": 1.000, "green": 1.000, "blue": 1.000},  # #FFFFFF
        "fg":     {"red": 0.110, "green": 0.110, "blue": 0.118},  # #1C1C1E
        "dim":    {"red": 0.430, "green": 0.430, "blue": 0.450},  # muted
        "accent": {"red": 1.000, "green": 0.420, "blue": 0.102},  # #FF6B1A
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
    def __init__(self, presentation_id, theme="light"):
        self.pid = presentation_id
        self.c = COLORS[theme]
        self.reqs = []

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

    def cover(self, oid, idx, title, subtitle="", dept="디자인부문ㅣ패키지디자인팀",
              name="한원진 담당", date="2026. 04."):
        """표지: 왼쪽 오렌지 세로선 | 제목 | 부제 | 하단 메타"""
        self._slide(oid, idx)
        self._bg(oid)
        self._vline(oid, 40, 55, 180)

        t = _uid()
        self._shape(oid, t, 60, 60, 610, 140)
        self._text(t, title)
        self._style(t, 34, bold=True)

        if subtitle:
            s = _uid()
            self._shape(oid, s, 60, 210, 610, 60)
            self._text(s, subtitle)
            self._style(s, 17, color=self.c["dim"])

        meta = f"{dept}  |  {name}  |  {date}"
        m = _uid()
        self._shape(oid, m, 40, 358, 640, 28)
        self._text(m, meta)
        self._style(m, 11, color=self.c["dim"])

    def slide(self, oid, idx, heading, body, body_size=14):
        """본문: 헤더 + 오렌지 가로선 + 텍스트박스"""
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

    def two_col(self, oid, idx, heading, left_title, left_body,
                right_title, right_body):
        """2단 슬라이드: 헤더 + 왼쪽/오른쪽 패널"""
        self._slide(oid, idx)
        self._bg(oid)

        h = _uid()
        self._shape(oid, h, 40, 20, 640, 38)
        self._text(h, heading)
        self._style(h, 22, bold=True)

        self._hline(oid, 40, 62, 640)

        # 왼쪽 패널
        lt = _uid()
        self._shape(oid, lt, 40, 76, 310, 28)
        self._text(lt, left_title)
        self._style(lt, 15, bold=True, color=self.c["accent"])

        lb = _uid()
        self._shape(oid, lb, 40, 108, 310, 274)
        self._text(lb, left_body)
        self._style(lb, 13)

        # 세로 구분선
        self._vline(oid, 365, 76, 300, weight=1, color=self.c["dim"])

        # 오른쪽 패널
        rt = _uid()
        self._shape(oid, rt, 375, 76, 310, 28)
        self._text(rt, right_title)
        self._style(rt, 15, bold=True, color=self.c["accent"])

        rb = _uid()
        self._shape(oid, rb, 375, 108, 310, 274)
        self._text(rb, right_body)
        self._style(rb, 13)

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
