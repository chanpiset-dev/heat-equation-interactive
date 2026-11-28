# V5.3 mathematical exposition audit

The baseline was V5.2 on `main` at `8c4e7de`. The review covered the 14 chapter fragments, six appendices, notation glossary, theorem catalogue, generated article and MathJax startup. It distinguished editable mathematical prose from canvas drawing labels, SVG diagram text, native options and generated numerical readouts.

## Notation and presentation

| V5.2 example | V5.3 treatment |
| --- | --- |
| `For conjugate p,q>1, convexity gives …` | State the conjugacy equation and Young bound separately. Apply concavity of the logarithm to the two positive powers, then handle the zero cases. |
| `Normalize the Lᵖ and Lᑫ norms and integrate to obtain Hölder.` | List the two Lebesgue-space assumptions, define the normalized functions and show the bound from the integrated Young inequality. |
| `the corresponding geometric-sum bound` | Display the discrete Grönwall sum with the factor $(1+C\Delta t)^{n-1-j}$ and its exponential majorant. |
| `Compactness makes one set cover K` | In Dini's proof, extract a finite subcover of the increasing open sets and take the largest index. |
| `L² contraction of the Neumann semigroup` | Use `\(L^2\)` in the heading and catalogue, and progressively render the corresponding contents and search labels. |
| `Δt = 0.07ℓ² and T = 0.28` | Use `\(\Delta t=0.07\ell^2\)` and `\(T=0.28\)` in the caption. The experiment parameters are the same. |

Publication prose and mathematical captions use the existing inline and display delimiters. Browser-native widgets and graphics use short semantic labels or compatible mathematical glyphs. Citation linkification preserves bracketed expressions in TeX. The existing equation-copy buttons still copy the source captured before typesetting.

## Appendices

| Appendix | Revision |
| --- | --- |
| A. Integration | Stated the product-measure assumptions and interchange identities. Separated monotone, Fatou, dominated and uniformly integrable limits. Displayed the Gaussian tail, the $L^2$ approximate-identity bounds and both recent-time estimates. Stated the polar endpoint conditions, proved the norm inequalities, and supplied the finite-subcover and finite-net arguments. |
| B. Functional analysis | Separated weak derivatives and first Sobolev spaces. Expanded the half-space trace calculation and distinguished weak and weak-* tests. Listed nonautonomous form hypotheses, retained the Hilbert-triple and nonlinear-testing proofs, displayed the Sobolev and parabolic gains, and supplied an explicit contraction iteration error. |
| C. Fourier analysis | Displayed the forward and inverse unitary conventions with the two multiplier identities. Retained the Schwartz and tempered-distribution settings and distinguished distribution multiplication from the density calculation in the harmonic-profile proof. Expanded the Gamma–Beta substitution and Jacobian. |
| D. Spectral theory | Displayed the spectral multiplier domain and norm, separated the shifted closed-form assumptions, and clarified the ambient, form and operator domains. Retained the spectral and semigroup estimates and the counterexample to inferring positivity from self-adjointness. |
| E. Probability | Separated the filtration, stopping time and conditional expectation definitions. Displayed the stochastic integral for a simple predictable integrand and its covariance argument. Stated the Brownian-bridge endpoint and variance convention and distinguished grid-time sampling, Stieltjes bias and Monte Carlo error. |
| F. Numerics | Displayed the weighted edge identity and Robin term. Separated consistency, stability and assumptions for estimating a mesh rate, with a distinction between rate estimates and certified error bounds. Linked the finite-box propositions and reproduction workflow. |

## Chapters

