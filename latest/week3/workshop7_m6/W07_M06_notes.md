# Workshop 7 · Module 6 — Course Notes
## Declutter & Redesign

### 1. Data-Ink Ratio Revisited
W01-M04 introduced Tufte's data-ink ratio conceptually. This module applies it as a **practical audit tool**: examine every element on your chart and ask "does removing this element reduce the reader's understanding?" If removing it changes nothing, remove it. If it reduces understanding, keep it. This is not minimalism for aesthetics — it is clarity through subtraction.

The common failure is "decoration by default": software like Excel adds gridlines, borders, background fills, 3D effects, and shadows automatically. Most of these defaults serve no analytical purpose and actively harm comprehension by competing with the data for the viewer's attention.

### 2. The Six Most Common Clutter Offenders
(1) **Heavy borders and box frames**: chart borders, axis boxes, legend borders. These draw the eye to the container rather than the content. Remove all borders; let the data define the space. (2) **Gridlines on both axes**: gridlines on one axis (usually y) can help read values in dashboards, but gridlines on both axes create a prison-cell effect. Remove minor gridlines always; remove major gridlines on story slides. (3) **3D effects, shadows, and bevels**: never add visual depth to 2D data. 3D bars distort area perception. Drop shadows are pure decoration. (4) **Redundant data labels**: labelling every bar or point creates visual noise. Label only the key data points (the peak, the callout, the endpoint). (5) **Decorative colour fills**: using different bright colours for every category when the distinction doesn't matter. Use grey for context and one accent colour for the story. (6) **Rotated axis labels**: if labels don't fit horizontally, the chart orientation is wrong. Flip to horizontal bars or abbreviate.

### 3. The 12-Step Makeover
The module's central demonstration transforms a deliberately cluttered chart into a clean explanatory visual through 12 specific changes. These 12 steps constitute a reusable checklist:

| Step | Element | Before | After |
|------|---------|--------|-------|
| 1 | Chart type | Grouped bar | Line (continuous data) |
| 2 | Title | Descriptive | Declarative (= the finding) |
| 3 | Legend | Box with shadow | Direct labels at endpoints |
| 4 | Borders | Heavy black lines | Removed entirely |
| 5 | Gridlines | Both axes, grey | Removed |
| 6 | Data labels | On every bar | Only the % callout |
| 7 | Background | Grey fill | White |
| 8 | Axis labels | Verbose | Minimal, muted colour |
| 9 | Colour | Two bright colours | Grey + one accent |
| 10 | Bar edges | Black outlines | None |
| 11 | Source line | Long, distracting | Removed or minimal |
| 12 | Spines | All 4, thick | Left + bottom, light grey |

### 4. Theme Engineering
Rather than decluttering each chart individually, set clean defaults that apply globally:

**R**: Create a `theme_clean` object and apply with `theme_set(theme_clean)`. Key elements: `panel.grid = element_blank()`, `axis.line = element_line(color = "#EEEEEE")`, `plot.title = element_text(face = "bold")`. Every subsequent `ggplot()` call inherits these settings.

**Python**: Update `plt.rcParams` with clean defaults: `"axes.spines.top": False`, `"axes.spines.right": False`, `"axes.edgecolor": "#EEEEEE"`, `"grid.alpha": 0`. Alternatively, use `plt.style.context("seaborn-v0_8-whitegrid")` as a starting point.

### 5. When Clutter Is Acceptable
The declutter rule is contextual, not absolute. Reader-driven contexts (dashboards, reference tables, scientific multi-panel figures) may require elements that would be clutter in a story slide:

**Dashboards**: gridlines help users read exact values without a narrator. Legends are necessary because there is no speaker to explain. Descriptive titles tell the user what the chart shows (they decide what it means).

**Scientific figures**: multiple panels with shared legends, axis labels on every panel, and dense annotations serve expert readers who will study the figure for minutes, not glance for seconds.

**Small multiples**: minimal per-panel formatting is acceptable because the grid structure itself provides the organising context.

The rule is not "always minimise" but "every element must earn its place." In a story slide for a board meeting, gridlines do not earn their place. In a monitoring dashboard, they do.

### 6. Incremental Declutter Process
For beginners, the 12-step transformation can feel overwhelming. An incremental approach works better:

**Stage 0**: the raw output from your plotting code (maximum clutter).
**Stage 1**: remove the most egregious elements — borders, background fill, 3D effects, shadows. Takes 30 seconds.
**Stage 2**: change the chart type if needed (bars → lines for time series), remove gridlines. Takes 2 minutes.
**Stage 3**: apply grey+accent colouring, replace legend with direct labels, add the declarative title and one callout. Takes 5 minutes.

Total transformation time: ~8 minutes. The payoff in clarity and persuasiveness is enormous.

### References
- Tufte, E. (2001). *The Visual Display of Quantitative Information*, 2nd ed. Chapter 6.
- Knaflic, C. N. (2015). *Storytelling with Data*. Chapter 3 ("Clutter is your enemy!").
- Schwabish, J. (2021). *Better Data Visualizations*. Chapter 5 (Declutter).
- Few, S. (2012). *Show Me the Numbers*, 2nd ed. Chapter 5 (Design principles).
