# Workshop 6 · Module 6 — Homework
## Animation Fundamentals

**Due**: Before Workshop 6, Module 8
**Format**: R script + Python script + GIF(s) + PDF report (max 6 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Cumulative Line Animation (25 points)
Animate Netflix monthly additions as a line that grows left-to-right from Jan 2015 to Dec 2021. In R: use `transition_reveal(date)` with a red dot at the growing tip. In Python: use `FuncAnimation` updating `line.set_data()` each frame. Save as GIF. Also produce a static 4-stage version (25%, 50%, 75%, 100% of the timeline) as a panel for the PDF report. In 100 words, describe what the reveal animation communicates that the static line chart does not.

### Part B — Gapminder Scatter (25 points)
Using the simulated (or real) Gapminder data, create an animated scatter: x = GDP (log), y = life expectancy, size = population, colour = continent. Animate across years. In R: `transition_time(year) + shadow_wake()`. In Python: `FuncAnimation` with `ax.clear()` per frame. Save as GIF. Produce a 4-panel key-frames static alternative (2000, 2007, 2014, 2020). In 100 words, compare: what does the animation reveal that the key-frames miss?

### Part C — Static Alternative (25 points)
For the Gapminder data, produce a 1×6 small-multiples panel (years 2000, 2004, 2008, 2012, 2016, 2020). In 150 words, compare the small-multiples panel to the animation: (a) what information is preserved in static? (b) what is lost? (c) which would you use for a research paper? (d) which for a TED-style presentation?

### Part D — When to Animate (25 points)
For each scenario below, recommend "animate" or "static" and justify in one sentence:
(a) Quarterly revenue trend for CFO board meeting
(b) Twitter post about climate change over 50 years
(c) Journal paper figure showing GDP convergence
(d) Shiny dashboard for real-time sales monitoring
(e) University lecture on population growth
(f) Email attachment summarising election results
(g) Interactive notebook for exploratory analysis

Bonus (+5 points): produce both an animated GIF and a static key-frames panel from the same data pipeline, demonstrating the "always provide a static companion" principle.

### Submission Checklist
- [ ] `W06_M06_homework.R` + `W06_M06_homework.py`
- [ ] GIFs: line_reveal.gif, gapminder.gif (or static alternatives if tools unavailable)
- [ ] Static figures: 4-stage line, key-frames panel, 6-panel multiples (300 dpi)
- [ ] PDF report (max 6 pages)
