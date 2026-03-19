# Workshop 4 · Module 10 — Course Notes
## Lab: Full EDA on Netflix

### 1. Dataset Challenges
The Netflix dataset (8,807 titles) presents three unique EDA challenges not seen in Google Play Store or e-Car: (1) **multi-valued columns** — `listed_in` contains comma-separated genres, `country` contains comma-separated countries, `cast` contains comma-separated actors. Counting genres requires `separate_rows()` (R) or `.str.split().explode()` (Python) to create one row per value before using `value_counts()`. (2) **Dual-unit duration** — "duration" means minutes for Movies but seasons for TV Shows. Never analyse them together; split into `dur_min` and `seasons`. (3) **MAR missingness** — `director` is 30% missing, overwhelmingly for TV Shows (which have per-episode directors rather than a single show director). This is MAR: missingness depends on the observed variable `type`.

### 2. Nine-Panel Dashboard
(a) Missing % bar — director 30%, country 10%, date_added 1%. (b) Movie/TV donut — 70%/30% split. (c) Releases per year by type — Movies peaked 2017, TV Shows grew steadily through 2021 (the "TV pivot"). (d) Top 10 genres (exploded) — International Movies #1, Dramas #2. (e) Movie duration histogram — near-normal, mean ≈ 100 min. (f) Content rating distribution — TV-MA dominates. (g) Top countries (lollipop) — US 37%, India 14%, long tail. (h) Duration by content rating (boxplot) — R-rated movies tend longer. (i) TV Show seasons — 72% are single-season.

### 3. Four Key Findings
**Finding 1**: Netflix pivoted to TV Shows post-2016 — Movie additions peaked then declined while TV grew. Any time-series analysis must account for this structural break. **Finding 2**: Director is 30% missing (MAR for TV Shows) — analyse director only for Movies. **Finding 3**: Movie duration is near-normally distributed (mean ≈ 100 min) — parametric methods OK. **Finding 4**: Extreme geographic concentration (US 37%, India 14%, top 2 = 51%) — group rare countries into "Other".

### 4. Three Datasets, One Framework
Google Play (10K apps, app marketplace), e-Car (208K loans, consumer finance), and Netflix (8.8K titles, streaming content) all follow the identical seven-section EDA report structure. The dashboard template, cleaning audit, finding format, and missingness protocol are domain-agnostic. Only the variable names and domain context change.

### 5. Workshop 4 EDA Toolkit
After 10 modules, students command: wrangling (dplyr/pandas pipe chains), missingness diagnosis (naniar/missingno, MCAR/MAR/MNAR), outlier detection (IQR, z-score, Mahalanobis, Cook's D), association measurement (Pearson, Spearman, Cramér's V, heatmaps, pairs plots), dashboard composition (patchwork/GridSpec), finding extraction (Finding → Evidence → Implication), and automation (skimr, ydata-profiling, Quarto parameterised reports).

### References
- Netflix Dataset: https://www.kaggle.com/shivamb/netflix-shows
- All W04 module references apply.
