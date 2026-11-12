#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""faq / use-guide / changelog 系列页面的 Sets→Uniques 导航替换。幂等。"""
import os

REPO = r"C:\Users\star\WorkBuddy\2026-06-23-02-05-48"
FILES = ['faq.html', 'use-guide.html', 'changelog.html',
         'seo_pages/faq.html', 'seo_pages/use-guide.html', 'seo_pages/changelog.html']

for f in FILES:
    p = os.path.join(REPO, f)
    h = open(p, encoding='utf-8').read()
    n = h.count('<a href="sets.html">Bundles</a>')
    h = h.replace('<a href="sets.html">Bundles</a>', '<a href="uniques.html">Uniques</a>')
    h = h.replace('from Common consumables to Legendary bundles',
                  'from Common consumables to Legendary items')
    open(p, 'w', encoding='utf-8', newline='\n').write(h)
    print(f, '| replaced', n, '| residual sets.html:', h.count('sets.html'))
