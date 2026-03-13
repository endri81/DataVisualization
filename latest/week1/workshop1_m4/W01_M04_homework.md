# Workshop 1 · Module 4 — Homework
## Color in Practice

**Due**: Before Workshop 1, Module 6  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Palette Selection (30 points)

1. Using the Google Play Store dataset (`googleplaystore.csv`), create
   three charts, each using the correct palette type:

   a. **Sequential**: A heatmap of average Rating by Category (rows) and
      Content Rating (columns). Use `viridis` or `YlGnBu`.

   b. **Diverging**: A bar chart showing each category's average rating
      minus the global mean. Use `RdBu` centred on zero.

   c. **Qualitative**: A scatter plot of Reviews vs Rating coloured by
      the top 5 categories. Use `Set2` or Tableau 10.

2. Produce all three in both R and Python (6 charts total).

3. In 100 words, explain why each palette type is appropriate for its
   chart and what would go wrong with the wrong type.

---

### Part B — Rainbow Audit (30 points)

1. Find one published chart that uses a rainbow (jet) colourmap for
   quantitative data. Include a screenshot or URL.

2. Identify at least one false contour boundary created by the rainbow
   palette.

3. Recreate the chart using the same data structure (or a synthetic
   approximation) in R or Python with `viridis` instead of rainbow.

4. In 100 words, explain how the viridis version changes interpretation
   of the data.

---

### Part C — CVD Simulation & Grey-Accent (40 points)

1. Using the Netflix dataset (`netflix.csv`), create a scatter plot of
   Release Year (x) vs a numeric feature of your choice (y), coloured
   by content type (Movie/TV Show) using a red-green palette
   (e.g., red = Movie, green = TV Show).

2. Simulate deuteranopia:
   - R: `colorspace::deutan(p)`
   - Python: use `colorspacious` or screenshot from coblis.org

3. Show that the two categories become indistinguishable under CVD.

4. Redesign the chart using the **grey + accent** strategy:
   - TV Shows in grey, Movies highlighted in blue (or vice versa)
   - Add a shape channel as insurance

5. In 150 words, explain why the redesign is both more accessible and
   more effective for storytelling, referencing pre-attentive pop-out
   (Module 3) and the grey-accent principle (Module 4).

---

### Submission Checklist

- [ ] PDF report (max 4 pages)
- [ ] `W01_M04_homework.R` — all R code, commented
- [ ] `W01_M04_homework.py` — all Python code, commented
- [ ] All figures exported as PNG (≥150 dpi)
- [ ] Screenshot/URL for rainbow audit (Part B)
