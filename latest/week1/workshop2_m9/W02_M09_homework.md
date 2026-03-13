# Workshop 2 · Module 9 — Homework
## Tidy Data & Wrangling Mastery

**Due**: Before Workshop 2, Module 10
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — Pivot (25 points)
Create a wide-format GDP growth table (5 countries × 3 years). Reshape to long with `pivot_longer()` (R) and `melt()` (Python). Plot a line chart with `aes(x=year, y=gdp, color=country)`. Show the wide table, long table, and chart.

### Part B — Six Verbs Pipeline (30 points)
Using the Google Play Store dataset, chain all six verbs in one pipeline:
filter → select → mutate → group_by → summarise → arrange.
Compute mean Rating ± SE for the top 10 categories by count. Plot as a horizontal bar with error bars. Produce in R (one pipe chain ending in ggplot) and Python (method chain + matplotlib).

### Part C — Data Cleaning (25 points)
Write a cleaning pipeline for the Google Play Store dataset that handles all six common problems: remove duplicates, fix types (Reviews, Installs, Price), handle NAs, fix inconsistent Category names, filter outliers, and reshape if needed. Show `dim()` / `.shape` before and after each step.

### Part D — Join + Plot (20 points)
Create a secondary table with 5 category descriptions (e.g., "GAME: Entertainment applications"). Join it to the Google Play Store summary using `left_join()` / `merge()`. Use the description as the y-axis label in a horizontal bar chart. Produce in R and Python.

### Submission Checklist
- [ ] `W02_M09_homework.R` + `W02_M09_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
