# Workshop 6 · Module 3 — Course Notes
## Line Charts in Code (R + Python)

### 1. Six Line Geometries
This module covers the six core line-based chart types available in both ggplot2 and matplotlib, each serving a distinct purpose:

**geom_line / ax.plot()**: The default for continuous time series. Connects data points with straight line segments in chronological order. Use when the underlying process is continuous (temperature, stock price, cumulative count). The x-axis must be a proper date/time type — never a character string. In R: `ggplot(aes(x = date, y = value)) + geom_line()`. In Python: `ax.plot(dates, values)`.

**geom_step / ax.step()**: Horizontal segments connected by vertical jumps. Use when the value changes **discretely** at specific points and remains constant between changes. Canonical examples: interest rates (the Fed announces a new rate, it stays fixed until the next announcement), tariff schedules, pricing tiers, regulatory thresholds. The `where` parameter in Python controls jump placement: `"pre"` (jump before), `"post"` (jump after), `"mid"` (jump at midpoint). In R, `geom_step()` defaults to `direction = "hv"` (horizontal then vertical).

**geom_area / fill_between()**: A line chart with the area between the line and the baseline (usually zero) filled with colour. The fill emphasises **magnitude** — the visual weight of the coloured region conveys cumulative volume or total quantity. Use for single-series displays where the visual mass of the area is informative (total revenue, rainfall accumulation, inventory levels). Use low alpha (0.2–0.4) so the line remains visible on top.

**Stacked area / stackplot()**: Multiple filled areas stacked so that each band represents one component and the total height represents the sum. Use for **parts-of-a-whole over time**: revenue by product line, energy mix by source, population by age group. **Design rule**: place the most stable series at the bottom (it forms the baseline and is easiest to read); place the most variable series at the top. Maximum 5–6 stacks; beyond that, the upper bands become unreadable because they sit on a wavy baseline.

**100% stacked area**: Each time point sums to 100%. Shows proportional composition over time. The top boundary is always flat at 100%. Useful when the absolute total is less important than the relative share — market share over time, demographic composition, budget allocation proportions. The disadvantage: the reader cannot tell if the total is growing or shrinking.

**Ribbon / fill_between(lower, upper)**: A shaded band around a central line representing a confidence interval, prediction interval, or uncertainty range. The most important underused chart element in time series visualization. A line without a ribbon implies false precision. For forecasts: use prediction intervals (wider than CI). For observed data: use bootstrapped CIs. Always use low alpha (0.1–0.2) so the central line remains clear. In R: `geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15)`. In Python: `ax.fill_between(x, lower, upper, alpha=0.15)`.

### 2. Date Axis Formatting
The x-axis of any time series chart must use a proper date/time scale. The two languages handle this differently:

**R (scales package)**: `scale_x_date(date_breaks = "3 months", date_labels = "%b %Y")`. The `date_breaks` argument accepts strings like "1 month", "3 months", "1 year", "2 weeks". The `date_labels` argument uses `strftime` format codes: %Y (4-digit year), %y (2-digit year), %m (month number 01–12), %b (abbreviated month name), %B (full month name), %d (day 01–31). For minor gridlines: `date_minor_breaks = "1 month"`. For label rotation: `theme(axis.text.x = element_text(angle = 30, hjust = 1))`. Multi-line labels: `date_labels = "%b\n%Y"` puts month and year on separate lines.

**Python (matplotlib.dates)**: `ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))` sets the label format. `ax.xaxis.set_major_locator(MonthLocator(interval=3))` controls tick placement. Available locators: `YearLocator()`, `MonthLocator(interval=N)`, `WeekdayLocator()`, `DayLocator()`. For rotation: `plt.xticks(rotation=30)` or `plt.setp(ax.get_xticklabels(), rotation=30, fontsize=7)`. Same strftime codes as R.

### 3. Stacked Area Design Decisions
The stacked area chart has three critical design decisions:

**Order**: The bottom series is the only one with a flat baseline, making it the only one whose individual trend is accurately readable. Upper series sit on wavy baselines formed by the cumulative sum of lower series, distorting their perceived trends. **Rule**: place the most stable (least volatile) series at the bottom, the most important series second from bottom, and the most variable at the top.

**Number of stacks**: Maximum 5–6. Beyond that, the upper bands become too thin and wavy to read. If you have more categories, aggregate the smallest into "Other" or switch to small multiples.

**Absolute vs 100%**: Use absolute stacked when the total matters (total revenue growing). Use 100% stacked when proportions matter and the total is irrelevant or known. If both matter, show both as a two-panel figure.

### 4. Ribbon: Communicating Uncertainty
The ribbon (confidence band) is the most important visual element that most time series charts lack. A line without a band implies that the central estimate is known with certainty — which it never is. The ribbon communicates the precision of the estimate.

Types of bands: **Confidence interval** (how precisely we know the mean — narrows with more data). **Prediction interval** (where a new observation might fall — always wider than CI). **Bootstrap CI** (empirical, no distributional assumption). **Model uncertainty** (ensemble spread, e.g., climate model projections).

Visual encoding: use low alpha (0.1–0.2) and the same hue as the central line. Never use error bars on a time series — they clutter the chart and break the temporal flow. A smooth ribbon is always preferable.

### References
- Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis*, 2nd ed. Springer. (Chapter 3: Geoms.)
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3rd ed. (Ribbon for prediction intervals.)
- matplotlib date documentation: https://matplotlib.org/stable/api/dates_api.html
- Few, S. (2012). *Show Me the Numbers*, 2nd ed. Analytics Press. (Stacked area design.)
