# Workshop 4 · Module 8 — Course Notes
## EDA Case Study: e-Car Loan Pricing

### 1. Dataset Overview
The e-Car dataset contains 208,087 auto loan applications from 2002–2012, with 12 variables: Tier (credit risk bucket 1–5), FICO (credit score 300–850), Approve Date, Term (months), Amount ($), Previous Rate (prior loan rate — 53% missing), Car Type (N=New, U=Used), Competition rate, Outcome (0=declined, 1=approved), Rate (offered interest rate), Cost of Funds (bank's capital cost), and Partner Bin (dealer partnership tier). The derived variable Spread = Rate − Cost of Funds represents the bank's margin on each loan.

### 2. Key Findings
**Finding 1: FICO dominates Rate.** Spearman ρ ≈ −0.65 — the strongest bivariate relationship in the dataset. Higher FICO scores yield lower offered rates. The tier system discretises this continuous relationship into 5 buckets, but within-tier scatter plots reveal residual FICO slopes, meaning the tier system loses information.

**Finding 2: Used cars get higher rates.** Median rate for Used ≈ +1.5 percentage points above New, reflecting a risk premium for depreciation and higher default probability on used vehicles. This effect is consistent across all tiers.

**Finding 3: Spread compressed post-2008.** The bank's margin (Spread) fell from ~4pp in 2002 to ~2pp around 2010, then partially recovered. This reflects macroeconomic forces (Federal Reserve rate changes, competitive pressure) and is invisible in cross-sectional analysis — only the time-series panel (f) reveals it.

**Finding 4: Previous Rate is structurally MNAR.** 53% of rows have no Previous Rate because those customers are new (no prior loan). This is not accidental missingness — the absence itself is informative. The correct action is to encode it as a binary indicator (`is_new_customer`), never to impute.

### 3. Framework Portability
The same seven-section EDA report structure used for Google Play Store applies identically to e-Car: Data Description, Cleaning Audit, Missingness Audit, Univariate EDA, Bivariate EDA, Key Findings, Limitations. The dashboard template (9 panels) transfers directly, with only the variable names and domain context changing. This demonstrates that EDA methodology is domain-agnostic.

### 4. Unique Features of Financial EDA
Large n (208K) enables precise CI estimation but requires sampling for scatter plots. Time dimension (11 years) adds a temporal layer absent in cross-sectional datasets. Domain context is critical: "Spread" is meaningless without understanding Cost of Funds; "Tier" is meaningless without understanding it discretises FICO. Always consult domain experts when exploring unfamiliar data.

### References
- Thomas, L. C. (2009). *Consumer Credit Models*. Oxford.
- Peng, R. (2016). *Exploratory Data Analysis with R*.
