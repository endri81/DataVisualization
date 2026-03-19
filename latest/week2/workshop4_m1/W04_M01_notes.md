# Workshop 4 · Module 1 — Course Notes
## Tukey's EDA Philosophy

### 1. Confirmatory vs Exploratory Data Analysis
John W. Tukey (1977) distinguished two complementary approaches to data analysis. **Confirmatory Data Analysis (CDA)** starts with a hypothesis, collects data, and tests the hypothesis using statistical inference (p-values, confidence intervals). **Exploratory Data Analysis (EDA)** starts with the data, visualises patterns, and generates hypotheses for subsequent testing. Most statistics courses emphasise CDA; Tukey argued that EDA must come first — you cannot test a hypothesis you haven't yet discovered.

### 2. The Detective Metaphor
Tukey likened the data analyst to a detective: (1) look at the data (inspect the scene), (2) find patterns (gather evidence), (3) form hypotheses (develop theories), (4) check residuals (look for what's left), (5) iterate (follow new leads). The key insight is that EDA is iterative: each plot raises new questions that demand new plots.

### 3. Tukey's Original Toolkit
Six methods from the 1977 book: **stem-and-leaf** (preserves every value while showing shape — replaced by histograms for large n), **box-and-whisker** (5-number summary + outliers — still a core EDA tool), **residual plots** (what's left after fitting a model — foundation of diagnostics), **median polish** (robust decomposition of two-way tables), **re-expression** (log, sqrt, reciprocal transforms to simplify patterns), **smoothing** (running medians — evolved into LOESS and GAM).

### 4. Letter-Value Plots
For large n (>200), standard boxplots waste information by showing only 5 quantiles. The letter-value plot (Hofmann, Wickham & Kafadar, 2017) extends the box with nested quantile boxes: M (median), F (fourths/quartiles), E (eighths), D (sixteenths), C (thirty-seconds). This reveals tail behaviour invisible in standard boxplots. In R: `lvplot::geom_lv()` or `ggplot2::geom_boxplot()` with extended whiskers. In Python: `seaborn.boxenplot()`.

### 5. The 4-Plot
Tukey's diagnostic panel for univariate data: (a) **run sequence** — detect shifts, trends, or cycles by plotting values against index; (b) **lag-1 plot** — detect autocorrelation by plotting Y(i) vs Y(i+1); (c) **histogram** — assess shape (unimodal, skewed, bimodal); (d) **normal Q-Q plot** — assess normality, with departures at tails indicating heavy/light tails or skewness. If all four look benign, parametric methods are appropriate.

### 6. Modern EDA Workflow
Four iterative phases: (1) **Import & Inspect** — `dim()`, `glimpse()`, `summary()` in R; `.shape`, `.info()`, `.describe()` in Python; or automated reports via `skimr::skim()` / `ydata-profiling`. (2) **Clean & Transform** — handle missing values, convert types, flag outliers. (3) **Visualise & Explore** — univariate (histograms, boxplots), bivariate (scatter, grouped box), multivariate (facets, heatmaps). (4) **Document & Communicate** — record findings, formulate questions, plan next steps.

### References
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Hofmann, H., Wickham, H. & Kafadar, K. (2017). Letter-value plots. *JCGS*.
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed., Chapters 2, 10.
