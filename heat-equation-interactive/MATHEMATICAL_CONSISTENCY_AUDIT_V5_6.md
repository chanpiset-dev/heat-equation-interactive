# V5.6 mathematical consistency audit

## Baseline

The baseline was V5.5 on `main` at `118dc19`, incorporating `a23fba2`. Its static build verified 1,125 IDs, 575 links and 52 local assets. The prior verification recorded 4,497 rendered expressions, 74 figures and 54 playback controls. This work uses the canonical modular sources and the regenerated Pages artifact.

## Chapter and appendix review

Severity refers to the issue encountered in the exposition. “Retained” means the section required no source change after review. The conclusions column distinguishes explanatory scope from research claims.

| Location and purpose | Severity | Review and action | Conclusions |
| --- | --- | --- | --- |
| 0 · Formulation and scaling, `intro-problem41`, `intro-scaling41` | None | Retained the nonsingular boundary domain and the separate bulk and normal derivative scalings. | Retained |
| 1 · Physical interpretation, `diffusion`, `boundary` | None | Retained the local diffusion examples and outward-normal sign conventions. The examples distinguish instantaneous changes from solutions. | Retained |
| 2 · Kernel, integral solution and order, `eq-neumann`, `def-solution`, `thm-series40` | None | Retained the distinction between the value on the nonsingular closed cylinder, interior integral equality, and conditional minimality by positive iteration. | Retained |
| 3 · Threshold and hypotheses, `ass-motion`, `thm31`–`thm34` | None | Retained the dimension-dependent normalization, the uniform short-increment condition and the separate compact and weighted data regimes. | Retained |
| 4 · Energy and sharp boundary form, `eq-energy-identity`, `eq-coercive` | None | Retained the sign of the Robin term and the loss of the positive gradient factor at equality. | Retained |
| 5 · Displacements and comparison, `prop-regularity`, `eq-kernel-comparison` | None | Retained both directions of Gaussian comparison and their different tolerance ranges. The half-Hölder bound remains distinct from a vanishing small-scale modulus. | Retained |
| 6 · Sharpness and profile, `ch6-sharp`, `eq-ground6` | Medium | The inner-cutoff estimate now shows the gradient and weighted trace errors separately. Cross-checked the Fourier normalization and Gamma/Beta cutoff exponents; clarified that the admissible weight lies strictly above the smaller root. | Retained |
| 7 · Integrability and minimality, `eq-final7`, `ch7-limit` | Medium | The local flux argument now divides by the strictly positive minimum of the kernel on a compact source set separated in time. Retained the approximation, continuity, and strong initial trace arguments and the critical/subcritical distinction. | Retained |
| 8 · Spectral amplification, `ch8-spectral`, (8.6)–(8.8) | Medium | Specified a trace tolerance and a lower-bound shift. Retained the form-domain Jensen argument and the order of the concentration and bounded regularization parameters. | Retained |
| 9 · Weighted solvability, `eq-window9`, `eq-majorant9`, `ch9-uniqueness` | Medium | Linked the jointly measurable kernel to the parameter-integral argument. Identified the radial power in the old-time majorant. Retained continuation and uniqueness in the weighted class. | Retained |
| 10 · Reflected process, `eq-skor10`, `eq-ito10`, `lemma-occupation10` | High | Linked the finite-variation regulator to the bracket calculation in E.2, and wrote the Doob/isometry error estimate for occupation. Retained backward physical time in the Feynman–Kac argument and the scope of its singular-limit statements. | Retained |
| 11 · Numerical stability, `result-11-2` | Medium | Justified the previously compressed hyperbolic-cosine bound for the discrete barrier. Retained the ghost orientation, fixed-box regularity hypotheses, energy identities and reproducibility data. | Retained |
| 12 · Consequences, `prop-time12`, `prop-localepisode12`, `prop-ground12` | None | Retained hypotheses for time-dependent coupling, local sufficient nonexistence conditions and stationary ground-state transformation. | Retained |
| 13 · Conditional and open results, `q-critical13`, `q-lower13`, `q-unique13` | None | Retained the difference between established stationary bounds, possible lower-profile mechanisms, and unresolved moving or critical questions. | Retained |
| A · Convergence and Gaussian estimates, `app-measure40`, `app-gaussian40` | None | Retained Tonelli/Fubini, the separate convergence prerequisites and the Gaussian tail estimate. B.9 supplies the more general parameter measurability used without a measure on the parameter space. | Retained |
| B.9 · Contraction and measurability, `app-contraction9` | High | Separated the contraction theorem, affine fixed point and parameter-integral measurability. Wrote the finite tail, the finite-measure Dynkin-system proof, and the monotone exhaustion. Repaired malformed math in the previous paragraph and split the three proofs. | Retained |
| C · Fourier normalization, `app-fourier-transform`, `app-gamma` | None | Retained the unitary normalization, density extension and the Gamma/Beta calculations. | Retained |
| D · Functional calculus, `app-spectral-heat` | Medium | Wrote the actual finite-measure spectral dominator for strong continuity; retained the distinction between form and operator domains. | Retained |
| E.2–E.4 · Probability foundations and numerics | High | Separated results and arguments, with the normalization and assumptions detailed below. | Retained |
| F · Numerical consistency and rates, `app-numerical` | None | Retained grid weights, distinctions between consistency and stability, and interpretation of empirical rates. | Retained |
| References · Catalogue, notation and bibliography | Low | Added notation cross-references to E.2 and E.4. Retained catalogue distinctions, manuscript links and bibliography. | Retained |

