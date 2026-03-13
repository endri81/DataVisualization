# Workshop 3 · Module 8 — Homework
## Small Multiples & Multi-Panel Composition

**Due**: Before Workshop 3, Module 10
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Spaghetti → Small Multiples (25 points)
Using Google Play Store data, show the rating distribution for the top 6 categories two ways: (a) overlaid density curves (spaghetti), (b) faceted small multiples with shared axes. In 100 words, explain why small multiples are easier to read.

### Part B — Heterogeneous Dashboard (35 points)
Build a four-panel dashboard with different chart types: (a) sorted horizontal bar, (b) histogram, (c) scatter with regression, (d) boxplot. Compose with `patchwork` in R and `GridSpec` in Python. Add panel labels (a–d), global title, and source caption.

### Part C — Asymmetric Layout (25 points)
Build a 3-panel layout where panel (a) spans the full top row (wide) and panels (b) and (c) split the bottom row. Use `plot_layout(heights=c(2,1))` in R and `gs[0,:] + gs[1,0] + gs[1,1]` in Python.

### Part D — subplot_mosaic (15 points)
Reproduce your Part B dashboard using `plt.subplot_mosaic()` with a named ASCII grid. Compare the code to GridSpec in 100 words.

### Submission Checklist
- [ ] `W03_M08_homework.R` + `W03_M08_homework.py`
- [ ] All figures as PNG (300 dpi) + one PDF export
- [ ] PDF report (max 4 pages)
