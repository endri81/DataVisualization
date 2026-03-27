# Workshop 7 · Module 3 — Homework
## Advanced Annotation in Code

**Due**: Before Workshop 7, Module 5
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 7 homework (5% of total grade)

### Part A — ggrepel / adjustText (25 points)
Using the Netflix dataset, produce a scatter plot of the top 15 countries (x = total titles, y = average rating or year span). Label all 15 points using ggrepel (R) and adjustText (Python) — no overlaps allowed. In 100 words, compare: how does the automatic placement differ between the two tools? Which produces cleaner results?

### Part B — Annotation Layers (30 points)
Produce a 2x2 panel showing the same Netflix movie additions chart at four annotation levels: (a) bare chart (no annotation), (b) + reference line at peak, (c) + direct label at endpoint, (d) + callout box with decline percentage and curved arrow. Produce in both R (patchwork) and Python (subplots). In 100 words, explain: at which layer does the chart become "explanatory"? Can you skip layers?

### Part C — Fully Dressed Explanatory Chart (25 points)
Produce a single "fully dressed" explanatory chart of your choice (Netflix or e-Car) using ALL annotation techniques: declarative title, direct labels (no legend), reference line, shaded region, callout box with curved arrow, source caption. This chart should be presentation-ready. In 100 words, describe the annotation hierarchy you applied.

### Part D — ggtext Title (20 points)
Using ggtext (R) or multi-coloured ax.text (Python), produce a chart where the title contains coloured words matching the data series — eliminating the need for a legend. If ggtext is not installed, simulate the effect by describing what the markdown title would look like and produce the closest approximation. In 100 words, explain why coloured-word titles are more effective than separate legends.

### Submission Checklist
- [ ] `W07_M03_homework.R` + `W07_M03_homework.py`
- [ ] Figures: repelled_labels, annotation_layers (2x2), fully_dressed, coloured_title (300 dpi)
- [ ] PDF report (max 6 pages)
