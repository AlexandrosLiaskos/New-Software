"""Curator batch-1 runner."""
import sys
sys.path.insert(0, r"C:\Users\alexl\Archive\TEMP\new-software")

from pipeline.models import SoftwareNews
from pipeline.agent_writer import AgentWriter, now_iso

aw = AgentWriter("batch-1")

CH = "intheworldofai"


def save(item, status="researched"):
    item.research_status = status
    item.research_date = now_iso()
    aw.save_news(item)
    return item


# ---------------------------------------------------------------
# Video 1: oekV5AQGRCY  — Gemini 3.5 Flash + Pro leak
# ---------------------------------------------------------------
v1_id = "oekV5AQGRCY"
v1_uid = "f9ae3741ae735fcf"
v1_items = []

n = SoftwareNews.make(
    title="Gemini 3.5 Pro checkpoint 'Cappuccino' surfaces ahead of Google I/O",
    source_video_id=v1_id,
    source_video_uid=v1_uid,
    source_channel_handle=CH,
    category="model",
    summary="A new Gemini 3.5 Pro checkpoint, internally referred to as 'Cappuccino', appears in arena testing ahead of Google I/O. The host reports notably stronger code generation, including a working Minecraft clone with mobs, health bar and creative mode.",
    timestamp_in_video="00:55",
    tags=["gemini", "google", "model-release", "frontier"],
    links=["https://io.google/2026/"],
)
n.research = {
    "homepage": "https://io.google/2026/",
    "notes": "Reported as a pre-IO checkpoint. The follow-up news cycle showed Google preparing Gemini 3.2 Flash for I/O on May 19-20 2026; the 'Cappuccino' codename is documented only in community reporting at this stage.",
    "web_findings": [
        {"title": "Google I/O 2026: Gemini Spark, Omni AI Video & Gemini 3.5 Rumors", "url": "https://nokiapoweruser.com/google-io-2026-gemini-spark-omni-gemini-3-5-rumors/", "snippet": "Reports point to a more capable Gemini 3.5 Pro model focused on advanced reasoning and coding tasks."},
        {"title": "Google prepares new upgrades for Gemini Flash model", "url": "https://www.testingcatalog.com/google-prepares-new-upgrades-for-gemini-flash-model/", "snippet": "New Gemini 3.5 Flash and Pro checkpoints appeared ahead of Google I/O 2026."},
    ],
}
v1_items.append(save(n))

n = SoftwareNews.make(
    title="Gemini 3.5 Flash checkpoint tested in LM Arena",
    source_video_id=v1_id,
    source_video_uid=v1_uid,
    source_channel_handle=CH,
    category="model",
    summary="A Gemini Flash-tier checkpoint, labelled 'Gemini 3.0 flash' inside the LM Arena but reported as Gemini 3.5 Flash, shows reasoning and front-end generation closer to Claude Opus 4.7 and Gemini 3.1 Pro. Pricing leaks elsewhere put it at $0.25/1M input and $2.00/1M output tokens.",
    timestamp_in_video="02:26",
    tags=["gemini", "google", "model-release", "flash"],
    links=["https://lmarena.ai/"],
)
n.research = {
    "homepage": "https://deepmind.google/technologies/gemini/",
    "notes": "Closely related to the Gemini 3.2 Flash leak documented by TestingCatalog; the host conflates the 3.2 and 3.5 naming because Google was rapidly renaming checkpoints in arena.",
    "web_findings": [
        {"title": "Gemini 3.2 Flash quietly leaks ahead of Google I/O 2026", "url": "https://www.testingcatalog.com/google-prepares-new-upgrades-for-gemini-flash-model/", "snippet": "Gemini 3.2 Flash priced at $0.25 per million input tokens and $2.00 per million output tokens, matching much of Gemini 3.1 Pro's capability."},
    ],
}
v1_items.append(save(n))

aw.record_video(v1_uid, [i.uid for i in v1_items], status="analyzed")


