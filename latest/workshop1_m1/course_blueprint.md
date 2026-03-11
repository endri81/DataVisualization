# Data Visualization — NYT Style
## Master Course Blueprint: 9 Workshops × 10 Modules × ~30 Slides

**Based on**: SMM635 Data Visualization (Bayes Business School)  
**Expanded by**: Lead Curriculum Developer  
**Approach**: Comparative R (ggplot2) ↔ Python (seaborn/plotnine), DataCamp pedagogy  
**Total Slides**: ~2,700 (9 workshops × ~300 slides)

---

## PHASE 1: FOUNDATIONS (Workshops 1–3) → Course Project 1

### Workshop 1 — Principles of Visual Design & Perception (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Why Visualize? The Case for Data Viz | 30 | Information overload, Anscombe's quartet, Datasaurus Dozen, historical examples (Minard, Nightingale, Snow) |
| M02 | Tufte's Principles of Graphical Excellence | 30 | Data-ink ratio, chartjunk, lie factor, small multiples, sparklines |
| M03 | Visual Perception & Pre-Attentive Attributes | 30 | Gestalt laws, pre-attentive processing, Weber's law, change blindness |
| M04 | Color Theory & Accessibility | 30 | Sequential/diverging/qualitative palettes, colorblindness, WCAG, viridis, ColorBrewer |
| M05 | Typography, Layout & Composition | 30 | Hierarchy, whitespace, grid systems, annotation best practices |
| M06 | The Design Process: From Data to Display | 30 | Cairo's functional art model, Munzner's nested model, design thinking for viz |
| M07 | Critique & Redesign Workshop | 30 | Before/after case studies, redesign methodology, peer review protocols |
| M08 | R Environment Setup & Base Graphics | 30 | RStudio, tidyverse ecosystem, base R plot(), par() system |
| M09 | Python Environment Setup & Matplotlib Basics | 30 | Jupyter, pandas, matplotlib figure/axes model, pyplot vs OO interface |
| M10 | Comparative Lab: First Plots in R vs Python | 30 | Side-by-side bar, scatter, line in both languages using Google Play Store data |

**Homework W01**: Redesign a "bad" visualization from the wild (find + critique + redesign in R and Python)  
**R Script**: `W01_scripts/viz_principles_demo.R`  
**Python Script**: `W01_scripts/viz_principles_demo.py`

---

### Workshop 2 — The Grammar of Graphics (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Wilkinson's Grammar of Graphics: Theory | 30 | The seven layers, algebra of graphics, specification vs implementation |
| M02 | Wickham's Layered Grammar & ggplot2 | 30 | aes(), geom_, stat_, scale_, coord_, facet_, theme_ |
| M03 | ggplot2 Deep Dive: Aesthetics & Geometries | 30 | Mapping vs setting, position adjustments, geom catalog |
| M04 | ggplot2 Deep Dive: Scales & Coordinates | 30 | scale_*_continuous/discrete/manual, coord_flip/polar/map |
| M05 | ggplot2 Deep Dive: Faceting & Themes | 30 | facet_wrap, facet_grid, theme_minimal/classic/void, custom themes |
| M06 | plotnine: ggplot2 in Python | 30 | Grammar parity, syntax comparison, pandas integration |
| M07 | seaborn: Statistical Visualization | 30 | Figure-level vs axes-level, FacetGrid, PairGrid, catplot/relplot/displot |
| M08 | Comparing Approaches: R vs Python GoG | 30 | Same plot in ggplot2, plotnine, seaborn, matplotlib — tradeoffs |
| M09 | Customization Masterclass | 30 | Publication themes, corporate branding, export formats (SVG, PDF, PNG) |
| M10 | Lab: Building a Visual Report | 30 | End-to-end exercise with Google Play Store data, complete styled report |

