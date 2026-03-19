# Workshop 4 · Module 6 — Homework
## Correlation & Association Visualization

**Due**: Before Workshop 4, Module 8
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Correlation Heatmap (25 points)
For the Google Play Store dataset, select 5–6 numeric variables (Rating, log(Reviews), log(Installs), Size, Price). Produce a correlation heatmap following all five design principles: diverging palette, annotated cells, lower triangle, clustered, fixed [-1, 1] scale. Produce in both R and Python. In 100 words, identify the two strongest and two weakest correlations and hypothesise why.

### Part B — Pairs Plot (25 points)
Produce a pairs plot of Rating, log(Reviews), Size, and Type (as colour) using GGally::ggpairs() (R) and sns.pairplot() (Python). In 100 words, describe one relationship that is visible in the scatter but would be missed by the heatmap alone (e.g., clustering by Type, nonlinearity).

### Part C — Three Coefficients (25 points)
For log(Reviews) vs Rating, compute Pearson, Spearman, and Kendall. Produce the scatter plot with regression line. In 100 words, explain why the three coefficients differ (or agree) and which is most appropriate for this data.

### Part D — Categorical Association (25 points)
Compute a chi-squared test and Cramér's V for Type × Category (top 5 categories). Produce a 100% stacked bar. In 100 words, interpret the visual pattern and the V statistic: is there a meaningful association between app category and pricing model?

### Submission Checklist
- [ ] `W04_M06_homework.R` + `W04_M06_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
