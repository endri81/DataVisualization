"""
============================================================
Workshop 1 — Module 9: Python Environment Setup & Matplotlib Basics
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)

# ── 0. Verify Installation ─────────────────────────────────
print(f"numpy:      {np.__version__}")
print(f"pandas:     {pd.__version__}")
print(f"matplotlib: {plt.matplotlib.__version__}")


# ── 1. Data Types ──────────────────────────────────────────
# float64 (numeric)
x_float = np.array([10.5, 20.3, 30.1])
print(f"\nfloat64: {x_float.dtype}")

# int64 (integer)
x_int = np.array([1, 2, 3])
print(f"int64:   {x_int.dtype}")

# object (string)
x_str = pd.Series(["Alice", "Bob", "Carol"])
print(f"object:  {x_str.dtype}")

# bool (logical)
x_bool = pd.Series([True, False, True])
print(f"bool:    {x_bool.dtype}")

# category (factor)
x_cat = pd.Categorical(["Low", "Med", "High"],
                        categories=["Low", "Med", "High"], ordered=True)
print(f"category:{x_cat.dtype}")

# datetime64
x_date = pd.to_datetime("2024-01-15")
print(f"datetime:{type(x_date).__name__}")


# ── 2. DataFrame Inspection ───────────────────────────────
# Create a small demo DataFrame
df = pd.DataFrame({
    "name":  ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "score": [88, 92, 75, 85, 91],
    "grade": pd.Categorical(["A", "A", "B", "B", "A"]),
    "date":  pd.to_datetime(["2024-01-10", "2024-01-11", "2024-01-12",
                             "2024-01-13", "2024-01-14"]),
})

print(f"\n── DataFrame Inspection ──")
print(f"Shape:   {df.shape}")
print(f"\nTypes:\n{df.dtypes}")
print(f"\nHead:\n{df.head()}")
print(f"\nDescribe:\n{df.describe()}")
print(f"\nMissing: {df.isna().sum().sum()}")


# ── 3. matplotlib OO Pattern: Scatterplot ─────────────────
np.random.seed(22)
x = np.random.uniform(1, 6, 80)
y = 0.5 * x + np.random.normal(0, 0.8, 80)

fig, ax = plt.subplots(figsize=(6, 4.5))

# Plot data
ax.scatter(x, y, s=30, c="#1565C0", alpha=0.6,
           edgecolors="white", linewidth=0.3)

# Add regression line
m, b = np.polyfit(x, y, 1)
xs = np.linspace(1, 6, 50)
ax.plot(xs, m * xs + b, color="#E53935", linewidth=1.5, linestyle="--",
        label=f"OLS: y = {m:.2f}x + {b:.2f}")

# Labels
ax.set_xlabel("Displacement (L)", fontsize=10)
ax.set_ylabel("Highway MPG", fontsize=10)
ax.set_title("Scatterplot with OLS Fit", fontsize=12, fontweight="bold")
ax.legend(fontsize=8, frameon=False)

# Tufte cleanup
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=8)
ax.grid(alpha=0.15)

plt.tight_layout()
fig.savefig("output/scatter.pdf", bbox_inches="tight")
fig.savefig("output/scatter.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 4. Histogram ──────────────────────────────────────────
np.random.seed(33)
data = np.random.normal(50, 15, 500)

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.hist(data, bins=25, color="#1565C0", edgecolor="white",
        linewidth=0.5, alpha=0.8)

# Mean reference line
mean_val = np.mean(data)
ax.axvline(x=mean_val, color="#E53935", linewidth=2, linestyle="--")
ax.text(mean_val + 1, ax.get_ylim()[1] * 0.9,
        f"Mean: {mean_val:.1f}", fontsize=9, color="#E53935", fontweight="bold")

ax.set_xlabel("Value", fontsize=10)
ax.set_ylabel("Frequency", fontsize=10)
ax.set_title("Histogram with Mean Reference", fontsize=12, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("output/histogram.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 5. Horizontal Bar Chart ──────────────────────────────
cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
vals = [47, 41, 62, 33, 11]

# Sort ascending for barh
idx = np.argsort(vals)
s_cats = [cats[i] for i in idx]
s_vals = [vals[i] for i in idx]

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.barh(s_cats, s_vals, color="#1565C0", height=0.55, edgecolor="none")

# Direct labels
for i, v in enumerate(s_vals):
    ax.text(v + 0.8, i, str(v), va="center", fontsize=9,
            fontweight="bold", color="#333")

ax.set_xlabel("Count", fontsize=10)
ax.set_title("Vehicle Count by Class (Sorted)", fontsize=12, fontweight="bold")

# Full Tufte cleanup
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.set_xticks([])
ax.tick_params(left=False, labelsize=9)

plt.tight_layout()
fig.savefig("output/bar_chart.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 6. Boxplot ────────────────────────────────────────────
np.random.seed(44)
group_a = np.random.normal(50, 10, 80)
group_b = np.random.normal(55, 15, 80)
group_c = np.random.normal(45, 8, 80)

fig, ax = plt.subplots(figsize=(6, 4.5))

bp = ax.boxplot([group_a, group_b, group_c],
                labels=["Group A", "Group B", "Group C"],
                patch_artist=True, widths=0.5, notch=True)

# Customise colours
fills = ["#E3F2FD", "#E8F5E9", "#FFF3E0"]
edges = ["#1565C0", "#2E7D32", "#E65100"]
for patch, fc, ec in zip(bp["boxes"], fills, edges):
    patch.set_facecolor(fc)
    patch.set_edgecolor(ec)
    patch.set_linewidth(1.5)
for median in bp["medians"]:
    median.set_color("#C62828")
    median.set_linewidth(2)

# Overlay mean points
means = [np.mean(d) for d in [group_a, group_b, group_c]]
ax.scatter(range(1, 4), means, c="#E53935", s=50, zorder=5,
           marker="D", edgecolors="white")

ax.set_ylabel("Value", fontsize=10)
ax.set_title("Grouped Boxplot with Notch and Means", fontsize=12, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("output/boxplot.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 7. Multi-Panel: plt.subplots(2, 2) ───────────────────
np.random.seed(55)

fig, axes = plt.subplots(2, 2, figsize=(8, 6))

# (a) Scatter
axes[0, 0].scatter(np.random.uniform(1, 10, 50),
                   np.random.uniform(1, 10, 50),
                   s=20, c="#1565C0", alpha=0.6, edgecolors="white", linewidth=0.3)
axes[0, 0].set_title("(a) Scatter", fontsize=9, fontweight="bold")

# (b) Histogram
axes[0, 1].hist(np.random.normal(50, 12, 300), bins=20, color="#2E7D32",
                edgecolor="white", linewidth=0.3)
axes[0, 1].set_title("(b) Histogram", fontsize=9, fontweight="bold")

# (c) Bar
axes[1, 0].barh(["A", "B", "C", "D"], [34, 52, 28, 45],
                color="#E65100", height=0.5, edgecolor="none")
axes[1, 0].set_title("(c) Bar Chart", fontsize=9, fontweight="bold")

# (d) Boxplot
bp = axes[1, 1].boxplot([np.random.normal(50, 10, 60),
                         np.random.normal(55, 15, 60)],
                        labels=["G1", "G2"], patch_artist=True, widths=0.4)
for patch in bp["boxes"]:
    patch.set_facecolor("#E3F2FD")
    patch.set_edgecolor("#1565C0")
axes[1, 1].set_title("(d) Boxplot", fontsize=9, fontweight="bold")

# Tufte cleanup on all panels
for ax in axes.flatten():
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.suptitle("Four-Panel Layout: plt.subplots(2, 2)", fontsize=11, fontweight="bold")
plt.tight_layout()
fig.savefig("output/multipanel.png", dpi=300, bbox_inches="tight")
fig.savefig("output/multipanel.pdf", bbox_inches="tight")
plt.close()


# ── 8. Method Chaining Preview (pandas) ──────────────────
# Equivalent to R's pipe |>

result = (
    df
    .query("score >= 80")          # filter
    .assign(bonus=lambda d: d["score"] * 0.1)  # mutate
    .sort_values("score", ascending=False)      # arrange
    .reset_index(drop=True)
)

print(f"\n── Method Chaining Result ──")
print(result)


print("\n── All M09 plots saved to output/ ──")
