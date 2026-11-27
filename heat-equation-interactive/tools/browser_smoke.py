#!/usr/bin/env python3
"""Optional Chromium regression test; defaults to serving the actual split assets."""
import argparse
import base64
import functools
import http.server
import re
import threading
from pathlib import Path
from urllib.parse import urlsplit
from export_data import read_dataset
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'

class RepoHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urlsplit(path).path.removeprefix('/project/')
        return super().translate_path('/' + path.lstrip('/'))
    def log_message(self, *args): pass

def embed_assets():
    # Keep separate classic script execution, in the original document order.
    def substitute(m):
        asset = SITE / m[2]
        mime = 'text/css' if asset.suffix == '.css' else 'text/javascript'
        return m[1] + 'data:' + mime + ';base64,' + base64.b64encode(asset.read_bytes()).decode('ascii') + m[3]
    return re.sub(r'(<link[^>]*?href="|<script[^>]*?src=")(assets/[^\"]+)(")', substitute, (SITE/'index.html').read_text(encoding='utf-8'))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embedded-assets', action='store_true', help='Use data URLs when direct local HTTP is blocked.')
    parser.add_argument('--chromium', help='Optional path to system Chromium.')
    args = parser.parse_args()
    server = None
    if not args.embedded_assets:
        server = http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(RepoHandler,directory=str(SITE)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}/' if server else None
    try:
        with sync_playwright() as pw:
            launch = {'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
            if args.chromium: launch['executable_path']=args.chromium
            browser = pw.chromium.launch(**launch)
            page = browser.new_page(viewport={'width':1440,'height':900})
            errors, failures, external, http_errors = [], [], [], []
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('requestfailed',lambda r:failures.append(r.url[:200]))
            page.on('response',lambda r:http_errors.append((r.status,r.url[:200])) if r.status>=400 else None)
            page.on('request',lambda r:external.append(r.url[:200]) if not r.url.startswith(('data:','blob:')) and (origin is None or not r.url.startswith(origin)) else None)
            if args.embedded_assets: page.set_content(embed_assets(),wait_until='load',timeout=60000)
            else: page.goto(origin+'project/',wait_until='load',timeout=60000)
            page.wait_for_function("window.MathJax?.startup?.document && document.querySelectorAll('mjx-container').length > 0",timeout=60000)
            page.evaluate('MathJax.startup.promise')
            page.wait_for_function('typeof pd!=="undefined" && pd?.frames?.length===61',timeout=40000)
            # Baseline counts for V5.1. Update intentionally if the monograph grows.
            counts=page.evaluate('''()=>({math:document.querySelectorAll('mjx-container').length,errors:document.querySelectorAll('mjx-merror,[data-mml-node="merror"]').length,figures:document.querySelectorAll('figure').length,players:players.size,frames:pd.frames.length,chapters:document.querySelectorAll('section.chapter[id^="ch"]').length})''')
            print('Rendering and worker:', counts, flush=True)
            assert counts=={'math':3357,'errors':0,'figures':74,'players':54,'frames':61,'chapters':14}, counts
            assert page.evaluate('window.chapter11Data')==read_dataset(), 'Dataset mismatch'
            for id in page.evaluate('Array.from(players.keys())'):
                assert page.evaluate('id=>{const p=players.get(id);p.button.click();const ok=activePlayer===p;stopPlayback(id);return ok}',id), id
            print('All 54 playback controls started and stopped.',flush=True)
            search=page.locator('#tocSearch50');search.fill('trajectory stability')
            assert page.locator('#toc a').filter(has_text=re.compile('trajectory stability',re.I)).count()>0
            search.fill('')
            page.evaluate("document.documentElement.style.scrollBehavior='auto';document.getElementById('ch7').scrollIntoView({behavior:'instant',block:'start'})")
            page.wait_for_timeout(500)
            assert page.evaluate("document.querySelector('#toc .toc-chapter50[open] .toc-start50')?.hash==='#ch7'")
            print('Contents search and current chapter tracking passed.',flush=True)
            for width in (1440,768,390):
                page.set_viewport_size({'width':width,'height':850});page.wait_for_timeout(300)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                if width<=1000:
                    page.evaluate("document.getElementById('menu').click()")
                    assert page.locator('#menu').get_attribute('aria-expanded')=='true'
                    page.keyboard.press('Escape')
                    assert page.locator('#menu').get_attribute('aria-expanded')=='false'
                print(f'Viewport {width}px passed.',flush=True)
            page.set_viewport_size({'width':1440,'height':900})
            page.evaluate("document.getElementById('fig-macro31').scrollIntoView({behavior:'instant'})")
            page.wait_for_function("document.getElementById('fig-macro31').textContent.includes('Completed estimate')",timeout=20000)
            print('Deferred Monte Carlo field completed.',flush=True)
            # The difference view must preserve the original solver.
            page.evaluate("document.querySelector('.pde-view51 button:nth-of-type(2)').click()")
            assert page.locator('.pde-view51 button').nth(1).get_attribute('aria-pressed')=='true'
            page.evaluate("document.querySelector('.pde-view51 button:nth-of-type(1)').click()")
            assert page.locator('.pde-view51 button').nth(0).get_attribute('aria-pressed')=='true'
            assert not errors and not failures and not external and not http_errors, (errors, failures, external, http_errors)
            print('Browser smoke test passed ('+('embedded assets' if args.embedded_assets else 'HTTP')+').')
            browser.close()
    finally:
        if server: server.shutdown(); server.server_close()

if __name__=='__main__': main()
