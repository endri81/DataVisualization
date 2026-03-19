# Workshop 4 · Module 6 — Course Notes
## Correlation & Association Visualization

### 1. Anscombe's Quartet (1973)
Four datasets with identical summary statistics (r = 0.82, slope = 0.50, mean of x = 9.0, mean of y = 7.5, R² = 0.67) but completely different visual patterns: I is linear, II is curved, III has one outlier, IV has one leverage point. The lesson: **always scatter plot before computing any correlation**. A single number cannot capture curvature, outliers, clusters, or leverage.

### 2. Three Correlation Coefficients
**Pearson r** measures linear association; assumes both variables are continuous and approximately normal. Sensitive to outliers. **Spearman ρ** measures monotonic association using ranks; robust to skew and outliers; appropriate for ordinal data. **Kendall τ** measures concordance (proportion of concordant minus discordant pairs); more robust than Spearman for small n or many ties. None captures non-monotonic dependence (e.g., U-shaped relationships) — use distance correlation (`energy::dcor()` in R, `dcor` in Python) for arbitrary dependence.

### 3. Correlation Heatmap Design
Five principles: (1) diverging palette centred at zero (RdBu, coolwarm); (2) annotate cells with r values (double encoding: colour + number); (3) reorder by hierarchical clustering to group correlated variables; (4) show only the lower triangle (the matrix is symmetric); (5) fix colour scale to [-1, 1] always. R: `ggcorrplot::ggcorrplot()` or `corrplot::corrplot()`. Python: `sns.heatmap(mask=np.triu(), annot=True, vmin=-1, vmax=1)`.

### 4. Pairs Plots (Scatterplot Matrices)
Combine scatter plots (lower triangle), histograms/density (diagonal), and r values (upper triangle) in one figure. R: `GGally::ggpairs()` with `lower`, `diag`, `upper` customisation and `color = group`. Python: `sns.pairplot(hue=group, diag_kind="kde")`. Scale poorly beyond ~8 variables; use correlation heatmap to identify strongest pairs first, then drill down.

### 5. Categorical Association
For two categorical variables, the visual equivalent of a chi-squared test is a 100% stacked bar (proportions) or balloon plot (counts, size ∝ count). If all bars look identical → independent. Differences → association. Quantify with Cramér's V = √(χ²/(n·min(r-1, c-1))), ranging from 0 (independent) to 1 (perfect association). R: `chisq.test()`. Python: `scipy.stats.chi2_contingency()`.

### 6. Correlation ≠ Causation
Three sources of spurious correlation: **confounders** (a third variable causes both — ice cream and drowning are both caused by summer heat), **reverse causation** (Y causes X, not X causes Y), **coincidence** (random co-trend in finite samples — Nicolas Cage films and pool drownings). Correlation establishes association; only controlled experiments or careful causal inference (DAGs, instrumental variables, difference-in-differences) establish causation.

### References
- Anscombe, F. J. (1973). Graphs in Statistical Analysis. *The American Statistician*, 27(1).
- Friendly, M. (2002). Corrgrams. *The American Statistician*, 56(4).
- Pearl, J. (2009). *Causality*, 2nd ed.
