# Workshop 4 · Module 3 — Course Notes
## Data Wrangling for Visualization (Python)

### 1. Method Chaining as Python's Pipe
pandas supports method chaining: `df.method1().method2().method3()`. Wrapping the entire chain in parentheses `(...)` enables multi-line expressions without backslash continuation. This is Python's equivalent of R's pipe `|>`, producing the same top-to-bottom readability. The `.assign()` method creates columns inline (like `mutate()`), and `.query()` filters rows with string expressions (like `filter()`).

### 2. R ↔ Python Rosetta Stone
Nine core mappings: `filter()` → `.query()` or boolean indexing; `select()` → `df[cols]`; `mutate()` → `.assign()`; `arrange()` → `.sort_values()`; `group_by() + summarise()` → `.groupby().agg()`; `count()` → `.value_counts()`; `pivot_longer()` → `pd.melt()`; `pivot_wider()` → `.pivot_table()`; `left_join()` → `pd.merge(how='left')`.

### 3. The Core Trio: .assign(), .query(), .groupby().agg()
**.assign()**: creates new columns using `lambda d:` to reference the DataFrame being transformed. Supports chained column creation where later lambdas can reference columns created by earlier ones (within the same `.assign()` call in pandas 0.25+). **.query()**: string-based row filtering with `@variable` syntax for external variables. **.groupby().agg()**: named aggregation with `(column, function)` tuples — the cleanest syntax for multi-metric summaries.

### 4. Reshaping
`pd.melt(df, id_vars, var_name, value_name)` converts wide→long (equivalent to `pivot_longer()`). `.pivot_table(index, columns, values, aggfunc)` converts long→wide (equivalent to `pivot_wider()`). `.explode()` handles multi-valued cells: split a string column into a list with `.str.split(", ")`, then `.explode()` to create one row per value (equivalent to `separate_rows()`).

### 5. Common Cleaning Patterns
Six patterns: (1) **Missing values**: `.dropna(subset=["col"])` or `.fillna(0)`. (2) **Type conversion**: `pd.to_numeric(errors="coerce")` converts unparseable values to NaN. (3) **String cleaning**: `.str.replace("M", "")` + `.pipe(pd.to_numeric)`. (4) **Date parsing**: `pd.to_datetime(format="%B %d, %Y", errors="coerce")`. (5) **Recoding**: `np.where(condition, true_val, false_val)` for binary; `np.select(conditions, values, default)` for multi-condition. (6) **Explode**: `.str.split(", ").explode()` for multi-valued columns.

### 6. Anti-Joins in pandas
pandas has no built-in `anti_join()`. Two patterns: (a) `df[~df["key"].isin(other["key"])]` — simple and common. (b) `pd.merge(df, other, on="key", how="left", indicator=True).query("_merge == 'left_only'")` — more explicit, handles composite keys.

### References
- McKinney, W. (2022). *Python for Data Analysis*, 3rd ed., Chapters 5, 7–8.
- VanderPlas, J. (2016). *Python Data Science Handbook*, Chapter 3.
- pandas docs: https://pandas.pydata.org/docs/
