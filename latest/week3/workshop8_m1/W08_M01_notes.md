# Workshop 8 · Module 1 — Course Notes
## Interactivity Theory: Shneiderman's Mantra

### 1. From Storytelling to Dashboards
Workshop 7 taught author-driven storytelling: static charts with declarative titles, grey+accent, callouts, and a controlled narrative arc. Workshop 8 shifts to the opposite end of the Segel & Heer spectrum (W07-M02): **reader-driven exploration** through interactive visualization and dashboards.

The Martini Glass model frames this transition: W07 was the narrow top (guided narrative), and W08 is the wide bottom (free exploration). In practice, most data products combine both: a presentation deck (W07) followed by a dashboard handoff (W08) where stakeholders can explore the data themselves.

Interactivity is not decoration. It enables the user to answer questions the designer could not anticipate. A static chart answers one question (the one the designer chose). An interactive chart answers many — whichever the user asks through zoom, filter, and details-on-demand.

### 2. Shneiderman's Visual Information Seeking Mantra
Ben Shneiderman (1996) proposed the most influential design principle for interactive visualization: **"Overview first, zoom and filter, then details on demand."** The full mantra has seven steps:

**Step 1 — Overview First**: display the entire dataset at a glance. A scatter plot of all 8,800 Netflix titles, or all 150,000 e-Car loans. The user needs the big picture to decide where to focus. **Never start with a filtered view** — if the first thing the user sees is a subset, they cannot assess what they're missing.

**Step 2 — Zoom**: let the user magnify a region of interest. Scroll-wheel zoom on axes, click-drag zoom box, map tile zoom. Zooming changes the viewport but does not remove data — everything is still there, just out of frame.

**Step 3 — Filter**: let the user remove items that are not relevant to their question. Sliders (date range), checkboxes (Movie/TV Show), dropdowns (country). Filtering changes the dataset itself — items that don't match the criteria disappear from all views.

**Step 4 — Details on Demand**: when the user selects a specific item, show its full details. The most common implementation is the **hover tooltip** — mousing over a point displays its metadata. Click-to-expand panels and detail tables are more elaborate versions.

**Step 5 — Relate**: let the user see relationships between items or views. **Linked brushing**: selecting points in one chart highlights the same points in another. **Cross-filtering**: selecting a category in one panel filters all other panels.

**Step 6 — History**: let the user undo, redo, and compare states. A "Reset" button returns to the overview. Bookmarks save specific filter states for later comparison.

**Step 7 — Extract**: let the user save their findings. Download the current view as PNG. Export the filtered data as CSV. Copy a chart to the clipboard for inclusion in a report. Without extraction, the interactive session is ephemeral.

### 3. Yi et al. (2007): Interaction Taxonomy
Yi, Kang, Stasko, and Jacko (2007) proposed a complementary taxonomy of six interaction types:

**Selection**: clicking a point to highlight it and retrieve its details. This maps to Shneiderman's "details on demand."

**Navigation**: panning, zooming, and rotating the viewport. This maps to "zoom."

**Filtering**: showing or hiding data based on criteria. Sliders, checkboxes, dropdowns. This maps to "filter."

**Reconfiguration**: changing the visual encoding or layout. Switching from bar to line chart, swapping x and y axes, changing the aggregation level.

**Encoding**: adjusting the visual mapping. Changing the colour palette, size scale, or opacity.

**Connection**: linking multiple views. Brushing in one chart highlights in another. Cross-filtering across panels.

### 4. Mapping Interactions to Tools
The W08 toolkit maps interactions to three tool families:

**plotly** (M02–M03): provides selection (hover, click), navigation (zoom, pan), and basic filtering (dropdown menus). Works in both R (`ggplotly()`, `plot_ly()`) and Python (`plotly.express`, `plotly.graph_objects`).

**Shiny** (M04, R) / **Dash** (M05, Python): adds full filtering (sliders, checkboxes, dropdowns as server-side widgets), reconfiguration (user chooses chart type), and connection (linked views through reactive data). These are the full dashboard frameworks.

**Tableau** (external tool): provides all six interaction types through a GUI-based interface. Not covered in depth in this course (license-dependent), but students should be aware of it as an industry-standard tool.

### 5. Static vs Interactive: Decision Framework
Interactivity is not always better. The decision depends on audience, medium, and purpose:

**Use static** (W07) when: the audience is captive (presentation), the medium doesn't support interaction (PDF, email, print), the goal is persuasion (author controls the message), or the audience is non-technical (simplicity > power).

**Use interactive** (W08) when: users have their own questions (self-service analytics), the medium supports interaction (web app, notebook), the goal is exploration (user finds their own insights), or the data is too large/complex for a single static view.

The most common pattern in practice: present the story statically (W07 slides), then hand off an interactive dashboard (W08) for exploration and follow-up.

### 6. Revised W08 Structure
This workshop is restructured from the blueprint to avoid tool-specific modules for unavailable software:

| M | Title | Key Content |
|---|-------|-------------|
| 01 | Interactivity Theory | Shneiderman, Yi taxonomy (this module) |
| 02 | plotly in R | ggplotly, plot_ly, hover, brushing |
| 03 | plotly in Python | plotly.express, go, same patterns |
| 04 | Shiny Fundamentals | UI/server, reactive, inputs/outputs |
| 05 | Dash Fundamentals | Layout, callbacks, components |
| 06 | Dashboard Design | Few's guidelines, KPI, layout grids |
| 07 | Netflix Dashboard | Interactive Netflix case study |
| 08 | e-Car Dashboard | Interactive financial case study |
| 09 | Deployment & Sharing | shinyapps.io, Render, Quarto dashboards |
| 10 | Lab: Build Dashboard | Summative assessment |

### References
- Shneiderman, B. (1996). The Eyes Have It. *Proc. IEEE Visual Languages*.
- Yi, J. S. et al. (2007). Toward a Deeper Understanding of Interaction. *IEEE TVCG*, 13(6).
- Few, S. (2006). *Information Dashboard Design*. Analytics Press.
- Sievert, C. (2020). *Interactive Web-Based Data Visualization with R, plotly, and shiny*. CRC Press.
