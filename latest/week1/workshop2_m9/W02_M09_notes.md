# Workshop 2 · Module 9 — Course Notes
## Tidy Data & Data Wrangling for Viz

### 1. Tidy Data: Three Rules
Wickham (2014) defines tidy data with three rules: (1) every column is a variable, (2) every row is an observation, (3) every cell is a single value. ggplot2 requires tidy data because `aes()` maps column names to visual channels. If a variable is encoded across multiple columns (e.g., years as column headers), the data must be reshaped before plotting.

### 2. Wide vs Long
**Wide** format stores each time period or category as a separate column — readable for humans but incompatible with `aes(color = year)`. **Long (tidy)** format stacks all values into a single column with an identifier column — verbose but plot-ready. `pivot_longer()` (R) / `melt()` (Python) converts wide to long. `pivot_wider()` / `pivot_table()` reverses the operation. The diagnostic test: "Can I name a single column for each aesthetic?"

### 3. Six Core Verbs
The dplyr verbs with pandas equivalents: **filter** → `query()` (keep rows), **select** → `[[cols]]` (keep columns), **mutate** → `assign()` (transform columns), **arrange** → `sort_values()` (sort rows), **group_by** → `groupby()` (set groups), **summarise** → `agg()` (compute aggregates). These six verbs chain via `|>` (R) or method chaining (Python) to form a linear data transformation pipeline.

### 4. The Wrangle-to-Viz Pipeline
The canonical pattern: `read_csv() |> filter() |> mutate() |> group_by() |> summarise() |> ggplot() + geom_*()`. In R, the pipe `|>` connects wrangling verbs; the `+` connects ggplot2 layers. In Python, parenthesised method chaining serves as the pipe, then `fig, ax = plt.subplots()` starts the plot.

### 5. Common Data Problems
Six problems arise repeatedly: missing values (`drop_na()` / `dropna()`), wrong types (`as.numeric()` / `pd.to_numeric()`), inconsistent categories (`fct_recode()` / `str.lower()`), wide format (`pivot_longer()` / `melt()`), duplicates (`distinct()` / `drop_duplicates()`), and outliers (filter with IQR rule).

### 6. Joins
`left_join()` (R) / `merge(how="left")` (Python) preserves all rows from the primary table and attaches matching columns from the secondary table. `inner_join` keeps only matches. `anti_join` finds unmatched rows. Use `left_join` by default to avoid silently dropping records.

### References
- McKinney, W. (2022). *Python for Data Analysis*, 3rd ed., Chs. 7–8.
- Wickham, H. (2014). Tidy Data. *JSS*, 59(10), 1–23.
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed., Chs. 3–7.
