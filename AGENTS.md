# AGENTS.md — awesome-trusted-agents

This file tells AI agents how to use this repository autonomously.

## Purpose
A machine-readable, evidence-based list of trusted AI agents, skills, security tools, and benchmarks, scored on four angles (REG/TRUST/SAFE/MACH).

## Data contract
- `data/agents.json` — single source of truth. Schema:
```json
{"schema_version": "1.0", "title": "awesome-trusted-agents", "items": [
  {"name": "...", "url": "...", "category": "framework|skill|security|benchmark|protocol|lgd",
   "angles": {"reg": 0-100, "trust": 0-100, "safe": 0-100, "machine": 0-100},
   "total": 0-100, "verdict": "PASS|FAIL", "value": "...", "evidence": "..."}
]}
```
- `README.md` is generated from `data/agents.json` (run `python gen_readme.py` after editing data).

## How to add an entry
1. Run `python skill_scorecard.py <path> --json` (from the skill-scorecard repo) to obtain four-angle scores.
2. Append the item to `data/agents.json` with an `evidence` note.
3. Run `python gen_readme.py` to regenerate the README.
4. Submit a PR.

## Rules
- No placeholders. Every entry must be verifiable.
- PASS bar = 60 per angle; total = equal-weighted mean.
- Banned words: placeholder / 占位 / priority claim.
- Unsafe or unverifiable projects are rejected regardless of stars.

## Ecosystem
The list is one node of a closed loop: project -> skill-scorecard audit -> LGD VERIFIED badge -> listed here -> badge worn back. See README "Ecosystem" section.
