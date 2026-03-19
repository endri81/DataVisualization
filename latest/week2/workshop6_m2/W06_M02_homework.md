# Workshop 6 · Module 2 — Homework
## Line Charts: Theory & Best Practices

**Due**: Before Workshop 6, Module 4
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Indexed Lines (25 points)
Using the Netflix dataset, compute three monthly time series (2015–2021): total titles added, Movie titles added, and TV Show titles added. Plot all three on the same chart: (a) raw values, (b) indexed to 100 (starting Jan 2015). Produce in both R and Python. In 150 words, explain why indexing changes the story: which type grew fastest in relative terms?

### Part B — Grey + Accent (25 points)
Using the Netflix dataset, compute monthly additions for the top 5 genres (2015–2021). Produce two versions: (a) all 5 lines coloured (spaghetti), (b) grey+accent highlighting the fastest-growing genre. Add a direct label at the line endpoint. In 100 words, explain why grey+accent is clearer than full colour for 5+ series.

### Part C — Dual Axis Critique (25 points)
Create a deliberately misleading dual y-axis chart showing Netflix movie additions and TV show additions on separate scales (manipulate the right-axis scale to make them appear to converge). Then create the honest alternative: two separate panels with shared x-axis. In 150 words, explain specifically how the dual axis chart misleads and what the honest version reveals.

### Part D — Event Annotation (25 points)
Produce a line chart of Netflix monthly additions (2015–2021) with three event annotations: (a) Netflix's first major original series launch (2016), (b) COVID-19 lockdown (March 2020), (c) content slowdown (2021). Use geom_vline + annotate (R) or axvline + annotate (Python). In 100 words, discuss whether the events correlate with visible changes in the trend.

### Submission Checklist
- [ ] `W06_M02_homework.R` + `W06_M02_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 5 pages)
