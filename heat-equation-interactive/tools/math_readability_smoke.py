#!/usr/bin/env python3
"""Exercise progressive math roots and proof disclosure on the generated site."""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

from browser_smoke import RepoHandler, SITE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()

    with ThreadingHTTPServer(('127.0.0.1', 0), partial(RepoHandler, directory=SITE)) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        origin = f'http://127.0.0.1:{server.server_port}/heat-equation-interactive/'
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(executable_path=args.chromium, args=['--no-sandbox'])
                page = browser.new_page(viewport={'width': 390, 'height': 844})
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                def console_error(message):
                    url = message.location.get('url', '')
                    if message.type == 'error' and not url.endswith('/favicon.ico'):
                        errors.append(message.text)
                page.on('console', console_error)
                page.goto(origin)
                page.wait_for_function("document.querySelector('article mjx-container')")
                assert page.locator('article mjx-container').count() < 100

                # Reproduce zero-area contact at the observer's preload boundary
                # before moving the mixed-content DD into the viewport.
                gronwall = page.locator('#app-gronwall + dd')
                gronwall.evaluate("""e => Object.assign(e.style, {
                    position: 'fixed', top: (innerHeight + 350) + 'px', left: '16px', right: '16px'
                })""")
                page.wait_for_timeout(120)
                assert gronwall.locator('mjx-container').count() == 0
                gronwall.evaluate("e => e.style.top = (innerHeight - 300) + 'px'")
                gronwall.locator(':scope > mjx-container').first.wait_for()
                gronwall.locator(':scope > .eq mjx-container').wait_for()
                assert gronwall.locator(':scope > mjx-container').count() == 6
                assert gronwall.locator('details mjx-container').count() == 0
                gronwall.evaluate("e => e.removeAttribute('style')")
                print('Zero-area preload contact, nested display, and closed proof passed.', flush=True)

                page.goto('about:blank')
                page.goto(origin + '#app-gronwall-factor')
                inner_eq = page.locator('#app-gronwall-factor')
                inner_eq.locator('mjx-container').wait_for()
                proof = page.locator('#app-gronwall + dd details')
                assert proof.get_attribute('open') is not None
                page.evaluate("""Object.defineProperty(navigator.clipboard, 'writeText',
                    {configurable:true, value: async text => {window.copiedTex = text;}})""")
                inner_eq.locator('.copy').evaluate('button => button.click()')
                page.wait_for_function(r"window.copiedTex?.includes('\\int_0^t')")
                proof.locator('summary').focus()
                page.keyboard.press('Enter')
                assert proof.get_attribute('open') is None
                page.keyboard.press('Enter')
                assert proof.get_attribute('open') is not None
                assert inner_eq.locator('mjx-container').count() == 1

                for id in ('app-monotone', 'app-fatou'):
                    item = page.locator(f'#{id} + dd')
                    item.locator('summary').click()
                    assert item.locator('details').get_attribute('open') is not None
                    item.locator('details mjx-container').first.wait_for()
                assert page.locator('#app-monotone + dd details[open]').count() == 1
                assert page.locator('#app-fatou + dd details[open]').count() == 1

                page.locator('#menu').click()
                page.locator('#tocSearch50').fill('integrating factor')
                page.locator('.toc-results50 a[href="#app-gronwall-factor"]').click()
                assert page.url.endswith('#app-gronwall-factor')
                assert page.locator('#menu').get_attribute('aria-expanded') == 'false'
                print('Direct link, keyboard, two open proofs, copying, and search passed.', flush=True)

                for id in page.locator('article > section.chapter[id^=ch], article > section.chapter[id^=app-]').evaluate_all('nodes => nodes.map(n=>n.id)'):
                    section = page.locator('#' + id)
                    eq = section.locator('.eq:visible')
                    if eq.count():
                        eq.first.evaluate("e => e.scrollIntoView({block:'center',behavior:'instant'})")
                        eq.first.locator('mjx-container').wait_for()
                    else:
                        section.evaluate("e => e.scrollIntoView({block:'start',behavior:'instant'})")
                        section.locator('mjx-container:visible').first.wait_for()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), id
                    print(f'Progressively rendered {id}', flush=True)

                variation = page.locator('#eq-brownian-variation-error')
                variation_proof = variation.locator('xpath=ancestor::details[1]')
                assert variation_proof.get_attribute('open') is None
                assert variation.locator('mjx-container').count() == 0
                page.goto(origin + '#eq-brownian-variation-error')
                variation.locator('mjx-container').wait_for()
                assert variation_proof.get_attribute('open') is not None
                variation.locator('.copy').evaluate('button => button.click()')
                page.wait_for_function(r"window.copiedTex?.includes('\\sum_{k=0}^{m-1}')")
                variation_proof.locator('summary').focus()
                page.keyboard.press('Enter')
                assert variation_proof.get_attribute('open') is None
                page.keyboard.press('Enter')
                assert variation_proof.get_attribute('open') is not None
                assert variation.locator('mjx-container').count() == 1
                print('Quadratic variation proof deferred, deep-linked, copied, and reopened.', flush=True)

                for id in ('result-11-2', 'result-11-first', 'result-11-3', 'result-11-4'):
                    assert page.locator('#' + id).evaluate("e => !e.closest('details')")
                proof.locator('summary').evaluate('e => {e.parentElement.open = false}')
                page.evaluate("dispatchEvent(new Event('beforeprint'))")
                assert proof.get_attribute('open') is not None
                assert page.locator('article mjx-merror, article [data-mml-node="merror"]').count() == 0
                page.evaluate("dispatchEvent(new Event('afterprint'))")
                assert proof.get_attribute('open') is None
                assert page.locator('#app-monotone + dd details[open]').count() == 1
                assert not errors, errors

                if args.screenshots:
                    args.screenshots.mkdir(parents=True, exist_ok=True)
                    for name, selector in (
                        ('convergence', '#app-measure40'),
                        ('holder', '#app-holder'),
                        ('gronwall', '#app-gronwall'),
                        ('theorem', '#thm31'),
                        ('technical-proof', '#eq-brownian-variation-error'),
                        ('figure', '#fig-gauss'),
                    ):
                        page.locator(selector).evaluate("e=>e.scrollIntoView({behavior:'instant',block:'start'})")
                        page.wait_for_timeout(400)
                        page.screenshot(path=args.screenshots / f'{name}.png')
                    page.locator('#menu').click()
                    page.screenshot(path=args.screenshots / 'mobile-nav.png')
                    page.keyboard.press('Escape')
                    page.set_viewport_size({'width':1440, 'height':900})
                    page.locator('#app-gronwall').evaluate("e=>e.scrollIntoView({behavior:'instant',block:'start'})")
                    page.screenshot(path=args.screenshots / 'gronwall-desktop.png')
                print('Print proof visibility and restoration passed.', flush=True)
                browser.close()
        finally:
            server.shutdown()


if __name__ == '__main__':
    main()
