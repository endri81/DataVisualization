# Workshop 7 · Module 5 — Course Notes
## Assertion-Evidence Slide Design

### 1. The Problem with Traditional Slides
Traditional presentation slides use a **topic title** ("Revenue Update") followed by 5–8 **bullet points** with a chart squeezed into a corner. Research shows this format fails: (a) the audience reads the bullets faster than the speaker can narrate, losing synchronisation; (b) 6+ bullet points exceed working memory capacity (Miller's 7±2); (c) the chart is decorative rather than central — it competes with the bullets for attention; (d) the topic title ("Revenue Update") conveys no information — the audience must read the entire slide to discover the message.

The assertion-evidence model, developed by Michael Alley and colleagues at Penn State (Alley & Neeley, 2005; Garner, 2013), replaces this structure with two elements: a **sentence headline** that states the finding (the assertion) and a **full-width visual** that provides the proof (the evidence).

### 2. The Assertion-Evidence Model
Each slide contains exactly two elements:

**The assertion (title)**: a complete sentence stating the finding. Not a topic label, not a question, not a fragment — a full declarative sentence. Maximum 2 lines, under 15 words. Examples: "Movie additions declined 42% from their 2019 peak." "India rose to #2 in content production."

**The evidence (body)**: a single full-width chart, diagram, or table that visually supports the assertion. No bullet points. The visual occupies 60–80% of the slide area. It must be annotated, focused, and carry exactly one message.

**Test**: cover the chart and read only the title. Can the audience understand the key message? If yes, the title is a proper assertion. If they need to see the chart to know what the slide is about, the title is a topic label and should be rewritten.

### 3. Writing Sentence Headlines
The most common mistake is writing topic titles ("Genre Breakdown") instead of assertion headlines ("International content is Netflix's fastest-growing category"). The transformation:

| Topic Title | Assertion Headline |
|---|---|
| "Revenue by Quarter" | "Q3 revenue exceeded target by 18%" |
| "Netflix Content Trends" | "Movie additions peaked in 2019 and declined since" |
| "Loan Rate Analysis" | "Tier 1 borrowers received the largest rate cuts" |
| "Genre Breakdown" | "International content is the fastest-growing category" |

Guidelines: (a) use a subject-verb-object structure; (b) include the specific finding (not just the topic); (c) keep under 15 words; (d) the headline should be understood without seeing the chart.

### 4. Progressive Reveal
In a live presentation, showing the complete annotated chart all at once overwhelms the audience. Progressive reveal builds the chart in 4 steps:

**Build 1 — Frame**: show only the axes (x-axis with dates, y-axis with scale). The speaker says: "Let me show you Netflix movie additions over 7 years."

**Build 2 — Data**: add the data line/bars. "Here's the trajectory — notice the peak around 2019."

**Build 3 — Annotation**: add the reference line, callout, and highlight. "The decline from peak is 42% — let me show you exactly where."

**Build 4 — Assertion**: reveal the sentence headline. "So the headline here: movie additions declined 42% from their 2019 peak."

Implementation: In Beamer, use `\only<1>{...}` overlays. In PowerPoint, use "Appear" animations on grouped chart layers. In Quarto Revealjs, use `.fragment` divs. In Python/R: save 4 PNG versions with increasing layers and insert as separate slides.

### 5. Deck-Level Structure
A 10-slide assertion-evidence deck follows the story arc (M01):

Slide 1: **Title slide** (presenter, topic, date)
Slides 2–3: **Context** — 1–2 assertion slides setting the scene ("Netflix built 8,800+ titles...")
Slides 4–6: **Complication** — 2–3 assertion slides presenting the problem ("But movies are declining...")
Slides 7–8: **Analysis** — 1–2 assertion slides explaining the drivers ("International content drives growth...")
Slide 9: **Resolution** — one assertion slide with the recommended action ("Invest in originals and local markets")
Slide 10: **Call to Action** — specific, measurable next steps ("Approve the Q2 content budget reallocation")

Each body slide = one assertion + one evidence chart. The slide count equals the number of key findings plus framing slides.

### 6. The One-Message-Per-Slide Rule
Each slide carries exactly one finding. If a chart supports two findings, split into two slides (duplicate the chart with different annotations). If a finding needs two charts for evidence, use a two-panel layout on one slide — but both panels must support the same assertion headline.

This rule prevents the common failure mode of "kitchen-sink" slides that try to communicate everything at once and communicate nothing effectively.

### References
- Garner, J. (2013). The Assertion-Evidence Approach. Penn State. https://www.assertion-evidence.com
- Alley, M. & Neeley, K. (2005). Rethinking the Design of Presentation Slides. *Technical Communication*, 52(4).
- Reynolds, G. (2012). *Presentation Zen*, 2nd ed. New Riders.
- Duarte, N. (2008). *slide:ology*. O'Reilly.
