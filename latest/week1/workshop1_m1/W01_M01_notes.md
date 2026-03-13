# Workshop 1 · Module 1 — Course Notes
## Why Visualize? The Case for Data Viz

---

### 1. The Information Overload Problem

Modern organisations generate data at rates that far exceed human cognitive
capacity. The working memory constraint of approximately seven items (Miller,
1956) means that tables with more than roughly 20 rows become effectively
unreadable without aggregation or visual encoding. Visualization exploits the
massive bandwidth of the human visual cortex—which processes spatial patterns
orders of magnitude faster than sequential text—to compress high-dimensional
data into interpretable form.

Visualization serves three distinct analytical purposes:

- **Exploratory**: discover unanticipated patterns and generate hypotheses
  (Tukey, 1977).
- **Explanatory**: communicate known findings to an audience (Knaflic, 2015).
- **Confirmatory**: assess whether observed data conform to a model (Cleveland,
  1993).

A common error is to skip the exploratory phase. One cannot explain what one
has not first discovered.


### 2. Historical Masterpieces

Four canonical examples demonstrate that principled data visualization has
a centuries-long tradition of combining statistical rigour with design clarity.

**Charles Joseph Minard (1869)** — *Carte figurative des pertes successives
en hommes de l'Armée française dans la campagne de Russie 1812–1813.* Encodes
six variables (army size, latitude, longitude, direction of travel,
temperature, date) on a single two-dimensional plane. Tufte (1983) calls it
"the best statistical graphic ever drawn."

**Florence Nightingale (1858)** — The polar-area diagram ("coxcomb") showing
that preventable disease killed far more soldiers in the Crimean War than
battle wounds. The chart persuaded Parliament to fund sanitary reforms.
A foundational example of *persuasive* visualization.

**John Snow (1854)** — The Broad Street cholera map, which plotted deaths as
stacked bars on a street map and revealed spatial clustering around a
contaminated water pump. Arguably the first spatial epidemiological analysis.

**W. E. B. Du Bois (1900)** — Data portraits presented at the Paris
Exposition documenting African-American economic progress post-Emancipation.
Striking modernist designs—spiral charts, proportional-area displays—used
data as a tool of social justice.


### 3. Anscombe's Quartet

Anscombe (1973) constructed four bivariate datasets that share identical
summary statistics:

| Statistic | Value |
|-----------|-------|
| Mean of x | 9.0 |
| Mean of y | 7.50 |
| SD of x | 3.32 |
| SD of y | 2.03 |
| Correlation | 0.816 |
| Regression | y = 3.0 + 0.5x |

Yet the four scatterplots reveal entirely different structures: Dataset I is
linear; Dataset II is curvilinear; Dataset III contains an outlier pulling the
regression; Dataset IV has a single influential leverage point.

**Lesson**: summary statistics are necessary but not sufficient. Always plot
your data before modelling.


### 4. The Datasaurus Dozen

Matejka and Fitzmaurice (2017) extended Anscombe's idea using simulated
annealing to generate 13 datasets—including a dinosaur shape—with identical
first-order statistics (means ≈ 54.3, SDs ≈ 16.8/26.9, r ≈ −0.06). The
exercise demonstrates that even in higher-dimensional or larger-N settings,
summary statistics are an unreliable proxy for data structure.

Both R (`datasauRus` package) and Python (TSV from the GitHub repository)
provide convenient access for classroom reproduction.


### 5. Principles of Effective Visualization

**Edward Tufte (1983)** defines graphical excellence as complex ideas
communicated with clarity, precision, and efficiency. Key concepts:

- **Data-ink ratio** = (ink representing data) / (total ink). Maximise by
  removing gridlines, borders, and decorative elements that do not encode data.
- **Chartjunk** = non-data ink that does not contribute to understanding:
  moiré patterns, 3-D effects, gradient fills, decorative images ("ducks").
- **Lie factor** = (size of effect in graphic) / (size of effect in data).
  Values outside the range [0.95, 1.05] indicate visual distortion.

**Alberto Cairo (2012)** offers five complementary qualities of good
visualization: truthful, functional, beautiful, insightful, and enlightening.

**Tamara Munzner (2014)** proposes a nested model of four design layers:
(1) domain problem characterisation, (2) data/task abstraction, (3) visual
encoding and interaction idiom, (4) algorithm design. Errors at outer layers
propagate inward and cannot be fixed by inner-layer improvements.


### 6. Practical Checklist

Before publishing any chart, verify:

1. **Purpose** — What specific question does this chart answer?
2. **Data integrity** — Does the encoding accurately represent the data?
3. **Audience** — Who will read this and what prior knowledge do they have?
4. **Clarity** — Can the message be grasped in under five seconds?


### References

- Anscombe, F. J. (1973). Graphs in statistical analysis. *The American
  Statistician*, 27(1), 17–21.
- Cairo, A. (2012). *The Functional Art*. New Riders.
- Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
- Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
- Matejka, J., & Fitzmaurice, G. (2017). Same stats, different graphs.
  *Proc. CHI 2017*, 1290–1294.
- Miller, G. A. (1956). The magical number seven. *Psychological Review*,
  63(2), 81–97.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*.
  Graphics Press.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
