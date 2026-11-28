# Appendix B.9 refinement audit

Baseline is V5.6 on `main` at `cd37fb7d1e87c227e774040edfa8aac24e6446ad`.

## Organization

| Location | V5.6 | Revised exposition |
| --- | --- | --- |
| Appendix A.1 | Tonelli, Fubini, and limiting operations | Introduces parameter-integral measurability and its proof before Tonelli and Fubini. Links to the moving integrals and the use of Tonelli in continuation. |
| Appendix B.9 | Completeness, contraction, the affine series, and parameter integration | Develops completeness, contraction, and the affine fixed point in order. States the affine positivity assumptions with the result. |
| Chapter 9 | Repeats parts of the completeness and fixed-point proofs | Cites the abstract results and derives the heat-kernel bounds, weighted truncation estimate, and initial value. |

## Mathematical review

- **Completeness.** The proof passes the supremum Cauchy bound to the measurable pointwise limit and obtains uniform convergence. Division by the strictly positive Borel weight is an isometric bijection, with multiplication as its inverse. The norm uses the pointwise supremum so the operator can use boundary values.
- **Contraction.** The statement and proof remain as in V5.6. Summing the successive-distance estimates gives the bound for the distance between iterates with indices \(k>j\). The bound gives the Cauchy property and passes to the limit to give the iteration error. The Lipschitz estimate gives the fixed-point identity and uniqueness.
- **Affine construction and positivity.** The geometric norm bound gives absolute convergence and the tail bound. Boundedness permits passage to the limit in the affine recurrence, and the contraction theorem gives uniqueness. Positivity uses nonnegative data and a cone-preserving operator. In the weighted space, the pointwise difference is bounded by the weight times the norm difference, so the nonnegative cone is closed.
- **Parameter integration.** Sections of product-measurable sets are measurable. For a finite measure the Dynkin-system argument uses subtraction of finite section measures. The rectangle argument then extends by the pi–lambda theorem, simple-function approximation, monotone convergence, and sigma-finite exhaustion. This proof precedes Tonelli and Fubini and is independent of both. The signed integral is finite where both parts are finite and undefined where both are infinite.
- **Weighted solvability.** Chapter 9 identifies the product Borel sigma-algebra using countable bases, then applies A.1 to the nonnegative integrands. The bound on the weighted operator ensures absolute integrability for signed candidates. Equations (9.10)–(9.12) still give the moving operator, its norm estimate, and the series and norm bound. The affine result gives local uniqueness in the weighted space, positivity, and the geometric truncation estimate. The sharper harmonic-barrier estimate and continuation argument retain their existing proofs and scope.

## Anchors and references

- `#app-contraction9`, `#app-affine-fixed-point`, `#proof-contraction-b9`, and `#proof-affine-b9` stay in B.9. The short completeness proof has the new anchor `#proof-bounded-completeness`.
- `#app-parameter-measurability` and `#proof-parameter-b9` now resolve in A.1 under their original identifiers.
- Definition 9.1 and the B.9 weighted isometry link to each other’s context. Proposition 9.2 links to the affine result, and the affine proof links back to the weighted Picard construction. The paragraph after (9.10) links to A.1, which links back to (9.10) and the continuation argument at `#eq-history9`.
- Compared with V5.6, all prior IDs, link destinations, equation tags, and figure and control attributes are preserved. Appendix A and B contents lists retain their five and nine section entries, respectively.

## Verification

| Check | Result |
| --- | --- |
| `python3 build.py` and `python3 build.py --check` | PASS. 1,148 unique IDs, 599 internal links, and 52 local CSS and JavaScript references. |
| `python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium` | PASS. Repo-prefixed HTTP at 320, 375, 390, 430, 768, 1024, and 1440 CSS pixels. Rendered 4,671 expressions with zero MathJax errors. Checked 74 figures and 54 playback controls. |
| `python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium` | PASS. At 390 CSS pixels, checked the B.9 fragment, independent disclosures, A and B contents targets, Chapter 9’s link to A.1, the preserved proof fragment, search, equation copying, touch and keyboard input, and print disclosure and restoration. |
| `python3 -B tools/mobile_benchmark.py docs` | PASS for numerical parity. The 61-frame PDE output and seeded Monte Carlo readout matched a build archived from V5.6. |
| WebKit and physical iOS Safari | NOT TESTED. This environment has neither a Playwright WebKit binary nor a physical iOS device. |

The PDE SHA-256 was `a771d661b0ee3005fcc69748de354d157fb6cc7f35a3b689d1e679550da292a5` in both runs. The seeded Monte Carlo estimate was `1.3858 ± 0.0401` (one sample standard error, 192 paths, 200 steps, seed 9131) in both runs.

On a physical iPhone, the remaining checks are to open the original and relocated fragment URLs, follow the Chapter 9 link, tap to open and close the proofs, copy a displayed equation, and inspect the math and disclosures in print preview.
