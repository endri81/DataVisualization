# Workshop 1 · Module 8 — Course Notes
## R Environment Setup & Base Graphics

---

### 1. Installation and RStudio

R is installed from CRAN (https://cran.r-project.org). RStudio (https://posit.co/download/rstudio-desktop) provides a four-pane IDE: Source Editor (top-left), Environment/History (top-right), Console (bottom-left), and Files/Plots/Help (bottom-right). The most critical keyboard shortcut is Cmd+Shift+M (macOS) or Ctrl+Shift+M (Windows) for inserting the native pipe operator `|>`.


### 2. The tidyverse Ecosystem

A single `library(tidyverse)` call loads eight core packages: `readr` (fast CSV/TSV import), `dplyr` (data wrangling verbs: filter, mutate, group_by, summarise, arrange), `tidyr` (reshaping: pivot_longer, pivot_wider), `ggplot2` (Grammar of Graphics visualisation), `stringr` (string operations), `forcats` (factor manipulation), `purrr` (functional programming), and `tibble` (modern data frames). Additional visualization packages installed separately include `viridis`, `RColorBrewer`, `ggthemes`, `patchwork`, `ggrepel`, and `scales`.


### 3. R Data Types

R's six fundamental data types relevant to visualization are:

- **numeric** (double): continuous measurements (`42.5`, `3.14`)
- **integer**: whole numbers, suffixed with `L` (`1L`, `42L`)
- **character**: text strings (`"hello"`, `"NYC"`)
- **logical**: boolean flags (`TRUE`, `FALSE`, `NA`)
- **factor**: categorical variables with defined levels, optionally ordered
- **Date**: calendar dates created via `as.Date("2024-01-15")`

Use `class(x)` to check a single object's type and `str(df)` or `glimpse(df)` to inspect all columns in a data frame. Type mismatches — numbers stored as characters, dates stored as strings — are the most common source of plotting errors.


### 4. Base R Graphics

Base R provides four fundamental plotting functions that require zero package dependencies.

**`plot(x, y)`** produces a scatterplot. Key parameters: `pch` (point shape; 16 = filled circle), `col` (colour), `cex` (size multiplier), `main` (title), `xlab/ylab` (axis labels). Use `abline()` to overlay regression lines and `legend()` for a manual legend.

**`hist(x)`** produces a histogram. Key parameters: `breaks` (number of bins or breakpoints), `col` (fill), `border` (edge colour). Overlay a density curve with `lines(density(x))`.

**`barplot()`** produces bar charts from named vectors or tables. Key parameters: `horiz = TRUE` (horizontal), `beside = TRUE` (grouped rather than stacked), `border = NA` (remove edges).

**`boxplot(y ~ group)`** uses R's formula interface to produce grouped box plots. Key parameters: `notch = TRUE` (confidence interval on median), `col` (fill colour per group). Overlay mean points with `points()`.


### 5. The par() System

`par()` controls global graphics parameters. `par(mfrow = c(r, c))` sets up an r×c grid for multi-panel layouts, filled row by row. `par(mar = c(bottom, left, top, right))` sets margins in lines. Always save the old parameters before modification (`old_par <- par(...)`) and restore afterward (`par(old_par)`) to prevent side effects on subsequent plots.


### 6. The Pipe Operator

R 4.1+ introduced the native pipe `|>`, which passes the left-hand side as the first argument of the right-hand function. The pipe transforms nested, inside-out function calls into linear, left-to-right data flows. The tidyverse historically used `%>%` from the magrittr package; the native `|>` is now preferred for new code.


### 7. Base R vs ggplot2

Base R graphics are optimal for rapid exploratory checks: one line of code produces a functional chart. ggplot2 excels at publication-quality output: its layered grammar, declarative theming system, and faceting infrastructure make it the tool of choice for any chart that will be shared with others. Workshop 2 covers ggplot2 in depth.


### References

- Murrell, P. (2018). *R Graphics*, 3rd ed. Chapman & Hall/CRC.
- Peng, R. D. (2016). *Exploratory Data Analysis with R*. Leanpub.
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed. O'Reilly. https://r4ds.hadley.nz
