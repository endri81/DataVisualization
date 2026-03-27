# Workshop 8 · Module 2 — Homework
## plotly in R: Interactive Charts

**Due**: Before Workshop 8, Module 4
**Format**: R script + Python script + HTML files + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — ggplotly Conversion (20 points)
Take TWO static charts from your W07 deck. Convert each to interactive using `ggplotly()` with custom `text` aesthetic and `tooltip = "text"`. Configure `hovermode = "x unified"` for time series and `"closest"` for scatter. Save as standalone HTML files. In 100 words, explain what interactive features the user gains.

### Part B — Native plot_ly (25 points)
Recreate ONE of your Part A charts using native `plot_ly()` with `add_trace()` and custom `hovertemplate`. Add a plotly `annotation` (the equivalent of ggplot2's `annotate()`). Save as HTML. In 100 words, compare the ggplotly version with the plot_ly version: which gives more control? Which was faster to build?

### Part C — Dropdown Filter (25 points)
Build a plot_ly chart with an `updatemenus` dropdown that lets the user filter Netflix data by rating category (at least 5 options + "All"). Save as HTML. In 100 words, explain: how does the dropdown implement Shneiderman's "filter" step?

### Part D — Subplot + Linked Brushing (30 points)
Build a two-panel subplot with shared x-axis: (a) scatter of Netflix titles (year vs duration), (b) histogram of ratings. Use `crosstalk::SharedData` and `highlight()` to link the panels — selecting points in the scatter should highlight corresponding bars in the histogram. Save as HTML. In 150 words, explain: what patterns can the user discover through linked brushing that are invisible in either chart alone?

### Submission Checklist
- [ ] `W08_M02_homework.R` + `W08_M02_homework.py`
- [ ] HTML files: ggplotly × 2, plot_ly × 1, dropdown × 1, linked brushing × 1
- [ ] PDF report (max 6 pages) with screenshots and explanations
