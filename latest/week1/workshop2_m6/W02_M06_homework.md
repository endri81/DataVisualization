# Workshop 2 · Module 6 — Homework
## Theme Mastery

**Due**: Before Workshop 2, Module 8
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — Before & After (25 points)
Take any chart from your W01 homework. Produce two versions: (a) with `theme_gray()` (ggplot2 default), (b) with a custom theme that applies at least 6 `element_*()` modifications. Show side by side in both R and Python. List each modification and explain its purpose.

### Part B — Custom Theme Function (25 points)
Write `theme_unyt()` in R that: starts with `theme_minimal()`, sets bold 14pt title, italic grey caption left-aligned, removes minor gridlines and major x gridlines, places legend at bottom, and adds 10pt margins. Write the Python equivalent as `apply_unyt_theme(ax)`. Apply both to a scatter plot of Reviews vs Rating.

### Part C — Theme Comparison (25 points)
Produce the same scatter plot with five different themes: theme_minimal, theme_classic, theme_bw, theme_void, and one from ggthemes (e.g., theme_economist). Arrange in a 2×3 patchwork grid. In 150 words, explain which theme you would use for: (a) a journal article, (b) an executive slide, (c) a web dashboard.

### Part D — Export Quality (25 points)
Export one chart in four formats: PDF, SVG, PNG@300dpi, PNG@72dpi. Compare file sizes. In 100 words, explain when to use each format and why JPEG should never be used for charts.

### Submission Checklist
- [ ] `W02_M06_homework.R` + `W02_M06_homework.py`
- [ ] theme_unyt() function (R) + apply_unyt_theme() function (Python)
- [ ] All figures as PNG (300 dpi) + one PDF export
- [ ] PDF report (max 4 pages)
