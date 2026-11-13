#!/usr/bin/env python3
"""Convert captured source DOM (work/bundles/<page>/dom.html) into EDS section files
(pages/<page>/NN-*.html) and download the referenced images into ../media/<page>/.
Usage: python3 tools/gen_content.py [page ...]"""
import html, json, pathlib, re, sys, urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
VOID = {'img', 'br', 'hr', 'input'}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []

    def cls(self):
        return (self.attrs.get('class') or '').split()


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node('root', [], None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, d):
        self.cur.kids.append(d)

    def handle_entityref(self, name):
        self.cur.kids.append(f'&{name};')

    def handle_charref(self, name):
        self.cur.kids.append(f'&#{name};')


def parse(s):
    t = Tree()
    t.feed(s)
    return t.root


def walk(n):
    if isinstance(n, str):
        return
    yield n
    for k in n.kids:
        yield from walk(k)


def find(n, pred):
    return next((x for x in walk(n) if pred(x)), None)


def text(n):
    if isinstance(n, str):
        return html.unescape(n)
    return ''.join(text(k) for k in n.kids)


KEEP = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'u', 'br', 'a', 'table', 'thead',
        'tbody', 'tr', 'th', 'td', 'b', 'i'}
UNWRAP = {'span', 'div', 'section', 'font', 'small'}


def media_name(url):
    return re.sub(r'[^A-Za-z0-9._-]', '-', url.split('/')[-1].split('?')[0])


CURRENT = {}  # page -> {src url: url of the rendition the source browser actually used}


def load_current(page, bundle):
    # img record keys (img:<file>) name the file the browser painted; map them back to URLs
    names = set()
    for w in ('1440', '1280'):
        for f in (bundle / w).glob('*.json'):
            if f.name in ('outline.json',):
                continue
            try:
                for e in json.loads(f.read_text()).get('els', []):
                    if e['key'].startswith('img:'):
                        names.add(re.sub(r'#\d+$', '', e['key'][4:]))
            except (ValueError, AttributeError):
                pass
    assets = json.loads((bundle / 'assets.json').read_text())['images']
    m = {}
    for a in assets:
        cands = [a['src']] + [c.split()[0] for c in a.get('srcset', '').split(',') if c.strip()]
        for c in cands:
            if c.split('/')[-1] in names:
                m[a['src']] = c
    CURRENT[page] = m


def fetch_image(url, page):
    url = CURRENT.get(page, {}).get(url, url)
    dest = REPO / 'media' / page / media_name(url)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        dest.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return f'/media/{page}/{dest.name}'


def render(n, page, base='https://www.sfntc.com'):
    if isinstance(n, str):
        return n
    inner = ''.join(render(k, page) for k in n.kids)
    t = n.tag
    if t == 'img':
        src = n.attrs.get('src', '')
        alt = html.escape(n.attrs.get('alt', ''), quote=True)
        dims = ''.join(f' {a}="{n.attrs[a]}"' for a in ('width', 'height') if n.attrs.get(a, '').isdigit())
        pic = f'<picture><img src="{fetch_image(src, page)}" alt="{alt}"{dims}></picture>'
        return pic
    if t == 'br':
        return '<br>'
    if t == 'table':
        rows = [r for r in walk(n) if not isinstance(r, str) and r.tag == 'tr']
        out = '<div class="table">'
        for r in rows:
            cells = [c for c in r.kids if not isinstance(c, str) and c.tag in ('th', 'td')]
            out += '<div>' + ''.join(f'<div>{render_inline(c, page)}</div>' for c in cells) + '</div>'
        return out + '</div>'
    if t == 'div' and 'display: flex' in (n.attrs.get('style') or ''):
        cells = [c for c in n.kids if not isinstance(c, str) and c.tag == 'p']
        return '<div class="columns contact"><div>' + ''.join(f'<div>{render(c, page)}</div>' for c in cells) + '</div></div>'
    if 'row' in n.cls() or 'image-overlay-container' in n.cls():
        return inner
    if t == 'a':
        href = n.attrs.get('href', '')
        href = re.sub(r'^https?://(www\.)?sfntc\.com', '', href) or '/'
        return f'<a href="{href}">{inner}</a>'
    if t == 'p' and inner.strip() in ('&nbsp;', ''):
        # DA drops paragraphs that only hold a non-breaking space; an empty line break survives
        return '<p><br></p>' if inner.strip() else ''
    if t in KEEP:
        return f'<{t}>{inner}</{t}>'
    return inner


def render_inline(n, page):
    return ''.join(render(k, page) for k in n.kids)


