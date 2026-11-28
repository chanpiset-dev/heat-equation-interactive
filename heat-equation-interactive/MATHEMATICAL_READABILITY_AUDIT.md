# V5.4 mathematical readability and rendering audit

The comparison baseline is V5.3 on main at `14d8299`. The review covered all chapter and appendix fragments, the reference material, the static build and the GitHub Pages workflow.

## Why Grönwall's inline math stayed raw

A Chromium run at 390 CSS pixels reproduced the reported failure before the fix. The definition-list item first touched the 350 px preload margin at an intersection height of zero. IntersectionObserver reported it as intersecting. The scheduler rejected the notification because the height was zero. With only threshold 0, moving the root farther into view produced no second notification. The nested display equation was a separate observed root and rendered independently. The reproduced state contained one rendered display and zero rendered inline expressions.

V5.4 asks the observer for both edge contact and a positive-area notification. On the same approach the root receives the second notification and renders both sets of expressions. The regression test holds the root at the edge, moves it into view, and checks the inline and nested display roots separately. The delimiters, display environment and MathJax configuration needed no change.

The queue processes up to eight visible roots per animation frame. When an observed parent is processed, still-registered descendant roots are temporarily excluded from its MathJax scan. This preserves each root's work and keeps closed proof bodies deferred. A completed root is unobserved. Reopened disclosures reuse the rendered DOM. Search results discard their MathJax items and observations when replaced or cleared. Synchronous batches from the bundled TeX/SVG renderer serialize with the print and search handlers. Print opens mathematical proof disclosures and their containing sections, renders the article, and restores the previous disclosure states afterward.

## Appendix review

| Appendix | Revision |
| --- | --- |
| A. Integration | Separated monotone, Fatou and dominated convergence into visible statements and individual proofs. Kept Hölder's short hypotheses together in prose. Split Young, Minkowski, uniform integrability, Dini and Arzelà–Ascoli into statements and proofs. Displayed the differential Grönwall integrating factor, and gave the integral and discrete forms their own hypotheses and proofs. |
| B. Functional analysis | Made the trace and contraction arguments separately expandable. Classified the existing chain-rule, Galerkin and Sobolev derivations as proofs or derivations. The accompanying estimates and form hypotheses stay visible. |
| C. Fourier analysis | Kept the unitary transform conventions and pointed inversion to its Gaussian regularization argument. Identified the strict beta log-convexity argument as a proof. |
| D. Spectral theory | Separated the closed-form representation from its Riesz-resolvent proof, and linked the Robin application to the precise trace inequality. |
| E. Probability | Put the Itô isometry and its centeredness in the statement. The proof now explains why conditioning cancels cross terms and gives the diagonal covariance. The sampling formulas and prescribed-path distinction are preserved. |
| F. Numerics | Put the edge identity before its derivation. Explained the bottom-node half-weight and ghost-point contribution to the Robin term, with the applications to mass and energy outside the derivation. |

## Chapter review

| Chapter | Revision |
| --- | --- |
| 0. Introduction | Tightened the link between the governing problem and the definition of an integral solution. |
| 1. Heat equation | Typeset the dimension condition in the Gaussian discussion. Preserved intuitive figure explanations and controls. |
| 2. Formulation | Separated the Fourier and kernel-identity derivations and the Neumann contraction proof. Typeset the radius in the comparison argument. |
| 3. Main theorems | Put the compact-data hypotheses of Theorem 3.1 into one sentence. Retained the separate longer conditions of the weighted theorem. |
| 4. Energy-critical coupling | Linked the motion condition where the energy estimate explains its independence from that condition. |
| 5. Parabolic scaling | Replaced the vague last implication in the regularity hierarchy with its Hölder justification. |
| 6. Sharp Kato inequality | Separated the Gaussian-mixture proof and clarified the characteristic lower bound in the proof roadmap. |
| 7. Global existence | Typeset the trace and representative variables and the space-time pair. Kept the main approximation, energy, local estimate, and limiting strategy visible. |
| 8. Nonexistence | Separated the scaling calculation, kept the proof strategy visible, and typeset the parameter in the comparison caption. |
| 9. Weighted solvability | Separated the characteristic-root proof and typeset the variables in the free-term and continuity arguments. |
| 10. Probabilistic interpretation | Standardized the signs, time comparisons and boundary-series operator in the reflected-path proofs. Retained the distinction between bounded regularized and singular interpretations. |
| 11. Numerics | Moved weighted stability, both conditional convergence statements, and the exact budgets out of collapsed sections. Their technical arguments have their own disclosures. The hypotheses and qualifications about a fixed box, regularization and compatibility remain visible. |
| 12. Further consequences | Linked the local power-integrability criterion to the explicit polar endpoint test. |
| 13. Extended theory | Linked the energy uniqueness argument to the Hilbert-triple chain rule and typeset remaining parameters in the conditional transfer and trajectory comparisons. Preserved open questions and conditional results as such. |

