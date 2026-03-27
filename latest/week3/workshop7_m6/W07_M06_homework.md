# Workshop 7 · Module 6 — Homework
## Declutter & Redesign

**Due**: Before Workshop 7, Module 8
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 7 homework (5% of total grade)

### Part A — Clutter Audit (20 points)
Take ONE chart from your W04–W06 work. List every non-data element present (gridlines, borders, legend style, background, etc.). For each element, state: (a) is it data-ink or non-data-ink? (b) does removing it reduce understanding? (c) should it stay or go? Present as a table with at least 8 rows.

### Part B — Before/After Makeover (35 points)
Using the same chart from Part A: (a) reproduce the original "before" version with all its clutter, (b) produce the "after" version applying as many of the 12 declutter steps as relevant. Produce both in R and Python (4 charts total). Present before/after side-by-side. In 200 words, describe each change you made and why it improves clarity.

### Part C — Incremental Declutter Panel (25 points)
For a DIFFERENT chart (Netflix or e-Car), produce the 4-stage incremental declutter: Stage 0 (raw), Stage 1 (remove borders/background), Stage 2 (fix chart type + remove grid), Stage 3 (grey+accent + labels + callout). Arrange as a 2×2 panel. This demonstrates the transformation process step-by-step.

### Part D — Theme Template (20 points)
Create a reusable clean theme: `theme_clean` in R (using `theme()` elements) and `clean_params` dict for `rcParams` in Python. Apply it to three different charts (line, bar, scatter) to demonstrate that it works across chart types. In 100 words, explain which theme settings you consider essential vs optional.

### Submission Checklist
- [ ] `W07_M06_homework.R` + `W07_M06_homework.py`
- [ ] Clutter audit table (in PDF)
- [ ] Before/after pair (300 dpi)
- [ ] 4-stage declutter panel (300 dpi)
- [ ] 3 charts with clean theme applied (300 dpi)
- [ ] PDF report (max 6 pages)
