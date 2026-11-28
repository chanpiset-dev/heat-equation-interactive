---
name: mathematical-exposition
description: Audit and edit the heat-equation research exposition for mathematical precision, concise proofs, stable references, and interactive/mobile regressions. Use for theorem, proof, appendix, equation, and mathematical readability changes.
---

# Mathematical exposition and verification skill

## 1. Establish the baseline

Read `AGENTS.md`, the nested project README, `VERIFICATION.md`, and relevant historical audit reports. Record the branch and commit SHA. Locate the exact modular source files first. Use the related research references when accessible; if you cannot verify a source-dependent claim, flag it rather than inventing a proof.

## 2. Classify before rewriting

For each candidate passage, identify its mathematical role: definition, hypothesis, theorem/proposition/lemma, calculation, proof, cited prerequisite, example, interpretation, numerical result, or open problem. Prioritize prose that conceals actual assumptions, an algebraic step, a bound, or a limit transition. Preserve useful intuition. Avoid cosmetic rewriting.

Ask:
- Is the conclusion stated unambiguously under sufficient hypotheses?
- Are all recurring objects and symbols defined consistently?
- Is a displayed equation more precise and shorter than verbal narration?
- Is the proof locally checkable, or does it rely on an unstated majorant, independence assumption, density result, boundary sign, or convergence theorem?
- Can the proof be separated from another argument without bloating the page?

## 3. Write concise visible results with independently expandable proofs

Use the site's existing `statement`, `eq`, and `details.proof` conventions. Keep the result and essential assumptions visible. Provide separate expandable proofs for distinct substantive claims; do not collapse a whole subsection into a single proof or create one disclosure per trivial identity. Write formulas for meaningful intermediate estimates and precise convergence modes. Provide stable IDs for necessary references without renumbering existing ones. Preserve MathJax delimiters and existing copy/source behavior.

For example, prefer:
```html
<div class="statement">
  <div class="label">Proposition — Descriptive mathematical result</div>
  <p>Explicit hypotheses and conclusion.</p>
  <div class="eq">\[ ... \]</div>
</div>
<details class="proof">
  <summary>Proof of the proposition</summary>
  <div class="proof-body">
    <p>Short reason for the calculation.</p>
    <div class="eq">\[ ... \]</div>
    <span class="qed">∎</span>
  </div>
</details>
```
Adapt to existing HTML and accessibility patterns, rather than introducing a new design system.

## 4. Verify actual mathematics

Check indices, algebra, normalization, dimensions, coefficients, geometric-series tails, integrability, operator domains, and hypotheses. Be exact about weak/strong, almost-sure, in-probability, and `L^p` convergence. For dominated convergence, show a legitimate integrable dominator where nontrivial. In probability sections check filtration, predictability, conditional independence, Itô isometry, quadratic variation, finite variation, stopping, Brownian reflection, bridge minima, and the variance-two driver `sqrt(2) W`. The regulator/local-time convention must agree with Chapter 10. Cite established advanced results rather than offering incomplete pseudo-proofs.

Treat mathematical corrections at two levels: (a) local exposition/notation/estimate errors may be corrected with explanation; (b) potential changes to published research results require a discrepancy report and human review, not silent alteration.

## 5. Preserve scientific meaning and interface

Do not change equation numbers, IDs, published manuscript links, bibliography semantics, conditions, experiments, solver parameters, seeds, data, or results. Do not alter the approved editorial design to accommodate formulas: prefer aligned, broken, or locally scrollable equations. Maintain lazy MathJax, search, deep links, copy, accessibility, disclosure semantics, responsive sidebar/drawer, print restoration, and deferred figures.

## 6. Test and record evidence

Run `python3 build.py` and `python3 build.py --check`. When browser tools are available, run project smoke/readability/benchmark tests and cover all 14 chapters + six appendices, including mobile widths and open/closed proofs. Compare numerical checksums and seeded stochastic outputs to baseline. Test physical iOS Safari/WebKit only when truly available; otherwise label it `NOT TESTED`, not passed. Capture actual commands, environment, failures and screenshots or traces when possible.

Write an audit with (1) location, (2) issue and rationale, (3) mathematical repair, (4) verification, (5) preservation checks, and (6) unresolved assumptions or manual-device gates. Historical reports remain intact.

## 7. Completion criterion

The final result should be **more mathematically explicit but less rhetorically repetitive**, and should not enlarge the research claims. Never report a mathematical or device audit as exhaustive without corresponding evidence.
