# Workshop 5 · Module 2 — Homework
## Parallel Coordinates & Radar Charts

**Due**: Before Workshop 5, Module 4
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Parallel Coordinates (35 points)
Using the e-Car loan dataset (sample 500 rows), produce parallel coordinates of FICO, Rate, Amount, Term, Spread. (a) Colour by Tier with viridis palette. (b) Same chart with grey+accent: highlight Tier 1 only. (c) Try 3 different axis orderings. In 150 words, explain which ordering best reveals the FICO–Rate–Tier relationship and why.

### Part B — Radar Chart (25 points)
Compute the mean profile (all 5 variables, normalised 0–1) for Tier 1 and Tier 5. Produce a radar chart comparing the two profiles. In 100 words, explain what the shape difference reveals about credit-tier profiles and note one way the radar chart is misleading.

### Part C — Comparison (20 points)
For the same data, produce a pairs plot (GGally/seaborn pairplot). In 150 words, compare what parallel coordinates reveals vs what the pairs plot reveals. Which relationships are visible in one but not the other?

### Part D — Interactive (20 points)
Produce an interactive parallel coordinates plot with plotly (R or Python). Export as a screenshot showing one axis brushed (e.g., FICO > 750 selected). In 100 words, explain what the brushing reveals about high-FICO applicants.

### Submission Checklist
- [ ] `W05_M02_homework.R` + `W05_M02_homework.py`
- [ ] All figures as PNG (300 dpi) + plotly screenshot
- [ ] PDF report (max 4 pages)
