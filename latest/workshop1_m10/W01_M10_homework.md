# Workshop 1 · Module 10 — Homework (Final Lab)
## Comparative EDA: Google Play Store

**Due**: Before Workshop 2, Module 1  
**Format**: PDF report (max 8 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### The Assignment

Produce a **complete EDA of the Google Play Store dataset** in both R and
Python. Every chart must appear in both languages, applying the principles
from Modules 1–9.

---

### Required Charts (60 points, 10 per chart)

Produce the following six charts in **both R and Python** (12 total):

1. **Horizontal bar**: Top 10 categories by count.
   Sort descending, direct-label each bar, remove non-data spines.

2. **Histogram**: Rating distribution with mean reference line.
   40 bins, dashed red mean line, annotated mean value.

3. **Scatterplot**: Reviews (log-scaled x) vs Rating, coloured by Type.
   Alpha = 0.3, legend or direct labels, Tufte cleanup.

4. **Boxplot**: Rating split by Type (Free vs Paid).
   Notched, coloured fills, mean points overlaid as red diamonds.

5. **Line chart**: Number of apps added per year (2010–2018), by Type.
   Direct labels at endpoints (no legend box).

6. **Stacked bar**: Content Rating × Type.
   Two-colour fill (Free/Paid), readable x-axis labels.

---

### Dashboard (20 points)

Combine all six charts into a single six-panel dashboard:
- R: use `patchwork` — `(p1 | p2 | p3) / (p4 | p5 | p6)`
- Python: use `GridSpec(2, 3)`

Add an overall title, subtitle, and panel labels (a)–(f).
Export as PDF (vector) and PNG (300 dpi).

---

### Written Analysis (20 points)

In 400 words (max), address:

1. **Key findings** (100 words): What are the 3 most interesting patterns
   visible in your dashboard?

2. **Design decisions** (150 words): For each of the six charts, name one
   specific Module 1–9 principle you applied and explain how it improved
   the chart.

3. **R vs Python comparison** (150 words): Which language felt more
   natural for this task? Which produced cleaner default output? Where
   did you need more manual code? Would you use different languages for
   different chart types?

---

### Submission Checklist

- [ ] `W01_M10_homework.R` — all 6 charts + dashboard, commented
- [ ] `W01_M10_homework.py` — same, commented
- [ ] 12 individual chart PNGs (6 R + 6 Python, 300 dpi)
- [ ] 2 dashboard files (R PDF + Python PDF)
- [ ] PDF report (max 8 pages) with all charts embedded and analysis text
