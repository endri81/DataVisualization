# Workshop 1 · Module 9 — Homework
## Python Fundamentals

**Due**: Before Workshop 1, Module 10  
**Format**: Python script (.py) or Jupyter notebook (.ipynb) + exported PNG figures  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Environment Verification (10 points)

1. Create a script or notebook called `W01_M09_homework.py`.
2. Print versions of numpy, pandas, matplotlib, and seaborn.
3. Load the Google Play Store dataset: `apps = pd.read_csv("googleplaystore.csv")`
4. Print `apps.shape`, `apps.dtypes`, `apps.info()`, and `apps.isna().sum()`.

---

### Part B — Data Types Audit (20 points)

1. Identify at least two columns where `dtype == object` but the data
   is really numeric (e.g., Reviews, Installs).
2. Convert Reviews to numeric: `pd.to_numeric(apps["Reviews"], errors="coerce")`
3. Clean and convert Installs: strip commas and "+", then convert to int.
4. Convert Last Updated to datetime: `pd.to_datetime(..., format="%B %d, %Y")`
5. Show `apps.dtypes` before and after the fixes.

---

### Part C — Matplotlib OO Charts (50 points)

Using the cleaned dataset from Part B, produce four charts using the
**OO API** (`fig, ax = plt.subplots()`):

1. **Scatterplot**: `ax.scatter(log10_reviews, rating)` with
   `alpha=0.3`, `s=15`, `c="#1565C0"`. Add a LOESS-like smooth using
   `np.polyfit()` degree 2 or `scipy.signal.savgol_filter()`.

2. **Histogram**: `ax.hist(rating, bins=40)` with a vertical mean line
   (`ax.axvline()`) and an annotated mean value label.

3. **Horizontal bar**: Top 10 categories by count. Sort ascending,
   use `ax.barh()`, add direct labels, remove non-data spines.

4. **Boxplot**: `ax.boxplot()` for Rating split by Type (Free vs Paid).
   Use `patch_artist=True`, different fill colours, and overlay means.

Export each as PNG at 300 dpi using `fig.savefig(..., dpi=300, bbox_inches="tight")`.

---

### Part D — Multi-Panel Layout (20 points)

1. Arrange all four charts in a 2x2 figure using
   `fig, axes = plt.subplots(2, 2, figsize=(10, 8))`.
2. Apply Tufte cleanup to all panels (loop over `axes.flatten()`).
3. Add panel labels: "(a)", "(b)", "(c)", "(d)" using
   `ax.text(0.02, 0.95, "(a)", transform=ax.transAxes, ...)`.
4. Export as PDF (vector) and PNG (300 dpi).

---

### Submission Checklist

- [ ] `W01_M09_homework.py` (or `.ipynb`) — complete, commented
- [ ] `scatter.png`, `hist.png`, `bar.png`, `box.png` — individual charts
- [ ] `multipanel.pdf` + `multipanel.png` — 2x2 layout
