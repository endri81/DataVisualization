# Workshop 4 · Module 4 — Course Notes
## Missing Data Visualization

### 1. Why Missing Data Matters for Visualization
Most plotting libraries silently drop rows with missing values. ggplot2 prints a warning ("Removed N rows") but still renders the chart without those rows. If missingness is not random (MAR or MNAR), every chart you produce is biased — but you won't know unless you explicitly visualize the missingness itself. Rule: **plot the missingness before any analysis** (Step 0).

### 2. Three Missing Data Mechanisms (Rubin, 1976)
**MCAR** (Missing Completely At Random): missingness is unrelated to any variable, observed or unobserved. Safe to drop rows — no bias. **MAR** (Missing At Random): missingness depends on observed variables (e.g., Paid apps are more likely to have missing Content Rating). Imputable from observed predictors. **MNAR** (Missing Not At Random): missingness depends on the missing value itself (e.g., low-rated apps hide their ratings). Most dangerous — guaranteed bias, no imputation fully corrects it.

### 3. Visualization Tools
**Missingness matrix**: rows × columns, coloured by present/missing. Reveals vertical stripes (one bad column), horizontal bands (bad rows), and block patterns (structured missingness). R: `visdat::vis_miss()`, Python: `msno.matrix()`. **Missing % bar**: sorted horizontal bar of % missing per column with a 5% threshold line. R: `naniar::gg_miss_var()`, Python: `df.isna().mean().plot.barh()`.

### 4. Shadow-Augmented Plots
The shadow matrix creates a parallel Boolean DataFrame recording "is this value missing?" for every cell. `naniar::bind_shadow()` (R) or `df.isna().add_suffix("_NA")` (Python) appends these columns, enabling: colour by missingness in scatter plots, facet histograms by "missing vs present" groups, and test whether distributions differ. If distributions differ between "Y missing" and "Y present" groups, the data is MAR or MNAR.

### 5. Co-occurrence Patterns
**UpSet plots** show which columns go missing together. Cascading missingness (Size missing → Reviews also missing) suggests shared data-entry failures. R: `naniar::gg_miss_upset()`. **Dendrograms** cluster columns by the correlation of their missingness indicators — columns that cluster together tend to go missing in the same rows. Python: `msno.dendrogram()`.

### 6. Visualizing Imputation Effects
Mean imputation creates an artificial spike at the centre of the distribution, shrinking variance. Always overlay before/after histograms to detect distortion. Gold standard: multiple imputation (mice in R, miceforest in Python) which generates multiple plausible datasets and produces correct confidence intervals.

### References
- Rubin, D. B. (1976). Inference and Missing Data. *Biometrika*, 63(3).
- Tierney, N. J. & Cook, D. (2023). naniar. *JSS*, 105(7).
- van Buuren, S. (2018). *Flexible Imputation of Missing Data*, 2nd ed.
