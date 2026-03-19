# Workshop 6 · Module 8 — Course Notes
## Case Study: Netflix Content Trends Over Time

### 1. The Netflix Dataset as Temporal Case Study
The Netflix dataset (8,800+ titles, 2008–2021) is ideal for demonstrating temporal visualization because it contains multiple temporal signals at different granularities: **yearly** trends (catalog growth, type shift), **monthly** patterns (release scheduling), **seasonal** cycles (holiday releases, Q4 spikes), and **event responses** (global expansion in 2016, COVID-19 in 2020). This module applies every W06 technique to extract these signals.

### 2. The Movie Peak and TV Pivot
The most important temporal finding: movie additions peaked around 2017–2019 and then declined, while TV Show additions grew steadily through 2020. This reflects Netflix's strategic shift from licensed movie content (cheap to acquire, high volume, low differentiation) to original series content (expensive to produce, lower volume, high differentiation and subscriber retention).

Visualization: a simple two-line chart (Movie vs TV Show yearly additions) makes this pivot immediately visible. The crossover point (~2019–2020 depending on metric) is the key strategic date. Use direct labels at line endpoints rather than a legend.

### 3. Genre Evolution
Different genres followed different trajectories. "International Movies" and "International TV Shows" grew fastest in relative terms, reflecting Netflix's aggressive global expansion strategy (starting with the January 2016 launch in 130+ new countries). "Dramas" and "Comedies" remained the largest absolute genres but grew more slowly in relative terms (mature categories).

Visualization: grey+accent strategy on a 5-genre line chart highlights the fastest grower. Alternative: small multiples (one panel per genre) with free y-axis reveals each genre's individual trajectory without the spaghetti problem.

### 4. Event Annotations Transform the Story
A monthly additions line chart without annotations is just a squiggly line. Add three vertical dashed lines with text labels and it becomes a narrative:

**January 2016 — Global expansion**: Netflix launched in 130 new countries simultaneously. The subsequent surge in additions reflects the need to fill new regional catalogs.

**March 2020 — COVID-19 lockdown**: production halted worldwide. The effect appears as a dip in new additions ~3–6 months later (pipeline lag: titles already in post-production continued arriving, but new productions stopped).

**Mid-2021 — Content slowdown**: the combined effect of COVID production delays, subscriber growth plateauing, and strategic shift toward fewer, higher-quality titles. Monthly additions declined from peak levels.

These annotations apply the M02 principle: event annotations transform description ("titles went up and down") into explanation ("titles went up because of X, down because of Y").

### 5. Cumulative vs Rate
Two complementary views of the same data:

**Cumulative stacked area**: shows total catalog size growing over time. Movies dominate the absolute count, but TV Shows' share is growing. The 100% stacked version reveals this proportional shift more clearly: TV Show share grew from ~20% to ~35% of the catalog.

**Rate (monthly additions)**: shows the velocity of growth — how many titles are added per month. This can decrease even while the cumulative total keeps growing. The rate view reveals the 2020 slowdown that the cumulative view smooths away.

**Design rule**: always state which you're showing. "Netflix added fewer titles in 2021" (rate) is very different from "Netflix had more titles in 2021 than ever before" (cumulative). Both are true.

### 6. Seasonal Pattern
The seasonal subseries plot (2016–2021 overlaid on Jan–Dec) reveals Netflix's release calendar: additions tend to spike in December/January (holiday season audience) and July (summer). The pattern is not as rigid as traditional TV (which has fixed "fall premiere" and "spring finale" seasons) because Netflix releases on a rolling basis, but there is a measurable seasonal shape.

The grey+accent technique (grey = historical years, red = current year) answers "is 2021 following the normal seasonal pattern?" — and the answer is "yes in shape, but lower in level" (the COVID production pipeline effect).

### 7. Country Dynamics
The top content-producing countries changed over time. The United States dominates in absolute count but its share has been declining as India, the UK, Japan, and South Korea ramp up production. A bump chart or bar chart race (M07) visualizes these rank changes. The temporal dimension reveals that India's growth accelerated sharply after 2018 (Netflix's investment in Bollywood and regional-language content).

### 8. Integration: Five-Panel Dashboard
The complete temporal case study combines: (a) yearly type line chart (the strategic overview), (b) monthly annotated timeline (the event narrative), (c) genre trends grey+accent (the content strategy), (d) cumulative stacked area (the catalog composition), (e) seasonal subseries (the release calendar). Each panel uses a different W06 technique and answers a different question. Together they constitute a complete temporal EDA.

### References
- Netflix dataset: Kaggle (Shivam Bansal, 2021).
- Netflix Q4 2020 Shareholder Letter (production pipeline disclosure).
- All W06 module references (M01–M07 techniques) apply.
