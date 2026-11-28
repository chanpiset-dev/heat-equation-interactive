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
        path = urlsplit(path).path.removeprefix('/heat-equation-interactive/')
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
    parser.add_argument('--browser', choices=['chromium','firefox','webkit'], default='chromium')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    server = None
    if not args.embedded_assets:
        server = http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(RepoHandler,directory=str(SITE)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}/' if server else None
    try:
        with sync_playwright() as pw:
            launch = {'headless': True}
            if args.browser == 'chromium':
                launch['args'] = ['--no-sandbox', '--disable-dev-shm-usage']
                if args.chromium:
                    launch['executable_path'] = args.chromium
            browser = getattr(pw, args.browser).launch(**launch)
            page = browser.new_page(viewport={'width':390,'height':844}, device_scale_factor=3)
            errors, failures, external, http_errors = [], [], [], []
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('requestfailed',lambda r:failures.append(r.url[:200]))
            page.on('response',lambda r:http_errors.append((r.status,r.url[:200])) if r.status>=400 else None)
            page.on('request',lambda r:external.append(r.url[:200]) if not r.url.startswith(('data:','blob:')) and (origin is None or not r.url.startswith(origin)) else None)
            if args.embedded_assets: page.set_content(embed_assets(),wait_until='load',timeout=60000)
            else: page.goto(origin+ 'heat-equation-interactive/',wait_until='load',timeout=60000)
            page.wait_for_function("window.MathJax?.startup?.document && document.querySelectorAll('mjx-container').length > 0",timeout=60000)
            page.evaluate('MathJax.startup.promise')
            assert page.locator('mjx-container').count() < 100
            assert page.evaluate('!pd && !activeWorker && allocatedPlots.size === 0')
            assert page.locator('.chapter-step51').first.evaluate("(e) => getComputedStyle(e).position") == 'static'
            proof = page.locator('article details[data-disclosure="proof"]').first
            proof.locator('summary').click()
            assert proof.get_attribute('open') is not None
            proof.locator('summary').click()
            assert proof.get_attribute('open') is None
            page.locator('#gauss').scroll_into_view_if_needed()
            page.wait_for_function("allocatedPlots.has(document.getElementById('gauss'))")
            assert page.locator('#gauss').evaluate('c => c.width / c.getBoundingClientRect().width') <= 1.51
            page.locator('#gplay').click()
            assert page.locator('#gplay').get_attribute('aria-pressed') == 'true'
            page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
            assert page.locator('#gplay').get_attribute('aria-pressed') == 'false'
            page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
            page.locator('#gplay').click()
            page.evaluate("document.getElementById('ch3').scrollIntoView({behavior:'instant'})")
            page.wait_for_function("!activePlayer && !allocatedPlots.has(document.getElementById('gauss'))")
            page.locator('#greset').click()
            page.locator('#fig-pde').evaluate("e => e.scrollIntoView({behavior:'instant'})")
            page.wait_for_function('typeof pd!=="undefined" && pd?.frames?.length===61',timeout=40000)
            assert page.evaluate('activeWorker !== null')
            page.evaluate("document.getElementById('phorizon').value='.42';document.getElementById('phorizon').dispatchEvent(new Event('input'))")
            page.wait_for_function('pd?.frames.length === 61 && activeWorker === null')
            print('Progressive load, proof disclosure, playback, simulated backgrounding and deferred PDE passed.', flush=True)
            # Exercise the existing numerical baseline before the full typesetting audit.
            page.locator('#fig-macro31').evaluate("e=>e.scrollIntoView({behavior:'instant'})")
            page.wait_for_function("document.getElementById('fig-macro31').textContent.includes('Completed estimate')", timeout=30000)
            assert page.evaluate('window.chapter11Data')==read_dataset(), 'Dataset mismatch'
            for id in page.evaluate('Array.from(players.keys())'):
                page.evaluate("id => players.get(id).button.closest('figure')?.scrollIntoView({behavior:'instant'})", id)
                page.wait_for_timeout(80)
                assert page.evaluate('id=>{const p=players.get(id);p.button.click();const ok=activePlayer===p;stopPlayback(id);return ok}',id), id
            print('All 54 playback controls started and stopped.',flush=True)
            page.set_viewport_size({'width':1440,'height':900})
            search=page.locator('#tocSearch50');search.fill('trajectory stability')
            assert page.locator('#toc a').filter(has_text=re.compile('trajectory stability',re.I)).count()>0
            search.fill('contraction of the Neumann semigroup')
            math_result = page.locator('.toc-results50 a[href="#lemma-l2-contraction"] mjx-container')
            math_result.wait_for(state='visible')
            search.fill('')
            page.evaluate("document.documentElement.style.scrollBehavior='auto';document.getElementById('ch7').scrollIntoView({behavior:'instant',block:'start'})")
            page.wait_for_timeout(500)
            assert page.evaluate("document.querySelector('#toc .toc-chapter50[open] .toc-start50')?.hash==='#ch7'")
            print('Contents search and current chapter tracking passed.',flush=True)
            for width in (320,375,390,430,768,1024,1440):
                page.set_viewport_size({'width':width,'height':850});page.wait_for_timeout(300)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                if width<=1000:
                    page.evaluate("document.getElementById('menu').click()")
                    assert page.locator('#menu').get_attribute('aria-expanded')=='true'
                    assert page.locator('#toc').evaluate('e => e.scrollHeight > e.clientHeight')
                    page.locator('#toc').evaluate('e => e.scrollTop = 100')
                    assert page.locator('#toc').evaluate('e => e.scrollTop > 0')
                    if args.screenshots and width == 390:
                        args.screenshots.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=args.screenshots / 'mobile-drawer.png')
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
            page.evaluate("dispatchEvent(new Event('beforeprint'))")
            counts=page.evaluate('''()=>({math:document.querySelectorAll('article mjx-container').length,errors:document.querySelectorAll('mjx-merror,[data-mml-node="merror"]').length,figures:document.querySelectorAll('figure').length,players:players.size,frames:pd.frames.length,chapters:document.querySelectorAll('section.chapter[id^="ch"]').length})''')
            print('Rendering and worker:', counts, flush=True)
            assert page.evaluate("() => {const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return new Set(ids).size===ids.length}"), 'Duplicate runtime IDs'
            assert counts=={'math':4671,'errors':0,'figures':74,'players':54,'frames':61,'chapters':14}, counts
            assert not page.evaluate(r'''() => {
                const walker = document.createTreeWalker(document.querySelector('article'), NodeFilter.SHOW_TEXT);
                while (walker.nextNode()) {
                    const n = walker.currentNode;
                    if (!n.parentElement.closest('svg,script,pre,code,select,textarea') && /\\[\[(]/.test(n.nodeValue))
                        return n.nodeValue.trim();
                }
                return '';
            }'''), 'Unrendered TeX after the complete article render'
            page.set_viewport_size({'width':320,'height':850})
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.set_viewport_size({'width':1440,'height':900})
            if not args.embedded_assets:
                equation = page.locator('article .eq[id]').last.get_attribute('id')
                for target in ['thm-stability13', equation, 'lemma-trace']:
                    page.goto('about:blank')
                    page.goto(origin + 'heat-equation-interactive/#' + target, wait_until='domcontentloaded')
                    page.wait_for_function('id => !!document.getElementById(id)?.querySelector("mjx-container")',
                                           arg=target, timeout=30000)
                    assert page.evaluate('id => {const r=document.getElementById(id).getBoundingClientRect();return r.top>=0 && r.top<innerHeight}', target)
                equation_box = page.locator('#lemma-trace .eq')
                page.evaluate("Object.defineProperty(navigator.clipboard, 'writeText', {configurable:true,value: async text => {window.copiedTex = text;}})")
                equation_box.locator('button.copy').evaluate("button => button.click()")
                page.wait_for_function(r"window.copiedTex?.includes('\\tag{B.1}')")
                print('Cold theorem, equation and appendix fragments and original TeX copy passed.', flush=True)
                page.evaluate("document.documentElement.style.scrollBehavior='auto'")
                for chapter in ['ch6', 'ch10', 'ch13', 'ch0'] * 3:
                    page.evaluate("id => document.getElementById(id).scrollIntoView()", chapter)
                    page.wait_for_timeout(100)
                page.wait_for_function('allocatedPlots.size === 0')
                step = page.locator('#ch0 .chapter-step51 a').last
                step.click()
                assert page.url.endswith('#ch1')
                assert step.evaluate('e => getComputedStyle(e.parentElement).position') == 'static'
                if args.screenshots:
                    page.goto(origin + 'heat-equation-interactive/')
                    page.wait_for_function("document.querySelector('mjx-container')")
                    page.screenshot(path=args.screenshots / 'desktop.png')
                    page.set_viewport_size({'width':390,'height':844})
                    page.screenshot(path=args.screenshots / 'mobile.png')
            assert not errors and not failures and not external and not http_errors, (errors, failures, external, http_errors)
            print('Browser smoke test passed ('+('embedded assets' if args.embedded_assets else 'HTTP')+').')
            browser.close()
    finally:
        if server: server.shutdown(); server.server_close()

if __name__=='__main__': main()
