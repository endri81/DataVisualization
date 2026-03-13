# Workshop 3 · Module 1 — Course Notes
## Distributions: Histograms, Density & Ridgeline

### 1. Histograms and Bin Width
A histogram partitions a continuous variable into bins and counts observations per bin. The critical parameter is bin width (or equivalently, the number of bins). Too few bins hides multimodality; too many creates noise from sampling variability. Two automatic rules provide starting points: Sturges' rule (k = 1 + log₂n, good for roughly normal data) and Freedman-Diaconis (h = 2·IQR·n^{-1/3}, robust to skewness). In practice, always try 2–3 bin counts and inspect visually.

Three histogram variants serve different purposes: **frequency** (raw counts, intuitive but scale-dependent), **density** (area sums to 1, comparable across different sample sizes), and **cumulative** (approximates the ECDF, useful for percentile statements like "50% of apps are rated below 4.2").

### 2. Kernel Density Estimation
KDE replaces the histogram's hard bins with soft kernels (typically Gaussian). At each data point, a symmetric kernel is placed; the sum of all kernels (normalized) produces a smooth density curve. The bandwidth parameter controls smoothness: too narrow undersmooths (noise), too wide oversmooths (hides modes). Silverman's rule-of-thumb bandwidth works for unimodal distributions but may oversmooth multimodal data. In R, `geom_density(adjust = ...)` scales the default bandwidth; in Python, `gaussian_kde(bw_method = ...)` or `sns.kdeplot(bw_adjust = ...)`.

### 3. Histogram + KDE Overlay
The most informative single-variable display combines a density-scaled histogram with a KDE overlay and reference lines for mean and median. The histogram shows the raw binned structure; the KDE shows the smooth shape; the mean/median gap reveals skewness direction (mean < median = left-skewed).

### 4. Grouped Distributions
For 2–3 groups, overlaid density curves with `fill = group, alpha = 0.2` work well. For 4+ groups, overlaid densities become unreadable (too much overlap). **Ridgeline plots** (joy plots) solve this by stacking densities vertically with slight overlap, using position to separate groups. In R: `ggridges::geom_density_ridges()`. In Python: manual vertical offset loop or the `joypy` package.

### References
- Silverman, B. W. (1986). *Density Estimation for Statistics and Data Analysis*. Chapman & Hall.
- Wickham, H. (2016). *ggplot2*, Chapter 5.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapters 7–9.
