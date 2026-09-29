#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse page_contents/changelog.txt into structured data/changelog.json."""
import json, os, re

BASE = r"C:\Users\star\WorkBuddy\2026-06-23-02-05-48"
src = os.path.join(BASE, "page_contents", "changelog.txt")
out = os.path.join(BASE, "ftfvalues-web", "data", "changelog.json")

KNOWN = {
    "Value Increase", "Value Decrease", "Demand Change",
    "New Items", "Description Change", "Bug Fix", "Other",
}

with open(src, encoding="utf-8-sig") as f:
    lines = [ln.rstrip("\n").rstrip("\r") for ln in f]

# find the main content section
start = None
for i, ln in enumerate(lines):
    if ln.strip() == "## 主要内容":
        start = i + 1
        break
if start is None:
    raise SystemExit("could not find '## 主要内容'")

versions = []
cur = None
pending = None
for ln in lines[start:]:
    s = ln.strip()
    if s == "":
        continue
    if s == "Stay Updated":
        break
    if s.startswith("Version "):
        if cur:
            versions.append(cur)
        cur = {"version": s[len("Version "):].strip(), "date": None, "changes": []}
        pending = None
        continue
    if cur is None:
        continue
    if cur["date"] is None:
        cur["date"] = s
        continue
    if s in KNOWN:
        pending = s
        continue
    if pending:
        cur["changes"].append({"type": pending, "text": s})

if cur:
    versions.append(cur)

with open(out, "w", encoding="utf-8") as f:
    json.dump(versions, f, ensure_ascii=False, indent=2)

print("WROTE", out, "versions=", len(versions))
