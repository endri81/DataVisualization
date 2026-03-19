# Workshop 4 · Module 4 — Homework
## Missing Data Visualization

**Due**: Before Workshop 4, Module 6
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Missingness Audit (30 points)
For the Google Play Store dataset, produce: (a) a missingness matrix (vis_miss or msno.matrix), (b) a sorted missing % bar chart with a 5% threshold line, (c) a summary table of n_miss and pct_miss per column. In 150 words, identify the three most problematic columns and hypothesise whether each is MCAR, MAR, or MNAR with justification.

### Part B — Shadow-Augmented Analysis (35 points)
Using naniar::bind_shadow() (R) or manual .isna() columns (Python): (a) produce a shadow scatter of Reviews vs Rating showing NA rows at the margin, (b) overlay histograms of Reviews split by "Rating present" vs "Rating missing" groups. In 150 words, interpret whether the distributions differ and what mechanism this suggests.

### Part C — Imputation Comparison (35 points)
For the Rating column: (a) produce a histogram of complete cases, (b) apply mean imputation and overlay the result, (c) apply median imputation and overlay. In 150 words, compare the two imputation effects on the distribution shape. Which is less distorting and why?

### Submission Checklist
- [ ] `W04_M04_homework.R` + `W04_M04_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