## Mathematical preservation

Source comparison preserved all 1,117 original IDs in order, all numbered equation tags, and the attributes of every figure and control. Six new anchors name prerequisites or a proof equation. The two changed Appendix A link instances now point to the precise subsections. Chapter TeX is preserved except for the equivalent wording “nonnegative and nonzero” in Theorem 3.1 and the regrouping of two previously split variable pairs. Appendix proofs were checked against their original reasoning. Bibliography and public manuscript links, solver code, datasets, reproduction tools and deployment configuration match the baseline.

The discrete Grönwall statement explicitly includes nonnegativity of the initial value. That assumption is used when replacing the geometric factor on the initial value by its exponential bound, and was already intended by the nonnegative sequence in the earlier exposition. No research theorem or numerical conclusion was changed. This was an exposition review, rather than an independent re-proof of the research results.

## Verification and performance

Chromium exercised progressive rendering in each of the 20 chapter and appendix sections, the full article render, several simultaneously expanded proofs, keyboard reopening, direct and search navigation into a proof, TeX copying, and print disclosure restoration. The complete rendering produced 4,381 article MathJax containers with zero error elements and no leftover TeX in mathematical prose. See [VERIFICATION.md](VERIFICATION.md) for commands and browser coverage.

| Metric | V5.3 | V5.4 |
| --- | ---: | ---: |
| Load event | 1188 ms | 822 ms |
| First contentful paint | 560 ms | 488 ms |
| Initial math expressions | 10 | 10 |
| Initial DOM elements | 7,968 | 8,060 |
| Initial JS heap | 8.82 MiB | 8.84 MiB |
| Initial long tasks (≥50 ms) | 5 | 4 |
| Longest initial task | 168 ms | 115 ms |
| Initial canvas backing stores | 0.00 MiB | 0.00 MiB |
| DOM elements after repeated navigation | 9,304 | 9,396 |
| Math expressions after repeated navigation | 29 | 29 |
| JS heap after repeated navigation | 9.74 MiB | 9.77 MiB |
| Long tasks through repeated navigation | 5 | 4 |
| Gaussian figure initialization after approaching it | 59 ms | 71 ms |
| Proof opening to first rendered expression (median) | 108 ms | 74 ms |

The startup and navigation measurements use fresh Chromium contexts with local HTTP, a 390 × 844 CSS-pixel viewport and DPR 3. The first snapshot is taken two seconds after load. The navigation snapshot follows three passes through Chapters 6, 10, 13 and 0 with the same dwell time. Estimated canvas bytes count four bytes per pixel. The heap snapshot is Chromium JavaScript heap after garbage collection. These figures exclude GPU and browser-native allocations and do not measure physical-device memory or scroll frame rates. Proof timing is the median of three openings of the same Chapter 10 technical proof, measured from opening to the first rendered expression. Single-run page timings and these short samples do not establish a general speed improvement.

The default 61-frame PDE checksum and seeded Monte Carlo estimate match V5.3. The audit's screenshots include the original Grönwall failure, the corrected statement, convergence, Hölder, a research theorem, an expanded technical proof, a scientific figure, and the mobile drawer. Playwright WebKit downloads returned HTTP 403. Mobile-width Chromium testing does not establish physical iPhone behavior.
