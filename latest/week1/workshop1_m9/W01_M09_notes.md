# Workshop 1 · Module 9 — Course Notes
## Python Environment Setup & Matplotlib Basics

---

### 1. Installation

The recommended Python setup uses Miniconda to create an isolated environment (`conda create -n dataviz python=3.11`), then installs packages with `pip install numpy pandas matplotlib seaborn plotnine scipy openpyxl`. JupyterLab (`pip install jupyterlab; jupyter lab`) provides a notebook-centric IDE with code cells, Markdown cells, inline plot output, and a file browser.

The critical JupyterLab shortcuts are Shift+Enter (run cell, advance), Escape (Command Mode for navigation), Enter (Edit Mode for typing), A/B (insert cell above/below), and M/Y (toggle Markdown/Code).


### 2. The Python Data Science Stack

The Python data science ecosystem parallels R's tidyverse. **NumPy** provides N-dimensional arrays and linear algebra — the foundation for all numerical computation. **pandas** provides the DataFrame abstraction, analogous to tibble + dplyr: `read_csv()`, `groupby()`, `merge()`, `pivot_table()`. **matplotlib** is the core plotting library, structured as Figure → Axes → Artists. **seaborn** sits atop matplotlib and provides statistical visualization functions with cleaner defaults and built-in aggregation. **plotnine** is a direct port of R's ggplot2 grammar to Python.


### 3. pandas Data Types

The six pandas data types relevant to visualization are:

- **float64**: continuous measurements (equivalent to R's numeric)
- **int64**: integers (equivalent to R's integer)
- **object**: strings — often indicates a column that needs type conversion
- **bool**: booleans (equivalent to R's logical)
- **category**: categorical with defined levels (equivalent to R's factor); created via `pd.Categorical()`
- **datetime64**: timestamps (equivalent to R's Date/POSIXct); created via `pd.to_datetime()`

Use `df.dtypes` to inspect all column types, `df.info()` for types plus null counts, and `df.describe()` for summary statistics. Type conversion uses `pd.to_numeric()`, `pd.to_datetime()`, and `pd.Categorical()`.


### 4. Matplotlib Architecture

Matplotlib is organised in three layers. The **Figure** is the entire canvas: `fig = plt.figure()` or `fig, ax = plt.subplots()`. It controls size (`figsize`), resolution (`dpi`), background, and the super-title. The **Axes** is a single plot area: each axes holds data, title, labels, ticks, and spines. A figure can contain multiple axes (multi-panel). **Artists** are every visible element: Line2D objects from `ax.plot()`, PathCollection from `ax.scatter()`, Rectangle patches from `ax.bar()`, and Text objects from `ax.set_title()`.

Matplotlib exposes two APIs. The **pyplot** API (`plt.plot()`) uses an implicit state machine modelled after MATLAB — convenient for one-liners but opaque for complex plots. The **Object-Oriented** API (`fig, ax = plt.subplots(); ax.plot()`) gives explicit control over every element. This course uses the OO API exclusively.


### 5. The Four Fundamental Chart Types

**`ax.scatter(x, y)`**: key parameters are `s` (marker size in points²), `c` (colour — single string or array), `alpha` (transparency 0–1), `edgecolors`, `marker` (shape).

**`ax.hist(data)`**: key parameters are `bins` (integer or sequence), `color`, `edgecolor`, `density=True` (normalize to PDF), `histtype` ("bar", "step", "stepfilled"), `cumulative=True`.

**`ax.barh(categories, values)`**: use horizontal bars by default (labels readable without rotation). Key parameters: `height` (bar width), `color`, `edgecolor`. Use `ax.bar()` for vertical only when the x-axis is temporal or ordinal.

**`ax.boxplot(list_of_arrays)`**: key parameters are `labels`, `patch_artist=True` (enables fill colour), `notch=True` (adds CI on median), `whis=1.5` (whisker extent), `vert=False` (horizontal).


### 6. Multi-Panel Layouts

`plt.subplots(rows, cols)` creates a regular grid and returns `(fig, axes)`. Access individual panels via `axes[row, col]`. Use `sharey=True` or `sharex=True` for shared axes. For unequal panels, use `matplotlib.gridspec.GridSpec` with `height_ratios` and `width_ratios`. Slice notation (`gs[1, :]`) spans multiple columns.


### 7. The OO Template

Every plot in this course follows the same five-step pattern: (1) create figure and axes, (2) plot data, (3) set labels and title, (4) apply Tufte cleanup (remove top/right spines), (5) save with `bbox_inches="tight"`. This template is the Python counterpart of R's `ggplot() + geom_*() + theme_minimal() + labs() + ggsave()`.


### References

- McKinney, W. (2022). *Python for Data Analysis*, 3rd ed. O'Reilly.
- VanderPlas, J. (2016). *Python Data Science Handbook*. O'Reilly. https://jakevdp.github.io/PythonDataScienceHandbook/
- Matplotlib Tutorials: https://matplotlib.org/stable/tutorials/