**Homework W02**: Create a "Grammar of Graphics Cheat Sheet" — implement 15 chart types using GoG layers in R + Python  
**R Script**: `W02_scripts/gog_ggplot2.R`  
**Python Script**: `W02_scripts/gog_plotnine_seaborn.py`

---

### Workshop 3 — Chart Types & Visual Forms Encyclopedia (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Distributions: Histograms, Density, Ridgeline | 30 | Bin width, bandwidth, ggridges, KDE theory |
| M02 | Distributions: Boxplots, Violins, Beeswarm | 30 | Quartile mechanics, jitter, ggbeeswarm, raincloud plots |
| M03 | Comparisons: Bar Charts, Lollipop, Cleveland Dot | 30 | Sorted bars, grouped vs stacked, horizontal best practices |
| M04 | Relationships: Scatter, Bubble, Hexbin | 30 | Overplotting, alpha, size encoding, 2D density |
| M05 | Proportions: Pie, Donut, Treemap, Waffle | 30 | When pies work, alternatives, treemapify, waffle package |
| M06 | Rankings & Part-to-Whole: Slope, Bump, Waterfall | 30 | Slopegraph, bump chart, ggbump, waterfall charts |
| M07 | Uncertainty: Error Bars, Confidence, Gradient | 30 | Pointrange, ribbon, hypothetical outcome plots |
| M08 | Small Multiples & Faceted Displays | 30 | Trellis philosophy, patchwork, cowplot, gridExtra |
| M09 | Tables as Visualization: gt, kableExtra, great_tables | 30 | Conditional formatting, sparklines in tables, data tables |
| M10 | Lab: Chart Selection Decision Framework | 30 | Flowchart for choosing charts, apply to Netflix dataset |

**Homework W03**: Visualize the Netflix dataset using ≥8 distinct chart types in R and Python  
**R Script**: `W03_scripts/chart_types_R.R`  
**Python Script**: `W03_scripts/chart_types_python.py`

### ★ COURSE PROJECT 1: Visual Redesign Portfolio
**Scope**: Select 5 published visualizations (news media, academic papers, corporate reports). For each: (a) critique using Tufte's principles, (b) redesign in R, (c) redesign in Python, (d) write a 300-word rationale.  
**Deliverable**: PDF portfolio + reproducible R and Python scripts  
**Data**: Self-sourced or provided datasets  
**Due**: End of Workshop 3 week

---

## PHASE 2: ANALYSIS (Workshops 4–6) → Course Project 2

### Workshop 4 — Exploratory Data Analysis (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Tukey's EDA Philosophy | 30 | Confirmatory vs exploratory, detective metaphor, stem-and-leaf, letter-value |
| M02 | Data Wrangling for Visualization (R) | 30 | dplyr verbs, tidyr reshaping, lubridate, stringr |
| M03 | Data Wrangling for Visualization (Python) | 30 | pandas operations, melt/pivot, datetime, string methods |
| M04 | Missing Data Visualization | 30 | naniar, visdat (R); missingno (Python); patterns of missingness |
| M05 | Outlier Detection & Visual Diagnostics | 30 | IQR, Mahalanobis, cook's distance, leverage plots |
| M06 | Correlation & Association Visualization | 30 | corrplot, ggcorrplot (R); heatmap, clustermap (Python) |
| M07 | EDA Case Study: Google Play Store (R) | 30 | Complete walkthrough: import → clean → explore → insight |
| M08 | EDA Case Study: Google Play Store (Python) | 30 | Same analysis, Python idioms, comparison of workflows |
| M09 | EDA Case Study: e-Car Loan Pricing (R) | 30 | Nomis Solutions dataset, pricing analysis, segmentation |
| M10 | EDA Case Study: e-Car Loan Pricing (Python) | 30 | Same e-Car analysis in Python |

**Homework W04**: Perform complete EDA on the CRM (Crop Residue Management) dataset in R and Python  
**R Script**: `W04_scripts/eda_googleplay.R`, `W04_scripts/eda_ecar.R`  
**Python Script**: `W04_scripts/eda_googleplay.py`, `W04_scripts/eda_ecar.py`

