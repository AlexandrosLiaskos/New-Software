"""Build the static site from data/news.json + data/videos.json."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import Entity, SoftwareNews, Video  # noqa: E402

SITE = ROOT / "docs"
DATA = ROOT / "data"


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def load_news() -> list[SoftwareNews]:
    p = DATA / "news.json"
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding="utf-8") or "[]")
    out = []
    for r in raw:
        e = Entity.from_dict(dict(r))
        if isinstance(e, SoftwareNews):
            out.append(e)
    # newest first by created_at
    out.sort(key=lambda x: x.created_at, reverse=True)
    return out


def load_videos() -> dict[str, Video]:
    raw = json.loads((DATA / "videos.json").read_text(encoding="utf-8") or "[]")
    out: dict[str, Video] = {}
    for r in raw:
        e = Entity.from_dict(dict(r))
        if isinstance(e, Video):
            out[e.uid] = e
    return out


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&family=Italianno&display=swap" rel="stylesheet">
</head>
<body>
<div class="container">
{body}
<div class="footer">
  <div>New Software · curated daily from transcripts</div>
  <div class="sig">— ns</div>
</div>
</div>
</body>
</html>
"""


def render_index(items: list[SoftwareNews], videos: dict[str, Video]) -> str:
    today = datetime.now(timezone.utc).strftime("%d %B %Y")
    rows = []
    for it in items:
        v = videos.get(it.source_video_uid)
        ch = it.source_channel_handle or (v.channel_handle if v else "")
        date = (it.research_date or it.created_at)[:10]
        cat = (it.category or "news").upper()
        rows.append(f"""
<li class="news-row">
  <div class="cat">{esc(cat)}</div>
  <div>
    <div class="title"><a href="news/{esc(it.uid)}.html">{esc(it.title)}</a></div>
    <div class="summary">{esc(it.summary)}</div>
    <div class="summary" style="font-style:normal;font-family:var(--sans);font-size:11px;letter-spacing:0.12em;text-transform:uppercase;margin-top:8px;">via @{esc(ch)}</div>
  </div>
  <div class="date">{esc(date)}</div>
</li>""")

    list_html = "\n".join(rows) if rows else """
<div class="empty">No software news archived yet. The daily curator has not yet run.</div>
"""

    body = f"""
<div class="masthead">
  <div class="rule"></div>
  <div class="title">New <em>Software</em></div>
  <div class="rule"></div>
</div>
<div class="frontispiece">
  <div class="eyebrow">A Daily Archive · MMXXVI</div>
  <p class="lede">Software news, releases, repositories, and notable
  incidents — distilled each morning from a small circle of YouTube channels,
  researched, and filed for the record.</p>
  <div class="meta">
    <div><span class="label">Issue</span><span class="value">{esc(today)}</span></div>
    <div class="div"></div>
    <div><span class="label">Items archived</span><span class="value">{len(items):03d}</span></div>
    <div class="div"></div>
    <div><span class="label">Sources</span><span class="value">03 channels</span></div>
  </div>
  <div class="flourish">New Software</div>
</div>
<div class="section-head">
  <h2><em>The Archive</em></h2>
  <div class="rule"></div>
</div>
<ul class="news-list">
{list_html}
</ul>
"""
    return PAGE.format(title="New Software", css="styles.css", body=body)


def render_detail(it: SoftwareNews, videos: dict[str, Video]) -> str:
    v = videos.get(it.source_video_uid)
    r = it.research or {}

    def row(k: str, v_: str) -> str:
        if not v_:
            return ""
        return f"<tr><th>{esc(k)}</th><td>{v_}</td></tr>"

    def linkify(u: str) -> str:
        return f'<a href="{esc(u)}">{esc(u)}</a>' if u else ""

    spec_rows = [
        row("Category",     esc(it.category)),
        row("Source video", f'<a href="{esc(v.url) if v else ""}">{esc(v.title) if v else ""}</a>'),
        row("Source channel", f"@{esc(it.source_channel_handle)}"),
        row("Repository",   linkify(r.get("repo_url",""))),
        row("Homepage",     linkify(r.get("homepage",""))),
        row("Stars",        esc(str(r.get("stars","")))),
        row("Forks",        esc(str(r.get("forks","")))),
        row("Language",     esc(r.get("language",""))),
        row("License",      esc(r.get("license",""))),
        row("Latest release", esc(str(r.get("latest_release","")))),
        row("Released on",  esc(r.get("latest_release_date",""))),
        row("First seen",   esc(it.created_at[:10])),
        row("Researched",   esc(it.research_date[:10] if it.research_date else "")),
    ]
    spec = "\n".join(s for s in spec_rows if s)

    findings_items = []
    for f in r.get("web_findings", []) or []:
        findings_items.append(f"""
<div class="item">
  <div class="t"><a href="{esc(f.get('url',''))}">{esc(f.get('title',''))}</a></div>
  <div class="s">{esc(f.get('snippet',''))}</div>
  <div class="u">{esc(f.get('url',''))}</div>
</div>""")
    findings = ""
    if findings_items:
        findings = f"""
<div class="section-head">
  <h2><em>Findings</em></h2>
  <div class="rule"></div>
</div>
<div class="findings">{"".join(findings_items)}</div>
"""

    extra_links = ""
    if it.links:
        ll = "".join(f'<li>{linkify(u)}</li>' for u in it.links)
        extra_links = f'<div class="section-head"><h2><em>Mentioned</em></h2><div class="rule"></div></div><ul style="list-style:none;padding:0;font-family:var(--mono);font-size:13px;">{ll}</ul>'

    notes = ""
    if r.get("notes"):
        notes = f'<p class="summary" style="border:none;font-size:16px;">{esc(r["notes"])}</p>'

    tags = ""
    if it.tags:
        tags = '<div class="tags">' + " · ".join(esc(t) for t in it.tags) + "</div>"

    body = f"""
<a class="back" href="../index.html">← Back to archive</a>
<div class="detail">
  <div class="kicker">{esc((it.category or 'news').upper())} · @{esc(it.source_channel_handle)}</div>
  <h1>{esc(it.title)}</h1>
  <p class="summary">{esc(it.summary)}</p>
  {notes}
  <table class="spec">{spec}</table>
  {extra_links}
  {findings}
  {tags}
</div>
"""
    return PAGE.format(title=f"{it.title} — New Software", css="../styles.css", body=body)


def main() -> None:
    items = load_news()
    videos = load_videos()

    (SITE / "index.html").write_text(render_index(items, videos), encoding="utf-8")

    news_dir = SITE / "news"
    news_dir.mkdir(parents=True, exist_ok=True)
    # purge stale detail pages
    seen = {f"{it.uid}.html" for it in items}
    for p in news_dir.glob("*.html"):
        if p.name not in seen:
            p.unlink()
    for it in items:
        (news_dir / f"{it.uid}.html").write_text(
            render_detail(it, videos), encoding="utf-8"
        )

    print(f"[site] built {len(items)} items -> {SITE/'index.html'}")


if __name__ == "__main__":
    main()
