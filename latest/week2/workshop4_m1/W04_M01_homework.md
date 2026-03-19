# Workshop 4 · Module 1 — Homework
## EDA Philosophy & First Look

**Due**: Before Workshop 4, Module 3
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — 4-Plot Diagnostic (30 points)
Using Google Play Store Rating data, produce Tukey's 4-plot (run sequence, lag-1, histogram, Q-Q) as a 2×2 panel. Produce in R (patchwork) and Python (plt.subplots). In 150 words, interpret each panel: Is there a trend? Autocorrelation? What shape? Normal?

### Part B — Letter-Value vs Boxplot (25 points)
Compare the standard boxplot and letter-value plot (geom_lv in R, sns.boxenplot in Python) of Rating by Type (Free/Paid). In 100 words, explain what additional information the letter-value plot reveals for this n ≈ 9,000 dataset.

### Part C — EDA First Look (25 points)
Using the Netflix dataset, produce an EDA first-look panel: (a) dimensions and types (printed output), (b) histogram of duration (movies), (c) boxplot of duration by type, (d) Q-Q plot of duration. In 150 words, summarise what you learn from this first look.

### Part D — Automated EDA Report (20 points)
Generate an automated EDA report using skimr::skim() (R) or ydata-profiling (Python) on the Google Play Store dataset. In 100 words, identify the three most important findings from the automated report that would guide your next exploration steps.

### Submission Checklist
- [ ] `W04_M01_homework.R` + `W04_M01_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
