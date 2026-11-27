#!/usr/bin/env python3
"""Profile a site directory over HTTP with a 390px, DPR 3 Chromium viewport."""
import argparse
import functools
import hashlib
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site', type=Path)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    handler = functools.partial(SimpleHTTPRequestHandler, directory=args.site)
    with ThreadingHTTPServer(('127.0.0.1', 0), handler) as server, sync_playwright() as pw:
        Thread(target=server.serve_forever, daemon=True).start()
        browser = pw.chromium.launch(executable_path=args.chromium, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        page.add_init_script("""(() => {
            window.longTasks = [];
            window.liveWorkers = 0;
            const OriginalWorker = window.Worker;
            window.Worker = class extends OriginalWorker {
                constructor(...args) { super(...args); liveWorkers++; }
                terminate() { liveWorkers--; super.terminate(); }
            };
            window.contexts = new WeakSet();
            const getContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(...args) {
                const context = getContext.apply(this, args);
                if (context) contexts.add(this);
                return context;
            };
            new PerformanceObserver(list => longTasks.push(...list.getEntries().map(e => e.duration)))
                .observe({type: 'longtask', buffered: true});
        })()""")
        cdp = page.context.new_cdp_session(page)

        def collect():
            cdp.send('HeapProfiler.collectGarbage')
            sample = page.evaluate("""() => {
                const canvases = [...document.querySelectorAll('canvas')].filter(c => contexts.has(c));
                const active = canvases.filter(c => c.width > 1 && c.height > 1);
                const nav = performance.getEntriesByType('navigation')[0];
                return {
                    loadMs: nav.loadEventEnd,
                    domReadyMs: nav.domContentLoadedEventEnd,
                    firstContentfulPaintMs: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
                    elements: document.querySelectorAll('*').length,
                    math: document.querySelectorAll('mjx-container').length,
                    initializedCanvases: active.length,
                    estimatedCanvasMiB: canvases.reduce((s,c) => s + 4*c.width*c.height, 0) / 2**20,
                    liveWorkers,
                    livePlaybackLoops: Number(!!playFrame),
                    longTaskCount: longTasks.length,
                    maxLongTaskMs: Math.max(0, ...longTasks),
                    chapterNavPosition: getComputedStyle(document.querySelector('.chapter-step51')).position
                };
            }""")
            sample['jsHeapMiB'] = cdp.send('Runtime.getHeapUsage')['usedSize'] / 2**20
            return sample

        def visit(element_id):
            page.evaluate("id => document.getElementById(id).scrollIntoView({behavior:'instant'})", element_id)

        try:
            page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='load')
            page.wait_for_timeout(2000)
            report = {'initial': collect()}
            report['firstFigureFromScrollMs'] = page.evaluate("""async () => {
                const t = performance.now(), canvas = document.getElementById('gauss');
                canvas.scrollIntoView({behavior:'instant'});
                while ((!contexts.has(canvas) || canvas.width <= 1) && performance.now()-t < 5000)
                    await new Promise(requestAnimationFrame);
                if (!contexts.has(canvas) || canvas.width <= 1) throw Error('Gaussian plot did not initialize');
                return performance.now()-t;
            }""")
            for chapter in ['ch6', 'ch10', 'ch13', 'ch0'] * 3:
                visit(chapter)
                page.wait_for_timeout(180)
            report['repeatedNavigation'] = collect()
            visit('fig-pde')
            page.wait_for_function('pd?.frames.length === 61', timeout=90000)
            arrays = page.evaluate("pd.frames.map(({n,f,m,ref,fs,ms,rs}) => [n,[...f],[...m],[...ref],fs,ms,rs])")
            report['pdeSha256'] = hashlib.sha256(json.dumps(arrays).encode()).hexdigest()
            visit('fig-macro31')
            page.wait_for_function("document.getElementById('macro31read').textContent.includes('Completed estimate')")
            report['monteCarlo'] = page.locator('#macro31read').inner_text()
            print(json.dumps(report, indent=2))
        finally:
            browser.close()
            server.shutdown()


if __name__ == '__main__':
    main()
