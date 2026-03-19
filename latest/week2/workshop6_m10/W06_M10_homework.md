# Workshop 6 — Final Homework
## Lab: Netflix Animated Time Series Dashboard

**Due**: Before Workshop 7, Module 1
**Format**: R + Python scripts + GIF + PDF/HTML report (max 8 pages)
**Weight**: 5% of total grade (summative assessment for Workshop 6)

### Required Components (100 marks)

**1. Monthly line chart with event annotations (15 marks)**
Produce a monthly additions line chart (2015–2021) with: proper date formatting, LOESS/smoothed trend overlay, at least two event annotations (2016 expansion, 2020 COVID). R: `geom_line() + geom_smooth() + geom_vline() + annotate()`. Python: `ax.plot() + savgol_filter() + ax.axvline() + ax.annotate()`.

**2. Stacked area of top 5 genres (10 marks)**
Monthly additions stacked by genre (2016–2021). Consider both absolute and 100% stacked versions. R: `geom_area(fill=genre)`. Python: `ax.stackplot()`.

**3. Sparklines by type (10 marks)**
Compact sparkline panel: one row for Movie, one for TV Show. Mark min (red), max (green), current (blue). No axes — Tufte-style.

**4. Calendar heatmap of 2020 (10 marks)**
Daily additions in 2020 as DOW × week grid. Colour = count. R: `geom_tile()`. Python: `pivot_table + imshow`.

**5. Seasonal subseries (10 marks)**
Overlay 2016–2021 on Jan–Dec axis. Grey+accent on 2021. Identify the seasonal pattern.

**6. Bar chart race — animated GIF (15 marks)**
Top 10 countries by cumulative titles, animated over 2016–2021. R: `gganimate::transition_states()`. Python: `FuncAnimation` or `bar_chart_race`. Save as GIF. Include one static key-frame in the PDF report. If animation tools are unavailable, produce a bump chart as alternative (full marks still available).

**7. Six-panel composed dashboard (10 marks)**
Compose panels 1–6 into a single figure using patchwork (R) / GridSpec (Python). Include a main title, subtitle listing techniques used, and panel tags (a–f). Save as PNG (300 dpi) and PDF.

**8. Four numbered temporal findings (15 marks)**
Each finding must follow the structure: **Finding** (one sentence) → **Temporal Evidence** (which panel, what pattern) → **Implication** (what does it mean for Netflix's strategy). Requirements:
- At least one finding about the overall **trend** (M01)
- At least one about **seasonal pattern** (M05)
- At least one about a specific **event** response (M02)
- At least one about **geographic** or **genre** shift (M07/M08)

**9. Limitations and next steps (5 marks)**
In 150 words: what temporal patterns might you be missing? What additional data (e.g., viewing hours, production budgets, competitor releases) would enable deeper temporal analysis?

### Bonus (+5 marks)
Produce an STL decomposition of monthly Netflix additions (M01) and include the seasonal component as a 7th panel or as a separate figure. Interpret: is the seasonal pattern strengthening or weakening over time?

### Submission Checklist
- [ ] `W06_homework.R` (complete script reproducing all panels)
- [ ] `W06_homework.py` (complete script reproducing all panels)
- [ ] `bar_race.gif` (animated, or bump_chart.png if animation unavailable)
- [ ] `w06_dashboard.png` (six-panel composed dashboard, 300 dpi)
- [ ] `w06_dashboard.pdf` (vector version)
- [ ] Individual panel PNGs (300 dpi each)
- [ ] PDF/HTML report (max 8 pages) with all figures, findings, and limitations
