"""Parallel-safe writer used by curator subagents.

Each subagent imports this and uses:
    aw = AgentWriter(agent_id="batch-3")
    aw.save_news(item)                 # writes ONLY data/news/<uid>.json
    aw.record_video(video_uid, news_uids=[...], status="analyzed")
    aw.finalise()                      # flushes data/agent_reports/<agent_id>.json

No subagent ever touches data/news.json or data/videos.json — the parent
process reduces the per-uid files and per-agent reports after all subagents
return. This avoids races on the shared index files.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipeline.models import SoftwareNews

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class AgentWriter:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.video_updates: list[dict[str, Any]] = []
        self.news_count = 0
        (DATA / "news").mkdir(parents=True, exist_ok=True)
        (DATA / "agent_reports").mkdir(parents=True, exist_ok=True)

    def save_news(self, item: SoftwareNews) -> None:
        p = DATA / "news" / f"{item.uid}.json"
        p.write_text(
            json.dumps(item.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        self.news_count += 1

    def record_video(
        self,
        video_uid: str,
        news_uids: list[str],
        status: str = "analyzed",
    ) -> None:
        self.video_updates.append({
            "video_uid": video_uid,
            "news_uids": news_uids,
            "status": status,
        })

    def finalise(self) -> str:
        report = {
            "agent_id": self.agent_id,
            "finished_at": now_iso(),
            "news_count": self.news_count,
            "videos": self.video_updates,
        }
        path = DATA / "agent_reports" / f"{self.agent_id}.json"
        path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return str(path)
