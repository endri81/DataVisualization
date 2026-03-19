# Workshop 6 · Module 10 — Course Notes
## Lab: Animated Time Series Dashboard

### 1. Lab Objective
This lab is the capstone assessment for Workshop 6. It integrates every temporal visualization technique from Modules 1–9 into a single coherent analysis of the Netflix dataset. The deliverable is a **six-panel temporal dashboard** plus an **animated bar chart race GIF**, accompanied by four numbered temporal findings with evidence.

The lab tests the student's ability to: (a) select the appropriate temporal chart type for each question, (b) implement it correctly in both R and Python, (c) annotate with events and context, (d) compose multiple panels into a readable dashboard, and (e) extract and articulate temporal findings with evidence.

### 2. Dashboard Structure (Six Panels)
The dashboard is deliberately designed so each panel uses a different W06 technique and answers a different temporal question:

**Panel (a): Monthly line chart with event annotations and LOESS trend** (M02–M03). Answers: "what is the overall trajectory of Netflix additions, and how do key events relate to trend changes?" The LOESS smoother reveals the underlying trend by removing monthly noise. Event annotations (2016 global expansion, 2020 COVID) transform description into explanation.

**Panel (b): Stacked area of top 5 genres over time** (M03). Answers: "how has the genre composition of Netflix's catalog changed?" The stacked area shows both absolute growth (total height increasing) and compositional shift (International genres growing as a proportion).

**Panel (c): Sparklines by type — Movie vs TV Show** (M04). Answers: "at a glance, what are the trajectories of the two content types?" Sparklines provide a compact comparison without the overhead of full axes and labels. Min/max/current dots mark key reference points.

**Panel (d): Calendar heatmap of 2020 daily additions** (M05). Answers: "what is Netflix's daily release pattern?" The DOW × week grid reveals that Friday is the primary release day (visible as a bright horizontal band) and that holiday periods show higher activity.

**Panel (e): Seasonal subseries — 2016–2021 overlaid** (M05). Answers: "is there a consistent monthly release pattern, and does 2021 follow it?" The grey+accent overlay reveals a Q4 spike (holiday content push) that is consistent across years, with 2021 following the pattern at a lower level (COVID production pipeline effect).

**Panel (f): Bar chart race static frame — 2021** (M07). Answers: "which countries dominate Netflix's catalog, and how has this changed?" The static frame shows the 2021 ranking; the accompanying GIF shows the trajectory from 2016. India's rise from outside the top 5 to #2 is the key finding.

### 3. Animation Component
The animated bar chart race (saved as GIF) shows the cumulative title count by country evolving from 2016 to 2021. In R: `gganimate::transition_states(year_added)` with `coord_flip()`. In Python: `FuncAnimation` with `ax.barh()` redrawn each frame. The GIF is a presentation/engagement tool; the static frame in Panel (f) is the analytical companion for the PDF report.

### 4. Four Key Findings Template
Each finding follows the **Finding → Temporal Evidence → Implication** structure:

**Finding 1 (Trend)**: Netflix additions peaked around 2019–2020 and have since declined. Evidence: the monthly line chart (Panel a) shows the LOESS trend flattening and turning downward after 2020. Implication: the era of aggressive catalog expansion is over; Netflix is shifting to fewer, higher-quality titles.

**Finding 2 (Composition)**: International content is the fastest-growing genre category. Evidence: the stacked area (Panel b) shows International genres expanding their share year-over-year. Implication: Netflix's global expansion strategy is driving content investment away from domestic US-centric genres.

**Finding 3 (Seasonal)**: Friday is the dominant release day, with a Q4 holiday spike. Evidence: the calendar heatmap (Panel d) shows a bright Friday band; the seasonal subseries (Panel e) shows December/January peaks. Implication: Netflix's release calendar is optimised for weekend binge-watching and holiday audiences.

**Finding 4 (Geography)**: India has risen from outside the top 5 to the #2 content-producing country. Evidence: the bar chart race (Panel f / GIF) shows India overtaking the UK, Japan, and South Korea between 2018 and 2021. Implication: Bollywood and regional-language content investment is a major growth vector.

### 5. Workshop 6 Temporal Toolkit — Complete Summary
After 10 modules, the student's temporal visualization toolkit includes:

| Technique | Module | R Function | Python Function |
|-----------|--------|-----------|----------------|
| Granularity control | M01 | `floor_date() + group_by()` | `df.resample()` |
| STL decomposition | M01 | `stl()` | `statsmodels.STL()` |
| Banking to 45° | M02 | `ggsave(width=, height=)` | `figsize=` |
| Grey+accent | M02 | Two `geom_line()` calls | Two `ax.plot()` calls |
| Indexing | M02 | `value / first(value) * 100` | `values / values[0] * 100` |
| Direct labels | M02 | `geom_text(data=last_point)` | `ax.text(x[-1], y[-1])` |
| Event annotation | M02 | `geom_vline() + annotate()` | `ax.axvline() + ax.annotate()` |
| Line / step / area | M03 | `geom_line/step/area()` | `ax.plot/step/fill_between()` |
| Stacked area | M03 | `geom_area(fill=group)` | `ax.stackplot()` |
| Ribbon (CI) | M03 | `geom_ribbon(ymin, ymax)` | `ax.fill_between(lo, hi)` |
| Sparklines | M04 | `facet_wrap(ncol=1) + theme_void()` | `subplots(n,1) + axis("off")` |
| Small multiples | M04 | `facet_wrap(~group)` | `subplots(rows, cols)` loop |
| Calendar heatmap | M05 | `geom_tile(x=week, y=dow)` | `pivot_table + imshow` |
| Seasonal subseries | M05 | `ggplot(group=year, color=is_current)` | Loop + conditional alpha |
| gganimate | M06 | `transition_time/states/reveal()` | `FuncAnimation()` |
| Bar chart race | M07 | `transition_states() + coord_flip()` | `bar_chart_race` or manual |
| Bump chart | M07 | `geom_line() + scale_y_reverse()` | `ax.plot() + set_ylim(N, 0)` |

### References
- All W06 M01–M09 references apply.
- Netflix dataset: Kaggle (Shivam Bansal, 2021).
