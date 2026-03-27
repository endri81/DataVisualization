# Workshop 8 · Module 6 — Course Notes
## Dashboard Design Principles

### 1. Tools vs Design
Modules M02–M05 taught the tools (plotly, Shiny, Dash). This module teaches the design principles that make dashboards effective regardless of the tool. A beautifully coded Shiny app with poor layout is worse than a well-designed Excel dashboard. Design comes first; implementation follows.

### 2. Few's Six Rules for Dashboard Design
Stephen Few's *Information Dashboard Design* (2006, 2013) provides the most widely adopted framework. Six rules:

**Rule 1 — Fit on one screen**: a dashboard that requires scrolling is a report, not a dashboard. The power of a dashboard is that the user sees all panels simultaneously, enabling cross-comparison and pattern detection. Design for 1920×1080 (standard desktop), test at 1366×768 (common laptop). If content overflows, reduce chart count or use tabs — do not add a scrollbar.

**Rule 2 — KPIs at the top**: the first thing the user sees should be the key numbers — total titles (8,807), movies (6,131), TV shows (2,676), countries (78). Each KPI card shows three elements: the big number (current value), the delta (change from reference: +12.3% vs last year), and optionally a sparkline (tiny trend line, no axes). KPIs answer "what is the current state?" in 2 seconds. Charts below answer "why?" and "how did we get here?"

**Rule 3 — Maximum 5–7 charts**: more than 7 charts on a single view overwhelms the user (cognitive load). If you have 12 analyses to show, use tabs or progressive disclosure (detail panels that expand on click). Prioritise ruthlessly: which 5–7 charts answer the most important questions?

**Rule 4 — Consistent colour across panels**: if "Movie" is blue in one chart, it must be blue in every chart. Define a global palette (`PALETTE = {"Movie": "#1565C0", "TV Show": "#E53935"}`) and apply it everywhere. Inconsistent colour forces the user to re-learn the encoding for each panel.

**Rule 5 — Filter sidebar**: all input widgets (dropdowns, sliders, checkboxes) should be grouped in a sidebar (left) or top bar. Never scatter inputs among the charts — the user needs to know where to find the controls without hunting.

**Rule 6 — Descriptive titles**: dashboards are reader-driven (M02). Use descriptive titles ("Yearly Additions by Type") not declarative titles ("Movie additions declined 42%"). The user draws their own conclusions; the dashboard provides the data.

### 3. The Layout Grid
The dashboard layout follows a hierarchy that matches the Z-pattern of web reading (Nielsen, 2006):

**Row 1 — Title + global filters**: dashboard name, date range selector, primary category filter. This is the "control bar" — always visible, always at the top.

**Row 2 — KPI cards (3–5)**: big numbers summarising the current state. These answer "how are we doing?" at a glance. Design as cards: value + delta + label. Optionally include a sparkline.

**Row 3 — Primary + secondary chart**: the primary chart (left, larger) shows the most important trend or comparison. The secondary chart (right, smaller) provides supporting context. Together they answer "what's happening?"

**Row 4 — Detail panels (2–3)**: drill-down tables, sparkline grids, or small supporting charts. These answer "what are the specifics?" and are the least prominent visual element.

The most important information is top-left; least important is bottom-right.

### 4. KPI Card Design
A KPI card has three elements:

**Big number**: the current value, large and bold. This is the first thing the eye hits. Use `format(n, big.mark = ",")` for readability.

**Delta**: the change from a reference point (last period, target, or average). Colour-coded: green (#2E7D32) for positive, red (#C62828) for negative. Include the direction symbol (↑ or ↓) for colour-blind accessibility.

**Sparkline** (optional): a tiny line chart showing the recent trend. No axes, no labels — just the shape of the trend. This provides temporal context without taking significant space.

In Shiny: `shinydashboard::valueBox()` or custom `renderUI()`. In Dash: `dbc.Card(dbc.CardBody([html.H3(value), html.P(delta)]))`.

### 5. Story Slide vs Dashboard: Design Differences
These are fundamentally different design contexts (M02):

| Element | Story Slide (W07) | Dashboard (W08) |
|---|---|---|
| Title | Declarative (= finding) | Descriptive (= metric) |
| Charts per view | 1 (full-width) | 5–7 (grid layout) |
| Legend | No (direct labels) | Yes (user decodes independently) |
| Gridlines | No (minimal) | Yes (user reads exact values) |
| Annotations | Heavy (callouts, arrows) | Light (hover tooltips) |
| Colour | Grey + accent | Consistent palette |
| Audience mode | Author-driven | Reader-driven |

### 6. Five Anti-Patterns
(1) **Chartjunk dashboard**: 3D effects, gradients, decorative borders → fix with flat, minimal, data-ink-focused design. (2) **Scroll-of-death**: 20+ charts in a vertical scroll → max 5–7, use tabs for additional content. (3) **Colour chaos**: different colour palettes per panel → global palette. (4) **No KPIs**: jumping straight to charts without summary → add KPI card row at top. (5) **Filter everywhere**: inputs scattered inline with charts → consolidate in sidebar or top bar.

### References
- Few, S. (2006). *Information Dashboard Design*. Analytics Press.
- Few, S. (2013). *Information Dashboard Design*, 2nd ed.
- Wexler, S. et al. (2017). *The Big Book of Dashboards*. Wiley.
- Nielsen, J. (2006). "F-Shaped Pattern." Nielsen Norman Group.
