# Workshop 6 · Module 4 — Course Notes
## Sparklines & Small Temporal Multiples

### 1. The Spaghetti Problem
When more than 4–5 lines share a single chart panel, the result is "spaghetti" — a tangle of coloured lines where no individual pattern is readable. The eye cannot track more than ~4 distinct lines simultaneously. Two solutions exist: **small temporal multiples** (separate panels) and **sparklines** (compact, axis-free strips). Both decompose the multi-line problem into separately readable units.

### 2. Small Temporal Multiples
Small multiples (Tufte, 1983) display the same chart type for multiple groups in a grid of panels. For temporal data, this means one time series panel per group — same x-axis (time), same chart geometry (line), differing only in the data subset shown.

Key design decisions:

**Shared x-axis**: Always share the x-axis across all panels in a temporal grid. This ensures that peaks, troughs, and events align vertically, enabling direct temporal comparison. In R: `facet_wrap()` shares x by default. In Python: `plt.subplots(sharex=True)`.

**Free vs fixed y-axis**: This is the most important choice. `scales = "free_y"` (R) or individual `set_ylim()` (Python) lets each panel use its own y range — optimising the visual space for each genre's individual pattern. This reveals relative trends (which months are high/low for each genre) but hides magnitude differences (one genre may have 10× the volume of another). `scales = "fixed"` uses the same y range for all panels — revealing absolute magnitude but compressing low-volume genres into nearly flat lines. **Recommendation**: produce both and compare. Free-y for pattern analysis; fixed-y for magnitude comparison.

**Panel count**: 4–12 panels work well on a standard slide or A4 page. Beyond 12, panels become too small. For 12+ groups, consider sparklines or aggregate small groups into "Other."

**Panel layout**: `ncol = 3` is typical for 6 panels (2×3 grid). Choose `ncol` to give each panel a landscape aspect ratio (wider than tall) — time series are usually wider than they are tall because the x-axis (time) spans a longer range than the y-axis.

In R: `ggplot(aes(x = date, y = value)) + facet_wrap(~group, ncol = 3, scales = "free_y")` — one line of code replaces a spaghetti chart. In Python: `fig, axes = plt.subplots(nrows, ncols, sharex=True)` + a loop over groups and axes.

### 3. Highlighted Multiples
A hybrid of grey+accent (M02) and small multiples: show **all** series as light grey in **every** panel, but highlight the focal series in a saturated colour. This preserves the multi-panel structure while providing context — each panel answers "how does this genre compare to all others?"

Implementation: in R, overlay `geom_line()` twice — first for all data (grey), then for the focal group (red). The trick is generating the "all-genres-in-every-panel" data, which requires either `cross_join()` or creating a separate data frame that repeats all genres within each facet.

In Python: loop over panels, and within each panel, loop over all genres (grey), then plot the focal genre (red) on top.

### 4. Sparklines (Tufte, 2006)
Sparklines are "word-sized graphics" — tiny time series charts designed for embedding in text, tables, or dashboards. They strip away everything non-essential: no axes, no labels, no gridlines, no title. What remains is pure shape — the trajectory, volatility, and current position.

Convention marks three points: **minimum** (red dot), **maximum** (green dot), and **current/latest** value (blue dot with numeric label). A subtle fill below the line adds visual weight without distracting from the shape.

Sparklines answer "what is the general trend?" at a glance, for many series simultaneously. They are ideal for: dashboard summary rows (one sparkline per KPI), summary tables in reports (one sparkline per category), and any context where 10–50 trends must be scanned quickly without detailed analysis.

**Critical limitation**: sparklines sacrifice precision for density. The reader cannot determine exact values, slopes, or timing. They are for overview, not analysis. If the reader needs to ask "exactly when did the peak occur?" or "what was the value in July?", use small multiples instead.

In R: the `gtExtras` package provides `gt_sparkline()` which embeds ggplot sparklines directly in `gt` tables — the most professional solution. Manual approach: `facet_wrap(ncol = 1, strip.position = "left") + theme_void()`. In Python: a loop of `ax.plot()` calls on `plt.subplots(n, 1)` with `ax.axis("off")` for each panel.

### 5. Decision Framework
The choice between multi-line, small multiples, and sparklines depends on the communication goal:

| Scenario | Series Count | Goal | Best Chart |
|----------|-------------|------|------------|
| Revenue by product | 2–4 | Show crossover | Multi-line |
| Genre trends | 6–12 | Individual patterns | Small multiples |
| Genre + context | 6–12 | Focal vs others | Highlighted multiples |
| Dashboard KPIs | 10–50 | Quick overview | Sparklines |
| Monitoring sensors | 50+ | Anomaly detection | Sparklines + alerting |

### 6. Free-y vs Fixed-y: The Hidden Decision
This deserves special emphasis because it fundamentally changes the story. A free-y sparkline for "Medical" apps might show dramatic growth — but on a fixed-y scale, Medical's volume is negligible compared to Games. Both are true; they answer different questions. **Always state which scale you're using and why.** For presentations: free-y (each genre's story). For executive dashboards: fixed-y (where is the volume?).

### References
- Tufte, E. (2006). *Beautiful Evidence*. Graphics Press. (Original sparklines chapter.)
- Tufte, E. (1983). *The Visual Display of Quantitative Information*. (Small multiples.)
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Ch. 21 (Multi-panel figures).
- gtExtras: https://jthomasmock.github.io/gtExtras/ (R sparkline tables)
