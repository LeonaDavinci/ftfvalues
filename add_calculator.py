#!/usr/bin/env python3
"""
Add the FTF trade calculator to the static site.

What it does:
  1. Writes calculator.html  - a dedicated calculator page (canonical /calculator.html)
  2. Injects the same calculator widget into index.html (section id="calculator")
  3. Adds a "🧮 Calculator" link as the FIRST item of .main-nav on every HTML page
  4. Adds a "Calculator" link to every .footer-links block

Run from project root:  python add_calculator.py
The script is idempotent - re-running it does not duplicate anything.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'home.html', 'sets.html', 'legendaries.html', 'epics.html',
         'rares.html', 'commons.html', 'use-guide.html', 'faq.html', 'changelog.html']
SEO_PAGES = ['index.html', 'sets.html', 'legendaries.html', 'epics.html', 'rares.html',
             'commons.html', 'use-guide.html', 'faq.html', 'changelog.html']

EMOJI = '&#129518;'  # 🧮 (U+1F9EE)

CALC_CSS = """
/* === TRADE CALCULATOR === */
.calc-hero{text-align:center;padding:40px 24px 20px}
.calc-hero h1{font-size:2.2rem;color:#e94560;margin-bottom:8px}
.calc-hero p{color:#a0a0b0;max-width:620px;margin:0 auto}
.calc-wrap{max-width:1040px;margin:0 auto;padding:16px 24px 40px}
.calc-panel{background:#13132a;border:1px solid #2a2a4e;border-radius:14px;padding:20px}
.calc-top{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #2a2a4e;padding-bottom:12px;margin-bottom:16px;gap:12px;flex-wrap:wrap}
.ctotal{font-size:1.5rem;font-weight:700;color:#f0f0f0}
.ctotal.right{text-align:right}
.ctotal small{font-size:.85rem;color:#808090;font-weight:600}
.clegend{display:flex;gap:14px;font-size:.85rem;font-weight:700}
.lw{color:#2ecc71}.lf{color:#f1c40f}.ll{color:#e74c3c}
.calc-add{display:flex;gap:12px;align-items:center;margin-bottom:18px;flex-wrap:wrap}
.side-pick{display:flex;gap:6px}
.side-pick button{background:#1a1a2e;border:1px solid #2a2a4e;color:#a0a0b0;padding:7px 14px;border-radius:20px;font-size:.82rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:inherit}
.side-pick button.on{background:rgba(233,69,96,.13);border-color:#e94560;color:#e94560}
.srch{position:relative;flex:1;min-width:220px}
.srch input{width:100%;background:#1a1a2e;border:1px solid #2a2a4e;color:#e0e0e0;padding:9px 16px;border-radius:20px;font-size:.9rem;font-family:inherit}
.srch input:focus{outline:none;border-color:#e94560}
.sr-drop{position:absolute;left:0;right:0;top:100%;margin-top:6px;background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;max-height:300px;overflow-y:auto;z-index:50;box-shadow:0 12px 30px rgba(0,0,0,.5)}
.sr-item{display:flex;align-items:center;gap:10px;width:100%;padding:8px 12px;background:none;border:none;cursor:pointer;text-align:left;color:#e0e0e0;transition:background .15s;font-family:inherit}
.sr-item:hover{background:#2a2a3e}
.sr-item img{width:34px;height:34px;object-fit:contain;background:#13132a;border-radius:6px;flex:none}
.sr-name{flex:1;font-size:.88rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sr-val{font-size:.8rem;color:#e94560;font-weight:700}
.sr-none{padding:14px;color:#808090;font-size:.85rem;text-align:center}
.calc-grid3{display:grid;grid-template-columns:1fr 190px 1fr;gap:16px;align-items:start}
.calc-side h3{text-align:center;font-size:1.05rem;color:#e0e0e0;margin-bottom:10px}
.slots{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.slot{position:relative;aspect-ratio:1;background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.slot.filled{border-color:#e94560}
.slot img{width:100%;height:100%;object-fit:contain;padding:6px}
.slot-ph{color:#3a3a5e;font-size:1.4rem}
.slot.empty{border-style:dashed;color:#3a3a5e;font-size:1.6rem;cursor:pointer;background:transparent;transition:all .15s;font-family:inherit}
.slot.empty:hover,.slot.empty.target{border-color:#e94560;color:#e94560;background:rgba(233,69,96,.05)}
.slot-rm{position:absolute;top:3px;right:4px;background:rgba(0,0,0,.55);color:#e0e0e0;border:none;border-radius:50%;width:20px;height:20px;font-size:.8rem;line-height:1;cursor:pointer;z-index:2}
.slot-rm:hover{background:#e94560;color:#fff}
.qty{position:absolute;bottom:4px;left:4px;right:4px;display:flex;align-items:center;justify-content:space-between;background:rgba(10,10,21,.78);border-radius:8px;padding:1px 4px;z-index:2}
.qty button{background:none;border:none;color:#e0e0e0;font-size:.95rem;font-weight:700;cursor:pointer;padding:0 6px}
.qty button:hover{color:#e94560}
.qty span{font-size:.8rem;font-weight:700;color:#fff}
.calc-mid{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:12px 0}
.vnum{font-size:2.4rem;font-weight:800;line-height:1}
.vnum.win{color:#2ecc71}.vnum.lose{color:#e74c3c}.vnum.fair{color:#f1c40f}.vnum.idle{color:#3a3a5e}
.vlab{font-size:.95rem;font-weight:800;letter-spacing:1px}
.vlab.win{color:#2ecc71}.vlab.lose{color:#e74c3c}.vlab.fair{color:#f1c40f}
.cbtn{background:#1a1a2e;border:1px solid #2a2a4e;color:#e0e0e0;padding:8px 20px;border-radius:8px;font-size:.85rem;font-weight:600;cursor:pointer;transition:all .2s;min-width:110px;font-family:inherit}
.cbtn:hover{border-color:#e94560;color:#e94560}
.cbtn:disabled{opacity:.45;cursor:default}
.calc-note{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:16px;color:#808090;font-size:.8rem}
.calc-note .cn2{color:#606070}
@media(max-width:860px){
  .calc-grid3{grid-template-columns:1fr}
  .calc-side.their-side{order:2}
  .calc-mid{order:3;flex-direction:row;justify-content:center;flex-wrap:wrap;padding:8px 0}
  .vnum{font-size:1.8rem}
}
"""

WIDGET_HTML = """
<!-- ========== TRADE CALCULATOR ========== -->
<div class="calc-wrap" id="calculator">
  <div class="calc-panel">
    <div class="calc-top">
      <div class="ctotal" id="ftfYourTotal">0 <small>fv</small></div>
      <div class="clegend"><span class="lw">Win</span><span class="lf">Fair</span><span class="ll">Lose</span></div>
      <div class="ctotal right" id="ftfTheirTotal">0 <small>fv</small></div>
    </div>

    <div class="calc-add">
      <div class="side-pick">
        <button type="button" id="ftfSideYour" class="on">Your Offer</button>
        <button type="button" id="ftfSideTheir">Their Offer</button>
      </div>
      <div class="srch">
        <input id="ftfSearch" type="text" placeholder="Search items to add&hellip;" aria-label="Search items" autocomplete="off">
        <div class="sr-drop" id="ftfDrop" style="display:none"></div>
      </div>
    </div>

    <div class="calc-grid3">
      <div class="calc-side" id="ftfYourSide">
        <h3>Your Offer</h3>
        <div class="slots" id="ftfYourSlots"></div>
      </div>
      <div class="calc-mid">
        <div class="vnum idle" id="ftfVerdictNum">&mdash;</div>
        <div class="vlab" id="ftfVerdictLab" style="color:#3a3a5e">FV &mdash;</div>
        <button class="cbtn" type="button" id="ftfReset">Reset</button>
        <button class="cbtn" type="button" id="ftfSave">Save Image</button>
      </div>
      <div class="calc-side their-side" id="ftfTheirSide">
        <h3>Their Offer</h3>
        <div class="slots" id="ftfTheirSlots"></div>
      </div>
    </div>

    <div class="calc-note">
      <span id="ftfUpdated">Last updated: &mdash;</span>
      <span class="cn2">Values in fv (valuables)</span>
    </div>
  </div>
</div>
"""

CALC_JS = r"""
(function () {
  if (window.__ftfCalcReady) return;
  var wrap = document.getElementById('calculator');
  if (!wrap) return;

  var DATA_URL = 'ftf_values_full_data.json';
  var S = { your: [], their: [], side: 'your', items: [], byKey: {}, updated: '' };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function fmt(n) { return (Number(n) || 0).toLocaleString('en-US'); }
  function imgSrc(p) { return 'images/' + String(p || '').replace(/ /g, '%20'); }

  var el = function (id) { return document.getElementById(id); };
  var drop = el('ftfDrop'), search = el('ftfSearch');
  var q = '', open = false;

  function total(list) {
    var sum = 0;
    for (var i = 0; i < list.length; i++) {
      var it = S.byKey[list[i].key];
      if (it) sum += (Number(it.value) || 0) * list[i].qty;
    }
    return sum;
  }

  function verdict() {
    if (!S.your.length || !S.their.length) return null;
    var diff = total(S.their) - total(S.your);
    var tol = Math.max(50, 0.05 * Math.max(total(S.your), total(S.their)));
    if (Math.abs(diff) <= tol) return { k: 'fair', d: Math.abs(diff) };
    return { k: diff > 0 ? 'win' : 'lose', d: Math.abs(diff) };
  }

  function renderSide(which) {
    var label = which === 'your' ? 'ftfYourSlots' : 'ftfTheirSlots';
    var box = el(label);
    if (!box) return;
    var list = S[which];
    var n = Math.max(9, Math.ceil((list.length + 1) / 3) * 3);
    var html = '';
    for (var i = 0; i < n; i++) {
      var e = list[i];
      if (e) {
        var it = S.byKey[e.key];
        if (!it) continue;
        html += '<div class="slot filled">' +
          '<button type="button" class="slot-rm" data-rm="' + which + '" data-key="' + esc(e.key) + '" aria-label="Remove">&times;</button>' +
          '<img src="' + esc(imgSrc(it.img)) + '" alt="' + esc(it.name) + '" loading="lazy" onerror="this.style.display=\'none\'">' +
          '<div class="qty">' +
            '<button type="button" data-q="' + which + '" data-key="' + esc(e.key) + '" data-d="-1">&minus;</button>' +
            '<span>' + e.qty + '</span>' +
            '<button type="button" data-q="' + which + '" data-key="' + esc(e.key) + '" data-d="1">+</button>' +
          '</div></div>';
      } else {
        html += '<button type="button" class="slot empty' + (S.side === which ? ' target' : '') + '" data-pick="' + which + '">+</button>';
      }
    }
    box.innerHTML = html;
  }

  function renderTotals() {
    var y = total(S.your), t = total(S.their);
    el('ftfYourTotal').innerHTML = fmt(y) + ' <small>fv</small>';
    el('ftfTheirTotal').innerHTML = fmt(t) + ' <small>fv</small>';
    var v = verdict();
    var num = el('ftfVerdictNum'), lab = el('ftfVerdictLab');
    if (v) {
      num.className = 'vnum ' + v.k;
      lab.className = 'vlab ' + v.k;
      num.textContent = fmt(v.d);
      lab.textContent = 'FV ' + (v.k === 'win' ? 'WIN' : v.k === 'lose' ? 'LOSE' : 'FAIR');
    } else {
      num.className = 'vnum idle';
      lab.className = 'vlab';
      num.innerHTML = '&mdash;';
      lab.innerHTML = 'FV &mdash;';
    }
    renderSide('your');
    renderSide('their');
  }

  function renderDrop() {
    var s = q.trim().toLowerCase();
    if (!open || !s) { drop.style.display = 'none'; drop.innerHTML = ''; return; }
    var res = S.items.filter(function (i) { return i.name.toLowerCase().indexOf(s) !== -1; }).slice(0, 40);
    if (!res.length) {
      drop.innerHTML = '<div class="sr-none">No items match &ldquo;' + esc(q) + '&rdquo;</div>';
      drop.style.display = 'block';
      return;
    }
    var html = '';
    for (var i = 0; i < res.length; i++) {
      var it = res[i];
      html += '<button type="button" class="sr-item" data-add="' + esc(it.key) + '">' +
        '<img src="' + esc(imgSrc(it.img)) + '" alt="" loading="lazy" onerror="this.style.display=\'none\'">' +
        '<span class="sr-name">' + esc(it.name) + '</span>' +
        '<span class="sr-val">' + fmt(it.value) + ' fv</span></button>';
    }
    drop.innerHTML = html;
    drop.style.display = 'block';
  }

  function addItem(key) {
    var list = S[S.side];
    for (var i = 0; i < list.length; i++) {
      if (list[i].key === key) { list[i].qty += 1; renderTotals(); return; }
    }
    list.push({ key: key, qty: 1 });
    q = ''; open = false;
    search.value = '';
    renderTotals();
    renderDrop();
    search.focus();
  }

  function setSide(which) {
    S.side = which;
    el('ftfSideYour').className = which === 'your' ? 'on' : '';
    el('ftfSideTheir').className = which === 'their' ? 'on' : '';
    renderTotals();
  }

  wrap.addEventListener('click', function (ev) {
    var t = ev.target;
    while (t && t !== wrap && !t.getAttribute('data-rm') && !t.getAttribute('data-q') &&
           !t.getAttribute('data-pick') && !t.getAttribute('data-add')) t = t.parentNode;
    if (!t || t === wrap) return;

    if (t.getAttribute('data-rm')) {
      var rk = t.getAttribute('data-key');
      S[t.getAttribute('data-rm')] = S[t.getAttribute('data-rm')].filter(function (e) { return e.key !== rk; });
      renderTotals();
      return;
    }
    if (t.getAttribute('data-q')) {
      var wk = t.getAttribute('data-q'), kk = t.getAttribute('data-key'), d = parseInt(t.getAttribute('data-d'), 10);
      var list = S[wk];
      for (var i = 0; i < list.length; i++) {
        if (list[i].key === kk) { list[i].qty += d; if (list[i].qty < 1) list.splice(i, 1); break; }
      }
      renderTotals();
      return;
    }
    if (t.getAttribute('data-pick')) { setSide(t.getAttribute('data-pick')); search.focus(); return; }
    if (t.getAttribute('data-add')) { addItem(t.getAttribute('data-add')); return; }
  });

  document.addEventListener('click', function (ev) {
    if (open && !ev.target.closest('.srch')) { open = false; renderDrop(); }
  });

  search.addEventListener('input', function () { q = search.value; open = true; renderDrop(); });
  search.addEventListener('focus', function () { if (q.trim()) { open = true; renderDrop(); } });
  el('ftfSideYour').addEventListener('click', function () { setSide('your'); });
  el('ftfSideTheir').addEventListener('click', function () { setSide('their'); });
  el('ftfReset').addEventListener('click', function () { S.your = []; S.their = []; renderTotals(); });

  el('ftfSave').addEventListener('click', function () {
    var loadImg = function (src) {
      return new Promise(function (res) {
        var im = new Image();
        im.onload = function () { res(im); };
        im.onerror = function () { res(null); };
        im.src = src;
      });
    };
    var W = 900, rowH = 52, maxRows = 7;
    var rows = Math.min(maxRows, Math.max(S.your.length, S.their.length, 1));
    var H = 400 + rows * rowH + 40;
    var cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    var ctx = cv.getContext('2d');

    ctx.fillStyle = '#0f0f1a'; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#13132a'; ctx.fillRect(30, 30, W - 60, H - 60);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#e94560'; ctx.font = "bold 32px 'Segoe UI', sans-serif";
    ctx.fillText('FTF Values — Trade Calculator', W / 2, 85);
    ctx.fillStyle = '#808090'; ctx.font = "15px 'Segoe UI', sans-serif";
    ctx.fillText(new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), W / 2, 112);

    var drawSide = function (list, x0, title) {
      ctx.textAlign = 'center';
      ctx.fillStyle = '#f0f0f0'; ctx.font = "bold 22px 'Segoe UI', sans-serif";
      ctx.fillText(title, x0 + 190, 165);
      ctx.fillStyle = '#e94560'; ctx.font = "bold 26px 'Segoe UI', sans-serif";
      ctx.fillText(fmt(total(list)) + ' fv', x0 + 190, 196);
      var shown = list.slice(0, maxRows), y = 230;
      var i = 0;
      var next = function () {
        if (i >= shown.length) {
          if (list.length > maxRows) {
            ctx.textAlign = 'left'; ctx.fillStyle = '#808090'; ctx.font = "14px 'Segoe UI', sans-serif";
            ctx.fillText('+' + (list.length - maxRows) + ' more…', x0 + 96, y + 10);
          }
          ctx.textAlign = 'center';
          return Promise.resolve();
        }
        var e = shown[i++], it = S.byKey[e.key];
        if (it) {
          return loadImg(imgSrc(it.img)).then(function (im) {
            ctx.fillStyle = '#1a1a2e'; ctx.fillRect(x0 + 40, y, 44, 44);
            if (im) ctx.drawImage(im, x0 + 40, y, 44, 44);
            ctx.textAlign = 'left'; ctx.fillStyle = '#e0e0e0'; ctx.font = "16px 'Segoe UI', sans-serif";
            ctx.fillText(it.name + (e.qty > 1 ? ' ×' + e.qty : ''), x0 + 96, y + 28);
            ctx.textAlign = 'right'; ctx.fillStyle = '#a0a0b0'; ctx.font = "15px 'Segoe UI', sans-serif";
            ctx.fillText(fmt((Number(it.value) || 0) * e.qty) + ' fv', x0 + 340, y + 28);
            y += rowH;
            return next();
          });
        }
        y += rowH;
        return next();
      };
      return next();
    };

    var v = verdict();
    Promise.all([drawSide(S.your, 50, 'Your Offer'), drawSide(S.their, W - 430, 'Their Offer')]).then(function () {
      ctx.strokeStyle = '#2a2a4e'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(W / 2, 150); ctx.lineTo(W / 2, 230 + rows * rowH); ctx.stroke();
      if (v) {
        ctx.fillStyle = v.k === 'win' ? '#2ecc71' : v.k === 'lose' ? '#e74c3c' : '#f1c40f';
        ctx.font = "bold 44px 'Segoe UI', sans-serif";
        ctx.fillText(fmt(v.d), W / 2, 260);
        ctx.font = "bold 20px 'Segoe UI', sans-serif";
        ctx.fillText('FV ' + (v.k === 'win' ? 'Win' : v.k === 'lose' ? 'Lose' : 'Fair'), W / 2, 292);
      } else {
        ctx.fillStyle = '#808090'; ctx.font = "18px 'Segoe UI', sans-serif";
        ctx.fillText('Add items to both sides', W / 2, 260);
      }
      ctx.fillStyle = '#606070'; ctx.font = "14px 'Segoe UI', sans-serif";
      ctx.fillText('www.ftfvalues.app', W / 2, H - 50);

      cv.toBlob(function (blob) {
        if (!blob) return;
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'ftf-trade-calculator.png';
        document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 5000);
      }, 'image/png');
    });
  });

  var taken = false;
  for (var key in S.items) { taken = true; break; }

  fetch(DATA_URL)
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var items = [];
      for (var cat in data) {
        var meta = (data[cat] && data[cat].metadata) || {};
        if (meta.last_updated && !S.updated) S.updated = meta.last_updated;
        var arr = (data[cat] && data[cat].items) || [];
        for (var i = 0; i < arr.length; i++) {
          var it = arr[i];
          var k = (it.rarity || '') + '__' + (it.slug || '');
          items.push({ key: k, name: it.name, value: Number(it.value) || 0, img: it.local_image_path || '' });
        }
      }
      items.sort(function (a, b) { return a.name.localeCompare(b.name); });
      S.items = items;
      S.byKey = {};
      for (var j = 0; j < items.length; j++) S.byKey[items[j].key] = items[j];
      var note = el('ftfUpdated');
      if (note) note.innerHTML = 'Last updated: ' + esc(S.updated || '—');
      renderTotals();
      renderDrop();
    })
    .catch(function () {
      var note = el('ftfUpdated');
      if (note) note.textContent = 'Could not load item data.';
    });

  renderTotals();
  window.__ftfCalcReady = true;
})();
"""

CALC_HERO = """
<!-- ========== CALCULATOR HERO ========== -->
<section class="calc-hero">
  <h1>&#129522; FTF Calculator</h1>
  <p>Pick items for both sides of your trade &mdash; totals and a Win / Fair / Lose verdict update instantly as you build the offer.</p>
</section>
"""


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


CALC_LINK_RE = re.compile(r'[ \t]*<a href="[^"]*"[^>]*>(?:&#129518;|&#129522;|🧮|🧲) Calculator</a>\r?\n')


def drop_existing_calc_nav(html):
    """Remove any previously injected Calculator nav links so the result is deterministic."""
    return CALC_LINK_RE.sub('', html)


def add_calculator_nav(html, href, active=False):
    """Insert exactly one Calculator link as the first item of .main-nav."""
    html = drop_existing_calc_nav(html)
    label = EMOJI + ' Calculator'
    cls = ' class="act"' if active else ''
    new_link = '    <a href="{}"{}>{}</a>\n'.format(href, cls, label)
    pattern = r'(<nav class="main-nav" id="mainNav">\r?\n)'
    if re.search(pattern, html):
        html2 = re.sub(pattern, lambda m: m.group(1) + new_link, html, count=1)
        return html2, html2 != html
    pattern2 = r'(<nav>\r?\n  <a href="home\.html">Home</a>\r?\n)'
    if re.search(pattern2, html):
        html2 = re.sub(pattern2, lambda m: m.group(1) + '  <a href="{}">{}</a>\n'.format(href, label), html, count=1)
        return html2, html2 != html
    return html, False


def add_footer_cat(html, href):
    """Category-page footers link through the 'Not affiliated…' paragraph."""
    if '>Calculator</a>' in html:
        return html, False
    m = re.search(r'<a href="use-guide\.html">Use Guide</a>', html)
    if not m:
        return html, False
    link = '<a href="{}">Calculator</a> | '.format(href)
    return html[:m.start()] + link + html[m.start():], True


def add_footer_link(html, href):
    if '>Calculator</a>' in html:
        return html, False
    marker = '<p class="footer-links">'
    if marker in html:
        link = '<a href="{}">Calculator</a> |\n    '.format(href)
        html2 = html.replace(marker, marker + link, 1)
        return html2, True
    return html, False


def inject_css(html):
    if '.calc-wrap{' in html:
        return html, False
    return html.replace('</style>', CALC_CSS + '</style>'), True


def main():
    log = []

    # ---------- 1. build calculator.html from index.html ----------
    idx = read(os.path.join(ROOT, 'index.html'))
    calc = idx

    # swap SEO head fields
    calc = re.sub(r'<title>.*?</title>',
                  '<title>FTF Calculator - Build Both Sides of Your Trade | FTF Values</title>', calc, count=1, flags=re.S)
    calc = re.sub(r'<meta name="description" content=".*?"\s*/?>',
                  '<meta name="description" content="FTF trade calculator — build both sides of a trade, compare totals in fv, and see instantly if you Win, Lose, or make a Fair trade." />',
                  calc, count=1, flags=re.S)
    calc = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>',
                  '<link rel="canonical" href="https://www.ftfvalues.app/calculator.html" />', calc, count=1, flags=re.S)
    calc = re.sub(r'<meta name="keywords" content="[^"]*"\s*/?>',
                  '<meta name="keywords" content="FTF calculator, FTF trade calculator, Flee the Facility, FTF item values, FTF trading" />',
                  calc, count=1, flags=re.S)

    # body: replace everything between </header> and the FOOTER marker
    footer_marker = '<!-- ========== FOOTER ========== -->'
    if footer_marker in calc:
        head_part = calc.split('<!-- ========== HEADER ========== -->')[0]
        header_part = calc.split('<!-- ========== HEADER ========== -->')[1].split('</header>')[0] + '</header>'
        body = CALC_HERO + WIDGET_HTML + '\n\n'
        calc = head_part + '<!-- ========== HEADER ========== -->' + header_part + '\n\n' + body + footer_marker + \
               calc.split(footer_marker, 1)[1]

    calc, css_ok = inject_css(calc)
    calc, nav_ok = add_calculator_nav(calc, 'calculator.html', active=True)
    calc, ft_ok = add_footer_link(calc, 'calculator.html')
    if 'id="calculator"' in calc and 'window.__ftfCalcReady' not in calc:
        calc = calc.replace('</body>', '<!-- Trade Calculator -->\n<script>\n' + CALC_JS + '\n</script>\n</body>')
    write(os.path.join(ROOT, 'calculator.html'), calc)
    log.append('calculator.html written (css:%s nav:%s footer:%s)' % (css_ok, nav_ok, ft_ok))

    # ---------- 2. inject the widget into index.html ----------
    home = read(os.path.join(ROOT, 'index.html'))
    FEATURES = '<!-- ========== FEATURES ========== -->'
    # strip any previously injected widget (old id variants included) so re-runs are idempotent
    home = re.sub(r'<!-- ========== CALCULATOR ========== -->\n.*?(?=<!-- ========== FEATURES ========== -->)',
                  '', home, count=1, flags=re.S)
    JS_BLOCK = '<!-- Trade Calculator -->\n<script>\n' + CALC_JS + '\n</script>\n'
    home = re.sub(r'<!-- Trade Calculator -->\s*<script>.*?</script>\s*', '', home, flags=re.S)
    if 'id="calculator"' not in home:
        home, css_ok = inject_css(home)
        section = ('<!-- ========== CALCULATOR ========== -->\n' + WIDGET_HTML + '\n')
        if FEATURES in home:
            home = home.replace(FEATURES, section + '\n' + FEATURES, 1)
        else:
            home = home.replace('<!-- ========== COMMUNITY ========== -->', section + '\n<!-- ========== COMMUNITY ========== -->', 1)
        home = home.replace('</body>', JS_BLOCK + '</body>')
        # hero button (deterministic: drop any previous copy first)
        HERO_BTN = '    <a href="#calculator" class="btn bp">&#129518; Open Trade Calculator</a>\n'
        home = re.sub(r'[ \t]*<a href="#calculator" class="btn bp">.*?</a>\n', '', home)
        if HERO_BTN not in home:
            home = home.replace('    <a href="legendaries.html" class="btn bp">View Legendary Values</a>',
                                HERO_BTN + '    <a href="legendaries.html" class="btn bp">View Legendary Values</a>', 1)
        write(os.path.join(ROOT, 'index.html'), home)
        log.append('index.html: widget injected')

    # ---------- 3. nav + footer on every other page ----------
    targets = []
    for name in PAGES:
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            targets.append((p, '#calculator' if name == 'index.html' else 'calculator.html'))
    for name in SEO_PAGES:
        p = os.path.join(ROOT, 'seo_pages', name)
        if os.path.exists(p):
            targets.append((p, '../calculator.html'))

    for path, href in targets:
        html = read(path)
        html, nav_ok = add_calculator_nav(html, href)
        html, ft_ok = add_footer_link(html, href)
        if not ft_ok:
            html, ft_ok = add_footer_cat(html, href)
        if nav_ok or ft_ok:
            write(path, html)
            log.append('%s: %s' % (os.path.basename(path), ' '.join(filter(None, ['nav' if nav_ok else '', 'footer' if ft_ok else '']))))

    print('\n'.join(log))
    print('done - %d files touched' % len(log))


if __name__ == '__main__':
    main()
