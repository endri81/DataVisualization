# Workshop 2 · Module 5 — Homework
## Faceting Mastery

**Due**: Before Workshop 2, Module 7
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — facet_wrap (25 points)
Using Google Play Store data, produce a histogram of Rating faceted by the top 6 categories. Use `facet_wrap(~Category, ncol=3, scales="fixed")`. Produce in R (ggplot2) and Python (plotnine or plt.subplots). Add custom strip labels showing the category name and sample size.

### Part B — facet_grid (25 points)
Produce a scatter of Reviews (log) vs Rating faceted by `Type ~ Content Rating` (2 rows × 4 columns). Use `facet_grid()` in R and `plt.subplots(2, 4)` in Python. Add `geom_smooth(method="lm")` to each panel.

### Part C — Fixed vs Free Scales (25 points)
Using the Netflix dataset, facet duration by content type (Movie vs TV Show). Produce two versions: (a) `scales="fixed"`, (b) `scales="free_y"`. In 150 words, explain why the fixed version is misleading for this data and why free scales are justified.

### Part D — Facet vs Patchwork (25 points)
Create a four-panel dashboard of the Google Play Store data:
1. Panel (a): bar chart of top 8 categories (facet would work)
2. Panel (b): histogram of Rating (different geom → needs patchwork)
3. Panel (c): scatter of Reviews vs Rating
4. Panel (d): boxplot of Rating by Type
Produce using patchwork (R) and GridSpec (Python). In 100 words, explain why this dashboard requires patchwork, not faceting.

### Submission Checklist
- [ ] `W02_M05_homework.R` + `W02_M05_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
