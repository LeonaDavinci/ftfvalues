#!/usr/bin/env python3
"""
FTF Values 静态页面爬取脚本 v2.0
爬取 Home, UseGuide, Changelog, FAQ 四个页面完整内容
"""

import json
import os
import time
import re
from bs4 import BeautifulSoup

# ============================================================
# 配置
# ============================================================
BASE_URL = "https://ftf-values.base44.app"
OUTPUT_DIR = "page_contents"
PAGES = [
    ("/",            "home"),
    ("/Home",        "home"),
    ("/UseGuide",    "useguide"),
    ("/Changelog",   "changelog"),
    ("/FAQ",         "faq"),
]

# ============================================================
# 启动浏览器
# ============================================================
def start_browser():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(user_agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ))
    return pw, browser, page

def close_browser(pw, browser):
    browser.close()
    pw.stop()

# ============================================================
# 爬取单个页面
# ============================================================
def scrape_page(page, path, name):
    url = BASE_URL + path
    print(f"\n{'='*60}")
    print(f"  爬取: {name.upper()}  ({path})")
    print(f"  URL: {url}")
    print(f"{'='*60}")

    try:
        page.goto(url, timeout=30000, wait_until="networkidle")
        time.sleep(3)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
    except Exception as e:
        print(f"  页面加载超时: {e}")
        try:
            page.goto(url, timeout=15000)
            time.sleep(4)
        except:
            print(f"  跳过 {name}")
            return None

    html = page.content()
    soup = BeautifulSoup(html, "lxml")

    # 提取标题
    title = ""
    for sel in ["h1", "title", ".page-title", "[class*='title']"]:
        el = soup.select_one(sel)
        if el and el.text.strip():
            title = el.text.strip()
            break
    if not title:
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else name

    # 提取主内容区
    main_text = ""
    for sel in ["main", "article", ".content", "#content", ".page-content", "body"]:
        el = soup.select_one(sel)
        if el:
            main_text = el.get_text(separator="\n", strip=True)
            break

    # 提取所有标题
    headers = []
    for h in soup.find_all(["h1","h2","h3","h4","h5"]):
        txt = h.get_text(strip=True)
        if txt:
            headers.append({"level": int(h.name[1]), "text": txt})

    # 提取所有链接
    links = []
    for a in soup.find_all("a", href=True):
        txt = a.get_text(strip=True)
        href = a["href"]
        if txt or href.startswith("http"):
            links.append({"text": txt or href, "url": href})

    # 提取所有图片
    images = []
    for img in soup.find_all("img", src=True):
        src = img["src"]
        alt = img.get("alt", "")
        images.append({"src": src, "alt": alt})

    # 下载图片
    img_dir = os.path.join("images", "pages", name)
    os.makedirs(img_dir, exist_ok=True)
    downloaded = []
    for img in images:
        src = img["src"]
        if not src.startswith("http"):
            src = BASE_URL + ("" if src.startswith("/") else "/") + src
        try:
            import requests
            r = requests.get(src, timeout=10, headers={"Referer": BASE_URL})
            if r.status_code == 200:
                fname = os.path.basename(img["src"].split("?")[0]) or f"{len(downloaded)}.png"
                fpath = os.path.join(img_dir, fname)
                with open(fpath, "wb") as f:
                    f.write(r.content)
                downloaded.append({"original": img["src"], "local": f"images/pages/{name}/{fname}", "alt": img["alt"]})
                print(f"    [图片] {fname}")
        except Exception as e:
            pass

    result = {
        "page_name": name,
        "path": path,
        "url": url,
        "title": title,
        "headers": headers,
        "main_text": main_text[:10000],
        "links": links[:50],
        "images": downloaded,
        "raw_html_sample": html[:5000],
    }

    # 保存原始文本
    txt_path = os.path.join(OUTPUT_DIR, f"{name}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"URL: {url}\n\n")
        f.write("## 标题结构\n\n")
        for h in headers:
            f.write(f"{'#'*h['level']} {h['text']}\n")
        f.write("\n## 主要内容\n\n")
        f.write(main_text)
        f.write("\n\n## 链接\n\n")
        for link in links[:50]:
            f.write(f"- [{link['text']}]({link['url']})\n")
        f.write("\n## 图片\n\n")
        for img in downloaded:
            f.write(f"- {img['local']} (alt: {img['alt']})\n")

    print(f"  [标题] {title}")
    print(f"  [标题数] {len(headers)}")
    print(f"  [链接数] {len(links)}")
    print(f"  [图片数] {len(downloaded)}")
    print(f"  [内容长度] {len(main_text)} 字符")
    print(f"  已保存到: {txt_path}")

    return result

# ============================================================
# 主函数
# ============================================================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("images/pages", exist_ok=True)

    pw, browser, page = start_browser()
    results = []

    try:
        seen = set()
        for path, name in PAGES:
            key = f"{path}_{name}"
            if key in seen:
                continue
            seen.add(key)
            r = scrape_page(page, path, name)
            if r:
                results.append(r)
    finally:
        close_browser(pw, browser)

    # 保存 JSON
    json_path = os.path.join(OUTPUT_DIR, "all_pages.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"  全部完成！共爬取 {len(results)} 个页面")
    print(f"  JSON: {json_path}")
    print(f"  文本: {OUTPUT_DIR}/*.txt")
    print(f"  图片: images/pages/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
