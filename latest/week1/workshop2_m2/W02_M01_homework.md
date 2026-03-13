# Workshop 2 · Module 1 — Homework
## Grammar Decomposition

**Due**: Before Workshop 2, Module 3  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 2 homework (5% of total grade)

---

### Part A — Layer Decomposition (30 points)

1. Find **three** published charts (from news, reports, or academic papers).

2. For each chart, decompose it into the seven grammar layers:

   | Layer | Your Specification |
   |-------|--------------------|
   | Data | (describe the data) |
   | Aesthetics | x = ?, y = ?, color = ?, size = ? |
   | Geometry | geom_? |
   | Scale | continuous / discrete / log / ... |
   | Statistics | identity / bin / smooth / count |
   | Facets | none / facet_wrap(~?) / facet_grid(?) |
   | Coordinates | cartesian / polar / map |
   | Theme | minimal / classic / custom |

3. In 50 words per chart, explain which layer is most critical to
   the chart's effectiveness.

---

### Part B — Same Data, Three Geometries (30 points)

1. Using the Google Play Store dataset, compute the top 8 categories
   by count.

2. Produce three different charts from the **same data and aesthetics**,
   changing only the geometry:
   - Vertical bar (`geom_col` / `ax.bar`)
   - Lollipop (`geom_point + geom_segment` / `ax.stem`)
   - Horizontal bar (`geom_col + coord_flip` / `ax.barh`)

3. Produce all three in both R and Python (6 charts total).

4. In 100 words, explain which geometry is most effective and why,
   referencing Cleveland & McGill's channel ranking (W01-M03).

---

### Part C — Coordinate System Swap (20 points)

1. Using any categorical variable from the Google Play Store dataset,
   produce a bar chart.

2. Apply `coord_polar(theta = "y")` (R) or `ax.pie()` (Python) to the
   same data to create a pie chart.

3. Place the bar and pie side by side. In 100 words, explain why the
   bar chart is more perceptually accurate, referencing angle vs
   position on the Cleveland ranking.

---

### Part D — plotnine Parity Test (20 points)

1. Install `plotnine` in Python: `pip install plotnine`

2. Reproduce **one** of your Part B charts using plotnine syntax:
   ```python
   from plotnine import *
   (ggplot(df, aes(x="Category", y="n"))
    + geom_col(fill="#1565C0")
    + coord_flip()
    + theme_minimal()
    + labs(title="..."))
   ```

3. In 50 words, compare the plotnine code to the ggplot2 R code:
   what is identical, what differs?

---

### Submission Checklist

- [ ] PDF report (max 4 pages)
- [ ] `W02_M01_homework.R` — Parts B, C in R
- [ ] `W02_M01_homework.py` — Parts B, C, D in Python
- [ ] Screenshots/URLs for Part A charts
- [ ] All figures exported as PNG (300 dpi)
