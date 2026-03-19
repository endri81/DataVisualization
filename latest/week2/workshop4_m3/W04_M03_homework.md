# Workshop 4 · Module 3 — Homework
## Data Wrangling for Visualization (Python)

**Due**: Before Workshop 4, Module 5
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### Part A — Full Cleaning Chain (25 points)
Translate the R cleaning pipeline (from W04-M02) into a single parenthesised pandas chain. Use .assign(), .query(), pd.to_numeric(), str.replace(), pd.to_datetime(). Print .shape and .describe() of the result. Compare the chain length to R in 100 words.

### Part B — Chain-to-Plot: Three Charts (30 points)
Using your cleaned DataFrame, produce three charts each as a single chained expression:
1. Sorted horizontal bar of top 8 categories by count (.value_counts().nlargest().plot.barh())
2. Scatter of Reviews (log) vs Rating coloured by Type
3. Pointrange of mean Rating ± 95% CI by Category (top 8)

### Part C — Melt and Plot (25 points)
Create a wide DataFrame with 4 Albanian cities × 4 quarters of revenue. Use pd.melt() to reshape to long. Plot as a line chart. Then use .pivot_table() to reshape back to wide and display. Compare melt/pivot_table to R's pivot_longer/pivot_wider in 100 words.

### Part D — Explode (20 points)
Using the Netflix dataset, split the listed_in column by ", " and .explode() to one row per genre. Produce a sorted horizontal bar of the top 10 genres. Produce in Python. Show the equivalent R code using separate_rows().

### Submission Checklist
- [ ] `W04_M03_homework.R` + `W04_M03_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
