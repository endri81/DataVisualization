# Workshop 4 · Module 7 — Course Notes
## EDA Case Study: Google Play Store

### 1. Dataset Overview
The Google Play Store dataset (Kaggle, 2018) contains 10,841 app records with 13 variables: App (name), Category (33 levels), Rating (1–5), Reviews (0–78M), Size, Installs, Type (Free/Paid), Price, Content Rating, Genres, Last Updated, Current Ver, and Android Ver. It is a messy real-world dataset with duplicates, mixed types, missing values, and inconsistent formatting — ideal for practising the full EDA pipeline.

### 2. Cleaning Audit Trail
Starting with 10,841 rows: (1) remove 1,181 duplicates on App name → 9,660; (2) convert Reviews, Installs, Price to numeric (handling +, comma, $ symbols) → 9,660 (but with new NAs from coercion failures); (3) drop 293 rows with missing Rating → 9,367; (4) filter to Free/Paid only and valid Rating range [1,5] → 9,360 final rows. Each step is documented with row counts and justification.

### 3. Nine-Panel Dashboard
The dashboard applies one technique per panel, each traced to a specific module: (a) missing % bar (M04), (b) Rating histogram with mean/median lines (M01), (c) violin by Type (W03-M02), (d) sorted category bar (W03-M03), (e) scatter + trend (M06), (f) correlation heatmap (M06), (g) pointrange with CI (W03-M07), (h) waffle for Free/Paid split (W03-M05), (i) Q-Q plot (M01). This demonstrates that EDA is not a single technique but an orchestration of the full chart vocabulary.

### 4. Four Key Findings
**Finding 1**: Rating is left-skewed with a ceiling effect at 5.0 (mean=4.17, median=4.30). Use Spearman over Pearson, median over mean. **Finding 2**: Free apps dominate at 93%. Any Free vs Paid comparison must account for this massive class imbalance. **Finding 3**: Reviews correlate weakly with Rating (ρ=0.18) — popularity ≠ quality. Log transform is essential given 4 orders of magnitude range. **Finding 4**: Category differences in mean Rating are small and CIs overlap — category is a weak predictor of quality.

### 5. EDA Report Structure
Every EDA report follows seven sections: (1) Data Description, (2) Cleaning Audit, (3) Missingness Audit, (4) Univariate EDA, (5) Bivariate EDA, (6) Key Findings (numbered with evidence + implication), (7) Limitations. This structure applies to every dataset in this course and in professional practice.

### References
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed., Ch. 10.
- Peng, R. (2016). *Exploratory Data Analysis with R*.
