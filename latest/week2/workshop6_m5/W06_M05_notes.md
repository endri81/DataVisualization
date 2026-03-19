# Workshop 6 · Module 5 — Course Notes
## Seasonal & Calendar Visualizations

### 1. Calendar Heatmaps
A calendar heatmap displays day-level data as a grid where rows represent the day of the week (Monday–Sunday) and columns represent the week of the year (1–52). Each cell's colour encodes the value for that specific day. This layout simultaneously reveals two temporal patterns: **weekly patterns** (weekday vs weekend differences appear as horizontal bands — e.g., GitHub contribution graphs show more commits on weekdays) and **seasonal patterns** (summer vs winter differences appear as colour gradients across columns).

Design decisions: use a sequential palette (YlGn for activity, YlOrRd for temperature) with white-to-dark mapping. Add thin white borders between cells for readability. Consider labelling months along the top axis (approximate positions at weeks 1, 5, 9, ...) for temporal context.

In R: `ggplot(aes(x = week, y = fct_rev(dow), fill = value)) + geom_tile(color = "white")`. The `calendR` package produces pre-formatted calendar displays. The `ggTimeSeries` package offers `ggplot_calendar_heatmap()`.

In Python: compute a pivot table `df.pivot_table(index="dow", columns="week", values="value")` then `ax.imshow(pivot.values, cmap="YlGn")`. The `calplot` package provides a one-liner: `calplot.calplot(series)`. For GitHub-style: `july` package.

### 2. Seasonal Subseries (Year-over-Year Overlay)
The most direct way to visualise seasonal patterns: plot the same variable on a Jan–Dec (or Mon–Sun) axis, with one line per year. The **grey+accent** strategy applies: all historical years in light grey (alpha 0.2–0.4), the current or focal year in saturated colour. This immediately reveals: (a) is this year above or below the historical pattern? (b) which months deviate most? (c) is the seasonal shape itself changing over time (amplitude increasing/decreasing)?

In R: `ggplot(aes(x = month, y = value, color = factor(year), alpha = factor(year))) + geom_line()` with `scale_alpha_manual()` controlling the grey+accent effect.

In Python: loop over years, plotting each with `ax.plot()` and controlling `color` and `alpha` per year.

### 3. Monthly Boxplot
An alternative to the subseries overlay: one boxplot per month, summarising the distribution of that month's values across all years. The box shows the IQR (typical range), the median shows the central tendency, and outlier dots show unusual years. Overlay a mean line (connecting monthly means) to show the average seasonal shape.

This is more analytically precise than the subseries overlay (which can become cluttered with >5 years) and directly answers "what is the typical range for January?" — useful for anomaly detection (is this January unusually high?).

### 4. Polar Time Plots
Polar (clock-face) charts arrange cyclical data around a circle: 12 months (annual cycle), 24 hours (daily cycle), 7 days (weekly cycle). The circular layout emphasises the cyclical nature of the data — December wraps visually to January, midnight wraps to the next day.

However, polar charts introduce perceptual distortion: bars near the centre appear smaller than bars of the same data value near the edge (because arc length increases with radius), and angles are harder to compare than lengths. **Recommendation**: use polar charts sparingly and always compare with the linear version. The linear bar chart is almost always easier to read for precise comparison; the polar version is better for communicating "this is cyclical data" to a general audience.

### 5. Month × Year Heatmap
A coarser alternative to the calendar heatmap: rows = years, columns = months, colour = value. This is essentially a temporal version of the correlation heatmap from W05-M04. Annotate cells with values (if the matrix is small enough, ≤6 years × 12 months = 72 cells). This view compresses daily data to monthly totals and shows both the seasonal pattern (column-to-column variation) and the trend (row-to-row growth).

### 6. Choosing the Right Seasonal Display
- **Calendar heatmap**: day-level data, simultaneous weekly + annual patterns, space-efficient
- **Seasonal subseries**: year-over-year comparison, grey+accent, pattern change detection
- **Monthly boxplot**: distribution per month across years, anomaly detection
- **Polar plot**: cyclical emphasis for general audience, less precise than linear
- **Month × Year heatmap**: compact summary of monthly values across years, annotated

### References
- Tufte, E. (2001). *The Visual Display of Quantitative Information*. (Calendar displays.)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, Ch. 3 (Seasonal plots).
- calplot documentation: https://github.com/tomkwok/calplot
- Wickham, H. (2016). *ggplot2*, 2nd ed. (coord_polar, facet_wrap for seasonal.)
