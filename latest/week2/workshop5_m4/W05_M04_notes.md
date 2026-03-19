# Workshop 5 · Module 4 — Course Notes
## Heatmaps & Clustered Displays

### 1. The Heatmap as a Multivariate Display
A heatmap encodes a matrix of values (rows × columns) as coloured cells. Rows typically represent observations (samples, genes, customers); columns represent variables (features, time points, metrics); colour intensity encodes the value. Without clustering, patterns are hidden by arbitrary row/column ordering. The heatmap's power comes from reordering rows and columns so that similar profiles are adjacent, revealing block patterns.

### 2. Hierarchical Clustering and Dendrograms
Hierarchical clustering builds a tree (dendrogram) by iteratively merging the two most similar items. The dendrogram shows the merge sequence and distances. Common linkage methods: **Ward** (minimises within-cluster variance — usually best for balanced clusters), **complete** (maximum pairwise distance — tends to produce compact clusters), **average** (mean pairwise distance — intermediate). Distance metrics: Euclidean (for continuous), correlation (for profile similarity), Manhattan (for sparse data). The dendrogram attached to the heatmap serves as both a clustering visualisation and a reordering mechanism.

### 3. Z-Score Normalisation
When rows have different baseline levels (e.g., gene A is always high, gene B always low), raw values obscure within-row patterns. Z-scoring per row: z_ij = (x_ij − x̄_i) / s_i. This centres each row at 0 with unit variance, so colour now encodes "how many SDs above/below this row's mean." Use z-scoring with a diverging palette (RdBu centred at 0). Without z-scoring, use a sequential palette (YlOrRd, viridis). For correlation matrices (already on [-1,1] scale), no z-scoring needed — just fix the colour scale to [-1,1].

### 4. Five Design Principles
(1) **Diverging palette** for deviation data (centred at reference value), **sequential** for magnitude. (2) **Cluster** both rows and columns (Ward/complete linkage) to reveal block structure. (3) **Annotate cells** with values if the matrix is small (≤15×15). (4) **Z-score rows** when variables have different scales. (5) **Add annotation tracks** (colour sidebars for row/column metadata).

### 5. Package Ecosystem
**R**: `pheatmap` is the most popular single-function heatmap (auto-dendrograms, annotation, z-scoring via `scale="row"`). `ComplexHeatmap` (Bioconductor) is the publication-quality tool: multi-panel heatmaps, multiple annotation tracks, row/column splits, integration with genomic data. **Python**: `sns.clustermap()` is the seaborn equivalent (auto-dendrograms, `standard_scale=0` for z-scoring, `row_colors` for annotation sidebar). For manual control: `scipy.cluster.hierarchy.linkage()` + `dendrogram()` + `ax.imshow()`.

### 6. When to Use Heatmaps
Sweet spot: 5–50 rows × 5–50 columns. For 2 variables → scatter. For 1 variable over time → line chart. For >500 rows → aggregate first (mean per group) then heatmap. Correlation matrices are an ideal use case (always square, symmetric, bounded [-1,1]).

### References
- Wilkinson, L. & Friendly, M. (2009). The History of the Cluster Heat Map. *The American Statistician*, 63(2).
- Gu, Z. et al. (2016). ComplexHeatmap. *Bioinformatics*, 32(18).
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Ch. 6.