| Chapter | Revision |
| --- | --- |
| 0. Introduction | Linked the governing problem directly to the integral-solution definition and clarified why no Robin value is assigned on the graph. |
| 1. Heat equation and boundary interaction | Typeset Gaussian and PDE parameters, temperature, flux and norm descriptions. Kept native controls readable. |
| 2. Mathematical formulation | Typeset half-line variables, kernel and iteration labels, and the semigroup contraction result. |
| 3. Main theorems | Listed the compact-data and weighted hypotheses of Theorems 3.1 and 3.4 and linked the trajectory condition. |
| 4. Energy-critical coupling | Standardized the squared norm, coupling, trajectory coordinate and form-margin notation. |
| 5. Parabolic scaling | Identified the mixed term in the shifted square and showed how adjustable Young gives each side of the Gaussian comparison. |
| 6. Sharp Kato inequality | Standardized the critical constant, mode, profile, logarithm and spherical normalization in proof summaries and figures. |
| 7. Global existence | Standardized approximation indices, energy spaces, cutoff and Moser parameters, and recent-time captions. |
| 8. Supercritical nonexistence | Standardized the concentration scale, spectral weights, time slices and effective-coupling parameters, separating them from numerical readouts. |
| 9. Weighted solvability | Linked the free-term estimate to the harmonic heat identity and typeset weights, contraction parameters, traces and endpoint limits. |
| 10. Probabilistic interpretation | Typeset the reflected-path proof, stopping and inverse-clock variables, quadrature settings and limits. Clarified the backward physical clock and zero-terminal-value event. |
| 11. Numerical investigations | Standardized mesh, diagnostic and reference-grid mathematics while retaining the experimental tables and controls. |
| 12. Further consequences | Standardized half-Hölder, time-dependent coupling and transformed diffusion notation in statements and figures. |
| 13. Extended theory | Standardized profile, stability, localization and multi-pole proof variables and display controls. |

## Mathematical preservation

A source comparison against V5.2 checked all 1,117 IDs in order, containment of all original links, exact figure and control attributes, and exact equation tags. Every original TeX expression in Chapters 0–13, the glossary and catalogue remains, ignoring whitespace and allowing movement between inline and display markup. Appendix formulas were compared by result where a derivation or statement was rewritten. The checks leave all source references, manuscript links, datasets, solver and reproduction code intact.

Clarifications during the mathematical review include the nonempty space in the contraction theorem, positive shift in the recent-time Gaussian estimate, and pathwise continuity of the coefficient in the Stieltjes truncation argument. The empirical-rate limit is conditional on an asymptotic power law and control of time error. The weighted discrete identity uses the same half-weight bottom nodes and zero Dirichlet extension as Proposition 11.4. These are prerequisite and interpretation clarifications. No main theorem, threshold, numerical algorithm or scientific conclusion was changed. This review is an exposition regression, with no independent re-proof of every research theorem.

## Rendering and performance

The V5.2 bounded queue, lazy canvas allocation, DPR limits, worker lifecycle and animation suspension remain in place. The queue now handles mathematical contents labels as well. The full render check exercises the existing print path. For normal browsing, the first viewport and nearby content render progressively.

| Metric | V5.2 | V5.3 |
| --- | ---: | ---: |
| Load event | 1129 ms | 1071 ms |
| First contentful paint | 684 ms | 656 ms |
| Initially rendered formulas | 10 | 10 |
| Initial DOM elements | 7,829 | 7,968 |
| Initially allocated canvases | 0 | 0 |
| Estimated initial RGBA backing stores | 0.00 MiB | 0.00 MiB |
| Initial JavaScript heap | 8.78 MiB | 8.83 MiB |
| Initial long tasks at least 50 ms | 4 | 4 |
| Longest initial task | 132 ms | 134 ms |
| Formulas after repeated navigation | 28 | 29 |
| DOM elements after repeated navigation | 9,154 | 9,304 |
| JavaScript heap after repeated navigation | 9.69 MiB | 9.75 MiB |
| Canvas stores after repeated navigation | 0.000004 MiB | 0.000004 MiB |
| Long tasks through repeated navigation | 4 | 4 |

The benchmark uses the same Linux Chromium, local HTTP, fresh contexts, a 390 × 844 CSS-pixel viewport and DPR 3. Initial samples are taken two seconds after load; the repeat visits Chapters 6, 10, 13 and 0 three times with identical dwell times. Each number represents one run. The backing-store estimate assumes four RGBA bytes per pixel; heap is sampled after CDP garbage collection and excludes browser-native and GPU memory. Device process memory and full-monograph retention were not measured.

The 61-frame default PDE checksum is `a771d661b0ee3005fcc69748de354d157fb6cc7f35a3b689d1e679550da292a5` on both versions. Both versions also give the seeded Monte Carlo estimate $1.3858\pm0.0401$ at the default observation point (one sample standard error). See [verification](VERIFICATION.md) for browser coverage. The environment denied the desktop WebKit download. The mobile checks use a narrow Chromium viewport, and physical iOS Safari was unavailable.
