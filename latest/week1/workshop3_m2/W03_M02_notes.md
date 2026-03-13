# Workshop 3 · Module 2 — Course Notes
## Distributions: Boxplots, Violins & Beeswarm

### 1. Boxplot Anatomy
The boxplot encodes the five-number summary: minimum (lower whisker), Q1 (25th percentile, box bottom), median (Q2, bold line), Q3 (75th percentile, box top), maximum (upper whisker). Whiskers extend to Q1 − 1.5·IQR and Q3 + 1.5·IQR respectively; points beyond are plotted individually as outliers. The Interquartile Range (IQR = Q3 − Q1) measures spread. Notched boxplots add a confidence interval on the median: non-overlapping notches indicate significantly different medians at approximately the 95% level.

### 2. The Shape-Blindness Problem
A boxplot compresses all distributional information into five numbers. Three fundamentally different distributions — unimodal, bimodal, and right-skewed — can produce nearly identical boxes. This is the central limitation: boxplots are efficient summaries but poor shape communicators. The solution is to always pair them with jitter (for small n) or violin (for large n).

### 3. Violin Plots
A violin plot mirrors a KDE on both sides of a vertical axis, revealing the full density shape. It shows bimodality, skewness, and multimodality that boxplots hide. Best practice: embed a narrow boxplot inside the violin (`geom_violin() + geom_boxplot(width=0.1)`) for both shape and summary. Split violins (`split=TRUE` in seaborn) place two groups side by side within each category.

### 4. Strip, Jitter, and Beeswarm
**Strip/jitter** (`geom_jitter()` / `sns.stripplot()`) shows every individual observation with random horizontal noise. Works for n < 200 per group. **Beeswarm** (`ggbeeswarm::geom_beeswarm()` / `sns.swarmplot()`) stacks points systematically to reveal local density without randomness. Works for n < 500. Both are superior to boxplots for small samples because no information is hidden.

### 5. Raincloud Plots
The raincloud plot (Allen et al., 2019) combines half-violin (density shape), narrow boxplot (summary), and jitter (raw data) into a single display. It is the current gold standard for distribution visualisation in scientific publications. In R: `ggrain::geom_rain()`. In Python: manual composition using half-violin fill + boxplot + scatter.

### References
- Allen, M. et al. (2019). Raincloud plots. *Wellcome Open Research*, 4, 63.
- Hintze, J. L. & Nelson, R. D. (1998). Violin plots. *The American Statistician*.
- Wickham, H. & Stryjewski, L. (2011). 40 years of boxplots. *The American Statistician*.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapters 7, 9.
