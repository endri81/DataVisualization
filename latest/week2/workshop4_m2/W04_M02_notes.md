# Workshop 4 · Module 2 — Course Notes
## Data Wrangling for Visualization (R)

### 1. The tidyverse Pipeline
The tidyverse is a collection of R packages sharing a common grammar and data structure (tibbles). The core wrangling pipeline flows: `readr::read_csv()` → `dplyr` verbs (filter, select, mutate, arrange, group_by, summarise) → `tidyr` reshaping (pivot_longer, pivot_wider) → `ggplot2` visualization. The pipe operator (`|>` or `%>%`) connects each step, passing the result of the left side as the first argument of the right side.

### 2. Six dplyr Verbs
**filter()**: keep rows matching a logical condition (equivalent to pandas `.query()` or boolean indexing). **select()**: keep, drop, or rename columns (equivalent to `df[cols]` or `.drop()`). **mutate()**: create new columns or transform existing ones (equivalent to `.assign()`). **arrange()**: sort rows (equivalent to `.sort_values()`). **group_by()**: set grouping for subsequent operations (equivalent to `.groupby()`). **summarise()**: compute one summary row per group (equivalent to `.agg()`).

### 3. Common Cleaning Patterns
Six patterns appear repeatedly when preparing data for visualization: (1) **Missing values**: `drop_na(col)` or `replace_na(list(col = 0))`. (2) **Type conversion**: `as.numeric()`, `as.Date()`, `mdy()` from lubridate. (3) **String cleaning**: `str_remove()`, `str_trim()`, `str_replace()` from stringr. (4) **Date parsing**: `lubridate::mdy()`, `dmy()`, `ymd()` for various date formats. (5) **Recoding**: `case_when()` for multi-condition recoding, `if_else()` for binary. (6) **Factor ordering**: `fct_reorder(Category, n)` sorts categories by a numeric variable for ggplot display.

### 4. Reshaping with tidyr
ggplot2 requires long (tidy) format. `pivot_longer(cols, names_to, values_to)` converts wide data (one column per year) to long (one row per year). `pivot_wider(names_from, values_from)` does the reverse for summary tables. `separate()` splits one column into two by a delimiter. `separate_rows()` explodes multi-valued cells into separate rows (essential for Netflix's `listed_in` column).

### 5. Pipe-to-Plot
The most powerful pattern: a single piped chain from raw data to finished chart with no intermediate variables. The chain reads: `read_csv() |> filter() |> mutate() |> group_by() |> summarise() |> ggplot() + geom_*()`. This makes the entire data→chart pipeline reproducible and auditable.

### 6. Joins
`left_join(x, y, by = "key")` keeps all rows from x and adds matching columns from y (most common for visualization). `inner_join()` keeps only matching rows. `anti_join()` keeps x rows with no match in y — invaluable for finding missing data.

### References
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed., Chapters 3–5.
- Wickham, H. (2014). Tidy Data. *JSS*, 59(10).
