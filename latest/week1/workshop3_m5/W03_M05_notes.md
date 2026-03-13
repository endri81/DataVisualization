# Workshop 3 · Module 5 — Course Notes
## Proportions: Pie, Donut, Treemap & Waffle

### 1. The Pie Chart Debate
Pie charts encode proportions via angle, the weakest perceptual channel in Cleveland & McGill's (1984) hierarchy. Humans are approximately 2× less accurate judging angles than lengths. Pies are acceptable only when: (a) ≤3 slices, (b) one slice clearly dominates, (c) the goal is showing "more than half" rather than precise comparison. For 4+ categories, a sorted horizontal bar with % labels always outperforms a pie.

### 2. Donut Charts
A donut is a pie with a centre hole. The centre provides space for a headline number (KPI), making donuts acceptable for single-metric dashboards (e.g., "73% Free"). For multi-category comparisons, donuts suffer the same angle-discrimination problem as pies.

### 3. Better Alternatives
**100% stacked bar**: encodes proportions via length (Cleveland rank 1), directly comparable. Use for showing composition across one or two groups. **Sorted horizontal bar with %**: the safest universal proportion chart — length encodes magnitude, direct labels show percentages, sorting reveals ranking. Default to this unless you have a specific reason for an alternative.

### 4. Treemaps
Treemaps encode part-to-whole via area within a rectangle. Area is more accurate than angle (pie) but less accurate than length (bar). Treemaps excel when the data is hierarchical (category → sub-category → item) and has 10–50 leaf nodes. In R: `treemapify::geom_treemap()`. In Python: `squarify.plot()`. For flat (non-hierarchical) data, a bar chart is almost always better.

### 5. Waffle Charts
Waffle charts use a 10×10 grid where each square represents 1%. They are more intuitive than pies because counting squares is easier than judging angles. Limit to ≤6 categories. In R: `waffle` package. In Python: `pywaffle` or manual `plt.Rectangle()` loop.

### 6. Decision Framework
2–3 parts → pie/donut acceptable; 4–7 parts → stacked bar or sorted bar with %; 8+ parts → treemap; single KPI highlight → donut with centre text; hierarchical → treemap or sunburst; general audience → waffle.

### References
- Cleveland, W. S. & McGill, R. (1984). Graphical Perception. *JASA*, 79(387).
- Spence, I. & Lewandowsky, S. (1991). Displaying proportions. *Applied Cognitive Psychology*.
- Schwabish, J. (2021). *Better Data Visualizations*, Chapter 6.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 10.
