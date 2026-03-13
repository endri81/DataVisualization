# Workshop 3 — Homework (Final)
## Netflix Dataset: Chart Types Encyclopedia

**Due**: Before Workshop 4, Module 1
**Format**: R script + Python script + PDF report (max 8 pages) + dashboard PDF
**Weight**: 5% of total grade

### The Assignment
Using the Netflix dataset, produce ≥8 distinct chart types addressing 8 analytical questions. Apply the chart selection decision framework: for each chart, state the question, explain why that chart type was chosen, and produce in both R and Python.

### Required Charts (minimum 8, choose from):
1. Sorted horizontal bar (genre or country counts)
2. Histogram or density (movie duration)
3. Ridgeline (duration by genre or rating)
4. Boxplot or violin (duration by rating, seasons by type)
5. Stacked bar or waffle (movie/TV split, rating × type)
6. Line chart (releases per year by type)
7. Lollipop or Cleveland dot (country counts)
8. Pointrange with CI (mean duration per rating)

### Bonus (up to +2 points each):
- Slopegraph or bump chart (genre ranking over time)
- Treemap (genre hierarchy)
- Waterfall (content additions/removals over years)
- Styled gt/kableExtra table with sparklines

### Dashboard Composition
Compose all charts into a single multi-panel dashboard using patchwork (R) and GridSpec (Python). Include panel labels (a–h), global title, subtitle, and source caption. Export as PDF and PNG@300dpi.

### Submission Checklist
- [ ] `W03_homework.R` + `W03_homework.py`
- [ ] `netflix_dashboard.pdf` + `netflix_dashboard.png`
- [ ] PDF report (max 8 pages): question → chart choice → interpretation
