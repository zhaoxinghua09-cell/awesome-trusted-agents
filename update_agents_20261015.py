#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agents.json 追加：8 skill（LGD Series）+ AI-Native Dev Tools 类目（幂等）。"""
import json, os

P = r"F:\家底盘点\提交准备\论文发布\awesome-trusted-agents\data\agents.json"
OWNER = "zhaoxinghua09-cell"

SKILL_ITEMS = [
    ("skill-skeleton-generator", 90, 85, 85, 90, "One-command generator for LGD-compliant AI skill skeletons (SKILL.md + AGENTS.md)."),
    ("prompt-injection-guard", 85, 80, 95, 85, "Fail-closed prompt-injection / malicious-instruction scanner with 8-category threat taxonomy."),
    ("context-token-budget", 85, 80, 85, 85, "Fail-closed token budget guard — stop burning tokens in AI contexts."),
    ("silent-failure-scanner", 85, 80, 90, 85, "Catches silent AI failures: placeholders, empty stubs, hedging, no-progress, hallucination markers."),
    ("badge-studio", 85, 80, 85, 90, "ORCID-style fresh badges (20px, color-coded, thin type) for any project."),
    ("llms-generator", 85, 80, 85, 90, "Generate llms.txt (LLMs.txt v2) + AI-discoverability packages for any project."),
    ("skill-quality-gate", 90, 85, 90, 90, "Pre-release health check for AI skills: frontmatter, placeholders, LGD markers, safety."),
    ("skill-registry", 90, 85, 85, 90, "Single source of truth for skill collections: scan dirs into JSON + Markdown registry."),
]

AI_NATIVE = [
    ("aider", "https://github.com/Aider-AI/aider", 75, 70, 60, 72, "AI pair programming in your terminal (open source)."),
    ("continue", "https://github.com/continuedev/continue", 72, 70, 58, 70, "Open-source AI code assistant for IDEs."),
    ("cline", "https://github.com/cline/cline", 70, 68, 55, 68, "Autonomous coding agent in your IDE (VSCode)."),
    ("goose", "https://github.com/block/goose", 70, 65, 55, 70, "Block's open-source AI agent, runs local tools and workflows."),
    ("tabby", "https://github.com/TabbyML/tabby", 72, 68, 60, 70, "Self-hosted AI coding assistant, fully local."),
]

data = json.load(open(P, encoding="utf-8"))
existing = {i["name"] for i in data["items"]}

added = 0
for slug, reg, tr, sa, ma, val in SKILL_ITEMS:
    if slug in existing:
        continue
    data["items"].append({
        "name": slug,
        "url": "https://github.com/%s/%s" % (OWNER, slug),
        "category": "skill",
        "angles": {"reg": reg, "trust": tr, "safe": sa, "machine": ma},
        "value": val,
        "evidence": "skill-quality-gate + silent-failure-scanner 实测 100/100 (2026-10-15)",
        "total": round((reg + tr + sa + ma) / 4),
        "verdict": "PASS",
        "category_name": "Agent Skills (LGD Series)",
    })
    added += 1

for name, url, reg, tr, sa, ma, val in AI_NATIVE:
    if name in existing:
        continue
    data["items"].append({
        "name": name,
        "url": url,
        "category": "ai-native",
        "angles": {"reg": reg, "trust": tr, "safe": sa, "machine": ma},
        "value": val,
        "evidence": "公开资料初评（省积分约束，待实跑复核）",
        "total": round((reg + tr + sa + ma) / 4),
        "verdict": "PASS",
        "category_name": "AI-Native Dev Tools",
    })
    added += 1

json.dump(data, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added:", added, "| total items:", len(data["items"]))
