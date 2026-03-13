# Workshop 3 · Module 5 — Homework
## Proportion Charts

**Due**: Before Workshop 3, Module 7
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Pie vs Bar (20 points)
Using the top 6 Google Play Store categories, produce a pie chart and a sorted horizontal bar chart with % labels side by side. In 100 words, explain which is more effective and why, citing Cleveland & McGill's perceptual ranking.

### Part B — Donut KPI (20 points)
Create a single-KPI donut showing the Free/Paid split (73%/27%) with the percentage as centre text. Produce in R (coord_polar) and Python (ax.pie with width parameter).

### Part C — Treemap (25 points)
Produce a treemap of all 10 categories (top 10 by count). Label each rectangle with the category name, count, and percentage. In R use treemapify; in Python use squarify. In 100 words, compare treemap readability to a sorted bar.

### Part D — Waffle (20 points)
Create a waffle chart of the top 4 categories (rounded to nearest %). In R use the waffle package; in Python use manual Rectangle loop. In 100 words, explain when waffles are better than pies.

### Part E — Best Alternative (15 points)
For the same 6-category data, produce a 100% stacked horizontal bar with % labels inside each segment. In 100 words, argue why this is the default choice for proportion visualization.

### Submission Checklist
- [ ] `W03_M05_homework.R` + `W03_M05_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
