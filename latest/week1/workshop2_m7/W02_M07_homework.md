# Workshop 2 · Module 7 — Homework
## seaborn & plotnine Mastery

**Due**: Before Workshop 2, Module 9
**Format**: Python script (.py or .ipynb) + R script (for comparison) + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — seaborn Gallery (30 points)
Using the Google Play Store dataset, produce six charts in seaborn:
1. `sns.scatterplot(x="Reviews", y="Rating", hue="Type")` with log x-scale
2. `sns.boxplot(x="Content_Rating", y="Rating", hue="Type")`
3. `sns.violinplot(x="Type", y="Rating", split=True)`
4. `sns.histplot(x="Rating", hue="Type", kde=True)`
5. `sns.heatmap()` of correlation matrix for numeric columns
6. `sns.catplot(kind="bar")` showing mean Rating by top 6 Categories

### Part B — Figure-Level vs Axes-Level (20 points)
Produce the same scatter plot two ways:
1. Figure-level: `sns.relplot(col="Content_Rating", col_wrap=2)`
2. Axes-level: `plt.subplots(2, 2)` with `sns.scatterplot(ax=axes[i,j])` loop
In 100 words, explain when each approach is more appropriate.

### Part C — plotnine Parity (30 points)
Translate **three** of your Part A charts from seaborn to plotnine syntax. Show the code side by side. In 100 words, compare the readability and code length.

### Part D — Three-Way Comparison (20 points)
Produce one scatter plot (Reviews vs Rating, coloured by Type) in:
1. matplotlib (OO API)
2. seaborn (axes-level)
3. plotnine (GoG syntax)
Compare code length (lines) and visual output. In 100 words, state which you prefer and why.

### Submission Checklist
- [ ] `W02_M07_homework.py` (seaborn + plotnine)
- [ ] `W02_M07_homework.R` (ggplot2 comparison)
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
