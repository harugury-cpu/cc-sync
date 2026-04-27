"""
spigen_models.py — shared slide/component spec models.

Preview HTML and Google Slides API renderers should consume the same
component payloads. This module defines those shared contracts.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ComponentSpec:
    type: str
    props: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "ComponentSpec":
        return cls(type=str(raw.get("type", "")).strip(), props=dict(raw.get("props", {}) or {}))

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "props": dict(self.props)}


@dataclass
class SlideSpec:
    slide_id: str
    title: str
    components: List[ComponentSpec]
    eyebrow: str = ""
    label: str = ""
    page_no: Optional[int] = None
    audience: str = ""
    purpose: str = ""
    detail_mode: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "SlideSpec":
        components = [ComponentSpec.from_dict(item) for item in raw.get("components", [])]
        return cls(
            slide_id=str(raw.get("slide_id", "")).strip(),
            title=str(raw.get("title", "")).strip(),
            eyebrow=str(raw.get("eyebrow", "")).strip(),
            label=str(raw.get("label", "")).strip(),
            page_no=raw.get("page_no"),
            audience=str(raw.get("audience", "")).strip(),
            purpose=str(raw.get("purpose", "")).strip(),
            detail_mode=str(raw.get("detail_mode", "")).strip(),
            metadata=dict(raw.get("metadata", {}) or {}),
            components=components,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slide_id": self.slide_id,
            "title": self.title,
            "eyebrow": self.eyebrow,
            "label": self.label,
            "page_no": self.page_no,
            "audience": self.audience,
            "purpose": self.purpose,
            "detail_mode": self.detail_mode,
            "metadata": dict(self.metadata),
            "components": [component.to_dict() for component in self.components],
        }


@dataclass
class SelectionInput:
    content_type: str = ""
    item_count: int = 0
    has_comparison: bool = False
    is_process: bool = False
    has_status: bool = False
    is_bilateral: bool = False
    is_kpi: bool = False
    audience: str = ""
    purpose: str = ""
    detail_mode: str = ""
    diagram_kind: str = ""
    message_shape: str = ""

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "SelectionInput":
        return cls(
            content_type=str(raw.get("content_type", "")).strip(),
            item_count=int(raw.get("item_count", 0) or 0),
            has_comparison=bool(raw.get("has_comparison", False)),
            is_process=bool(raw.get("is_process", False)),
            has_status=bool(raw.get("has_status", False)),
            is_bilateral=bool(raw.get("is_bilateral", False)),
            is_kpi=bool(raw.get("is_kpi", False)),
            audience=str(raw.get("audience", "")).strip(),
            purpose=str(raw.get("purpose", "")).strip(),
            detail_mode=str(raw.get("detail_mode", "")).strip(),
            diagram_kind=str(raw.get("diagram_kind", "")).strip(),
            message_shape=str(raw.get("message_shape", "")).strip(),
        )


@dataclass
class SelectionResult:
    component_name: str
    function_name: str
    rationale: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "component_name": self.component_name,
            "function_name": self.function_name,
            "rationale": self.rationale,
        }
