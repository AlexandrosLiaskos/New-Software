"""Convenience helpers used by the curating agent (see AGENT.md)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.models import Entity, Video, SoftwareNews, JsonStore

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

videos = JsonStore(DATA / "videos.json")
news = JsonStore(DATA / "news.json")


def load_video(uid: str) -> Video | None:
    e = videos.by_uid(uid)
    return e if isinstance(e, Video) else None


def transcript_text(video: Video) -> str:
    if not video.transcript_path:
        return ""
    p = ROOT / video.transcript_path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def save_news(item: SoftwareNews) -> None:
    news.upsert(item)
    pretty = DATA / "news" / f"{item.uid}.json"
    pretty.parent.mkdir(parents=True, exist_ok=True)
    pretty.write_text(
        json.dumps(item.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def mark_video_analyzed(video: Video, news_uids: list[str], *,
                        no_software: bool = False) -> None:
    video.extracted_news_uids = news_uids
    video.analysis_status = "no_software_content" if no_software else "analyzed"
    videos.upsert(video)


def clear_pending() -> None:
    (DATA / "pending_analysis.json").write_text("[]", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
