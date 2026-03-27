# Workshop 8 · Module 8 — Course Notes
## Case Study: e-Car Interactive Dashboard

### 1. Financial vs Content Dashboards
The e-Car dashboard applies the same W08 framework as the Netflix dashboard (M07) but adapts it for financial analytics. Key differences: the primary dimension is credit tier (ordered 1–5) rather than content type (categorical), the key metrics are rate and spread (continuous financial variables) rather than title count, and the domain requires event annotation (2008 crisis) and uncertainty visualisation (CI ribbon) that are less common in content analytics.

### 2. Dashboard Specification
The e-Car dashboard has the same structural template as Netflix (Few's grid) but with domain-specific panels:

**Filter bar**: Tier checkboxes (not dropdown — users compare tier subsets), Year range slider, Metric radio buttons (Rate / Spread / CoF — a reconfiguration interaction), Reset button.

**KPI row**: Total filtered loans, Average rate, Average spread, Approval rate. Each updates reactively when filters change.

**Primary chart — Rate Trend by Tier**: plotly line chart with one trace per selected tier, using a sequential blue palette (Tier 1 = lightest, Tier 5 = darkest). The 2008 crisis is annotated as a shaded rectangle + dashed vertical line on every temporal panel.

**Secondary chart — Spread Distribution**: plotly histogram with tier-coloured overlays. Shows the distributional shape of the bank's margin — useful for identifying bimodal pricing or tier-specific outliers.

**Detail panels**: (a) Quarterly CI ribbon — mean rate ± 1.96·SE, showing pricing volatility. CI width is a leading risk indicator (M06-W06). (b) Approval rate by tier over time — reveals credit-standard tightening during the crisis. (c) Loan table — sortable, searchable, filterable.

### 3. Domain-Specific Design Choices

**Sequential colour for ordered tiers**: unlike Netflix's categorical palette (Movie=blue, TV=red), e-Car's tiers have a natural order (1=best credit, 5=worst). The palette should reflect this ordering: light blue for Tier 1 (low risk) through dark blue for Tier 5 (high risk). This is a direct application of W01-M03 colour theory: ordered data → sequential palette; categorical data → qualitative palette.

**Metric switcher (reconfiguration)**: radio buttons let the user switch the y-variable across all charts without changing the dashboard structure. This implements Yi et al.'s "reconfiguration" interaction type (M01). The chart template stays the same; only the data column changes. Implementation: `input$metric` in Shiny or `Input("metric", "value")` in Dash selects which column to aggregate.

**Crisis annotation on all temporal panels**: the 2008 crisis is the dominant feature of the dataset. Every temporal chart (rate trend, CI ribbon, approval rate) should include the same annotation — a shaded rectangle (2007.5–2009.5) and optionally a "Lehman collapse" text marker. Consistency ensures the user sees the crisis impact across all metrics simultaneously. In plotly: use `layout(shapes=list(...))` to add the rectangle.

**CI ribbon**: unique to analytical dashboards. The CI ribbon shows not just the mean rate per quarter but the uncertainty around that mean. During the 2008 crisis, the CI widens dramatically — indicating pricing volatility and inconsistency. This is the financial equivalent of a "risk signal" and is a forward-looking monitoring metric: if CI starts widening again, it may signal a new stress period.

### 4. Netflix vs e-Car: Dashboard Comparison

| Dimension | Netflix (M07) | e-Car (M08) |
|---|---|---|
| Primary dimension | Content type (2 categories) | Credit tier (5 ordered levels) |
| Colour palette | Categorical (blue/red) | Sequential (light→dark blue) |
| Key metric | Title count | Rate / Spread / CoF |
| Unique input | Type dropdown | Tier checkboxes + metric radio |
| Event annotation | Global expansion, COVID | 2008 financial crisis |
| Unique panel | Genre breakdown | CI ribbon (volatility) |
| Regulatory relevance | None | Fair lending, credit standards |
| Cross-filter | Click country → filter all | Click tier → filter (optional) |

### 5. Single Reactive Pattern (Reused)
The architectural pattern from M07 is identical: one `reactive()` / `@callback` filters the data, and all panels read from this single filtered source. This ensures consistency — when the user deselects Tier 5, ALL panels (trend, distribution, CI, approval, table) exclude Tier 5 loans simultaneously.

### References
- All M01–M07 references apply.
- Thomas, L. C. (2009). *Consumer Credit Models*. Oxford.
- Few, S. (2006). *Information Dashboard Design*. Analytics Press.
