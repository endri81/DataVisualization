# Workshop 7 · Module 9 — Course Notes
## Audience Adaptation

### 1. One Finding ≠ One Chart
The same finding requires fundamentally different visual treatment depending on who will see it. A chart designed for a board meeting will fail on social media; a chart designed for a data science team will confuse an executive. This module teaches the six dimensions of adaptation and demonstrates them on both course datasets.

### 2. Three Audience Archetypes

**Executive audience**: time-poor (30 seconds per slide), needs the finding + implication + action, prefers the simplest possible chart (one series, one callout, no gridlines), uses declarative titles (the finding IS the headline), expects business vocabulary (ROI, pipeline, market share), and wants a specific CTA ("approve budget X"). The executive is not interested in your methodology — they trust you did it correctly and want to know what it means.

**Technical audience**: time-rich (5–10 minutes per chart, will scrutinise), needs methodology + uncertainty + reproducibility, prefers detailed charts (multiple series, CI ribbons, facets, raw data points), uses descriptive titles (states what the chart shows, not what it means), expects technical vocabulary (confidence interval, STL decomposition, p-value), and wants methodological recommendations ("use STL instead of moving average"). The technical audience WANTS the complexity that executives don't — but complexity must not become clutter. Show all series and show uncertainty, but keep the chart well-organised.

**Public audience**: time-absent (3 seconds scrolling past on social media), needs immediate understanding with zero cognitive effort, prefers the simplest possible geometry (single bar chart, pictogram, large font), uses conversational titles in everyday language ("Netflix is adding fewer movies"), expects zero jargon, and the "CTA" is simply awareness ("here is what is happening").

### 3. The Six Dimensions of Adaptation

| Dimension | Executive | Technical | Public |
|---|---|---|---|
| **Title style** | Declarative (= finding) | Descriptive (= metric) | Conversational (= plain English) |
| **Chart complexity** | Simple: 1 series, 1 callout | Detailed: multi-series, CI, facets | Very simple: 1 bar, big labels |
| **Annotations** | One key callout (the %) | Multiple: reference lines, CI, labels | None or minimal |
| **Legend** | No (direct labels) | Yes (multiple series) | No (one series or in title) |
| **Jargon** | Business (ROI, pipeline) | Technical (CI, STL, p-value) | None (everyday words) |
| **CTA** | Specific action | Methodological recommendation | Awareness only |

### 4. Medium Adaptation
Beyond audience, the communication **medium** adds a second adaptation layer:

**Live presentation** (projected): large fonts (minimum 18pt), minimal detail (speaker provides context verbally), high contrast (projector washes out subtle colours). Design for 2 metres viewing distance.

**Printed report** (high DPI): can include more detail (reader controls pace), full annotations (no speaker to explain), multiple panels, dense legends. Design for 30cm viewing distance.

**Email attachment**: must be fully self-contained — the title and annotations must tell the complete story because there is no speaker and the recipient may forward it without context.

**Social media** (mobile): must be understood in 3 seconds at thumbnail size, very large fonts, bold colours, minimal data points (≤6), conversational title. Consider vertical aspect ratio for mobile feeds.

**Dashboard** (interactive): descriptive titles, legends, gridlines — the user controls what to look at. This is reader-driven (M02).

### 5. Practical Application: Netflix + e-Car
The module demonstrates all three variants on both datasets:

**Netflix executive**: grey+accent movie line with –42% callout. Title: "Movie additions declined 42% from peak." CTA: "Reallocate budget."

**Netflix technical**: monthly line with 3-month rolling mean ± 1.96σ CI ribbon, both Movie and TV Show series, raw data points, descriptive title, legend. CTA: "Use STL not moving average for seasonal decomposition."

**Netflix public**: simple bar chart of yearly movie additions, big value labels, no jargon. Title: "Netflix is adding fewer movies every year since 2019."

The same exercise applies to e-Car: executive (rate line with crisis callout), technical (tier-stratified rates with all tiers), public (bar chart of yearly rates).

### 6. The Adaptation Workflow
1. **Write the finding** as a single declarative sentence.
2. **Identify the primary audience** (executive, technical, public, or mixed).
3. **Select the adaptation settings** for all six dimensions (title, complexity, annotations, legend, jargon, CTA).
4. **Choose the medium** and adjust resolution, font size, and self-containment.
5. **Produce the variant** — ideally from the SAME script with conditional parameters, so all variants stay in sync when data updates.

### References
- Knaflic, C. N. (2015). *Storytelling with Data*. Chapter 1 (Context: who, what, how).
- Schwabish, J. (2021). *Better Data Visualizations*. Chapter 2 (Know your audience).
- Cairo, A. (2019). *How Charts Lie*. Chapter 1.
- Kirk, A. (2019). *Data Visualisation: A Handbook*, 2nd ed. Chapter 3 (Formulating your brief).
