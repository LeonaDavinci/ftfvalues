"""Inject the GA4 (gtag.js) snippet into the <head> of every shipped page.

Idempotent: re-running does not duplicate the snippet. The two page generators
(generate_pages.py, update_home.py) also get the snippet in their <head>
template so a regeneration never drops it again.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ID = 'G-H7X4B4YV1B'

PAGES = [
    'index.html', 'home.html', 'calculator.html',
    'sets.html', 'legendaries.html', 'epics.html', 'rares.html', 'commons.html',
    'use-guide.html', 'faq.html', 'changelog.html',
]
SEO_PAGES = [
    'index.html', 'sets.html', 'legendaries.html', 'epics.html', 'rares.html',
    'commons.html', 'use-guide.html', 'faq.html', 'changelog.html',
]
# Generators that rebuild pages from a <head> template.
TEMPLATES = ['generate_pages.py', 'update_home.py']

SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{ID}');
</script>""".format(ID=ID)


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def has_snippet(html):
    return ('googletagmanager.com/gtag/js?id=' + ID) in html


def inject_head(html):
    """Insert the snippet just before </head>; tolerate any whitespace/newlines."""
    m = re.search(r'[ \t]*</head>', html)
    if not m:
        return html, False
    return html[:m.start()] + SNIPPET + '\n' + html[m.start():], True


def main():
    log = []

    targets = [(os.path.join(ROOT, n), n) for n in PAGES
               if os.path.exists(os.path.join(ROOT, n))]
    targets += [(os.path.join(ROOT, 'seo_pages', n), 'seo_pages/' + n) for n in SEO_PAGES
                if os.path.exists(os.path.join(ROOT, 'seo_pages', n))]

    for path, label in targets:
        html = read(path)
        if has_snippet(html):
            log.append('%s: already has GA4' % label)
            continue
        html2, ok = inject_head(html)
        if ok:
            write(path, html2)
            log.append('%s: GA4 added' % label)

    # keep the generators in sync so a rebuild keeps the tag
    for name in TEMPLATES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        src = read(path)
        if has_snippet(src):
            continue
        src2 = re.sub(r'\n[ \t]*</head>\n<body>', '\n' + SNIPPET + '\n</head>\n<body>', src, count=1)
        if src2 == src:
            src2 = re.sub(r'\n[ \t]*</head>', '\n' + SNIPPET + '\n</head>', src, count=1)
        if src2 != src:
            write(path, src2)
            log.append('%s: head template patched' % name)
        else:
            log.append('%s: could NOT find </head> in template' % name)

    for line in log:
        print(line)
    added = len([l for l in log if l.endswith('GA4 added')])
    tmpl = len([l for l in log if 'template' in l])
    print('done - %d page(s) tagged, %d head template(s) patched' % (added, tmpl))


if __name__ == '__main__':
    main()
