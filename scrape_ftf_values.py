#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FTF Values Data Extractor v3 - Pure HTML Parser + Image Downloader
Parses saved HTML files, extracts item data, downloads all images.
No browser needed - works from saved debug HTML files.
"""

import json
import os
import re
import sys
import io
from urllib.parse import unquote

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from bs4 import BeautifulSoup
import requests

OUTPUT_DIR = r"C:\Users\star\WorkBuddy\2026-06-23-02-05-48"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
DATA_FILE = os.path.join(OUTPUT_DIR, "ftf_values_full_data.json")
SQL_FILE = os.path.join(OUTPUT_DIR, "ftf_values_data.sql")

# Page config: HTML file -> page name -> rarity
PAGE_CONFIGS = [
    ("debug_sets.html",       "Sets",        "set"),
    ("debug_legendaries.html","Legendaries", "legendary"),
    ("debug_epics.html",     "Epics",       "epic"),
    ("debug_rares.html",     "Rares",       "rare"),
    ("debug_commons.html",   "Commons",     "common"),
]


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def clean_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\s+', '_', name.strip())
    return name[:80]


def parse_html_file(html_path: str, page_name: str, rarity: str) -> dict:
    """Parse a single saved HTML file and extract all items"""
    print(f"\n{'='*60}")
    print(f"[PARSE] {page_name} <- {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Extract metadata from body text
    body_text = soup.get_text(separator='\n')
    meta = {}
    dm = re.search(r'Last\s+Updated[:\s]+(.+?)(?:\n|$)', body_text)
    if dm:
        meta['last_updated'] = dm.group(1).strip()
    vm = re.search(r'Total\s*Value\s*[:\s]*(\d[\d,]*)', body_text, re.I)
    if vm:
        meta['total_value'] = int(vm.group(1).replace(',', ''))
    cm = re.search(r'Items?\s*[:\s]*(\d+)', body_text, re.I)
    if cm:
        meta['items_count'] = int(cm.group(1))
    print(f"  [META] {meta}")

    # ===== Find all item images =====
    # Strategy: find img tags with alt + object-contain/object-cover class
    # Skip display:none images and FTF icon
    seen_names = set()
    items = []
    
    for img in soup.find_all('img'):
        src = (img.get('src') or '').strip()
        alt = (img.get('alt') or '').strip()
        cls = (img.get('class') or [])
        style = (img.get('style') or '').strip()
        
        cls_str = ' '.join(cls) if isinstance(cls, list) else str(cls)
        
        # Must have alt attribute with a real name
        if not alt or alt.lower() == 'ftf icon':
            continue
        
        # Must be content image
        if not ('object-contain' in cls_str or 'object-cover' in cls_str):
            continue
        
        # Skip hidden
        if 'display' in style and 'none' in style:
            continue
        
        # Skip duplicates
        if alt in seen_names:
            continue
        seen_names.add(alt)
        
        # Find the card container by walking up
        container = img.parent
        for _ in range(5):
            if container is None:
                break
            t = container.get_text(strip=True)
            if len(t) > 15 and len(t) < 400 and alt in t:
                break
            container = container.parent
        else:
            container = img.parent  # fallback to immediate parent
        
        # Collect all text nodes from container
        raw_texts = []
        if container:
            for text_node in container.find_all(text=True):
                tx = text_node.strip()
                if tx:
                    raw_texts.append(tx)
        
        # Parse fields from texts
        value = None
        value_min = None
        value_max = None
        stability = None
        demand = None
        
        for t in raw_texts:
            ts = t.strip()
            tl = ts.lower().strip()

            if tl in ('demand', 'value', 'stability', 'status'):
                continue
            
            if tl in ('legendary','legendaries','epic','epics',
                      'rare','rares','common','commons'):
                continue
                
            stab_kw = {'stable','rising','doing well','dropping',
                        'fluctuating','struggling','improving','receding'}
            if tl in stab_kw:
                stability = tl.title()
                continue

            full_stars = sum(1 for c in ts if c in '\u2605\u2b50')
            empty_stars = sum(1 for c in ts if c in '\u2606\u2b51\u25c7')
            if full_stars > 0 or empty_stars > 0:
                demand = full_stars
                continue

            nm = re.match(r'^(\d{1,5})$', ts)
            if nm:
                v = int(nm.group(1))
                if value is None:
                    value = v
                elif value_min is None and abs(v - value) <= max(value * 0.3, 10):
                    lo, hi = min(value, v), max(value, v)
                    value_min, value_max = lo, hi
                continue

            rm = re.match(r'^(\d+)\s*-\s*(\d+)$', ts)
            if rm:
                lo, hi = int(rm.group(1)), int(rm.group(2))
                value_min, value_max = lo, hi
                if value is None:
                    value = lo
                continue

        # Determine image extension
        ext = "png"
        if src:
            sl = src.lower()
            if '.webp' in sl: ext = "webp"
            elif any(x in sl for x in ['.jpg', '.jpeg']): ext = "jpg"
            elif '.gif' in sl: ext = "gif"
        
        subfolder = rarity if rarity != 'set' else 'sets'
        
        item = {
            "id": len(items) + 1,
            "name": alt,
            "rarity": rarity,
            "value": value or 0,
            "value_min": value_min,
            "value_max": value_max,
            "stability": stability or "Stable",
            "demand": demand,
            "status": None,
            "image_url": src,
            "slug": clean_filename(alt).lower(),
            "local_image_path": f"{subfolder}/{clean_filename(alt)}.{ext}",
        }
        items.append(item)

    print(f"  [OK] Found {len(items)} items")
    
    return {
        "page_name": page_name,
        "page_url": f"https://ftf-values.base44.app/{page_name}",
        "metadata": meta,
        "items": items,
    }


def download_images(data: dict):
    """Download all item images to local disk"""
    print(f"\n{'='*60}")
    print(f"[IMG] Downloading images...")
    
    total = sum(len(d['items']) for d in data.values())
    ok = fail = skip = 0
    
    for pdata in data.values():
        subfolder = pdata['items'][0]['rarity'] if pdata['items'] else 'unknown'
        ensure_dir(os.path.join(IMAGES_DIR, subfolder))
        
        for item in pdata['items']:
            url = item.get('image_url', '')
            local_path = item.get('local_image_path', '')
            
            if not url:
                skip += 1
                continue
            
            save_to = os.path.join(IMAGES_DIR, local_path)
            
            if os.path.exists(save_to) and os.path.getsize(save_to) > 200:
                ok += 1
                continue
            
            try:
                r = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Referer': 'https://ftf-values.base44.app/',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                }, timeout=20, stream=True)
                
                if r.status_code == 200 and len(r.content) > 200:
                    ensure_dir(os.path.dirname(save_to))
                    with open(save_to, 'wb') as f:
                        f.write(r.content)
                    ok += 1
                else:
                    fail += 1
            except Exception:
                fail += 1
            
            if (ok + fail) % 30 == 0 and (ok + fail) > 0:
                print(f"  [PROGRESS] {ok+fail}/{total} processed ({ok} OK, {fail} fail)")
    
    print(f"  [DONE] {ok} downloaded, {fail} failed, {skip} skipped / {total} total")


def generate_sql(data: dict):
    """Generate SQL INSERT statements for all scraped items"""
    lines = []
    lines.append("-- FTF Values - Full Item Data")
    lines.append("-- Auto-generated from ftf-values.base44.app scrape")
    lines.append("")
    
    item_id = 1
    for pdata in data.values():
        for item in pdata['items']:
            n = item['name'].replace("'", "\\'").replace('"', '\\"')
            s = item['slug'].replace("'", "\\'")
            r = item['rarity']
            v = item['value']
            vmin = str(item['value_min']) if item['value_min'] else 'NULL'
            vmax = str(item['value_max']) if item['value_max'] else 'NULL'
            st = item['stability']
            de = str(item['demand']) if item['demand'] else 'NULL'
            iu = item['image_url'].replace("'", "\\'") if item['image_url'] else ''
            li = item['local_image_path'].replace("'", "\\'") if item.get('local_image_path') else ''
            
            sql = (f"INSERT INTO items (id, name, slug, rarity, value, value_min, "
                   f"value_max, stability, demand, image_url, local_image, "
                   f"is_active, created_at) VALUES "
                   f"({item_id}, '{n}', '{s}', '{r}', {v}, {vmin}, {vmax}, "
                   f"'{st}', {de}, '{iu}', '{li}', 1, NOW());")
            lines.append(sql)
            item_id += 1
    
    with open(SQL_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\n[SQL] Generated: {SQL_FILE} ({item_id-1} rows)")


def main():
    ensure_dir(IMAGES_DIR)
    
    all_data = {}
    
    for html_file, page_name, rarity in PAGE_CONFIGS:
        html_path = os.path.join(OUTPUT_DIR, html_file)
        if not os.path.exists(html_path):
            print(f"  [SKIP] File not found: {html_file}")
            continue
        result = parse_html_file(html_path, page_name, rarity)
        all_data[page_name] = result
    
    # Save JSON
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n[JSON] Saved: {DATA_FILE}")
    
    # Generate SQL
    generate_sql(all_data)
    
    # Download images
    download_images(all_data)
    
    # Summary
    total = sum(len(d['items']) for d in all_data.values())
    print(f"\n{'='*60}")
    print(f"[FINAL SUMMARY]")
    print(f"{'='*60}")
    for pn, pd in all_data.items():
        n = len(pd['items'])
        m = pd.get('metadata', {})
        print(f"  {pn:12s}: {n:4d} items | TV={str(m.get('total_value','?')):>6s} "
              f"Cnt={str(m.get('items_count','?')):>4s} | Updated={m.get('last_updated','?')}")
    print(f"  {'TOTAL':12s}: {total:4d} items")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
