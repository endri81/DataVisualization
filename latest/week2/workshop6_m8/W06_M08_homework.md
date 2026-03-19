# Workshop 6 · Module 8 — Homework
## Case Study: Netflix Content Trends Over Time

**Due**: Before Workshop 6, Module 10
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Yearly Type Trend (15 points)
Produce a two-line chart of Netflix yearly additions by type (Movie vs TV Show, 2015–2021) with direct labels showing counts at each point. Identify the movie peak year and the crossover point. In 100 words, explain the strategic significance of the TV pivot.

### Part B — Monthly + Events (20 points)
Produce a monthly additions line chart (2015–2021) with three event annotations: (a) January 2016 global expansion, (b) March 2020 COVID lockdown, (c) mid-2021 content slowdown. Use geom_vline + annotate (R) or axvline + annotate (Python). In 150 words, discuss: do the events correlate with visible trend changes? Is there a lag between event and effect?

### Part C — Genre Trends (20 points)
Compute yearly additions for the top 5 genres. Produce two versions: (a) grey+accent highlighting the fastest-growing genre, (b) small multiples (one panel per genre). In 150 words, which genres drive Netflix's growth? Which are plateauing?

### Part D — Cumulative + Composition (20 points)
Produce: (a) a cumulative stacked area by type, (b) a 100% stacked area showing the proportion shift. In 100 words, how has the Movie/TV Show composition changed? What does the rate view show that the cumulative view hides?

### Part E — Four Temporal Findings (25 points)
Write four numbered findings in the format: Finding → Temporal Evidence → Strategic Implication. Each finding must reference a specific visualization from Parts A–D. At least one finding must address the seasonal pattern, and at least one must address an event (COVID, expansion, slowdown).

### Submission Checklist
- [ ] `W06_M08_homework.R` + `W06_M08_homework.py`
- [ ] Figures: yearly_type, monthly_annotated, genre_trends (2 versions), cumulative (2 versions), seasonal (300 dpi)
- [ ] PDF report (max 6 pages)
