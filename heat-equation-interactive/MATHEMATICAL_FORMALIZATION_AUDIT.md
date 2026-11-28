# V5.5 mathematical formalization audit

The baseline is V5.4 on `main` at `904d685`. The audit used the modular sources, the V5.4 readability report, and the generated site. Changes focus on passages where an equation, defined object, or intermediate bound makes the reasoning easier to verify.

## Chapter and appendix inventory

| Location | Baseline issue and revision |
| --- | --- |
| [0.4, scaling](src/content/chapters/00-introduction.html#intro-scaling41) | The derivative scaling was compressed into a sentence. The bulk and boundary chain rules now give the derivatives at their rescaled arguments, followed by the stationary power identities. |
| [1.1, diffusion](src/content/chapters/01-heat-equation.html#diffusion) | The local peak and valley calculations now explicitly give the instantaneous derivative. A saddle with negative Laplacian illustrates why directional curvatures must be added. |
| [2.6, integral solutions](src/content/chapters/02-mathematical-formulation.html#solution) | The zero datum now gives the two zero terms in the integral equation and directly explains the nonzero-data hypothesis in Theorem 3.2. |
| [3.1, threshold](src/content/chapters/03-main-theorems.html#ch3-threshold) | The three regimes are displayed together against the sharp threshold. The Gamma integral and recurrence are referenced at their derivation in Appendix C.4. |
| [4.2, sharp inequality](src/content/chapters/04-energy-critical-coupling.html#ch4-kato) | The subcritical control, critical nonnegativity and supercritical negative test are expressed with the form, its coercivity factor and the sharp quotient. |
| [5.1, diffusion length](src/content/chapters/05-parabolic-scaling.html#ch5-diffusion) | A line of integration by parts gives the coordinate variance. The endpoint decay used in the calculation is stated. |
| [6.1, variational question](src/content/chapters/06-sharp-kato-inequality.html#ch6-variational) | The sharpness proof now names the exact lower bound and the requirement on the approximating sequence of test functions, with links to both arguments. |
| [7, global existence](src/content/chapters/07-global-existence.html#ch7) | The critical case identifies the surviving energy bound and the separate compact-set estimate. The weak passage displays the quantities controlled by translated Kato and identifies the actual integrable majorant. |
| [8.2, concentration](src/content/chapters/08-supercritical-nonexistence.html#ch8-scaling) | The scaled regularized boundary integrand is compared with the integrable singular trace density, justifying its limit. |
| [9.1 and 9.4, weight and contraction](src/content/chapters/09-weighted-solvability.html#ch9-contraction) | The weight constants are the extrema on the closed unit hemisphere. A finite geometric sum gives the norm tail and the partial-sum recurrence gives the fixed-point identity. |
| [10.1, Brownian motion](src/content/chapters/10-probabilistic-interpretation.html#ch10-brownian) | The one-time visualization and Brownian path have the same Gaussian marginals. Their two-time covariance formulas explain the difference. |
| [11.2–11.3, finite differences](src/content/chapters/11-numerical-investigations.html#ch11-stencil) | The oriented Robin difference is written before solving for the ghost point. The weighted residual recurrence now gives the full accumulated error bound under the existing assumptions. |
| [12.1 and 12.3, dimension and order](src/content/chapters/12-further-consequences.html#ch12-two) | The boundary polar integral displays the dimension-two logarithmic divergence. Kernel positivity and induction justify the upper comparison of iterates. |
| [13.1 and 13.6, motion and stability](src/content/chapters/13-extended-theory.html#ch13-stability) | The known motion regimes link to their precise theorem hypotheses. For a fixed regularization the resolvent identity and boundary kernel integral derive the stated stability constant. The open problems are preserved. |
| [A.2, approximate identities](src/content/appendices/a-integration.html#app-gaussian40) | The ball/tail argument is an explicit pointwise inequality with the order of limits and the compact-uniform conclusion stated. |
| [B.4, convergence](src/content/appendices/b-functional-analysis.html#app-convergence) | The pairing proving weak lower semicontinuity is written out. Bessel's inequality justifies the orthonormal example. |
| [C.3, convolution](src/content/appendices/c-fourier-analysis.html#app-fourier-convolution) | Tonelli gives the absolute convolution bound and almost-everywhere definition before Fubini is used for the Fourier formula. |
| [D.1, spectral measures](src/content/appendices/d-spectral-theory.html#app-spectral-measure) | Strong countable additivity is stated on each vector for disjoint Borel sets. |
| [E.1–E.4, probability](src/content/appendices/e-probability.html#app-prob-foundations) | Filtration, adaptedness, stopping, conditional expectation and martingales have separate definitions. The stopped expectation limit identifies its domination assumption. E.2 specifies the predictable integrand space, cites density, and proves the extension by an isometry. It gives an independent quadratic variation proof, finite-variation and mixed-increment bounds, and the reflected Itô coefficient. E.4 distinguishes the paired variance from its estimate. |
| [F.1, discrete edge identity](src/content/appendices/f-numerical-analysis.html#app-numerical) | The Robin contribution now shows the ghost term, half-weight and test factor in the grid pairing. |

## Representative before and after

- **“Completion extends the integral by this isometry.”** The revision defines the equivalence classes in the predictable product space and compares two simple approximants by the squared isometry. Completeness then gives a unique integral in square mean, and the same bound establishes independence of the approximating sequence.
- **“Independence makes the variance bounded by a constant times the mesh size.”** With Brownian coordinate indices `i,j`, the proof derives the exact factor `1 + δᵢⱼ` from the Gaussian fourth moment. It bounds the mean-square error by `2t|π|`. The statement remains visible while that proof is closed.
- **“Iteration in the weighted norm gives at most … times the uniform residual bound.”** Chapter 11 identifies the forced discrete error equation, weights each time level by its remaining stability factors, and bounds the sum on the fixed box.
- **“The inner contribution … the outer contribution ….”** Appendix A now displays one inequality for the approximate identity and takes the small-time limit before shrinking the ball.

## Preservation and mathematical review

A source comparison verified the original 1,123 IDs in order, retained hrefs, all numbered equation tags, unchanged figure and control attributes, and balanced mathematical delimiters. No research theorem statement or hypothesis block was replaced. The revised passages were checked directly against their previous arguments. Gamma identities removed from the threshold introduction remain in Appendix C.4. The PDE worker, figure code, datasets, reproduction scripts, bibliography, approved manuscript links, MathJax scheduler, and Pages workflow match the baseline.

One small bound was made explicit in Appendix A.2. The tail factor is now the essential supremum plus the actual value at the evaluation point, so the inequality holds even for a bounded representative whose value at that point exceeds its essential supremum. This leaves the continuity-point and compact-uniform conclusions intact. The dimension-two explanation specifies a trace bounded below by a positive constant when using the divergent kernel integral as a lower bound. Neither clarification changes a research result.

The stochastic integration text invokes predictable density and general Itô calculus and derives the claims specific to this article. Mixed increment convergence is in probability; Brownian quadratic variation along the stated deterministic partitions is in square mean. The correction explains the Laplacian coefficient without asserting a new general stochastic-calculus theorem. This was an exposition review of the rewritten arguments, with no independent re-proof of the unchanged research results.

## Verification and performance

| Test | Result and evidence |
| --- | --- |
| Static build | PASS. 1,125 IDs, 575 links and 52 local assets. |
| Source preservation | PASS. Original anchors, numbered equation tags, link targets and scientific control attributes retained. Mathematical delimiters balanced. |
| Chromium HTTP regression | PASS. Seven widths from 320 to 1440 px under the repository URL prefix. All 4,497 formulas rendered with no MathJax errors or exposed TeX. All 54 playback controls passed. |
| Progressive proof regression | PASS. Brought mathematical content into view in every chapter and appendix. Verified the closed quadratic variation proof, deep link, copy, keyboard reopening and single SVG rendering. The suite also checked search, simultaneous disclosures and print restoration. |
| Numerical regression | PASS. The default 61 PDE snapshots gave the same checksum and the seeded Monte Carlo value matched at 1.3858 ± 0.0401 (one standard error). |
| WebKit installation | FAIL. Playwright download endpoints returned HTTP 403. |
| WebKit and physical iOS Safari | NOT RUN. Tests used desktop Chromium with narrow viewports. |

| Metric | V5.4 | V5.5 |
| --- | ---: | ---: |
| Load event | 1134 ms | 1005 ms |
| First contentful paint | 636 ms | 564 ms |
| Initial formulas | 10 | 10 |
| Initial DOM elements | 8,060 | 8,172 |
| Initial JS heap | 8.83 MiB | 8.85 MiB |
| Initial canvas backing stores | 0.00 MiB | 0.00 MiB |
| Initial long tasks (≥50 ms) | 4 | 4 |
| Longest initial task | 124 ms | 145 ms |
| DOM elements after repeated navigation | 9,396 | 9,459 |
| Formulas after repeated navigation | 29 | 30 |
| JS heap after repeated navigation | 9.76 MiB | 9.66 MiB |
| Long tasks through repeated navigation | 4 | 5 |
| First figure after scroll | 58 ms | 57 ms |

The benchmark uses local HTTP, fresh Linux Chromium contexts and a 390 × 844 CSS-pixel viewport at DPR 3. The initial sample follows the load event by two seconds. The follow-up sample follows three passes through Chapters 6, 10, 13 and 0 with identical dwell times. Reported heap excludes native and GPU allocations. Canvas storage is estimated at four bytes per pixel. Single-run timings are descriptive. WebKit and physical-device performance were not measured.
