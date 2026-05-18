"""Apply research enrichment to the seeded news items."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import SoftwareNews, Entity
from pipeline.curator_helpers import news as news_store, save_news, now_iso


# Indexed by title prefix (case-insensitive).
ENRICHMENT: list[tuple[str, dict]] = [
    ("Shai-Hulud npm worm", {
        "homepage": "https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html",
        "notes": "Compromised packages carry valid SLSA Build Level 3 provenance attestations — the first npm worm documented to produce validly-attested malicious packages. Attacker pwned a fork-triggered pull_request_target workflow, then extracted OIDC tokens from /proc/<pid>/mem of the GitHub Actions runner.",
        "web_findings": [
            {"title": "Mini Shai-Hulud Worm Compromises TanStack, Mistral AI, Guardrails AI & More Packages",
             "url": "https://thehackernews.com/2026/05/mini-shai-hulud-worm-compromises.html",
             "snippet": "84 npm artifacts across 42 @tanstack/* packages compromised on May 11 2026 by chaining GitHub Actions Pwn Request, cache poisoning and OIDC token exploitation."},
            {"title": "Our response to the TanStack npm supply chain attack — OpenAI",
             "url": "https://openai.com/index/our-response-to-the-tanstack-npm-supply-chain-attack/",
             "snippet": "OpenAI postmortem covering exposure surface and remediation."},
            {"title": "TanStack npm Packages Hit by Mini Shai-Hulud — Snyk",
             "url": "https://snyk.io/blog/tanstack-npm-packages-compromised/",
             "snippet": "Snyk's technical breakdown of the worm propagation mechanism."},
        ],
    }),
    ("pnpm 11 ships supply-chain", {
        "homepage": "https://pnpm.io/",
        "web_findings": [
            {"title": "pnpm — Fast, disk space efficient package manager",
             "url": "https://pnpm.io/",
             "snippet": "minimumReleaseAge, blockExoticSubdependencies and approved-builds are documented as defaults from v11."},
        ],
    }),
    ("Sentry ships Seer", {
        "homepage": "https://sentry.io/product/seer/",
        "notes": "Seer Agent launched April 28 2026; January 2026 update added local-development and code-review debugging plus flat unlimited pricing.",
        "web_findings": [
            {"title": "Sentry Launches Seer Agent — Sentry press release",
             "url": "https://sentry.io/about/press-releases/sentry-launches-seer-agent/",
             "snippet": "Investigate production problems in plain language; multi-player from Slack."},
            {"title": "Sentry's Seer Agent lets developers debug production issues in natural language — The New Stack",
             "url": "https://thenewstack.io/sentrys-seer-agent-debug/",
             "snippet": "Walks the dependency graph across services to identify root cause and draft fixes."},
            {"title": "Sentry Expands Seer AI Debugging Agent to Local Development and Code Review",
             "url": "https://sentry.io/about/press-releases/sentry-expands-seer-ai-debugging-agent/",
             "snippet": "PR-level defect analysis and background root-cause triage on incoming errors."},
        ],
    }),
    ("Musk v. Altman", {
        "homepage": "",
        "web_findings": [],
        "notes": "Trial heard in U.S. District Court for the Northern District of California (Oakland) before Judge Yvonne Gonzalez Rogers; advisory jury, USD 134 billion in claimed damages plus an unwinding of OpenAI's for-profit conversion.",
    }),
    ("Kernel open-sources", {
        "homepage": "https://www.kernel.sh/",
        "repo_url": "https://github.com/kernel/kernel-images",
        "license": "Apache-2.0",
        "notes": "Founded 2025 by Rafael Garcia and Catherine Jue (YC). Unikernel-per-browser architecture; reports <325 ms cold start vs 3–5 s for container-based equivalents.",
        "web_findings": [
            {"title": "Kernel: Browser infrastructure for web agents and automations",
             "url": "https://www.kernel.sh/",
             "snippet": "Sandboxed unikernel per browser; MP4 replay; Apache-2.0 infra and SDKs."},
            {"title": "kernel/kernel-images — GitHub",
             "url": "https://github.com/kernel/kernel-images",
             "snippet": "Browsers-as-a-service for automations and web agents."},
            {"title": "Kernel vs Browserbase — Kernel Blog",
             "url": "https://onkernel.com/blog/kernel-vs-browserbase",
             "snippet": "Reports 5.8× faster cold starts and 50–98% lower cost vs Browserbase."},
        ],
    }),
    ("Telegraf:", {
        "repo_url": "https://github.com/influxdata/telegraf",
        "homepage": "https://influxdata.com/telegraf",
        "stars": 17517, "forks": 5807,
        "language": "Go", "license": "MIT",
    }),
    ("n8n-mcp:", {
        "repo_url": "https://github.com/czlonkowski/n8n-mcp",
        "homepage": "https://www.n8n-mcp.com/",
        "stars": 21055, "forks": 3417,
        "language": "TypeScript", "license": "MIT",
        "notes": "MCP server for Claude Desktop / Claude Code / Windsurf / Cursor that lets these agents author n8n workflows.",
    }),
    ("Hysteria:", {
        "repo_url": "https://github.com/apernet/hysteria",
        "homepage": "https://v2.hysteria.network/",
        "stars": 21162, "forks": 2177,
        "language": "Go", "license": "MIT",
    }),
    ("Hermes Agent: autonomous", {
        "repo_url": "https://github.com/NousResearch/hermes-agent",
        "homepage": "https://hermes-agent.nousresearch.com",
        "stars": 155606, "forks": 24979,
        "language": "Python", "license": "MIT",
        "notes": "Nous Research's flagship self-evolving agent. Companion repos exist for plugins, function-calling, self-evolution and compression evaluation.",
    }),
    ("Hermes Agent 0.14.0", {
        "repo_url": "https://github.com/NousResearch/hermes-agent",
        "homepage": "https://hermes-agent.nousresearch.com",
        "stars": 155606, "forks": 24979,
        "language": "Python", "license": "MIT",
        "latest_release": "v2026.5.16 — Hermes Agent v0.14.0",
        "latest_release_date": "2026-05-16",
    }),
    ("Hermes proxy", {
        "repo_url": "https://github.com/NousResearch/hermes-agent",
        "notes": "Ships as part of Hermes Agent 0.14 — exposes a local OpenAI-compatible endpoint backed by the user's chat subscription.",
    }),
    ("Claude for Legal", {
        "repo_url": "https://github.com/anthropics/claude-cookbooks",
        "stars": 43216, "forks": 4904,
        "language": "Jupyter Notebook", "license": "MIT",
        "notes": "The host described this as 'Claude for Legal'; the closest first-party Anthropic surface for legal-workflow recipes is the public claude-cookbooks notebook collection. A dedicated 'claude-for-legal' repo could not be confirmed at research time.",
    }),
    ("Awesome AI Agents", {
        "repo_url": "https://github.com/e2b-dev/awesome-ai-agents",
        "homepage": "https://e2b.dev/docs",
        "stars": 27888, "forks": 2892,
        "license": "NOASSERTION",
    }),
    ("ds4:", {
        "repo_url": "https://github.com/antirez/ds4",
        "stars": 10522, "forks": 860,
        "language": "C", "license": "MIT",
        "notes": "The video summary mis-identifies the project: antirez/ds4 is in fact a local inference engine for DeepSeek 4 Flash (Metal and CUDA), not a generic data-structures library. Worth tracking on the strength of the author and the topic.",
    }),
    ("k3s:", {
        "repo_url": "https://github.com/k3s-io/k3s",
        "homepage": "https://k3s.io",
        "stars": 33033, "forks": 2661,
        "language": "Go", "license": "Apache-2.0",
    }),
    ("MTEB:", {
        "repo_url": "https://github.com/embeddings-benchmark/mteb",
        "homepage": "https://embeddings-benchmark.github.io/mteb/",
        "stars": 3265, "forks": 616,
        "language": "Python", "license": "Apache-2.0",
        "notes": "Video calls this 'MTV'; the canonical project is MTEB (Massive Text Embedding Benchmark).",
    }),
    ("Higgsfield Supercomputer", {
        "homepage": "https://higgsfield.ai/supercomputer-intro",
        "notes": "Launched 14 May 2026. Built on a custom Hermes 3 series from Nous Research, fine-tuned for agentic orchestration; routes across Claude Opus 4.7 / Sonnet 4.6, GPT-5.5 Pro and Gemini 3.1 Pro. Underlying video model is Seedance 2.0.",
        "web_findings": [
            {"title": "Higgsfield Supercomputer — Agentic AI Content Creation",
             "url": "https://higgsfield.ai/supercomputer-intro",
             "snippet": "Self-learning cloud-native agent for the full marketing creative process."},
            {"title": "Higgsfield AI Supercomputer — explainx.ai analysis",
             "url": "https://explainx.ai/blog/higgsfield-ai-supercomputer-hermes-agent-2026",
             "snippet": "Architecture overview; 40+ built-in tools, three layers of memory."},
        ],
    }),
    ("DeepSeek V4 Flash free", {
        "homepage": "https://portal.nousresearch.com/",
        "notes": "Hosted on Nous Research's portal with sponsorship from NVIDIA AI; available free for a limited window.",
    }),
    ("Mistral Vibe:", {
        "homepage": "https://mistral.ai/news/devstral-2-vibe-cli",
        "repo_url": "https://github.com/mistralai/mistral-vibe",
        "license": "Apache-2.0",
        "notes": "Launched late January 2026 alongside Devstral 2; in 2026 the model under the hood was swapped to Mistral Medium 3.5. ACP-compatible for IDE integration.",
        "web_findings": [
            {"title": "Introducing Devstral 2 and Mistral Vibe CLI — Mistral AI",
             "url": "https://mistral.ai/news/devstral-2-vibe-cli",
             "snippet": "Native CLI built for Devstral; explores, modifies, and executes changes across a codebase from natural language."},
            {"title": "mistralai/mistral-vibe — GitHub",
             "url": "https://github.com/mistralai/mistral-vibe",
             "snippet": "Minimal CLI coding agent by Mistral. Apache-2.0."},
            {"title": "Remote agents in Vibe — Mistral AI",
             "url": "https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5",
             "snippet": "Adds remote agents and swaps in Mistral Medium 3.5."},
        ],
    }),
]


def main() -> None:
    items = news_store.all()
    enriched = 0
    for it in items:
        if not isinstance(it, SoftwareNews):
            continue
        for prefix, data in ENRICHMENT:
            if it.title.lower().startswith(prefix.lower()):
                merged = dict(it.research or {})
                merged.update(data)
                it.research = merged
                it.research_status = "researched"
                it.research_date = now_iso()
                save_news(it)
                enriched += 1
                print(f"  ✓ {it.title[:70]}")
                break
        else:
            it.research_status = "transcript_only"
            save_news(it)
            print(f"  · {it.title[:70]}  (kept transcript-only)")
    print(f"\n[enrich] researched={enriched} / {sum(1 for i in items if isinstance(i, SoftwareNews))}")


if __name__ == "__main__":
    main()
