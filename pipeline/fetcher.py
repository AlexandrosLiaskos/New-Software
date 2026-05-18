"""Fetch new videos via YouTube channel RSS (no API key required).

Feed URL: https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxx
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt":   "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


@dataclass
class FeedEntry:
    video_id: str
    title: str
    published: str
    channel_id: str
    channel_handle: str


def fetch_feed(channel_id: str, channel_handle: str = "") -> list[FeedEntry]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (NewSoftwareBot)"}, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    out: list[FeedEntry] = []
    for e in root.findall("atom:entry", NS):
        vid = e.find("yt:videoId", NS)
        title = e.find("atom:title", NS)
        published = e.find("atom:published", NS)
        if vid is None or title is None:
            continue
        out.append(FeedEntry(
            video_id=vid.text or "",
            title=(title.text or "").strip(),
            published=(published.text if published is not None else "") or "",
            channel_id=channel_id,
            channel_handle=channel_handle,
        ))
    return out
