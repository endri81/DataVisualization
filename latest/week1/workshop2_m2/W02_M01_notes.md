# Workshop 2 · Module 1 — Course Notes
## Wilkinson's Grammar of Graphics: Theory

---

### 1. The Problem with Chart Catalogues

The traditional approach to data visualization treats charts as a finite taxonomy: bar charts, pie charts, scatter plots, line charts, and so on. Each type has its own function signature, parameter set, and mental model. This catalogue approach has three structural weaknesses. First, it is inherently finite — novel analytical needs require inventing new chart types. Second, it is rigid — modifying one visual aspect (e.g., swapping colour encoding for faceting) often requires rewriting the entire chart from scratch. Third, it provides no systematic language for describing *why* one chart works better than another.


### 2. Wilkinson's Grammar: A Compositional System

Leland Wilkinson's *The Grammar of Graphics* (1999, 2nd ed. 2005) replaces the catalogue with a formal specification language. Just as a natural language grammar generates infinite sentences from finite vocabulary and syntax rules, the Grammar of Graphics generates infinite chart types from a finite set of composable components.

Wilkinson's specification pipeline has seven stages:

1. **Variables** — raw data columns
2. **Algebra** — cross, nest, and blend operations on variables
3. **Scales** — map data domains to visual ranges (position, colour, size)
4. **Statistics** — transform data (bin, smooth, aggregate) before rendering
5. **Geometry** — choose the visual mark (point, line, bar, area, polygon)
6. **Coordinates** — define the geometric space (Cartesian, polar, geographic)
7. **Aesthetics** — render the specification to screen or print

The key insight is independence: each stage can be modified without affecting the others. Changing the geometry from bars to lines does not require changing the data, scales, or coordinate system.


### 3. The Algebra of Graphics

At the core of Wilkinson's theory is a cross-product formulation:

    Chart = Data × Aesthetics × Geometry

This algebra means that the number of possible charts grows as the product of data mappings, aesthetic channels, and geometric marks — a combinatorial explosion that replaces the fixed catalogue. A scatter plot is (x, y) × (position, position) × point. A grouped bar chart is (x, y, fill) × (position, position, colour) × rectangle. A heatmap is (x, y, fill) × (position, position, colour) × tile.


### 4. Layered Construction

Wickham (2010) operationalised Wilkinson's theory in the ggplot2 R package, introducing a layered architecture where each `+` operator adds one component:

```
ggplot(data, aes(x, y, color)) +    # data + aesthetics
  geom_point() +                     # geometry
  geom_smooth(method = "lm") +       # statistic + geometry
  scale_color_brewer(palette) +      # scale
  facet_wrap(~group) +               # facets
  coord_cartesian() +                # coordinates
  theme_minimal()                    # theme
```

This progressive construction mirrors the design process: start by seeing the data (empty axes), add marks (points), add structure (smooth), then polish (labels, theme). The Python library `plotnine` implements near-identical syntax.


### 5. Same Data, Different Layers

The grammar's power is most visible when you hold some layers constant and vary one:

- **Same data + same aesthetics + different geometry**: a bar chart, line chart, and dot plot from the same mapping
- **Same data + same geometry + different aesthetics**: colour encoding vs faceting for a grouping variable
- **Same data + same geometry + different coordinates**: a bar chart in Cartesian becomes a pie chart in polar


### 6. Wilkinson (1999) vs Wickham (2010)

Wilkinson provided the mathematical theory: a formal specification language independent of any implementation. Wickham provided the practical implementation: ggplot2 in R, with four extensions — layered stacking, position adjustments (dodge, stack, jitter), default statistics per geometry, and a theme system that separates data encoding from visual styling. Read Wilkinson for the "why," Wickham for the "how."


### References

- Wickham, H. (2010). A layered grammar of graphics. *JCGS*, 19(1), 3–28.
- Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis*, 2nd ed. Springer.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly.
- Wilkinson, L. (2005). *The Grammar of Graphics*, 2nd ed. Springer.
