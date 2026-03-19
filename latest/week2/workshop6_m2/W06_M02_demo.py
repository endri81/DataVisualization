"""W06-M02: Line Charts — Theory & Best Practices — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter, MonthLocator
os.makedirs("output", exist_ok=True); np.random.seed(42)

# Simulated 3-product revenue series
months = pd.date_range("2020-01", "2023-12", freq="ME")
n = len(months)
prod_a = 100 * np.cumprod(1 + np.random.normal(0.005, 0.03, n))
prod_b = 500 * np.cumprod(1 + np.random.normal(0.003, 0.04, n))
prod_c = 50  * np.cumprod(1 + np.random.normal(0.008, 0.02, n))

# 1. ASPECT RATIO COMPARISON
fig, axes = plt.subplots(1, 3, figsize=(14, 3))
for ax, ratio, title, color in zip(axes,
    [(14,2),(7,3),(4,5)],
    ["Too wide: trend exaggerated", "Banked to ~45: optimal", "Too tall: noise exaggerated"],
    ["#C62828", "#1565C0", "#E65100"]):
    ax.plot(months, prod_a, color=color, lw=1.5)
    ax.set_title(title, fontsize=9, fontweight="bold", color=color)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=5); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Aspect Ratio: Banking to 45 degrees (Cleveland, 1988)", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/aspect_ratio.png", dpi=300); plt.close()

# 2. DUAL Y-AXIS: BAD vs GOOD
temp = 20 + 10 * np.sin(2 * np.pi * np.arange(n) / 12) + np.random.normal(0, 1, n)
sales = 50000 + 20000 * np.sin(2 * np.pi * np.arange(n) / 12 + 0.5) + np.random.normal(0, 3000, n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
# BAD: dual axes
ax1.plot(months, temp, color="#E53935", lw=1.5, label="Temperature")
ax1b = ax1.twinx()
ax1b.plot(months, sales, color="#1565C0", lw=1.5, label="Sales")
ax1.set_ylabel("Temp (C)", color="#E53935"); ax1b.set_ylabel("Sales (EUR)", color="#1565C0")
ax1.set_title("BAD: Dual Y-Axes\n(correlation implied by shared space)", fontsize=9, fontweight="bold", color="#C62828")
ax1.tick_params(labelsize=5); ax1b.tick_params(labelsize=5)
# GOOD: separate
ax2.plot(months, temp, color="#E53935", lw=1.5)
ax2.set_title("GOOD: Separate panel (or index to 100)", fontsize=9, fontweight="bold", color="#1565C0")
ax2.set_ylabel("Temp (C)"); ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
fig.suptitle("The Dual Y-Axis Debate", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/dual_axes.png", dpi=300); plt.close()

# 3. INDEXED LINES
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
for name, vals, c in [("A", prod_a, "#1565C0"), ("B", prod_b, "#E53935"), ("C", prod_c, "#2E7D32")]:
    ax1.plot(months, vals, color=c, lw=1.5, label=name)
    ax2.plot(months, vals / vals[0] * 100, color=c, lw=1.5, label=name)
ax1.legend(fontsize=7); ax1.set_title("Raw: B dominates visually", fontweight="bold")
ax2.legend(fontsize=7); ax2.set_title("Indexed to 100: C outperforms", fontweight="bold")
ax2.axhline(y=100, color="#888", lw=0.5, ls=":")
for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Indexing: Normalise Start Values for Fair Comparison", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/indexed.png", dpi=300); plt.close()

# 4. GREY + ACCENT
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
for name, vals, c in [("A", prod_a, "#1565C0"), ("B", prod_b, "#E53935"), ("C", prod_c, "#2E7D32")]:
    ax1.plot(months, vals, color=c, lw=1.5, label=name)
ax1.legend(fontsize=7); ax1.set_title("All coloured: which is the story?", fontweight="bold", color="#C62828")
# Grey+accent
for name, vals in [("A", prod_a), ("B", prod_b), ("C", prod_c)]:
    ax2.plot(months, vals, color="#DDDDDD", lw=0.8)
ax2.plot(months, prod_c, color="#E53935", lw=2.5)
ax2.text(months[-1], prod_c[-1], " C (best)", fontsize=8, fontweight="bold", color="#E53935", va="center")
ax2.set_title("Grey+accent: story is clear", fontweight="bold", color="#1565C0")
for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Grey + Accent: Highlight the Story", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/grey_accent.png", dpi=300); plt.close()

# 5. DIRECT LABELS + EVENT ANNOTATION
fig, ax = plt.subplots(figsize=(10, 5))
idx_a, idx_b, idx_c = prod_a/prod_a[0]*100, prod_b/prod_b[0]*100, prod_c/prod_c[0]*100
for vals in [idx_a, idx_b]:
    ax.plot(months, vals, color="#DDDDDD", lw=0.8)
ax.plot(months, idx_c, color="#E53935", lw=2.5)
# Direct labels at end
for name, vals, c in [("A", idx_a, "#AAAAAA"), ("B", idx_b, "#AAAAAA"), ("C", idx_c, "#E53935")]:
    ax.text(months[-1], vals[-1], f"  {name}", fontsize=8, fontweight="bold", color=c, va="center")
# Event annotation
ax.axvline(x=pd.Timestamp("2020-03-11"), ls="--", color="#888", lw=0.8)
ax.annotate("WHO declares\npandemic", xy=(pd.Timestamp("2020-03-11"), max(idx_c)*0.95),
    xytext=(pd.Timestamp("2020-06-01"), max(idx_c)*0.90),
    fontsize=7, color="#888", arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
ax.axhline(y=100, color="#888", lw=0.5, ls=":")
ax.set_title("Direct Labels + Event Annotation (indexed, grey+accent)", fontweight="bold")
ax.set_ylabel("Index (start = 100)"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
plt.tight_layout(); plt.savefig("output/annotated.png", dpi=300); plt.close()

# 6. LOG SCALE
fig, ax = plt.subplots(figsize=(8, 5))
for name, vals, c in [("A", prod_a, "#1565C0"), ("B", prod_b, "#E53935"), ("C", prod_c, "#2E7D32")]:
    ax.plot(months, vals, color=c, lw=1.5, label=name)
ax.set_yscale("log"); ax.legend(fontsize=7)
ax.set_title("Log Scale: Constant growth = straight line", fontweight="bold")
ax.set_ylabel("Revenue (log)"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("output/log_scale.png", dpi=300); plt.close()

print("\nAll W06-M02 Python outputs saved")
print("Figures: aspect_ratio, dual_axes, indexed, grey_accent, annotated, log_scale")
