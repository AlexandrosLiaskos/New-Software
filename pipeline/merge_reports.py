"""After all subagents finish, merge per-agent reports into videos.json
and rebuild news.json from per-uid files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import Entity, Video, JsonStore  # noqa: E402

DATA = ROOT / "data"


def main() -> None:
    # 1. Apply agent_reports to videos.json
    videos = JsonStore(DATA / "videos.json")
    reports_dir = DATA / "agent_reports"
    if reports_dir.exists():
        for fp in sorted(reports_dir.glob("*.json")):
            r = json.loads(fp.read_text(encoding="utf-8"))
            for vu in r.get("videos", []):
                v = videos.by_uid(vu["video_uid"])
                if isinstance(v, Video):
                    v.extracted_news_uids = list(vu.get("news_uids", []))
                    v.analysis_status = vu.get("status", "analyzed")
                    videos.upsert(v)
            print(f"[merge] {fp.name}: {len(r.get('videos', []))} video updates, {r.get('news_count', 0)} news")

    # 2. Rebuild news.json from per-uid files
    news_dir = DATA / "news"
    items: list[dict] = []
    for fp in sorted(news_dir.glob("*.json")):
        try:
            items.append(json.loads(fp.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  ! skip {fp.name}: {e}")
    items.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    (DATA / "news.json").write_text(
        json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[merge] news.json <- {len(items)} per-uid files")

    # 3. Clear pending queue
    (DATA / "pending_analysis.json").write_text("[]", encoding="utf-8")


if __name__ == "__main__":
    main()
