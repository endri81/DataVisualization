"""
Generate ALL figures for Workshop 1, Module 10
Comparative Lab: First Plots in R vs Python
Using Google Play Store data structure
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m10"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)

# ── Simulate Google Play Store data ────────────────────────
categories = ["GAME","FAMILY","TOOLS","BUSINESS","MEDICAL","PRODUCTIVITY",
              "PERSONALIZATION","COMMUNICATION","SPORTS","SOCIAL"]
cat_counts = [959, 1832, 843, 420, 395, 374, 376, 342, 325, 259]
# Simulated ratings per category
np.random.seed(42)


# ================================================================
# 1. BAR CHART — R-style (ggplot2 look)
# ================================================================
def fig_bar_r():
    idx = np.argsort(cat_counts)
    s_cats = [categories[i] for i in idx]
    s_vals = [cat_counts[i] for i in idx]
    
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.barh(s_cats, s_vals, color="#1565C0", height=0.6, edgecolor="none")
    for i, v in enumerate(s_vals):
        ax.text(v + 15, i, f"{v:,}", va="center", fontsize=7, fontweight="bold", color="#333")
    ax.set_xlabel("Count", fontsize=9)
    ax.set_title("Top 10 Categories (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="x", alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/bar_r.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. BAR CHART — Python-style (matplotlib)
# ================================================================
def fig_bar_py():
    idx = np.argsort(cat_counts)
    s_cats = [categories[i] for i in idx]
    s_vals = [cat_counts[i] for i in idx]
    
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.barh(s_cats, s_vals, color="#2E7D32", height=0.6, edgecolor="none")
    for i, v in enumerate(s_vals):
        ax.text(v + 15, i, f"{v:,}", va="center", fontsize=7, fontweight="bold", color="#333")
    ax.set_xlabel("Count", fontsize=9)
    ax.set_title("Top 10 Categories (matplotlib style)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/bar_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. HISTOGRAM — R-style
# ================================================================
def fig_hist_r():
    np.random.seed(55)
    ratings = np.concatenate([
        np.random.normal(4.1, 0.5, 6000),
        np.random.normal(3.0, 0.8, 1500),
        np.random.uniform(1, 5, 500)
    ]).clip(1, 5)
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.hist(ratings, bins=40, color="#1565C0", edgecolor="white", linewidth=0.5, alpha=0.85)
    mean_r = np.mean(ratings)
    ax.axvline(x=mean_r, color="#E53935", linewidth=2, linestyle="--")
    ax.text(mean_r - 0.35, ax.get_ylim()[1]*0.92, f"Mean: {mean_r:.2f}",
            fontsize=8, color="#E53935", fontweight="bold")
    ax.set_xlabel("Rating", fontsize=9)
    ax.set_ylabel("Count", fontsize=9)
    ax.set_title("Rating Distribution (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/hist_r.pdf", bbox_inches="tight")
    plt.close()
    return ratings


# ================================================================
# 4. HISTOGRAM — Python-style
# ================================================================
def fig_hist_py(ratings):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.hist(ratings, bins=40, color="#2E7D32", edgecolor="white", linewidth=0.5, alpha=0.85)
    mean_r = np.mean(ratings)
    ax.axvline(x=mean_r, color="#E53935", linewidth=2, linestyle="--")
    ax.text(mean_r + 0.08, ax.get_ylim()[1]*0.92, f"Mean: {mean_r:.2f}",
            fontsize=8, color="#E53935", fontweight="bold")
    ax.set_xlabel("Rating", fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.set_title("Rating Distribution (matplotlib style)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/hist_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. SCATTER — R-style
# ================================================================
def fig_scatter_r():
    np.random.seed(77)
    n = 500
    reviews = 10 ** np.random.uniform(1, 6, n)
    rating = 3.5 + 0.15 * np.log10(reviews) + np.random.normal(0, 0.6, n)
    rating = np.clip(rating, 1, 5)
    app_type = np.random.choice(["Free", "Paid"], n, p=[0.92, 0.08])
    
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    for t, c in [("Free", "#1565C0"), ("Paid", "#E53935")]:
        mask = app_type == t
        ax.scatter(reviews[mask], rating[mask], s=12, c=c, alpha=0.4,
                   edgecolors="none", label=t)
    ax.set_xscale("log")
    ax.set_xlabel("Reviews (log scale)", fontsize=9)
    ax.set_ylabel("Rating", fontsize=9)
    ax.set_title("Reviews vs Rating (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, title="Type", title_fontsize=8, frameon=True)
    ax.set_facecolor("#FAFAFA")
    ax.grid(alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/scatter_r.pdf", bbox_inches="tight")
    plt.close()
    return reviews, rating, app_type


# ================================================================
# 6. SCATTER — Python-style
# ================================================================
def fig_scatter_py(reviews, rating, app_type):
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    palette = {"Free": "#2E7D32", "Paid": "#E53935"}
    for t, c in palette.items():
        mask = app_type == t
        ax.scatter(reviews[mask], rating[mask], s=12, c=c, alpha=0.4,
                   edgecolors="none", label=t)
    ax.set_xscale("log")
    ax.set_xlabel("Reviews (log scale)", fontsize=9)
    ax.set_ylabel("Rating", fontsize=9)
    ax.set_title("Reviews vs Rating (seaborn/matplotlib style)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, title="Type", title_fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/scatter_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. BOXPLOT — R-style
# ================================================================
def fig_box_r():
    np.random.seed(88)
    free_r = np.random.normal(4.15, 0.55, 800).clip(1, 5)
    paid_r = np.random.normal(4.25, 0.45, 200).clip(1, 5)
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    bp = ax.boxplot([free_r, paid_r], labels=["Free", "Paid"],
                    patch_artist=True, widths=0.45, notch=True)
    bp["boxes"][0].set_facecolor("#BBDEFB")
    bp["boxes"][0].set_edgecolor("#1565C0")
    bp["boxes"][1].set_facecolor("#FFCDD2")
    bp["boxes"][1].set_edgecolor("#E53935")
    for med in bp["medians"]:
        med.set_color("#333"); med.set_linewidth(2)
    means = [np.mean(free_r), np.mean(paid_r)]
    ax.scatter([1, 2], means, c="#E53935", s=50, zorder=5, marker="D", edgecolors="white")
    ax.set_ylabel("Rating", fontsize=9)
    ax.set_title("Rating by Type (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/box_r.pdf", bbox_inches="tight")
    plt.close()
    return free_r, paid_r


# ================================================================
# 8. BOXPLOT — Python-style
# ================================================================
def fig_box_py(free_r, paid_r):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    bp = ax.boxplot([free_r, paid_r], labels=["Free", "Paid"],
                    patch_artist=True, widths=0.45, notch=True)
    bp["boxes"][0].set_facecolor("#C8E6C9")
    bp["boxes"][0].set_edgecolor("#2E7D32")
    bp["boxes"][1].set_facecolor("#FFCDD2")
    bp["boxes"][1].set_edgecolor("#E53935")
    for med in bp["medians"]:
        med.set_color("#333"); med.set_linewidth(2)
    means = [np.mean(free_r), np.mean(paid_r)]
    ax.scatter([1, 2], means, c="#E53935", s=50, zorder=5, marker="D", edgecolors="white")
    ax.set_ylabel("Rating", fontsize=9)
    ax.set_title("Rating by Type (matplotlib style)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/box_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. LINE CHART — R-style (content added per year)
# ================================================================
def fig_line_r():
    years = np.arange(2010, 2019)
    movies = [80, 120, 200, 350, 500, 700, 900, 1100, 1300]
    shows = [30, 50, 80, 130, 200, 300, 450, 600, 700]
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.plot(years, movies, "o-", color="#1565C0", linewidth=2, markersize=5, label="Free")
    ax.plot(years, shows, "s-", color="#E53935", linewidth=2, markersize=5, label="Paid")
    ax.text(2018.2, movies[-1], "Free", fontsize=8, fontweight="bold", color="#1565C0", va="center")
    ax.text(2018.2, shows[-1], "Paid", fontsize=8, fontweight="bold", color="#E53935", va="center")
    ax.set_xlim(2009.5, 2019.5)
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("App Count", fontsize=9)
    ax.set_title("Apps Added per Year (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.set_facecolor("#FAFAFA")
    ax.grid(alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/line_r.pdf", bbox_inches="tight")
    plt.close()
    return years, movies, shows


# ================================================================
# 10. LINE CHART — Python-style
# ================================================================
def fig_line_py(years, movies, shows):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.plot(years, movies, "o-", color="#2E7D32", linewidth=2, markersize=5)
    ax.plot(years, shows, "s-", color="#E53935", linewidth=2, markersize=5)
    ax.text(2018.2, movies[-1], "Free", fontsize=8, fontweight="bold", color="#2E7D32", va="center")
    ax.text(2018.2, shows[-1], "Paid", fontsize=8, fontweight="bold", color="#E53935", va="center")
    ax.set_xlim(2009.5, 2019.5)
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("App Count", fontsize=9)
    ax.set_title("Apps Added per Year (matplotlib style)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/line_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 11. STACKED BAR — R-style (Content Rating × Type)
# ================================================================
def fig_stacked_r():
    cr = ["Everyone", "Teen", "Mature 17+", "Everyone 10+"]
    free = [5200, 1100, 400, 800]
    paid = [300, 80, 30, 50]
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    x = np.arange(len(cr))
    ax.bar(x, free, 0.55, label="Free", color="#1565C0", edgecolor="white")
    ax.bar(x, paid, 0.55, bottom=free, label="Paid", color="#E53935", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(cr, fontsize=7)
    ax.set_ylabel("Count", fontsize=9)
    ax.set_title("Content Rating × Type (ggplot2 style)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, frameon=True)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/stacked_r.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 12. STACKED BAR — Python-style
# ================================================================
def fig_stacked_py():
    cr = ["Everyone", "Teen", "Mature 17+", "Everyone 10+"]
    free = [5200, 1100, 400, 800]
    paid = [300, 80, 30, 50]
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    x = np.arange(len(cr))
    ax.bar(x, free, 0.55, label="Free", color="#2E7D32", edgecolor="white")
    ax.bar(x, paid, 0.55, bottom=free, label="Paid", color="#E53935", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(cr, fontsize=7)
    ax.set_ylabel("Count", fontsize=9)
    ax.set_title("Content Rating × Type (matplotlib style)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/stacked_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 13. SYNTAX COMPARISON CARD
# ================================================================
def fig_syntax_card():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    
    rows = [
        ("Load data", 'read_csv("data.csv")', 'pd.read_csv("data.csv")'),
        ("Filter rows", 'filter(df, Type == "Free")', 'df.query("Type == \'Free\'"'),
        ("Count", "count(Category)", 'value_counts("Category")'),
        ("Sort", "arrange(desc(n))", ".sort_values(ascending=False)"),
        ("Bar chart", "geom_col(fill='blue')", "ax.barh(cats, vals, color='blue')"),
        ("Histogram", "geom_histogram(bins=30)", "ax.hist(x, bins=30)"),
        ("Scatter", "geom_point(aes(color=Type))", "ax.scatter(x, y, c=colors)"),
        ("Boxplot", "geom_boxplot(fill=Type)", "ax.boxplot([g1,g2], patch_artist)"),
        ("Line", "geom_line(aes(color=grp))", "ax.plot(x, y, color='blue')"),
        ("Save", 'ggsave("plot.pdf", w=7, h=5)', 'fig.savefig("plot.pdf")'),
    ]
    
    # Headers
    col_x = [0.01, 0.22, 0.60]
    headers = ["Operation", "R (tidyverse + ggplot2)", "Python (pandas + matplotlib)"]
    header_colors = ["#333", "#1565C0", "#2E7D32"]
    for x, h, hc in zip(col_x, headers, header_colors):
        ax.text(x, 0.95, h, fontsize=10, fontweight="bold", color=hc, va="center")
    ax.axhline(y=0.91, xmin=0.01, xmax=0.99, color="#333", linewidth=1.5)
    
    for i, (op, r_code, py_code) in enumerate(rows):
        y = 0.85 - i * 0.085
        ax.text(col_x[0], y, op, fontsize=8, fontweight="bold", color="#555", va="center")
        ax.text(col_x[1], y, r_code, fontsize=7.5, fontfamily="monospace", color="#1565C0", va="center")
        ax.text(col_x[2], y, py_code, fontsize=7.5, fontfamily="monospace", color="#2E7D32", va="center")
        if i < len(rows) - 1:
            ax.axhline(y=y - 0.042, xmin=0.01, xmax=0.99, color="#E0E0E0", linewidth=0.5)
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("R ↔ Python Syntax Comparison: Complete Cheat Sheet",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/syntax_card.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 14. FULL DASHBOARD — 6-panel (simulating final lab output)
# ================================================================
def fig_dashboard():
    np.random.seed(42)
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    # (a) Bar chart
    ax = fig.add_subplot(gs[0, 0])
    idx = np.argsort(cat_counts)[-6:]
    ax.barh([categories[i] for i in idx], [cat_counts[i] for i in idx],
            color="#1565C0", height=0.55, edgecolor="none")
    ax.set_title("(a) Top Categories", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    # (b) Histogram
    ax = fig.add_subplot(gs[0, 1])
    ratings = np.random.normal(4.1, 0.55, 2000).clip(1, 5)
    ax.hist(ratings, bins=30, color="#2E7D32", edgecolor="white", linewidth=0.3)
    ax.axvline(x=np.mean(ratings), color="#E53935", linewidth=1.5, linestyle="--")
    ax.set_title("(b) Rating Distribution", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    # (c) Scatter
    ax = fig.add_subplot(gs[0, 2])
    rev = 10**np.random.uniform(1, 6, 300)
    rat = 3.5 + 0.15*np.log10(rev) + np.random.normal(0, 0.5, 300)
    ax.scatter(rev, rat.clip(1,5), s=8, c="#E65100", alpha=0.4, edgecolors="none")
    ax.set_xscale("log")
    ax.set_title("(c) Reviews vs Rating", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    # (d) Boxplot
    ax = fig.add_subplot(gs[1, 0])
    bp = ax.boxplot([np.random.normal(4.15, 0.55, 500).clip(1,5),
                     np.random.normal(4.25, 0.45, 100).clip(1,5)],
                    labels=["Free", "Paid"], patch_artist=True, widths=0.4)
    bp["boxes"][0].set_facecolor("#BBDEFB"); bp["boxes"][1].set_facecolor("#FFCDD2")
    ax.set_title("(d) Rating by Type", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    # (e) Line chart
    ax = fig.add_subplot(gs[1, 1])
    years = np.arange(2010, 2019)
    ax.plot(years, np.cumsum(np.random.normal(200, 80, 9)) + 500, color="#1565C0", linewidth=1.5)
    ax.set_title("(e) Cumulative Apps", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    # (f) Stacked bar
    ax = fig.add_subplot(gs[1, 2])
    cr = ["Everyone", "Teen", "Mature", "10+"]
    free_v = [52, 11, 4, 8]
    paid_v = [3, 0.8, 0.3, 0.5]
    x = np.arange(len(cr))
    ax.bar(x, free_v, 0.5, label="Free", color="#1565C0", edgecolor="white")
    ax.bar(x, paid_v, 0.5, bottom=free_v, label="Paid", color="#E53935", edgecolor="white")
    ax.set_xticks(x); ax.set_xticklabels(cr, fontsize=5)
    ax.legend(fontsize=5)
    ax.set_title("(f) Content × Type", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    
    fig.suptitle("Google Play Store EDA Dashboard — Workshop 1 Lab Output",
                 fontsize=13, fontweight="bold")
    fig.savefig(f"{OUT}/dashboard.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
if __name__ == "__main__":
    funcs_simple = [
        ("bar_r", fig_bar_r),
        ("bar_py", fig_bar_py),
        ("stacked_r", fig_stacked_r),
        ("stacked_py", fig_stacked_py),
        ("syntax_card", fig_syntax_card),
        ("dashboard", fig_dashboard),
    ]
    
    for name, func in funcs_simple:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    # Functions with return values
    try:
        ratings = fig_hist_r(); print("  ✓ hist_r")
        fig_hist_py(ratings); print("  ✓ hist_py")
    except Exception as e:
        print(f"  ✗ hist: {e}")
    
    try:
        rev, rat, atype = fig_scatter_r(); print("  ✓ scatter_r")
        fig_scatter_py(rev, rat, atype); print("  ✓ scatter_py")
    except Exception as e:
        print(f"  ✗ scatter: {e}")
    
    try:
        fr, pr = fig_box_r(); print("  ✓ box_r")
        fig_box_py(fr, pr); print("  ✓ box_py")
    except Exception as e:
        print(f"  ✗ box: {e}")
    
    try:
        yrs, mov, sh = fig_line_r(); print("  ✓ line_r")
        fig_line_py(yrs, mov, sh); print("  ✓ line_py")
    except Exception as e:
        print(f"  ✗ line: {e}")
    
    print(f"\nAll M10 figures saved to {OUT}/")
