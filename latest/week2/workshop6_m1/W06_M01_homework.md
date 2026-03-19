# Workshop 6 · Module 1 — Homework
## Time as a Visual Dimension

**Due**: Before Workshop 6, Module 3
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Granularity Comparison (25 points)
Using the Netflix dataset, compute the number of titles added per day, per week, per month, and per year (filter to 2015–2021). Produce a 2×2 panel showing all four granularities of the same "titles added over time" data. In 100 words, explain which granularity best reveals the Netflix content strategy shift (movie → TV show pivot) and why.

### Part B — Decomposition (30 points)
Using the monthly count of Netflix titles added (2015–2021), run an STL decomposition in both R (`stl()`) and Python (`STL()`). Produce the four-panel decomposition plot (observed, trend, seasonal, residual). In 150 words, interpret: (a) what does the trend component reveal? (b) is there a seasonal pattern in Netflix's content releases? (c) are there any notable residual spikes?

### Part C — Chart Type Selection (25 points)
Produce the monthly Netflix additions data using three different chart types: (a) line chart, (b) step chart, (c) bar chart. Arrange as a 1×3 panel. In 100 words, argue which chart type is most appropriate for this data and why.

### Part D — Pitfall Detection (20 points)
Create a deliberately BAD time chart that commits at least 2 of the pitfalls discussed (categorical axis, truncated y-axis, connected through missing data). Then create the CORRECTED version side-by-side. In 100 words, explain what each pitfall distorts.

### Submission Checklist
- [ ] `W06_M01_homework.R` + `W06_M01_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
