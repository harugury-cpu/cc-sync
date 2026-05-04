"""
spigen_build.py — Spigen Slides v5.4

표지: 테마별 템플릿 복사 후 텍스트 교체 (클로징 없음)
중간 콘텐츠 슬라이드: createSlide로 직접 생성
헤더/색/간격 토큰: spigen_tokens 참조
"""
import os, subprocess, json, uuid
import spigen_tokens as _T


# ─────────────────────────────────────────────────────────────────
# V5.8: PID 캐시 헬퍼 — 같은 빌드 이름에 누적 수정 (in-place 업데이트)
# ─────────────────────────────────────────────────────────────────

def _pid_cache_path(name):
    return f"/tmp/spigen_pid_{name}.json"


def load_pid(name, theme):
    """저장된 PRESENTATION_ID 로드 (없으면 None).
    name: 빌드 식별자 (예: 'foldable_qr')
    theme: 'dark' | 'light' | 'kpi'
    """
    path = _pid_cache_path(name)
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        return data.get(theme)
    except (json.JSONDecodeError, OSError):
        return None


def save_pid(name, theme, pid):
    """PID 저장. 같은 name+theme에 다음 빌드부터 in-place 모드 동작."""
    path = _pid_cache_path(name)
    data = {}
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    data[theme] = pid
    with open(path, "w") as f:
        json.dump(data, f)


