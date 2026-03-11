# Workshop 1 · Module 7 — Course Notes
## Critique & Redesign Workshop

---

### 1. The Four-Quadrant Critique Framework

Systematic chart critique requires a shared vocabulary that avoids subjective reactions ("I don't like it") in favour of diagnostic specificity. The four-quadrant framework organises critique into distinct quality dimensions:

**Quadrant 1 — Data Integrity**: Does the chart honestly represent the underlying data? Check axes for truncation (lie factor), verify that scales are labelled with units, confirm that the data has not been cherry-picked or selectively filtered to support a predetermined narrative. References: Tufte's lie factor (M02), Anscombe's quartet (M01).

**Quadrant 2 — Visual Encoding**: Is each variable mapped to the most effective perceptual channel? Verify against the Cleveland & McGill ranking (M03). Check whether the chart type matches the analytical goal (comparison → bar, trend → line, relationship → scatter). Flag any use of area or angle for precise quantitative comparisons.

**Quadrant 3 — Design Craft**: Evaluate the data-ink ratio (M02), typographic hierarchy (M05), colour palette selection (M04), and whitespace allocation (M05). Look for chartjunk: 3-D effects, moiré patterns, decorative images, heavy gridlines.

**Quadrant 4 — Communication**: Can the intended audience extract the main message within the expected viewing time? Does the title state a finding rather than merely naming the chart? Are annotations guiding the reading? Is a clear takeaway present?


### 2. Five Canonical Redesign Patterns

**Pie → Horizontal Bar**: Pie charts encode values as angles, which rank fifth on Cleveland & McGill's accuracy scale. Redesigning as a sorted horizontal bar with direct labels replaces angle with position (rank 1) and eliminates the legend.

**Dual Y-Axis → Indexed Lines**: Dual y-axes create a false visual correlation between two unrelated series. Indexing both series to 100 at the first period normalises them to a common scale, and relative growth rates become directly comparable.

**Spaghetti Lines → Small Multiples**: When more than three lines overlap on a single panel, conjunction search (M03) makes individual trend identification impossible. Faceting into small multiples exploits Gestalt proximity to create readable per-series panels.

**Rainbow Scatter → Grey + Accent**: Colouring all categories with equal saturation creates visual egalitarianism — no category stands out. Replacing with grey background points and a single accent colour on the focal category leverages pre-attentive pop-out (M03).

**Truncated Axis → Zero Baseline**: A y-axis starting near the data minimum inflates visual differences. Restoring the zero baseline brings the lie factor to approximately 1.0. Adding a dashed reference line at the first-period value provides context for change.


### 3. The Redesign Workflow

Every redesign follows five steps:

1. **Identify** the visual problem (what feels wrong or misleading).
2. **Diagnose** which critique quadrant the problem belongs to.
3. **Sketch** an alternative on paper (3 minutes maximum).
4. **Implement** in code (R or Python), applying the relevant principle.
5. **Validate** with a peer using the five-step review protocol.


### 4. Peer Review Protocol

The five-step peer review protocol structures feedback:

1. **First Impression** (5 seconds): What do you see first? What is the message?
2. **Data Integrity Check**: Verify axes, labels, scales; compute lie factor if suspicious.
3. **Encoding Audit**: Is each variable on the best available channel?
4. **Design Craft Review**: Data-ink ratio, chartjunk, typography, whitespace.
5. **Communication Test**: Can a non-expert understand the chart in 30 seconds?

Feedback should follow the **SBI model** (Situation, Behaviour, Impact): describe the context, identify the specific design decision, and explain its effect on the reader's interpretation.


### References

- Kirk, A. (2019). *Data Visualisation*, 2nd ed. SAGE.
- Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
- Schwabish, J. (2021). *Better Data Visualizations*. Columbia University Press.
- Wainer, H. (1984). How to display data badly. *The American Statistician*, 38(2), 137–147.