## Appendix E verification

- **Simple Itô isometry.** The coefficients belong to the square-integrable past of each deterministic step. Conditional centering gives zero cross terms, and conditional covariance is the step length times the identity. The proof covers arbitrary truncation by refining the deterministic grid. The displayed isometry and martingale conclusions are outside the proof.
- **Completion and localization.** The predictable space uses product-measure equivalence. Density is cited to reference [8]. The norm identity makes approximating integrals Cauchy in the complete target and proves independence of the approximation. Conditional expectation contracts square mean, preserving the martingale property. Localized integrals use hitting times of the accumulated squared norm, a continuous adapted process on the locally square-integrable event. The stopped-integral identity ensures agreement and the stopping times diverge almost surely. Fixed-time eventual agreement under localization does not require global square-integrability.
- **Quadratic variation and Itô.** Off-diagonal products have variance equal to squared step length. The Gaussian fourth moment gives twice that variance on the diagonal. Independence across disjoint deterministic steps gives the existing fixed-time square-mean bound. Finite-variation square sums vanish pathwise and mixed sums in probability, with no stronger convergence inferred. For the reflected process the bracket is twice the standard Brownian bracket, hence the Laplacian has coefficient one. The normal regulator term remains the normalization of (10.2) and (10.4).
- **Reflection and regulator.** Reflect at the first hit using strong Markov and symmetry. The reflected endpoint has unit absolute Jacobian and density with normalization `(4πt)^(-1/2)`. The formula allows a nonzero starting height and is valid for endpoints above the barrier. The half-normal maximum law gives the regulator's one-time law, with a positive part for the initial height. Completing the square gives its uniform exponential moment bound. The two-sided maximum is treated separately by a union bound.
- **Bridge minimum and inverse.** The crossing-to-unrestricted density ratio cancels the normalized Gaussian factors; the difference of their squares is four times the product of the two distances to the barrier. The conditional CDF is increasing below the smaller endpoint. The smaller quadratic root is the unique admissible root for an interior uniform draw. Given all driver endpoints, bridge interiors are conditionally independent. Taking successive minima and applying (10.2) is exact jointly on the ideal grid. This gives neither the contact times nor the tangential path between grid points.
- **Stieltjes quadrature.** With bounded continuous coefficient on the plane at fixed regularization and bounded measurable terminal data, the pathwise modulus times `L_T` controls right-endpoint error. The exponential bound with coefficient norm times `L_T` actually dominates the weighted integrands. This gives convergence of expectations on a common path. Joint grid exactness does not imply exact finite-mesh quadrature or justify a singular-limit representation.
- **Monte Carlo.** The fixed-mesh mean uses independent ideal draws with finite second moment. The variance of the mean, unbiased sample variance and estimated standard error are distinct. The coarse minimum is the minimum across compatible fine intervals; coupling preserves the within-pair covariance. Paired differences compare two meshes, while standard error, continuum bias and floating-point error describe different quantities. Numerical checks sampled the density ratio, inverse CDF, and half-normal moment formula.

## Rendering, navigation and preservation

