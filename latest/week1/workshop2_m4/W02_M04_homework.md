# Workshop 2 · Module 4 — Homework
## Scales & Coordinates Mastery

**Due**: Before Workshop 2, Module 6
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — Log Scale (25 points)
Using Google Play Store data, produce a scatter of Reviews (x) vs Rating (y), coloured by Type. Show two versions side by side: (a) linear x, (b) log10 x. Format x-axis labels with commas. Produce in R and Python. In 100 words, explain which scale reveals the relationship better.

### Part B — Colour Scale Selection (25 points)
Produce three charts using the correct colour scale type:
1. Categorical: bar chart of top 8 categories, each a different colour (`scale_fill_brewer`)
2. Sequential: heatmap of Rating by Category × Content Rating (`scale_fill_viridis_c`)
3. Diverging: deviation from mean Rating per category (`scale_fill_gradient2`, midpoint = mean)

### Part C — Axis Formatting (25 points)
Create a bar chart of simulated quarterly revenue ($1.2M–$3.2M). Produce three versions with y-axis formatted as: (a) raw numbers, (b) comma-separated, (c) dollar with M suffix. Produce in R and Python.

### Part D — Zoom Experiment (25 points)
Using any scatter + geom_smooth combination:
1. Show the full data with regression line
2. Zoom to x ∈ [25, 75] using scale limits — note the slope change
3. Zoom to x ∈ [25, 75] using coord_cartesian — note the slope preservation
4. In 100 words, explain why coord_cartesian is safer.

### Submission Checklist
- [ ] `W02_M04_homework.R` + `W02_M04_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
