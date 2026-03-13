# Workshop 3 · Module 4 — Homework
## Relationship Charts

**Due**: Before Workshop 3, Module 6
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Scatter + Regression (20 points)
Using Google Play Store data, produce a scatter of Reviews (log x) vs Rating, coloured by Type, with OLS regression lines per group. Produce in R and Python.

### Part B — Overplotting (25 points)
Show the same Reviews vs Rating data four ways: (a) raw, (b) alpha=0.05, (c) hexbin, (d) 2D density contour. Arrange as 1×4 panel. In 100 words, explain which works best for this dataset's n.

### Part C — Bubble Chart (25 points)
Create a Gapminder-style bubble from the Google Play Store: x=Reviews (log), y=Rating, size=Installs, color=Category (top 5). Produce in R and Python. In 100 words, discuss the 5-variable encoding limit.

### Part D — Marginal Distributions (15 points)
Add marginal histograms to your scatter from Part A using ggMarginal (R) and sns.jointplot or GridSpec (Python).

### Part E — Smoother Comparison (15 points)
Show the same scatter with: (a) method="lm", (b) method="loess". In 100 words, explain which smoother is more appropriate for this data and why.

### Submission Checklist
- [ ] `W03_M04_homework.R` + `W03_M04_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
