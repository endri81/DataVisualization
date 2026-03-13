# Workshop 1 · Module 3 — Homework
## Perception-Driven Design

**Due**: Before Workshop 1, Module 5  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Pre-Attentive Pop-Out (30 points)

1. Using the Google Play Store dataset (`googleplaystore.csv`), create a
   scatter plot of Rating (y) vs Reviews (x, log-scaled) for all apps.

2. Colour all points grey (#AAAAAA), then highlight a single category of
   your choice (e.g., "GAME") in a pre-attentive accent colour (#E53935).

3. Produce this "grey + accent" plot in both R and Python.

4. In 100 words, explain why this design produces pop-out and what
   insight the highlighted category reveals compared to the background.

---

### Part B — Gestalt Application (40 points)

1. Using the Netflix dataset (`netflix.csv`), create three charts that
   each leverage a different Gestalt law:
   - **Proximity**: Use faceting to compare content types (Movie vs TV Show)
   - **Enclosure**: Use a shaded band on a time series of content additions
     to highlight a specific year range
   - **Connection**: Use lines to connect paired data points (e.g., average
     duration by genre for Movies vs TV Shows in a slope chart)

2. Produce all three charts in both R and Python (6 total).

3. For each chart, write 50 words identifying which Gestalt law is active
   and how it aids interpretation.

---

### Part C — Channel Selection (30 points)

1. Consider a dataset with four variables: Revenue (quantitative),
   Region (nominal, 4 levels), Quarter (ordinal, 4 levels), and Growth
   Rate (quantitative).

2. Design two charts that encode all four variables. In one chart, assign
   Revenue to position (best channel); in the other, assign Revenue to
   area (weaker channel). Keep the other variable-to-channel mappings
   identical.

3. Produce both charts in R or Python.

4. In 150 words, explain which chart makes it easier to compare Revenue
   across Regions, and why, referencing Cleveland & McGill (1984).

---

### Submission Checklist

- [ ] PDF report (max 4 pages)
- [ ] `W01_M03_homework.R` — all R code, commented
- [ ] `W01_M03_homework.py` — all Python code, commented
- [ ] All figures exported as PNG (≥150 dpi)
