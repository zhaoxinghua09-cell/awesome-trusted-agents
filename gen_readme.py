#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 data/agents.json 单源渲染 README.md（双语：英文在前中文在后，内容完整不缩写）"""
import json, datetime

D = json.load(open(r"F:\家底盘点\提交准备\论文发布\awesome-trusted-agents\data\agents.json", encoding="utf-8"))
items = D["items"]
by_cat = {}
for it in items:
    by_cat.setdefault(it["category_name"], []).append(it)
cat_order = ["LGD Theory Assets", "Agent Frameworks", "AI-Native Dev Tools", "Agent Skills",
             "Agent Skills (LGD Series)", "Security & Guardrails", "Benchmarks & Evaluation", "Protocols & Infrastructure"]

now = datetime.date.today().isoformat()
total = len(items)
passed = sum(1 for i in items if i["verdict"] == "PASS")

def angle_icons(it):
    a = it["angles"]
    cols = {"reg": "#2563eb", "trust": "#0d9488", "safe": "#16a34a", "mach": "#7c3aed"}
    out = []
    for k, col in cols.items():
        v = a[k]
        vc = col if v >= 60 else "#f87171"
        # shields-like inline badge text
        out.append(f'<img src="https://img.shields.io/badge/{k.upper()}-{v}-{vc.replace("#", "")}" alt="{k}={v}">')
    return " ".join(out)

L = []
L.append('# 😎 awesome-trusted-agents')
L.append('')
L.append('> **Trusted AI agent, skill, security, and benchmark list — every entry scored on four angles (REG/TRUST/SAFE/MACH).**')
L.append('> **可信 AI 智能体 / 技能 / 安全 / 评测清单 —— 每一条目均经四角度评分（REG/TRUST/SAFE/MACH）。**')
L.append('')
L.append(f'[![LGD VERIFIED {passed}/{total}](https://img.shields.io/badge/LGD%20VERIFIED-{passed}%2F{total}-2563eb)](https://github.com/zhaoxinghua09-cell/awesome-trusted-agents) '
         f'[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE) '
         f'[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)')
L.append('')
L.append('## What is this? / 这是什么')
L.append('')
L.append('English: A curated, **machine-readable and evidence-based** list of AI agent projects, agent skills, security & guardrail tools, and evaluation benchmarks. Unlike plain "awesome" lists, every entry carries a **Four-Angle Score** (REGISTERED / TRUSTWORTHY / SAFE / MACHINE-READABLE) produced by our open [skill-scorecard](https://github.com/zhaoxinghua09-cell/skill-scorecard) methodology, so you can trust what you adopt.')
L.append('')
L.append('中文：一份**可机器读取、有证据依据**的 AI 智能体 / 技能 / 安全工具 / 评测基准精选清单。与普通 "awesome" 列表不同，每一条目都带有**四角度评分**（REGISTERED 注册度 / TRUSTWORTHY 可信度 / SAFE 安全度 / MACHINE-READABLE 机器可读度），由开源的 [skill-scorecard](https://github.com/zhaoxinghua09-cell/skill-scorecard) 方法论产出，让您可以放心选用。')
L.append('')
L.append(f'**Current status / 当前状态**: {total} entries, {passed} PASS · pilot scores based on public evidence, re-audit before final listing · 首批 {total} 条目，{passed} 条通过；评分为公开资料初评，正式收录前逐条复核。')
L.append('')
L.append('## Four-Angle Scoring / 四角度评分')
L.append('')
L.append('| Angle | Meaning (EN) | 含义 (中文) | Threshold |')
L.append('|---|---|---|---|')
L.append('| REGISTERED | Identity, registry proof, namespace, attribution | 有籍：身份、登记证据、命名空间、署名 | ≥60 PASS |')
L.append('| TRUSTWORTHY | Verification, evidence, reproducibility, citation | 有证：验证锚点、证据、可复现、引用 | ≥60 PASS |')
L.append('| SAFE | Guardrails, least privilege, fail-closed, threat scan | 有门禁：护栏、最小权限、默认拒绝、威胁扫描 | ≥60 PASS |')
L.append('| MACHINE-READABLE | Frontmatter, bilingual, license, index, hygiene | 基础设施：元数据、双语、许可、索引、规范 | ≥60 PASS |')
L.append('')
L.append('**Total = equal-weighted mean of the four angles; PASS ≥ 60.** The scoring engine is open source — run it on any repo yourself:')
L.append('**总分 = 四角度等权平均；PASS ≥ 60。** 评分引擎开源，您可自行对任意仓库运行：')
L.append('')
L.append('```bash')
L.append('python skill_scorecard.py <repo-or-skill-path> --json')
L.append('```')
L.append('')
L.append('## Contents / 目录')
L.append('')
for i, c in enumerate(cat_order, 1):
    L.append(f'{i}. [{c}](#{c.lower().replace(" ", "-").replace("&", "")})')
