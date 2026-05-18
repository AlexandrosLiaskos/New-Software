# New Software

A daily archive of software news, releases, repositories, and notable
incidents — distilled from a short list of YouTube channels, researched
on the web and GitHub, and filed for the record.

The site is generated as static HTML and published via GitHub Pages.
The data model is OOP-shaped JSON: every record carries a `__class__`
discriminator (`Channel`, `Video`, `SoftwareNews`) and is round-tripped
through small Python dataclasses in [`pipeline/models.py`](pipeline/models.py).

## How it works

```
                ┌──────────────────────────────────────┐
   YouTube RSS  │  pipeline/run_fetch.py               │  → data/videos.json
   ───────────► │  • discover new videos               │  → data/transcripts/
                │  • pull transcripts                  │  → data/pending_analysis.json
                └──────────────┬───────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────────────┐
   Claude       │  AGENT.md runbook                    │  → data/news.json
   (scheduled)  │  • extract SoftwareNews items        │  → data/news/<uid>.json
                │  • research via gh + web             │
                │  • mark video analysed               │
                └──────────────┬───────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────────────┐
                │  docs/build.py                       │  → docs/index.html
                │  • render editorial-classicism HTML  │  → docs/news/<uid>.html
                └──────────────┬───────────────────────┘
                               │
                               ▼
                       GitHub Pages
```

The Python steps are deterministic and pure. The judgment-heavy step
(turning a transcript into a clean list of researched news items) is
performed by a Claude agent following [AGENT.md](AGENT.md).

## Watched channels

- [@intheworldofai](https://www.youtube.com/@intheworldofai)
- [@ManuAGI](https://www.youtube.com/@ManuAGI)
- [@Fireship](https://www.youtube.com/@Fireship)

## Layout

```
data/
  channels.json              # watched channels
  videos.json                # quicklook DB of every video ever seen
  news.json                  # flat list of SoftwareNews records
  news/<uid>.json            # one pretty file per news item
  transcripts/<vid>.txt      # raw transcripts, timestamped
  pending_analysis.json      # queue of video uids awaiting analysis
pipeline/
  models.py                  # Entity / Channel / Video / SoftwareNews
  fetcher.py                 # YouTube RSS
  transcripts.py             # youtube-transcript-api wrapper
  curator_helpers.py         # convenience for the curating agent
  run_fetch.py               # discover videos + pull transcripts
  seed_initial.py            # one-shot backfill of the first wave
  enrich_initial.py          # one-shot research enrichment of the first wave
docs/
  build.py                   # static HTML generator
  styles.css                 # editorial classicism stylesheet
  index.html                 # generated archive view
  news/<uid>.html            # generated detail view
daily.py                     # the scheduled daily entrypoint
AGENT.md                     # runbook for the curating agent
```

## Style

The site follows editorial classicism: hairline rules, serif italic for
"voice", tracked uppercase for labels, monospace for measured values.
No rounded cards, no gradients, no shadows. See [`docs/styles.css`](docs/styles.css).
