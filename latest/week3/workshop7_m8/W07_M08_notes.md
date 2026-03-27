# Workshop 7 · Module 8 — Course Notes
## Case Study: e-Car Data Story

### 1. A Different Kind of Story
The Netflix story (M07) was a **forward-looking strategy pitch**: "here's what's happening, here's what we should do." The e-Car story is a **backward-looking post-mortem**: "here's what happened during the 2008 crisis, here's what we should learn, and here's what we should monitor going forward." Both use the same storytelling techniques (assertion-evidence, grey+accent, callouts, story arc) but with fundamentally different tone, audience, and call to action.

### 2. The Big Idea
"The bank should integrate CI-based pricing volatility monitoring because the 2008 crisis caused a ~2pp rate drop with differential tier impact and slow spread recovery."

Subject: the bank. Action: integrate monitoring. Evidence: crisis impact + tier differential + slow recovery + CI signal.

### 3. The 8-Slide Storyboard

**Title**: "e-Car Lending: Lessons from the 2008 Crisis"

**Slide 1 — Context** (Zoom Out): "150,000 auto loans processed across five credit tiers." Volume bar chart establishes the portfolio scale. The audience needs to know this is substantial — not a toy dataset.

**Slide 2 — Complication / Hero** (Change Over Time): "Loan rates dropped ~2pp after the 2008 crisis." Grey+accent line with the full annotation treatment. This is the hero chart — the core finding that motivates the rest of the analysis.

**Slide 3 — Mechanism** (Factors): "Rate = Cost of Funds + Spread. The Fed cut CoF; competition compressed spread." Three-line decomposition chart. This is the analytical contribution — it explains WHY rates dropped, not just that they dropped. The audience should think: "oh, it wasn't that banks became generous — it was a mechanical effect."

**Slide 4 — Tier Impact** (Contrast): "Tier 1 borrowers received the largest rate cuts — a regressive benefit." Grey+accent on Tier 1 across all tiers over time. This is the equity insight: the safest borrowers got the best deals during the crisis, while high-risk borrowers saw minimal relief.

**Slide 5 — Uncertainty Signal** (Outlier): "Quarterly CI width is an early warning indicator of financial stress." CI ribbon chart showing widening during the crisis and narrowing after. This is the forward-looking insight that transforms a backward-looking post-mortem into an actionable monitoring recommendation. The CI widened BEFORE the crisis peaked — suggesting it could serve as a leading indicator.

**Slide 6 — Recovery + CTA**: "Spread recovered post-2010 but never returned to pre-crisis levels." Three-period comparison bar chart (pre/crisis/recovery median spread). The partial recovery means a new equilibrium, not a return to normal. CTA: "Integrate CI-based pricing volatility monitoring into the quarterly review process."

### 4. The Mechanism Slide
The mechanism slide (Slide 3) deserves special attention because it's the slide that distinguishes a data story from a data report. A report would say "rates dropped." The story explains WHY: the three-line decomposition (Rate = CoF + Spread) shows that the rate drop was driven by two distinct forces — the Fed cutting Cost of Funds (monetary policy) AND banks competing for shrinking demand (compressing their margin). This decomposition is the analytical insight that makes the story valuable to a risk officer.

### 5. Netflix vs e-Car: Structural Comparison

| Dimension | Netflix (M07) | e-Car (M08) |
|---|---|---|
| Domain | Entertainment | Finance |
| Audience | Content strategist | Risk officer |
| Orientation | Forward-looking (what to do) | Backward-looking (what to learn) |
| Complication | Decline = opportunity for pivot | Crisis = systemic risk event |
| Mechanism | Genre shift + global expansion | Fed rate cuts + competition |
| Key annotation | Growth % callout | Crisis event marker + CI width |
| Tone | Optimistic strategic pivot | Cautionary analytical lesson |
| CTA | "Invest in originals" | "Build early warning system" |

The storytelling TECHNIQUES are identical (assertion-evidence, grey+accent, callout boxes, story arc). The CONTENT and TONE adapt to domain and audience. This demonstrates that the W07 framework is domain-agnostic.

### 6. Financial Storytelling Specifics
Financial data stories have distinctive requirements: (a) **event annotations** are essential — the audience needs to connect data patterns to events they remember (Lehman collapse, Fed rate decisions). (b) **decomposition** (factors story type) is the analytical contribution — stakeholders want to know the mechanism, not just the symptom. (c) **forward-looking insights** transform post-mortems from "interesting history" to "actionable monitoring" — the CI width as early warning is the bridge. (d) **regulatory context** matters — if the audience includes compliance officers, mention regulatory implications.

### References
- Thomas, L. C. (2009). *Consumer Credit Models*. Oxford.
- Reinhart, C. & Rogoff, K. (2009). *This Time Is Different*. Princeton.
- Federal Reserve rate history: https://fred.stlouisfed.org
- Knaflic, C. N. (2019). *SWD: Let's Practice!* Ch. 10.