def clear_pid(name, theme=None):
    """PID 캐시 삭제 — 다음 빌드 시 새 파일 생성.
    theme=None 이면 모든 테마 삭제.
    """
    path = _pid_cache_path(name)
    if not os.path.exists(path):
        return
    if theme is None:
        os.remove(path)
        return
    try:
        with open(path) as f:
            data = json.load(f)
        data.pop(theme, None)
        with open(path, "w") as f:
            json.dump(data, f)
    except (json.JSONDecodeError, OSError):
        pass

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
DARK_COVER_TITLE_OID  = "g3db53c0022e_0_2"   # V5.9: 사용자가 cover 정리, 새 OID
DARK_COVER_TEAM_OID   = "g3db53c0022e_0_3"   # 부서 | 담당자
DARK_COVER_META_OID   = "g3db53c0022e_0_4"   # 날짜
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
        "bg":        {"red": 0.110, "green": 0.110, "blue": 0.118},  # #1C1C1E
        "fg":        {"red": 1.000, "green": 1.000, "blue": 1.000},
        "dim":       {"red": 0.650, "green": 0.650, "blue": 0.660},
        "accent":    {"red": 1.000, "green": 0.420, "blue": 0.102},  # #FF6B1A
        # 시트 실측: 강조 카드 fill = ORANGE_DIM (rgb 61,26,5)
        "accent_bg": {"red": 0.239, "green": 0.102, "blue": 0.020},
        # 시트 실측: 일반 카드 fill = SURFACE (rgb 14,14,14)
        "surface":   {"red": 0.055, "green": 0.055, "blue": 0.055},
        # 시트 실측: BORDER = rgb(32,32,32)
        "border":    {"red": 0.125, "green": 0.125, "blue": 0.125},
    },
    "light": {
        "bg":        {"red": 1.000, "green": 1.000, "blue": 1.000},
        "fg":        {"red": 0.110, "green": 0.110, "blue": 0.118},
        "dim":       {"red": 0.430, "green": 0.430, "blue": 0.450},
        "accent":    {"red": 1.000, "green": 0.420, "blue": 0.102},
        # light 강조 카드: 옅은 오렌지 배경
        "accent_bg": {"red": 1.000, "green": 0.941, "blue": 0.902},
        "surface":   {"red": 1.000, "green": 1.000, "blue": 1.000},
        "border":    {"red": 0.851, "green": 0.851, "blue": 0.824},  # rgb(217,217,210)
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
    def __init__(self, title, theme="dark", template="standard", presentation_id=None):
        """템플릿을 복사해 새 프레젠테이션 생성. (V5.7: default dark)

        template="standard": 테마별 지정 템플릿 커버만 복사, 불필요 슬라이드 삭제.
          theme="dark"  → 다크 템플릿 (default, V5.7)
          theme="light" → KPI 라이트 템플릿 cover 기준 (사용자 명시 시에만)
        template="kpi": 라이트 KPI 템플릿. cover + kpi_status + kpi_tasks.

        V5.8 in-place 모드:
          presentation_id 가 주어지면 해당 파일에 직접 업데이트.
          - 표지(첫 슬라이드)는 보존, 콘텐츠 슬라이드는 모두 삭제 후 재생성.
          - 같은 URL 유지 — 사용자가 처음 만든 파일에 계속 누적 수정 가능.
        """
        if theme not in COLORS:
            theme = "light"
        if template == "kpi":
            self._cover_oids = (KPI_COVER_TITLE_OID, KPI_COVER_META_OID, KPI_COVER_DATE_OID)
        elif theme == "dark":
            self._cover_oids = (DARK_COVER_TITLE_OID, DARK_COVER_TEAM_OID, DARK_COVER_META_OID)
        else:
            self._cover_oids = (LIGHT_COVER_TITLE_OID, LIGHT_COVER_META_OID, LIGHT_COVER_DATE_OID)
        self.c = COLORS[theme]
        self.reqs = []
        self._n = 0
        self.template = template

        # V5.8 in-place 모드
        if presentation_id:
            self.pid = presentation_id
            r = subprocess.run(
                ["gws", "slides", "presentations", "get",
                 "--params", json.dumps({"presentationId": presentation_id})],
                capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"기존 파일 조회 실패: {r.stderr or r.stdout}")
            raw = r.stdout
            ji = raw.find("{")
            if ji < 0:
                raise RuntimeError(f"기존 파일 응답 파싱 실패: {raw[:200]}")
            data = json.loads(raw[ji:])
            slides = data.get("slides", [])
            # 표지(첫 슬라이드) 보존, 나머지 모두 삭제
            for s in slides[1:]:
                self.reqs.append({"deleteObject": {"objectId": s["objectId"]}})
            return

        # 기본: 템플릿 복사 모드
        if template == "kpi":
            tmpl_id = KPI_TEMPLATE_ID
        elif theme == "dark":
            tmpl_id = DARK_TEMPLATE_ID
        else:
            tmpl_id = LIGHT_TEMPLATE_ID
        r = subprocess.run(
            ["gws", "drive", "files", "copy",
             "--params", json.dumps({"fileId": tmpl_id}),
             "--json", json.dumps({"name": title})],
            capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"템플릿 복사 실패: {r.stderr or r.stdout}")
        self.pid = json.loads(r.stdout)["id"]
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

    def _shape(self, page_oid, shape_oid, x, y, w, h, valign="MIDDLE"):
        """텍스트박스 생성 + 세로 정렬 자동 적용.
        valign: TOP / MIDDLE / BOTTOM. 기본값 MIDDLE — 모든 텍스트 세로 중앙.
        """
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
        if valign:
            self.reqs.append({
                "updateShapeProperties": {
                    "objectId": shape_oid,
                    "shapeProperties": {"contentAlignment": valign},
                    "fields": "contentAlignment",
                }
            })

    def _text(self, oid, text):
        self.reqs.append({
            "insertText": {"objectId": oid, "insertionIndex": 0, "text": text}
        })

    def _text_md(self, oid, text):
        """**굵게** 마크업 인식해서 텍스트 삽입 + bold 범위 반환.

        예: '관리 **복잡** 발생' → 'bold_ranges' 에는 (3, 5) 반환.
        호출자는 _style() 후 _apply_bold_ranges(oid, ranges) 호출.
        """
        import re
        parts = re.split(r"(\*\*[^*]+\*\*)", text)
        full_text = ""
        bold_ranges = []
        for part in parts:
            if part.startswith("**") and part.endswith("**") and len(part) > 4:
                inner = part[2:-2]
                start = len(full_text)
                full_text += inner
                bold_ranges.append((start, len(full_text)))
            else:
                full_text += part
        if full_text:
            self._text(oid, full_text)
        return bold_ranges

    def _apply_bold_ranges(self, oid, ranges):
        """_text_md 후 호출 — 지정 범위만 bold 적용."""
        for start, end in ranges:
            self.reqs.append({
                "updateTextStyle": {
                    "objectId": oid,
                    "style": {"bold": True},
                    "textRange": {"type": "FIXED_RANGE",
                                  "startIndex": start, "endIndex": end},
                    "fields": "bold",
                }
            })

    def _style(self, oid, size, bold=False, color=None, italic=False, align="START"):
        if color is None:
            color = self.c["fg"]
        # V5.7: 8pt 본문(non-bold)에 line spacing 1.5 자동 적용
        para_style = {"alignment": align}
        para_fields = "alignment"
        if size == 8 and not bold:
            para_style["lineSpacing"] = 150
            para_fields += ",lineSpacing"
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
                    "style": para_style,
                    "textRange": {"type": "ALL"},
                    "fields": para_fields,
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
        """표지: 템플릿 커버 슬라이드의 텍스트를 교체.

        V5.9: title + subtitle 합계 2줄 이내 강제.
              합계 3줄 이상이면 subtitle 자동 제거, title도 2줄 초과면 트림.
        """
        # V5.9 가드: title + subtitle 합계 2줄 이내
        title_lines = title.count("\n") + 1
        sub_lines = (subtitle.count("\n") + 1) if subtitle else 0
        total = title_lines + sub_lines
        if total > 2:
            print(f"[WARN] cover title+subtitle 합계 {total}줄 → 2줄 한도 초과, subtitle 자동 제거")
            subtitle = ""
            # title 자체가 2줄 초과면 마저 트림
            if title_lines > 2:
                parts = title.split("\n")
                print(f"[WARN] cover title {title_lines}줄 → 2줄로 트림")
                title = "\n".join(parts[:2])
        title_oid, meta_oid, date_oid = self._cover_oids
        title_text = f"{title}\n{subtitle}" if subtitle else title
        meta_text  = f"{dept}\n{name}"
        # V5.9: 표지 표준 폰트 사이즈 (light template 기준 — dark는 가이드 덱이라 14.5)
        # 일반 표지 표준: title 36 / meta 12 / date 12 (양 테마 통일)
        title_size = 36
        meta_size = 12
        entries = [
            (title_oid, title_text, title_size, True),
            (meta_oid,  meta_text,  meta_size,  False),
            (date_oid,  date,       meta_size,  False),
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

    def checklist(self, heading, items, eyebrow=""):
        """체크리스트 슬라이드: 헤더 + 항목 목록.

        V5.9: 헤더 생성을 _make_slide_with_header로 통일 — 좌표 일관성 자동 보장.

        Args:
            heading: 22pt 슬라이드 타이틀
            items: [(label, done), ...]
            eyebrow: 타이틀 위 8pt ORANGE 메타 (선택)
        """
        oid = self._make_slide_with_header(heading=heading, eyebrow=eyebrow)

        # V5.7: 콘텐츠 시작 y=100, 끝 y=373 (위·아래 32pt 빈 여백 대칭)
        content_y_start = 100
        content_y_end = 373  # 405 - 32 (eyebrow 시작과 대칭)
        n = max(len(items), 1)
        gap = 4
        # 마지막 항목 끝 y = start + (n-1)*(item_h+gap) + item_h <= end
        # → item_h <= (end - start - (n-1)*gap) / n
        max_item_h = (content_y_end - content_y_start - (n - 1) * gap) // n
        item_h = max(16, min(52, max_item_h))
        for i, (label, done) in enumerate(items):
            y = content_y_start + i * (item_h + 4)
            mark = _uid()
            self._shape(oid, mark, 40, y, 32, item_h)
            self._text(mark, "●" if done else "○")
            color = self.c["accent"] if done else self.c["dim"]
            # V5.8: 다른 페이지 본문 폰트 위계와 일관 (16→12)
            self._style(mark, 12, color=color, align="CENTER")

            txt = _uid()
            self._shape(oid, txt, 82, y, 598, item_h)
            self._text(txt, label)
            # V5.8: card title 위계(10.5)와 일관 (13→10.5)
            self._style(txt, 10.5, color=self.c["dim"] if done else self.c["fg"])

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

    # ── 빌딩 블록 (자유 레이아웃) ─────────────────────────────────
    # 시트 디자인을 "참고만" 하면서 콘텐츠 구조에 맞게 자유 조합.
    # mk_* 컴포넌트의 슬롯 강제를 우회하고 싶을 때 사용.

    def _rect(self, page_oid, x, y, w, h, fill, border, weight=0.5):
        """채움+테두리가 있는 사각형 한 개 그리기."""
        oid = _uid()
        self.reqs.append({
            "createShape": {
                "objectId": oid,
                "shapeType": "RECTANGLE",
                "elementProperties": {
                    "pageObjectId": page_oid,
                    "size": _size(w, h),
                    "transform": _transform(x, y),
                },
            }
        })
        self.reqs.append({
            "updateShapeProperties": {
                "objectId": oid,
                "shapeProperties": {
                    "shapeBackgroundFill": {"solidFill": {"color": _rgb(fill)}},
                    "outline": {
                        "outlineFill": {"solidFill": {"color": _rgb(border)}},
                        "weight": _pt(weight),
                    },
                },
                "fields": "shapeBackgroundFill,outline",
            }
        })
        return oid

    def _make_slide_with_header(self, heading="", eyebrow=""):
        """V5.9 단일 진입점 — 모든 슬라이드 생성의 공통 헤더 함수.

        모든 콘텐츠 슬라이드 메서드 (start_slide / checklist / conclusion 등)는
        이 함수를 호출해서 헤더 좌표·폰트·여백 일관성 자동 보장.

        좌표 토큰: spigen_tokens.HEADER 참조
        - eyebrow: y=32, h=10, 8pt bold ORANGE, valign=MIDDLE
        - title (with eyebrow): y=46, h=26, 22pt bold, valign=MIDDLE
        - title (only):         y=20, h=38, 22pt bold, valign=MIDDLE

        반환: 슬라이드 OID
        """
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)
        if eyebrow:
            eb = _uid()
            self._shape(oid, eb, 40, 32, 320, 10)
            self._text(eb, eyebrow)
            self._style(eb, 8, bold=True, color=self.c["accent"])
            if heading:
                h = _uid()
                self._shape(oid, h, 40, 46, 640, 26)
                self._text(h, heading)
                self._style(h, 22, bold=True)
        elif heading:
            h = _uid()
            self._shape(oid, h, 40, 20, 640, 38)
            self._text(h, heading)
            self._style(h, 22, bold=True)
        self._current_slide = oid
        return oid

    def start_slide(self, heading="", eyebrow=""):
        """자유 레이아웃 슬라이드 시작 — _make_slide_with_header 의 public 진입점.

        eyebrow: 타이틀 위 8pt bold ORANGE 메타 (선택)
        heading: 22pt bold 슬라이드 타이틀

        반환: 슬라이드 OID. 이후 빌딩 블록(card/flow_step/compare_pair 등) 자유 호출.
        """
        return self._make_slide_with_header(heading=heading, eyebrow=eyebrow)

    def card(self, x, y, w, h, title="", body="", label="", primary=False,
             emphasis=None, footer_label="", footer_body=""):
        """카드 블록 — 카드 높이에 따라 자동 모드 선택.

        - h >= 80 + (label/title/body 3섹션): 시트 표준 좌표
            label_y=16, title_y=39, body_y=79
        - h < 80 또는 단일/이중 섹션: 카드 가득 채워 vertical-center 배치

        폰트:
          - label: 8pt bold
          - title: 10.5pt bold
          - body: 8pt regular

        강조 (emphasis):
          - None / "normal" : surface fill + border (일반)
          - "dim"           : accent_bg + accent border (약한 강조, 기존 primary=True)
          - "full"          : accent 풀 ORANGE 배경 + 검정 텍스트 (강한 강조)

        primary=True 는 emphasis="dim" 호환 유지.
        """
        sid = getattr(self, "_current_slide", None)
        if sid is None:
            raise RuntimeError("card(): start_slide()를 먼저 호출하세요.")
        fg = self.c["fg"]
        # primary 호환
        if primary and emphasis is None:
            emphasis = "dim"
        if emphasis == "full":
            fill = self.c["accent"]
            border = self.c["accent"]
            border_w = 0.5
            label_color = {"red": 0, "green": 0, "blue": 0}
            title_color = {"red": 0, "green": 0, "blue": 0}
            body_color = {"red": 0.20, "green": 0.07, "blue": 0.02}
        elif emphasis == "dim":
            fill = self.c["accent_bg"]
            border = self.c["accent"]
            border_w = 0.5
            label_color = self.c["accent"]
            title_color = fg
            body_color = self.c["dim"]
        else:
            fill = self.c["surface"]
            border = self.c["border"]
            border_w = 0.4
            label_color = self.c["dim"]
            title_color = fg
            body_color = self.c["dim"]
        self._rect(sid, x, y, w, h, fill, border, border_w)
        pad_x = 18
        sections = [s for s in (label, title, body) if s]
        # 짧은 카드: 시트 표준이 안 맞음 → 카드 가득 채워 vertical-center
        if h < 80 or len(sections) == 1:
            if title:
                to = _uid()
                self._shape(sid, to, x + pad_x, y, w - pad_x * 2, h)
                br = self._text_md(to, title)
                self._style(to, 10.5, bold=True, color=title_color)
                self._apply_bold_ranges(to, br)
            elif body:
                bo = _uid()
                self._shape(sid, bo, x + pad_x, y, w - pad_x * 2, h)
                br = self._text_md(bo, body)
                self._style(bo, 8, color=body_color)
                self._apply_bold_ranges(bo, br)
            elif label:
                lo = _uid()
                self._shape(sid, lo, x + pad_x, y, w - pad_x * 2, h)
                self._text(lo, str(label).upper())
                self._style(lo, 8, bold=True, color=label_color)
            return
        # 시트 표준 좌표 (h>=80, 2섹션 이상)
        # footer 사용 시 본문 영역 줄임
        has_footer = bool(footer_label or footer_body)
        footer_h = 56 if has_footer else 0
        if label:
            lo = _uid()
            self._shape(sid, lo, x + pad_x, y + 16, w - pad_x * 2, 12)
            self._text(lo, str(label).upper())
            self._style(lo, 8, bold=True, color=label_color)
        if title:
            to = _uid()
            self._shape(sid, to, x + pad_x, y + 39, w - pad_x * 2, 28)
            br = self._text_md(to, title)
            self._style(to, 10.5, bold=True, color=title_color)
            self._apply_bold_ranges(to, br)
        if body:
            bo = _uid()
            body_y = y + 79 if (label or title) else y + 16
            body_h = max(16, h - (body_y - y) - 14 - footer_h)
            self._shape(sid, bo, x + pad_x, body_y, w - pad_x * 2, body_h)
            br = self._text_md(bo, body)
            self._style(bo, 8, color=body_color)
            self._apply_bold_ranges(bo, br)
        # footer 섹션 (divider + label + body)
        if has_footer:
            footer_y = y + h - footer_h - 8
            # divider
            self._hline(sid, x + pad_x, footer_y, w - pad_x * 2,
                        weight=0.5, color=self.c["dim"])
            if footer_label:
                flo = _uid()
                self._shape(sid, flo, x + pad_x, footer_y + 6,
                            w - pad_x * 2, 12)
                self._text(flo, str(footer_label).upper())
                self._style(flo, 8, bold=True, color=label_color)
            if footer_body:
                fbo = _uid()
                self._shape(sid, fbo, x + pad_x, footer_y + 22,
                            w - pad_x * 2, 24)
                br = self._text_md(fbo, footer_body)
                self._style(fbo, 10, bold=True, color=title_color)
                self._apply_bold_ranges(fbo, br)

    def flow_step(self, x, y, w, h, num, name, desc="", primary=False):
        """플로우 단계 1개 — mk_flow_focus 시트 표준 좌표 사용.

        시트 측정값:
          - padding_x=16, num_y=14, name_y=36, desc_y=62
          - num=10B (오렌지), name=14B, desc=10 (dim)
          - 일반: surface + border, primary: accent_bg + accent border
        """
        sid = getattr(self, "_current_slide", None)
        if sid is None:
            raise RuntimeError("flow_step(): start_slide()를 먼저 호출하세요.")
        if primary:
            fill = self.c["accent_bg"]
            border = self.c["accent"]
            border_w = 0.5
        else:
            fill = self.c["surface"]
            border = self.c["border"]
            border_w = 0.4
        self._rect(sid, x, y, w, h, fill, border, border_w)
        pad_x = 16
        no = _uid()
        self._shape(sid, no, x + pad_x, y + 14, w - pad_x * 2, 16)
        self._text(no, str(num))
        self._style(no, 10, bold=True, color=self.c["accent"])
        ne = _uid()
        self._shape(sid, ne, x + pad_x, y + 36, w - pad_x * 2, 22)
        self._text(ne, name)
        self._style(ne, 10.5, bold=True, color=self.c["fg"])
        if desc:
            de = _uid()
            self._shape(sid, de, x + pad_x, y + 62, w - pad_x * 2, max(16, h - 76))
            self._text(de, desc)
            self._style(de, 8, color=self.c["dim"])

    def compare_pair(self, y, item, before, after, h=44):
        """비교 행 1개 — mk_compare_rows 시트 비율(140:240:240) 사용.

        좌(item) | 중(before, surface) | 우(after, accent border).
        여러 번 호출하면 세로로 쌓임 (y 좌표를 각자 지정).
        h는 28pt 이상이어야 안전.
        """
        sid = getattr(self, "_current_slide", None)
        if sid is None:
            raise RuntimeError("compare_pair(): start_slide()를 먼저 호출하세요.")
        h = max(28, h)
        x0, total_w = 40, 640
        item_w, before_w, after_w = 140, 240, 240
        gap = (total_w - item_w - before_w - after_w) // 2  # = 10
        v_pad = min(8, max(2, (h - 16) // 2))
        text_h = max(12, h - v_pad * 2)
        # 항목 (좌)
        io = _uid()
        self._shape(sid, io, x0, y + v_pad, item_w, text_h)
        self._text(io, item)
        self._style(io, 10.5, bold=True, color=self.c["fg"])
        # before (중) — surface fill, border weight 0.4
        bx = x0 + item_w + gap
        self._rect(sid, bx, y, before_w, h, self.c["surface"], self.c["border"], 0.4)
        bo = _uid()
        self._shape(sid, bo, bx + 12, y + v_pad, before_w - 24, text_h)
        self._text(bo, before)
        self._style(bo, 8, color=self.c["dim"])
        # after (우, accent_bg + 오렌지 border 0.5)
        ax = bx + before_w + gap
        self._rect(sid, ax, y, after_w, h, self.c["accent_bg"], self.c["accent"], 0.5)
        ao = _uid()
        self._shape(sid, ao, ax + 12, y + v_pad, after_w - 24, text_h)
        self._text(ao, after)
        self._style(ao, 8, color=self.c["fg"])

    def callout(self, text, sub=""):
        """단일 슬라이드 = 강조 메시지. 큰 글씨로 한 문장 + 부연 설명."""
        oid, idx = self._next()
        self._slide(oid, idx)
        self._bg(oid)
        # 좌측 오렌지 세로 바
        self._vline(oid, 60, 130, 145, weight=4)
        # 본문
        to = _uid()
        self._shape(oid, to, 90, 140, 590, 60)
        self._text(to, text)
        self._style(to, 22, bold=True, color=self.c["fg"])
        if sub:
            so = _uid()
            self._shape(oid, so, 90, 210, 590, 50)
            self._text(so, sub)
            self._style(so, 8, color=self.c["dim"])
        self._current_slide = oid
        return oid

    def conclusion(self, metric, caption="", details=None, heading="", eyebrow=""):
        """결론 슬라이드 — mk_conclusion_detail 시트 양식 직접 재현.

        좌측: 큰 메트릭(56pt ORANGE) + 캡션(9pt dim)
        우측: 디테일 카드 4개 (라벨 + 본문 + sub-라벨)

        대부분의 덱은 결론 페이지가 필요 없다 — 명시적으로 호출할 때만 사용.

        Args:
            metric:   큰 글씨 — '96.4%' 또는 'QR 1종' 같은 핵심 메시지
            caption:  메트릭 아래 작은 한두 줄 설명 (**굵게** 마크업 가능)
            details:  [{"label": "관리", "body": "...", "sub": "선택사항"}, ...] 최대 4개
            heading:  슬라이드 타이틀 (선택)
            eyebrow:  타이틀 위 메타 (선택)
        """
        self.start_slide(heading=heading, eyebrow=eyebrow)
        sid = self._current_slide

        # 좌측 큰 메트릭 (56pt ORANGE bold)
        mo = _uid()
        self._shape(sid, mo, 36, 130, 290, 80)
        br = self._text_md(mo, metric)
        self._style(mo, 56, bold=True, color=self.c["accent"])
        self._apply_bold_ranges(mo, br)

        # 좌측 캡션 (V5.6 페르소나 합의: 9pt → 11pt 가독성 개선)
        if caption:
            co = _uid()
            self._shape(sid, co, 42, 215, 290, 50)
            br = self._text_md(co, caption)
            self._style(co, 11, color=self.c["dim"])
            self._apply_bold_ranges(co, br)

        # 우측 디테일 카드 4개 (시트 좌표: card 314×44, gap 8)
        # 시트 양식 좌우 2단 — 좌측 라벨, 우측 본문
        # 본문 박스 valign=MIDDLE 자동 적용으로 카드 안 세로 가운데
        for i, d in enumerate((details or [])[:4]):
            cy = 110 + i * (44 + 8)
            self._rect(sid, 370, cy, 314, 44,
                       self.c["surface"], self.c["border"], 0.4)
            # 좌측 라벨 (작은 ORANGE)
            if d.get("label"):
                lo = _uid()
                self._shape(sid, lo, 382, cy + 6, 80, 32)
                self._text(lo, str(d["label"]))
                self._style(lo, 8, bold=True, color=self.c["accent"])
            # 좌측 sub (라벨 아래 작은 dim) — 사용 시 라벨 위치 위로
            if d.get("sub"):
                so = _uid()
                self._shape(sid, so, 382, cy + 24, 80, 14)
                self._text(so, str(d["sub"]))
                self._style(so, 7, color=self.c["dim"])
            # 우측 본문 (메인 메시지) — 박스 h=32 카드 안 세로 가운데
            if d.get("body"):
                bo = _uid()
                self._shape(sid, bo, 470, cy + 6, 210, 32)
                br = self._text_md(bo, d["body"])
                self._style(bo, 9, color=self.c["fg"])
                self._apply_bold_ranges(bo, br)
        return sid

    def text(self, x, y, w, h, content, size=10.5, bold=False, color=None, align="START"):
        """자유 위치 텍스트박스 한 개. **굵게** 마크업 자동 인식.

        용도: 큰 헤더, 라벨, 자유 본문 등 카드/플로우 외 자유 배치 텍스트.
        """
        sid = getattr(self, "_current_slide", None)
        if sid is None:
            raise RuntimeError("text(): start_slide()를 먼저 호출하세요.")
        if color is None:
            color = self.c["fg"]
        oid = _uid()
        self._shape(sid, oid, x, y, w, h)
        br = self._text_md(oid, content)
        self._style(oid, size, bold=bold, color=color, align=align)
        self._apply_bold_ranges(oid, br)
        return oid

    def divider(self, x, y, w, orange=True):
        """수평 구분선. orange=True면 오렌지 헤더선 2pt, False면 dim 0.75pt (시트 표준)."""
        sid = getattr(self, "_current_slide", None)
        if sid is None:
            raise RuntimeError("divider(): start_slide()를 먼저 호출하세요.")
        if orange:
            self._hline(sid, x, y, w, weight=2, color=self.c["accent"])
        else:
            self._hline(sid, x, y, w, weight=0.75, color=self.c["dim"])

    # ── API 플러시 ────────────────────────────────────────────────

    def _validate(self):
        """V5.9 자동 검사 — flush 직전 reqs를 스캔해 룰 위반 검출.

        검사 항목:
          1. 콘텐츠 영역 초과 (y + h > 373, 캔버스 밖 또는 아래 32pt 여백 침범)
          2. 캔버스 우측 초과 (x + w > 720)
          3. 음수 좌표

        경고만 출력 (raise 안 함) — 빌드는 진행, 사용자가 결과로 판단.
        """
        warnings = []
        for r in self.reqs:
            create = r.get("createShape") or r.get("createLine")
            if not create:
                continue
            ep = create.get("elementProperties", {})
            tx = ep.get("transform", {})
            sz = ep.get("size", {})
            x = tx.get("translateX", 0) / 12700
            y = tx.get("translateY", 0) / 12700
            w = sz.get("width", {}).get("magnitude", 0) / 12700
            h = sz.get("height", {}).get("magnitude", 0) / 12700
            oid = create.get("objectId", "?")[:12]
            if x < 0 or y < 0:
                warnings.append(f"shape {oid}: 음수 좌표 (x={x:.0f}, y={y:.0f})")
            if x + w > 720:
                warnings.append(f"shape {oid}: 캔버스 우측 초과 (x+w={x+w:.0f} > 720)")
            if y + h > 405:
                warnings.append(f"shape {oid}: 캔버스 하단 초과 (y+h={y+h:.0f} > 405)")
            elif y + h > 373 + 0.5 and y < 373:  # 0.5 부동소수점 여유
                warnings.append(
                    f"shape {oid}: 콘텐츠 영역 침범 (y+h={y+h:.0f} > 373, 아래 32pt 여백 위반)"
                )
        if warnings:
            print(f"[V5.9 검사] 경고 {len(warnings)}개:")
            for w in warnings[:8]:
                print(f"  ⚠ {w}")
            if len(warnings) > 8:
                print(f"  ... +{len(warnings) - 8}개")
        return len(warnings)

    def flush(self):
        self._validate()
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
