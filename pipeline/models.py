"""OOP entity model for the New Software archive.

Every persisted record carries:
  __class__  : Python class name (acts as type discriminator)
  uid        : stable unique identifier
  created_at : ISO-8601 first-seen timestamp

Subclasses add their own fields. to_dict / from_dict round-trip
preserves the discriminator so a flat JSON list can be heterogeneous.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _uid(*parts: str) -> str:
    h = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()
    return h[:16]


@dataclass
class Entity:
    """Root of the OOP hierarchy. All persisted records derive from this."""

    uid: str
    created_at: str = field(default_factory=_now)

    REGISTRY: ClassVar[dict[str, type]] = {}

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        Entity.REGISTRY[cls.__name__] = cls

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["__class__"] = type(self).__name__
        return d

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Entity":
        cls_name = d.pop("__class__", "Entity")
        cls = Entity.REGISTRY.get(cls_name, Entity)
        accepted = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in accepted})


@dataclass
class Channel(Entity):
    handle: str = ""
    channel_id: str = ""
    title: str = ""

    @classmethod
    def make(cls, handle: str, channel_id: str, title: str = "") -> "Channel":
        return cls(uid=_uid("channel", channel_id), handle=handle,
                   channel_id=channel_id, title=title)


@dataclass
class Video(Entity):
    """Quicklook record for a YouTube video. Transcript stored separately."""

    video_id: str = ""
    channel_id: str = ""
    channel_handle: str = ""
    title: str = ""
    published: str = ""
    url: str = ""
    transcript_path: str = ""    # relative path under data/transcripts/
    analysis_status: str = "pending"   # pending | analyzed | failed | no_software_content
    extracted_news_uids: list[str] = field(default_factory=list)

    @classmethod
    def make(cls, video_id: str, **kw) -> "Video":
        return cls(
            uid=_uid("video", video_id),
            video_id=video_id,
            url=f"https://www.youtube.com/watch?v={video_id}",
            **kw,
        )


@dataclass
class SoftwareNews(Entity):
    """A single software news / update / release / repo, extracted from a video.

    research_status moves: pending -> researched | failed.
    """

    category: str = ""              # repo | release | news | tool | model | other
    title: str = ""
    summary: str = ""               # short summary from transcript context
    source_video_uid: str = ""
    source_video_id: str = ""
    source_channel_handle: str = ""
    timestamp_in_video: str = ""    # optional, mm:ss if known
    links: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    # Enrichment after web/gh research:
    research_status: str = "pending"
    research: dict[str, Any] = field(default_factory=dict)
    # research shape (free-form, but conventional keys):
    #   homepage, repo_url, stars, forks, license, language,
    #   description, latest_release, latest_release_date,
    #   web_findings: [{title,url,snippet}], notes

    research_date: str = ""

    @classmethod
    def make(cls, title: str, source_video_id: str, **kw) -> "SoftwareNews":
        return cls(
            uid=_uid("news", source_video_id, title),
            title=title,
            source_video_id=source_video_id,
            **kw,
        )


class JsonStore:
    """Tiny file-backed JSON list keyed by uid. Append-or-update semantics."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def all(self) -> list[Entity]:
        raw = json.loads(self.path.read_text(encoding="utf-8") or "[]")
        return [Entity.from_dict(dict(r)) for r in raw]

    def by_uid(self, uid: str) -> Entity | None:
        for e in self.all():
            if e.uid == uid:
                return e
        return None

    def has(self, uid: str) -> bool:
        return self.by_uid(uid) is not None

    def upsert(self, entity: Entity) -> None:
        items = self.all()
        replaced = False
        for i, e in enumerate(items):
            if e.uid == entity.uid:
                items[i] = entity
                replaced = True
                break
        if not replaced:
            items.append(entity)
        self.path.write_text(
            json.dumps([e.to_dict() for e in items], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
