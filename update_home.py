#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 home.html：
1. 导航链接改为相对路径
2. 增加5个栏目（Bundles/Legendaries/Epics/Rares/Commons）的物品预览区
"""

import json, os, textwrap

with open('ftf_values_full_data.json', 'r', encoding='utf-8') as f:
    ALL_DATA = json.load(f)

STABILITY_COLORS = {
    'Rising': '#2ecc71', 'Stable': '#3498db', 'Fluctuating': '#f39c12',
    'Dropping': '#e74c3c', 'Volatile': '#9b59b6', 'Unstable': '#e67e22',
    'Stable-Ish': '#1abc9c', 'Undetermined': '#95a5a6',
}
RARITY_MAP = {
    'set': 'Sets',
    'legendary': 'Legendaries',
    'epic': 'Epics',
    'rare': 'Rares',
    'common': 'Commons',
}

CONFIG = {
    'Sets':      {'name': 'Bundles & Sets', 'emoji': '🎁', 'color': '#e94560', 'file': 'sets.html'},
    'Legendaries': {'name': 'Legendaries',     'emoji': '👑', 'color': '#f1c40f', 'file': 'legendaries.html'},
    'Epics':     {'name': 'Epics',           'emoji': '💎', 'color': '#9b59b6', 'file': 'epics.html'},
    'Rares':     {'name': 'Rares',           'emoji': '🔥', 'color': '#e74c3c', 'file': 'rares.html'},
    'Commons':   {'name': 'Commons',         'emoji': '✨', 'color': '#3498db', 'file': 'commons.html'},
}

def demand_stars(n):
    if n is None:
        return '☆☆☆☆☆'
    n = int(n)
    full = min(5, n // 2 + (1 if n % 2 else 0))
    return '★' * full + '☆' * (5 - full)

def mini_card(it, color):
    """首页预览用的小卡片（只显示图片、名称、价值）"""
    local = it.get('local_image_path', '')
    if local:
        img = '../images/' + local.replace(' ', '%20')
    else:
        img = it.get('image_url', '')
    name = it['name'].replace('"', '&quot;')
    val = str(it['value'])
    stab = it.get('stability', '')
    sc = STABILITY_COLORS.get(stab, '#95a5a6')
    ds = demand_stars(it.get('demand'))
    # 映射 rarity 到 CONFIG 键
    rar = it.get('rarity', 'set')
    cfg_key = RARITY_MAP.get(rar, 'Sets')
    cfg_file = CONFIG[cfg_key]['file']

    return (
        '<a href="{}" class="mc" data-v="{}">'
        '<div class="mi"><img src="{}" alt="{}" loading="lazy" onerror="this.onerror=null;this.src=&quot;data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect fill=%22%23222%22 width=%22100%22 height=%22100%22/%3E%3Ctext fill=%22%23888%22 x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22%3EIMG%3C/text%3E%3C/svg%3E&quot;"></div>'
        '<div class="mn">{}</div>'
        '<div class="mv" style="color:{}">&#9889; {}</div>'
        '<div class="mt"><span class="ms" style="background:{}22;color:{};border:1px solid {}">{}</span></div>'
        '<div class="md"><span class="mds" style="color:#f1c40f">{}</span></div>'
        '</a>'.format(
            cfg_file + '#' + it.get('slug', ''),
            it['value'], img, name, name, val,
            color, sc, sc, sc, stab, ds
        )
    )

def preview_section(key):
    cfg = CONFIG[key]
    items = ALL_DATA.get(key, {}).get('items', [])
    # 按价值降序取前12个
    top = sorted(items, key=lambda x: x.get('value', 0), reverse=True)[:12]
    cards = '\n'.join(mini_card(it, cfg['color']) for it in top)
    count = len(items)
    return '''
    <section class="ps" id="{}">
      <div class="psh">
        <h2 style="color:{}"><a href="{}" style="color:{};text-decoration:none">{} {}</a></h2>
        <a href="{}" class="psl" style="border-color:{};color:{}">View All {} Items &rarr;</a>
      </div>
      <div class="psg">{}</div>
    </section>'''.format(
        key.lower(), cfg['color'], cfg['file'], cfg['color'],
        cfg['emoji'], cfg['name'],
        cfg['file'], cfg['color'], cfg['color'], count,
        cards
    )

home_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FTF Values - Flee the Facility Trading Value Guide & Item Calculator</title>
<meta name="description" content="The ultimate Flee the Facility value guide. Check item values, stability tags, demand ratings for Legendary, Epic, Rare and Common items. Updated daily.">
<meta name="keywords" content="Flee the Facility, FTF, Roblox FTF, FTF values, FTF trading, FTF item values">
<link rel="canonical" href="https://yourdomain.com/">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;background:#0f0f1a;color:#e0e0e0}
a{text-decoration:none;color:inherit}
header{background:#1a1a2e;padding:10px 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #e94560;position:sticky;top:0;z-index:100;flex-wrap:wrap}
.logo{font-size:1.3rem;font-weight:700;color:#e94560}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#e0e0e0;padding:6px 12px;border-radius:6px;font-size:0.85rem;transition:all 0.2s}
nav a:hover,nav a.act{background:#e9456022;color:#e94560}
.hero{text-align:center;padding:64px 24px;background:radial-gradient(ellipse at center,#1a1a3e 0%,#0f0f1a 70%)}
.hero h1{font-size:3rem;background:linear-gradient(90deg,#e94560,#0f3460);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:16px}
.hero p{font-size:1.2rem;color:#a0a0b0;max-width:600px;margin:0 auto 24px}
.cb{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{padding:12px 28px;border-radius:8px;font-weight:600;transition:transform 0.2s,box-shadow 0.2s;cursor:pointer}
.bp{background:linear-gradient(135deg,#e94560,#c23152);color:#fff;border:none}
.bs{background:#16213e;color:#e94560;border:2px solid #e94560}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(233,69,96,0.3)}
.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;padding:40px 24px;max-width:1100px;margin:0 auto}
.fc{background:#1a1a2e;border-radius:12px;padding:24px;border:1px solid #2a2a4e;transition:transform 0.2s,border-color 0.2s}
.fc:hover{transform:translateY(-4px);border-color:#e94560}
.fc h3{color:#e94560;margin-bottom:10px}
.fc p{color:#a0a0b0;line-height:1.6;font-size:0.9rem}

/* Preview Sections */
.ps{padding:40px 24px;max-width:1400px;margin:0 auto}
.psh{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.psh h2{font-size:1.5rem}
.psl{font-size:0.85rem;padding:6px 16px;border:1px solid #555;border-radius:20px;transition:all 0.2s}
.psl:hover{background:rgba(255,255,255,0.05)}
.psg{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}

/* Mini Card */
.mc{display:block;background:#1a1a2e;border-radius:10px;overflow:hidden;border:1px solid #2a2a4e;transition:transform 0.2s,border-color 0.2s;padding-bottom:8px}
.mc:hover{transform:translateY(-3px);border-color:#e94560}
.mi{width:100%;aspect-ratio:1;background:#13132a;display:flex;align-items:center;justify-content:center;padding:6px}
.mi img{width:100%;height:100%;object-fit:contain}
.mn{font-size:0.8rem;font-weight:600;color:#f0f0f0;padding:6px 8px 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mv{font-size:0.9rem;font-weight:700;padding:0 8px 2px}
.mt{padding:0 8px 2px}
.ms{font-size:0.65rem;font-weight:600;padding:1px 6px;border-radius:8px}
.md{font-size:0.75rem;padding:0 8px}
.mds{letter-spacing:1px}

.community{text-align:center;padding:40px 24px;background:#1a1a2e}
.community h2{color:#e94560;margin-bottom:12px}
.community p{color:#a0a0b0;max-width:600px;margin:0 auto 20px}
.db{display:inline-flex;align-items:center;gap:8px;background:#5865F2;color:#fff;padding:10px 24px;border-radius:8px;font-weight:600;transition:transform 0.2s;text-decoration:none}
.db:hover{transform:translateY(-2px)}
.staff{max-width:1100px;margin:0 auto;padding:40px 24px}
.staff h2{color:#e94560;text-align:center;margin-bottom:20px}
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px}
.sc{background:#1a1a2e;border-radius:10px;padding:16px;text-align:center;border:1px solid #2a2a4e}
.sc .av{width:56px;height:56px;border-radius:50%;background:#e94560;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:#fff}
.sc h4{color:#e0e0e0;font-size:0.9rem;margin-bottom:4px}
.sc .ro{color:#e94560;font-size:0.75rem}
footer{background:#0a0a15;padding:20px;text-align:center;color:#606070;font-size:0.85rem;border-top:1px solid #1a1a2e;margin-top:40px}
footer a{color:#e94560;text-decoration:none}
@media(max-width:768px){
  .hero h1{font-size:2rem}
  .hero p{font-size:1rem}
  header{flex-direction:column;gap:8px}
  nav{justify-content:center}
  .psg{grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px}
}
</style>
</head>
<body>

<header>
  <div class="logo">FTF Values</div>
  <nav>
    <a href="home.html" class="act">Home</a>
    <a href="use-guide.html">Use Guide</a>
    <a href="changelog.html">Changelog</a>
    <a href="faq.html">FAQ</a>
    <a href="sets.html">Bundles</a>
    <a href="legendaries.html">Legendaries</a>
    <a href="epics.html">Epics</a>
    <a href="rares.html">Rares</a>
    <a href="commons.html">Commons</a>
  </nav>
</header>

<section class="hero">
  <h1>Flee the Facility Value Guide</h1>
  <p>Your trusted source for FTF item values, trading insights, and market trends. Make smarter trades with accurate, community-driven value data updated daily.</p>
  <div class="cb">
    <a href="legendaries.html" class="btn bp">View Legendary Values</a>
    <a href="use-guide.html" class="btn bs">How to Use</a>
  </div>
</section>

<section class="features">
  <div class="fc"><h3>Real-Time Value Tracking</h3><p>Stay up-to-date with the latest FTF item values. Data reflects actual trading patterns from the community.</p></div>
  <div class="fc"><h3>Stability & Demand Indicators</h3><p>Each item includes stability tags and demand ratings to help you predict market movements.</p></div>
  <div class="fc"><h3>Complete Item Coverage</h3><p>From Legendary bundles to Common consumables, we track values across all rarities.</p></div>
  <div class="fc"><h3>Active Community</h3><p>Join thousands of traders in our Discord. Get trading advice and value updates.</p></div>
</section>

{{PREVIEW_SECTIONS}}

<section class="community">
  <h2>Join the FTF Trading Community</h2>
  <p>Connect with thousands of active Flee the Facility traders. Get real-time value updates and trading tips.</p>
  <a href="https://discord.gg/YYUwQfGcXt" class="db" target="_blank">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.078.078 0 00-.079.038c-.21.375-.444.864-.608 1.24a18.566 18.566 0 00-5.487 0 12.36 12.36 0 00-.617-1.24.077.077 0 00-.079-.037 19.736 19.736 0 00-4.885 1.515.07.07 0 00-.039.112c-.322.536-.667 1.179-.994 1.907a19.588 19.588 0 00-1.669 3.105.075.075 0 00.029.095c.256.194.54.377.837.55a19.1 19.1 0 004.268 1.772.077.077 0 00.084.014c1.731-.728 3.272-1.728 4.51-2.913.073-.066.073-.173 0-.239-1.238-1.185-2.779-2.185-4.51-2.913a.077.077 0 00-.084.014 19.1 19.1 0 01-4.268-1.772c-.297-.173-.581-.356-.837-.55a.075.075 0 00-.029-.095 19.588 19.588 0 011.669-3.105c.327-.728.672-1.371.994-1.907a.07.07 0 01.039-.112 19.736 19.736 0 014.885-1.515.077.077 0 01.079.038c.21.375.444.864.608 1.24.302-.518.641-.973 1.004-1.349a.077.077 0 01.078-.028c1.596.771 3.03 1.869 4.178 3.232a.077.077 0 01.013.085c-.37.535-.77 1.066-1.204 1.567a.077.077 0 00.028.118c1.377.508 2.84.84 4.327.962a.077.077 0 00.082-.055c.23-.658.42-1.335.586-2.015a.077.077 0 00-.078-.09 19.7 19.7 0 01-2.065-.372.077.077 0 00-.082.055c-.225.713-.522 1.417-.891 2.087a.077.077 0 00.024.084c1.404.983 2.903 1.702 4.427 2.142a.077.077 0 00.095-.022c.551-.77 1.035-1.585 1.46-2.432a.077.077 0 00-.039-.093 19.775 19.775 0 01-2.414-1.643z"/></svg>
    Join our Discord
  </a>
</section>

<section class="staff">
  <h2>Meet Our Staff Team</h2>
  <div class="sg">
    <div class="sc"><div class="av">R</div><h4>Rox</h4><div class="ro">Value List Holder / Manager</div></div>
    <div class="sc"><div class="av">K</div><h4>Kory</h4><div class="ro">Website Manager / Value Staff</div></div>
    <div class="sc"><div class="av">S</div><h4>Shoya</h4><div class="ro">Value List Staff</div></div>
    <div class="sc"><div class="av">L</div><h4>Lzyh</h4><div class="ro">Value List Staff</div></div>
    <div class="sc"><div class="av">Z</div><h4>Zarys</h4><div class="ro">Value List Staff</div></div>
    <div class="sc"><div class="av">S2</div><h4>Sul</h4><div class="ro">Value List Staff</div></div>
    <div class="sc"><div class="av">S3</div><h4>Selkis</h4><div class="ro">Value List Staff</div></div>
    <div class="sc"><div class="av">A</div><h4>Alex</h4><div class="ro">Value List Staff</div></div>
  </div>
</section>

<footer>
  <p>&copy; 2026 FTF Values. This is an unofficial fan-made value guide for Flee the Facility on Roblox.</p>
  <p>Not affiliated with Dream Builder Development or Roblox Corporation. | <a href="use-guide.html">Use Guide</a> | <a href="faq.html">FAQ</a> | <a href="changelog.html">Changelog</a></p>
</footer>

</body>
</html>'''

def main():
    # 生成5个栏目预览区
    sections = ''
    for key in ['Sets', 'Legendaries', 'Epics', 'Rares', 'Commons']:
        print('Generating preview for {}...'.format(key))
        sections += preview_section(key)

    home = home_html.replace('{{PREVIEW_SECTIONS}}', sections)

    with open('seo_pages/home.html', 'w', encoding='utf-8') as f:
        f.write(home)
    print('Home page updated: seo_pages/home.html')

if __name__ == '__main__':
    main()
