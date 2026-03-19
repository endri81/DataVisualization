# Workshop 5 · Module 10 — Course Notes
## Lab: Multivariate EDA on Real Estate Data

### 1. Dataset Overview
The real estate dataset contains 200 property listings in Tirana, Albania with 13 variables: price (EUR), area (sqm), bedrooms, bathrooms, year_built, floor, type (apartment/house), condition (new/renovated/original), longitude, latitude, neighbourhood, and derived price_sqm. This dataset is both **multivariate** (6 numeric features for PCA, heatmaps, parallel coordinates) and **spatial** (lat/lon for point maps). The lab integrates every W05 technique into a single coherent analysis.

### 2. The Integration Challenge
Previous modules taught individual techniques in isolation. This lab requires combining them:
- **W04 EDA** (M01–M06): cleaning, distributions, outliers, correlation → the dashboard
- **W05 multivariate** (M01–M04): PCA biplot, parallel coordinates, clustered heatmap → feature structure
- **W05 spatial** (M05–M09): point map, interactive map → geographic patterns

The key question is: **do the multivariate patterns (PCA clusters, correlation structure) align with the spatial patterns (geographic price gradients)?** This is the kind of integrated analysis that separates data scientists from analysts.

### 3. Analysis Pipeline

**Step 1: Six-panel dashboard** (W04 pattern). (a) Price histogram (right-skewed → log-normal), (b) area histogram (approximately normal), (c) type bar (75% apartment, 25% house), (d) area vs price scatter by type (positive, houses steeper), (e) price/sqm by neighbourhood boxplot (Blloku premium visible), (f) price by condition violin.

**Step 2: PCA biplot** (W05-M03). Six numeric features → StandardScaler → PCA(n=2). PC1 captures the "size-price axis" (price, area, bedrooms load together). PC2 captures the "age-floor axis" (year_built, floor). Houses separate from apartments along PC1 (larger, more expensive). Loading arrows show which variables drive each PC; the angle between price and area arrows ≈ 0° (strong positive correlation).

**Step 3: Correlation heatmap** (W05-M04). Lower-triangle clustered heatmap of the 6 numeric features. Price–area correlation is strongest (~0.7). Bedrooms–bathrooms cluster together. Year_built is weakly correlated with other features (independent dimension).

**Step 4: Parallel coordinates** (W05-M02). Five axes (price, area, bedrooms, bathrooms, year_built), coloured by type. Houses trace a higher path on price and area; apartments cluster in the lower range. The grey+accent strategy highlights the type separation.

**Step 5: Spatial point map** (W05-M05–M07). Properties plotted on Tirana coordinates, colour = price/sqm (plasma), size = area. Geographic patterns emerge: Blloku neighbourhood (central) shows higher price/sqm; peripheral areas are cheaper. This spatial gradient was invisible in the non-spatial panels.

**Step 6: Interactive map** (W05-M08). Folium/leaflet with popups showing all property details. Zoom into Blloku to see the premium cluster. Toggle between price/sqm colouring and type colouring. The interactive version enables individual property inspection impossible in static maps.

### 4. Four Key Findings (Finding → Evidence → Implication)

**Finding 1**: Price is driven primarily by area, with a type multiplier. Evidence: PCA biplot shows price and area arrows nearly parallel; scatter shows houses have steeper slope. Implication: price prediction models should use area × type interaction.

**Finding 2**: Blloku commands a ~30% price premium. Evidence: boxplot of price/sqm by neighbourhood; spatial map shows central cluster of high values. Implication: neighbourhood is a critical feature for pricing; location effects dominate physical characteristics.

**Finding 3**: Year_built is an independent dimension. Evidence: PCA biplot shows year_built arrow orthogonal to price-area cluster; weak correlation in heatmap. Implication: age is not priced into the market (perhaps because renovation status matters more than original build year).

**Finding 4**: 75% of listings are apartments. Evidence: type bar chart + parallel coordinates show apartments dominate. Implication: house comparisons have wider confidence intervals (smaller sample); stratify any analysis by type.

### 5. Workshop 5 Synthesis
This lab demonstrates that multivariate and spatial visualization are complementary, not competing. PCA reveals the feature structure; the heatmap confirms it; the spatial map adds the geographic dimension invisible in feature space. The complete toolkit from W05: multi-encoded scatter (M01), parallel coordinates (M02), PCA biplot (M03), clustered heatmap (M04), spatial data handling (M05), choropleth (M06), point maps (M07), interactive maps (M08), spatial reasoning (M09). Every technique contributes a unique perspective.

### References
- All W05 module references apply.
- Tirana real estate market context: INSTAT Albania (https://www.instat.gov.al)
