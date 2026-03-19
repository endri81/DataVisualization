# Workshop 6 · Module 9 — Homework
## Case Study: e-Car Temporal Analysis

**Due**: Before Workshop 6, Module 10 (Lab)
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 6 homework (5% of total grade)

### Part A — Three-Line Rate Chart (20 points)
Produce a line chart showing yearly mean Rate, Cost of Funds, and Spread (2002–2012) with 2008 crisis annotation (vertical line + shaded rectangle + text label). In 150 words, explain the mechanism: why did rates drop? Why did spreads compress? When did spreads recover?

### Part B — Volume and Approval (15 points)
Produce side-by-side: (a) yearly loan volume bar chart, (b) yearly approval rate line chart. Both with 2008 annotation. In 100 words, describe how volume and approval responded to the crisis.

### Part C — Quarterly CI Ribbon (20 points)
Compute quarterly mean Rate ± 95% CI. Produce a ribbon chart with the Lehman collapse (September 15, 2008) annotated. In 150 words, explain: (a) why do CIs widen during the crisis? (b) when do they narrow again? (c) could CI width serve as an early warning indicator of financial stress?

### Part D — Tier Stratification (20 points)
Produce: (a) small multiples of mean Rate by Tier over time (one panel per tier), (b) grey+accent highlighting Tier 1. In 150 words, compare: did the crisis affect all tiers equally? Which tier's rate changed most, and why?

### Part E — Four Temporal Findings (25 points)
Write four numbered findings in Finding → Evidence → Implication format:
- At least one must reference the spread dynamics
- At least one must reference the tier stratification
- At least one must reference the quarterly CI pattern
- At least one must discuss the pre vs post 2008 distributional shift

### Submission Checklist
- [ ] `W06_M09_homework.R` + `W06_M09_homework.py`
- [ ] Figures: rate_spread_cof, volume_approval, quarterly_ci, tier_multiples, tier_accent, spread_pre_post (300 dpi)
- [ ] PDF report (max 6 pages)
