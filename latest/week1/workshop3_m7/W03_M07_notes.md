# Workshop 3 · Module 7 — Course Notes
## Uncertainty: Error Bars, Confidence & Gradient

### 1. Why Visualize Uncertainty
Bar charts of means without error bars imply a precision that does not exist. Two means may look different (e.g., 4.18 vs 4.22) but with overlapping 95% confidence intervals, the difference is likely not statistically significant. The rule: **every point estimate needs an uncertainty interval**.

### 2. Three Error Metrics
**Standard Error (SE)** = SD/√n. It measures the precision of the sample mean as an estimate of the population mean. Smaller with larger n. **95% Confidence Interval** = mean ± 1.96·SE. It provides a range likely containing the true population mean. Non-overlapping CIs suggest a significant difference (approximately). **Standard Deviation (SD)** = spread of individual observations. It describes variability in the data, not precision of the mean. Always label which metric you are showing.

### 3. Pointrange
Pointrange plots (a point for the mean + lines extending to CI bounds) are superior to bar+errorbar for comparing group means. They eliminate the misleading filled-bar area and focus attention on the estimate and its precision. In R: `stat_summary(fun.data = mean_cl_normal, geom = "pointrange")`. In Python: `ax.errorbar(fmt="o", capsize=5)`.

### 4. Confidence Ribbons
For time series, shade the region between CI bounds around the trend line using `geom_ribbon()` (R) or `ax.fill_between()` (Python). Two-layer ribbons work well: lighter shade for 95% CI, darker shade for ±1 SE. ggplot2's `geom_smooth(se = TRUE)` generates CI ribbons automatically.

### 5. Gradient Density Bands
A single CI ribbon has a sharp boundary that implies certainty beyond the edge. Gradient bands solve this by layering multiple ribbons at decreasing alpha with increasing multiples of SE, producing a smooth fade from centre (high probability) to edges (low probability). In R: `ggdist::stat_lineribbon()`. In Python: loop `fill_between()` with decreasing alpha.

### 6. Forest Plots
Forest plots display effect sizes with CIs for multiple studies, with a pooled (summary) estimate at the bottom. A vertical dashed line at zero (or the null effect) serves as reference. If a CI crosses zero, the effect is not significant. Standard in medical and social science meta-analysis. In R: the `forestplot` package or manual `geom_pointrange()`. In Python: manual `ax.errorbar()` loop.

### References
- Cumming, G. (2014). The new statistics. *Psychological Science*, 25(1), 7–29.
- Kay, M. et al. (2016). When (ish) is my bus? *CHI '16*.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 16.
