# V5.2 mobile performance audit

## Findings

At 390 CSS pixels, Chromium computed `position: fixed` for the previous/next chapter rows. The mobile `nav` rule in `base.css` applied to both the contents drawer and the landmark rows added by `editorial.js`. The later `.chapter-step51` rule restored `display: flex`, exposing each fixed row. The sidebar rules now target `nav#toc`. The chapter rows compute to `position: static`. The drawer and its backdrop follow the measured sticky header height, and the drawer has independent scrolling and safe-area padding.

The original page eagerly rendered 3,357 MathJax SVGs, drew 93 canvases, retained a default continuous PDE worker, and performed document-wide or chapter-wide redraws on resize and disclosure changes. Three intervals polled playback-dependent state even when idle. The comparison below confirms the startup workload and the overlay's CSS cause. The reported Safari process failure could involve memory pressure, main-thread work, or another WebKit-specific behavior. No iOS crash trace or physical-device measurement was available to distinguish these possibilities.

The generated HTML is still approximately 624 KiB, and local MathJax and the Chapter 11 dataset total roughly 4 MiB on disk. The parser, editorial setup and TeX discovery still traverse the full document. Math rendering queues viewport-adjacent containers in batches of at most eight, with one MathJax operation at a time. The original TeX remains in place until rendering, equation links and copy controls use the existing IDs and original source, and there are no TeX label or reference macros that depend on a document-wide compilation order. Print uses the full MathJax render.

## Figures and numerical work

- Plot canvases reserve layout space using their existing CSS dimensions. IntersectionObserver activates plots near the reader and releases off-screen backing stores by shrinking them to 1 × 1. ResizeObserver watches active canvases and coalesces redraws using animation frames. The display DPR cap is 1.5 at widths up to 1000 px and 2 above that width. A plot redraw uses the existing controls and numerical state.
- Shared playback allows one running animation. It stops when its figure leaves the reading area or when the tab is hidden. Synchronized views listen for playback changes instead of polling. Viewport observers are registered once per plot.
- The PDE starts near its figure. Changing parameters invalidates older replies and terminates the previous worker. A fixed-horizon worker exits after delivering frames. Continuous mode keeps one solver alive so extension can continue from the same state. The existing cap of 1,201 cached frames remains, equivalent to about 11.8 MiB of Float32 field values at the cap, plus diagnostics and worker state. Pausing retains the current frame and range.
- The large Monte Carlo field yields between groups of paths and grid cells, abandons a superseded run, and retains just the 14 plotted paths after all 192 contribute to the same estimates. Smaller explicit and near-viewport probability comparisons still run synchronously. The discretizations, seeds, solver source and precomputed data are unchanged.
- Narrow layouts allow raw TeX to wrap before MathJax replaces it and constrain wide formulas and controls within the article. The browser tests cover viewport resizing. Native Safari toolbar transitions, safe-area behavior and orientation changes still require device testing.

## Architecture comparison

| Architecture | Startup and memory | Navigation and maintenance |
| --- | --- | --- |
| Optimized single document, implemented | Keeps the original HTML and downloads the local scripts and datasets. Defers SVG and canvas work. Canvases are released off screen. Rendered SVGs accumulate while reading new sections. | Keeps cross-references, fragment URLs, continuous reading, search and browser find in one document. |
| Mount and unmount sections, evaluated as a design | Can cap live DOM and SVG by mounted section if detached DOM and associated data are released. Requires measurement with a prototype. | Needs a global anchor index, height estimates, explicit scroll restoration and mount/unmount hooks for interactions. Browser find and copying across sections would need new behavior. |
| Separate chapter pages, evaluated as a design | Can limit parsed HTML, data and figures to the current page. A bounded set of chapter assets can be cached. Requires measurement with a prototype. | Needs build-generated cross-page links and search, and an entry page that routes existing fragment URLs. Native navigation is predictable, but moves between chapters interrupt continuous reading. |

