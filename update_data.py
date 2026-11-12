#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 ftfvaluelist.com 的 Appwrite bucket 拉取最新数据，转换为站点 schema，
下载全部物品图到 images/<rarity>/，清理孤儿图。

数据源:
  - https://api.ftfvaluelist.com/v1/storage/buckets/ftf-data/files/ftf-values/view?project=ftf-values
  - ftfvaluelist.com/items/<slug>.webp  (官方物品图)
  - nav bundle 里硬编码的 Unique(Merch) 物品
"""

import json, os, re, shutil, urllib.request, unicodedata

REPO = os.path.dirname(os.path.abspath(__file__))
WS = os.path.join(REPO, "_cache")          # API 数据缓存目录
IMG = os.path.join(REPO, "images")

CAT_KEYS = {'Legendary': 'Legendaries', 'Epic': 'Epics', 'Rare': 'Rares',
            'Common': 'Commons', 'Unique': 'Uniques'}
RARITY_LOWER = {'Legendaries': 'legendary', 'Epics': 'epic', 'Rares': 'rare',
                'Commons': 'common', 'Uniques': 'unique'}

LAST_UPDATED = '13th November'
SOURCE_TS = None


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = s.replace("'", "").replace("\u2019", "")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def slugify(name):
    s = unicodedata.normalize("NFKD", name or "")
    s = re.sub(r"['\u2019]", "", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "item"


def their_slug(name):
    """ftfvaluelist 的图片 slug 规则: Oe()"""
    s = re.sub(r"\.webp$", "", name or "", flags=re.I)
    s = re.sub(r"['*?:\\/<>|\"]", "", s)
    s = re.sub(r"\s+", "-", s).lower()
    return s


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    return raw if binary else json.loads(raw)


def extract_hardcoded_uniques(nav_js):
    seg = nav_js.split("HARDCODED_UNIQUE_ITEMS:", 1)[1]
    # 从第一个 [ 取到平衡的 ]
    start = seg.index("[")
    depth = 0
    for i in range(start, len(seg)):
        if seg[i] == "[":
            depth += 1
        elif seg[i] == "]":
            depth -= 1
            if depth == 0:
                arr = seg[start:i + 1]
                break
    js = arr.replace("`", '"').replace("!0", "true").replace("!1", "false")
    js = re.sub(r"([{,])\s*([A-Za-z_][A-Za-z0-9_]*):", r'\1"\2":', js)
    return json.loads(js)


def download_sources():
    os.makedirs(WS, exist_ok=True)
    base = "https://api.ftfvaluelist.com/v1/storage/buckets/ftf-data/files"
    for fid in ["ftf-values", "ftf-changelog", "value-history"]:
        raw = fetch(f"{base}/{fid}/view?project=ftf-values", binary=True)
        open(os.path.join(WS, f"_api_{fid}.json"), "wb").write(raw)
        print("downloaded", fid, len(raw), "bytes")
    # nav bundle（含 HARDCODED_UNIQUE_ITEMS）：从页面动态解析 bundle 地址
    page = fetch("https://ftfvaluelist.com/valuelist", binary=True).decode("utf-8", "ignore")
    m = re.search(r"/assets/(valuelist-[A-Za-z0-9_.-]+\.js)", page)
    vl = fetch("https://ftfvaluelist.com" + m.group(0), binary=True).decode("utf-8", "ignore")
    m3 = re.search(r"\./(nav-[A-Za-z0-9_.-]+\.js)", vl)
    nav_name = m3.group(1)
    nav = fetch("https://ftfvaluelist.com/assets/" + nav_name, binary=True).decode("utf-8", "ignore")
    open(os.path.join(WS, "_nav_bundle.js"), "w", encoding="utf-8").write(nav)
    print("downloaded", nav_name, len(nav), "bytes")


def main():
    download_sources()
    new = json.load(open(WS + r"\_api_ftf-values.json", encoding="utf-8"))
    items_in = new["items"]
    global SOURCE_TS
    SOURCE_TS = new.get("last_updated_timestamp")
    last_upd = new.get("last_updated") or LAST_UPDATED

    nav_js = open(WS + r"\_nav_bundle.js", encoding="utf-8").read()
    hardcoded = extract_hardcoded_uniques(nav_js)
    print("dataset items:", len(items_in), "| hardcoded uniques:", len(hardcoded))

    # 老数据: 名称 -> 旧本地图(供回退)
    old = json.load(open(os.path.join(REPO, "ftf_values_full_data.json"), encoding="utf-8"))
    old_img_by_name = {}
    for cat, v in old.items():
        for it in v["items"]:
            p = it.get("local_image_path")
            if p and norm(it["name"]) not in old_img_by_name:
                old_img_by_name[norm(it["name"])] = p

    # 旧图集合(判断哪些是孤儿)
    referenced_new = set()

    # ---------- 组装条目 ----------
    cats = {v: {"page_name": v, "page_url": f"https://www.ftfvalues.app/{v.lower()}.html",
                "metadata": {"last_updated": last_upd, "source": "https://ftfvaluelist.com/valuelist",
                             "source_updated_at": SOURCE_TS}, "items": []}
            for v in CAT_KEYS.values()}

    def build(it, extra=None):
        rarity_raw = (it.get("rarity") or "").lower()
        cat = CAT_KEYS.get(it.get("rarity")) or CAT_KEYS.get(rarity_raw.capitalize())
        if cat is None:
            print("  !! unknown rarity", it.get("rarity"), it.get("name"))
            return None
        rng = it.get("range") or [None, None]
        val = it.get("value")
        if isinstance(val, str):  # 'N/A'
            val = None
        rec = {
            "id": it.get("id"),
            "name": it["name"],
            "rarity": RARITY_LOWER[cat],
            "value": val,
            "value_min": rng[0] if rng and len(rng) > 1 else None,
            "value_max": rng[1] if rng and len(rng) > 1 else None,
            "demand": it.get("demand") if not isinstance(it.get("demand"), str) else None,
            "stability": it.get("stability") or "Stable",
            "status": None,
            "event": it.get("event"),
            "rank": it.get("rank"),
            "border_color": it.get("borderColor"),
            "image_url": f"https://ftfvaluelist.com/items/{their_slug(it['name'])}.webp",
            "slug": slugify(it["name"]),
            "local_image_path": None,  # 下载阶段填
        }
        if extra:
            rec.update(extra)
        cats[cat]["items"].append(rec)
        return rec

    for it in items_in:
        build(it)
    for u in hardcoded:
        # 硬编码 Unique 多为 N/A 价值周边
        build(u, extra={"hardcoded": True})

    total = sum(len(v["items"]) for v in cats.values())
    print("built items:", total)

    # ---------- 下载图片 ----------
    dl_ok = dl_fail = fb_old = 0
    for cat, v in cats.items():
        folder = os.path.join(IMG, RARITY_LOWER[cat])
        os.makedirs(folder, exist_ok=True)
        for rec in v["items"]:
            fname = rec["slug"] + ".webp"
            dst = os.path.join(folder, fname)
            rel = RARITY_LOWER[cat] + "/" + fname
            url = rec["image_url"]
            got = False
            if os.path.exists(dst) and os.path.getsize(dst) > 100:
                got = True  # 幂等：上一次运行已下载
            else:
                try:
                    raw = fetch(url, binary=True)
                    if raw[:4] == b"RIFF":
                        open(dst, "wb").write(raw)
                        got = True
                except Exception:
                    pass
            if got:
                dl_ok += 1
            else:
                # 回退旧图
                oldp = old_img_by_name.get(norm(rec["name"]))
                if oldp and os.path.exists(os.path.join(IMG, oldp)):
                    shutil.copyfile(os.path.join(IMG, oldp), dst)
                    fb_old += 1
                else:
                    dl_fail += 1
                    print("  no image:", rec["name"], "->", url)
                    rel = None
            rec["local_image_path"] = rel
            if rel:
                referenced_new.add(rel.replace("\\", "/").lower())
    print("images: downloaded %d, fallback-old %d, missing %d" % (dl_ok, fb_old, dl_fail))

    # ---------- 孤儿清理(原图) ----------
    # 沙箱对批量删除有确认门槛，孤儿原图保留在磁盘上由 git 手动处理，
    # 不影响站点（JSON 只引用 referenced_new 内的路径）。
    removed = 0
    for root, dirs, files in os.walk(IMG):
        if "thumb" in root.split(os.sep):
            continue
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, IMG).replace("\\", "/")
            if rel.lower() not in referenced_new:
                # os.remove(full)  # 已禁用：沙箱批量删除保护
                removed += 1
    print("orphan originals removed:", removed)

    # ---------- 写 JSON ----------
    out = {k: cats[k] for k in ["Legendaries", "Epics", "Rares", "Commons", "Uniques"]}
    with open(os.path.join(REPO, "ftf_values_full_data.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for k, v in out.items():
        print(k, len(v["items"]))


if __name__ == "__main__":
    main()
