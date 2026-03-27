# Workshop 8 · Module 6 — Homework
## Dashboard Design Principles

**Due**: Before Workshop 8, Module 8
**Format**: R script + Python script + PDF report (max 8 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — Dashboard Layout Mockup (30 points)
Using either R (patchwork) or Python (GridSpec), create a static dashboard mockup for the Netflix dataset following Few's layout grid: (a) 4 KPI cards in a row (total titles, movies, TV shows, countries — each with value + delta), (b) a primary chart (yearly additions by type), (c) a secondary chart (top 10 countries), (d) 2–3 detail panels (type split, top ratings, monthly sparkline). Compose as a single figure. Verify: does it follow all 6 of Few's rules?

### Part B — Few's Rules Audit (20 points)
Find a real dashboard online (Tableau Public gallery, government open data portal, or corporate example). In a 6-row table, evaluate it against each of Few's rules: (a) one screen? (b) KPIs at top? (c) ≤7 charts? (d) consistent colour? (e) filter sidebar? (f) descriptive titles? For each rule, state: pass/fail + one-sentence justification.

### Part C — Anti-Pattern → Fix (25 points)
Produce TWO versions of the same Netflix data: (a) the "anti-pattern" version (deliberately violate at least 3 of Few's rules: wrong colours, borders, no KPIs, scattered filters), (b) the "fixed" version (applying all 6 rules). Present side-by-side. In 150 words, list each violation and its fix.

### Part D — KPI Cards (25 points)
Build a reusable KPI card function in both R and Python: (a) the function takes `title`, `value`, and `delta` as parameters, (b) it returns a styled card component (Shiny valueBox or Dash dbc.Card), (c) delta is green if positive, red if negative. Demonstrate with 4 KPI cards in a row. Include the code and a screenshot/rendered output.

### Submission Checklist
- [ ] `W08_M06_homework.R` + `W08_M06_homework.py`
- [ ] Dashboard mockup figure (300 dpi)
- [ ] Anti-pattern + fixed pair (300 dpi)
- [ ] KPI card code + output
- [ ] PDF report (max 8 pages) with Few's rules audit table
