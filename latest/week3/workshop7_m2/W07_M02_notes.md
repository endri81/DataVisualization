# Workshop 7 · Module 2 — Course Notes
## Exploratory vs Explanatory Visualization

### 1. Segel & Heer's Narrative Visualization Taxonomy
Segel and Heer (2010) analysed 58 narrative visualizations from journalism, science, and business, identifying a spectrum of narrative control:

**Author-driven** visualizations are linear narratives where the author controls the order, pace, and message. The audience follows a predetermined path from beginning to end. Examples: Knaflic-style slide decks, scrollytelling articles (NYT "Snow Fall"), Hans Rosling's TED talk. Characteristics: low/no interactivity, high messaging control, one intended reading path, works well for persuasion and explanation.

**Reader-driven** visualizations are open exploration environments where the user controls what to see, filter, and investigate. There is no fixed path. Examples: Tableau Public dashboards, Shiny apps, Power BI reports, data portals. Characteristics: high interactivity (filters, drill-down, tooltips), low messaging control (user draws own conclusions), multiple possible reading paths, works well for monitoring and ad-hoc analysis.

**Hybrid** approaches combine elements of both. The most common hybrid is the **Martini Glass** model.

### 2. The Martini Glass Model
The Martini Glass (Segel & Heer, 2010) is a two-phase structure shaped like a martini glass:

**Narrow top (author-driven)**: the presentation begins with a guided narrative — 3–7 slides or scrolled panels that set up context, present key findings, and deliver the main message. The author controls the sequence and emphasis. This is the "storytelling" phase.

**Wide bottom (reader-driven)**: after the narrative, the audience transitions to an interactive exploration environment — a dashboard, interactive chart, or data tool where they can filter, drill down, and ask their own questions. This is the "exploration" phase.

**Transition point**: the critical moment where the author says "Now let me show you the data" or "You can explore further in this dashboard." This transition transfers control from author to reader.

The Martini Glass is the most versatile model for data science communication because it satisfies both needs: stakeholders who want the story (author-driven top) and analysts who want to explore (reader-driven bottom). Practical implementation: present 5 key findings as slides (Quarto/PowerPoint), then open a Shiny/Streamlit/Tableau dashboard for Q&A exploration.

### 3. The Redesign Transformation
The core skill of W07 is transforming an exploratory chart (suitable for analysis) into an explanatory chart (suitable for communication). This transformation involves eight systematic changes:

(1) **Title**: descriptive ("Additions by Type") → declarative ("Movie additions declined 42%"). The title becomes the finding.

(2) **Legend**: remove entirely → replace with direct labels at line endpoints. Eliminates the cognitive load of the legend-to-element lookup.

(3) **Colour**: all series get distinct colours → grey+accent. Only the story line gets colour; everything else is grey context.

(4) **Gridlines**: visible reference grid → minimal or none. The story slide should be clean; the audience doesn't need to read exact values from gridlines.

(5) **Annotations**: none → callouts, arrows, percentage labels, and reference lines. These guide the eye to the specific pattern that IS the story.

(6) **Data density**: show all data → show only what supports the story. Remove series, time periods, or categories that are not part of the narrative.

(7) **Interactivity**: filters and tooltips → static. Story slides are consumed sequentially, not interacted with.

(8) **Subtitle**: metric description ("count of titles by year") → strategic implication ("the content pipeline is contracting").

### 4. When to Use Each Approach
The choice depends on three factors:

**Audience**: captive (presentation, meeting) → author-driven. Self-service (dashboard users, analysts) → reader-driven. Mixed (client deliverable) → Martini Glass.

**Medium**: live presentation → author-driven (you narrate). Emailed report → author-driven (report narrates itself). Interactive web app → reader-driven. Combined deliverable → Martini Glass.

**Goal**: persuade (budget approval, strategy change) → author-driven (control the message). Inform (routine monitoring, KPI tracking) → reader-driven (let users check what they need). Both → Martini Glass (present the case, then hand off the tool).

### 5. Reverse Transformation: Story → Dashboard
Sometimes the opposite transformation is needed — converting an explanatory story slide into a dashboard component:

Restore the legend (user needs to decode independently). Use descriptive title (user chooses what to look at). Add filters (year, country, genre). Add tooltips and hover details. Show more data (multiple metrics, not just the story line). Add gridlines for precise value reading.

This reverse transformation is the focus of **Workshop 8** (Interactive Dashboards), where reader-driven design principles are applied systematically.

### 6. The Segel & Heer Spectrum in Practice
Most real-world data products sit somewhere on the author-reader spectrum rather than at the extremes:

| Product | Spectrum Position | Author Control |
|---------|------------------|----------------|
| NYT scrollytelling | 90% author | Very high |
| Knaflic slide deck | 85% author | High |
| Quarto report + appendix | 70% author | Moderate-high |
| Observable notebook | 50% hybrid | Balanced |
| Tableau Story | 40% hybrid | Moderate |
| Shiny dashboard | 20% reader | Low |
| Open data portal | 5% reader | Minimal |

The Martini Glass occupies the 50–70% range — starting high (guided narrative) and transitioning to low (free exploration).

### References
- Segel, E. & Heer, J. (2010). Narrative Visualization: Telling Stories with Data. *IEEE TVCG*, 16(6), 1139–1148.
- Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
- Kirk, A. (2019). *Data Visualisation: A Handbook*, 2nd ed. Chapter 3.
- Hullman, J. & Diakopoulos, N. (2011). Visualization Rhetoric. *IEEE TVCG*, 17(12).
