"""
Generate ALL figures for Workshop 1, Module 2
Tufte's Principles of Graphical Excellence
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as ticker
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m02"

np.random.seed(42)

# ================================================================
# 1. DATA-INK RATIO: step-by-step erasure
# ================================================================
def fig_data_ink_steps():
    """4-step progressive removal of non-data ink from a bar chart."""
    cats = ["A", "B", "C", "D", "E"]
    vals = [34, 52, 28, 45, 38]
    
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2))
    titles = ["Step 1: Default", "Step 2: Remove Fill",
              "Step 3: Remove Grid", "Step 4: Tufte Style"]
    
    # Step 1 — default matplotlib
    ax = axes[0]
    ax.bar(cats, vals, color="steelblue", edgecolor="black", linewidth=1)
    ax.set_facecolor("#EEEEEE")
    ax.grid(True, linewidth=0.8, color="white")
    ax.set_title(titles[0], fontsize=8, fontweight="bold")
    ax.tick_params(labelsize=7)
    
    # Step 2 — remove background fill
    ax = axes[1]
    ax.bar(cats, vals, color="steelblue", edgecolor="black", linewidth=0.5)
    ax.grid(True, axis="y", linewidth=0.5, color="#DDDDDD")
    ax.set_title(titles[1], fontsize=8, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    
    # Step 3 — remove gridlines
    ax = axes[2]
    ax.bar(cats, vals, color="steelblue", edgecolor="none")
    ax.set_title(titles[2], fontsize=8, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    for i, v in enumerate(vals):
        ax.text(i, v + 1, str(v), ha="center", fontsize=7)
    ax.tick_params(labelsize=7)
    
    # Step 4 — Tufte style (minimal)
    ax = axes[3]
    ax.barh(range(len(cats)), vals, color="#1565C0", height=0.5, edgecolor="none")
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(cats, fontsize=8)
    ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=8, color="#333")
    ax.set_title(titles[3], fontsize=8, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    
    fig.suptitle("Progressive Data-Ink Maximisation", fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/data_ink_steps.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 2. DATA-INK RATIO FORMULA — visual
# ================================================================
def fig_data_ink_formula():
    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.axis("off")
    
    ax.text(0.5, 0.72,
            "Data-Ink Ratio  =  Ink used to represent data  /  Total ink on graphic",
            ha="center", va="center", fontsize=13, fontweight="bold",
            fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#E3F2FD",
                      edgecolor="#1565C0", linewidth=2))
    
    ax.text(0.5, 0.30,
            "Goal: maximise this ratio towards 1.0\n"
            "\"Erase non-data ink, within reason\" — Tufte (1983)",
            ha="center", va="center", fontsize=10, fontstyle="italic",
            color="#555555")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    fig.savefig(f"{OUT}/data_ink_formula.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 3. CHARTJUNK TAXONOMY
# ================================================================
def fig_chartjunk_3d():
    """3-D pie chart — classic chartjunk."""
    labels = ["Product A", "Product B", "Product C", "Product D"]
    sizes = [35, 30, 20, 15]
    explode = (0.08, 0.05, 0, 0)
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#DDA0DD"]
    
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct="%1.0f%%", shadow=True, startangle=140,
        textprops={"fontsize": 8})
    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title("3-D Pie Chart\n(Chartjunk: shadow, explosion, hard to compare)",
                 fontsize=9, fontweight="bold", color="#C62828")
    plt.tight_layout()
    fig.savefig(f"{OUT}/chartjunk_3d_pie.pdf", bbox_inches="tight")
    plt.close()

def fig_chartjunk_fixed():
    """Clean horizontal bar — chartjunk removed."""
    labels = ["Product A", "Product B", "Product C", "Product D"]
    sizes = [35, 30, 20, 15]
    
    sorted_idx = np.argsort(sizes)
    s_labels = [labels[i] for i in sorted_idx]
    s_sizes = [sizes[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.barh(s_labels, s_sizes, color="#1565C0", height=0.55, edgecolor="none")
    for i, v in enumerate(s_sizes):
        ax.text(v + 0.5, i, f"{v}%", va="center", fontsize=9)
    ax.set_xlabel("Market Share (%)", fontsize=9)
    ax.set_title("Clean Bar Chart\n(Same data, honest encoding)",
                 fontsize=9, fontweight="bold", color="#1565C0")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/chartjunk_fixed.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 4. MOIRE VIBRATION PATTERN
# ================================================================
def fig_moire():
    """Demonstrate moiré vibration patterns vs clean fills."""
    cats = ["A", "B", "C"]
    vals = [40, 55, 35]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    
    # Moiré — hatched bars with tight patterns
    bars = ax1.bar(cats, vals, color="white", edgecolor="black", linewidth=0.5)
    hatches = ["///", "\\\\\\", "xxx"]
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    ax1.set_title("Moiré Vibration\n(visual noise from hatching)", fontsize=9,
                  fontweight="bold", color="#C62828")
    ax1.set_facecolor("#F5F5F5")
    ax1.grid(True, color="gray", linewidth=0.8)
    ax1.tick_params(labelsize=8)
    
    # Clean
    ax2.bar(cats, vals, color=["#1565C0", "#2E7D32", "#E53935"],
            edgecolor="none", width=0.5)
    for i, v in enumerate(vals):
        ax2.text(i, v + 1, str(v), ha="center", fontsize=9)
    ax2.set_title("Clean Alternative\n(distinct colour, no pattern)", fontsize=9,
                  fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_yticks([])
    ax2.tick_params(labelsize=8)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/moire.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 5. LIE FACTOR — detailed example
# ================================================================
def fig_lie_factor_detail():
    """Fuel economy lie-factor example with calculation."""
    years = ["2019", "2020", "2021", "2022"]
    mpg = [24.0, 24.5, 25.2, 25.8]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Misleading — bubble area encoding
    sizes = [(v - 23)**3 * 500 for v in mpg]  # exaggerated
    ax1.scatter(years, [1]*4, s=sizes, c="#E53935", alpha=0.7, edgecolors="white")
    for i, v in enumerate(mpg):
        ax1.text(i, 1.08, f"{v}", ha="center", fontsize=9, fontweight="bold")
    ax1.set_ylim(0.7, 1.3)
    ax1.set_yticks([])
    ax1.set_title("Misleading: Bubble Area\nData Δ = 7.5% → Visual Δ ≈ 150%\nLie Factor ≈ 20",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.tick_params(labelsize=8)
    
    # Honest — bar chart from zero
    ax2.bar(years, mpg, color="#1565C0", width=0.5, edgecolor="white")
    ax2.set_ylim(0, 30)
    ax2.set_ylabel("Average MPG", fontsize=9)
    for i, v in enumerate(mpg):
        ax2.text(i, v + 0.4, f"{v}", ha="center", fontsize=8)
    ax2.set_title("Honest: Bar from Zero\nData Δ = 7.5% → Visual Δ ≈ 7.5%\nLie Factor ≈ 1.0",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=8)
    
    fig.suptitle("Lie Factor = Effect in Graphic / Effect in Data",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/lie_factor_detail.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 6. SMALL MULTIPLES
# ================================================================
def fig_small_multiples():
    """Demonstrate Tufte's small multiples with time-series panels."""
    np.random.seed(7)
    months = np.arange(1, 13)
    regions = ["North", "South", "East", "West", "Central", "Coastal"]
    
    fig, axes = plt.subplots(2, 3, figsize=(10, 5), sharey=True)
    
    for ax, region in zip(axes.flatten(), regions):
        base = np.random.uniform(50, 120)
        trend = np.cumsum(np.random.normal(2, 8, 12)) + base
        ax.plot(months, trend, color="#1565C0", linewidth=1.8)
        ax.fill_between(months, trend, alpha=0.1, color="#1565C0")
        ax.set_title(region, fontsize=9, fontweight="bold")
        ax.set_xticks([1, 6, 12])
        ax.set_xticklabels(["Jan", "Jun", "Dec"], fontsize=6)
        ax.tick_params(labelsize=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.2)
    
    fig.suptitle("Small Multiples: Same Scale, Easy Comparison\n"
                 "\"At the heart of quantitative reasoning is a single question:\n"
                 "Compared to what?\" — Tufte",
                 fontsize=10, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/small_multiples.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 7. SPARKLINES
# ================================================================
def fig_sparklines():
    """Tufte-style sparklines embedded in a table context."""
    np.random.seed(12)
    metrics = ["Revenue", "Users", "Retention", "NPS Score"]
    
    fig, axes = plt.subplots(4, 1, figsize=(5, 4))
    
    for ax, metric in zip(axes, metrics):
        data = np.cumsum(np.random.normal(0.5, 3, 52))
        ax.plot(data, color="#1565C0", linewidth=1.2)
        ax.fill_between(range(len(data)), data, alpha=0.05, color="#1565C0")
        
        # Mark min and max
        ax.plot(np.argmin(data), data.min(), "o", color="#E53935", markersize=4)
        ax.plot(np.argmax(data), data.max(), "o", color="#2E7D32", markersize=4)
        
        # End value
        ax.plot(len(data)-1, data[-1], "o", color="#1565C0", markersize=3)
        
        ax.set_ylabel(metric, fontsize=8, rotation=0, labelpad=55, va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
    
    fig.suptitle("Sparklines: Intense, Simple, Word-Sized Graphics\n"
                 "Red = min, Green = max, Blue = current",
                 fontsize=10, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/sparklines.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 8. DUCK vs DATA (gratuitous decoration)
# ================================================================
def fig_duck_data():
    """Show the 'duck' concept — decoration overpowering data."""
    x = np.arange(5)
    vals = [23, 45, 31, 58, 40]
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))
    
    # Duck — excessive decoration
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A8E6CF", "#DDA0DD"]
    bars = ax1.bar(labels, vals, color=colors, edgecolor="black", linewidth=2, width=0.6)
    # Add fake shadows
    for b in bars:
        shadow = plt.Rectangle((b.get_x()+0.06, 0), b.get_width(), b.get_height(),
                               color="gray", alpha=0.25, zorder=0)
        ax1.add_patch(shadow)
    ax1.set_facecolor("#FFFDE7")
    ax1.grid(True, color="gray", linewidth=1)
    ax1.set_title("The \"Duck\"\nDecoration dominates data",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_ylabel("Sales (K)", fontsize=8)
    ax1.tick_params(labelsize=7)
    
    # Data — clean
    ax2.plot(labels, vals, "o-", color="#1565C0", linewidth=2, markersize=7,
             markerfacecolor="white", markeredgewidth=2)
    for i, v in enumerate(vals):
        ax2.annotate(str(v), (i, v), textcoords="offset points",
                     xytext=(0, 10), ha="center", fontsize=8, fontweight="bold")
    ax2.set_title("The Data\nClean encoding, same information",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.set_ylabel("Sales (K)", fontsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", alpha=0.15)
    ax2.tick_params(labelsize=7)
    ax2.set_ylim(15, 70)
    
    fig.suptitle("Tufte's \"Ducks\": When Decoration Overpowers Data",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/duck_vs_data.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 9. GRAPHICAL INTEGRITY — truncated axis
# ================================================================
def fig_truncated_axis():
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    revenue = [982, 995, 1003, 1010]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))
    
    # Truncated
    ax1.plot(quarters, revenue, "o-", color="#E53935", linewidth=2.5, markersize=8)
    ax1.set_ylim(975, 1015)
    ax1.fill_between(quarters, revenue, 975, alpha=0.15, color="#E53935")
    ax1.set_title("Truncated Y-Axis\n\"Revenue soaring!\"",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_ylabel("Revenue ($M)", fontsize=8)
    ax1.tick_params(labelsize=7)
    ax1.grid(axis="y", alpha=0.3)
    
    # Honest
    ax2.plot(quarters, revenue, "o-", color="#1565C0", linewidth=2.5, markersize=8)
    ax2.set_ylim(0, 1200)
    ax2.fill_between(quarters, revenue, 0, alpha=0.08, color="#1565C0")
    ax2.set_title("Full Y-Axis\n\"Revenue stable\"",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.set_ylabel("Revenue ($M)", fontsize=8)
    ax2.tick_params(labelsize=7)
    ax2.grid(axis="y", alpha=0.3)
    
    fig.suptitle("Graphical Integrity: Baseline Matters",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/truncated_axis.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 10. INTEGRATION OF TEXT & GRAPHICS — annotated scatter
# ================================================================
def fig_annotated_scatter():
    np.random.seed(99)
    n = 50
    spend = np.random.uniform(10, 100, n)
    roi = 0.4 * spend + np.random.normal(0, 12, n)
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.scatter(spend, roi, s=40, c="#1565C0", alpha=0.6, edgecolor="white", linewidth=0.5)
    
    # Regression line
    m, b = np.polyfit(spend, roi, 1)
    xs = np.linspace(5, 105, 100)
    ax.plot(xs, m*xs + b, color="#E53935", linewidth=1.5, linestyle="--")
    
    # Annotations — Tufte-style direct labels
    outlier_idx = roi.argmax()
    ax.annotate(
        f"Top performer\nROI={roi[outlier_idx]:.0f}%",
        xy=(spend[outlier_idx], roi[outlier_idx]),
        xytext=(spend[outlier_idx] - 20, roi[outlier_idx] + 10),
        fontsize=7, fontweight="bold", color="#2E7D32",
        arrowprops=dict(arrowstyle="->", color="#2E7D32", linewidth=1))
    
    low_idx = roi.argmin()
    ax.annotate(
        f"Under-performer\nROI={roi[low_idx]:.0f}%",
        xy=(spend[low_idx], roi[low_idx]),
        xytext=(spend[low_idx] + 15, roi[low_idx] - 8),
        fontsize=7, fontweight="bold", color="#C62828",
        arrowprops=dict(arrowstyle="->", color="#C62828", linewidth=1))
    
    ax.set_xlabel("Marketing Spend ($K)", fontsize=9)
    ax.set_ylabel("ROI (%)", fontsize=9)
    ax.set_title("Integration: Data + Annotation\n\"Words and graphics belong together\" — Tufte",
                 fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/annotated_scatter.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 11. R ggplot2: data-ink reduction demo output
# ================================================================
def fig_r_data_ink():
    """Simulate ggplot2 theme_tufte output."""
    np.random.seed(55)
    cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
    vals = [47, 41, 62, 33, 11]
    
    sorted_idx = np.argsort(vals)[::-1]
    s_cats = [cats[i] for i in sorted_idx]
    s_vals = [vals[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    y = range(len(s_cats))
    ax.barh(y, s_vals, color="#1565C0", height=0.5, edgecolor="none")
    ax.set_yticks(y)
    ax.set_yticklabels(s_cats, fontsize=8)
    for i, v in enumerate(s_vals):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=8, color="#333")
    ax.set_xlabel("Count", fontsize=8)
    ax.set_title("ggplot2 + ggthemes::theme_tufte()", fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_yticks(y)
    ax.tick_params(left=False, labelsize=7)
    ax.grid(axis="x", alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/r_data_ink.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 12. Python matplotlib: Tufte-style output
# ================================================================
def fig_py_data_ink():
    """matplotlib with manual Tufte styling."""
    cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
    vals = [47, 41, 62, 33, 11]
    sorted_idx = np.argsort(vals)[::-1]
    s_cats = [cats[i] for i in sorted_idx]
    s_vals = [vals[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    y = range(len(s_cats))
    ax.barh(y, s_vals, color="#2E7D32", height=0.5, edgecolor="none")
    ax.set_yticks(y)
    ax.set_yticklabels(s_cats, fontsize=8)
    for i, v in enumerate(s_vals):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=8, color="#333")
    ax.set_xlabel("Count", fontsize=8)
    ax.set_title("matplotlib + manual Tufte styling", fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, labelsize=7)
    ax.grid(axis="x", alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/py_data_ink.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 13. RANGE-FRAME (Tufte's axis innovation)
# ================================================================
def fig_range_frame():
    """Show Tufte's range-frame: axis extent = data range only."""
    np.random.seed(22)
    x = np.random.normal(50, 12, 80)
    y = 0.6 * x + np.random.normal(0, 8, 80)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Standard axes
    ax1.scatter(x, y, s=25, c="#888888", alpha=0.6, edgecolors="none")
    ax1.set_title("Standard Axes", fontsize=9, fontweight="bold")
    ax1.set_xlabel("x", fontsize=9)
    ax1.set_ylabel("y", fontsize=9)
    ax1.tick_params(labelsize=7)
    
    # Range-frame
    ax2.scatter(x, y, s=25, c="#1565C0", alpha=0.6, edgecolors="none")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    # Set spine bounds to data range
    ax2.spines["bottom"].set_bounds(x.min(), x.max())
    ax2.spines["left"].set_bounds(y.min(), y.max())
    ax2.set_title("Range-Frame (Tufte)", fontsize=9, fontweight="bold")
    ax2.set_xlabel("x", fontsize=9)
    ax2.set_ylabel("y", fontsize=9)
    ax2.tick_params(labelsize=7)
    # Tick marks only at data range endpoints
    ax2.set_xticks([round(x.min(), 0), round(x.max(), 0)])
    ax2.set_yticks([round(y.min(), 0), round(y.max(), 0)])
    
    fig.suptitle("Range-Frame: Axis Shows Data Range, Not Arbitrary Extent",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/range_frame.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 14. VISUAL SUMMARY — Tufte's 5 principles
# ================================================================
def fig_tufte_summary():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axis("off")
    
    principles = [
        ("1", "Data-Ink Ratio", "Maximise the share of ink\ndevoted to data", "#1565C0"),
        ("2", "Chartjunk", "Eliminate non-data ink\nthat does not inform", "#E53935"),
        ("3", "Lie Factor", "Visual effect must match\nthe data effect", "#2E7D32"),
        ("4", "Small Multiples", "Repeat a design to show\nvariation across categories", "#7B1FA2"),
        ("5", "Integration", "Words, numbers, and graphics\nbelong together", "#E65100"),
    ]
    
    for i, (num, title, desc, color) in enumerate(principles):
        y = 0.88 - i * 0.185
        ax.add_patch(FancyBboxPatch((0.02, y - 0.06), 0.06, 0.12,
                     boxstyle="round,pad=0.01", facecolor=color, edgecolor="none"))
        ax.text(0.05, y, num, ha="center", va="center", fontsize=14,
                fontweight="bold", color="white")
        ax.text(0.12, y + 0.02, title, fontsize=11, fontweight="bold",
                va="center", color="#222")
        ax.text(0.12, y - 0.035, desc, fontsize=8, va="center", color="#555")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Tufte's Five Core Principles", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/tufte_summary.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    
    funcs = [
        ("data_ink_steps", fig_data_ink_steps),
        ("data_ink_formula", fig_data_ink_formula),
        ("chartjunk_3d_pie", fig_chartjunk_3d),
        ("chartjunk_fixed", fig_chartjunk_fixed),
        ("moire", fig_moire),
        ("lie_factor_detail", fig_lie_factor_detail),
        ("small_multiples", fig_small_multiples),
        ("sparklines", fig_sparklines),
        ("duck_vs_data", fig_duck_data),
        ("truncated_axis", fig_truncated_axis),
        ("annotated_scatter", fig_annotated_scatter),
        ("r_data_ink", fig_r_data_ink),
        ("py_data_ink", fig_py_data_ink),
        ("range_frame", fig_range_frame),
        ("tufte_summary", fig_tufte_summary),
    ]
    
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    print(f"\nAll M02 figures saved to {OUT}/")
