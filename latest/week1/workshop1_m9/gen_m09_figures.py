"""
Generate ALL figures for Workshop 1, Module 9
Python Environment Setup & Matplotlib Basics
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m09"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. JUPYTER LAB LAYOUT — wireframe
# ================================================================
def fig_jupyter_layout():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis("off")
    
    panes = [
        (0.02, 0.55, 0.25, 0.38, "File Browser\n\n• Navigate folders\n• Open notebooks\n• Upload files",
         "#E65100", "#FFF3E0"),
        (0.30, 0.55, 0.68, 0.38, "Notebook Editor\n\n• Code cells (Python)\n• Markdown cells (text)\n• Inline plot output\n• Cell-by-cell execution",
         "#1565C0", "#E3F2FD"),
        (0.02, 0.04, 0.46, 0.46, "Terminal / Console\n\n• pip install packages\n• Run .py scripts\n• System commands",
         "#2E7D32", "#E8F5E9"),
        (0.52, 0.04, 0.46, 0.46, "Inspector / Help\n\n• Docstrings on hover\n• Variable inspector\n• Contextual help",
         "#7B1FA2", "#F3E5F5"),
    ]
    
    for x, y, w, h, text, edge, fill in panes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                     facecolor=fill, edgecolor=edge, linewidth=2))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=7.5, color="#333", linespacing=1.5)
    
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1)
    ax.set_title("JupyterLab IDE: Notebook-Centric Workflow", fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/jupyter_layout.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. PYTHON DATA SCIENCE STACK — package map
# ================================================================
def fig_python_stack():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis("off")
    
    packages = [
        (0.5, 0.88, "Python Data Science Stack", "", "#1A237E", 12),
        (0.10, 0.62, "numpy", "N-dim arrays\nlinear algebra", "#1565C0", 9),
        (0.30, 0.62, "pandas", "DataFrames\nread_csv, groupby\nmerge, pivot", "#2E7D32", 9),
        (0.50, 0.62, "matplotlib", "Core plotting\nfig/axes model\nplt.savefig", "#C62828", 9),
        (0.70, 0.62, "seaborn", "Statistical viz\nFacetGrid, lmplot\nheatmap", "#7B1FA2", 9),
        (0.90, 0.62, "scipy", "Statistics\nhypothesis tests", "#E65100", 9),
        (0.10, 0.30, "plotnine", "ggplot2 clone\nfor Python", "#00695C", 9),
        (0.30, 0.30, "plotly", "Interactive\ncharts", "#4E342E", 9),
        (0.50, 0.30, "altair", "Declarative\nviz (Vega-Lite)", "#1565C0", 9),
        (0.70, 0.30, "scikit-learn", "ML models\nPCA, clustering", "#2E7D32", 9),
        (0.90, 0.30, "statsmodels", "Regression\ntime series", "#E65100", 9),
    ]
    
    for cx, cy, name, desc, color, fs in packages:
        w = 0.16 if cy > 0.8 else 0.14
        h = 0.08 if cy > 0.8 else 0.22
        ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                     edgecolor=color, linewidth=1.5))
        ax.text(cx, cy + (0.01 if cy > 0.8 else 0.05), name, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=color)
        if desc:
            ax.text(cx, cy - 0.04, desc, ha="center", va="center",
                    fontsize=5.5, color="#555", linespacing=1.3)
    
    ax.set_xlim(0, 1); ax.set_ylim(0.12, 0.98)
    ax.set_title("The Python Data Science Ecosystem", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig(f"{OUT}/python_stack.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. MATPLOTLIB ARCHITECTURE: Figure → Axes → Artists
# ================================================================
def fig_mpl_architecture():
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.axis("off")
    
    layers = [
        (0.5, 0.82, 0.7, 0.12, "Figure",
         "The entire canvas: fig = plt.figure() or plt.subplots()\nControls size, dpi, background, suptitle",
         "#1565C0", "#E3F2FD"),
        (0.5, 0.58, 0.55, 0.12, "Axes",
         "One plot area: ax = fig.add_subplot()\nHolds data, title, labels, ticks, spines",
         "#2E7D32", "#E8F5E9"),
        (0.5, 0.34, 0.40, 0.12, "Artists",
         "Every visible element: Line2D, Patch, Text\nCreated by ax.plot(), ax.bar(), ax.scatter()",
         "#E65100", "#FFF3E0"),
    ]
    
    for cx, cy, w, h, title, desc, edge, fill in layers:
        ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                     boxstyle="round,pad=0.02", facecolor=fill, edgecolor=edge, linewidth=2))
        ax.text(cx, cy + 0.025, title, ha="center", va="center",
                fontsize=12, fontweight="bold", color=edge)
        ax.text(cx, cy - 0.03, desc, ha="center", va="center",
                fontsize=7, color="#555", linespacing=1.4)
    
    for y1, y2 in [(0.75, 0.65), (0.51, 0.41)]:
        ax.annotate("", xy=(0.5, y2), xytext=(0.5, y1),
                    arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))
    
    # Sidebar: two APIs
    ax.add_patch(FancyBboxPatch((0.78, 0.2), 0.20, 0.55,
                 boxstyle="round,pad=0.02", facecolor="#FCE4EC", edgecolor="#C62828", linewidth=1.5))
    ax.text(0.88, 0.62, "Two APIs", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#C62828")
    ax.text(0.88, 0.48, "pyplot\n(plt.plot())\nMATLAB-style\nquick & implicit", ha="center", va="center",
            fontsize=7, color="#C62828", linespacing=1.3)
    ax.text(0.88, 0.30, "Object-Oriented\n(ax.plot())\nExplicit control\nrecommended", ha="center", va="center",
            fontsize=7, color="#1565C0", linespacing=1.3, fontweight="bold")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.12, 0.95)
    ax.set_title("Matplotlib Architecture: Figure → Axes → Artists",
                 fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_architecture.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. pyplot vs OO — side by side
# ================================================================
def fig_pyplot_vs_oo():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 60)
    y = 0.5 * x + np.random.normal(0, 0.8, 60)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # pyplot style (implicit state machine)
    ax1.scatter(x, y, s=25, c="black")
    ax1.set_xlabel("x"); ax1.set_ylabel("y")
    ax1.set_title("pyplot API\nplt.scatter(x, y)\nImplicit, MATLAB-style",
                  fontsize=9, fontweight="bold")
    for sp in ax1.spines.values(): sp.set_linewidth(1)
    ax1.tick_params(labelsize=7)
    
    # OO style (explicit axes)
    colors = np.where(y > np.median(y), "#E53935", "#1565C0")
    ax2.scatter(x, y, s=35, c=colors, alpha=0.7, edgecolors="white", linewidth=0.3)
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(1, 6, 50)
    ax2.plot(xs, m*xs + b, color="#888", linewidth=1, linestyle="--")
    ax2.set_xlabel("Displacement (L)", fontsize=9)
    ax2.set_ylabel("MPG", fontsize=9)
    ax2.set_title("Object-Oriented API\nfig, ax = plt.subplots()\nExplicit, recommended",
                  fontsize=9, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_facecolor("#FAFAFA")
    ax2.grid(True, alpha=0.2)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("pyplot vs Object-Oriented: Same Library, Two Paradigms",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/pyplot_vs_oo.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. SCATTER — matplotlib
# ================================================================
def fig_mpl_scatter():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 80)
    y = 0.5 * x + np.random.normal(0, 0.8, 80)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(x, y, s=30, c="#1565C0", alpha=0.6, edgecolors="white", linewidth=0.3)
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(1, 6, 50)
    ax.plot(xs, m*xs + b, color="#E53935", linewidth=1.5, linestyle="--")
    ax.set_xlabel("Displacement (L)", fontsize=9)
    ax.set_ylabel("MPG", fontsize=9)
    ax.set_title("ax.scatter() + ax.plot()", fontsize=10, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_scatter.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. HISTOGRAM — matplotlib
# ================================================================
def fig_mpl_hist():
    np.random.seed(33)
    data = np.random.normal(50, 15, 500)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(data, bins=25, color="#1565C0", edgecolor="white", linewidth=0.5, alpha=0.8)
    ax.axvline(x=np.mean(data), color="#E53935", linewidth=2, linestyle="--")
    ax.text(np.mean(data) + 1, ax.get_ylim()[1] * 0.9,
            f"Mean: {np.mean(data):.1f}", fontsize=8, color="#E53935", fontweight="bold")
    ax.set_xlabel("Value", fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.set_title("ax.hist() + ax.axvline()", fontsize=10, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_hist.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. BAR CHART — matplotlib
# ================================================================
def fig_mpl_bar():
    cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
    vals = [47, 41, 62, 33, 11]
    idx = np.argsort(vals)
    s_c = [cats[i] for i in idx]
    s_v = [vals[i] for i in idx]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.barh(s_c, s_v, color="#1565C0", height=0.55, edgecolor="none")
    for i, v in enumerate(s_v):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=9, fontweight="bold", color="#333")
    ax.set_xlabel("Count", fontsize=9)
    ax.set_title("ax.barh() + direct labels", fontsize=10, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_bar.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. BOXPLOT — matplotlib
# ================================================================
def fig_mpl_box():
    np.random.seed(44)
    data = [np.random.normal(50, 10, 80), np.random.normal(55, 15, 80),
            np.random.normal(45, 8, 80)]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    bp = ax.boxplot(data, labels=["Group A", "Group B", "Group C"],
                    patch_artist=True, widths=0.5, notch=True)
    colors_box = ["#E3F2FD", "#E8F5E9", "#FFF3E0"]
    edges = ["#1565C0", "#2E7D32", "#E65100"]
    for patch, fc, ec in zip(bp["boxes"], colors_box, edges):
        patch.set_facecolor(fc)
        patch.set_edgecolor(ec)
        patch.set_linewidth(1.5)
    for median in bp["medians"]:
        median.set_color("#C62828")
        median.set_linewidth(2)
    
    # Mean points
    means = [np.mean(d) for d in data]
    ax.scatter(range(1, 4), means, c="#E53935", s=50, zorder=5, marker="D", edgecolors="white")
    
    ax.set_ylabel("Value", fontsize=9)
    ax.set_title("ax.boxplot(patch_artist=True, notch=True)", fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_box.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. SUBPLOTS — 2x2 grid
# ================================================================
def fig_mpl_subplots():
    np.random.seed(55)
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    
    # Scatter
    x = np.random.uniform(1, 10, 50)
    y = 0.5 * x + np.random.normal(0, 1.5, 50)
    axes[0,0].scatter(x, y, s=20, c="#1565C0", alpha=0.6, edgecolors="white", linewidth=0.3)
    axes[0,0].set_title("(a) ax.scatter()", fontsize=8, fontweight="bold")
    
    # Histogram
    axes[0,1].hist(np.random.normal(50, 12, 300), bins=20, color="#2E7D32",
                   edgecolor="white", linewidth=0.3)
    axes[0,1].set_title("(b) ax.hist()", fontsize=8, fontweight="bold")
    
    # Bar
    axes[1,0].barh(["A","B","C","D"], [34,52,28,45], color="#E65100", height=0.5, edgecolor="none")
    axes[1,0].set_title("(c) ax.barh()", fontsize=8, fontweight="bold")
    
    # Box
    bp = axes[1,1].boxplot([np.random.normal(50, 10, 60), np.random.normal(55, 15, 60)],
                           labels=["G1", "G2"], patch_artist=True, widths=0.4)
    for patch in bp["boxes"]:
        patch.set_facecolor("#E3F2FD")
        patch.set_edgecolor("#1565C0")
    axes[1,1].set_title("(d) ax.boxplot()", fontsize=8, fontweight="bold")
    
    for ax in axes.flatten():
        ax.tick_params(labelsize=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    
    fig.suptitle("plt.subplots(2, 2): Four-Panel Layout", fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpl_subplots.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. PANDAS DATA TYPES — visual card
# ================================================================
def fig_pandas_types():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    
    types = [
        ("float64", "42.5, 3.14, NaN", "Continuous measurements", "#1565C0"),
        ("int64", "1, 42, -3", "Whole numbers (integers)", "#2E7D32"),
        ("object", '"hello", "NYC"', "Strings (text)", "#E65100"),
        ("bool", "True, False", "Boolean flags", "#7B1FA2"),
        ("category", 'pd.Categorical([...])', "Categorical (ordered/unordered)", "#C62828"),
        ("datetime64", 'pd.to_datetime("2024-01-15")', "Timestamps", "#00695C"),
    ]
    
    for i, (name, example, desc, color) in enumerate(types):
        y = 0.88 - i * 0.14
        ax.add_patch(FancyBboxPatch((0.02, y - 0.04), 0.14, 0.08,
                     boxstyle="round,pad=0.01", facecolor=color, edgecolor="none", alpha=0.85))
        ax.text(0.09, y, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", fontfamily="monospace")
        ax.text(0.20, y + 0.01, example, va="center", fontsize=8.5,
                fontfamily="monospace", color="#333")
        ax.text(0.20, y - 0.03, desc, va="center", fontsize=7.5, color="#777")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.05, 1)
    ax.set_title("pandas Data Types for Visualization", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/pandas_types.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
if __name__ == "__main__":
    funcs = [
        ("jupyter_layout", fig_jupyter_layout),
        ("python_stack", fig_python_stack),
        ("mpl_architecture", fig_mpl_architecture),
        ("pyplot_vs_oo", fig_pyplot_vs_oo),
        ("mpl_scatter", fig_mpl_scatter),
        ("mpl_hist", fig_mpl_hist),
        ("mpl_bar", fig_mpl_bar),
        ("mpl_box", fig_mpl_box),
        ("mpl_subplots", fig_mpl_subplots),
        ("pandas_types", fig_pandas_types),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M09 figures saved to {OUT}/")
