# Workshop 2 · Module 3 — Homework
## Aesthetics & Geometries Mastery

**Due**: Before Workshop 2, Module 5
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — Multi-Aesthetic Encoding (30 points)
Using the Google Play Store dataset, create a scatter plot encoding four variables: Reviews (x, log), Rating (y), Type (colour), and Installs (size). Produce in both R (ggplot2) and Python (plotnine or matplotlib). In 100 words, explain your channel-to-variable mapping using Cleveland & McGill ranking.

### Part B — Geom Layering (30 points)
Produce three composite charts in both R and Python:
1. `geom_boxplot() + geom_jitter()` — Rating by Content Rating (top 4)
2. `geom_col() + geom_errorbar()` — Mean Rating ± SE by Category (top 8)
3. Lollipop chart — App count per Category (top 10), using `geom_segment() + geom_point()`

### Part C — Overplotting (20 points)
Using Reviews (x) vs Rating (y) from the Google Play Store (all 10K+ rows):
1. Show the overplotting problem (raw scatter, no alpha)
2. Apply three fixes: alpha, jitter+alpha, geom_hex
3. In 100 words, explain which fix is best for this dataset and why.

### Part D — Dumbbell Chart (20 points)
Create synthetic data for 6 app categories with mean ratings in 2020 and 2024. Produce a dumbbell chart in both R and Python showing the change. Use grey connector, blue for 2020, red for 2024.

### Submission Checklist
- [ ] `W02_M03_homework.R` + `W02_M03_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