---

### Workshop 5 — Multivariate & Spatial Visualization (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | High-Dimensional Data: Challenges & Strategies | 30 | Curse of dimensionality, visual encoding channels, aggregation |
| M02 | Parallel Coordinates & Radar Charts | 30 | GGally::ggparcoord (R), plotly parallel (Python), radar/spider |
| M03 | Dimensionality Reduction Visualization | 30 | PCA biplots, t-SNE, UMAP — visual interpretation |
| M04 | Heatmaps & Clustered Displays | 30 | pheatmap, ComplexHeatmap (R); seaborn clustermap (Python) |
| M05 | Introduction to Spatial Data | 30 | Coordinate reference systems, shapefiles, GeoJSON, sf package |
| M06 | Choropleth Maps (R) | 30 | tmap, ggplot2 + sf, leaflet for interactive |
| M07 | Choropleth Maps (Python) | 30 | geopandas, folium, plotly.express.choropleth |
| M08 | Point Maps & Spatial Patterns | 30 | KDE maps, hexbin maps, cartograms |
| M09 | Case: Saving Lives with Data (Cholera Maps) | 30 | Snow's map, modern GIS recreation, public health viz |
| M10 | Lab: Multivariate EDA on Real Estate Data | 30 | real_estate.xlsx — PCA, maps, heatmaps in R and Python |

**Homework W05**: Recreate John Snow's cholera map using modern tools (R + Python), add interactive version  
**R Script**: `W05_scripts/multivariate_R.R`, `W05_scripts/spatial_R.R`  
**Python Script**: `W05_scripts/multivariate_python.py`, `W05_scripts/spatial_python.py`

---

### Workshop 6 — Time Series & Temporal Visualization (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Time as a Visual Dimension | 30 | Temporal granularity, periodicity, trend/season/residual |
| M02 | Line Charts: Theory & Best Practices | 30 | Aspect ratio (banking to 45°), dual axes debate, indexed lines |
| M03 | Line Charts in R (ggplot2 + scales) | 30 | date scales, breaks, labels, geom_line, geom_step, geom_area |
| M04 | Line Charts in Python (matplotlib + pandas) | 30 | DateFormatter, date_range, fill_between, area charts |
| M05 | Sparklines & Small Temporal Multiples | 30 | Tufte's sparklines, ggplot2 facets for time, panel dashboards |
| M06 | Seasonal & Calendar Visualizations | 30 | Heatmap calendars, seasonal subseries, polar time plots |
| M07 | Animation: gganimate (R) | 30 | transition_time, transition_states, shadow_wake, rendering |
| M08 | Animation: matplotlib.animation (Python) | 30 | FuncAnimation, bar chart races, animated scatter |
| M09 | Case: Netflix Content Trends Over Time | 30 | Temporal EDA of Netflix catalog: releases, genres, countries |
| M10 | Lab: Animated Time Series Dashboard | 30 | Build animated viz of e-Car loan approvals over time |

**Homework W06**: Build animated "bar chart race" of Netflix content by country (R + Python)  
**R Script**: `W06_scripts/timeseries_R.R`, `W06_scripts/animation_R.R`  
**Python Script**: `W06_scripts/timeseries_python.py`, `W06_scripts/animation_python.py`

### ★ COURSE PROJECT 2: Multidimensional EDA Report
**Scope**: Analyze the e-Car loan pricing dataset (Nomis Solutions). Produce a 15-page visual EDA report with: (a) univariate profiles, (b) bivariate relationships, (c) multivariate analysis (PCA, heatmaps), (d) temporal trends, (e) actionable pricing recommendations.  
**Deliverable**: PDF report + R and Python scripts  
**Data**: `data/ecar.csv`  
**Due**: End of Workshop 6 week

