"""
spigen_build.py — Spigen Slides v5.3

표지: 테마별 템플릿 복사 후 텍스트 교체 (클로징 없음)
중간 콘텐츠 슬라이드: createSlide로 직접 생성
"""
import subprocess, json, uuid

# ── 라이트 표지 템플릿 (KPI 기준) ────────────────────────────────
LIGHT_TEMPLATE_ID  = "1BBG9PR6ZBsEABbJLhbUUfRMkgGYQtNMOWAmLQgPhr70"
LIGHT_COVER_TITLE_OID = "g3d96284c9ce_0_1"
LIGHT_COVER_META_OID  = "g3d96284c9ce_0_2"
LIGHT_COVER_DATE_OID  = "g3d96284c9ce_0_3"
LIGHT_GUIDE_SLIDES    = [
    "test_rule",
    "test_flow",
    "test_arch",
    "test_map",
    "guide_kpi_status_light",
    "guide_kpi_key_tasks_light",
]

# ── 다크 템플릿 ────────────────────────────────────────────────
DARK_TEMPLATE_ID      = "1HJbTWXPCr38gXDQuarglSLrkheDQXAojlrYUKcfVgAc"
DARK_COVER_TITLE_OID  = "rebuild_cover_title"
DARK_COVER_TEAM_OID   = "rebuild_cover_team"   # 부서 | 담당자
DARK_COVER_META_OID   = "rebuild_cover_meta"   # 날짜
DARK_GUIDE_SLIDES     = [
    "ref_toc", "g3dab74f0851_0_70", "g3e667bf10ea_0_0",
    "SLIDES_API1345277958_51", "SLIDES_API1345277958_78",
    "SLIDES_API1345277958_156", "g3e667bf10ea_0_97",
    "dsgv31_10_flow", "SLIDES_API1345277958_241",
    "gal_8e928ff12b09", "g3dab74f0851_0_37",
    "SLIDES_API1345277958_269", "SLIDES_API1345277958_296",
    "gal_572682a9c20e", "gal_bf0db096e52a",
    "guide_last_selection_v2", "g3e667bf10ea_0_135",
    "g3e667bf10ea_0_24",
]

KPI_TEMPLATE_ID     = LIGHT_TEMPLATE_ID
KPI_COVER_TITLE_OID = "g3d96284c9ce_0_1"
KPI_COVER_META_OID  = "g3d96284c9ce_0_2"
KPI_COVER_DATE_OID  = "g3d96284c9ce_0_3"
KPI_TEST_SLIDES     = ["test_rule", "test_flow", "test_arch", "test_map"]
KPI_STATUS_EYEBROW  = "guide_kpi_status_light_eyebrow"
KPI_STATUS_TITLE    = "guide_kpi_status_light_title"
KPI_STATUS_TOP_TBL  = "guide_kpi_status_light_kpi_top_tbl"
KPI_STATUS_DTL_TBL  = "guide_kpi_status_light_kpi_detail_tbl"
KPI_TASKS_EYEBROW   = "guide_kpi_key_tasks_light_eyebrow"
KPI_TASKS_TITLE     = "guide_kpi_key_tasks_light_title"
KPI_TASKS_TBL       = "guide_kpi_key_tasks_light_kpi_task_tbl"


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


# ── 오버플로우 방지 헬퍼 ──────────────────────────────────────────
_BODY_H = 310   # slide() 본문 박스 높이 pt
_COL_H  = 274   # two_col() 컬럼 본문 높이 pt
_LINE_H = {10: 14, 11: 15, 12: 17, 13: 18, 14: 20, 16: 23}


def _line_count(text: str) -> int:
    return max(len(text.splitlines()), 1)


def _fits(h_avail: int, lines: int, size: int) -> bool:
    return lines * _LINE_H.get(size, int(size * 1.4)) <= h_avail


def _safe_size(h_avail: int, lines: int, start: int = 14) -> int:
    """박스에 들어오는 최대 font_size 반환. 최소 10pt."""
    for s in (start, 13, 12, 11, 10):
        if _fits(h_avail, lines, s):
            return s
    return 10


