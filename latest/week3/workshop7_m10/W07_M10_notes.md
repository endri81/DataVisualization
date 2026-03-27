# Workshop 7 · Module 10 — Course Notes
## Lab: Build a 10-Slide Data Story Deck

### 1. Lab Purpose
This is the summative assessment for Workshop 7 (Storytelling with Data). It integrates every technique from M01–M09 into a single deliverable: a 10-slide assertion-evidence deck built from one of the course datasets. The lab tests the student's ability to execute the complete pipeline from raw EDA findings to a presentation-ready data story.

### 2. The Complete Pipeline
The 10-step pipeline maps directly to workshop modules:

**Step 1** (M01): Write the Big Idea — one sentence with subject + action + evidence. This anchors the entire deck.

**Step 2** (M04): List all EDA findings from W04–W06. Classify each by story type (change, drill-down, zoom-out, contrast, intersection, factors, outlier).

**Step 3** (M01): Select 5–8 findings that form a coherent story arc. Order as: context → complication → evidence → resolution → CTA. Discard findings that don't serve the narrative (most EDA findings will be discarded).

**Step 4** (M05): Write an assertion headline for each slide — a complete sentence under 15 words that IS the finding. Apply the cover-chart test: can the audience understand the message from the title alone?

**Step 5** (M06): Set the clean theme globally (`theme_set()` in R, `rcParams` in Python) so every chart inherits decluttered defaults.

**Step 6** (M03): Build each chart with appropriate annotations — ggrepel for scatter labels, callout boxes for key findings, reference lines for benchmarks, shaded regions for highlighted periods, direct labels instead of legends.

**Step 7** (M06): Audit each chart against the 12-step declutter checklist. Remove any non-data-ink element that doesn't earn its place.

**Step 8** (M02): Verify that every chart is author-driven (explanatory), not reader-driven (exploratory). No chart should look like raw EDA output.

**Step 9** (M09): Produce at least one audience variant — the same finding adapted for a different audience (executive, technical, or public). This demonstrates the adaptation skill.

**Step 10**: Compose all slides as individual PNGs (300 DPI) plus one composed vertical panel for the PDF report. Write the 300-word reflection.

### 3. The 10-Slide Structure
The required structure ensures narrative coherence:

| Slide | Role | Story Type | Purpose |
|-------|------|-----------|---------|
| 1 | Title | — | Dataset, audience, date, presenter |
| 2 | Context | Zoom Out | Establish scale/baseline |
| 3 | Complication | Change | The tension (hero chart) |
| 4 | Evidence 1 | Varies | First supporting finding |
| 5 | Evidence 2 | Varies | Second supporting finding |
| 6 | Evidence 3 | Varies | Third supporting finding |
| 7 | Mechanism | Factors | Why the pattern exists |
| 8 | Resolution | Factors | Recommended actions |
| 9 | Audience variant | — | Same hero, different audience |
| 10 | CTA | — | Specific actionable request |

Slides 4–6 must use at least 3 different story types (from the seven in M04), demonstrating range.

### 4. Assessment Rubric (100 points)

| Criterion | Points | Key Question |
|-----------|--------|-------------|
| Big Idea statement | 10 | Subject + action + evidence in one sentence? |
| Story arc structure | 15 | Storyboard follows context → complication → resolution? |
| Assertion headlines | 15 | Every title is a complete sentence stating the finding? |
| Chart quality | 25 | Grey+accent, direct labels, callouts, decluttered, clean? |
| Audience fit | 15 | Title style, jargon, complexity match stated audience? |
| Code quality | 10 | Runs end-to-end, commented, theme set globally? |
| Reflection | 10 | Thoughtful 300-word process reflection? |

### 5. Common Pitfalls
(1) Topic titles instead of assertion headlines — the most common mistake. (2) Bullet points anywhere in the deck — assertion-evidence means NO bullets. (3) Raw EDA charts without M03/M06 treatment — every chart must be explanatory. (4) No CTA — the deck ends with "interesting" instead of "here's what to do." (5) Skipping the audience variant (slide 9) — this is a required element. (6) Forgetting the reflection essay — 10 points for 300 words of honest process reflection.

### 6. Workshop 7 Complete Summary
After 10 modules, the student's storytelling toolkit includes: narrative arc (M01), exploratory→explanatory transition (M02), advanced annotation (M03), seven story types (M04), assertion-evidence design (M05), systematic decluttering (M06), case study execution on two datasets (M07–M08), audience adaptation across three archetypes (M09), and integrated deck building (M10). This toolkit applies to any dataset, any domain, and any audience.

### References
- All M01–M09 references apply.
- Knaflic, C. N. (2019). *SWD: Let's Practice!* Chapter 11 (Final exercises).
