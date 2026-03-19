# Workshop 4 · Module 5 — Course Notes
## Outlier Detection & Visual Diagnostics

### 1. Outlier Taxonomy
Three types require different detection strategies: **Univariate** outliers are extreme on a single variable (detected by IQR fences or z-scores). **Multivariate** outliers are normal on each variable individually but extreme in their joint distribution (detected by Mahalanobis distance). **Contextual** outliers are normal globally but anomalous in local context — e.g., a warm January day is only anomalous because it's January (detected by time-series decomposition or domain knowledge).

### 2. IQR Fences (Tukey, 1977)
The boxplot's whiskers extend to Q1 − 1.5·IQR and Q3 + 1.5·IQR. Points beyond these fences are flagged as potential outliers. The IQR method is **robust**: quartiles are resistant to extreme values, unlike the mean and SD used in z-scores. For approximately normal data, the 1.5·IQR fence corresponds to roughly ±2.7σ, catching about 0.7% of observations. Use 3·IQR for "far outliers."

### 3. Z-Score
z = (x − x̄) / s. Points with |z| > 2 (or > 3 for stricter thresholds) are flagged. **Problem**: the mean and SD are themselves distorted by the outliers you're trying to detect (masking effect). For skewed distributions, the z-score is unreliable. Prefer IQR for EDA; use z-scores only after confirming approximate normality.

### 4. Mahalanobis Distance
Measures the distance from a point to the centre of the multivariate distribution, accounting for correlation structure. The threshold is based on the χ² distribution with p degrees of freedom. A robust version uses the Minimum Covariance Determinant (MCD) estimator instead of the sample covariance. R: `mahalanobis()` + `robustbase::covMcd()`. Python: `scipy.spatial.distance.mahalanobis` + `sklearn.covariance.EllipticEnvelope`.

### 5. Regression Diagnostics: Leverage, Influence, Cook's D
**Leverage** measures how far a point's x-value is from the centre of the x-distribution (hat matrix diagonal). **Influence** measures how much the fitted model changes when the point is removed. **Cook's Distance** combines leverage and residual: D_i = (r_i² · h_i) / (p · (1-h_i)²). Threshold: D > 4/n. The four diagnostic plots: (a) residuals vs fitted (linearity, homoscedasticity), (b) Q-Q of residuals (normality), (c) scale-location (constant variance), (d) Cook's D (influence). R: `plot(lm())` produces all four. Python: `statsmodels.get_influence()`.

### 6. What to Do with Outliers
Cause determines action: **data entry error** → correct or remove; **measurement error** → flag, run sensitivity analysis; **rare but real** → keep, report separately; **different population** → segment, analyse apart; **influential on model** → fit with and without, report both. Never delete without justification. The "fit with and without" protocol: if conclusions change when influential points are removed, the finding is fragile — report this honestly.

### References
- Tukey, J. W. (1977). *Exploratory Data Analysis*, Ch. 2.
- Rousseeuw, P. J. & van Zomeren, B. C. (1990). Unmasking multivariate outliers. *JASA*, 85(411).
- Cook, R. D. (1977). Detection of influential observations. *Technometrics*, 19(1).