The single document was retained because the observed startup allocation and repeated-navigation footprint fell sharply, while preserving the existing URL and reading model. This is a decision based on desktop Chromium measurements. A sustained physical-iPhone failure or unacceptable memory growth while reading all chapters would justify prototyping separate static pages using the same modular fragments.

## Benchmark

Chromium 156 on the same Linux machine, with fresh browser contexts, a 390 × 844 viewport, DPR 3, and local HTTP. Initial snapshots were taken two seconds after the load event. Repeated navigation jumped among Chapters 6, 10, 13 and 0 three times with the same 180 ms dwell per chapter. These are single-run observations, with no network or CPU throttling. Reproduce with `python3 tools/mobile_benchmark.py PATH_TO_DOCS` on each revision.

| Metric | V5.1 (`9e2e91f`) | V5.2 |
| --- | ---: | ---: |
| Load event | 10,124 ms | 1,324 ms |
| DOM ready | 9,538 ms | 1,231 ms |
| First contentful paint (proxy for initial readability) | 656 ms | 640 ms |
| First Gaussian plot after approaching it, post-load | <1 ms | 78 ms |
| Initially rendered math | 3,357 | 10 |
| Initial DOM elements | 179,488 | 7,829 |
| Initially allocated article canvases | 93 | 0 |
| Estimated initial RGBA backing stores | 121.34 MiB | 0 MiB |
| Initial live workers / playback loops | 1 / 0 | 0 / 0 |
| Initial JS heap after forced collection | 60.69 MiB | 8.79 MiB |
| JS heap after repeated navigation | 60.71 MiB | 9.70 MiB |
| Estimated canvas backing stores after repeated navigation | 121.34 MiB | <0.001 MiB |
| Initial long tasks ≥50 ms / longest | 9 / 7,575 ms | 5 / 191 ms |
| Long tasks through repeated navigation | 19 | 9 |

The first late plot pays a small deferred initialization cost that the baseline had already paid by the load event. The backing-store estimate assumes 4 bytes per pixel and excludes browser, compositor, temporary, and GPU allocations. CDP heap excludes much native memory. Total WebKit/iOS process memory, a frame-by-frame layout trace, energy use and memory after a complete reading session were unavailable. Repeated navigation visits a small subset of the document and cannot establish a long-session memory ceiling.

The full 61-frame default PDE result, including all three sampled fields and diagnostics, produced the same SHA-256 on both revisions (`a771d661b0ee3005fcc69748de354d157fb6cc7f35a3b689d1e679550da292a5`). The seeded Monte Carlo field agreed at the default observation point, 1.3858 ± 0.0401 (one sample standard error).

## Physical-iPhone acceptance checks

1. Open the reviewed branch build over HTTPS in both Safari and the Slack in-app browser. Repeat cold loads on the oldest supported iPhone and a current model. Record device, iOS version, browser, crashes and any diagnostics.
2. In portrait and landscape, show and hide Safari's toolbar. Open the contents drawer, scroll to its bottom, search for a late theorem, and dismiss using the backdrop and an external keyboard if available. Check header alignment, focus and safe areas.
3. Open a previously shared theorem and equation fragment from outside the page. Check that each target is visible and rendered, that TeX copy works, and that history and previous/next links place the reader at the intended chapter.
4. Scroll rapidly across multiple chapters and back, expand and collapse proofs, and swipe across long formulas and tables. Confirm the page itself stays within the viewport.
5. Start, pause and reset the Gaussian and PDE views. Scroll away or background Safari during playback, then return and check the selected frame. Change solver parameters repeatedly, run a fixed horizon, and extend continuous mode. Run the Chapter 10 Monte Carlo field and verify its seeded readout.
6. Repeat navigation through all chapters and appendices, then revisit the numerical figures. Record any slowdown, reload or blank plot. Where available, capture Safari Web Inspector timelines and process memory.
