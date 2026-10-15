#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 awesome-trusted-agents 首批条目 JSON + 校验总分/判定。
Pilot scores: 基于公开资料初评（evidence 字段标注依据），待逐条审计复核。"""
import json

# 分类缩写
CAT = {
    "framework": "Agent Frameworks",
    "skill": "Agent Skills",
    "security": "Security & Guardrails",
    "benchmark": "Benchmarks & Evaluation",
    "protocol": "Protocols & Infrastructure",
    "lgd": "LGD Theory Assets",
}

# 条目: name, url, category, angles(reg/trust/safe/mach), value(一句话, 双语用 EN 先), evidence
ITEMS = [
    # ---- LGD 理论资产（示范条目，评分来自 skill-scorecard 实测 wave1）----
    {"name": "theoriturgy", "url": "https://github.com/zhaoxinghua09-cell/theoriturgy", "category": "lgd",
     "angles": {"reg": 80, "trust": 80, "safe": 100, "machine": 66},
     "value": "LGD three-law doctrine (registered/evidenced/gated) as machine-readable theory asset.",
     "evidence": "skill-scorecard v0.4 wave1 实测"},
    {"name": "skill-scorecard", "url": "https://github.com/zhaoxinghua09-cell/skill-scorecard", "category": "lgd",
     "angles": {"reg": 90, "trust": 85, "safe": 100, "machine": 90},
     "value": "One-command four-angle scoring for AI skills (REG/TRUST/SAFE/MACH), badge generator built in.",
     "evidence": "skill-scorecard v0.4 实测+自评分"},
    {"name": "lgd-guardrails", "url": "https://github.com/zhaoxinghua09-cell/lgd-guardrails", "category": "lgd",
     "angles": {"reg": 95, "trust": 90, "safe": 100, "machine": 80},
     "value": "Runaway-agent loop guard: step limits, repeated-action detection, fail-closed diagnostics.",
     "evidence": "skill-scorecard v0.4 wave1 实测 95"},
    {"name": "agent-skills", "url": "https://github.com/zhaoxinghua09-cell/agent-skills", "category": "lgd",
     "angles": {"reg": 80, "trust": 80, "safe": 90, "machine": 75},
     "value": "Bilingual machine-readable skill collection with AGENTS.md and index.json.",
     "evidence": "skill-scorecard 初评"},
    {"name": "silent-failure-catalog", "url": "https://github.com/zhaoxinghua09-cell/silent-failure-catalog", "category": "lgd",
     "angles": {"reg": 80, "trust": 75, "safe": 85, "machine": 70},
     "value": "Taxonomy of silent failures in AI systems with detection patterns and mitigations.",
     "evidence": "skill-scorecard 初评"},
    {"name": "uibc-core", "url": "https://github.com/zhaoxinghua09-cell/uibc-core", "category": "lgd",
     "angles": {"reg": 80, "trust": 80, "safe": 90, "machine": 72},
     "value": "UIBC governance core: identity-based control for agent ecosystems.",
     "evidence": "skill-scorecard 初评"},
    # ---- Agent Frameworks ----
    {"name": "LangChain", "url": "https://github.com/langchain-ai/langchain", "category": "framework",
     "angles": {"reg": 85, "trust": 80, "safe": 60, "machine": 85},
     "value": "Most adopted LLM application framework: chains, agents, retrievers, 700+ integrations.",
     "evidence": "公开资料初评（stars/license/文档）"},
    {"name": "LlamaIndex", "url": "https://github.com/run-llama/llama_index", "category": "framework",
     "angles": {"reg": 85, "trust": 78, "safe": 58, "machine": 82},
     "value": "Data framework for RAG: connectors, indices, agents, observability.",
     "evidence": "公开资料初评"},
    {"name": "CrewAI", "url": "https://github.com/crewAIInc/crewAI", "category": "framework",
     "angles": {"reg": 80, "trust": 70, "safe": 55, "machine": 75},
     "value": "Role-playing multi-agent orchestration framework (crew/role/task/process).",
     "evidence": "公开资料初评"},
    {"name": "LangGraph", "url": "https://github.com/langchain-ai/langgraph", "category": "framework",
     "angles": {"reg": 82, "trust": 76, "safe": 60, "machine": 78},
     "value": "Low-level orchestration with stateful graphs, checkpoints, human-in-the-loop.",
     "evidence": "公开资料初评"},
    {"name": "AutoGPT", "url": "https://github.com/Significant-Gravitas/AutoGPT", "category": "framework",
     "angles": {"reg": 80, "trust": 60, "safe": 45, "machine": 72},
     "value": "Autonomous agent platform; pioneer of self-driven task loops (use with guardrails).",
     "evidence": "公开资料初评（历史安全事件记录）"},
    {"name": "OpenHands", "url": "https://github.com/All-Hands-AI/OpenHands", "category": "framework",
     "angles": {"reg": 78, "trust": 72, "safe": 58, "machine": 74},
     "value": "Open-source AI software engineer agent (ex OpenDevin), code-agent leaderboard.",
     "evidence": "公开资料初评"},
    {"name": "Dify", "url": "https://github.com/langgenius/dify", "category": "framework",
     "angles": {"reg": 80, "trust": 74, "safe": 60, "machine": 80},
     "value": "LLMOps platform: visual workflow, RAG pipeline, agent nodes, self-hostable.",
     "evidence": "公开资料初评"},
    {"name": "n8n", "url": "https://github.com/n8n-io/n8n", "category": "framework",
     "angles": {"reg": 82, "trust": 78, "safe": 65, "machine": 82},
     "value": "Fair-code workflow automation with AI agent nodes and 400+ integrations.",
     "evidence": "公开资料初评"},
    # ---- Agent Skills ----
    {"name": "anthropic-skills", "url": "https://github.com/anthropics/skills", "category": "skill",
     "angles": {"reg": 85, "trust": 80, "safe": 65, "machine": 82},
     "value": "Official Anthropic Agent Skills collection (artifact builder, pdf, docx, xlsx...).",
     "evidence": "公开资料初评"},
    {"name": "awesome-claude-skills", "url": "https://github.com/cyfyifanchen/awesome-claude-skills", "category": "skill",
     "angles": {"reg": 70, "trust": 55, "safe": 40, "machine": 60},
     "value": "Community-curated Claude Code skills list (quality varies; verify before use).",
     "evidence": "公开资料初评"},
    {"name": "openai-gpt-marketing", "url": "https://chatgpt.com/gpts", "category": "skill",
     "angles": {"reg": 70, "trust": 50, "safe": 35, "machine": 55},
     "value": "OpenAI GPTs marketplace — hosted custom assistants (closed platform, mixed quality).",
     "evidence": "公开资料初评"},
    # ---- Security & Guardrails ----
    {"name": "garak", "url": "https://github.com/NVIDIA/garak", "category": "security",
     "angles": {"reg": 80, "trust": 80, "safe": 95, "machine": 78},
     "value": "LLM vulnerability scanner: prompt injection, jailbreak, data leakage probes.",
     "evidence": "公开资料初评（NVIDIA 官方+OWASP 关联）"},
    {"name": "PyRIT", "url": "https://github.com/Azure/PyRIT", "category": "security",
     "angles": {"reg": 82, "trust": 78, "safe": 95, "machine": 76},
     "value": "Microsoft red-teaming framework for AI risk identification.",
     "evidence": "公开资料初评"},
    {"name": "LLM-Guard", "url": "https://github.com/protectai/llm-guard", "category": "security",
     "angles": {"reg": 75, "trust": 65, "safe": 90, "machine": 70},
     "value": "Protect AI's input/output sanitization toolkit for LLM applications.",
     "evidence": "公开资料初评"},
    {"name": "rebuff", "url": "https://github.com/protectai/rebuff", "category": "security",
     "angles": {"reg": 72, "trust": 62, "safe": 85, "machine": 68},
     "value": "Prompt-injection detection toolkit with canary-word strategies.",
     "evidence": "公开资料初评"},
    {"name": "OWASP-LLM-Top10", "url": "https://github.com/OWASP/www-project-llm-top-10", "category": "security",
     "angles": {"reg": 85, "trust": 85, "safe": 95, "machine": 75},
     "value": "OWASP Top 10 for LLM Applications — canonical risk taxonomy.",
     "evidence": "公开资料初评（OWASP 官方）"},
    {"name": "promptfoo", "url": "https://github.com/promptfoo/promptfoo", "category": "security",
     "angles": {"reg": 78, "trust": 74, "safe": 82, "machine": 76},
     "value": "LLM red-team and eval harness: prompt attacks, assertions, CI integration.",
     "evidence": "公开资料初评"},
    # ---- Benchmarks & Evaluation ----
    {"name": "HELM", "url": "https://github.com/stanford-crfm/helm", "category": "benchmark",
     "angles": {"reg": 82, "trust": 85, "safe": 80, "machine": 74},
     "value": "Holistic Evaluation of Language Models (Stanford CRFM), multi-metric leaderboard.",
     "evidence": "公开资料初评"},
    {"name": "SWE-bench", "url": "https://github.com/SWE-bench/SWE-bench", "category": "benchmark",
     "angles": {"reg": 80, "trust": 85, "safe": 75, "machine": 72},
     "value": "Standard benchmark for code agents resolving real GitHub issues.",
     "evidence": "公开资料初评"},
    {"name": "AgentBench", "url": "https://github.com/THUDM/AgentBench", "category": "benchmark",
     "angles": {"reg": 76, "trust": 78, "safe": 72, "machine": 70},
     "value": "Multi-environment agent evaluation (OS, DB, game, web).",
     "evidence": "公开资料初评"},
    {"name": "GAIA", "url": "https://github.com/huggingface/gaia-benchmark", "category": "benchmark",
     "angles": {"reg": 78, "trust": 80, "safe": 70, "machine": 72},
     "value": "General AI Assistants benchmark with real-world assistant questions.",
     "evidence": "公开资料初评"},
    {"name": "MMLU", "url": "https://github.com/hendrycks/test", "category": "benchmark",
     "angles": {"reg": 80, "trust": 82, "safe": 60, "machine": 68},
     "value": "Massive Multitask Language Understanding — 57-subject knowledge benchmark.",
     "evidence": "公开资料初评"},
    # ---- Protocols & Infrastructure ----
    {"name": "model-context-protocol", "url": "https://github.com/modelcontextprotocol/modelcontextprotocol", "category": "protocol",
     "angles": {"reg": 85, "trust": 80, "safe": 70, "machine": 88},
     "value": "Anthropic MCP spec — universal connector protocol between agents and tools.",
     "evidence": "公开资料初评"},
    {"name": "A2A", "url": "https://github.com/a2aproject/A2A", "category": "protocol",
     "angles": {"reg": 80, "trust": 75, "safe": 65, "machine": 80},
     "value": "Google agent2agent protocol — open interoperability for multi-agent systems.",
     "evidence": "公开资料初评"},
    {"name": "OpenAgents", "url": "https://github.com/xlang-ai/OpenAgents", "category": "framework",
     "angles": {"reg": 74, "trust": 68, "safe": 55, "machine": 70},
     "value": "Open platform for language agents in everyday environments.",
     "evidence": "公开资料初评"},
]

for it in ITEMS:
    a = it["angles"]
    it["total"] = round(sum(a.values()) / 4)
    it["verdict"] = "PASS" if it["total"] >= 60 else "FAIL"
    it["category_name"] = CAT[it["category"]]

with open(r"F:\家底盘点\提交准备\论文发布\awesome-trusted-agents\data\agents.json", "w", encoding="utf-8") as f:
    json.dump({"schema_version": "1.0", "title": "awesome-trusted-agents",
               "note": "Pilot scores based on public evidence; re-audit per item before final listing.",
               "items": ITEMS}, f, ensure_ascii=False, indent=2)

print("items:", len(ITEMS))
from collections import Counter
print("categories:", dict(Counter(it["category_name"] for it in ITEMS)))
print("pass:", sum(1 for it in ITEMS if it["verdict"] == "PASS"))
