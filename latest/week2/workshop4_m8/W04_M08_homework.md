# Workshop 4 · Module 8 — Homework
## EDA Case Study: e-Car Loan Pricing

**Due**: Before Workshop 4, Module 10
**Format**: R script + Python script + PDF report (max 6 pages)
**Weight**: Part of Workshop 4 homework (5% of total grade)

### The Assignment (50 points)

1. **Cleaning & derived variables** (10 points): Clean the e-Car dataset (fix types, derive Spread and is_new_customer). Document an audit trail with row counts.

2. **Six-panel dashboard** (20 points): Build a 2×3 dashboard including: FICO histogram, Rate by Tier (boxplot), FICO vs Rate scatter with trend, Spread over time with CI ribbon, New vs Used violin, and one chart of your choice. Compose with patchwork (R) and GridSpec (Python).

3. **Structural MNAR analysis** (10 points): Produce shadow histograms comparing FICO distributions for "Has Previous Rate" vs "No Previous Rate" groups. In 150 words, explain why this is MNAR and why imputation would be inappropriate.

4. **Three findings** (10 points): Following the Finding → Evidence → Implication format, present three insights from your dashboard. At least one must involve the time dimension (Year).

### Submission Checklist
- [ ] `W04_M08_homework.R` + `W04_M08_homework.py`
- [ ] Dashboard as PDF + PNG (300 dpi)
- [ ] PDF report (max 6 pages)
