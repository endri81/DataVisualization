# Workshop 6 · Module 1 — Course Notes
## Time as a Visual Dimension

### 1. Why Time Is Special
Time differs from other variables in four fundamental ways. It is **ordered**: there is a natural before/after relationship that other continuous variables (e.g., height, income) do not inherently possess. It is **continuous** with **natural units** (seconds, hours, days, weeks, months, years) that carry meaning — a "day" is universally understood. It enables **causal reasoning**: events plotted chronologically allow us to observe cause-before-effect sequences. And it has **hierarchical granularity**: we can zoom from seconds to centuries on the same axis, choosing the level of detail appropriate to the question.

These properties demand specialised chart types (line, area, step) and specialised axis formatting (date breaks, labels, proper spacing). The most common error in temporal visualization is treating dates as categorical labels — evenly spacing "Jan 2020, Jun 2020, Jan 2022" even though the gap between the last two points is 18 months, not 6.

### 2. Temporal Granularity
Granularity is the time resolution at which data is recorded or displayed. The same underlying process looks very different at daily, weekly, monthly, and yearly resolution: daily is noisy but captures individual events; yearly is smooth but loses all sub-annual patterns.

**Rule**: always start at the finest available granularity, then aggregate up as needed. You can always smooth daily → monthly, but you cannot recover daily detail from monthly aggregates. In R: `floor_date(date, "month") |> group_by() |> summarise()`. In Python: `df.resample("ME").mean()`.

Choosing granularity depends on the question: daily for event detection and short-span analysis (<3 months), weekly for medium spans (3–12 months, smooths day-of-week effects), monthly for annual seasonal analysis, quarterly for financial reporting, yearly for multi-decade macro trends.

### 3. Time Series Decomposition
A time series can be decomposed into three components: **trend** (the long-term direction — increasing, decreasing, or flat), **seasonal** (a repeating cyclical pattern with a fixed period — annual, weekly, daily), and **residual** (the random noise remaining after trend and seasonality are removed).

Two models: **additive** (Y = T + S + R) when the seasonal amplitude is constant regardless of the trend level — typical for temperature data. **Multiplicative** (Y = T × S × R) when the seasonal amplitude grows proportionally with the trend — typical for retail sales and economic data. Quick visual test: if the envelope of peaks and troughs widens as the trend rises, use multiplicative.

**STL** (Seasonal-Trend decomposition using Loess) is the most robust method: handles outliers, allows the seasonal component to change slowly over time, and works with any period. R: `stl(ts_data, s.window="periodic")`. Python: `statsmodels.tsa.seasonal.STL(series, period=365)`. Classical `decompose()` is simpler but less robust.

### 4. Temporal Chart Taxonomy
Five core types: **Line chart** — the default for continuous time series; shows trajectory/trend. **Area chart** — like a line but filled below; use stacked areas for parts-of-a-whole over time. **Step chart** — horizontal segments with vertical jumps; ideal for discrete changes (interest rates, policy thresholds). **Bar chart (temporal)** — one bar per period (month, year); best for aggregated totals/counts. **Heatmap calendar** — a grid of day-cells coloured by value; reveals day-of-week and seasonal patterns simultaneously (used by GitHub contribution graphs, fitness trackers).

### 5. Time-Axis Pitfalls
(1) **Categorical spacing**: converting dates to strings and plotting as evenly-spaced categories. This misrepresents gaps — a 2-month gap looks the same as a 2-year gap. Always use a true date/time axis (`scale_x_date()` in R, `DateFormatter` in Python). (2) **Truncated y-axis**: starting the y-axis at a non-zero value exaggerates small changes. For context, include zero or clearly mark the y-axis start. (3) **Missing dates**: if data is missing for certain dates, the chart should show a gap (broken line), not a straight connection through the missing period. (4) **Time zone ambiguity**: always document the time zone; a dataset recorded in UTC and displayed in local time can shift events by hours.

### References
- Cleveland, R. B. et al. (1990). STL: A Seasonal-Trend Decomposition. *Journal of Official Statistics*, 6(1).
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3rd ed. https://otexts.com/fpp3/
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Ch. 13.
