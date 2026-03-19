# Workshop 5 · Module 3 — Homework
## Dimensionality Reduction

**Due**: Before Workshop 5, Module 5
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — PCA on e-Car (30 points)
Using the e-Car dataset (FICO, Rate, Amount, Term, Cost of Funds, Spread — 6 numeric vars), scale the data and run PCA. Produce: (a) scree plot with 80% threshold, (b) biplot coloured by Tier. In 150 words, interpret the biplot: which variables drive PC1? Which drive PC2? What does the angle between FICO and Rate arrows tell you?

### Part B — t-SNE Perplexity Experiment (25 points)
Run t-SNE on the same data with perplexities 5, 15, 30, 50. Produce a 1×4 panel. In 100 words, explain how perplexity changes the embedding and which value best reveals the Tier clusters.

### Part C — PCA vs t-SNE vs UMAP (25 points)
Produce a 1×3 panel comparing PCA, t-SNE (best perplexity from Part B), and UMAP on the same data, coloured by Tier. In 150 words, compare: which method best separates tiers? Which preserves the FICO gradient?

### Part D — Pitfall Check (20 points)
Run PCA on the e-Car data WITHOUT scaling. Compare the biplot to Part A (scaled). In 100 words, explain what goes wrong and why scaling is mandatory.

### Submission Checklist
- [ ] `W05_M03_homework.R` + `W05_M03_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 5 pages)