# ---------------------------------------------------------------
# Video 2: dLk2Imx-0uk  — Hermes Agentic OS (Hermes + AionUI)
# ---------------------------------------------------------------
v2_id = "dLk2Imx-0uk"
v2_uid = "459e150ef430cf52"
v2_items = []

n = SoftwareNews.make(
    title="Hermes Agent: self-improving autonomous agent from Nous Research",
    source_video_id=v2_id,
    source_video_uid=v2_uid,
    source_channel_handle=CH,
    category="repo",
    summary="Hermes Agent is an open-source persistent autonomous agent from Nous Research, designed to run continuously on the user's infrastructure while building long-term memory and reusable skills. Released under the MIT license.",
    timestamp_in_video="00:08",
    tags=["hermes-agent", "nous-research", "agent", "open-source"],
    links=["https://github.com/NousResearch/hermes-agent", "https://hermes-agent.nousresearch.com"],
)
n.research = {
    "repo_url": "https://github.com/NousResearch/hermes-agent",
    "homepage": "https://hermes-agent.nousresearch.com",
    "stars": 155627,
    "forks": 24984,
    "language": "Python",
    "license": "MIT",
    "description": "The agent that grows with you",
    "notes": "Multi-platform (Telegram, Discord, Slack, WhatsApp, Email, CLI), with five execution backends (local, Docker, SSH, Singularity, Modal).",
}
v2_items.append(save(n))

n = SoftwareNews.make(
    title="AionUi: open-source Cowork desktop app for 20+ AI CLIs",
    source_video_id=v2_id,
    source_video_uid=v2_uid,
    source_channel_handle=CH,
    category="tool",
    summary="AionUi (referred to in the video as 'ION UI') is a free, local, open-source Cowork desktop application that hosts AI agents such as Hermes Agent, Claude Code, Codex, Gemini CLI and others. It auto-detects locally installed CLIs and stores all data in a local SQLite database.",
    timestamp_in_video="01:48",
    tags=["aionui", "cowork", "agent", "open-source", "desktop"],
    links=["https://github.com/iOfficeAI/AionUi", "https://www.aionui.com"],
)
n.research = {
    "repo_url": "https://github.com/iOfficeAI/AionUi",
    "homepage": "https://www.aionui.com",
    "stars": 25531,
    "forks": 2341,
    "language": "TypeScript",
    "license": "Apache-2.0",
    "description": "Free, local, open-source 24/7 Cowork app for OpenClaw, Hermes Agent, Claude Code, Codex, OpenCode, Gemini CLI and 20+ more CLI",
    "notes": "Built with Electron + React; runs on macOS, Windows and Linux. Often presented as a free alternative to Claude Cowork.",
}
v2_items.append(save(n))

aw.record_video(v2_uid, [i.uid for i in v2_items], status="analyzed")


# ---------------------------------------------------------------
# Video 3: JFgD4c3Tab0  — AI news roundup
# ---------------------------------------------------------------
v3_id = "JFgD4c3Tab0"
v3_uid = "fd8c1d4fb99c38ed"
v3_items = []

