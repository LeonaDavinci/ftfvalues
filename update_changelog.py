#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 ftfvaluelist.com API 的 changelog 数据重建 changelog.html 的版本区。
幂等：以 "<!-- FTF-CHANGELOG-START -->" 哨兵为界整段替换。
"""

import json, os, re

WS = r"E:\workbuddy\2026-09-29-22-21-39"
REPO = r"C:\Users\star\WorkBuddy\2026-06-23-02-05-48"

LABELS = {
    'Value Increase': 'label-value-up',
    'Value Decrease': 'label-value-down',
    'Demand Change': 'label-demand',
    'Description Change': 'label-desc',
    'New Item': 'label-new',
    'Correction': 'label-other',
}
LABEL_TEXT = {
    'Value Increase': 'Value Increase',
    'Value Decrease': 'Value Decrease',
    'Demand Change': 'Demand Change',
    'Description Change': 'Description Change',
    'New Item': 'New Items',
    'Correction': 'Correction',
}
ESC_IN = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}


def esc(s):
    for k, v in ESC_IN.items():
        s = s.replace(k, v)
    return s


def version_block(v, idx, total):
    label = v['version'].replace('Version 2,0', 'Version 2.0')
    badge = ''
    if idx == 0:
        badge = ' <span style="font-size:0.8rem; color:#22c55e; margin-left:0.5rem;">Latest</span>'
    dv = 'recent' if idx < 3 else 'major'
    cls = 'version version-3' if idx == 0 else 'version'

    # 按 type 分组
    groups = {}
    for ch in v['changes']:
        groups.setdefault(ch['type'], []).append(ch['description'])

    body = []
    for t, descs in groups.items():
        body.append('            <div class="change-group">')
        body.append('                <div class="change-label {}">{}</div>'.format(LABELS[t], esc(LABEL_TEXT[t])))
        for d in descs:
            body.append('                <div class="change-item">{}</div>'.format(esc(d)))
        body.append('            </div>')
    return '''    <!-- FTF-CHANGELOG-START -->
    <div class="{cls}" data-version="{dv}">
        <div class="version-header">
            <h3>{label}{badge}</h3>
            <span class="date">{date}</span>
        </div>
        <div class="version-body">
{body}
        </div>
    </div>'''.format(cls=cls, dv=dv, label=esc(label), badge=badge, date=esc(v['date']),
                     body='\n'.join(body))


def main():
    data = json.load(open(WS + r"\_api_ftf-changelog.json", encoding="utf-8"))
    versions = data['versions']
    blocks = '\n\n'.join(version_block(v, i, len(versions)) for i, v in enumerate(versions))
    # 首块去掉重复的 START 哨兵
    blocks = blocks.replace('<!-- FTF-CHANGELOG-START -->\n    <div class="version version-3"',
                            '<div class="version version-3"', 1)
    blocks = '    <!-- FTF-CHANGELOG-START -->\n' + blocks.lstrip()

    c = open(os.path.join(REPO, 'changelog.html'), encoding='utf-8').read()

    start = c.find('<!-- Version 3.6 -->')
    if start == -1:
        start = c.find('<!-- FTF-CHANGELOG-START -->')
    end_marker = '<div style="text-align:center; margin:3rem 0;'
    end = c.find(end_marker)
    assert start != -1 and end != -1 and end > start, (start, end)
    new = c[:start] + blocks + '\n\n    ' + c[end:]

    # 说明行 + 统计数字
    new = re.sub(r'Showing \d+(?: of \d+\+?)? versions\.',
                 'Showing all {} versions.'.format(len(versions)), new)
    new = new.replace('<div class="stat-num">30+</div>\n            <div class="stat-label">Versions Tracked</div>',
                      '<div class="stat-num">{}</div>\n            <div class="stat-label">Versions Tracked</div>'.format(len(versions)))
    new = new.replace('<div class="stat-num">625+</div>\n            <div class="stat-label">Items Tracked</div>',
                      '<div class="stat-num">485+</div>\n            <div class="stat-label">Items Tracked</div>')
    new = new.replace('Recent (v3.x)', 'Recent')

    open(os.path.join(REPO, 'changelog.html'), 'w', encoding='utf-8', newline='\n').write(new)
    print('changelog rebuilt | versions:', len(versions), '| len', len(new))


if __name__ == '__main__':
    main()
