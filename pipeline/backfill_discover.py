"""Backfill discovery: list recent N videos per channel via yt-dlp.

yt-dlp's flat-playlist gives id+title (fast) without per-video page hits;
upload_date is NA in flat mode, so for accurate date filtering we fall back
to youtube-transcript-api timing later. For practical purposes, the N most
recent uploads from a channel cover ~3 months for the watched set.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import Channel, Video, JsonStore, Entity  # noqa: E402
from pipeline.transcripts import fetch_transcript  # noqa: E402

DATA = ROOT / "data"
TRANSCRIPTS = DATA / "transcripts"

PER_CHANNEL = 40


def load_channels() -> list[Channel]:
    raw = json.loads((DATA / "channels.json").read_text(encoding="utf-8"))
    return [Entity.from_dict(dict(r)) for r in raw]


def list_channel(handle: str, n: int) -> list[tuple[str, str]]:
    cmd = [
        "yt-dlp", "--flat-playlist",
        "--playlist-items", f"1:{n}",
        "--print", "%(id)s\t%(title)s",
        f"https://www.youtube.com/@{handle}/videos",
    ]
    p = subprocess.run(cmd, capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    out: list[tuple[str, str]] = []
    for line in text.splitlines():
        if "\t" not in line:
            continue
        vid, title = line.split("\t", 1)
        if vid and not vid.startswith("["):
            out.append((vid.strip(), title.strip()))
    return out


def main(per_channel: int = PER_CHANNEL) -> None:
    videos = JsonStore(DATA / "videos.json")
    pending: list[str] = []
    new_count = 0

    for ch in load_channels():
        print(f"\n[discover] {ch.handle} (top {per_channel})")
        entries = list_channel(ch.handle, per_channel)
        print(f"  yt-dlp returned {len(entries)} ids")

        for vid, title in entries:
            v_uid = Video.make(vid).uid
            existing = videos.by_uid(v_uid)
            if existing is not None:
                continue
            print(f"  + {vid}  {title[:70]}")
            tpath = fetch_transcript(vid, TRANSCRIPTS)
            v = Video.make(
                video_id=vid,
                channel_id=ch.channel_id,
                channel_handle=ch.handle,
                title=title,
                transcript_path=tpath,
            )
            v.analysis_status = "no_transcript" if not tpath else "pending"
            videos.upsert(v)
            new_count += 1
            if tpath:
                pending.append(v.uid)

    (DATA / "pending_analysis.json").write_text(
        json.dumps(pending, indent=2), encoding="utf-8"
    )
    print(f"\n[discover] new videos={new_count}  with-transcripts={len(pending)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else PER_CHANNEL)
