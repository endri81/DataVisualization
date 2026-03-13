# Workshop 3 · Module 9 — Homework
## Tables as Visualization

**Due**: Before Workshop 3, Module 10 (Lab)
**Format**: R script + Python script + HTML outputs + PDF report (max 3 pages)
**Weight**: Part of Workshop 3 homework (5% of total grade)

### Part A — Styled Summary Table (30 points)
Using Google Play Store data, create a summary table of the top 8 categories with columns: Category, Count, Mean Rating, Paid %. Style it with: bold header, alternating rows, right-aligned numbers, formatted (comma, 2 decimals, percent). Produce with gt (R) and pandas Styler (Python). Export as HTML.

### Part B — Conditional Formatting (30 points)
Add colour encoding to the Mean Rating column (RdYlGn gradient) and bar charts in the Count column. Highlight the maximum Rating in green. Produce in both R and Python.

### Part C — Sparklines (25 points)
Add a "Trend" column with simulated 6-year rating trends. Render as inline sparklines using gt_plt_sparkline (R) or matplotlib inline (Python). Colour each sparkline green (improving) or red (declining).

### Part D — Table vs Chart (15 points)
Present the same 8-category data as: (a) a styled table, (b) a horizontal bar chart. In 150 words, explain when you would use each format in a business presentation vs a technical report.

### Submission Checklist
- [ ] `W03_M09_homework.R` + `W03_M09_homework.py`
- [ ] HTML table outputs
- [ ] PDF report (max 3 pages)
