# Workshop 1 · Module 10 — Course Notes
## Comparative Lab: First Plots in R vs Python

---

### 1. Purpose of the Comparative Lab

This module is the capstone of Workshop 1. Its purpose is threefold: (a) demonstrate that R and Python produce identical analytical outputs from the same data, (b) build fluency in switching between the two languages, and (c) apply every principle from Modules 1–9 to a real dataset.

The Google Play Store dataset (Kaggle, ~10K apps) serves as the common testbed. It contains categorical variables (Category, Type, Content Rating), continuous variables (Rating, Reviews), and temporal data (Last Updated) — exercising all four fundamental chart types plus line charts and stacked bars.


### 2. Six Chart Types: R ↔ Python Mapping

**Horizontal Bar** (top 10 categories by count):
- R: `count() |> slice_max() |> fct_reorder() |> geom_col() + coord_flip()`
- Python: `.value_counts().head(10).sort_values()` → `ax.barh()`
- Principles applied: Tufte sorting (M02), direct labels (M05), spine removal (M05)

**Histogram** (rating distribution):
- R: `geom_histogram(bins=40)` + `geom_vline()` + `annotate("text")`
- Python: `ax.hist(bins=40)` + `ax.axvline()` + `ax.text()`
- Principles applied: reference line for context (M05), bin width choice (M03)

**Scatterplot** (reviews vs rating, coloured by type):
- R: `geom_point(aes(color=Type))` + `scale_x_log10()`
- Python: loop over types with `ax.scatter()` + `ax.set_xscale("log")`
- Principles applied: log scale for skewed data (M01), colour for nominal distinction (M04), alpha for overplotting (M03)

**Boxplot** (rating by Free/Paid):
- R: `geom_boxplot(notch=TRUE)` + `stat_summary(fun=mean)`
- Python: `ax.boxplot(patch_artist=True, notch=True)` + `ax.scatter()` for means
- Principles applied: notch for median CI, mean overlay for richer comparison (M03)

**Line Chart** (apps added per year by type):
- R: `geom_line() + geom_point()` + direct labels at endpoint
- Python: `ax.plot("o-")` + `ax.text()` at endpoint
- Principles applied: direct labelling eliminates legend (M05), temporal x-axis (M06)

**Stacked Bar** (Content Rating × Type):
- R: `geom_bar(position="stack")` + `scale_fill_manual()`
- Python: `pd.crosstab().plot.bar(stacked=True)`
- Principles applied: composition chart for part-to-whole (M06), categorical colour (M04)


### 3. Dashboard Assembly

Both R and Python support multi-panel composition. In R, `patchwork` operators (`|` for side-by-side, `/` for stacked) combine ggplot2 objects with `plot_annotation()` for titles. In Python, `GridSpec(2, 3)` creates a 2×3 grid with `fig.add_subplot()` for each panel and `fig.suptitle()` for the overall title.

The final six-panel dashboard is the deliverable for this lab: it demonstrates that a complete EDA can be produced in either language with equivalent quality and comparable code length.


### 4. Syntax Cheat Sheet

| Operation | R (tidyverse + ggplot2) | Python (pandas + matplotlib) |
|-----------|------------------------|------------------------------|
| Load CSV | `read_csv("f.csv")` | `pd.read_csv("f.csv")` |
| Filter | `filter(df, x == "a")` | `df.query("x == 'a'")` |
| Count | `count(Category)` | `.value_counts("Category")` |
| Sort | `arrange(desc(n))` | `.sort_values(ascending=False)` |
| Bar chart | `geom_col(fill="blue")` | `ax.barh(cats, vals)` |
| Histogram | `geom_histogram(bins=30)` | `ax.hist(x, bins=30)` |
| Scatter | `geom_point(aes(color=g))` | `ax.scatter(x, y, c=colors)` |
| Boxplot | `geom_boxplot(fill=Type)` | `ax.boxplot(data, patch_artist)` |
| Line | `geom_line(aes(color=g))` | `ax.plot(x, y)` |
| Save | `ggsave("p.pdf", w=7, h=5)` | `fig.savefig("p.pdf")` |
| Multi-panel | `patchwork: (p1 | p2) / p3` | `GridSpec(2, 3)` |


### 5. Workshop 1 Summary

Across ten modules, Workshop 1 established the theoretical and practical foundations for the entire course:

- M01–M02: Why visualize + Tufte's principles
- M03–M04: Perception science + colour theory
- M05–M06: Typography/layout + design process
- M07: Critique and redesign methodology
- M08–M09: R and Python environment setup
- M10: Comparative lab proving language parity

Workshop 2 builds directly on this foundation by introducing the Grammar of Graphics — ggplot2's layered system (R) and plotnine/seaborn (Python).


### References

- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed. https://r4ds.hadley.nz
- McKinney, W. (2022). *Python for Data Analysis*, 3rd ed. O'Reilly.
- Kaggle Google Play Store dataset: https://www.kaggle.com/datasets/lava18/google-play-store-apps
