"""Rebuild data/news.json from data/news/*.json (the per-uid source of truth).

Used after parallel subagents have each written their own per-uid news files —
this reduces them into the flat index. Idempotent; safe to run any time.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import Entity, SoftwareNews, Video, JsonStore  # noqa: E402

DATA = ROOT / "data"


def main() -> None:
    files = sorted((DATA / "news").glob("*.json"))
    items: list[dict] = []
    for fp in files:
        try:
            items.append(json.loads(fp.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  ! skip {fp.name}: {e}")
    items.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    (DATA / "news.json").write_text(
        json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[rebuild] news.json <- {len(items)} per-uid files")


if __name__ == "__main__":
    main()