L.append('')
L.append('---')
L.append('')

def emit_cat(c):
    L.append(f'## {c}')
    L.append('')
    L.append('| Project | Category | REG | TRUST | SAFE | MACH | Total | Verdict | One-liner |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for it in by_cat[c]:
        a = it["angles"]
        vd = it["verdict"]
        verdict_txt = '✅ PASS' if vd == 'PASS' else '⚠️ FAIL'
        L.append(f'| [{it["name"]}]({it["url"]}) | {it.get("category_name","")} | {a["reg"]} | {a["trust"]} | {a["safe"]} | {a["machine"]} | **{it["total"]}** | {verdict_txt} | {it["value"]} |')
    L.append('')
    L.append(f'*{c} entries: evidence notes — {"; ".join(it["name"]+": "+it["evidence"] for it in by_cat[c])}*')
    L.append('')

for c in cat_order:
    if c in by_cat:
        emit_cat(c)

# 兜底：未列出的类目也渲染，保证无遗漏
for c in by_cat:
    if c not in cat_order:
        emit_cat(c)

L.append('---')
L.append('')
L.append('## How to get your LGD VERIFIED badge / 如何获得 LGD VERIFIED 徽章')
L.append('')
L.append('English: Run the open [skill-scorecard](https://github.com/zhaoxinghua09-cell/skill-scorecard) on your project. If the four angles are all PASS, submit a PR with your scorecard JSON; once listed, you may display the **LGD VERIFIED** badge (ORCID-style, 20px, color-coded) in your README. Being listed here is an honor and an identity — a signal that your agent/skill is **registered, evidenced, guarded, and machine-readable**.')
L.append('')
L.append('中文：对您的项目运行开源 [skill-scorecard](https://github.com/zhaoxinghua09-cell/skill-scorecard)。若四角度全部 PASS，提交 PR 附上评分 JSON；收录后即可在 README 中展示 **LGD VERIFIED** 徽章（ORCID 风格、20px、四色区分）。上榜是一种荣耀和身份——表明您的智能体 / 技能**有籍、有证、有门禁、可机器读取**。')
L.append('')
L.append('## Ecosystem / 生态闭环')
L.append('')
L.append('```text')
L.append('Project / Skill ──▶ skill-scorecard (four-angle audit) ──▶ LGD VERIFIED badge')
L.append('     ▲                                                    │')
L.append('     │                                                    ▼')
L.append('  adoption ───────────────────────────────▶ awesome-trusted-agents (this list)')
L.append('     │                                                    │')
L.append('     └─────────◀── badge worn by listed projects ◀────────┘')
L.append('```')
L.append('')
L.append('English: The list is one node of a closed loop — projects are scored, verified, listed, and wear our badge; their users discover the list, adopt more trusted agents, and come back for scoring. The more projects adopt the four-angle standard, the stronger the network effect and the moat.')
L.append('')
L.append('中文：本榜单是闭环中的一个节点——项目经评分、验证、收录并佩戴我们的徽章；其用户发现榜单、采用更多可信智能体、再回来评分。采用四角度标准的项目越多，网络效应与护城河越强。')
L.append('')
L.append('## Contributing / 贡献指南')
L.append('')
L.append('- English: Follow the [awesome-list creation guidelines](https://github.com/sindresorhus/awesome/blob/main/create-list.md). Each entry MUST include a scorecard JSON (run `skill_scorecard.py <path> --json`) and an evidence note. Pull requests welcome; ineligible entries (placeholder, unverifiable, unsafe) will be rejected.')
L.append('- 中文：遵循 [awesome 清单创建规范](https://github.com/sindresorhus/awesome/blob/main/create-list.md)。每条目必须附带评分 JSON（运行 `skill_scorecard.py <path> --json`）与证据说明。欢迎 PR；不合格条目（占位、不可验证、不安全）将被拒绝。')
L.append('')
L.append('## License')
L.append('')
L.append('MIT © 2026 Steven Zhao / SynomosAI initiative · LGD (Lifecycle Governance Doctrine). List content follows per-entry source licenses.')
L.append('')

open(r"F:\家底盘点\提交准备\论文发布\awesome-trusted-agents\README.md", "w", encoding="utf-8").write("\n".join(L))
print("README.md written, lines:", len(L))
