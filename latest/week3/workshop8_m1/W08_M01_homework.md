# Workshop 8 · Module 1 — Homework
## Interactivity Theory: Shneiderman's Mantra

**Due**: Before Workshop 8, Module 3
**Format**: R script + Python script + HTML files + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — Static vs Interactive (25 points)
Take ONE chart from your W07 work (a static assertion-evidence chart). Reproduce it as: (a) the original static ggplot2/matplotlib PNG, (b) an interactive plotly version with hover tooltips showing all relevant metadata. Save the plotly version as a standalone HTML file. In 150 words, describe: what can the user discover in the interactive version that was invisible in the static version?

### Part B — Shneiderman's Mantra Applied (30 points)
Using the Netflix OR e-Car dataset, build a plotly scatter plot that demonstrates the first 4 steps of Shneiderman's mantra: (1) Overview: show all data points, (2) Zoom: verify that scroll-zoom works, (3) Filter: add a dropdown menu that filters by type/tier, (4) Details on demand: configure hover tooltip with 4+ metadata fields. Save as HTML. In 100 words, map each step to the specific plotly feature you used.

### Part C — Interaction Classification (20 points)
For each of Yi et al.'s six interaction types (selection, navigation, filtering, reconfiguration, encoding, connection), identify ONE example from a real interactive visualization you use (e.g., Google Maps, Spotify Wrapped, a news interactive). Present as a 6-row table: interaction type → example app → specific interaction → which Yi category.

### Part D — Decision Framework (25 points)
For each of the following scenarios, recommend "static" or "interactive" and justify in one sentence: (a) quarterly report emailed to board members, (b) real-time sales monitoring for regional managers, (c) exploratory analysis notebook shared with data science team, (d) Twitter thread about climate data, (e) patient health dashboard for a clinic, (f) conference poster presentation, (g) Quarto report embedded in a company wiki.

### Submission Checklist
- [ ] `W08_M01_homework.R` + `W08_M01_homework.py`
- [ ] Static chart PNG + interactive HTML (Part A)
- [ ] Shneiderman demo HTML (Part B)
- [ ] PDF report (max 6 pages) with interaction table and decision framework