The B.6–B.9 entries were present in source navigation and added a second time at runtime. B.1–B.9 are now in the same canonical source list and the runtime insertion is removed. A link to a disclosure's own anchor now opens that disclosure as well as any containing disclosures. The navigation appearance, MathJax scheduler, figure deferral, worker, solver, datasets, numerical implementations and deployment workflow were retained.

Source comparison preserved every original ID in order, numbered equation tags, original scientific control attributes, catalogue entries and public manuscript URLs. Two internal link instances were replaced with more specific anchors in B.9 and E.3. Mathematical delimiters checked out. The local corrections concern the B.9 malformed TeX, strict interior weight choice, and explicit constants and domination. They do not change a published research result. The unchanged research proofs were reviewed for consistency as part of this edit; no independent re-proof of all results is claimed.

## Verification evidence

| Check | Outcome |
| --- | --- |
| Static build | PASS. 1,147 unique IDs, 598 links and 52 local assets. |
| Chromium HTTP smoke | PASS. Repo-prefixed URLs at 320, 375, 390, 430, 768, 1024 and 1440 px. 4,645 expressions, zero MathJax errors or leftover mathematical TeX, 74 figures, 54 playback controls. |
| Readability and navigation | PASS. Progressively reached each of the 20 chapter and appendix sections, opened all 14 new proofs independently, confirmed exactly nine Appendix B subsection links, and tested search, proof links, keyboard, copy and print restoration. |
| Numerical regression | PASS. All 61 default PDE frames yielded the same checksum. The seeded Monte Carlo readout matched at 1.3858 ± 0.0401 (one sample standard error). |
| WebKit installation | FAIL. Playwright browser archive downloads returned HTTP 403. |
| WebKit browser, physical Safari, and Slack in-app execution | NOT RUN. No WebKit browser binary or physical device was available. |

The commands run were:

```sh
python3 build.py
python3 build.py --check
python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium
python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium
python3 -B tools/mobile_benchmark.py PATH_TO_DOCS
```

### Performance comparison

The same local HTTP benchmark ran in fresh Linux Chromium contexts before and after the change at 390 × 844 CSS pixels and DPR 3. Navigation repeated the same chapter sequence. Heap measures JavaScript storage after garbage collection; it excludes native and GPU memory. Canvas storage is estimated at four bytes per pixel. The proof figure is the median of three cold-page openings of the existing Brownian quadratic-variation proof, measured from opening to the first rendered expression. Single-run load figures and three proof samples describe this test only.

| Metric | V5.5 | V5.6 |
| --- | ---: | ---: |
| Load event | 1223 ms | 935 ms |
| First contentful paint | 676 ms | 516 ms |
| Initial expressions | 10 | 10 |
| Initial DOM elements | 8,172 | 8,287 |
| Initial JS heap | 8.85 MiB | 8.86 MiB |
| Initial long tasks | 4 | 4 |
| Longest initial task | 183 ms | 147 ms |
| Initial canvas backing stores | 0.00 MiB | 0.00 MiB |
| Initial active workers | 0 | 0 |
| DOM elements after repeated navigation | 9,459 | 9,574 |
| JS heap after repeated navigation | 9.67 MiB | 9.68 MiB |
| Long tasks through repeated navigation | 6 | 4 |
| First figure after scroll | 63 ms | 64 ms |
| Proof opening to first expression, median | 69 ms | 61 ms |

## Physical-mobile acceptance

**PHYSICAL IOS SAFARI: NOT TESTED**

No physical iPhone or Slack in-app browser was available. The remaining physical acceptance gate covers cold load, contents and direct E.2–E.4 navigation, proof reopening, rapid scrolling and toolbar changes, rotation, local formula overflow, search, back/forward and copy, an existing animation, and visiting Chapter 11 before revisiting earlier math. Device model, iOS/Safari version and any reloads, freezes or blank figures remain unrecorded. The Linux Chromium viewport runs cannot establish physical stability. Playwright WebKit availability is listed separately in verification.

## Remaining mathematical limitations

The critical lower profile, full classification for rough supercritical trajectories, and unrestricted uniqueness remain open in the article. The bounded coefficient expectation limit is mesh convergence at fixed regularization. It gives no uniform estimate as regularization vanishes. All physical-device outcomes are pending.
