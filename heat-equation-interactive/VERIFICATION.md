# Verification

## Appendix B.9 refinement

| Check | Result |
| --- | --- |
| Static build | PASS. 1,148 unique IDs, 599 internal links, and 52 local CSS and JavaScript references. |
| Chromium HTTP browser smoke | PASS at seven widths from 320 to 1440 CSS pixels. 4,671 rendered expressions, zero MathJax errors, 74 figures, and 54 playback controls. |
| Mathematical readability suite | PASS. The B.9 URL, A.1 statement and proof URLs, Chapter 9 cross-reference, Appendix A and B contents, equation copying, touch and keyboard input, and print disclosure and restoration were verified. |
| Scientific regression | PASS. The 61-frame PDE checksum and seeded Monte Carlo readout matched V5.6. |
| WebKit and physical iOS Safari | NOT TESTED. |

The [Appendix B.9 refinement audit](APPENDIX_B9_REFINEMENT_AUDIT.md) records the baseline, proof review, test commands, and remaining physical-device checks.

## V5.6 mathematical consistency and rigor

| Check | Result |
| --- | --- |
| Static build | PASS. 1,147 unique IDs, 598 internal links, and 52 local CSS and JavaScript references. |
| Chromium HTTP browser smoke | PASS. Repo-prefixed HTTP, 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels. 4,645 rendered expressions, zero MathJax errors, no leftover mathematical TeX, 74 figures and all 54 playback controls. |
| Mathematical readability suite | PASS. Progressive math in 14 chapters and six appendices, all 14 added proof disclosures, proof-root deep links, unique B.1–B.9 navigation, search, copying, keyboard operation and print restoration. |
| Scientific regression | PASS. The 61-frame default PDE checksum and seeded Monte Carlo readout matched V5.5. |
| WebKit install | FAIL. Playwright download HTTP 403. |
| WebKit execution and physical iOS Safari | NOT RUN. No browser binary or physical device was available. |

Run the checks from the project directory:

```sh
python3 build.py
python3 build.py --check
python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium
python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium
python3 -B tools/mobile_benchmark.py docs
```

The [V5.6 audit](MATHEMATICAL_CONSISTENCY_AUDIT_V5_6.md) records the mathematical review, performance comparison and physical acceptance checklist.

## V5.5 mathematical formalization

| Check | Result |
| --- | --- |
| Static build and source comparison | PASS. 1,125 IDs, 575 internal links and 52 local CSS and JavaScript references. Original IDs, equation tags, links and scientific control attributes were preserved. |
| Chromium HTTP regression | PASS. Ran at the repository URL prefix at 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels. The full render contained 4,497 formulas with no raw TeX or MathJax errors. |
| Progressive math and proofs | PASS. Visited all 14 chapters and six appendices, including the new quadratic variation proof. Tested closed-proof deferral, direct links, TeX copying, keyboard reopen, simultaneous disclosures, search, and print restoration. |
| Scientific behavior | PASS. All 74 figures remain, and all 54 playback controls were exercised. The default PDE snapshots and Monte Carlo readout matched V5.4. |
| Playwright WebKit installation | FAIL. The browser download returned HTTP 403. |
| WebKit and physical iOS Safari | NOT RUN. The browser binary and a physical device were unavailable. |

Commands used from the project directory:

```sh
python3 build.py --check
python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium
python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium
python3 -B tools/mobile_benchmark.py docs
```

The [formalization audit](MATHEMATICAL_FORMALIZATION_AUDIT.md) records the mathematical review and baseline comparison.

## V5.4 mathematical readability

- `python3 build.py --check` verified 1,123 unique IDs, 557 internal links and 52 CSS and JavaScript references. The source audit verified balanced mathematical delimiters, preserved equation numbering, and unchanged scientific figure and control attributes.
- `python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium` exercised the GitHub Pages prefix over HTTP at 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels. It checked all 4,381 rendered article formulas, zero MathJax errors, all 74 figures, all 54 playback controls, the PDE and Monte Carlo workflows, and absence of raw TeX and duplicate runtime IDs.
- `python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium` reproduced the failing observer geometry and checked the fixed inline and display roots. It exercised keyboard and repeated disclosure, simultaneous proofs, proof search, deep links, copy, progressive rendering in all 20 chapter and appendix sections, and opening and restoration for print.
- The [readability audit](MATHEMATICAL_READABILITY_AUDIT.md) contains the V5.3 comparison and the mathematical preservation report. The browser engine was desktop Chromium on Linux. The environment blocked WebKit installation, and no physical iOS device was available.

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