class SpigenBuilder:
    def __init__(self, title, theme="light", template="standard"):
        """템플릿을 복사해 새 프레젠테이션 생성.
        template="standard": 테마별 지정 템플릿 커버만 복사, 불필요 슬라이드 삭제.
          theme="light" → KPI 라이트 템플릿 cover 기준
          theme="dark"  → 다크 템플릿 (가이드 슬라이드 전체 삭제)
        template="kpi": 라이트 KPI 템플릿. cover + kpi_status + kpi_tasks.
        """
        if theme not in COLORS:
            theme = "light"
        if template == "kpi":
            tmpl_id = KPI_TEMPLATE_ID
            self._cover_oids = (KPI_COVER_TITLE_OID, KPI_COVER_META_OID, KPI_COVER_DATE_OID)
        elif theme == "dark":
            tmpl_id = DARK_TEMPLATE_ID
            self._cover_oids = (DARK_COVER_TITLE_OID, DARK_COVER_TEAM_OID, DARK_COVER_META_OID)
        else:
            tmpl_id = LIGHT_TEMPLATE_ID
            self._cover_oids = (LIGHT_COVER_TITLE_OID, LIGHT_COVER_META_OID, LIGHT_COVER_DATE_OID)
        r = subprocess.run(
            ["gws", "drive", "files", "copy",
             "--params", json.dumps({"fileId": tmpl_id}),
             "--json", json.dumps({"name": title})],
            capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"템플릿 복사 실패: {r.stderr or r.stdout}")
        self.pid = json.loads(r.stdout)["id"]
        self.c = COLORS[theme]
        self.reqs = []
        self._n = 0
        self.template = template
        if template == "kpi":
            for oid in KPI_TEST_SLIDES:
                self.reqs.append({"deleteObject": {"objectId": oid}})
        elif theme == "dark":
            for oid in DARK_GUIDE_SLIDES:
                self.reqs.append({"deleteObject": {"objectId": oid}})
        else:
            for oid in LIGHT_GUIDE_SLIDES:
                self.reqs.append({"deleteObject": {"objectId": oid}})

    def _next(self):
        """콘텐츠 슬라이드용 (oid, idx) 반환 후 카운터 증가."""
        oid = _uid()
        idx = 1 + self._n   # 커버(0) 뒤에 순서대로 삽입
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

    def _replace_text(self, oid, text):
        """shape 텍스트 전체 교체 (deleteText + insertText)."""
        self.reqs += [
            {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
            {"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}},
        ]

    def _tbl_cell(self, tbl_oid, row, col, text):
        """테이블 셀 텍스트 교체. 빈/None 값은 skip — merged 이차 셀 deleteText 오류 방지."""
        if text is None:
            return
        text = str(text).strip()
        if not text:
            return
        self.reqs += [
            {"deleteText": {
                "objectId": tbl_oid,
                "cellLocation": {"rowIndex": row, "columnIndex": col},
                "textRange": {"type": "ALL"},
            }},
            {"insertText": {
                "objectId": tbl_oid,
                "cellLocation": {"rowIndex": row, "columnIndex": col},
                "insertionIndex": 0,
                "text": text,
            }},
        ]

    def cover(self, title, subtitle="", dept="디자인부문ㅣ패키지디자인팀",
              name="한원진 담당", date="2026. 04."):
        """표지: 템플릿 커버 슬라이드의 텍스트를 교체. deleteText 후 insertText + 스타일 재적용."""
        title_oid, meta_oid, date_oid = self._cover_oids
        title_text = f"{title}\n{subtitle}" if subtitle else title
        meta_text  = f"{dept}\n{name}"
        entries = [
            (title_oid, title_text, 28, True),
            (meta_oid,  meta_text,  11, False),
            (date_oid,  date,       11, False),
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

    def auto_slide(self, role, heading,
                   body=None,
                   left_title=None, left_body=None,
                   right_title=None, right_body=None,
                   steps=None, items=None,
                   question=None,
                   yes_label=None, yes_body=None,
                   no_label=None, no_body=None):
        """역할 기반 자동 컴포넌트 선택 + 오버플로우 방지.

        role: "설명" | "결정유도" | "비교" | "순서" | "체크" | "분기"
        내용이 박스를 초과하면 font_size를 자동 축소 (최소 10pt).
        내용은 절대 자르지 않는다.
        """
        if role in ("설명", "결정유도"):
            lines = _line_count(body or "")
            size = _safe_size(_BODY_H, lines, start=14)
            self.slide(heading, body or "", body_size=size)

        elif role == "비교":
            self.two_col(
                heading,
                left_title or "", left_body or "",
                right_title or "", right_body or "",
            )

        elif role == "순서":
            self.flow(heading, steps or [])

        elif role == "체크":
            self.checklist(heading, items or [])

        elif role == "분기":
            self.decision(
                heading,
                question or "",
                yes_label or "", yes_body or "",
                no_label or "", no_body or "",
            )

        else:
            lines = _line_count(body or "")
            size = _safe_size(_BODY_H, lines, start=14)
            self.slide(heading, body or "", body_size=size)

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

    def kpi_status(self, title="1. KPI 진행 현황", eyebrow="2025년도",
                   top_rows=None, detail_rows=None):
        """KPI 현황 슬라이드: 템플릿 슬라이드 텍스트 교체. template='kpi' 전용.
        top_rows: [[목표, kpi, 가중치, h1목표, h1실적, h1달성률, 연간목표, 연간실적, 연간달성률], ...]  (최대 3행)
        detail_rows: [[kpi, 정의, 측정산식, 증빙], ...]  (최대 3행)
        """
        if self.template != "kpi":
            raise ValueError("kpi_status()는 template='kpi'에서만 사용 가능합니다.")
        self._replace_text(KPI_STATUS_EYEBROW, eyebrow)
        self._replace_text(KPI_STATUS_TITLE, title)
        for ri, row in enumerate((top_rows or [])[:3]):
            for ci, val in enumerate(row[:9]):
                if ri == 1 and ci == 0:
                    continue  # [2,0] rs=2 merge가 row3 col0을 cover — 쓰기 불가
                self._tbl_cell(KPI_STATUS_TOP_TBL, ri + 2, ci, val)
        for ri, row in enumerate((detail_rows or [])[:3]):
            for ci, val in enumerate(row[:4]):
                self._tbl_cell(KPI_STATUS_DTL_TBL, ri + 1, ci, val)

    def kpi_tasks(self, title="2. 핵심과제", eyebrow="2025", rows=None):
        """주요 과제 슬라이드: 템플릿 슬라이드 텍스트 교체. template='kpi' 전용.
        rows: [[연관kpi, 핵심과제, 실행계획, 나의역할], ...]  (최대 3행)
        """
        if self.template != "kpi":
            raise ValueError("kpi_tasks()는 template='kpi'에서만 사용 가능합니다.")
        self._replace_text(KPI_TASKS_EYEBROW, eyebrow)
        self._replace_text(KPI_TASKS_TITLE, title)
        for ri, row in enumerate((rows or [])[:3]):
            for ci, val in enumerate(row[:4]):
                if ri == 1 and ci == 0:
                    continue  # [1,0] rowSpan=2 → row 2 col 0은 covered cell
                self._tbl_cell(KPI_TASKS_TBL, ri + 1, ci, val)

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
