# Workshop 2 · Module 2 — Homework
## ggplot2 Mastery

**Due**: Before Workshop 2, Module 4
**Format**: PDF report (max 4 pages) + R script + Python script
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — Mapping vs Setting (25 points)
1. Using Google Play Store data, create a scatter plot of Reviews (log) vs Rating.
2. Produce three versions: (a) all points blue (setting), (b) coloured by Type (mapping), (c) coloured by Content Rating (mapping).
3. In 100 words, explain the visual and legend differences.

### Part B — Position Adjustments (25 points)
1. Create a bar chart of Content Rating, filled by Type (Free/Paid).
2. Produce four versions with position = "stack", "dodge", "fill", and "identity" (with alpha=0.5).
3. In R and Python (8 charts total).
4. In 100 words, explain when each position is most appropriate.

### Part C — Inheritance (25 points)
1. Create a scatter of displ vs hwy (mpg dataset), coloured by drv.
2. Add geom_smooth. Produce two versions: (a) global aes (one smooth per drv), (b) local aes (one overall smooth).
3. In 100 words, explain the visual and analytical difference.

### Part D — stat_summary (25 points)
1. Compute mean Rating ± SE per Category (top 8) using stat_summary(geom = "pointrange").
2. Produce in both R (ggplot2) and Python (plotnine or matplotlib errorbar).
3. Add coord_flip() and theme_minimal().

### Submission Checklist
- [ ] `W02_M02_homework.R` + `W02_M02_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