def main():
    pages = json.loads((ROOT / 'pages.json').read_text())['pages']
    only = sys.argv[1:]
    for name, spec in pages.items():
        if only and name not in only or name == 'home':
            continue
        load_current(name, ROOT / spec['bundle'])
        h = (ROOT / spec['bundle'] / 'dom.html').read_text()
        i, j = h.index('<main'), h.index('</main>')
        main_node = parse(h[i:j + 7]).kids[0]
        out = ROOT / 'pages' / name
        out.mkdir(parents=True, exist_ok=True)
        for f in out.glob('*.html'):
            f.unlink()
        ph = find(main_node, lambda x: 'page-header' in x.cls())
        title = text(ph).strip()
        bc = find(main_node, lambda x: 'breadcrumbs' in x.cls())
        crumbs = ''
        if bc:
            parts = []
            for sp in bc.kids[0].kids if bc.kids and not isinstance(bc.kids[0], str) else []:
                if isinstance(sp, str):
                    continue
                a = find(sp, lambda x: x.tag == 'a')
                if a:
                    parts.append(render(a, name))
                else:
                    parts.append(html.escape(text(sp).strip(), quote=False))
            crumbs = ' '.join(parts)
        secs = []
        first = f'<div class="page-header"><div><div><h1>{html.escape(title, quote=False)}</h1></div></div>'
        if crumbs:
            first += f'<div><div><p>{crumbs}</p></div></div>'
        first += '</div>'
        secs.append(('010-header', first))
        ec = find(main_node, lambda x: 'entry-content' in x.cls())
        k = 20
        kinds = []
        for child in ec.kids:
            if isinstance(child, str) or not child.tag == 'div' and not child.tag == 'section':
                continue
            c = child.cls()
            before = len(secs)
            if 'generic-content' in c:
                body = ''.join(render(x, name) for x in child.kids).strip()
                body = re.sub(r'<h2></h2>', '', body)
                if not re.sub(r'<[^>]*>|&nbsp;|\s', '', body) and '<picture' not in body:
                    continue
                els = [x for x in child.kids if not isinstance(x, str)]
                if len(els) > 1 and els[0].tag == 'h2' and els[1].tag == 'p':
                    im = find(els[1], lambda x: x.tag == 'img')
                    if im is not None and 'alignnone' in im.cls():
                        body += '<div class="section-metadata"><div><div>Style</div><div>flush-image</div></div></div>'
                h2 = next((x for x in child.kids if not isinstance(x, str) and x.tag == 'h2'), None)
                if h2 is not None and 'text-align: center' in (h2.attrs.get('style') or ''):
                    body += '<div class="section-metadata"><div><div>Style</div><div>title-center</div></div></div>'
                secs.append((f'{k:03d}-text', body))
            elif 'spacer' in c:
                # 20px gap after the previous section
                if secs and 'space-after' not in secs[-1][1]:
                    fn, body = secs[-1]
                    if 'section-metadata' in body:
                        body = body.replace('</div></div></div>', ', space-after</div></div></div>', 1) if False else re.sub(r'(Style</div><div>)([^<]*)', r'\1\2, space-after', body)
                    else:
                        # a list ends with a 25px item margin instead of the 20px paragraph margin
                        style = 'space-after-list' if re.search(r'</(ul|ol)>$', body) else 'space-after'
                        body += f'<div class="section-metadata"><div><div>Style</div><div>{style}</div></div></div>'
                    secs[-1] = (fn, body)
                continue
            elif 'content-carousel' in c:
                slides = {}
                for sl in walk(child):
                    if not isinstance(sl, str) and 'swiper-slide' in sl.cls() and sl.attrs.get('data-swiper-slide-index') is not None:
                        slides.setdefault(int(sl.attrs['data-swiper-slide-index']), sl)
                rows = ''
                for idx in sorted(slides):
                    sc = find(slides[idx], lambda x: 'slide-content' in x.cls())
                    rows += '<div><div>' + ''.join(render(x, name) for x in sc.kids if not isinstance(x, str)) + '</div></div>'
                secs.append((f'{k:03d}-carousel', f'<div class="carousel">{rows}</div>'))
            elif 'highlighted-content' in c:
                body = ''.join(render(x, name) for x in find(child, lambda x: 'highlighted-content-container' in x.cls()).kids).strip()
                secs.append((f'{k:03d}-highlight', body + '<div class="section-metadata"><div><div>Style</div><div>band, highlight</div></div></div>'))
            elif 'quote-component' in c:
                q = find(child, lambda x: 'quote' in x.cls() and x.tag != 'div' or x.cls() == ['quote'])
                a = find(child, lambda x: 'author' in x.cls())
                body = f'<p>{html.escape(text(q).strip(), quote=False)}</p><p>{html.escape(text(a).strip(), quote=False)}</p>'
                secs.append((f'{k:03d}-quote', body + '<div class="section-metadata"><div><div>Style</div><div>band, quote</div></div></div>'))
            else:
                print(f'  {name}: unhandled {child.tag}.{".".join(c)} (skipped)')
                continue
            k += 10
        last = ec.kids[-1] if ec.kids else None
        kids = [x for x in ec.kids if not isinstance(x, str)]
        if kids and 'generic-content' in kids[-1].cls() and not text(kids[-1]).strip() and secs and 'section-metadata' in secs[-1][1]:
            fn, body = secs[-1]
            secs[-1] = (fn, re.sub(r'(Style</div><div>)([^<]*)', r'\1\2, end-gap', body))
        secs.append(('999-metadata', f'<div class="metadata"><div><div>title</div><div>{html.escape(title, quote=False)} - Santa Fe Natural Tobacco Company</div></div></div>'))
        for fn, body in secs:
            (out / f'{fn}.html').write_text(body + '\n')
        print(name, [s[0] for s in secs])


main()
