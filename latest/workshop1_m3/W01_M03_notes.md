# Workshop 1 · Module 3 — Course Notes
## Visual Perception & Pre-Attentive Attributes

---

### 1. Pre-Attentive Processing

The human primary visual cortex (V1) detects certain stimulus properties
within 200–250 milliseconds, before conscious attention is engaged and
independently of the number of distractor items in the visual field. Healey
and Enns (2012) identify four canonical pre-attentive channels: **colour
(hue)**, **form (shape)**, **size (length/area)**, and **orientation
(angle/tilt)**.

A target that differs from distractors along a single pre-attentive channel
"pops out" — detection time is constant regardless of the number of
distractors. When the target is defined by a *conjunction* of two features
(e.g., red AND square among red circles and blue squares), the visual system
must search serially at approximately 50 ms per item (Treisman & Gelade,
1980). The design implication is direct: encode the most critical data
distinction using a single pre-attentive channel, never a conjunction.


### 2. Gestalt Laws of Perceptual Grouping

The Gestalt psychologists (Wertheimer, 1923; Koffka, 1935) identified
principles by which the visual system organises individual stimuli into
coherent groups:

**Proximity** — elements that are spatially near each other are perceived as
belonging to the same group. In chart design, inter-group spacing must exceed
intra-group spacing.

**Similarity** — elements that share a visual property (colour, shape, size)
are grouped together, even when uniformly spaced. This is why colour legends
function: matching hues are read as "the same category."

**Continuity** — the visual system prefers smooth, continuous paths over
abrupt angular transitions. Two intersecting curves are seen as two paths,
not four segments.

**Closure** — the brain fills in missing information to perceive complete
shapes. Partially obscured elements are "completed" perceptually.

**Enclosure** — a bounded region (shaded rectangle, outline) groups all
elements within it, overriding proximity cues. In ggplot2, `annotate("rect")`
creates enclosure; in matplotlib, `axvspan()`.

**Connection** — lines connecting elements create a grouping that can override
proximity and similarity. Time-series line charts exploit this principle:
sequential points are perceived as a single evolving entity.


### 3. Visual Encoding Channels

Cleveland and McGill (1984) ranked the accuracy of visual encoding channels
through controlled experiments:

1. Position on a common scale (bar chart, dot plot)
2. Position on non-aligned scales (small multiples)
3. Length (bar chart without common baseline)
4. Angle / slope (pie chart, line chart slope)
5. Area (bubble chart, treemap)
6. Volume / curvature (3-D chart)
7. Colour saturation / hue (heatmap, choropleth)

The practical guideline is to map the most analytically important variable to
the highest-ranked channel (position), and reserve lower-ranked channels
(area, colour) for secondary variables.


### 4. Weber's Law and Just-Noticeable Difference

Weber's law states that the smallest detectable change in a stimulus (the
just-noticeable difference, JND) is a constant proportion of the baseline
stimulus: ΔS / S = k. For position judgments, k ≈ 0.02 (viewers detect a 2%
change). For area, k ≈ 0.10 (a 10% change is needed). For colour saturation,
k ≈ 0.15–0.20.

The implication: if two data values differ by only 5%, encoding them as areas
(bubbles) will render the difference invisible, but encoding them as positions
(bars from a common baseline) will make the difference perceptible.


### 5. Change Blindness

When comparing two views of a dataset (before/after, version A/B), viewers
routinely miss subtle changes unless those changes are explicitly highlighted
through annotation, colour contrast, or connecting lines. This phenomenon —
change blindness — explains why side-by-side comparison charts should always
include direct visual cues pointing to the specific elements that differ.


### References

- Cleveland, W. S. & McGill, R. (1984). Graphical perception: Theory,
  experimentation, and application. *JASA*, 79(387), 531–554.
- Few, S. (2012). *Show Me the Numbers*, 2nd ed. Analytics Press.
- Healey, C. G. & Enns, J. T. (2012). Attention and visual memory in
  visualization and computer graphics. *IEEE TVCG*, 18(7), 1170–1188.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Treisman, A. M. & Gelade, G. (1980). A feature-integration theory of
  attention. *Cognitive Psychology*, 12(1), 97–136.
- Ware, C. (2021). *Information Visualization*, 4th ed. Morgan Kaufmann.
- Wertheimer, M. (1923). Untersuchungen zur Lehre von der Gestalt II.
  *Psychologische Forschung*, 4, 301–350.
