#!/usr/bin/env python3
"""
Update all HTML files in seo_pages/ with new navigation.
Run: python update_all_nav2.py
"""
import os
import re

SEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seo_pages')

# New header template - page arg determines which link gets class="act"
def make_header(active):
    pre = ' class="act"' if active == 'sets' else ''
    lre = ' class="act"' if active == 'legendaries' else ''
    ere = ' class="act"' if active == 'epics' else ''
    rre = ' class="act"' if active == 'rares' else ''
    cre = ' class="act"' if active == 'commons' else ''
    return (
        '<header>\n'
        '  <div class="logo">FTF Values</div>\n'
        '\n'
        '  <!-- Main Nav - 5 item categories (prominent position) -->\n'
        '  <nav class="main-nav" id="mainNav">\n'
        '    <a href="sets.html"' + pre + '>Bundles</a>\n'
        '    <a href="legendaries.html"' + lre + '>Legendaries</a>\n'
        '    <a href="epics.html"' + ere + '>Epics</a>\n'
        '    <a href="rares.html"' + rre + '>Rares</a>\n'
        '    <a href="commons.html"' + cre + '>Commons</a>\n'
        '  </nav>\n'
        '\n'
        '  <!-- More menu (secondary pages) -->\n'
        '  <div class="nav-more">\n'
        '    <button class="nav-more-btn" onclick="toggleMoreMenu()" aria-label="More pages">&#9881; More</button>\n'
        '    <div class="nav-more-menu" id="moreMenu">\n'
        '      <a href="index.html">&#127968; Home</a>\n'
        '      <a href="use-guide.html">&#128214; Use Guide</a>\n'
        '      <a href="changelog.html">&#128221; Changelog</a>\n'
        '      <a href="faq.html">&#10067; FAQ</a>\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <!-- Mobile menu button -->\n'
        '  <button class="mobile-menu-btn" onclick="toggleMobileMenu()" aria-label="Toggle menu">&#9776;</button>\n'
        '</header>\n'
    )

# Nav CSS to inject (once per page)
NAV_CSS = (
    '\n    /* === Nav CSS === */\n'
    '    .main-nav{display:flex;gap:2px;flex-wrap:wrap;justify-content:center;flex:1;margin:0 16px}\n'
    '    .main-nav a{padding:6px 14px;border-radius:6px;font-size:0.85rem;font-weight:600;transition:all 0.2s;white-space:nowrap;color:#e0e0e0;text-decoration:none}\n'
    '    .main-nav a:hover,.main-nav a.act{background:rgba(233,69,96,0.13);color:#e94560}\n'
    '    .nav-more{position:relative}\n'
    '    .nav-more-btn{background:none;border:1px solid #333;border-radius:6px;color:#a0a0b0;padding:6px 12px;cursor:pointer;font-size:0.85rem;transition:all 0.2s;white-space:nowrap}\n'
    '    .nav-more-btn:hover{background:#2a2a3e;color:#e0e0e0;border-color:#555}\n'
    '    .nav-more-menu{display:none;position:absolute;right:0;top:100%;margin-top:6px;background:#1a1a2e;border:1px solid #2a2a4e;border-radius:8px;padding:6px 0;min-width:160px;box-shadow:0 8px 30px rgba(0,0,0,0.4);z-index:200}\n'
    '    .nav-more-menu.show{display:block}\n'
    '    .nav-more-menu a{display:block;padding:8px 16px;color:#a0a0b0;font-size:0.85rem;transition:all 0.15s;text-decoration:none}\n'
    '    .nav-more-menu a:hover{background:#2a2a3e;color:#e94560}\n'
    '    .mobile-menu-btn{display:none;background:none;border:none;color:#e0e0e0;font-size:1.4rem;cursor:pointer;padding:4px 8px}\n'
    '    @media(max-width:900px){header{padding:0 12px;height:50px}.main-nav{gap:1px}.main-nav a{font-size:0.78rem;padding:5px 8px}.logo{font-size:1.1rem}}\n'
    '    @media(max-width:768px){.mobile-menu-btn{display:block}.main-nav{display:none;position:absolute;top:50px;left:0;right:0;background:#1a1a2e;border-bottom:2px solid #e94560;padding:8px 12px;flex-wrap:wrap;gap:4px;justify-content:flex-start}.main-nav.show{display:flex}.main-nav a{padding:8px 12px;font-size:0.85rem}}\n'
)

MOBILE_JS = (
    '<script>\n'
    'function toggleMoreMenu(){document.getElementById("moreMenu").classList.toggle("show")}\n'
    'function toggleMobileMenu(){document.getElementById("mainNav").classList.toggle("show")}\n'
    'document.addEventListener("click",function(e){\n'
    '  var mm=document.getElementById("moreMenu");\n'
    '  if(mm&&!e.target.closest(".nav-more"))mm.classList.remove("show");\n'
    '});\n'
    '</script>\n'
)

def update_file(fpath, active_key):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # 1. Replace header
    new_hdr = make_header(active_key)
    # Match <header ...> ... </header> (non-greedy)
    hdr_re = re.compile(r'<header[^>]*>.*?</header>', re.DOTALL | re.IGNORECASE)
    c = hdr_re.sub(new_hdr, c, count=1)

    # 2. Fix home.html -> index.html
    c = c.replace('href="home.html"', 'href="index.html"')
    c = c.replace("href='home.html'", "href='index.html'")
    c = c.replace('href="/">', 'href="index.html">')
    c = c.replace('href="/use-guide">', 'href="use-guide.html">')
    c = c.replace('href="/changelog">', 'href="changelog.html">')
    c = c.replace('href="/faq">', 'href="faq.html">')
    c = c.replace('href="/sets">', 'href="sets.html">')

    # 3. Inject NAV_CSS before </style>
    if 'main-nav' not in c:
        c = c.replace('</style>', NAV_CSS + '  </style>', 1)

    # 4. Inject MOBILE_JS before </body>
    if 'toggleMoreMenu' not in c:
        c = c.replace('</body>', MOBILE_JS + '</body>', 1)

    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False


def main():
    tasks = [
        ('index.html',       'index'),
        ('sets.html',        'sets'),
        ('legendaries.html', 'legendaries'),
        ('epics.html',      'epics'),
        ('rares.html',      'rares'),
        ('commons.html',    'commons'),
        ('use-guide.html',  'use-guide'),
        ('changelog.html',  'changelog'),
        ('faq.html',        'faq'),
    ]
    for fname, key in tasks:
        fp = os.path.join(SEO, fname)
        if not os.path.exists(fp):
            print('  [SKIP - not found] ' + fname)
            continue
        ok = update_file(fp, key)
        st = 'UPDATED' if ok else 'UNCHANGED'
        print('  [' + st + '] ' + fname)

if __name__ == '__main__':
    main()
