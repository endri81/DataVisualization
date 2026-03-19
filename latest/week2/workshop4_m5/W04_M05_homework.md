# Workshop 4 · Module 5 — Homework
## Outlier Detection & Visual Diagnostics

**Due**: Before Workshop 4, Module 7
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Univariate Detection (25 points)
For Google Play Store Rating: (a) compute IQR fences and count outliers, (b) compute z-scores and count |z| > 2 outliers, (c) produce a boxplot with outliers highlighted in red, (d) produce a scatter of z-scores with threshold lines. In 100 words, explain why the two methods flag different counts.

### Part B — Mahalanobis (25 points)
Using log(Reviews) and Rating as two variables, compute Mahalanobis distance for all apps. Produce a scatter coloured by outlier status (threshold = χ²(2, 0.95)). In 100 words, identify one point that is normal on each axis individually but is a multivariate outlier, and explain why.

### Part C — Regression Diagnostics (30 points)
Fit Rating ~ log(Reviews) in both R and Python. Produce the four diagnostic plots. Identify observations with Cook's D > 4/n. Refit without those observations and compare slopes. In 150 words, interpret: is the regression relationship robust to influential points?

### Part D — Decision (20 points)
For the 3 most influential observations from Part C, look up the actual app name, category, and reviews. For each, determine the likely cause (data error, real extreme, different population) and recommend an action. Present as a 3-row table.

### Submission Checklist
- [ ] `W04_M05_homework.R` + `W04_M05_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
