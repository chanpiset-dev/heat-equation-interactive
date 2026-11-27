Chapter 11 V3.3 — reproducible numerical experiments

1. Create a Python environment (tested with Python 3.13).
2. Install dependencies: python -m pip install -r requirements.txt
3. Run: python reproduce_chapter11.py numerical_investigations_v3_3.json

The supplied JSON is the precomputed dataset embedded in the standalone HTML. The script recomputes original and supplementary studies, including every plotted balance term, terminal error and Monte Carlo sample statistic. Python and NumPy versions are recorded in metadata; floating-point and random-library differences across environments may affect last digits. Slices are rounded to seven decimals. Monte Carlo seeds are fixed. No internet or manuscript files are required after dependencies are installed.

The finite-box computations use bounded regularized coefficients; none proves convergence to the singular PDE.

V5.1 repository layout: the original precomputed JSON is split into the registration files in ../docs/assets/data/chapter-11/. From the repository root, run python3 tools/export_data.py numerical_investigations_v3_3.json to reconstruct it. The website's download controls are also unchanged.
