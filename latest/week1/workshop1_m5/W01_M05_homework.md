# Workshop 1 · Module 5 — Homework
## Professional Chart Layout

**Due**: Before Workshop 1, Module 7  
**Format**: PDF report (max 4 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Typographic Hierarchy (30 points)

1. Using the Google Play Store dataset (`googleplaystore.csv`), create a
   horizontal bar chart of the top 10 categories by count.

2. Apply a complete five-level typographic hierarchy:
   - Title: bold, 16pt — states the main finding
   - Subtitle: regular, 11pt — data source and date
   - Axis label: 10pt
   - Direct labels: 8pt, on each bar
   - Caption: italic, 8pt — "Source: Kaggle Google Play Store Apps"

3. Produce the chart in both R (`theme()` + `element_text()`) and
   Python (`rcParams` + per-element `fontsize`).

4. In 100 words, explain the reading order your hierarchy creates.

---

### Part B — Direct Labelling vs Legend (30 points)

1. Using the Netflix dataset (`netflix.csv`), compute the count of titles
   added per year for Movies and TV Shows separately (2015–2021).

2. Create two versions of the same line chart:
   a. **Version A**: with a traditional legend box
   b. **Version B**: with direct labels at line endpoints (no legend)

3. Produce both versions in R (`ggrepel`) and Python (`adjustText` or
   manual `ax.text()`).

4. In 100 words, explain which version is easier to read and why,
   referencing the legend-shuttle problem.

---

### Part C — Multi-Panel Composition (40 points)

1. Build a four-panel composite figure from the Google Play Store data:
   - Panel (a): bar chart of top 5 categories
   - Panel (b): histogram of Ratings
   - Panel (c): scatter of Reviews vs Rating (log-scaled)
   - Panel (d): full-width time series of apps added per year

2. Use `patchwork` in R: `(p1 | p2 | p3) / p4` with `tag_levels = "a"`.
   Use `GridSpec` in Python: `gs = GridSpec(2, 3); ax4 = fig.add_subplot(gs[1, :])`.

3. Ensure consistent fonts, colours, and margins across all panels.

4. Export as PDF (vector) and PNG (300 dpi).

5. In 100 words, explain the layout logic: why is panel (d) full width?

---

### Submission Checklist

- [ ] PDF report (max 4 pages)
- [ ] `W01_M05_homework.R`
- [ ] `W01_M05_homework.py`
- [ ] Exported figures: PDF (vector) and PNG (300 dpi)
