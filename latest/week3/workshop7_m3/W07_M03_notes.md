# Workshop 7 · Module 3 — Course Notes
## Advanced Annotation in Code

### 1. Beyond Basic Annotation
W06-M02 introduced `geom_vline() + annotate()` for event markers and `geom_text()` for direct labels. This module covers the **full annotation toolkit** needed to produce publication-quality explanatory charts: non-overlapping labels, rich text formatting, callout boxes with curved arrows, highlight rectangles, and the layered annotation hierarchy.

### 2. Non-Overlapping Labels: ggrepel and adjustText
The most common annotation problem is **label overlap**: when multiple text labels are placed at their data positions, they collide and become unreadable. Two packages solve this automatically:

**ggrepel (R)**: provides `geom_text_repel()` and `geom_label_repel()` which use a physics-based repulsion algorithm to position labels near their data points without overlapping. Key parameters: `max.overlaps` (how many overlap attempts before giving up), `box.padding` (minimum space around labels), `force` (repulsion strength), `segment.color` / `segment.size` (the connector line from label to point), `seed` (for reproducible placement). For time series: use `direction = "y"` to constrain labels to move only vertically (keeping them at the correct x-position).

**adjustText (Python)**: `from adjustText import adjust_text`. Create text objects first with `ax.text()`, then call `adjust_text(texts, ax=ax, arrowprops=...)` to reposition them. Key parameters: `force_text` (repulsion between labels), `force_points` (repulsion from data points), `arrowprops` (connector line style).

### 3. Rich Text: ggtext
The `ggtext` package for R enables **markdown formatting in ggplot text elements** — titles, subtitles, axis labels, annotations. This is powerful for explanatory charts because you can colour specific words in the title to match their data series, eliminating the need for a legend.

Example: `labs(title = "**<span style='color:#1565C0'>Movies</span>** peaked in 2019")` with `theme(plot.title = element_markdown())`. The word "Movies" renders in blue bold, matching the blue line on the chart. The audience can read the title and immediately know which line it refers to.

Python equivalent: matplotlib supports basic rich text through `fontweight`, `fontstyle`, and `color` parameters in `ax.text()`, but does not support inline markdown. For multi-colour text, use multiple `ax.text()` calls at adjacent positions, or use `bbox` parameter for boxed text.

### 4. Callout Boxes and Curved Arrows
The most professional annotation style is a **callout box** — a text label with a background box and an arrow pointing to the specific data element it references.

**R**: `annotate("label", x, y, label = "text", fill = "white", label.size = 0.5)` creates a boxed label. Pair with `annotate("segment", ..., arrow = arrow())` for the arrow.

**Python**: `ax.annotate("text", xy=(target), xytext=(label_pos), bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="red"), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"))`. The `connectionstyle="arc3,rad=0.2"` creates a curved arrow that avoids crossing other elements. Positive rad curves counterclockwise; negative curves clockwise.

Arrow styles in matplotlib: `"->"` (standard), `"-|>"` (filled triangle), `"-["` (bar end), `"fancy"` (fancy curved), `"wedge"` (wedge-shaped). The most common for data annotation is `"->"`.

### 5. Highlight Rectangles and Shaded Regions
Shaded rectangles draw attention to a specific region of the chart:

**Vertical span** (time period): R `annotate("rect", xmin, xmax, ymin = -Inf, ymax = Inf, fill = "red", alpha = 0.05)`. Python: `ax.axvspan(xmin, xmax, alpha=0.05, color="red")`. Use for highlighting crisis periods, policy windows, or focal time ranges.

**Horizontal span** (threshold): R `annotate("rect", ymin, ymax, xmin = -Inf, xmax = Inf, ...)`. Python: `ax.axhspan(ymin, ymax, ...)`. Use for highlighting target zones, normal ranges, or benchmark levels.

Always use very low alpha (0.03–0.08) so the shading provides context without obscuring the data.

### 6. The Annotation Hierarchy
Build annotations in layers, from structural to specific:

**Layer 0: Bare chart** — just the geometry (line, scatter, bar). Good for exploratory work.

**Layer 1: Reference elements** — horizontal lines (target, average, peak), vertical lines (events), shaded regions (crisis windows). These provide the interpretive context.

**Layer 2: Direct labels** — series names at endpoints, axis labels, value labels on bars. These replace the legend and make the chart self-contained.

**Layer 3: Callout boxes** — 1–2 annotated findings with arrows pointing to the specific evidence. These deliver the "so what" message. **Maximum 2 callouts per chart** — more than that creates clutter. If you have 4 findings, use 4 charts.

**Layer 4: Title + subtitle** — declarative title (the finding), subtitle (the context or implication), caption (source attribution).

### 7. Common Mistakes
(1) **Too many annotations**: the chart becomes a text document. Max 2 callouts. (2) **Annotations that obscure data**: always place labels and boxes in white space, not on top of data points. Use `fill = "white"` with slight alpha to ensure text is readable over data. (3) **Inconsistent style**: keep all annotations in the same font, size, and colour scheme. (4) **Missing connector lines**: a callout without an arrow leaves the reader guessing which element it refers to. Always connect the label to the data.

### References
- ggrepel: https://ggrepel.slowkow.com/ (Kamil Slowikowski)
- ggtext: https://wilkelab.org/ggtext/ (Claus Wilke)
- adjustText: https://github.com/Phlya/adjustText (Ilya Flyamer)
- matplotlib annotation tutorial: https://matplotlib.org/stable/tutorials/text/annotations.html
- Knaflic, C. N. (2015). *Storytelling with Data*, Chapter 4 (Focus attention).