---

## PHASE 3: COMMUNICATION (Workshops 7–9) → Course Project 3

### Workshop 7 — Storytelling with Data (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Narrative Structure in Data Communication | 30 | Knaflic's framework, story arc, setup-conflict-resolution |
| M02 | Exploratory vs Explanatory Visualization | 30 | Author-driven vs reader-driven, Segel & Heer taxonomy |
| M03 | Annotation, Emphasis & Focus | 30 | Direct labeling, callouts, highlighting, de-emphasis |
| M04 | Annotation in R (ggplot2 + ggtext) | 30 | annotate(), geom_text/label, ggrepel, ggtext markdown |
| M05 | Annotation in Python (matplotlib + adjustText) | 30 | ax.annotate(), arrow props, text boxes, adjustText |
| M06 | Color as Narrative Device | 30 | Strategic color: grey + accent, sequential narrative, NYT style |
| M07 | Case: Crop Residue Management — Data Story | 30 | Full storytelling exercise: survey data → insight → narrative |
| M08 | The Seven Basic Data Stories | 30 | Change over time, drilldown, zoom-out, contrast, intersections, factors, outliers |
| M09 | Presentation Design for Data Stories | 30 | Slide layout, progressive reveal, assertion-evidence model |
| M10 | Lab: Build a Data Story Deck | 30 | Create 10-slide explanatory deck from CRM data |

**Homework W07**: Write a "data story memo" (1,500 words + 5 annotated charts) on CRM dataset insights  
**R Script**: `W07_scripts/storytelling_R.R`  
**Python Script**: `W07_scripts/storytelling_python.py`

---

### Workshop 8 — Interactive Visualization & Dashboards (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Interactivity Theory: Shneiderman's Mantra | 30 | Overview, zoom, filter, details-on-demand, history, relate, extract |
| M02 | plotly in R (ggplotly + plot_ly) | 30 | Hover, zoom, pan, linked brushing, animations |
| M03 | plotly in Python (plotly.express + go) | 30 | Same interactivity patterns, Dash teaser |
| M04 | Shiny Fundamentals (R) | 30 | UI/server, reactive, inputs/outputs, deployment |
| M05 | Dash Fundamentals (Python) | 30 | Layout, callbacks, dcc/html components, deployment |
| M06 | Dashboard Design Principles | 30 | Few's dashboard guidelines, KPI design, layout grids |
| M07 | Tableau Fundamentals (Part 1) | 30 | Data connection, pill model, marks card, chart building |
| M08 | Tableau Fundamentals (Part 2) | 30 | Calculated fields, parameters, filters, reference lines |
| M09 | Tableau Dashboards & Story Points | 30 | Dashboard layout, actions, device designer, stories |
| M10 | Case: Toby Biotech Receivables Dashboard | 30 | Accounting visualization, risk assessment, Tableau dashboard |

**Homework W08**: Build an interactive Shiny app (R) or Dash app (Python) for the Netflix dataset  
**R Script**: `W08_scripts/interactive_R.R`, `W08_scripts/shiny_app.R`  
**Python Script**: `W08_scripts/interactive_python.py`, `W08_scripts/dash_app.py`

---

### Workshop 9 — Advanced Topics & Professional Practice (~300 slides)

