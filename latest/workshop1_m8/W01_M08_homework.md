# Workshop 1 · Module 8 — Homework
## R Fundamentals

**Due**: Before Workshop 1, Module 10  
**Format**: R script (.R) + exported PNG figures  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Environment Verification (10 points)

1. Open RStudio and create a new R script called `W01_M08_homework.R`.
2. Print your R version (`R.version.string`) and the tidyverse version
   (`packageVersion("tidyverse")`).
3. Load the Google Play Store dataset: `apps <- readr::read_csv("googleplaystore.csv")`
4. Print `dim(apps)`, `glimpse(apps)`, and `sum(is.na(apps))`.

---

### Part B — Data Types Audit (20 points)

1. For each column in the Google Play Store dataset, identify the R
   data type using `sapply(apps, class)`.
2. Identify at least two columns where the type is incorrect for
   visualization (e.g., Reviews stored as character instead of numeric).
3. Fix the types:
   - Convert Reviews to numeric: `apps$Reviews <- as.numeric(apps$Reviews)`
   - Convert Installs to a clean numeric (remove commas and "+")
4. Show `str(apps)` before and after the fixes.

---

### Part C — Base R Graphics (50 points)

Using the cleaned dataset from Part B, produce the following four charts
using **base R only** (no ggplot2):

1. **Scatterplot**: `plot(log10(Reviews), Rating)` with `pch = 16`,
   `col = adjustcolor("steelblue", 0.4)`, and a LOESS smoother
   (`lines(lowess(...))`).

2. **Histogram**: `hist(Rating, breaks = 40)` with a vertical line at
   the mean and a legend showing the mean value.

3. **Bar chart**: `barplot(sort(table(Category))[20:30])` — the top 10
   categories by count, displayed horizontally with `horiz = TRUE`.

4. **Boxplot**: `boxplot(Rating ~ Type)` for Free vs Paid apps, with
   mean points overlaid and `notch = TRUE`.

Export each as PNG at 150 dpi using `png()` ... `dev.off()`.

---

### Part D — Multi-Panel Layout (20 points)

1. Arrange all four charts from Part C in a single 2×2 figure using
   `par(mfrow = c(2, 2))`.
2. Customise margins with `par(mar = c(4, 4, 3, 1))`.
3. Export as a single PNG at 300 dpi, 8×6 inches.
4. Remember to reset par after: `par(old_par)`.

---

### Submission Checklist

- [ ] `W01_M08_homework.R` — complete, commented
- [ ] `scatter.png`, `hist.png`, `bar.png`, `box.png` — individual charts
- [ ] `multipanel.png` — 2×2 layout
