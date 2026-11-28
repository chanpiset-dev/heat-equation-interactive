# Heat Equation with a Dynamical Singular Potential on the Boundary

Interactive mathematical exposition — V5.6 Mathematical Consistency and Rigor Edition. The site retains the accepted editorial design, fourteen chapters, six appendices, theorem catalogue, bibliography, and scientific experiments.

## Preview locally

Requires Python 3.9+; no Node.js, npm, framework, CDN or build dependencies are required.

```sh
python3 build.py
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000> in a browser. The server only serves static files. Stop it with Ctrl+C. Serving the site over HTTP is recommended rather than double-clicking the HTML, because browser policies for local files and workers vary.

## Project structure

```text
.
├── src/                         # Editable article source
│   ├── template.html            # Page shell and ordered asset references
│   ├── navigation.html          # Table of contents source
│   ├── manifest.json            # Article fragment order
│   ├── content/
│   │   ├── front-matter/hero.html
│   │   ├── chapters/            # 00–13: one HTML fragment per chapter
│   │   ├── appendices/          # A–F
│   │   └── reference/           # Theorem catalogue, notation, bibliography
│   └── workers/pde-worker.js    # Editable PDE worker
├── docs/                        # GitHub Pages publishing directory
│   ├── index.html               # GENERATED article; do not edit directly
│   ├── .nojekyll
│   └── assets/
│       ├── css/                 # Editable ordered stylesheets
│       ├── js/                  # Editable shared and chapter scripts
│       │   └── generated/       # GENERATED worker wrapper; do not edit
│       ├── data/chapter-11/     # Editable precomputed datasets, by experiment
│       └── vendor/mathjax/      # Original local MathJax + license
├── reproduction/                # Chapter 11 Python experiments and instructions
├── tools/                       # Dataset export and optional browser checks
├── .github/workflows/check.yml   # CI build/anchor check
├── build.py                     # Standard-library static-site assembly
└── REFACTOR_BRIEF.md
```

The `src/content/` files are **HTML fragments**, not independent browser pages. The generated index assembles them at build time. This is intentional: the original global navigation, cross-references, math renderer, and shared figure functions depend on the full document and original script order. Each chapter is now independently editable without duplicating navigation or changing the reader experience. There is no runtime fetching of article fragments. A future multi-page redesign is possible, but requires isolating figure initialization and remapping links; it is not part of this preservation refactor.

## Mathematical exposition

The six appendices distinguish hypotheses, conclusions and derivations. Mathematical prose, captions and reference labels use the site’s MathJax conventions. See the [mathematical exposition audit](MATHEMATICAL_EXPOSITION_AUDIT.md) for examples, chapter-by-chapter changes and verification.

The [V5.4 readability audit](MATHEMATICAL_READABILITY_AUDIT.md) documents the Grönwall rendering fix, the proof disclosures, and the chapter-by-chapter review.

The [V5.5 formalization audit](MATHEMATICAL_FORMALIZATION_AUDIT.md) covers the revised probability reference, chapter-by-chapter changes, and regression evidence.

The [V5.6 consistency audit](MATHEMATICAL_CONSISTENCY_AUDIT_V5_6.md) covers Appendix E, the B.9 proof separation, and the remaining physical-mobile acceptance gate.

## Mobile rendering

MathJax typesets approaching article content in batches. Figure controls retain their state when off-screen canvases are released. The PDE starts near its figure, and the contents drawer uses a separate navigation landmark from the previous/next chapter links.

See [the mobile performance audit](MOBILE_PERFORMANCE_AUDIT.md) for Chromium benchmarks, the architecture comparison and physical-iPhone acceptance checks.

## Common maintenance tasks

| Task | Edit |
|---|---|
| Edit Chapter 7 text or equations | `src/content/chapters/07-global-existence.html` |
| Edit Appendix E | `src/content/appendices/e-probability.html` |
| Edit bibliography | `src/content/reference/bibliography.html` (also check all in-text references and `assets/js/editorial.js` citation rules if numbering changes) |
| Edit article order | `src/manifest.json` and `src/navigation.html` |
| Edit theme | `docs/assets/css/editorial.css` and `base.css` |
| Edit Chapter 9 figures | `docs/assets/js/chapter-09.js` |
| Edit Chapter 1 or shared plot functions | `docs/assets/js/foundations-and-shared.js` |
| Edit PDE solver | `src/workers/pde-worker.js` |
| Edit Chapter 11 scientific results | `docs/assets/data/chapter-11/` (regenerate with the Python reproduction workflow when appropriate) |
| Change site-wide navigation or accessibility behavior | `docs/assets/js/editorial.js` |

After changing content, navigation, template or worker source, run `python3 build.py`. Commit both the editable files and generated `docs/index.html`/worker wrapper. Styles, scripts and data under `docs/assets/` are maintained directly; they are already served by Pages and don't require a copying step. The CSS and classic scripts are loaded in the order listed in `src/template.html`; preserve this order unless dependencies are deliberately refactored. The `data/chapter-11/` registration scripts populate `window.chapter11Data` before Chapter 11 starts. Do not replace them with asynchronous fetches without coordinating initialization. The two large field datasets and MathJax are intentionally separate from authoring files.

Use stable element IDs for equations, theorems, figure controls, and headings. Mathematical cross-references rely on these IDs. Run:

```sh
python3 build.py --check
```

This verifies that generated files match their source and that internal links, IDs, stylesheet and script paths are valid. The GitHub Actions check uses the same command.

## Publish on GitHub Pages

1. Create a GitHub repository (for example, `heat-equation-exposition`).
2. Extract this ZIP, then put the **contents of the `heat-equation-github` folder** in the repository root. Keep the `.github` and `docs/.nojekyll` files.
3. Commit and push the files to your default branch, normally `main`.
4. In the repository, open **Settings → Pages**. Under Build and deployment, choose **Deploy from a branch**, select `main` and `/docs`, and save.
5. Open the URL GitHub reports when the deployment succeeds. For a project repository it is typically `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`.

All published asset paths are relative, so a repository subpath works without editing the site. The ZIP includes the already generated site: initial deployment does not require a separate build server. The check workflow validates later commits; it does not publish independently. GitHub Pages may make your site publicly accessible, so confirm your repository's visibility and permission to publish your material before enabling it.

### Typical Git workflow

```sh
# After editing an article or worker:
python3 build.py
python3 build.py --check
git add src docs
git commit -m "Refine Chapter 7 exposition"
git push
```

## Scientific data and reproducibility

`reproduction/` includes the original Chapter 11 reproduction code and Python requirements. See its README. The site uses the same numerical values as V5.1. To export the split JavaScript data as a conventional JSON file, run:

```sh
python3 tools/export_data.py numerical_investigations_v3_3.json
```

The browser's existing JSON and Python download buttons remain functional. Keep numerical experiments separate from mathematical claims about the singular limit.

## Optional browser regression

Install Playwright in your local Python environment and its Chromium browser:

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
python3 tools/browser_smoke.py
# Use a system Chromium or select an installed Playwright engine.
python3 tools/browser_smoke.py --chromium /usr/bin/chromium
python3 tools/math_readability_smoke.py --chromium /usr/bin/chromium
python3 tools/browser_smoke.py --browser webkit
```

The smoke test uses a temporary local HTTP server at a repository-like subpath. It checks rendering, data, animation controls, navigation, mobile widths and the PDE worker. Use `--embedded-assets` only when the browser environment blocks HTTP navigation; this loads the same files through data URLs and does not verify an actual deployment. See `VERIFICATION.md` for the checks run during the refactor.

## Licensing

The original article and scientific code have no new project-wide license assigned by this refactor. Choose a license yourself before inviting reuse. The original MathJax dependency retains its Apache-2.0 license under `docs/assets/vendor/mathjax/`. The revised research paper and thesis are linked to their existing public URLs, not copied into the repository.
