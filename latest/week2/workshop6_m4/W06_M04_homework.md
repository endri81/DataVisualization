# Workshop 6 · Module 4 — Homework
## Sparklines & Small Temporal Multiples

**Due**: Before Workshop 6, Module 6
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Spaghetti vs Small Multiples (25 points)
Using the Netflix dataset, compute monthly additions for the top 6 genres (2016–2021). Produce side-by-side: (a) a single-panel spaghetti chart with all 6 genres, (b) small temporal multiples (2×3 grid, shared x-axis, free y-axis). Produce in both R (`facet_wrap`) and Python (`subplots`). In 150 words, explain what patterns are visible in the small multiples that are hidden in the spaghetti chart. Reference at least one specific genre.

### Part B — Free-y vs Fixed-y (20 points)
Produce the same 2×3 small multiples twice: (a) with `scales = "free_y"` (each panel's own y-range), (b) with `scales = "fixed"` (shared y-range). In 150 words, compare: which version tells the "individual patterns" story? Which tells the "relative volume" story? Which would you choose for a presentation to Netflix content strategists, and why?

### Part C — Sparkline Panel (25 points)
Produce a vertical sparkline panel (6 rows, one per genre) showing 72-month trends (2016–2021). Mark the minimum (red dot), maximum (green dot), and current (blue dot) for each series. No axes or gridlines — pure Tufte-style. Place the genre name at the left edge and the current numeric value at the right edge. Produce in both R and Python.

### Part D — Highlighted Multiples (15 points)
Produce highlighted multiples: 2×3 grid where every panel shows all 6 genres as light grey background lines, with the focal genre highlighted in red. In 100 words, which genre's trajectory is most distinctive relative to the others?

### Part E — Decision Table (15 points)
For each scenario below, state whether you would use a multi-line chart, small multiples, highlighted multiples, or sparklines. Justify each choice in one sentence.
(a) 3 product lines for CFO quarterly review
(b) 8 country GDP trends for an economics textbook
(c) 30 stock tickers on a trading dashboard
(d) 6 Netflix genres for a content strategy meeting
(e) 50 server CPU metrics in a monitoring tool

### Submission Checklist
- [ ] `W06_M04_homework.R` + `W06_M04_homework.py`
- [ ] All figures as PNG (300 dpi): spaghetti, multiples (free + fixed), sparklines, highlighted
- [ ] PDF report (max 6 pages)
