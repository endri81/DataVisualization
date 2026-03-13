# Workshop 3 · Module 7 — Homework
## Uncertainty Visualization

**Due**: Before Workshop 3, Module 9
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — SE vs CI vs SD (20 points)
Using Google Play Store Ratings for the top 6 categories, compute mean, SE, 95% CI, and SD per category. Produce three pointrange plots side by side: one showing ±SE, one ±CI, one ±SD. In 100 words, explain which is most appropriate for comparing whether category means differ.

### Part B — Pointrange vs Bar+Error (25 points)
Produce the same grouped mean comparison two ways: (a) bar chart with error bars, (b) pointrange (dot+line only). Place side by side. In 100 words, explain why pointrange is preferred.

### Part C — Confidence Ribbon (25 points)
Using simulated time series (10 years), produce a line chart with two-layer ribbon: lighter 95% CI, darker ±SE. Produce in R (geom_ribbon) and Python (fill_between).

### Part D — Forest Plot (30 points)
Create a simulated forest plot with 6 studies + pooled estimate. Use diamond marker for pooled. Add a dashed vertical reference line at zero. Label each CI numerically. Produce in R and Python. In 100 words, interpret the plot: which studies show significant effects?

### Submission Checklist
- [ ] `W03_M07_homework.R` + `W03_M07_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
