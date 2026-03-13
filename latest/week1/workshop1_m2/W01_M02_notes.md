# Workshop 1 · Module 2 — Course Notes
## Tufte's Principles of Graphical Excellence

---

### 1. The Data-Ink Ratio

Tufte (1983, pp. 93–96) defines the data-ink ratio as the proportion of total
ink on a graphic that represents data. The operational directive is twofold:
above all else, show the data; and erase non-data ink, within reason.

Non-data ink encompasses background fills, heavy gridlines, decorative borders,
redundant axis ticks, and any visual element that does not encode a data value.
The progressive erasure test proceeds iteratively: remove one element, assess
whether any information is lost, and retain only those elements that survive
the test.

The **range-frame** extends this idea to the axes themselves. In a conventional
plot the axis spans from an arbitrary minimum to an arbitrary maximum. Tufte
proposes that the axis line should extend only from the data minimum to the
data maximum, so the axis itself conveys the data range rather than occupying
empty space.


### 2. Chartjunk

Tufte classifies non-data decoration into three categories.

**Moiré vibration** arises from dense hatching or crosshatch patterns that
cause optical interference. The human visual system interprets the resulting
shimmer as signal, distracting from the actual data. The remedy is to replace
hatching with distinct hues at moderate saturation.

**Heavy grids** compete with data marks for visual dominance. Gridlines should
be faint (low-alpha) or removed entirely when direct labels or annotations
provide sufficient reference.

**Ducks** (after Venturi et al., 1972) occur when decorative imagery dominates
the chart to the point that the data becomes secondary. Common offenders
include 3-D bar effects, pictorial backgrounds, and clip-art embellishments.


### 3. Graphical Integrity and the Lie Factor

The lie factor quantifies the degree of visual distortion:

    Lie Factor = (Size of effect in graphic) / (Size of effect in data)

A lie factor of 1.0 indicates faithful representation. Values outside the
tolerance band of [0.95, 1.05] indicate deception. The three most common
sources of inflated lie factors are:

- **Truncated axes**: Starting the y-axis above zero exaggerates small
  differences. A 2.8% increase can appear tenfold when the baseline is set
  near the minimum value.
- **Area encoding of linear quantities**: When bar height encodes a value
  but the bar is rendered as a 3-D cylinder, the viewer perceives volume
  (which grows cubically), not height (which grows linearly).
- **Perspective projection**: Tilting a pie chart causes foreshortening
  of rear slices, making them appear proportionally smaller.


### 4. Small Multiples

Small multiples repeat a single design template across panels that differ
only in the data. Tufte writes: "At the heart of quantitative reasoning is a
single question: Compared to what?" By holding the visual structure constant,
the viewer's pattern-recognition apparatus focuses entirely on cross-panel
variation.

In R, `facet_wrap()` and `facet_grid()` create small multiples natively. The
critical parameter `scales = "fixed"` ensures a common axis, enabling fair
comparison. In Python, `plt.subplots(sharey=True)` achieves the same effect.


### 5. Sparklines

Tufte (2006) introduced sparklines as "intense, simple, word-sized graphics."
A sparkline is a miniature time-series chart — typically without axes, labels,
or gridlines — embedded inline with text or within a table cell. Three key
markers (minimum, maximum, and current value) convey essential context.

The data-ink ratio of a well-crafted sparkline approaches 1.0 because every
visible pixel encodes either the trend line or a critical data point.


### 6. Integration of Words and Graphics

Tufte argues that the segregation of text from graphics is an anachronistic
legacy of nineteenth-century engraving technology. Modern computational tools
allow seamless integration of annotations, callouts, and contextual labels
directly onto the data plane. Direct labelling replaces legends; embedded
annotations replace footnotes; the chart becomes a self-contained analytical
document.


### References

- Few, S. (2004). Tapping the power of visual perception. *Intelligent
  Enterprise*.
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*.
  Graphics Press.
- Tufte, E. R. (2006). *Beautiful Evidence*. Graphics Press.
- Venturi, R., Scott Brown, D., & Izenour, S. (1972). *Learning from Las
  Vegas*. MIT Press.
- Wainer, H. (1984). How to display data badly. *The American Statistician*,
  38(2), 137–147.
