# Workshop 6 · Module 7 — Homework
## Advanced Animation: Bar Chart Races

**Due**: Before Workshop 6, Module 9
**Format**: R script + Python script + GIF (if possible) + PDF report (max 6 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Static Bar Chart Frame (20 points)
Using the Netflix dataset, compute cumulative titles per country for 2021 (top 10 countries). Produce a horizontal bar chart showing the final "frame" of a bar chart race: bars sorted by value, country labels, formatted counts. Produce in both R and Python.

### Part B — Key-Frames Panel (20 points)
Produce a 1×3 faceted panel showing the top-10 country bar chart at three time points: 2017, 2019, 2021. Use the same country order (sorted by 2021 values). In 100 words, describe: which countries gained the most between frames? Which stayed stable?

### Part C — Bump Chart (25 points)
Produce a bump chart (rank plot) showing the rank trajectories of the top 10 countries over 2016–2021. x = year, y = rank (1 at top, inverted axis), one coloured line per country, direct labels at the right end. In 150 words, compare the bump chart to the bar chart race: what does each reveal that the other cannot? When would you choose each?

### Part D — Animated Bar Race (20 points)
Produce an animated bar chart race using gganimate (R) or FuncAnimation / bar_chart_race (Python). Save as GIF. If animation tools are not available, produce a slope chart (2016 → 2021 rank shift) as an alternative. Include one screenshot of the GIF in your PDF report.

### Part E — Critique (15 points)
Find a bar chart race on YouTube or social media. In 200 words, critique it: (a) does the animation add analytical insight or just entertainment? (b) what static chart would convey the same information more precisely? (c) are there misleading aspects (scale changes, missing context, interpolation artefacts)?

### Submission Checklist
- [ ] `W06_M07_homework.R` + `W06_M07_homework.py`
- [ ] Static figures: bar_frame.png, keyframes.png, bump_chart.png (300 dpi)
- [ ] Animation: bar_race.gif (or slope_chart.png if animation unavailable)
- [ ] PDF report (max 6 pages)
