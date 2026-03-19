# Workshop 5 · Module 9 — Course Notes
## Snow's Cholera Map: Saving Lives with Data

### 1. The 1854 Broad Street Outbreak
In August–September 1854, a devastating cholera outbreak struck the Soho district of London, killing 616 people in a concentrated area around Broad Street (now Broadwick Street). The prevailing medical theory was **miasma** — the belief that cholera spread through "bad air" from rotting organic matter. John Snow, a physician who had already published on waterborne cholera transmission, saw the outbreak as an opportunity to test his hypothesis empirically.

Snow's method was revolutionary in its simplicity: **map the deaths, map the water pumps, and look for spatial association**. He walked the streets, recorded the address of every death, and plotted them on a map alongside the 13 public water pumps in the area. The visual evidence was striking: deaths clustered tightly around the Broad Street pump, with far fewer deaths near other pumps. Snow presented this evidence to the Board of Guardians, who removed the pump handle on September 8, 1854. The outbreak was already waning (as cholera outbreaks naturally do), but the pump removal was a landmark moment in public health: a policy decision driven by spatial data visualization.

### 2. The Map's Visual Logic
Snow's original map (published in the 1855 second edition of *On the Mode of Communication of Cholera*) used **stacked bars** at each address to represent death counts, not individual dots. Modern recreations typically use dot maps for clarity. The key visual insight requires only two layers: deaths (points) and pumps (points). When overlaid, the spatial clustering is immediately apparent — no statistical test needed.

This is the foundational principle of **spatial epidemiology**: overlay outcome data (disease cases) on exposure data (environmental features) and look for spatial association. The same logic applies to any point-source hypothesis: pollution and cancer clusters, fast-food outlets and obesity, bus stops and pedestrian accidents.

### 3. Voronoi Tessellation
A Voronoi tessellation partitions the plane so that every location is assigned to its nearest "seed" point (in this case, the nearest pump). The resulting polygons are called Voronoi cells. If cholera transmission were unrelated to pumps, deaths would be distributed proportionally across Voronoi cells (i.e., roughly proportional to each cell's population). Instead, the Broad Street cell contains a grossly disproportionate share of deaths — strong spatial evidence of a point-source.

In R: `st_voronoi(st_union(pumps_sf))` from the `sf` package. In Python: `scipy.spatial.Voronoi(pump_coords)` + `voronoi_plot_2d()`. The Voronoi approach formalises what Snow's eye did intuitively: assign each death to the nearest pump and count.

Modern applications of Voronoi in spatial analysis: hospital catchment areas (which hospital is closest to each neighbourhood?), school districts, delivery zones, cell tower coverage, and any "nearest facility" problem.

### 4. Modern GIS Recreation
With today's tools, Snow's analysis takes minutes rather than weeks:

| 1854 (Snow) | 2025 (Modern GIS) |
|---|---|
| Hand-drawn map on paper | `leaflet` / `folium` interactive map |
| Visual clustering by eye | KDE density surface (quantitative) |
| Manual pump-distance estimation | Voronoi tessellation + `st_distance()` |
| Miasma debate, no formal test | Spatial point pattern tests (Ripley's K) |
| One-time report to Board of Guardians | Reproducible Quarto report, shareable HTML |

The technology changes; the reasoning is timeless. Snow's genius was not the tools but the **logic**: form a spatial hypothesis, collect georeferenced data, visualize the overlay, and use the visual evidence to drive policy.

### 5. Spatial Epidemiology Today
Snow's method generalised: map the outcome (disease), map the exposure (environmental feature), look for spatial association. Contemporary examples:

**COVID-19 dashboards** (Johns Hopkins, WHO): choropleth maps of case rates + time series. Used globally for policy decisions (lockdowns, vaccine distribution).

**Environmental health**: pollution sources (factories, waste sites) overlaid with disease clusters. The "Erin Brockovich" pattern: if cancer cases cluster around a contamination source, the spatial association suggests (but doesn't prove) a causal link.

**Healthcare access**: Voronoi analysis of hospital locations reveals "healthcare deserts" — areas where the nearest hospital is >30 minutes away. Isochrone maps (travel-time contours) are a more realistic alternative to Voronoi when road networks matter.

**Vaccination coverage**: district-level choropleth maps of vaccination rates identify under-served areas. Overlaying with demographic data reveals equity gaps.

### 6. The Broader Lesson for Data Visualization
Snow's map is one of the most cited examples in the history of data visualization (Tufte, 1997; Johnson, 2006) not because of its technical sophistication but because of its **impact**: a single map changed public health policy. The lesson for all data visualization: the goal is not a pretty picture but a **decision**. The best visualization is one that makes the correct action obvious.

### References
- Snow, J. (1855). *On the Mode of Communication of Cholera*, 2nd ed. London: John Churchill.
- Johnson, S. (2006). *The Ghost Map: The Story of London's Most Terrifying Epidemic*. Riverhead Books.
- Tufte, E. (1997). *Visual Explanations*, Chapter 2 ("The Cholera Epidemic in London, 1854").
- Gilbert, E. W. (1958). "Pioneer Maps of Health and Disease in England." *Geographical Journal*, 124(2).
- UCLA Snow dataset: https://blog.rtwilson.com/john-snows-cholera-data/
- Robin Wilson's GitHub: https://github.com/robinwilson/john-snow-data (real coordinates)
