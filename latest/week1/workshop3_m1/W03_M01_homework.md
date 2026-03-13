# Workshop 3 · Module 1 — Homework
## Distribution Visualization

**Due**: Before Workshop 3, Module 3
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Bin Width Experiment (25 points)
Using Google Play Store Rating data, produce histograms with bins = 5, 10, 20, 40, 80, 160. Arrange as a 2×3 grid. In 100 words, explain which bin count best reveals the distribution's shape and why.

### Part B — Histogram + KDE Overlay (25 points)
Produce a density-scaled histogram with KDE overlay, mean line (dashed green), and median line (dotted orange). Add a text annotation describing the skewness. Produce in R and Python.

### Part C — Grouped Density (25 points)
Compare Rating distributions for the top 3 Content Rating categories using overlaid density curves. Then compare all 5 categories using a ridgeline plot (ggridges in R, manual offset in Python). In 100 words, explain why ridgeline is better for 5+ groups.

### Part D — Bandwidth Sensitivity (25 points)
Using KDE on Rating data, produce three density curves with adjust = 0.3, 1.0, 3.0 (R) or bw_method = 0.05, 0.2, 0.8 (Python). In 100 words, explain the bias-variance tradeoff: what information is lost at each extreme?

### Submission Checklist
- [ ] `W03_M01_homework.R` + `W03_M01_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