n = SoftwareNews.make(
    title="Gemini 3.2 Flash leaks in iOS app and AI Studio",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="model",
    summary="Gemini 3.2 Flash is reportedly being A/B tested through Antigravity, LM Arena, Google AI Studio and the Gemini iOS app. Pricing is reported at $0.25 per 1M input tokens and $2.00 per 1M output tokens, with a January 2026 knowledge cutoff.",
    timestamp_in_video="03:54",
    tags=["gemini", "google", "model-release", "leak"],
    links=["https://aistudio.google.com/"],
)
n.research = {
    "homepage": "https://deepmind.google/technologies/gemini/",
    "notes": "Confirmed as a real pre-I/O 2026 rollout. The host's video timestamps May 2026.",
    "web_findings": [
        {"title": "Gemini 3.2 Flash: Google's Model Surfaces in iOS App and AI Studio Ahead of I/O 2026", "url": "https://pasqualepillitteri.it/en/news/2013/gemini-3-2-flash-leak-ios-ai-studio-2026-en", "snippet": "Gemini 3.2 Flash appeared inside the official iOS Gemini app and Google AI Studio on May 5, 2026."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="SubQ: first sub-quadratic frontier LLM with 12M-token context",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="model",
    summary="Subquadratic, a Miami-based startup, launches SubQ, a frontier model built on a fully sub-quadratic sparse attention architecture supporting a 12 million-token context window. The company claims up to 52x speedup over FlashAttention at 1M tokens and roughly a fifth of the cost of Claude Opus or GPT-5.5 for comparable workloads.",
    timestamp_in_video="06:32",
    tags=["subq", "subquadratic", "long-context", "sparse-attention", "model-release"],
    links=["https://subquadratic.ai/"],
)
n.research = {
    "homepage": "https://subquadratic.ai/",
    "notes": "Launched 5 May 2026 with a $29M seed round. Claims benchmark scores of 95.0 on RULER-128K, 65.9 on MRCR v2 at 1M tokens, 81.8 on SWE-Bench Verified. Independent verification has been requested by researchers.",
    "web_findings": [
        {"title": "The context window has been shattered: Subquadratic debuts a 12-million-token window", "url": "https://thenewstack.io/subquadratic-12-million-context-window/", "snippet": "SubQ ships with a 12 million token context window, runs roughly 52x faster than FlashAttention at 1M tokens."},
        {"title": "Subquadratic launches with $29M to bring 12M-token context windows to AI", "url": "https://siliconangle.com/2026/05/05/subquadratic-launches-29m-bring-12m-token-context-windows-ai/", "snippet": "Founded by Justin Dangel and Alex Whedon (former Head of Generative AI at Meta)."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="OpenAI rolls out GPT-5.5 Instant in ChatGPT",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="OpenAI begins rolling out GPT-5.5 Instant in ChatGPT, described as a faster, more accurate variant of the flagship with stronger performance in medicine, law and finance, improved image analysis and adaptive web-search invocation.",
    timestamp_in_video="07:33",
    tags=["gpt-5.5", "openai", "model-release", "chatgpt"],
    links=["https://openai.com/index/introducing-gpt-5-5/"],
)
n.research = {
    "homepage": "https://openai.com/index/introducing-gpt-5-5/",
    "notes": "Official OpenAI announcement page corroborates the launch.",
    "web_findings": [
        {"title": "Introducing GPT-5.5 | OpenAI", "url": "https://openai.com/index/introducing-gpt-5-5/", "snippet": "OpenAI's newest frontier model for coding, computer use, knowledge work and research."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Anthropic ships 10 Claude finance agent templates",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Anthropic releases a suite of ten Claude agent templates for financial services, including pitch builder, meeting preparer, earnings reviewer, model builder, market researcher, valuation reviewer, statement auditor, KYC screener, general ledger reconciler and month-end closer. Templates run as plugins in Claude Cowork and Claude Code, or as cookbooks for Claude Managed Agents.",
    timestamp_in_video="08:16",
    tags=["anthropic", "claude", "finance", "agents", "release"],
    links=["https://www.anthropic.com/news/finance-agents"],
)
n.research = {
    "homepage": "https://www.anthropic.com/news/finance-agents",
    "notes": "Announced 5 May 2026. Bundled with Microsoft 365 add-in support across Excel, PowerPoint, Word and Outlook, plus data connectors to FactSet, S&P Capital IQ, MSCI, PitchBook, Morningstar, Daloopa, LSEG, Chronograph.",
    "web_findings": [
        {"title": "Anthropic — Finance agents", "url": "https://www.anthropic.com/news/finance-agents", "snippet": "Ten ready-to-run AI agent templates for financial services."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Gemma 4 gains multi-token prediction drafters for ~3x faster inference",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Google releases Multi-Token Prediction (MTP) drafter models for the Gemma 4 family. Through speculative decoding the drafters deliver up to a 3x speedup with no degradation in output quality. The drafters ship under the Apache 2.0 license, with weights on Hugging Face and Kaggle.",
    timestamp_in_video="09:27",
    tags=["gemma", "google", "open-weights", "inference", "speculative-decoding"],
    links=["https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/"],
)
n.research = {
    "homepage": "https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/",
    "notes": "Released 5 May 2026. Compatible with transformers, MLX, vLLM, SGLang and Ollama.",
    "web_findings": [
        {"title": "Accelerating Gemma 4: faster inference with multi-token prediction drafters", "url": "https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/", "snippet": "Up to 3x speedup with no degradation in output quality, Apache 2.0 license."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Google AI Studio integrates Nano Banana for in-app image asset generation",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Google AI Studio integrates the Nano Banana image model so that custom assets can be generated and inserted into apps as they are built. A redesigned edit tool provides component-level visual control, annotation and asset swapping.",
    timestamp_in_video="10:04",
    tags=["google-ai-studio", "nano-banana", "image-generation", "google"],
    links=["https://aistudio.google.com/"],
)
n.research = {
    "homepage": "https://aistudio.google.com/",
    "notes": "Described only briefly in the video; no dedicated launch page found in the consulted sources.",
}
n.research_status = "transcript_only"
n.research_date = now_iso()
aw.save_news(n)
v3_items.append(n)

n = SoftwareNews.make(
    title="NotebookLM mind maps gain prompt-driven customisation",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Google updates NotebookLM mind maps with prompt-based customisation, scoping to specific sources or topics, renaming and sharing, and smoother navigation between notes.",
    timestamp_in_video="10:32",
    tags=["notebooklm", "google", "feature-update"],
    links=["https://notebooklm.google.com/"],
)
n.research = {
    "homepage": "https://notebooklm.google.com/",
    "notes": "Documented in Google Workspace Updates and NotebookLM Help pages.",
    "web_findings": [
        {"title": "Use Mind Maps in NotebookLM - NotebookLM Help", "url": "https://support.google.com/notebooklm/answer/16212283?hl=en", "snippet": "Customise mind maps with prompts to focus on a specific source, concept, timeline or goal."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Google Pomelli adds product catalogs and AI photoshoots",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Pomelli, a Google Labs and DeepMind AI marketing tool for small-to-medium businesses, adds a Catalog feature that turns uploaded products or services into personalised marketing campaigns and AI photoshoots. Public beta, free.",
    timestamp_in_video="10:59",
    tags=["pomelli", "google", "marketing", "image-generation"],
    links=["https://labs.google.com/pomelli/about"],
)
n.research = {
    "homepage": "https://labs.google.com/pomelli/about",
    "notes": "Public beta in US, Canada, Australia and New Zealand. Free.",
    "web_findings": [
        {"title": "Google Labs and DeepMind launch AI marketing tool Pomelli", "url": "https://blog.google/innovation-and-ai/models-and-research/google-labs/pomelli/", "snippet": "Pomelli analyses a website to build a 'Business DNA' profile and generates branded campaigns."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Perplexity launches Computer for Professional Finance",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="release",
    summary="Perplexity launches Computer for Professional Finance, integrating licensed data from Morningstar, PitchBook, Daloopa and Carbon Arc via MCP. The release ships with 35 dedicated finance workflows aimed at recurring analyst tasks.",
    timestamp_in_video="11:23",
    tags=["perplexity", "finance", "computer-use", "mcp"],
    links=["https://www.perplexity.ai/"],
)
n.research = {
    "homepage": "https://www.perplexity.ai/",
    "notes": "Announced in early May 2026; positioned in direct competition with Anthropic's finance agent templates.",
    "web_findings": [
        {"title": "Perplexity launches 'Computer for professional finance' with Morningstar PitchBook data", "url": "https://www.newsbytesapp.com/news/science/perplexity-launches-computer-for-professional-finance-with-morningstar-pitchbook-data/tldr", "snippet": "Licensed Morningstar, PitchBook, Daloopa and Carbon Arc data through MCP, plus 35 finance workflows."},
    ],
}
v3_items.append(save(n))

n = SoftwareNews.make(
    title="Google shuts down Project Mariner, folds tech into Gemini and Chrome",
    source_video_id=v3_id,
    source_video_uid=v3_uid,
    source_channel_handle=CH,
    category="news",
    summary="Google quietly retires Project Mariner, the experimental browser-based AI agent showcased at Google I/O 2024. Components of the technology are folded into a persistent 24/7 personal agent inside the Gemini app and into Chrome's auto-browse features.",
    timestamp_in_video="06:06",
    tags=["google", "project-mariner", "agent", "discontinuation"],
    links=["https://labs.google/mariner"],
)
n.research = {
    "homepage": "https://labs.google/mariner",
    "notes": "Shut down on 4 May 2026 after a 17-month experiment.",
    "web_findings": [
        {"title": "Project Mariner is Over: Google Folds its AI Web Agent into Gemini & Chrome", "url": "https://www.androidheadlines.com/2026/05/google-shuts-down-project-mariner-ai-agent.html", "snippet": "Project Mariner shut down on May 4 2026; tech absorbed into Gemini Agent and Chrome."},
    ],
}
v3_items.append(save(n))

aw.record_video(v3_uid, [i.uid for i in v3_items], status="analyzed")


# ---------------------------------------------------------------
# Video 4: Du34BzfVRas  — Codex browser/computer use
# ---------------------------------------------------------------
v4_id = "Du34BzfVRas"
v4_uid = "447fee0a72a9da2a"
v4_items = []

n = SoftwareNews.make(
    title="OpenAI Codex app adds Browser Use plugin",
    source_video_id=v4_id,
    source_video_uid=v4_uid,
    source_channel_handle=CH,
    category="release",
    summary="OpenAI ships a Browser Use plugin inside the Codex desktop app, allowing the GPT-5.5 backed agent to operate the in-app browser to click through rendered UIs, inspect console and network logs, and verify fixes locally.",
    timestamp_in_video="00:53",
    tags=["openai", "codex", "browser-use", "agent", "plugin"],
    links=["https://developers.openai.com/codex/app", "https://developers.openai.com/codex/changelog"],
)
n.research = {
    "homepage": "https://developers.openai.com/codex/app",
    "notes": "Documented in the official Codex changelog. Browser Use is bundled as a Codex plugin.",
    "web_findings": [
        {"title": "Changelog – Codex | OpenAI Developers", "url": "https://developers.openai.com/codex/changelog", "snippet": "The Codex app can now operate the in-app browser through the bundled Browser plugin."},
    ],
}
v4_items.append(save(n))

n = SoftwareNews.make(
    title="Codex computer-use loop runs 42% faster",
    source_video_id=v4_id,
    source_video_uid=v4_uid,
    source_channel_handle=CH,
    category="release",
    summary="A Codex app update reports a 42% speedup for the computer-use loop. The host claims GPT-5.5 reaches 78.7% on OSWorld Verified, the benchmark measuring autonomous operation of real computer environments.",
    timestamp_in_video="02:39",
    tags=["openai", "codex", "computer-use", "performance"],
    links=["https://developers.openai.com/codex/app/computer-use"],
)
n.research = {
    "homepage": "https://developers.openai.com/codex/app/computer-use",
    "notes": "Computer use is available on macOS only at launch, excluding the EEA, UK and Switzerland.",
    "web_findings": [
        {"title": "Computer Use – Codex app | OpenAI Developers", "url": "https://developers.openai.com/codex/app/computer-use", "snippet": "Codex can see and operate graphical user interfaces on macOS."},
    ],
}
v4_items.append(save(n))

aw.record_video(v4_uid, [i.uid for i in v4_items], status="analyzed")


# ---------------------------------------------------------------
# Video 5: eV3lAY77IpU  — DeepSeek V4 preview
# ---------------------------------------------------------------
v5_id = "eV3lAY77IpU"
v5_uid = "e6375e3e0a09d71a"
v5_items = []

n = SoftwareNews.make(
    title="DeepSeek V4 Preview: Pro (1.6T) and Flash (284B) open-source models",
    source_video_id=v5_id,
    source_video_uid=v5_uid,
    source_channel_handle=CH,
    category="model",
    summary="DeepSeek releases the V4 Preview, open-sourcing two models: DeepSeek-V4-Pro at 1.6T total / 49B active parameters and DeepSeek-V4-Flash at 284B total / 13B active parameters. Both support a 1M-token context length and are released on Hugging Face under the MIT license. Pro pricing is $0.14/$3.48 per 1M input/output tokens, Flash is $0.03/$0.28.",
    timestamp_in_video="00:18",
    tags=["deepseek", "open-source", "model-release", "moe", "long-context"],
    links=["https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro", "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash", "https://api-docs.deepseek.com/news/news260424"],
)
n.research = {
    "homepage": "https://api-docs.deepseek.com/news/news260424",
    "notes": "Released 24 April 2026 as a public preview. Hybrid attention combining Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA). The host disputes the team's claim that V4 matches Claude Opus 4.5/4.6 on real-world agentic coding, calling the front-end and 3D-rendering outputs subpar relative to GLM 5.1, Kimi K2.6 and MiniMax M2.7.",
    "web_findings": [
        {"title": "DeepSeek V4 Preview Release | DeepSeek API Docs", "url": "https://api-docs.deepseek.com/news/news260424", "snippet": "DeepSeek-V4-Pro has 1.6T total / 49B active params; Flash has 284B total / 13B active params."},
        {"title": "DeepSeek V4 — almost on the frontier, a fraction of the price", "url": "https://simonwillison.net/2026/Apr/24/deepseek-v4/", "snippet": "1M-token context; MIT license; weights available on Hugging Face."},
    ],
}
v5_items.append(save(n))

aw.record_video(v5_uid, [i.uid for i in v5_items], status="analyzed")


# ---------------------------------------------------------------
# Video 6: UfUBW9QcTjU  — GPT-5.5 leak
# ---------------------------------------------------------------
v6_id = "UfUBW9QcTjU"
v6_uid = "5c12e84400a6ee3d"
v6_items = []

n = SoftwareNews.make(
    title="GPT-5.5 ('Spud') leak: Crest Pro Alpha checkpoint surfaces in ChatGPT",
    source_video_id=v6_id,
    source_video_uid=v6_uid,
    source_channel_handle=CH,
    category="model",
    summary="OpenAI A/B-tests a GPT-5.5 candidate (internal code name 'Spud') inside ChatGPT, with one checkpoint labelled 'Crest Pro Alpha' surfacing for some users. The host reports stronger reasoning, faster token output, improved SVG and three.js scene generation, and a Minecraft-clone with textures, inventory and animation in one shot.",
    timestamp_in_video="00:01",
    tags=["openai", "gpt-5.5", "model-release", "leak"],
    links=["https://openai.com/index/introducing-gpt-5-5/"],
)
n.research = {
    "homepage": "https://openai.com/index/introducing-gpt-5-5/",
    "notes": "GPT-5.5 was subsequently launched officially by OpenAI and surfaced in the Codex app as the recommended model. The 'Spud' / 'Crest Pro Alpha' codename is documented only via community reporting around the leak window.",
    "web_findings": [
        {"title": "Introducing GPT-5.5 | OpenAI", "url": "https://openai.com/index/introducing-gpt-5-5/", "snippet": "GPT-5.5 is OpenAI's newest frontier model for coding, computer use, knowledge work and research."},
    ],
}
v6_items.append(save(n))

aw.record_video(v6_uid, [i.uid for i in v6_items], status="analyzed")


# ---------------------------------------------------------------
print(aw.finalise())
print(f"news_count={aw.news_count}")
all_items = v1_items + v2_items + v3_items + v4_items + v5_items + v6_items
for i in all_items:
    print(f"{i.category:8s}  {i.title}  ({CH})")