| Module | Title | Slides | Key Content |
|--------|-------|--------|-------------|
| M01 | Network Visualization | 30 | igraph, ggraph (R); networkx, pyvis (Python); force-directed |
| M02 | Text & NLP Visualization | 30 | Word clouds, TF-IDF heatmaps, topic model viz, sentiment plots |
| M03 | Hierarchical Data: Treemaps & Sunbursts | 30 | treemap, sunburstR (R); squarify, plotly sunburst (Python) |
| M04 | Publication-Quality Figures | 30 | Journal specs, multi-panel figures, patchwork/cowplot, vector export |
| M05 | Reproducible Visualization Workflows | 30 | RMarkdown, Quarto, Jupyter → reports, parameterized reports |
| M06 | Performance & Large Data Visualization | 30 | Sampling, aggregation, datashader, scattermore, WebGL |
| M07 | Ethics in Data Visualization | 30 | Misleading charts, truncated axes, cherry-picking, responsibility |
| M08 | The NYT Graphics Style: A Case Study | 30 | Deconstructing NYT visual journalism, style replication |
| M09 | Case: Market Street Wine — Dashboard Decision | 30 | Wine assortment problem, geographic viz, Tableau dashboard |
| M10 | Lab: Portfolio Review & Professional Presentation | 30 | Final presentation prep, code review, portfolio assembly |

**Homework W09**: Produce 3 publication-quality figures + 1 interactive dashboard for portfolio  
**R Script**: `W09_scripts/advanced_R.R`, `W09_scripts/network_R.R`  
**Python Script**: `W09_scripts/advanced_python.py`, `W09_scripts/network_python.py`

### ★ COURSE PROJECT 3: Capstone — Persuasive Dashboard
**Scope**: Real estate development case (Flying Around Real Estate Development, UVA-BC-0285). Build: (a) static explanatory report (R/Python, 10 annotated charts), (b) interactive Shiny/Dash dashboard, (c) 5-minute video presentation.  
**Deliverable**: PDF report + interactive app + recorded presentation + all code  
**Data**: `data/real_estate.xlsx`  
**Due**: End of Workshop 9 week

---

## Cross-Cutting Elements

### Datasets Used Across Workshops
| Dataset | File | Workshops | Purpose |
|---------|------|-----------|---------|
| Google Play Store | `googleplaystore.csv` | W01–W03 | GoG, chart types, univariate/bivariate |
| Google Play Reviews | `googleplaystore_user_reviews.csv` | W02, W09 | Text viz, sentiment |
| Netflix | `netflix.csv` | W03, W06, W08 | Temporal, categorical, dashboards |
| e-Car Loans | `ecar.csv` | W04, W06 | EDA, pricing analysis, time series |
| CRM Survey | `crm.xlsx` | W04, W07 | Missing data, storytelling |
| Real Estate | `real_estate.xlsx` | W05, W09 | Spatial, multivariate, capstone |

### Assessment Weighting
| Component | Weight | Due |
|-----------|--------|-----|
| Workshop Homeworks (9 × 5%) | 45% | Weekly |
| Course Project 1 | 10% | End W03 |
| Course Project 2 | 20% | End W06 |
| Course Project 3 (Capstone) | 25% | End W09 |

### Essential Readings (Cumulative)
1. Tufte, E. R. (1983). *The Visual Display of Quantitative Information*
2. Cairo, A. (2012). *The Functional Art*
3. Wilkinson, L. (2005). *The Grammar of Graphics*
4. Wickham, H. (2010). "A Layered Grammar of Graphics," *JCGS*
5. Healy, K. (2024). *Data Visualization: A Practical Introduction*
6. Knaflic, C. N. (2015). *Storytelling with Data*
7. Munzner, T. (2014). *Visualization Analysis and Design*
8. Few, S. (2006). *Information Dashboard Design*
9. Wilke, C. O. (2019). *Fundamentals of Data Visualization*

---

## Generation Protocol

Each module is generated on request: "Generate Workshop W, Module M."  
Output: LaTeX Beamer file (~30 frames) following `Latex_Boilerplate.tex` and `Style_Guide.txt`.  
Constraints:
- Metropolis theme, `[fragile]` on all code frames
- Comparative approach: R slide → Python slide
- Max 4 bullets per slide
- `\includegraphics[width=\textwidth]{placeholder}` for all plots
- Two-column layouts for code vs output
- `exampleblock{Data Insight}` for interpretations
- `alertblock{Pro-Tip}` for syntax warnings
