# Workshop 4 · Module 9 — Homework
## EDA Automation & Reproducible Reports

**Due**: Before Workshop 4, Module 10 (Lab)
**Format**: Quarto/RMarkdown + Jupyter notebook + HTML outputs
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Auto-EDA Report (25 points)
Generate an automated EDA report for the Netflix dataset using: (a) skimr::skim() in R (console output, screenshot for report), (b) ydata-profiling in Python (HTML export). In 150 words, list the 3 most important alerts or anomalies flagged by the automated report.

### Part B — Hybrid Workflow (35 points)
Starting from the auto-EDA alerts in Part A, perform 3 manual deep-dives: (a) one distribution finding requiring a custom histogram with annotation, (b) one correlation finding requiring a scatter plot with smoother, (c) one missingness finding requiring a shadow analysis. For each, explain why the auto-report flagged it and what your manual analysis reveals.

### Part C — Reproducible Report (25 points)
Write a Quarto (.qmd) or Jupyter (.ipynb) document that: (a) loads the Netflix data, (b) produces the 3 manual deep-dive charts from Part B inline, (c) includes interpretive prose between code chunks, (d) renders to HTML. Submit the source file and the rendered HTML.

### Part D — Parameterisation Sketch (15 points)
Write (but do not render) a parameterised Quarto YAML header that accepts `dataset`, `target`, and `group` parameters. Show the first code chunk that reads the parameterised dataset and produces a faceted histogram. Explain in 100 words how you would use this template to generate EDA reports for all 5 course datasets.

### Submission Checklist
- [ ] Auto-EDA HTML outputs (skimr screenshot, ydata-profiling HTML)
- [ ] Quarto/Jupyter source + rendered HTML
- [ ] PDF summary (max 4 pages)
