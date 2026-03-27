# Workshop 7 · Module 1 — Course Notes
## Narrative Structure in Data Communication

### 1. From Exploration to Explanation
Workshops 1–6 built the technical toolkit: chart types, perception, EDA, multivariate, spatial, and temporal visualization. Workshop 7 addresses the critical last mile: **turning findings into decisions**. A chart that nobody acts on has zero value regardless of its technical sophistication.

The core shift is from **exploratory** visualization (for the analyst: see everything, find patterns) to **explanatory** visualization (for the audience: focused, annotated, one message per chart). Knaflic (2015) frames this as the difference between showing your work and sharing your conclusions. In exploratory mode, the analyst is the audience — complexity is acceptable because you control the pace. In explanatory mode, you are presenting to someone who has 30 seconds of attention and needs to understand the implication immediately.

### 2. The Data Story Arc
Every effective data presentation follows a narrative arc adapted from dramatic structure:

**Act 1 — Context**: establish what the audience already knows or needs to know. "Netflix grew its catalog to 8,800+ titles by 2021." This is the shared ground — uncontroversial facts that set up the tension.

**Act 2 — Complication**: introduce the problem, gap, or surprise. "But movie additions have declined 40% since their 2019 peak." This creates tension — the audience wants to know why and what to do about it.

**Act 3 — Climax**: the key insight. "COVID halted production pipelines, and Netflix's strategic shift toward original series accelerated the movie decline." This is the peak of information density — the chart that carries the main finding.

**Act 4 — Resolution**: what the data means. "The era of massive catalog expansion is over. Quality over quantity is the new strategy." This translates the finding into business meaning.

**Act 5 — Call to Action**: what should happen next. "Invest in 20 flagship original series per quarter; reduce catalog filler acquisitions by 30%." This is the decision the data supports. Without a call to action, the presentation is informational but not actionable.

### 3. Knaflic's Framework: Six Lessons
Cole Nussbaumer Knaflic's *Storytelling with Data* (2015) provides the most widely adopted framework for explanatory visualization. The six lessons map directly to our course:

**Lesson 1: Understand the context** — before making any chart, answer: Who is the audience? What do you want them to *do*? How will you communicate (live presentation, email, dashboard)? Write a one-sentence **Big Idea**: "[Subject] should [action] because [data evidence]."

**Lesson 2: Choose an effective display** — W03 (chart type selection). Bar, line, scatter — pick the geometry that best encodes the relationship you want to show.

**Lesson 3: Eliminate clutter** — W01 (data-ink ratio, Tufte). Remove gridlines, borders, redundant labels, and decorations that don't carry data. This will be elaborated in W07-M06 (Declutter & Redesign).

**Lesson 4: Focus attention** — W01 (pre-attentive attributes), W06-M02 (grey+accent). Use colour, size, and position to direct the eye to the one element that carries the message.

**Lesson 5: Think like a designer** — W01 (affordances, alignment, whitespace). Gestalt principles, typography, and layout create a professional, trustworthy impression.

**Lesson 6: Tell a story** — this module. Weave findings into a narrative arc. This is the NEW content of W07 — everything else was covered in earlier workshops.

### 4. The Big Idea
Before creating any explanatory visualization, write a one-sentence Big Idea:

**Structure**: [Subject] should [action] because [data evidence].

**Example**: "Netflix should accelerate original series investment because movie additions have declined 40% since 2019 while TV Show additions continue to grow."

The Big Idea has three components: the **subject** (who should act), the **action** (what they should do), and the **evidence** (why the data supports this). If you cannot write this sentence, you are not ready to present — you need more analysis.

### 5. Descriptive vs Declarative Titles
The chart title is the single most important text element. Two philosophies:

**Descriptive** (exploratory default): "Monthly Netflix Additions (2015–2021)". States what the chart shows. Appropriate for dashboards and exploratory notebooks where the reader draws their own conclusions.

**Declarative** (explanatory best practice): "Netflix additions peaked in 2019 and have since declined". States what the chart **means**. The title IS the finding; the chart is the evidence. This is the **assertion-evidence** model (Garner, 2013) that will be elaborated in W07-M05.

For every explanatory chart, use a declarative title. It forces you to articulate the finding explicitly, and it ensures the audience gets the message even if they only glance at the chart.

### 6. From Findings to Narrative
The practical process of building a data story from EDA results:

1. **List findings** from W04–W06 (e.g., the "Key Findings" printed at the end of each case study module).
2. **Rank by audience impact** — what matters most to *them*, not to you.
3. **Select 3–5 findings** — more dilutes the message.
4. **Order as a story arc** — start with context, build to the most important finding (climax), end with the action.
5. **One chart per finding** — each chart carries exactly one message.
6. **Annotate for the audience** — declarative title, direct labels, callouts, no legend where possible.

### References
- Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
- Knaflic, C. N. (2019). *Storytelling with Data: Let's Practice!* Wiley.
- Segel, E. & Heer, J. (2010). Narrative Visualization. *IEEE TVCG*, 16(6).
- Duarte, N. (2010). *Resonate*. Wiley.
- Garner, J. (2013). The Assertion-Evidence Approach. Penn State.
