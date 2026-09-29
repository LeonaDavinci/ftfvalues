#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 FTF Values 5个栏目数据展示页面
方式：读取 template.html，替换占位符，插入物品卡片
"""

import json, os, textwrap

with open('ftf_values_full_data.json', 'r', encoding='utf-8') as f:
    ALL_DATA = json.load(f)

STABILITY_COLORS = {
    'Rising':      '#2ecc71',
    'Stable':      '#3498db',
    'Fluctuating':'#f39c12',
    'Dropping':   '#e74c3c',
    'Volatile':   '#9b59b6',
    'Unstable':   '#e67e22',
    'Stable-Ish': '#1abc9c',
    'Undetermined':'#95a5a6',
}

CONF = {
    'Sets':        {'name':'Bundles & Sets', 'emoji':'🎁', 'color':'#e94560', 'gradient':'linear-gradient(135deg,#1a1a2e 0%,#2d1a2e 100%)',  'desc':'Exclusive item bundles and themed collections with unique trading value.'},
    'Legendaries': {'name':'Legendaries',       'emoji':'👑', 'color':'#f1c40f', 'gradient':'linear-gradient(135deg,#1a1a2e 0%,#2e2a1a 100%)',  'desc':'Highest-tier items with the most valuable trading worth in Flee the Facility.'},
    'Epics':       {'name':'Epics',            'emoji':'💎', 'color':'#9b59b6', 'gradient':'linear-gradient(135deg,#1a1a2e 0%,#1a1a2e 100%)',  'desc':'Mid-to-high tier items highly sought after by experienced traders.'},
    'Rares':       {'name':'Rares',            'emoji':'🔥', 'color':'#e74c3c', 'gradient':'linear-gradient(135deg,#1a1a2e 0%,#2e1a1a 100%)',  'desc':'Moderately valued items with steady trading activity in the community.'},
    'Commons':     {'name':'Commons',          'emoji':'✨', 'color':'#3498db', 'gradient':'linear-gradient(135deg,#1a1a2e 0%,#1a2a2e 100%)',  'desc':'Entry-level items perfect for new traders and fair starter trades.'},
}

def demand_stars(n):
    if n is None:
        return '☆☆☆☆☆'
    n = int(n)
    full = min(5, n // 2 + (1 if n % 2 else 0))
    return '★' * full + '☆' * (5 - full)

def make_cards(items):
    """为一批物品生成卡片HTML片段"""
    out = []
    for it in items:
        # 图片路径
        local = it.get('local_image_path', '')
        if local:
            img = '../images/' + local.replace(' ', '%20')
        else:
            img = it.get('image_url', '')

        name = it['name'].replace('"', '&quot;')
        namelc = name.lower()

        # 价值
        if it.get('value_min') and it.get('value_max'):
            val = '{}–{}'.format(it['value_min'], it['value_max'])
            hint = '<div class="vh">Range: {}–{} valuables</div>'.format(it['value_min'], it['value_max'])
        else:
            val = str(it['value'])
            hint = ''

        # 稳定性标签
        stab = it.get('stability', '')
        sc = STABILITY_COLORS.get(stab, '#95a5a6')
        stab_html = '<span class="b s" style="background:{}33;color:{};border:1px solid {}">{}</span>'.format(sc, sc, sc, stab)

        # 状态标签
        status = it.get('status')
        if status:
            pc = {'Bio':'#2ecc71','Fake':'#e74c3c','Perm':'#3498db'}.get(status, '#95a5a6')
            status_html = '<span class="b t" style="background:{}33;color:{};border:1px solid {}">{}</span>'.format(pc, pc, pc, status)
        else:
            status_html = ''

        ds = demand_stars(it.get('demand'))

        out.append(textwrap.dedent('''
            <div class="ic" data-v="{v}" data-n="{n}">
              <div class="ii"><img src="{img}" alt="{name}" loading="lazy"
                onerror="this.onerror=null;this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect fill=%22%23222%22 width=%22100%22 height=%22100%22/%3E%3Ctext fill=%22%23888%22 x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22%3EIMG%3C/text%3E%3C/svg%3E'"></div>
              <div class="in">
                <h3>{name}</h3>
                <div class="va">&#9889; {val} <small>valuables</small></div>
                {hint}
                <div class="tg">{stab} {status}</div>
                <div class="dm"><span class="dl">Demand:</span><span class="ds">{ds}</span></div>
              </div>
            </div>
        ''').strip().format(v=it['value'], n=namelc, img=img, name=name, val=val, hint=hint, stab=stab_html, status=status_html, ds=ds))
    return '\n'.join(out)

def stability_filters(items):
    sc = {}
    for i in items:
        s = i.get('stability', 'Unknown')
        sc[s] = sc.get(s, 0) + 1
    parts = []
    for s, c in sorted(sc.items(), key=lambda x: -x[1]):
        pc = STABILITY_COLORS.get(s, '#999')
        parts.append('<button class="fb" data-f="s" data-v="{s}"><span class="dot" style="background:{pc}"></span>{s} ({c})</button>'.format(s=s, pc=pc, c=c))
    return '\n'.join(parts)

def gen(key):
    cfg = CONF[key]
    items = ALL_DATA.get(key, {}).get('items', [])
    updated = ALL_DATA.get(key, {}).get('metadata', {}).get('last_updated', 'Unknown')
    total = sum(i['value'] for i in items if i.get('value'))
    avg = total // len(items) if items else 0

    # 导航 active 状态
    nav = {}
    for k in CONF:
        nav[k] = ' class="act"' if k == key else ''

    # 替换模板
    html = TEMPLATE.replace('{{COLOR}}', cfg['color'])
    html = html.replace('{{GRADIENT}}', cfg['gradient'])
    html = html.replace('{{EMOJI}}', cfg['emoji'])
    html = html.replace('{{NAME}}', cfg['name'])
    html = html.replace('{{DESC}}', cfg['desc'])
    html = html.replace('{{COUNT}}', str(len(items)))
    html = html.replace('{{AVG}}', str(avg))
    html = html.replace('{{UPDATED}}', updated)
    html = html.replace('{{FILTERS}}', stability_filters(items))
    html = html.replace('{{CARDS}}', make_cards(items))
    for k in CONF:
        html = html.replace('{{ACT_' + k.upper() + '}}', nav[k])
    html = html.replace('{{CANONICAL}}', 'https://yourdomain.com/' + key.lower() + '/')
    html = html.replace('{{DESC_META}}', 'Browse all {} FTF items. {} items with values, stability and demand info.'.format(key.lower(), len(items)))

    return html

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{NAME}} - FTF Values | Flee the Facility Trading Value Guide</title>
<meta name="description" content="{{DESC_META}}">
<meta name="keywords" content="FTF {{NAME}}, Flee the Facility, Roblox FTF, {{NAME}} values">
<link rel="canonical" href="{{CANONICAL}}">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;background:#0f0f1a;color:#e0e0e0}
a{text-decoration:none;color:inherit}
header{background:#1a1a2e;padding:10px 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid {{COLOR}};position:sticky;top:0;z-index:100;flex-wrap:wrap}
.logo{font-size:1.3rem;font-weight:700;color:{{COLOR}}}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:#e0e0e0;padding:6px 12px;border-radius:6px;font-size:0.85rem;transition:all 0.2s}
nav a:hover,nav a.act{background:{{COLOR}}22;color:{{COLOR}}}
.hero{background:{{GRADIENT}};padding:40px 24px 24px;text-align:center}
.hero h1{font-size:2.2rem;color:{{COLOR}};margin-bottom:8px}
.hero p{color:#a0a0b0;max-width:600px;margin:0 auto}
.sb{display:flex;justify-content:center;gap:32px;margin-top:24px;flex-wrap:wrap}
.st{text-align:center}
.stv{font-size:1.8rem;font-weight:700;color:{{COLOR}}}
.stl{font-size:0.8rem;color:#808090}
.filters{background:#13132a;padding:12px 24px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;border-bottom:1px solid #2a2a4e}
.fg{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.fl{font-size:0.8rem;color:#808090;margin-right:6px}
.fb{background:#1a1a2e;border:1px solid #2a2a4e;color:#e0e0e0;padding:4px 10px;border-radius:20px;cursor:pointer;font-size:0.8rem;transition:all 0.2s;display:flex;align-items:center;gap:4px}
.fb:hover,.fb.act{background:{{COLOR}}22;border-color:{{COLOR}};color:{{COLOR}}}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.sb2{margin-left:auto}
.sb2 input{background:#1a1a2e;border:1px solid #2a2a4e;color:#e0e0e0;padding:6px 16px;border-radius:20px;font-size:0.85rem;width:200px}
.sb2 input:focus{outline:none;border-color:{{COLOR}}}
.section{padding:24px;max-width:1400px;margin:0 auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.ic{background:#1a1a2e;border-radius:12px;overflow:hidden;border:1px solid #2a2a4e;transition:transform 0.2s,border-color 0.2s}
.ic:hover{transform:translateY(-4px);border-color:{{COLOR}};box-shadow:0 8px 25px rgba(0,0,0,0.3)}
.ic.hidden{display:none !important}
.ii{width:100%;aspect-ratio:1;background:#13132a;display:flex;align-items:center;justify-content:center;padding:8px}
.ii img{width:100%;height:100%;object-fit:contain}
.in{padding:10px}
.in h3{font-size:0.95rem;font-weight:600;color:#f0f0f0;margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.va{font-size:1.1rem;font-weight:700;color:{{COLOR}};margin-bottom:6px}
.va small{font-size:0.7rem;color:#808090;font-weight:400}
.vh{font-size:0.7rem;color:#f39c12;margin-bottom:4px}
.tg{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px}
.b{padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:600}
.dm{display:flex;align-items:center;gap:8px;font-size:0.8rem}
.dl{color:#808090}
.ds{color:#f1c40f;letter-spacing:2px}
#noR{display:none;text-align:center;padding:48px;color:#808090;font-size:1.1rem}
footer{background:#0a0a15;padding:24px;text-align:center;color:#606070;font-size:0.85rem;border-top:1px solid #1a1a2e;margin-top:32px}
footer a{color:{{COLOR}}}
@media(max-width:768px){
  header{flex-direction:column;gap:8px}
  nav{justify-content:center}
  .hero h1{font-size:1.6rem}
  .grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
  .sb2{margin-left:0;width:100%}
  .sb2 input{width:100%}
  .filters{padding:10px}
}
</style>
</head>
<body>

<header>
<div class="logo">FTF Values</div>
<nav>
  <a href="home.html">Home</a>
  <a href="use-guide.html">Use Guide</a>
  <a href="changelog.html">Changelog</a>
  <a href="faq.html">FAQ</a>
  <a href="sets.html"{{ACT_SETS}}>Bundles</a>
  <a href="legendaries.html"{{ACT_LEGENDARIES}}>Legendaries</a>
  <a href="epics.html"{{ACT_EPICS}}>Epics</a>
  <a href="rares.html"{{ACT_RARES}}>Rares</a>
  <a href="commons.html"{{ACT_COMMONS}}>Commons</a>
</nav>
</header>

<section class="hero">
  <h1>{{EMOJI}} {{NAME}}</h1>
  <p>{{DESC}}</p>
  <div class="sb">
    <div class="st"><div class="stv">{{COUNT}}</div><div class="stl">Total Items</div></div>
    <div class="st"><div class="stv">{{AVG}}</div><div class="stl">Avg Value</div></div>
    <div class="st"><div class="stv" style="font-size:1.1rem">{{UPDATED}}</div><div class="stl">Last Updated</div></div>
  </div>
</section>

<section class="filters">
  <div class="fg">
    <span class="fl">Stability:</span>
    <button class="fb act" data-f="s" data-v="all">All ({{COUNT}})</button>
    {{FILTERS}}
  </div>
  <div class="sb2"><input type="text" id="sq" placeholder="Search items..." oninput="filterItems()"></div>
</section>

<section class="section">
  <div class="grid" id="grid">{{CARDS}}</div>
  <div id="noR">No items found matching your criteria.</div>
</section>

<footer>
  <p>&copy; 2026 FTF Values. Unofficial fan-made guide for Flee the Facility on Roblox.</p>
  <p>Not affiliated with Dream Builder Development or Roblox Corporation. | <a href="use-guide.html">Use Guide</a> | <a href="faq.html">FAQ</a> | <a href="changelog.html">Changelog</a></p>
</footer>

<script>
(function(){
  var cards = document.querySelectorAll('.ic');
  var sq = document.getElementById('sq');
  function filterItems(){
    var q = (sq.value||'').toLowerCase();
    var ab = document.querySelector('.fb.act[data-f="s"]');
    var sv = ab ? ab.dataset.v : 'all';
    var vis = 0;
    cards.forEach(function(c){
      var n = c.dataset.n;
      var el = c.querySelector('.s');
      var s = el ? el.textContent.trim() : '';
      var ok = true;
      if(q && n.indexOf(q)===-1) ok=false;
      if(sv!=='all' && s!==sv) ok=false;
      c.classList.toggle('hidden',!ok);
      if(ok) vis++;
    });
    document.getElementById('noR').style.display = vis===0?'block':'none';
  }
  document.querySelectorAll('.fb').forEach(function(b){
    b.addEventListener('click',function(){
      var f = this.dataset.f;
      document.querySelectorAll('.fb[data-f="'+f+'"]').forEach(function(x){x.classList.remove('act')});
      this.classList.add('act');
      filterItems();
    });
  });
})();
</script>
</body>
</html>'''

def main():
    os.makedirs('seo_pages', exist_ok=True)
    for key in ['Sets','Legendaries','Epics','Rares','Commons']:
        print('Generating {}...'.format(key))
        html = gen(key)
        path = 'seo_pages/{}.html'.format(key.lower())
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('  -> {} ({} items)'.format(path, len(ALL_DATA.get(key,{}).get('items',[]))))
    print('\nDone!')

if __name__ == '__main__':
    main()
