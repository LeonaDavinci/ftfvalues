#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 index.html / home.html / seo_pages/index.html 里的 Bundles(Sets) 预览区
替换为 Uniques 预览区（数据来自新的 ftf_values_full_data.json），
并更新导航、hero 按钮、页脚链接。

幂等：重复运行结果一致。
"""

import json, os, re

REPO = r"C:\Users\star\WorkBuddy\2026-06-23-02-05-48"

IMG_FALLBACK = ('onerror="this.onerror=null;this.src=&quot;data:image/svg+xml,'
                '%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E'
                '%3Crect fill=%22%23222%22 width=%22100%22 height=%22100%22/%3E'
                '%3Ctext fill=%22%23888%22 x=%2250%25%22 y=%2250%25%22 '
                'dominant-baseline=%22middle%22 text-anchor=%22middle%22%3EIMG%3C/text%3E'
                '%3C/svg%3E&quot;"')

COLOR = '#ffaa00'
STABILITY_COLORS = {
    'Rising': '#2ecc71', 'Stable': '#3498db', 'Fluctuating': '#f39c12',
    'Dropping': '#e74c3c', 'Volatile': '#9b59b6', 'Unstable': '#e67e22',
    'Stable-Ish': '#1abc9c', 'Undetermined': '#95a5a6',
}


def stars(n):
    if n is None:
        full = 0
    else:
        try:
            full = max(0, min(5, int(round(float(n)))))
        except (TypeError, ValueError):
            full = 0
    return '&#9733;' * full + '&#9734;' * (5 - full)


def mini_card(it):
    local = (it.get('local_image_path') or '').replace(' ', '%20')
    img = '../images/' + local if local else (it.get('image_url') or '')
    name = it['name'].replace('"', '&quot;')
    val = str(it['value']) if it.get('value') is not None else 'N/A'
    stab = it.get('stability') or 'Stable'
    sc = STABILITY_COLORS.get(stab, '#95a5a6')
    ds = stars(it.get('demand'))
    return (
        '<a href="uniques.html#{slug}" class="mc" data-v="{v}">'
        '<div class="mi"><img src="{img}" alt="{name}" loading="lazy" {fb}></div>'
        '<div class="mn">{name}</div>'
        '<div class="mv" style="color:{color}">&#9889; {val}</div>'
        '<div class="mt"><span class="ms" style="background:{sc}22;color:{sc};border:1px solid {sc}">{stab}</span></div>'
        '<div class="md"><span class="mds" style="color:#f1c40f">{ds}</span></div>'
        '</a>'.format(slug=it.get('slug', ''), v=it['value'] if it.get('value') is not None else 0,
                      img=img, fb=IMG_FALLBACK, name=name, val=val, color=COLOR, sc=sc, stab=stab, ds=ds))


def uniques_section(data):
    items = data['Uniques']['items']
    top = sorted(items, key=lambda x: (x.get('value') is None, -(x.get('value') or 0)))[:12]
    cards = '\n'.join(mini_card(it) for it in top)
    return '''<section class="ps" id="uniques">
      <div class="psh">
        <h2 style="color:{color}">&#127753; Uniques</h2>
        <a href="uniques.html" class="psl" style="border-color:{color};color:{color}">View All {count} Items &rarr;</a>
      </div>
      <div class="psg">{cards}</div>
    </section>'''.format(color=COLOR, count=len(items), cards=cards)


def transform(html, data):
    # 1) 导航 + 页脚 + hero 链接
    html = html.replace('<a href="sets.html">Bundles</a>', '<a href="uniques.html">Uniques</a>')
    html = html.replace('Browse Bundles', 'Browse Uniques')
    # 2) 整段替换 sets 预览区
    sec_new = uniques_section(data)
    html, n = re.subn(r'<section class="ps" id="sets">.*?</section>', sec_new, html, count=1, flags=re.S)
    print('  sets section replaced:', n)
    # 3) 兜底：任何残留 sets.html 引用 -> uniques.html
    html = html.replace('sets.html', 'uniques.html')
    return html


def main():
    data = json.load(open(os.path.join(REPO, 'ftf_values_full_data.json'), encoding='utf-8'))
    for f in ['index.html', 'home.html', 'seo_pages/index.html']:
        p = os.path.join(REPO, f)
        html = open(p, encoding='utf-8').read()
        before = html.count('sets.html')
        html = transform(html, data)
        open(p, 'w', encoding='utf-8', newline='\n').write(html)
        print(f, '| sets refs', before, '->', html.count('sets.html'),
              '| uniques section', html.count('id="uniques"'))


if __name__ == '__main__':
    main()
