# Workshop 1 · Module 6 — Course Notes
## The Design Process: From Data to Display

---

### 1. The Visualization Pipeline

Effective visualization follows a five-step pipeline that disciplines the transition from raw data to finished chart.

**Acquire** — Obtain the data via API, database query, file import, or web scraping. Document the provenance: who collected it, when, how, and what biases may be present.

**Parse** — Structure the data into a clean, analysis-ready format. This includes type conversion (dates, numerics, factors), column renaming, and schema validation.

**Filter** — Remove noise, outliers, and out-of-scope records. Filtering is an analytical decision, not a cleaning step; every exclusion should be documented and justified.

**Mine** — Compute summary statistics, aggregations, and derived variables. This is where exploratory data analysis (EDA) occurs: distributions, correlations, group comparisons.

**Represent** — Map data to visual form using the principles from Modules 1–5: choose the chart type, assign encoding channels, apply typography, colour, and layout.

The critical insight is that Steps 1–4 consume approximately 80% of the effort but determine 80% of the chart's analytical value. A polished chart built on uncleaned data is misleading regardless of its aesthetics.


### 2. Cairo's Visualization Wheel

Cairo (2012) models visualization design as a set of six continuous trade-offs, not binary choices:

1. **Abstraction ↔ Figuration**: statistical encodings vs pictorial representations
2. **Functionality ↔ Decoration**: analytical precision vs aesthetic appeal
3. **Density ↔ Lightness**: data-rich displays vs minimal, focused displays
4. **Multidimensional ↔ Unidimensional**: many variables vs one variable
5. **Originality ↔ Familiarity**: novel chart forms vs standard conventions
6. **Novelty ↔ Redundancy**: surprising insights vs reinforcing known facts

There is no universally "correct" position on any axis. The appropriate position depends on the audience and the communication goal. Analytical audiences benefit from abstraction, density, and multidimensionality. General audiences respond better to figuration, lightness, and familiarity.


### 3. Munzner's Nested Model

Munzner (2014) proposes four nested layers of visualization design, each validating the layer above it:

**Layer 1 — Domain Problem Characterisation**: Who are the users and what questions do they ask? The threat is solving the wrong problem.

**Layer 2 — Data/Task Abstraction**: What data types are involved (tables, networks, spatial, temporal)? What tasks will the user perform (compare, trend, outlier detection)? The threat is a wrong abstraction — e.g., treating ordinal data as nominal.

**Layer 3 — Visual Encoding / Interaction Idiom**: How will data be mapped to marks and channels? The threat is an ineffective encoding — e.g., using area for precise comparisons.

**Layer 4 — Algorithm Design**: Is the implementation computationally efficient? The threat is slow rendering for large datasets.

Errors at outer layers propagate inward. No amount of visual polish at Layer 3 can fix a chart that answers the wrong question (Layer 1). Validation must proceed outward-in.


### 4. Audience Analysis

Three archetypical personas drive distinct design strategies:

The **executive** wants a single key takeaway in under 10 seconds. Design for this persona with one annotated chart per slide, a bold callout, and a grey-plus-accent colour strategy.

The **analyst** wants to explore the full dataset interactively over 30 minutes. Design with a dashboard grid, full granularity, multi-hue qualitative palettes, and drill-down interactivity.

The **general public** wants to understand the story in about 2 minutes. Design as a curated infographic or article with highlighted data points and narrative flow.


### 5. Chart Selection

The analytical goal determines the chart type:

| Goal         | Chart Types                        |
|--------------|------------------------------------|
| Comparison   | Bar, dot, lollipop                 |
| Distribution | Histogram, density, boxplot        |
| Relationship | Scatter, bubble, hexbin            |
| Composition  | Stacked bar, treemap, waffle       |
| Trend        | Line, area, sparkline              |
| Ranking      | Horizontal bar, bump, slope        |
| Spatial      | Choropleth, point map, hexbin map  |


### 6. Iterative Refinement

Iteration is not optional. The three-stage cycle is:

**Sketch** — Produce a rough, default-styled chart in 30 seconds. The only goal is to see the data structure.

**Draft** — Correct the form: sort categories, flip to horizontal, choose the right chart type, apply a clean palette.

**Polished** — Refine typography (five-level hierarchy), apply colour strategy (grey + accent), add annotations, remove non-data ink, and export as vector PDF.

In R, the pipe operator (`|>`) makes the pipeline explicit: each verb corresponds to one step. In Python, method chaining (`.query().value_counts().head().sort_values()`) serves the same purpose.


### References

- Cairo, A. (2012). *The Functional Art*. New Riders.
- Kirk, A. (2019). *Data Visualisation: A Handbook for Data Driven Design*, 2nd ed. SAGE.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Schwabish, J. (2021). *Better Data Visualizations*. Columbia University Press.
