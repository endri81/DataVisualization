# Workshop 2 · Module 10 — Homework (Final Lab)
## Grammar of Graphics Cheat Sheet

**Due**: Before Workshop 3, Module 1
**Format**: PDF document (15 pages, one chart per page) + R script + Python script
**Weight**: Part of Workshop 2 homework (5% of total grade)

### The Assignment
Create a "Grammar of Graphics Cheat Sheet" implementing 15 chart types. Each page shows: (a) the chart rendered, (b) the ggplot2 R code, (c) the plotnine or seaborn Python code, (d) a one-sentence description of the grammar layers used.

### Required Chart Types (15)
1. Horizontal bar (sorted, direct labels)
2. Grouped bar (position = "dodge")
3. Stacked bar (position = "stack")
4. Histogram (bins = 30, mean line)
5. Density plot (filled, grouped)
6. Boxplot (notch, mean overlay)
7. Violin plot (split by group)
8. Scatter (color = group, log scale)
9. Bubble chart (4 variables: x, y, color, size)
10. Line chart (direct labels, no legend)
11. Area chart (stacked)
12. Lollipop chart (segment + point)
13. Dumbbell chart (two points + segment)
14. Heatmap (annotated, diverging scale)
15. Faceted scatter (facet_wrap + geom_smooth)

### Submission Checklist
- [ ] PDF document (15 pages)
- [ ] `W02_M10_cheatsheet.R` — all 15 charts in ggplot2
- [ ] `W02_M10_cheatsheet.py` — all 15 charts in plotnine/seaborn
- [ ] All charts use Google Play Store or mpg data
