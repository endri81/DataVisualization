# Workshop 7 · Module 7 — Course Notes
## Case Study: Netflix Data Story

### 1. From EDA to Narrative
This module demonstrates the complete transformation from exploratory findings (W04-W06) to a polished explanatory data story. The Netflix dataset serves as the case because students have already extracted findings in W04-M10 (Netflix Lab), W06-M08 (Netflix Temporal), and earlier modules. The task is not to find new insights but to **assemble known findings into a compelling narrative**.

### 2. Planning the Deck: Storyboard First
The deck is planned as a **storyboard** before any code is written. The process:

**Step 1 — Big Idea**: "Netflix should accelerate investment in original series and local-language content because movie additions have declined 42% since 2019 while international genres are the fastest-growing category."

**Step 2 — List findings**: from W04-W06, the student has 10–15 findings. Not all belong in the story.

**Step 3 — Select 6–8 findings** ranked by audience impact: the movie decline, the TV pivot, genre growth, India's rise, seasonal patterns, composition shift. Cut anything that doesn't serve the Big Idea.

**Step 4 — Order as story arc**: Context (catalog growth) → Complication (movie decline) → Contrast (Movie vs TV) → Analysis/Climax (genre growth + India) → Seasonal detail → Resolution (composition shift) → Call to Action (4 strategic recommendations).

**Step 5 — Assign chart types** using the story type framework (M04): each finding maps to a story type, each story type maps to a natural chart.

### 3. The 10-Slide Structure
| Slide | Assertion Headline | Story Type | Chart | Arc Position |
|-------|-------------------|------------|-------|--------------|
| 1 | (Title) | — | — | — |
| 2 | Netflix built 8,800+ titles over a decade | Zoom Out | Area | Context |
| 3 | Movie additions declined 42% from peak | Change | Line (accent) | Complication |
| 4 | TV grew 3× faster than Movies (indexed) | Contrast | Dual line | Complication |
| 5 | International = fastest-growing genre | Change | Bar (accent) | Analysis |
| 6 | India rose from #5 to #2 | Zoom Out | Bump chart | Analysis |
| 7 | Friday + Q4 = release calendar | Drill Down | Calendar heatmap | Detail |
| 8 | TV share grew 20% → 35% | Change | Stacked area % | Resolution |
| 9 | Four strategic actions | Factors | Action table | CTA |
| 10 | Explore the dashboard | — | Link/QR | Appendix |

### 4. Design Consistency Across Slides
The deck maintains visual consistency through:

**Colour language**: grey (#DDDDDD) = context, blue (#1565C0) = primary story, red (#E53935) = warnings/callouts, green (#2E7D32) = positive findings. This palette is used consistently — the audience learns the encoding from slide 2 and reads all subsequent slides faster.

**Layout**: every body slide uses assertion-evidence format (M05). Title = finding. Body = full-width annotated chart. No bullet points.

**Typography**: bold 14pt titles, 10pt subtitles in grey, 7pt captions. Consistent across all slides.

**Annotation style**: direct labels at endpoints (no legends), callout boxes for key metrics, reference lines for benchmarks.

### 5. The Title Sequence Test
The most powerful quality check: read ONLY the 10 slide titles in sequence, ignoring all charts. Does the story make sense? If the titles alone tell a coherent narrative, the deck works. The charts provide proof; the speaker provides colour and nuance.

This test catches two common failures: (a) topic titles that convey no information ("Genre Analysis"), and (b) illogical ordering (resolution before complication).

### 6. The Martini Glass Ending
Slides 1–9 are **author-driven** (linear narrative). Slide 10 transitions to **reader-driven** by providing a dashboard link for self-service exploration. This implements the Martini Glass model (M02): guided narrative → free exploration. The appendix slide says "I've told you the story; now here's the tool to ask your own questions."

### References
- Knaflic, C. N. (2015). *Storytelling with Data*. Chapters 7–10.
- Knaflic, C. N. (2019). *SWD: Let's Practice!* Chapters 9–10.
- Duarte, N. (2010). *Resonate*. Chapter 4.
