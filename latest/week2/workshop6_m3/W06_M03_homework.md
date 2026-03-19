# Workshop 6 · Module 3 — Homework
## Line Charts in Code

**Due**: Before Workshop 6, Module 5
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Six Geometries on Netflix Data (30 points)
Using the Netflix dataset (monthly additions, 2015–2021), produce a 2×3 panel showing the same monthly data with six different geometries: (a) line chart, (b) step chart, (c) area chart, (d) stacked area by type (Movie + TV Show), (e) 100% stacked area by type, (f) line with ±1 SD ribbon (computed across years for each month-of-year). Produce in both R (patchwork) and Python (GridSpec). In 100 words, explain: when is each geometry appropriate, and when would it mislead?

### Part B — Date Formatting (20 points)
Produce the Netflix monthly additions line chart with four different date label formats: (a) "%Y" (year only), (b) "%b %Y" (abbreviated month + year), (c) "%Y-%m" (ISO format), (d) "%b" with year shown only on January ticks. Arrange as a 2×2 panel. In 100 words, explain which format is best for: a 7-year overview, a 2-year analysis, and a 6-month zoom.

### Part C — Stacked Area Design (25 points)
Compute monthly Netflix additions for the top 5 genres (2015–2021). Produce: (a) an absolute stacked area chart, (b) a 100% stacked area chart. Try two different stack orderings (alphabetical vs most-stable-at-bottom). In 150 words, discuss: (i) does the proportion of International content grow over time? (ii) what does the 100% version reveal that the absolute version hides? (iii) how does stack order affect readability?

### Part D — Confidence Ribbon (25 points)
For each month-of-year (January–December), compute the mean and 95% CI of Netflix monthly additions across the years 2016–2021 (6 observations per month). Produce a ribbon chart: the mean line with a shaded ±95% CI band. In 100 words, interpret: which months have the tightest CIs (most consistent)? Which have the widest (most variable)? Is there a clear seasonal pattern?

### Submission Checklist
- [ ] `W06_M03_homework.R` + `W06_M03_homework.py`
- [ ] All figures as PNG (300 dpi): six_geoms panel, date_formats panel, stacked area (2 orderings), ribbon
- [ ] PDF report (max 5 pages)
