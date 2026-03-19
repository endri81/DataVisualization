# Workshop 5 · Module 3 — Course Notes
## Dimensionality Reduction Visualization: PCA, t-SNE, UMAP

### 1. Why Reduce Dimensions?
Standard scatter plots fail beyond 2–3 variables. Dimension reduction algorithms project high-dimensional data into 2D (or 3D) while preserving important structure. The goal is not to discard information but to find the viewing angle that reveals the most structure — clusters, gradients, outliers — in a plottable space.

### 2. PCA (Principal Component Analysis)
PCA finds orthogonal linear combinations (principal components) that capture maximum variance. PC1 captures the most variance, PC2 the second most (orthogonal to PC1), etc. **Scree plot**: bar chart of variance explained per component + cumulative line. Keep components until the elbow (diminishing returns) or until cumulative variance exceeds 80%. **Biplot**: scores (observations as points) + loadings (original variables as arrows). Arrow direction shows which PC a variable contributes to; arrow length shows the strength; angle between arrows approximates correlation (cos θ ≈ r). Always scale variables first (`scale.=TRUE` in R, `StandardScaler()` in Python). PCA is linear, deterministic, and fast (O(np²)). R: `prcomp() + ggfortify::autoplot()`. Python: `sklearn.decomposition.PCA`.

### 3. t-SNE (t-distributed Stochastic Neighbor Embedding)
t-SNE (van der Maaten & Hinton, 2008) preserves local neighbourhoods: nearby points in high-D stay nearby in 2D. Excellent at revealing clusters. Key limitations: (1) inter-cluster distances are meaningless — cluster size and gap width are artefacts; (2) axes have no interpretation (unlike PCA); (3) stochastic — different runs give different layouts; (4) slow (O(n²)) for large datasets. The **perplexity** hyperparameter (5–50) controls neighbourhood size; always try 2–3 values and show in a panel. R: `Rtsne::Rtsne()`. Python: `sklearn.manifold.TSNE`.

### 4. UMAP (Uniform Manifold Approximation and Projection)
UMAP (McInnes et al., 2018) is conceptually similar to t-SNE but preserves both local and global topology, runs faster (O(n log n)), and produces more stable layouts. Key hyperparameters: `n_neighbors` (5–50, like perplexity) and `min_dist` (0.0–1.0, controls cluster tightness). Preferred over t-SNE for large datasets (>50K rows) and when global structure matters. R: `umap::umap()`. Python: `umap-learn`.

### 5. Decision Framework
Start with PCA (interpretable, fast). If PC1+PC2 capture <50% variance, the data has complex nonlinear structure → try t-SNE or UMAP. For understanding variable contributions → PCA biplot. For discovering clusters → t-SNE or UMAP. For large n → UMAP. For reproducibility → PCA (deterministic). Best practice: always show PCA alongside t-SNE/UMAP for comparison.

### 6. Five Pitfalls
(1) Forgetting to scale: variables with larger variance dominate PCA. (2) Over-interpreting t-SNE distances: only local structure is preserved. (3) Single perplexity: always try multiple values. (4) Treating PCs as real variables: they're linear combinations; interpret via loadings. (5) Running t-SNE on >50K rows: use UMAP or subsample.

### References
- Jolliffe, I. T. (2002). *Principal Component Analysis*, 2nd ed. Springer.
- van der Maaten, L. & Hinton, G. (2008). Visualizing Data using t-SNE. *JMLR*, 9.
- McInnes, L. et al. (2018). UMAP. arXiv:1802.03426.
- Wattenberg, M. et al. (2016). How to Use t-SNE Effectively. *Distill*.
