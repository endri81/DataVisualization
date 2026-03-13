# Workshop 1 · Module 1 — Homework
## "Always Plot Your Data" Exercise

**Due**: Before Workshop 1, Module 3  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Objective

Demonstrate empirically why summary statistics are an inadequate substitute
for visualization, and practise producing identical analyses in both R and
Python.

---

### Part A — Anscombe Replication (30 points)

1. Load Anscombe's quartet using the built-in dataset in R (`anscombe`) and
   Python (`seaborn.load_dataset("anscombe")`).

2. Compute the following summary statistics for each of the four datasets:
   mean of x, mean of y, standard deviation of x and y, Pearson correlation,
   and the OLS regression coefficients (intercept and slope).

3. Present the statistics in a single, well-formatted table (one per
   language). Verify that all four datasets yield approximately identical
   values.

4. Produce a 2×2 faceted scatterplot with regression lines overlaid. Use
   `facet_wrap()` in ggplot2 and `sns.lmplot()` with `col_wrap=2` in seaborn.

5. In 150 words, explain *which structural feature of the data* each dataset
   reveals that summary statistics miss. Reference Anscombe (1973).

---

### Part B — Datasaurus Extension (40 points)

1. Load the Datasaurus Dozen dataset:
   - R: `datasauRus::datasaurus_dozen`
   - Python: download the TSV from the datasauRus GitHub repository

2. Verify that all 13 datasets share the same first-order statistics (means,
   SDs, correlation). Present a summary table.

3. Produce a faceted grid of all 13 datasets (≤5 columns). Each panel should
   be a scatterplot with no axis labels (to maximise the data-ink ratio).

4. Select **three** datasets from the Dozen and, for each:
   a. Describe the visual pattern you observe (e.g., "linear", "circular",
      "star-shaped").
   b. Propose a real-world scenario where data might naturally assume that
      shape.
   c. Explain whether a linear regression model would be appropriate.

---

### Part C — Find a "Lie" in the Wild (30 points)

1. Find one published visualization (from news media, a corporate report, or
   social media) that has a **lie factor > 1.05 or < 0.95**.

2. Include a screenshot or URL of the original.

3. Calculate the approximate lie factor. Show your working.

4. Redesign the chart in either R or Python so that the lie factor ≈ 1.0.

5. In 100 words, explain what design decision created the distortion and how
   your redesign corrects it.

---

### Submission Checklist

- [ ] PDF report (max 4 pages, including all figures and tables)
- [ ] `W01_M01_homework.R` — complete, commented R script
- [ ] `W01_M01_homework.py` — complete, commented Python script
- [ ] All figures exported as PNG (≥150 dpi)
- [ ] Screenshot/URL of the "wild" visualization for Part C

---

### Grading Rubric

| Criterion | Excellent (90–100%) | Good (70–89%) | Needs Work (<70%) |
|-----------|--------------------|--------------|--------------------|
| Statistical accuracy | All values correct, tables well-formatted | Minor rounding issues | Incorrect computations |
| Visualization quality | Clean, labelled, publication-ready | Functional but rough | Missing labels, hard to read |
| Code quality | Commented, reproducible, idiomatic | Runs but poorly structured | Does not execute |
| Written analysis | Precise, references literature | Adequate but vague | Missing or superficial |
| Lie factor exercise | Correctly computed, strong redesign | Approximate but valid | Incorrect or missing |
