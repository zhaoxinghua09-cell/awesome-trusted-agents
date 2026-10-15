#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""建仓 awesome-trusted-agents + 推送首批文件。Usage: python create_awesome_repo.py <token>"""
import base64, json, sys, time, urllib.request, urllib.error

TOKEN = sys.argv[1]
OWNER = "zhaoxinghua09-cell"
REPO = "awesome-trusted-agents"
BASE = r"F:\家底盘点\提交准备\论文发布\awesome-trusted-agents"

def api(url, method="GET", payload=None, raw=False):
    h = {"Authorization": "token " + TOKEN,
         "Accept": "application/vnd.github.raw+json" if raw else "application/vnd.github+json"}
    data = json.dumps(payload).encode() if payload else None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, data=data, headers=h, method=method)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception as e:
            if attempt == 3:
                return -1, "NETFAIL: %s" % e
            time.sleep(2 * (attempt + 1))

# 1) 建仓
desc = ("Trusted AI agent / skill / security / benchmark list with four-angle scoring (REG/TRUST/SAFE/MACH). "
        "可信 AI 智能体/技能/安全/评测四角度评分精选清单。")
payload = {"name": REPO, "description": desc, "private": False,
           "has_issues": True, "has_wiki": True, "has_projects": False,
           "auto_init": True, "license_template": "mit", "homepage": ""}
s, body = api("https://api.github.com/user/repos", "POST", payload)
print("create repo:", s, body[:200] if s != 200 else "OK")

# 2) 推送文件
files = [
    ("README.md", "README.md"),
    ("data/agents.json", "data/agents.json"),
    ("AGENTS.md", "AGENTS.md"),
    ("LICENSE", "LICENSE"),
    ("gen_agents_json.py", "gen_agents_json.py"),
    ("gen_readme.py", "gen_readme.py"),
]
for local, path in files:
    with open(BASE + "\\" + local, "r", encoding="utf-8") as f:
        content = f.read()
    base = "https://api.github.com/repos/%s/%s/contents/" % (OWNER, REPO)
    s0, b0 = api(base + path)
    sha = json.loads(b0).get("sha") if s0 == 200 else None
    p = {"message": "init %s" % path, "content": base64.b64encode(content.encode()).decode()}
    if sha:
        p["sha"] = sha
    s2, _ = api(base + path, "PUT", p)
    print("  %-18s %s" % (path, s2))
print("=== done ===")
