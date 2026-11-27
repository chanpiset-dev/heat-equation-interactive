#!/usr/bin/env python3
"""Assemble the static GitHub Pages site with Python's standard library only."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
SOURCE, SITE = ROOT / 'src', ROOT / 'docs'

class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'a' and a.get('href','').startswith('#'):
            self.links.append(unquote(a['href'][1:]))
        if tag == 'script' and a.get('src'): self.assets.append(a['src'])
        if tag == 'link' and a.get('rel') == 'stylesheet': self.assets.append(a['href'])
    handle_startendtag = handle_starttag

def outputs():
    manifest = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8'))
    content = ''.join((SOURCE / 'content' / f).read_text(encoding='utf-8') for f in manifest['content'])
    nav = (SOURCE / 'navigation.html').read_text(encoding='utf-8')
    template = (SOURCE / 'template.html').read_text(encoding='utf-8')
    assert template.count('{{ARTICLE_CONTENT}}') == template.count('{{NAVIGATION}}') == 1
    html = template.replace('{{ARTICLE_CONTENT}}', content).replace('{{NAVIGATION}}', nav)
    worker = (SOURCE / 'workers/pde-worker.js').read_text(encoding='utf-8')
    return {
        SITE / 'index.html': html,
        SITE / 'assets/js/generated/pde-worker-source.js': '// Generated from src/workers/pde-worker.js; do not edit.\nconst WORKER_SOURCE = '+json.dumps(worker,ensure_ascii=True)+';\n',
        SITE / '.nojekyll': ''
    }

def validate(html):
    a=PageAudit(); a.feed(html)
    ids=set(a.ids)
    if len(ids)!=len(a.ids): raise ValueError('Duplicate HTML IDs')
    missing=sorted(set(a.links)-ids-{''})
    if missing: raise ValueError('Unresolved internal anchors: '+str(missing))
    for path in a.assets:
        if urlsplit(path).scheme or path.startswith('/'):
            raise ValueError('Use repository-relative asset paths: '+path)
        if not (SITE / path).is_file(): raise FileNotFoundError(path)
    print(f'{len(ids)} unique IDs, {len(a.links)} internal links, {len(a.assets)} local CSS/JS assets verified.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify committed generated files are up to date.')
    args=parser.parse_args()
    for path, text in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                raise SystemExit(f'Out of date: {path.relative_to(ROOT)}. Run python3 build.py.')
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text,encoding='utf-8')
    validate((SITE / 'index.html').read_text(encoding='utf-8'))
    print('Site '+('verified' if args.check else 'built')+': docs/index.html')
