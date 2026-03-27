# Workshop 8 · Module 10 — Course Notes
## Lab: Build an Interactive Dashboard

### 1. Lab Purpose
This is the summative assessment for Workshop 8. It integrates every technique from M01–M09 into a single deliverable: a fully interactive, deployed dashboard. The lab tests the student's ability to execute the complete pipeline: wireframe → layout → charts → reactive filtering → cross-filtering → deployment.

### 2. The Dashboard Building Pipeline
The 10-step pipeline maps directly to workshop modules:

**Step 1** (M06): Sketch the wireframe following Few's grid (KPI row → primary chart → secondary chart → detail panels). This is done on paper before any code.

**Step 2** (M06): Define the global colour palette. `PALETTE <- c(Movie = "#1565C0", "TV Show" = "#E53935")` in R or `PALETTE = {"Movie": "#1565C0", "TV Show": "#E53935"}` in Python. Apply to every chart.

**Step 3** (M01): Map each panel to a Shneiderman step: KPIs = overview, dropdowns = filter, hover = details, click = relate, reset = history, table = extract.

**Step 4** (M04/M05): Build the Shiny UI or Dash layout. Use `fluidRow/column` (Shiny) or `dbc.Row/Col` (Dash) to implement the grid.

**Step 5** (M02/M03): Create plotly charts for each panel. Use `ggplotly()` or `px.line/bar/scatter()`. Apply PALETTE consistently.

**Step 6** (M04/M05): Wire the reactive pipeline. One `reactive()` or one `@callback` filters the data and feeds all panels. Single source of truth.

**Step 7** (M07/M08): Add cross-filtering. Click on a country bar → update the country dropdown → all panels re-filter. This is the most advanced interaction.

**Step 8** (M06): Audit against Few's 6 rules: one screen? KPIs at top? ≤7 charts? Consistent colour? Filter sidebar? Descriptive titles?

**Step 9** (M09): Deploy to shinyapps.io (Shiny), Render.com (Dash), or render as Quarto HTML.

**Step 10**: Write the 300-word reflection with Shneiderman audit.

### 3. Assessment Rubric (100 points)

| Criterion | Points | Key Question |
|-----------|--------|-------------|
| Layout (Few's grid) | 15 | KPIs at top, 1 screen, Z-pattern hierarchy? |
| KPI cards | 10 | 4 cards with value + delta, auto-update on filter? |
| Chart quality | 25 | ≥4 plotly panels, hover, consistent palette, 4 chart types? |
| Filter inputs | 15 | ≥3 inputs + reset, all panels react simultaneously? |
| Cross-filtering | 10 | Click on chart → filter other panels? |
| Deployment | 15 | URL or HTML submitted, runs without errors? |
| Reflection | 10 | 300-word process reflection + Shneiderman 7-step audit? |

### 4. Shneiderman Audit Template
The reflection must include a 7-row table mapping each Shneiderman step to the specific dashboard component:

| Mantra Step | Dashboard Component | Widget/Interaction |
|---|---|---|
| 1. Overview first | KPI row | 4 value cards (total, movies, TV, countries) |
| 2. Zoom | plotly charts | Scroll-zoom on any chart |
| 3. Filter | Input bar | Type dropdown + year slider + country dropdown |
| 4. Details on demand | All charts | Hover tooltips |
| 5. Relate | Country bar | Click bar → filter all panels |
| 6. History | Reset button | Restores all defaults |
| 7. Extract | Data table | Sort, search, filter, mentally export |

### 5. Workshop 8 Complete Summary
After 10 modules, the student's interactive visualization toolkit includes: Shneiderman's mantra as design framework (M01), plotly in R (M02) and Python (M03), Shiny reactive apps (M04), Dash callback apps (M05), Few's dashboard design rules (M06), two complete case study dashboards (M07–M08), deployment to multiple platforms (M09), and integrated dashboard building (M10).

Combined with W07 (storytelling), students can now produce both author-driven presentations (static slides) and reader-driven dashboards (interactive apps) from the same data — the complete Martini Glass.

### References
- All M01–M09 references apply.
- Few, S. (2013). *Information Dashboard Design*, 2nd ed. Analytics Press.
- Shneiderman, B. (1996). The Eyes Have It. *Proc. IEEE VL*.
