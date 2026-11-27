# Refactoring brief

**Input:** the accepted V5.1 Editorial Polish standalone HTML.

**Task:** Convert the existing mathematical exposition into a maintainable, GitHub Pages–ready static website. Separate chapter and appendix authoring files, reference material, layout, navigation, styles, chapter-specific JavaScript, scientific data, and third-party dependencies. Keep the current editorial design and English content. Do not rewrite the mathematics, change theorem hypotheses, modify numerical algorithms or parameters, remove interactive features, or restore references to the original thesis.

Preserve the existing single scrolling reading experience and all section and theorem anchor IDs. Prefer a dependency-free deterministic build over runtime fragment loading, because the existing scripts depend on a complete DOM and their original execution order. Extract the PDE worker to editable JavaScript and generate the existing blob-worker source from that file. Separate the Chapter 11 datasets without rounding values. Retain the local MathJax bundle and its license.

Deliver the complete project with generated deployment output, clear ownership of editable versus generated files, a build check for missing assets and anchors, reproducible browser smoke tests, numerical reproduction instructions, and a GitHub Pages deployment guide. Verify the refactor against V5.1 and report any testing restrictions. Do not publish to a repository or add a license for the author's own work without permission.
