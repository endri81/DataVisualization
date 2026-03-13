# Workshop 3 · Module 6 — Course Notes
## Rankings: Slope, Bump & Waterfall

### 1. Slopegraphs
A slopegraph (Tufte, 1983) connects values for each item across exactly two time points. The slope of each line encodes the rate of change; the absolute position encodes magnitude; crossing lines reveal rank reversals. Slopegraphs are optimal for 5–15 items across two time points. For more items, apply the grey-accent strategy: all lines in light grey except 1–2 highlighted items in colour with direct labels at both ends.

### 2. Bump Charts
Bump charts track ordinal rank positions over 3–8 time periods. The y-axis is inverted so rank #1 appears at the top. Each line represents one entity's rank trajectory; crossing lines show rank changes. In R, the `ggbump` package produces smooth sigmoid curves between rank positions. In Python, manual `ax.plot()` loops with `ax.invert_yaxis()`. Best for 4–10 entities; apply grey-accent for more. Direct-label at the rightmost point to eliminate the legend.

### 3. Waterfall Charts
Waterfall charts decompose a total into sequential additions and subtractions. The first and last bars (totals) are typically blue; intermediate bars are green (positive contribution) or red (negative contribution). Dashed connector lines show the running total. Standard in financial reporting for P&L statements, budget variance analysis, and revenue decomposition. In R: manual `geom_rect()` or the `waterfalls` package. In Python: manual `ax.bar(bottom=)` with connector lines via `ax.plot()`.

### 4. Grey-Accent Strategy
All three chart types become unreadable with too many items (spaghetti). The universal solution: render all items in light grey (#CCCCCC, alpha=0.3), then highlight 1–2 key items in saturated colour with direct labels. This technique applies equally to slopegraphs, bump charts, line charts (W06), and faceted displays.

### References
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*, pp. 158–161.
- Schwabish, J. (2021). *Better Data Visualizations*, Chapter 5.
- Few, S. (2006). *Information Dashboard Design*, Chapter 6.
