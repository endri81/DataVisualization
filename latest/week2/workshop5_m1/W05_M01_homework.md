# Workshop 5 · Module 1 — Homework
## High-Dimensional Data

**Due**: Before Workshop 5, Module 3
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Multi-Encoded Scatter (30 points)
Using the e-Car loan dataset, produce a scatter of FICO (x) vs Rate (y) encoding Tier (colour), Amount (size), and Car Type (shape). Produce in R (ggplot2) and Python (matplotlib). In 150 words, explain which encoding is most effective and which is hardest to read, referencing the Cleveland & McGill ranking.

### Part B — Overload Experiment (20 points)
Add a 6th encoding (e.g., Term as line style or transparency). Produce the chart. In 100 words, explain why this makes the chart worse, citing the Healey & Enns cognitive limit.

### Part C — Aggregation Comparison (30 points)
For the full e-Car dataset (208K rows), produce: (a) raw scatter (2K sample), (b) hexbin, (c) 2D KDE contour, (d) scatter + marginal histograms. Arrange as a 2×2 panel. In 150 words, compare which aggregation technique best reveals the FICO–Rate relationship.

### Part D — Strategy Selection (20 points)
Given a dataset with 15 numeric variables and 50K rows, which of the five strategies would you choose and why? Write 150 words justifying your choice and naming the specific chart type and R/Python function you would use.

### Submission Checklist
- [ ] `W05_M01_homework.R` + `W05_M01_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
