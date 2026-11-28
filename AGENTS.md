# Codex repository instructions

This repository publishes an interactive mathematical exposition of **Heat Equation with a Dynamical Singular Potential on the Boundary**. The application lives in `heat-equation-interactive/`.

## Scope and hierarchy

Read `heat-equation-interactive/README.md`, `heat-equation-interactive/VERIFICATION.md`, and the existing mathematical audit reports before mathematical editorial work. For V5.6, follow `prompts/v5.6-mathematical-consistency.md` and the reusable `.agents/skills/mathematical-exposition/SKILL.md`. The task prompt is the release-specific checklist; the skill is the enduring editing standard.

**Do not treat agent instructions as permission to change the research.** Preserve all established results, hypotheses, classifications, limitations, theorem/equation IDs and links, bibliography, scientific experiments, data, figure behavior, visual identity, and accessibility unless the user specifically requests a change. If a discrepancy would alter a research result, document it for human review rather than silently changing a theorem. Do not convert numerical/heuristic evidence into mathematical proof.

## Source of truth

- Edit `heat-equation-interactive/src/content/` fragments, `src/navigation.html`, `src/template.html`, or maintained assets only when the task requires it.
- `heat-equation-interactive/docs/index.html` and the generated worker wrapper are build outputs. Never hand-edit them.
- Preserve the existing single-document architecture, fragment URLs, MathJax lazy rendering, disclosure behavior, and figure/worker initialization.
- The scientific manuscripts linked in the repository README are references; do not reinstate the removed original 2022 thesis citation or replace established public manuscript links with internal file labels.

## Mathematical exposition standard

Prefer a visible hypothesis/statement/conclusion followed by a *separate, individually expandable* proof for nontrivial arguments. Display meaningful intermediate equalities, inequalities, majorants, and limit justifications. Distinguish proven results from cited standard prerequisites, conditional claims, numerical observations, and open questions. Avoid gratuitous formalism and long textbook detours. Confirm constants, factors of two, sign conventions, measurable spaces, norms, convergence modes and all stated assumptions. Coordinate the stochastic conventions in Chapter 10 and Appendix E.

Do not mechanically convert every explanation into a proposition; preserve intuitive passages and readable transitions.

## Verification discipline

From `heat-equation-interactive/`, run as applicable:
```sh
python3 build.py
python3 build.py --check
python3 -B tools/browser_smoke.py --chromium /usr/bin/chromium
python3 -B tools/math_readability_smoke.py --chromium /usr/bin/chromium
python3 -B tools/mobile_benchmark.py docs
```
Adapt the browser binary to the available environment and document the exact command and result. Verify all chapter/appendix rendering, disclosures, deep links, search, equation copying, print, navigation, figure controls, and numerical checks. Compare against the recorded V5.5 baseline where meaningful.

**Never equate mobile-size desktop Chromium with physical iPhone Safari.** Test actual WebKit and a physical iPhone only if available. Otherwise say explicitly `NOT TESTED` and list the remaining manual acceptance steps. Do not claim tests or mathematical proofs have been independently validated when they have not.

For V5.6, produce `heat-equation-interactive/MATHEMATICAL_CONSISTENCY_AUDIT_V5_6.md` documenting section-by-section changes, mathematical checks, preservation, measured regressions, and limitations. Do not overwrite historical audit reports.
