#!/usr/bin/env python3
"""
Update all HTML files in seo_pages/ to use the new navigation structure.
Run from project root:  python update_all_nav.py
"""
import os
import re

PAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seo_pages')

# Header template - {} is replaced with page-specific class="act" markers
# We generate one header per page by string replacement.
# Keys: sets / legendaries / epics / rares / commons / index / use-guide / changelog / faq
def make_header(active_page):
    # active_page: one of 'sets','legendaries','epics','rares','commons','index','use-guide','changelog','faq'
    items = [
        ('sets.html',        'Bundles',     'sets'),
        ('legendaries.html', 'Legendaries',  'legendaries'),
        ('epics.html',      'Epics',       'epics'),
        ('rares.html',      'Rares',       'rares'),
        ('commons.html',    'Commons',     'commons'),
    ]
    more_items = [
        ('index.html',       'Home'),
        ('use-guide.html',  'Use Guide'),
        ('changelog.html',  'Changelog'),
        ('faq.html',        'FAQ'),
    ]
    lines = []
    lines.append('<header>')
    lines.append('  <div class="logo">FTF Values</div>')
    lines.append('')
    lines.append('  <!-- Main Nav - 5 item categories (prominent position) -->')
    lines.append('  <nav class="main-nav" id="mainNav">')
    for href, label, key in items:
        cls = ' class="act"' if key == active_page else ''
        lines.append('    <a href="{}"{}>{}</a>'.format(href, cls, label))
    lines.append('  </nav>')
    lines.append('')
    lines.append('  <!-- More menu (secondary pages) -->')
    lines.append('  <div class="nav-more">')
    lines.append('    <button class="nav-more-btn" onclick="toggleMoreMenu()" aria-label="More pages">&#9881; More</button>')
    lines.append('    <div class="nav-more-menu" id="moreMenu">')
    for href, label in more_items:
        lines.append('      <a href="{}">{}</a>'.format(href, label))
    lines.append('    </div>')
    lines.append('  </div>')
    lines.append('')
    lines.append('  <!-- Mobile menu button -->')
    lines.append('  <button class="mobile-menu-btn" onclick="toggleMobileMenu()" aria-label="Toggle menu">&#9776;</button>')
    lines.append('</header>')
    return '\n'.join(lines)


def get_active_key(filename):
    mapping = {
        'index.html':       'index',
        'sets.html':        'sets',
        'legendaries.html': 'legendaries',
        'epics.html':      'epics',
        'rares.html':      'rares',
        'commons.html':    'commons',
        'use-guide.html':  'use-guide',
        'changelog.html':  'changelog',
        'faq.html':        'faq',
    }
    return mapping.get(filename, 'index')


NAV_CSS = (
    '.main-nav{display:flex;gap:2px;flex-wrap:wrap;'
    'justify-content:center;flex:1;margin:0 16px}'
    '.main-nav a{padding:6px 14px;border-radius:6px;font-size:0.85rem;'
    'font-weight:600;transition:all 0.2s;white-space:nowrap;'
    'color:#e0e0e0;text-decoration:none}'
    '.main-nav a:hover,.main-nav a.act{background:rgba(233,69,96,0.13);color:#e94560}'
    '.nav-more{position:relative}'
    '.nav-more-btn{background:none;border:1px solid #333;border-radius:6px;'
    'color:#a0a0b0;padding:6px 12px;cursor:pointer;font-size:0.85rem;'
    'transition:all 0.2s;white-space:nowrap}'
    '.nav-more-btn:hover{background:#2a2a3e;color:#e0e0e0;border-color:#555}'
    '.nav-more-menu{display:none;position:absolute;right:0;top:100%;'
    'margin-top:6px;background:#1a1a2e;border:1px solid #2a2a4e;'
    'border-radius:8px;padding:6px 0;min-width:160px;'
    'box-shadow:0 8px 30px rgba(0,0,0,0.4);z-index:200}'
    '.nav-more-menu.show{display:block}'
    '.nav-more-menu a{display:block;padding:8px 16px;color:#a0a0b0;'
    'font-size:0.85rem;transition:all 0.15s;text-decoration:none}'
    '.nav-more-menu a:hover{background:#2a2a3e;color:#e94560}'
    '.mobile-menu-btn{display:none;background:none;border:none;color:#e0e0e0;'
    'font-size:1.4rem;cursor:pointer;padding:4px 8px}'
    '@media(max-width:900px){header{padding:0 12px;height:50px}'
    '.main-nav{gap:1px}.main-nav a{font-size:0.78rem;padding:5px 8px}'
    '.logo{font-size:1.1rem}}'
    '@media(max-width:768px){'
    '.mobile-menu-btn{display:block}'
    '.main-nav{display:none;position:absolute;top:50px;left:0;right:0;'
    'background:#1a1a2e;border-bottom:2px solid #e94560;'
    'padding:8px 12px;flex-wrap:wrap;gap:4px;justify-content:flex-start}'
    '.main-nav.show{display:flex}'
    '.main-nav a{padding:8px 12px;font-size:0.85rem}}'
)

MOBILE_JS = (
    '<script>'
    'function toggleMoreMenu(){document.getElementById("moreMenu").classList.toggle("show")}'
    'function toggleMobileMenu(){document.getElementById("mainNav").classList.toggle("show")}'
    'document.addEventListener("click",function(e){'
    'var mm=document.getElementById("moreMenu");'
    'if(mm&&!e.target.closest(".nav-more"))mm.classList.remove("show");});'
    '</script>'
)


def update_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    active = get_active_key(filename)
    new_header = make_header(active)

    # 1. Replace old <header>...</header> (match greedily with DOTALL)
    header_re = re.compile(r'<header[^>]*>.*?</header>', re.DOTALL | re.IGNORECASE)
    content = header_re.sub(new_header, content, count=1)

    # 2. Fix home.html -> index.html everywhere in <a> tags
    content = content.replace('href="home.html"', 'href="index.html"')
    content = content.replace("href='home.html'", "href='index.html'")
    # Fix href="/" style links
    content = content.replace('href="/">Home<', 'href="index.html">Home<')
    content = content.replace('href="/use-guide">', 'href="use-guide.html">')
    content = content.replace('href="/changelog">', 'href="changelog.html">')
    content = content.replace('href="/faq">', 'href="faq.html">')
    content = content.replace('href="/sets">', 'href="sets.html">')

    # 3. Inject NAV_CSS into <style> block (before existing content, after <style>)
    if 'main-nav' not in content:
        # Insert before the first </style>
        # We insert after <style> tag content starts - just before existing rules
        # Simple approach: append before </style>
        nav_css_str = '\n    /* === Nav CSS === */\n    ' + NAV_CSS + '\n'
        content = content.replace('</style>', nav_css_str + '  </style>', 1)

    # 4. Inject mobile menu JS before </body>
    if 'toggleMoreMenu' not in content:
        content = content.replace('</body>', MOBILE_JS + '\n</body>', 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    files = [
        'index.html',
        'sets.html',
        'legendaries.html',
        'epics.html',
        'rares.html',
        'commons.html',
        'use-guide.html',
        'changelog.html',
        'faq.html',
    ]
    for fname in files:
        fpath = os.path.join(PAGES_DIR, fname)
        if not os.path.exists(fpath):
            print('  [SKIP - not found] ' + fname)
            continue
        changed = update_file(fpath, fname)
        status = 'UPDATED' if changed else 'UNCHANGED'
        print('  [' + status + '] ' + fname)

if __name__ == '__main__':
    main()
