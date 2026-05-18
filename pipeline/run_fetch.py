"""Daily fetch step: discover new videos and pull their transcripts.

Reads  data/channels.json
Writes data/videos.json  (quicklook DB of all known videos)
Writes data/transcripts/<video_id>.txt
Writes data/pending_analysis.json (list of video uids awaiting analysis)

Designed to be IDEMPOTENT - safe to run repeatedly.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import Channel, Video, JsonStore, Entity  # noqa: E402
from pipeline.fetcher import fetch_feed  # noqa: E402
from pipeline.transcripts import fetch_transcript  # noqa: E402


DATA = ROOT / "data"
TRANSCRIPTS = DATA / "transcripts"


def load_channels() -> list[Channel]:
    raw = json.loads((DATA / "channels.json").read_text(encoding="utf-8"))
    return [Entity.from_dict(dict(r)) for r in raw]


def main(limit_per_channel: int = 5) -> None:
    videos = JsonStore(DATA / "videos.json")
    pending: list[str] = []
    new_count = 0

    for ch in load_channels():
        print(f"[fetch] {ch.handle} ({ch.channel_id})")
        try:
            entries = fetch_feed(ch.channel_id, ch.handle)
        except Exception as e:
            print(f"  feed error: {e}")
            continue

        for entry in entries[:limit_per_channel]:
            v_uid = Video.make(entry.video_id).uid
            if videos.has(v_uid):
                continue
            print(f"  new: {entry.video_id}  {entry.title[:70]}")
            tpath = fetch_transcript(entry.video_id, TRANSCRIPTS)
            v = Video.make(
                video_id=entry.video_id,
                channel_id=entry.channel_id,
                channel_handle=entry.channel_handle,
                title=entry.title,
                published=entry.published,
                transcript_path=tpath,
            )
            if not tpath:
                v.analysis_status = "no_transcript"
            videos.upsert(v)
            new_count += 1
            if tpath:
                pending.append(v.uid)

    (DATA / "pending_analysis.json").write_text(
        json.dumps(pending, indent=2), encoding="utf-8"
    )
    print(f"[fetch] done. new={new_count}  pending_analysis={len(pending)}")


if __name__ == "__main__":
    main()
