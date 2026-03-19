# Workshop 6 · Module 9 — Course Notes
## Case Study: e-Car Temporal Analysis (2002–2012)

### 1. The e-Car Dataset as Temporal Case Study
The e-Car dataset contains ~150,000 auto loan applications spanning 2002–2012, a period that includes the 2008 global financial crisis — the dominant temporal feature in any financial dataset from this era. Each loan records the offered Rate, Cost of Funds (the bank's borrowing cost), the resulting Spread (Rate − CoF, i.e., the bank's margin), credit Tier (1–5), and the Outcome (approved/declined). This module treats the dataset as a temporal analysis exercise, applying W06 techniques to extract the crisis narrative.

### 2. The Three-Line Chart: Rate, Cost of Funds, and Spread
The most informative temporal view plots three lines: the offered Rate (what the customer sees), the Cost of Funds (what the bank pays to borrow), and the Spread (the bank's profit margin = Rate − CoF). Pre-2008, rates were high (~7%), CoF was moderate (~3%), and spreads were wide (~4pp). The 2008 crisis caused the Fed to slash benchmark rates, dragging CoF to near zero. Banks followed with lower offered rates, but spreads also compressed as banks competed for a shrinking pool of creditworthy borrowers. Post-2010, spreads began recovering as the market stabilised.

This three-variable temporal plot is more informative than any single-variable view because it reveals the **mechanism**: the rate drop was not banks being generous — it was the mechanical effect of lower CoF, with the competitive response visible in the spread compression.

### 3. Event Annotation: The 2008 Crisis
The crisis annotation is essential for interpretation. Without it, the chart shows "rates went down" — with it, the chart explains "rates went down because of the financial crisis." Three annotation techniques used: (a) a vertical dashed line at 2008, (b) a subtle shaded rectangle spanning 2007.5–2009.5 (the crisis window), (c) a text label. The Lehman Brothers collapse (September 15, 2008) is annotated on the quarterly chart as the specific trigger point.

### 4. Quarterly Resolution with Confidence Ribbon
Monthly or quarterly aggregation with ±95% CI ribbon reveals not just the level but the **precision** of the estimate. Pre-2008: narrow CIs (consistent pricing across loans). During 2008–2009: CIs widen dramatically (volatile, inconsistent pricing as banks scrambled to reprice risk). Post-2010: CIs narrow again (new equilibrium). This pattern — widening uncertainty during crisis — is a signature of financial stress that is invisible in point estimates alone.

### 5. Tier Stratification Over Time
Credit tiers encode risk: Tier 1 = best credit, Tier 5 = worst. Plotting mean rate by tier over time reveals differential crisis impact: Tier 1 rates dropped the most (banks competed aggressively for the safest borrowers, driving down margins), while Tier 5 rates remained high or even increased (risk premium persisted or grew as banks tightened credit standards). The grey+accent strategy highlights Tier 1 against a backdrop of all tiers.

This is a **multivariate temporal** pattern — combining W05 (multivariate: tier as a categorical moderator) with W06 (temporal: 11-year trajectory). Small multiples (one panel per tier) show the same information differently: each tier's trajectory is clearly readable, but direct comparison between tiers requires more eye movement.

### 6. Pre vs Post 2008: Distributional Shift
Overlaid histograms of Spread for pre-2008 and post-2008 periods reveal a distributional shift: the post-2008 distribution is shifted left (lower spreads) and has a different shape (more concentrated, fewer extreme outliers). Marking the median of each distribution with a dashed vertical line quantifies the shift. This static comparison complements the temporal line chart: the line shows when the shift happened, the histogram shows how much the distribution changed.

### 7. STL Decomposition
Applying STL decomposition to monthly mean Rate reveals: (a) the **trend** component captures the crisis-driven rate decline and partial recovery — the long-term story; (b) the **seasonal** component shows a modest within-year cycle (rates slightly higher in spring, lower in fall) — the bank's pricing calendar; (c) the **residual** shows spikes during the crisis — months where rates deviated from both trend and seasonal expectations. The 2008 crisis annotation on the trend panel highlights the exact timing.

### 8. Four Key Findings (Finding → Evidence → Implication)
**Finding 1**: The 2008 crisis caused a ~2pp rate drop over 2 years. Evidence: yearly rate line dropping from ~7% to ~5%. Implication: borrowers in 2009–2010 got historically cheap auto loans.

**Finding 2**: Spread compression was temporary, not permanent. Evidence: spread line shows recovery after 2010. Implication: the bank's pricing power returned as markets stabilised.

**Finding 3**: Tier 1 borrowers received the largest rate cuts. Evidence: tier stratification chart. Implication: the crisis benefited the safest borrowers most — a regressive effect.

**Finding 4**: Pricing volatility (CI width) is a leading indicator of financial stress. Evidence: quarterly CI ribbon widened before the official crisis declaration. Implication: CI width could serve as an early warning metric.

### References
- Thomas, L. C. (2009). *Consumer Credit Models: Pricing, Profit and Portfolios*. Oxford.
- Federal Reserve rate history: https://fred.stlouisfed.org/series/FEDFUNDS
- Cleveland, R. B. et al. (1990). STL: A Seasonal-Trend Decomposition. *Journal of Official Statistics*.
- All W06 module references apply.
