# Workshop 4 — Homework (Final)
## Netflix Dataset: Complete EDA

**Due**: Before Workshop 5, Module 1
**Format**: R script + Python script + PDF/HTML report (max 8 pages) + dashboard exports
**Weight**: 5% of total grade

### The Assignment
Perform a complete EDA on the Netflix dataset following the seven-section structure. This is the summative assessment for Workshop 4.

### Required Sections
1. **Data description** (1 page): rows, columns, types, multi-valued columns, duration split
2. **Cleaning audit trail**: steps with row counts, genre/country explosion, duration parsing
3. **Missingness audit**: matrix + % bar + shadow analysis of director by type
4. **Univariate EDA**: duration histogram (Movies), seasons bar (TV), genre bar, rating bar
5. **Bivariate EDA**: releases per year by type (line), duration by rating (boxplot), country by type (stacked bar)
6. **Six-panel dashboard**: composed with patchwork (R) and GridSpec (Python), panel labels, title, caption
7. **Four numbered findings**: Finding → Evidence → Implication format. At least one temporal, one missingness, one distributional.

### Bonus (up to +3 points)
- Auto-EDA report (ydata-profiling or DataExplorer) with 3 anomalies identified
- Parameterised Quarto template that accepts Movie vs TV Show as a parameter

### Submission Checklist
- [ ] `W04_homework.R` + `W04_homework.py`
- [ ] `netflix_dashboard_R.pdf` + `netflix_dashboard_R.png`
- [ ] `netflix_dashboard_Py.pdf` + `netflix_dashboard_Py.png`
- [ ] PDF/HTML report (max 8 pages)
