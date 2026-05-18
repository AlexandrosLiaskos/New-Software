"""One-shot extraction of software news items from the initial 6 transcripts.

This is the seed/backfill script. After this runs, the curator agent (see
AGENT.md) takes over and does extraction + research live, one video at a time.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.models import SoftwareNews, Entity, Video, JsonStore
from pipeline.curator_helpers import (
    save_news, mark_video_analyzed, clear_pending, videos as videos_store
)


def vuid(video_id: str) -> str:
    return Video.make(video_id).uid


ITEMS: list[dict] = [
    # ============================================================
    # Fireship — npm Shai-Hulud worm (gwTQLZSIlsU)
    # ============================================================
    dict(
        video_id="gwTQLZSIlsU", channel_handle="Fireship",
        title="Shai-Hulud npm worm compromises 169 packages",
        category="vuln",
        summary="A self-propagating supply-chain worm slipped through npm Trusted Publishing by abusing GitHub Actions pull_request_target on TanStack, then spread via stolen tokens to packages at Mistral AI, UiPath, OpenSearch, and Guardrails AI; security firm Aikido tracked 373 poisoned versions across 169 packages.",
        tags=["npm", "supply-chain", "security", "github-actions"],
        links=["https://www.aikido.dev/"],
    ),
    dict(
        video_id="gwTQLZSIlsU", channel_handle="Fireship",
        title="pnpm 11 ships supply-chain mitigations by default",
        category="release",
        summary="pnpm 11 enables three defaults that block this class of attack: minimumReleaseAge refuses packages younger than 24 hours, blockExoticSubdependencies refuses non-registry transitive deps, and approvedBuilds disables install scripts unless whitelisted.",
        tags=["pnpm", "package-manager", "security"],
        links=["https://pnpm.io/"],
    ),
    dict(
        video_id="gwTQLZSIlsU", channel_handle="Fireship",
        title="Sentry ships Seer agent for production debugging",
        category="release",
        summary="Sentry launched Seer, an AI agent that investigates production errors by pulling traces, spans, logs, and replays from existing Sentry data, walking upstream across services to identify root cause, and drafting fixes as pull requests. Open beta.",
        tags=["observability", "ai-agent", "sentry"],
        links=["https://sentry.io/"],
    ),

    # ============================================================
    # Fireship — Musk vs Altman closing arguments (3tbB2dffx0s)
    # ============================================================
    dict(
        video_id="3tbB2dffx0s", channel_handle="Fireship",
        title="Musk v. Altman closing arguments begin in Oakland",
        category="news",
        summary="Closing arguments opened in Elon Musk's USD 134 billion suit against Sam Altman, OpenAI and Microsoft, alleging breach of charitable trust in the for-profit conversion. Trial discovery surfaced internal emails and Brockman testimony; the case is heard before Judge Yvonne Gonzalez Rogers with an advisory jury.",
        tags=["openai", "litigation", "ai-industry"],
        links=[],
    ),
    dict(
        video_id="3tbB2dffx0s", channel_handle="Fireship",
        title="Kernel open-sources GPU-accelerated browser sandbox for agents",
        category="tool",
        summary="Kernel provides open-source browser infrastructure that spins up sandboxed Chromium instances in under 30 ms on GPU-accelerated hardware, aimed at AI agent workloads. Includes session replay for debugging; in production at Framer and Cash App, billed only when active.",
        tags=["ai-agent", "browser", "infrastructure", "open-source"],
        links=["https://onkernel.com/"],
    ),

    # ============================================================
    # ManuAGI — Top 20 GitHub Projects (CtxB7U0EVhg)
    # ============================================================
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="scientific-agent-skills: reusable skills for scientific AI agents",
        category="repo",
        summary="Open-source collection of structured prompts, tool interactions, and domain-specific actions for scientific AI agents; integrates as a capability layer into assistant systems and research pipelines.",
        tags=["ai-agent", "skills", "research"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Telegraf: plugin-driven metrics collection agent",
        category="repo",
        summary="InfluxData's open-source agent for collecting metrics, logs, and events through a large plugin ecosystem, forwarding to time-series databases and observability platforms.",
        tags=["observability", "metrics", "go"],
        links=["https://github.com/influxdata/telegraf"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="n8n-mcp: Model Context Protocol layer for n8n workflows",
        category="repo",
        summary="Bridges n8n automation workflows with MCP, letting AI agents and external tools invoke n8n workflows through structured context and execution interfaces.",
        tags=["mcp", "n8n", "automation", "ai-agent"],
        links=["https://github.com/czlonkowski/n8n-mcp"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="DeepSeek TUI: terminal interface for DeepSeek models",
        category="repo",
        summary="Text-based terminal application for interacting with DeepSeek language models — running prompts, managing conversations, and accessing workflows from the command line.",
        tags=["llm", "cli", "deepseek"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Hysteria: high-performance proxy and tunneling protocol",
        category="repo",
        summary="Open-source proxy and tunneling system using modern transport protocols to improve latency and throughput across unstable or restricted networks.",
        tags=["networking", "proxy", "tunneling"],
        links=["https://github.com/apernet/hysteria"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Hermes Agent: autonomous framework for tool-using AI agents",
        category="repo",
        summary="Framework from Nous Research that combines language models with memory, APIs, file operations, and iterative execution loops to drive multi-step autonomous workflows.",
        tags=["ai-agent", "nous-research", "framework"],
        links=["https://github.com/NousResearch/hermes"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="OpenSRE: AI-assisted platform for SRE workflows",
        category="repo",
        summary="Open-source SRE platform combining observability, diagnostics, and operational tooling with AI assistance for incident response and reliability automation.",
        tags=["sre", "observability", "ai-assisted"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Rufflow: structured workflow manager for AI outputs",
        category="repo",
        summary="Organises and transforms AI-generated outputs into structured workflows; targets consistency and repeatability across automation pipelines.",
        tags=["ai-workflow", "automation"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Claude for Legal: legal workflow patterns from Anthropic",
        category="repo",
        summary="Anthropic's open collection of example prompts, reasoning patterns, and structured workflows demonstrating Claude in document review, drafting, and legal analysis with human-in-the-loop review.",
        tags=["claude", "anthropic", "legal", "skills"],
        links=["https://github.com/anthropics/claude-cookbooks"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="Awesome AI Agents: curated directory of agent frameworks",
        category="repo",
        summary="Curated index of AI-agent frameworks, multi-agent systems, orchestration tools, and autonomous-workflow projects — a discovery hub for comparing approaches.",
        tags=["ai-agent", "awesome-list", "discovery"],
        links=["https://github.com/e2b-dev/awesome-ai-agents"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="ds4: compact systems-programming data structures in C (antirez)",
        category="repo",
        summary="Antonio (antirez) Sanfilippo's compact C library of efficient data structures for systems programming; targets memory and runtime efficiency in low-level applications.",
        tags=["c", "data-structures", "antirez", "systems"],
        links=["https://github.com/antirez/ds4"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="k3s: lightweight Kubernetes for edge and local clusters",
        category="repo",
        summary="Production Kubernetes distribution packaged into a smaller, easier-to-manage runtime; designed for edge, IoT, CI, and resource-constrained environments while remaining upstream-compatible.",
        tags=["kubernetes", "edge", "infrastructure"],
        links=["https://github.com/k3s-io/k3s"],
    ),
    dict(
        video_id="CtxB7U0EVhg", channel_handle="ManuAGI",
        title="MTEB: benchmark suite for embedding models",
        category="repo",
        summary="Massive Text Embedding Benchmark — datasets, evaluation pipelines, and standardised metrics for comparing retrieval, classification, and semantic similarity across embedding models.",
        tags=["embeddings", "benchmark", "evaluation"],
        links=["https://github.com/embeddings-benchmark/mteb"],
    ),

    # ============================================================
    # ManuAGI — Higgsfield Supercomputer (GZUQoSf7GR0)
    # ============================================================
    dict(
        video_id="GZUQoSf7GR0", channel_handle="ManuAGI",
        title="Higgsfield Supercomputer: agentic product+distribution workflow",
        category="tool",
        summary="Higgsfield AI's Supercomputer combines research, branding, landing-page generation, launch video, and ad variations into one agentic chat — positioned as an end-to-end go-to-market workflow rather than an isolated video generator.",
        tags=["ai-agent", "video", "marketing", "higgsfield"],
        links=["https://higgsfield.ai/"],
    ),

    # ============================================================
    # ManuAGI — Hermes Agent 0.14.0 foundation update (uZIijUyMT20)
    # ============================================================
    dict(
        video_id="uZIijUyMT20", channel_handle="ManuAGI",
        title="Hermes Agent 0.14.0 — Foundation release",
        category="release",
        summary="Nous Research's Hermes Agent ships its 'Foundation' release: native Windows beta, ~19 s faster cold start, persistent Chrome DevTools Protocol connection (some browser flows up to 180x faster), 1-hour cross-session prompt cache, native video generation, and a /handoff command for transferring live sessions across models without losing context.",
        tags=["nous-research", "ai-agent", "windows", "release"],
        links=["https://github.com/NousResearch/hermes"],
    ),
    dict(
        video_id="uZIijUyMT20", channel_handle="ManuAGI",
        title="Hermes proxy: route one subscription across coding agents",
        category="release",
        summary="A local OpenAI-compatible proxy in Hermes 0.14 lets a single Claude/ChatGPT/Grok subscription drive any compatible coding agent without separate API keys — runs as a local host endpoint authenticated by the user's existing plan.",
        tags=["proxy", "openai-compatible", "nous-research"],
    ),
    dict(
        video_id="uZIijUyMT20", channel_handle="ManuAGI",
        title="DeepSeek V4 Flash free on the Nous portal (limited time)",
        category="model",
        summary="DeepSeek V4 Flash is available free for a limited window on the Nous Research portal, courtesy of NVIDIA AI — usable for coding, reasoning, and long-context autonomous workflows.",
        tags=["deepseek", "model", "nvidia", "free-tier"],
        links=["https://portal.nousresearch.com/"],
    ),

    # ============================================================
    # ManuAGI — Mistral Vibe CLI (WxjviB1pJbk)
    # ============================================================
    dict(
        video_id="WxjviB1pJbk", channel_handle="ManuAGI",
        title="Mistral Vibe: open-source terminal coding agent",
        category="release",
        summary="Mistral's open-source terminal-native coding agent — async tasks, sub-agents, slash-command skills, multi-choice clarification, IDE plugins (VS Code, JetBrains), bring-your-own-key, and a paid tier on Le Chat Pro at USD 14.99/month with student discount. Powered by Devstral, Codestral, and Codestral Embed.",
        tags=["mistral", "cli", "coding-agent", "open-source"],
        links=["https://mistral.ai/", "https://chat.mistral.ai/"],
    ),
]


def main() -> None:
    by_video: dict[str, list[str]] = {}
    for raw in ITEMS:
        vid = raw["video_id"]
        v_uid = vuid(vid)
        item = SoftwareNews.make(
            title=raw["title"],
            source_video_id=vid,
            category=raw.get("category", "news"),
            summary=raw.get("summary", ""),
            source_video_uid=v_uid,
            source_channel_handle=raw.get("channel_handle", ""),
            links=raw.get("links", []),
            tags=raw.get("tags", []),
            timestamp_in_video=raw.get("timestamp_in_video", ""),
        )
        save_news(item)
        by_video.setdefault(v_uid, []).append(item.uid)
        print(f"  + {item.category:8s} {item.title[:70]}")

    for v_uid, news_uids in by_video.items():
        v = videos_store.by_uid(v_uid)
        if isinstance(v, Video):
            mark_video_analyzed(v, news_uids)

    clear_pending()
    print(f"\n[seed] saved {len(ITEMS)} items across {len(by_video)} videos")


if __name__ == "__main__":
    main()
