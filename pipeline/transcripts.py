"""Pull a transcript for a video and write it to data/transcripts/<video_id>.txt.

Uses youtube-transcript-api. Returns the relative transcript path on success
or empty string if no transcript is available.
"""

from __future__ import annotations

from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
)


def fetch_transcript(video_id: str, out_dir: Path) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{video_id}.txt"
    if out_file.exists() and out_file.stat().st_size > 0:
        return str(out_file.relative_to(out_dir.parent.parent))
    try:
        api = YouTubeTranscriptApi()
        ft = api.fetch(video_id, languages=["en", "en-US", "en-GB"])
        snippets = ft.snippets if hasattr(ft, "snippets") else list(ft)
        lines = []
        for s in snippets:
            t = int(getattr(s, "start", 0))
            mm, ss = divmod(t, 60)
            text = getattr(s, "text", "").replace("\n", " ").strip()
            if text:
                lines.append(f"[{mm:02d}:{ss:02d}] {text}")
        out_file.write_text("\n".join(lines), encoding="utf-8")
        return str(out_file.relative_to(out_dir.parent.parent))
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return ""
    except Exception as e:
        print(f"[transcript] {video_id}: {type(e).__name__}: {e}")
        return ""
