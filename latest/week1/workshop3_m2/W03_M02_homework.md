# Workshop 3 · Module 2 — Homework
## Boxplots, Violins & Beeswarm

**Due**: Before Workshop 3, Module 4
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Shape Blindness Demo (25 points)
Create three synthetic datasets with identical boxplot statistics but different shapes (unimodal, bimodal, right-skewed). Show boxplot (top row) and histogram (bottom row) in a 2×3 grid. In 100 words, explain why boxplots alone are insufficient.

### Part B — Boxplot + Jitter (25 points)
Using Google Play Store data, produce a horizontal boxplot of Rating by the top 6 categories. Add jitter overlay (`geom_jitter` / `sns.stripplot`), mean diamonds, and notches. Sort by median. Produce in R and Python.

### Part C — Violin + Box (25 points)
Produce violin plots of Rating by Type (Free vs Paid) with an embedded narrow boxplot inside each violin. Then produce a split violin comparing Free vs Paid within each of the top 4 categories. Produce in R and Python.

### Part D — Raincloud (25 points)
Produce a raincloud plot of Rating by Type showing half-violin + box + jitter. In R, use `ggrain::geom_rain()` (or manual layers). In Python, use manual composition. In 100 words, explain why rainclouds are preferred in scientific publications.

### Submission Checklist
- [ ] `W03_M02_homework.R` + `W03_M02_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
