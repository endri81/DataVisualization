# Workshop 4 · Module 2 — Homework
## Data Wrangling for Visualization (R)

**Due**: Before Workshop 4, Module 4
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Full Cleaning Pipeline (25 points)
Write a single piped chain that reads googleplaystore.csv and produces a clean tibble: remove duplicates, convert Reviews/Installs/Size/Price to numeric (handling $, +, M, k), parse Last Updated to date, filter valid Rating and Type, lump rare categories. Print dim() and summary() of the result. Produce in R.

### Part B — Pipe-to-Plot: Three Charts (30 points)
Using your cleaned data, produce three charts each as a single piped chain (no intermediate variables):
1. Sorted horizontal bar of top 8 categories by count
2. Scatter of Reviews (log) vs Rating coloured by Type
3. Pointrange of mean Rating ± 95% CI by Category (top 8)
Produce all three in R.

### Part C — Pivot and Plot (25 points)
Create a wide tibble with 4 regions × 4 quarters of revenue. Pivot to long format. Plot as a line chart with colour = region. Produce in R. Then do the same in Python using pd.melt().

### Part D — Python Equivalent (20 points)
Translate your Part A cleaning pipeline to pandas (using .assign(), .query(), pd.to_numeric(), etc.). Compare code length and readability in 100 words.

### Submission Checklist
- [ ] `W04_M02_homework.R` + `W04_M02_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
