# Workshop 7 · Module 4 — Course Notes
## The Seven Basic Data Stories

### 1. Why Story Types Matter
Before choosing a chart type, identify which **story** your data tells. The story type determines the chart type — not the other way around. If your finding is about change over time, a scatter plot is wrong regardless of how pretty it looks. If your finding is about composition, a line chart is wrong. The seven story types provide a decision framework: finding → story → chart.

### 2. The Seven Stories

**Story 1 — Change Over Time**: the most common data story. Any finding involving growth, decline, peak, shift, or trend. Keywords: "increased," "declined," "peaked," "shifted," "grew." Natural charts: line, area, step, bar (temporal). Example: "Netflix movie additions peaked in 2019 and have declined 42% since."

**Story 2 — Drill Down (Whole → Parts)**: decomposing an aggregate into its components. Keywords: "composed of," "breakdown," "share," "proportion." Natural charts: stacked bar, treemap, pie/donut (sparingly), 100% bar. Example: "69% of Netflix's catalog is movies, 31% is TV shows."

**Story 3 — Zoom Out (Detail → Context)**: placing a finding in its broader context. The opposite of drill-down — instead of looking inside, you look outside. Keywords: "compared to the industry," "in the global context," "relative to historical average." Natural charts: small multiples, benchmark line, map, ranked bar. Example: "India rose from #5 to #2 in global content production."

**Story 4 — Contrast & Compare**: highlighting differences between two or more entities. Keywords: "vs," "gap between," "before/after," "A differs from B." Natural charts: grouped bar, slope chart, dumbbell chart, back-to-back bar. Example: "Pre-2008 spread: 3.8pp vs Post-2008: 2.9pp."

**Story 5 — Intersections & Relationships**: showing how two variables relate. Keywords: "correlated," "associated," "relationship between," "as X increases, Y..." Natural charts: scatter, bubble, heatmap (correlation matrix), network graph. Example: "Higher credit tier → lower offered rate."

**Story 6 — Factors & Drivers**: explaining what causes or contributes to an outcome. Keywords: "driven by," "because of," "contributors to," "explained by." Natural charts: waterfall, tornado (horizontal bar ranked by impact), forest plot, Pareto. Example: "Genre growth is driven by global expansion (35%), original production (28%), and local-language content (22%)."

**Story 7 — Outliers & Anomalies**: identifying what is unusual or unexpected. Keywords: "unusual," "anomaly," "spike," "deviation," "extreme." Natural charts: scatter with highlighted points, control chart (process mean ± control limits), box plot with annotated outliers. Example: "December 2020: 160 titles added — 3× the monthly average."

### 3. The Decision Workflow
When you have a finding from EDA, follow this three-step workflow:

**Step 1**: Write the finding as a declarative sentence (this becomes the chart title).

**Step 2**: Identify the keywords that signal the story type (see the keyword table above).

**Step 3**: Select the chart type that is the natural partner for that story type.

This workflow prevents the common mistake of choosing a chart type based on what looks interesting or what you know how to code, rather than what serves the finding.

### 4. Combining Stories in a Presentation
A typical data presentation uses 3–5 stories in sequence, following the narrative arc (M01):

**Opening (context)**: Story 3 (Zoom Out) — set the scene. "Netflix built 8,800+ titles by 2021."

**Complication**: Story 1 (Change) or Story 4 (Contrast) — introduce the tension. "But movie additions are declining while TV grows."

**Analysis**: Story 6 (Factors) or Story 2 (Drill Down) — explain why. "Three factors drive the shift: global expansion, originals, local content."

**Evidence**: Story 5 (Intersection) or Story 7 (Outlier) — support with specific data. "The correlation between international investment and genre growth is r = 0.8."

**Conclusion**: back to Story 1 (Change) — what will happen next. "At current rates, TV Shows will overtake Movies by 2024."

### 5. Story Types Applied to Course Datasets
Each dataset naturally supports multiple story types:

**Netflix**: Change (movie decline), Drill Down (genre composition), Zoom Out (country comparison), Contrast (Movie vs TV), Factors (growth drivers), Outliers (December spikes).

**e-Car**: Change (rate drop post-2008), Contrast (pre vs post crisis), Intersection (tier vs rate), Factors (CoF + tier + LTV as rate drivers), Outliers (extreme-rate loans), Zoom Out (compared to Fed funds rate).

### References
- Dykes, B. (2020). *Effective Data Storytelling*. Wiley.
- Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
- Few, S. (2012). *Show Me the Numbers*, 2nd ed. Analytics Press.
