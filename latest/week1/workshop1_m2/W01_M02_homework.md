# Workshop 1 · Module 2 — Homework
## Tufte Principles Applied

**Due**: Before Workshop 1, Module 4  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Data-Ink Ratio Erasure (40 points)

1. Using the Google Play Store dataset (`googleplaystore.csv`), create a
   bar chart of the top 10 app categories by count.

2. Produce **four versions** of the same chart, each progressively removing
   non-data ink — following the erasure sequence demonstrated in lecture:
   - Version 1: default ggplot2/matplotlib output
   - Version 2: remove background fill and border
   - Version 3: remove gridlines, flip to horizontal
   - Version 4: Tufte-style — direct labels, minimal spines, range-frame

3. Create all four versions in both R and Python (8 charts total).

4. In 200 words, estimate the data-ink ratio of Version 1 vs Version 4.
   You may approximate visually (what fraction of ink carries data?).

---

### Part B — Lie Factor Audit (30 points)

1. Find **two** published charts (news, corporate, or social media) that
   exhibit a lie factor > 1.05. Include screenshots or URLs.

2. For each chart:
   a. Identify the source of distortion (truncated axis, area encoding,
      perspective, etc.)
   b. Calculate the approximate lie factor. Show working.
   c. Produce an honest redesign in R **or** Python.

3. In 150 words per chart, explain the correction and its effect on
   interpretation.

---

### Part C — Small Multiples (30 points)

1. Using the Google Play Store dataset, select a continuous variable
   (e.g., Rating) and a categorical variable with 6–8 levels
   (e.g., Content Rating or top categories).

2. Create a small-multiples display:
   - R: use `facet_wrap()` with `scales = "fixed"`
   - Python: use `plt.subplots()` with `sharey=True`

3. Apply Tufte-style formatting to the small multiples:
   - Remove heavy grids
   - Use minimal spines
   - Keep the same scale across panels

4. In 100 words, describe one pattern visible in the small multiples
   that would be hidden in a single overlaid chart.

---

### Submission Checklist

- [ ] PDF report (max 4 pages)
- [ ] `W01_M02_homework.R` — all R code, commented
- [ ] `W01_M02_homework.py` — all Python code, commented
- [ ] All figures exported as PNG (≥150 dpi)
- [ ] Screenshots/URLs for lie-factor audit (Part B)
