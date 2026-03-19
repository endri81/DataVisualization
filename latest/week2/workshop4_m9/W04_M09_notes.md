# Workshop 4 · Module 9 — Course Notes
## EDA Automation & Reproducible Reports

### 1. Manual vs Automated EDA
Manual EDA (M07–M08) gives full narrative control but takes 2–4 hours per dataset. Automated EDA generates a comprehensive baseline in 30 seconds but lacks interpretive depth. They are complementary: auto-EDA screens for anomalies; manual EDA produces the publishable analysis. The hybrid workflow uses both sequentially.

### 2. Auto-EDA Packages
**R**: `skimr::skim()` provides a compact console summary grouped by variable type — ideal for pipe chains. `DataExplorer::create_report()` generates a complete HTML report with distributions, correlations, missingness, PCA. `summarytools::dfSummary()` produces frequency tables with embedded mini-graphs.
**Python**: `ydata-profiling` (formerly pandas-profiling) is the gold standard — comprehensive HTML with alerts, interactions, correlations, and missing data analysis. `sweetviz` specialises in side-by-side comparison of two datasets or subgroups. `dtale` provides an interactive browser-based explorer with click-to-code functionality.

### 3. The Hybrid Workflow
Five steps: (1) Auto-EDA report (30 seconds), (2) Scan for anomalies — missingness patterns, skew, outlier alerts, high correlations, (3) Manual deep-dives on the 3–5 findings that matter — custom plots with annotations, (4) Compose dashboard via patchwork/GridSpec (30 minutes), (5) Write reproducible report with narrative (1 hour). Total: ~3 hours for a complete EDA, down from 4+ hours for purely manual work.

### 4. Reproducible Report Formats
**Quarto (.qmd)**: The modern standard from Posit (2022+). Renders to HTML, PDF, revealjs slides, docx, and dashboards. Supports R, Python, Julia, and Observable JS in the same document. **RMarkdown (.Rmd)**: The legacy R standard (2014+), still widely used. knitr + pandoc pipeline. **Jupyter (.ipynb)**: The Python standard. Cell-based notebooks with inline plots and markdown. Can be rendered by Quarto for cross-language compatibility. All three embed code + prose + output in a single source file, ensuring reproducibility.

### 5. Parameterised Reports
A parameterised report uses a YAML header to define variables (dataset path, target column, grouping variable) that are injected at render time. One template generates many outputs: `quarto_render("template.qmd", execute_params = list(dataset = "netflix.csv"))`. Applications: batch EDA across multiple datasets, coursework grading (one template per variant), automated monthly reporting.

### 6. Why Reproducibility Matters
Six benefits: auditability (reviewer re-runs code, gets identical output), version control (git diff shows exactly what changed), error correction (fix one line, re-render — no manual copy-paste), scalability (same report for 10 datasets via parameterisation), collaboration (co-authors edit code, not screenshots), and publication (journals increasingly require reproducible code archives).

### References
- Peng, R. (2011). Reproducible Research in Computational Science. *Science*, 334(6060).
- Quarto documentation: https://quarto.org
- ydata-profiling: https://docs.profiling.ydata.ai
