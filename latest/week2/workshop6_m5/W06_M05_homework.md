# Workshop 6 · Module 5 — Homework
## Seasonal & Calendar Visualizations

**Due**: Before Workshop 6, Module 7
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Calendar Heatmap (25 points)
Compute daily Netflix additions for 2020. Produce a calendar heatmap (DOW × week, colour = count of titles added that day). Produce in both R (`geom_tile`) and Python (`pivot_table + imshow` or `calplot`). In 100 words, identify: (a) are there weekly patterns (certain days get more releases)? (b) are there seasonal patterns (certain months busier)?

### Part B — Seasonal Subseries (25 points)
Compute monthly Netflix additions for 2016–2021. Overlay all 6 years on a Jan–Dec axis using the grey+accent strategy (highlight 2021 in red). Produce in both R and Python. In 100 words, answer: is the seasonal shape consistent across years, or has it changed? Does 2020 (COVID year) look different from other years?

### Part C — Monthly Boxplot (25 points)
Produce a monthly boxplot summarising the distribution of titles added per month (one box per month, spanning 2016–2021). Overlay the mean line. In 100 words, identify: which month has the highest median? Which has the widest IQR (most variable)? Is there a clear seasonal release strategy?

### Part D — Polar vs Linear (25 points)
Produce the same average monthly Netflix additions as: (a) a linear bar chart, (b) a polar bar chart. Place side-by-side. In 150 words, compare: which is easier to read for precise value comparison? Which better communicates the cyclical nature of the data? When would you choose each?

### Submission Checklist
- [ ] `W06_M05_homework.R` + `W06_M05_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 5 pages)
