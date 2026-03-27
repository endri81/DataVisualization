# Workshop 8 · Module 3 — Course Notes
## plotly in Python: Interactive Charts

### 1. The Python plotly Ecosystem
Python's plotly library has three layers of increasing control:

**plotly.express (px)**: high-level, DataFrame-oriented API. One function call creates a complete interactive chart: `px.line(df, x="col1", y="col2", color="group")`. Automatic legends, hover tooltips, zoom, pan. Best for: quick EDA, Jupyter notebooks, and prototyping. Comparable to R's `ggplotly()` in convenience but with a different syntax.

**plotly.graph_objects (go)**: low-level, trace-based API. You create a `go.Figure()` and add individual traces (`go.Scatter`, `go.Bar`, `go.Heatmap`). Full control over every visual property: `hovertemplate`, `updatemenus`, annotations, shapes. Best for: production dashboards, custom layouts. Comparable to R's `plot_ly()`.

**plotly.subplots (make_subplots)**: creates multi-panel figures with optional shared axes. `make_subplots(rows=2, cols=1, shared_xaxes=True)` creates a two-row layout where zooming one panel zooms both. Comparable to R's `subplot()`.

**Dash** (covered in M05): a full web application framework built on top of plotly. Adds server-side callbacks, layout components, and deployment. This is where linked brushing and complex filtering happen in Python (since there's no `crosstalk` equivalent).

### 2. plotly.express (px) — The Fast Path
px provides ~30 chart types as single function calls:

**px.line()**: `px.line(df, x="year", y="n", color="type", markers=True)`. Creates an interactive line chart with automatic legend, hover, zoom, and pan. The `color` parameter creates one trace per group.

**px.scatter()**: `px.scatter(df, x="x", y="y", color="type", hover_name="title", hover_data={"rating": True})`. The `hover_name` parameter makes the specified column bold in the tooltip header. The `hover_data` dict controls which columns appear in the tooltip body.

**px.bar()**: `px.bar(df, x="category", y="value", color="group", barmode="group")`. Creates grouped or stacked bar charts.

**Common parameters**: `color_discrete_map={"A": "#1565C0"}` for custom colours, `opacity=0.5` for transparency, `facet_col="country"` for small multiples, `animation_frame="year"` for animations, `template="plotly_white"` for clean background.

### 3. plotly.graph_objects (go) — Full Control
Switch from px to go when you need:

**Custom hovertemplate**: `hovertemplate="<b>Movie</b><br>Year: %{x}<br>Titles: %{y:,}<extra></extra>"`. The `%{x}` and `%{y}` reference trace data. The `:,` format adds comma separators. The `<extra></extra>` tag suppresses the secondary tooltip box.

**Annotations**: `fig.add_annotation(x=2020, y=950, text="<b>–42%</b>", showarrow=True, arrowhead=2, arrowcolor="#E53935")`. Equivalent to R's `layout(annotations=list(...))`.

**Dropdown filters (updatemenus)**: identical API to R — create buttons with `method="restyle"` and `args=[{"visible": [True, False, ...]}]`.

**Shapes and reference lines**: `fig.add_hline(y=peak, line_dash="dot")` or `fig.add_vrect(x0=2007.5, x1=2009.5, fillcolor="red", opacity=0.05)`.

### 4. Animations with px
plotly.express provides one-parameter animation: add `animation_frame="year"` to any px chart, and it generates:

- A slider at the bottom showing all frame values
- Play/pause buttons
- Smooth transitions between frames (configurable via `fig.update_layout(transition=dict(duration=500))`)

This is the interactive equivalent of gganimate (W06-M06): the user controls playback, can pause at any frame, and scrub back and forth. In R, the equivalent is `plot_ly(frame=~year) |> animation_opts()`.

### 5. Subplots and Facets
Two approaches for multi-panel:

**make_subplots**: `from plotly.subplots import make_subplots; fig = make_subplots(rows=2, cols=1, shared_xaxes=True)`. Then `fig.add_trace(go.Scatter(...), row=1, col=1)`. Provides full control but requires manual trace assignment.

**px facets**: `px.line(df, x="year", y="n", facet_col="country")`. Creates small multiples automatically from a single function call — much faster for EDA. Each facet gets its own axes but shares the colour scale.

### 6. R ↔ Python Translation
The plotly API is designed to be nearly identical across languages:

| Concept | R | Python |
|---------|---|--------|
| Quick chart | `ggplotly(ggplot()+geom_*())` | `px.line/scatter/bar()` |
| Native trace | `plot_ly() |> add_trace()` | `go.Figure(); fig.add_trace()` |
| Layout config | `layout(hovermode=...)` | `fig.update_layout(hovermode=...)` |
| Hover format | `hovertemplate="%{x}"` | `hovertemplate="%{x}"` (identical!) |
| Dropdown | `updatemenus=list(list(...))` | `updatemenus=[dict(...)]` |
| Subplots | `subplot(shareX=TRUE)` | `make_subplots(shared_xaxes=True)` |
| Animation | `frame=~year` | `animation_frame="year"` |
| Save | `saveWidget(p, "f.html")` | `fig.write_html("f.html")` |
| Linked brushing | `crosstalk + highlight()` | Dash callbacks (M05) |

The hovertemplate, layout, and updatemenus syntax is literally the same string format. Students who learn plotly in one language can translate to the other in minutes.

### References
- plotly.py docs: https://plotly.com/python/
- plotly.express: https://plotly.com/python/plotly-express/
- make_subplots: https://plotly.com/python/subplots/
- Sievert, C. (2020). *Interactive Web-Based Data Visualization with R, plotly, and shiny*. CRC Press.
