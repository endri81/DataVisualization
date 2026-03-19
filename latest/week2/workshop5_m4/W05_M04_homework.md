# Workshop 5 · Module 4 — Homework
## Heatmaps & Clustered Displays

**Due**: Before Workshop 5, Module 6
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Correlation Heatmap (25 points)
Using the e-Car loan dataset, produce a clustered correlation heatmap of FICO, Rate, Amount, Term, Cost of Funds, and Spread. Apply: lower triangle mask, diverging palette (RdBu), fixed [-1,1] scale, annotated cells, Ward clustering. Produce in both R (`pheatmap`) and Python (`sns.heatmap`). In 100 words, identify the two strongest positive and negative correlations and explain why they make domain sense.

### Part B — Z-Score Effect (25 points)
Create a 20-sample × 6-variable subset of the e-Car data (select 20 random loans, use the 6 numeric variables). Produce: (a) raw-value heatmap with sequential palette, (b) z-scored heatmap with diverging palette. Both clustered with Ward linkage. In 150 words, explain what patterns become visible after z-scoring that were hidden in the raw-value version.

### Part C — Clustered Heatmap with Annotation (30 points)
Using the same 20-sample subset, add a row-colour sidebar showing Tier (1–5 as different colours). Produce with `pheatmap(annotation_row=)` in R and `sns.clustermap(row_colors=)` in Python. In 100 words, discuss whether the dendrogram clusters align with the Tier categories.

### Part D — Design Critique (20 points)
Find a heatmap in a published paper or online article (screenshot or URL). Identify which of the five design principles it follows and which it violates. Suggest specific improvements. 150 words.

### Submission Checklist
- [ ] `W05_M04_homework.R` + `W05_M04_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 5 pages)
