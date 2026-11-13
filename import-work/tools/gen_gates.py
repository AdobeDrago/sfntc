#!/usr/bin/env python3
"""Write gate/<page>.json for inner pages from the captured source DOM: header, page-header,
crumbs, one entry per content child that becomes a section, footer.
Source: main .entry-content > :nth-child(n); rebuild: the matching section (or its default
content wrapper)."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
pages = json.loads((ROOT / 'pages.json').read_text())['pages']


def children(dom):
    s = dom[dom.index('class="entry-content'):dom.index('</main>')]
    s = s[s.index('>') + 1:]
    depth, out, start, cls = 0, [], 0, ''
    for m in re.finditer(r'<(/?)(div|section)\b([^>]*)>', s):
        if not m.group(1):
            if depth == 0:
                start = m.start()
                c = re.search(r'class="([^"]*)"', m.group(3))
                cls = c.group(1) if c else ''
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((cls, s[start:m.end()]))
            if depth < 0:
                break
    return out


for name, spec in pages.items():
    if name == 'home' or (sys.argv[1:] and name not in sys.argv[1:]):
        continue
    dom = (ROOT / spec['bundle'] / 'dom.html').read_text()
    secs = [{"name": "header", "source": "header.site-header", "rebuild": "header"},
            {"name": "page-header", "source": "main .page-header", "rebuild": "main .page-header"},
            {"name": "crumbs", "source": "main > .page-container", "rebuild": "main .page-header-crumbs"}]
    idx = 1  # rebuild section index (section 1 is the page header)
    n = 0
    for i, (cls, body) in enumerate(children(dom), 1):
        c = cls.split()
        if 'spacer' in c:
            continue
        if 'generic-content' in c:
            txt = re.sub(r'<[^>]+>|&nbsp;|\s', '', body)
            if not txt and '<img' not in body:
                continue
            kind = 'text'
        elif 'highlighted-content' in c or 'quote-component' in c:
            kind = 'band'
        elif 'content-carousel' in c:
            kind = 'block'
        else:
            continue
        idx += 1
        n += 1
        reb = f"main > .section:nth-child({idx})" + ''
        secs.append({"name": f"content{n}", "source": f"main .entry-content > :nth-child({i})", "rebuild": reb})
    secs.append({"name": "footer", "source": "footer.site-footer", "rebuild": "footer"})
    g = {"site": "../site.json", "page": name, "source": spec['source'],
         "rebuild": "http://localhost:3017/" + ('' if spec['path'] == 'index' else spec['path']),
         "widths": [1440, 1280], "out": f"work/gate/{name}", "bundle": f"../work/bundles/{name}",
         "timelines": [], "sections": secs}
    (ROOT / 'gate' / f'{name}.json').write_text(json.dumps(g, indent=1))
    print(name, len(secs))
