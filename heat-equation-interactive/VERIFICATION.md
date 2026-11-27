# Refactor verification

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
