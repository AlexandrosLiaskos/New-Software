# New Software — Daily Agent Runbook

You are the daily curator of the **New Software** archive. Your job is to turn
fresh YouTube transcripts into a clean, researched, archived index of software
news, releases, repos, and tools.

## Pipeline (run in order)

### 1. Fetch new videos
```
python pipeline/run_fetch.py
```
This idempotently discovers new videos on the watched channels, downloads
transcripts to `data/transcripts/<video_id>.txt`, updates `data/videos.json`,
and writes the queue `data/pending_analysis.json` (list of video uids).

### 2. Analyse each pending video
For every uid in `data/pending_analysis.json`:

1. Look it up in `data/videos.json` to get its `video_id`, `title`, `channel_handle`, `transcript_path`.
2. Read the transcript file.
3. Extract a list of **software news items**. An item is anything concretely
   about software: a GitHub repo, a model release, a CLI tool, a vulnerability,
   a framework update, a product launch, a noteworthy bug or incident. Skip
   pure opinion, motivational content, sponsor reads, channel chatter.

   For each item, draft a `SoftwareNews` record with:
   - `title`           : crisp imperative phrase (≤ 70 chars)
   - `category`        : `repo` | `release` | `news` | `tool` | `model` | `vuln` | `other`
   - `summary`         : 1–3 sentence neutral summary derived from transcript
   - `links`           : any URLs the host mentions verbatim
   - `tags`            : 2–6 lower-case kebab-case tags
   - `timestamp_in_video`: `mm:ss` if extractable
   - `source_video_id` : the video's id (used to derive uid)
   - `source_video_uid`: the video record's uid
   - `source_channel_handle`: the channel handle

4. **Research each item.** For each `SoftwareNews`:
   - If the item is a GitHub repo (or you can find one), call
     `gh api repos/{owner}/{name}` to populate `research.repo_url`,
     `stars`, `forks`, `language`, `license`, `description`,
     `latest_release`, `latest_release_date`.
   - Otherwise (news, model, tool) use `WebSearch` + `WebFetch` to gather
     a homepage URL, a short description, and 1–3 corroborating web findings
     (`title`, `url`, `snippet`) into `research.web_findings`.
   - Set `research_status = "researched"`, `research_date = <iso8601>`.
   - On failure set `research_status = "failed"` with a `notes` reason.

5. Append the record to `data/news.json` (use `JsonStore.upsert`). Also write
   the per-uid pretty file `data/news/<uid>.json`.

6. Update the source `Video`'s `extracted_news_uids` and set
   `analysis_status = "analyzed"` (or `no_software_content` if nothing useful).

7. When done with every pending video, **empty** `data/pending_analysis.json`
   (`[]`).

Helper: see `pipeline/curator_helpers.py` for `load_video()`, `save_news()`,
`mark_video_analyzed()` — use them instead of hand-editing JSON.

### 3. Rebuild the site
```
python docs/build.py
```
Regenerates `docs/index.html` and `docs/news/<uid>.html` from the JSON store.

### 4. Commit and push
```
git add -A
git commit -m "daily: <N> new videos, <M> new software items"
git push
```
GitHub Pages will redeploy automatically.

## Conventions

- **OOP JSON convention.** Every record carries `__class__` (`Channel`,
  `Video`, `SoftwareNews`). Construct via `Entity.from_dict` /
  `entity.to_dict`. Never invent the discriminator by hand.
- **UID stability.** UIDs come from `models._uid(...)`. Same inputs ⇒ same
  uid, so re-running the pipeline never duplicates a record.
- **Style.** The site follows editorial classicism: hairline rules,
  serif italic for "voice", tracked uppercase eyebrows, monospace for
  measured values, no rounded SaaS cards, no gradients, no shadows.
- **Brevity.** News summaries are descriptive, not promotional. No emoji.
  No "🚀 amazing new release". Cite the channel as the source, the repo or
  homepage as the artifact.
