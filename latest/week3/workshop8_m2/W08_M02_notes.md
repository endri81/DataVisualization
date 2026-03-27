# Workshop 8 · Module 2 — Course Notes
## plotly in R: Interactive Charts

### 1. The R plotly Ecosystem
The `plotly` R package provides four core functions for building interactive visualizations:

**`ggplotly(p, tooltip)`**: converts any ggplot2 object into an interactive plotly chart. Zero learning curve for students who already know ggplot2. The `tooltip` parameter controls which aesthetics appear in the hover tooltip — use `tooltip = "text"` with a custom `text` aesthetic for clean, formatted tooltips.

**`plot_ly(data, x, y, type, mode)`**: the native plotly API, providing full control over every aspect of the chart. Requires learning a new syntax (trace-based rather than grammar-of-graphics), but offers features that ggplotly cannot access: custom `hovertemplate` strings, `updatemenus` for dropdown filters, and fine-grained animation control.

**`highlight(on, off, color)`**: enables linked brushing — selecting points in one chart highlights corresponding points in another. Requires `crosstalk::SharedData` as the data source.

**`subplot(p1, p2, nrows, shareX)`**: combines multiple plotly objects into a single figure with optional shared axes. When `shareX = TRUE`, zooming in one panel zooms all panels — essential for dashboards where time alignment matters.

### 2. The ggplotly Pipeline
The recommended workflow for most use cases:

**Step 1 — Build in ggplot2**: create the chart using familiar ggplot2 syntax. Add a `text` aesthetic containing the formatted tooltip text using `paste0()` with HTML-like `<br>` for line breaks and `<b>` for bold.

**Step 2 — Convert**: call `ggplotly(p, tooltip = "text")` to convert. The interactive version inherits all ggplot2 geoms, colours, and theme settings.

**Step 3 — Customise layout**: use the pipe `|>` to add `layout()` calls. Key settings: `hovermode = "x unified"` (single tooltip per x-value, ideal for time series), `hoverlabel = list(bgcolor = "white")` (clean tooltip background), `legend = list(orientation = "h")` (horizontal legend to save vertical space).

**Step 4 — Save**: `htmlwidgets::saveWidget(p, "file.html", selfcontained = TRUE)` creates a standalone HTML file that opens in any browser. The `selfcontained = TRUE` flag embeds all JavaScript dependencies (resulting in a ~3MB file) — no server needed.

### 3. Native plot_ly: When You Need Full Control
Switch from ggplotly to plot_ly when you need:

**Custom hovertemplate**: `hovertemplate = "Year: %{x}<br>Titles: %{y:,}<extra></extra>"`. The `%{x}` and `%{y}` placeholders reference the trace's x and y data. The `:,` format adds comma separators. The `<extra></extra>` tag suppresses the trace name in the tooltip secondary box.

**Dropdown filters (updatemenus)**: `layout(updatemenus = list(list(type = "dropdown", buttons = list(...))))`. Each button specifies a `method` ("restyle" to change trace properties, "update" to change both traces and layout) and `args` (e.g., `list("visible", list(TRUE, FALSE))` to show/hide traces).

**Animations**: `animation_opts(frame = 500, transition = 300)` controls playback speed. Combined with a `frame` aesthetic in the data, this creates animated transitions between states (similar to gganimate but interactive with play/pause controls).

### 4. Hover Modes
plotly offers three hover modes that determine how tooltips appear:

**`"closest"`**: tooltip appears for the single nearest point to the cursor. Best for scatter plots where points are sparse.

**`"x unified"`**: a single vertical tooltip shows all traces at the current x-value. Best for time series where you want to compare series at the same date.

**`"x"` / `"y"`**: tooltip appears for all traces at the nearest x/y value, with separate tooltip boxes per trace. A middle ground.

### 5. Linked Brushing with crosstalk
The `crosstalk` package enables linked selection across multiple plotly charts without a Shiny server:

```r
library(crosstalk)
sd <- SharedData$new(df, key = ~id_column)
p1 <- plot_ly(sd, x = ~x, y = ~y, type = "scatter", mode = "markers")
p2 <- plot_ly(sd, x = ~category, type = "histogram")
subplot(p1, p2) |>
  highlight(on = "plotly_selected", off = "plotly_deselect", color = "#E53935")
```

The `SharedData$new()` wrapper creates a reactive data object. When the user selects points in p1 (via lasso or box select), the corresponding rows are highlighted in p2. This implements Shneiderman's "relate" step (M01) — the user sees relationships across views.

**Limitation**: crosstalk works for client-side filtering (no server needed) but is limited to ~10,000 rows and simple selection. For server-side filtering with complex logic, use Shiny (M04).

### 6. R ↔ Python plotly Equivalence
The plotly API is nearly identical across R and Python:

| R | Python | Note |
|---|--------|------|
| `ggplotly(p)` | `px.line(df, ...)` | Quick interactive |
| `plot_ly(df, x=~x)` | `go.Scatter(x=df.x)` | Native API |
| `add_trace(...)` | `fig.add_trace(go.Scatter(...))` | Add series |
| `layout(hovermode=...)` | `fig.update_layout(hovermode=...)` | Config |
| `hovertemplate='%{x}'` | `hovertemplate='%{x}'` | IDENTICAL |
| `subplot(shareX=TRUE)` | `make_subplots(shared_xaxes=True)` | Multi-panel |
| `saveWidget(p, 'f.html')` | `fig.write_html('f.html')` | Export |
| `highlight() + crosstalk` | No equivalent (use Dash) | Brushing |

### References
- Sievert, C. (2020). *Interactive Web-Based Data Visualization with R, plotly, and shiny*. CRC Press. https://plotly-r.com
- plotly R reference: https://plotly.com/r/
- crosstalk: https://rstudio.github.io/crosstalk/
- htmlwidgets: https://www.htmlwidgets.org/
