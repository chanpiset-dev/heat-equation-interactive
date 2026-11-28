# Verification

## V5.3 mathematical exposition

- `python3 build.py --check` passed with 1,117 unique IDs, 550 internal links and 52 local CSS and JavaScript references. The generated site still uses the GitHub Pages directory and repository URL prefix.
- Baseline comparison preserved original IDs, equation tags, links, control attributes and all original chapter TeX expressions. The six rewritten appendices were rendered independently in Chromium; each passed with zero MathJax errors.
- The Chromium HTTP suite checked progressive rendering, complete rendering, original TeX copying, a mathematical contents result, late theorem, equation and appendix fragments, expandable proofs, the drawer, search, chapter navigation and viewport widths from 320 through 1440 CSS pixels. The complete article rendered 4,342 expressions. The test found no malformed or leftover TeX, duplicate runtime IDs, missing asset requests or uncaught JavaScript errors.
- All 74 figures, 54 playback controls and 14 chapters remain. The browser dataset matches the exported dataset, and both versions agree on the default 61-frame PDE checksum and the seeded Monte Carlo readout.
- This was Linux desktop Chromium with mobile viewport emulation. The environment blocked the desktop WebKit download. Physical iOS Safari behavior was unavailable.

See the [mathematical exposition audit](MATHEMATICAL_EXPOSITION_AUDIT.md) for the chapter and appendix review, original versus revised examples, and the V5.2/V5.3 benchmark.

## V5.2 mobile stability

- `python3 build.py --check` passed with 1,117 unique source IDs, 528 internal links and 52 local CSS/JavaScript references. The generated site is served from the same `docs/` directory used by the existing Pages workflow.
- The Chromium 156 smoke test ran over HTTP at the repository URL prefix. Viewports of 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels passed the page-width check. The viewport changes exercised responsive resizing in desktop Chromium.
- Verified cold-load deferral, canvas release and reinitialization, drawer scrolling and Escape dismissal, search, proof disclosures, fragment links to a late theorem and equation, repeated chapter jumps, previous/next navigation, playback and simulated backgrounding, fixed-horizon PDE worker release, the temperature/difference switch and the deferred Monte Carlo field.
- The full render still contains 3,357 mathematical expressions with zero MathJax errors, 74 figures, 54 working playback controls and 14 chapters. The Chapter 11 browser data equals the exported dataset. The benchmark compares the complete default 61-frame PDE result and the seeded Monte Carlo readout against V5.1.
- Browser downloads for Playwright Firefox and WebKit returned HTTP 403 from the environment network policy. Desktop WebKit and physical iPhone Safari and Slack were not exercised. The results do not establish that the reported iOS crashes are resolved.

See [the audit](MOBILE_PERFORMANCE_AUDIT.md) for benchmark methods, architecture tradeoffs and physical-iPhone checks.

## Historical V5.1 refactor verification

Baseline: accepted V5.1 Editorial Polish standalone HTML.

## Source equivalence

- All article markup (including theorem statements, proofs, TeX, references, figures, control elements and captions) was preserved verbatim.
- Article SHA-256: `419f259e195e97d0d963a3d60a1628a9d40c80b0f7f82c824375c708bc51fc41`.
- The original 18 CSS blocks were extracted without textual changes and are loaded in the same cascade order.
- Thirteen of the fifteen original JavaScript blocks (including the MathJax bundle) were preserved verbatim. The remaining two were changed only by extracting the PDE worker source and replacing the inline Chapter 11 data literal with the equivalent registered data object.
- The worker JavaScript source is exactly the decoded original worker string. The generated wrapper passes the same source to the existing blob-worker mechanism.
- The split Chapter 11 dataset was decoded and compared against the complete original data object: all values are equal. The browser data object also equals the exported dataset. Numerical algorithms, parameters and seeds have not been changed.
- The article retains the revised research paper and thesis references of V5.1. The removed original 2022 thesis was not reintroduced.

## Static build

`python3 build.py --check` passed: 1,117 unique element IDs, 528 internal links, and 50 local CSS/JavaScript asset references. All assets use relative URLs. The package includes the generated index and worker wrapper.

## Browser smoke test

Executed `python3 tools/browser_smoke.py --embedded-assets --chromium /usr/bin/chromium` successfully.

| Check | Result |
|---|---|
| Chapter count | 14 |
| Mathematical expressions rendered | 3,357 |
| MathJax errors | 0 |
| Scientific figures | 74 |
| Playback controls started/stopped | 54/54 |
| Initial PDE worker snapshots | 61 |
| Dataset equality | Pass |
| Contents search and active-chapter tracking | Pass |
| Desktop (1440px), tablet (768px), mobile (390px) overflow | Pass |
| Mobile drawer opening and Escape dismissal | Pass |
| Deferred Monte Carlo field | Pass |
| Temperature/difference switch | Pass |
| JavaScript errors, failed asset requests or external startup requests | None in the completed test |

## Limitations

The available Chromium environment blocked navigation both to a local HTTP server and a routed synthetic web origin with `ERR_BLOCKED_BY_ADMINISTRATOR`. Therefore the successful regression loaded the generated page with the individual local CSS/JavaScript resources represented as data URLs, preserving their loading order. It is a meaningful rendering and behavior regression, but it does not replace an ordinary HTTP or deployed GitHub Pages test. The included smoke test defaults to ordinary HTTP for that purpose. No live deployment was attempted. The scientific computation code and data were checked for equivalence, not independently re-derived or rerun in their entirety. This is not exhaustive cross-browser, accessibility or parameter-range certification.
