# Workshop 8 · Module 3 — Homework
## plotly in Python: Interactive Charts

**Due**: Before Workshop 8, Module 5
**Format**: Python script + R script + HTML files + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — px One-Liners (20 points)
Produce THREE plotly.express charts from the Netflix dataset: (a) `px.line` of yearly additions by type, (b) `px.scatter` of titles with hover_name=title and 4+ hover_data fields, (c) `px.bar` of top 10 countries. Save all three as HTML. Each should have a meaningful title, appropriate hovermode, and `template="plotly_white"`.

### Part B — go.Scatter with Annotation (25 points)
Recreate the movie decline hero chart using `go.Scatter` with: (a) custom `hovertemplate` with comma formatting, (b) a plotly `annotation` showing the –42% decline with arrow, (c) `hovermode="x unified"`. Save as HTML. In 100 words, compare the effort of building this in go vs px.

### Part C — Dropdown + Animation (25 points)
Build TWO interactive features: (a) a `go.Figure` with `updatemenus` dropdown that filters by genre (5+ options + "All"), (b) a `px.bar` or `px.scatter` with `animation_frame="year_added"` showing genre evolution animated. Save both as HTML. In 100 words, explain when animation adds value vs when a static small-multiples panel would be better.

### Part D — R ↔ Python Translation (30 points)
Take your Part B Python chart (go.Scatter with annotation). Reproduce it in R using `plot_ly() |> add_trace() |> layout(annotations=...)`. Save as HTML. In 200 words, compare: (a) which syntax feels more natural? (b) are the hovertemplate strings identical? (c) which language makes subplot creation easier? (d) how does the output HTML differ (file size, behaviour)?

### Submission Checklist
- [ ] `W08_M03_homework.py` + `W08_M03_homework.R`
- [ ] HTML files: px_line, px_scatter, px_bar, go_annotated, dropdown, animation, R_translation (7 files)
- [ ] PDF report (max 6 pages) with screenshots and comparisons
