"""
Generate ALL figures for Workshop 1, Module 8
R Environment Setup & Base Graphics
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m08"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. RSTUDIO PANE LAYOUT — wireframe
# ================================================================
def fig_rstudio_layout():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis("off")
    
    # Four panes
    panes = [
        (0.02, 0.5, 0.46, 0.42, "Source Editor\n\n• Write .R scripts\n• Syntax highlighting\n• Code completion",
         "#1565C0", "#E3F2FD"),
        (0.52, 0.5, 0.46, 0.42, "Environment / History\n\n• Objects in memory\n• Data frames, vectors\n• Command history",
         "#2E7D32", "#E8F5E9"),
        (0.02, 0.04, 0.46, 0.42, "Console\n\n• Execute R commands\n• See output / errors\n• Interactive REPL",
         "#E65100", "#FFF3E0"),
        (0.52, 0.04, 0.46, 0.42, "Files / Plots / Help\n\n• File browser\n• Plot viewer\n• Documentation",
         "#7B1FA2", "#F3E5F5"),
    ]
    
    for x, y, w, h, text, edge, fill in panes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                     facecolor=fill, edgecolor=edge, linewidth=2))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=8, color="#333", linespacing=1.5)
    
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1)
    ax.set_title("RStudio IDE: Four-Pane Layout", fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/rstudio_layout.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. TIDYVERSE ECOSYSTEM — package map
# ================================================================
def fig_tidyverse_ecosystem():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axis("off")
    
    packages = [
        (0.5, 0.85, "tidyverse", "Meta-package: loads all below", "#1A237E", 12),
        (0.12, 0.58, "readr", "Read CSV/TSV", "#1565C0", 9),
        (0.32, 0.58, "dplyr", "Data wrangling\nfilter, mutate,\nsummarise", "#2E7D32", 9),
        (0.52, 0.58, "tidyr", "Reshape\npivot_longer,\npivot_wider", "#E65100", 9),
        (0.72, 0.58, "ggplot2", "Visualization\nGrammar of\nGraphics", "#C62828", 9),
        (0.90, 0.58, "stringr", "String ops", "#7B1FA2", 9),
        (0.12, 0.28, "forcats", "Factor levels", "#00695C", 9),
        (0.32, 0.28, "lubridate", "Date/time", "#4E342E", 9),
        (0.52, 0.28, "purrr", "Functional\nprogramming", "#1565C0", 9),
        (0.72, 0.28, "tibble", "Modern\ndata frames", "#E65100", 9),
        (0.90, 0.28, "readxl", "Read Excel", "#2E7D32", 9),
    ]
    
    for cx, cy, name, desc, color, fs in packages:
        w = 0.16 if cy > 0.7 else 0.14
        h = 0.1 if cy > 0.7 else 0.2
        ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                     edgecolor=color, linewidth=1.5))
        ax.text(cx, cy + (0.02 if cy > 0.7 else 0.04), name, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=color)
        if cy < 0.7:
            ax.text(cx, cy - 0.04, desc, ha="center", va="center",
                    fontsize=6, color="#555", linespacing=1.3)
    
    # Arrows from tidyverse to each package
    for cx, cy, *_ in packages[1:]:
        ax.annotate("", xy=(cx, cy + 0.1 if cy > 0.4 else cy + 0.1),
                    xytext=(0.5, 0.79),
                    arrowprops=dict(arrowstyle="->", color="#AAA", lw=0.8,
                                   connectionstyle="arc3,rad=0.0"))
    
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 0.98)
    ax.set_title("The tidyverse Ecosystem", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig(f"{OUT}/tidyverse_ecosystem.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. BASE R plot() — scatter
# ================================================================
def fig_base_scatter():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 80)
    y = 0.5 * x + np.random.normal(0, 0.8, 80)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(x, y, s=30, c="black", marker="o", edgecolors="none")
    ax.set_xlabel("Displacement (L)", fontsize=10)
    ax.set_ylabel("Highway MPG", fontsize=10)
    ax.set_title("Base R: plot(x, y)", fontsize=10, fontstyle="italic")
    ax.tick_params(labelsize=8)
    # Simulate base R look: box around plot
    for sp in ax.spines.values():
        sp.set_linewidth(1)
    ax.grid(False)
    plt.tight_layout()
    fig.savefig(f"{OUT}/base_scatter.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. BASE R hist() — histogram
# ================================================================
def fig_base_hist():
    np.random.seed(33)
    data = np.random.normal(50, 15, 500)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(data, bins=20, color="lightblue", edgecolor="black", linewidth=0.8)
    ax.set_xlabel("Value", fontsize=10)
    ax.set_ylabel("Frequency", fontsize=10)
    ax.set_title("Base R: hist(x)", fontsize=10, fontstyle="italic")
    ax.tick_params(labelsize=8)
    for sp in ax.spines.values():
        sp.set_linewidth(1)
    ax.grid(False)
    plt.tight_layout()
    fig.savefig(f"{OUT}/base_hist.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. BASE R barplot() — bar chart
# ================================================================
def fig_base_bar():
    cats = ["A", "B", "C", "D", "E"]
    vals = [34, 52, 28, 45, 38]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(cats, vals, color=["grey"]*5, edgecolor="black", linewidth=0.8, width=0.6)
    ax.set_ylabel("Count", fontsize=10)
    ax.set_title("Base R: barplot(vals)", fontsize=10, fontstyle="italic")
    ax.tick_params(labelsize=8)
    for sp in ax.spines.values():
        sp.set_linewidth(1)
    ax.grid(False)
    plt.tight_layout()
    fig.savefig(f"{OUT}/base_bar.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. BASE R boxplot() — box plot
# ================================================================
def fig_base_box():
    np.random.seed(44)
    data = [np.random.normal(50, 10, 80), np.random.normal(55, 15, 80),
            np.random.normal(45, 8, 80)]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    bp = ax.boxplot(data, labels=["Group A", "Group B", "Group C"],
                    patch_artist=True, widths=0.5)
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")
        patch.set_edgecolor("black")
    ax.set_ylabel("Value", fontsize=10)
    ax.set_title("Base R: boxplot(x ~ group)", fontsize=10, fontstyle="italic")
    ax.tick_params(labelsize=8)
    for sp in ax.spines.values():
        sp.set_linewidth(1)
    ax.grid(False)
    plt.tight_layout()
    fig.savefig(f"{OUT}/base_box.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. par() SYSTEM — multi-panel with par(mfrow)
# ================================================================
def fig_par_system():
    np.random.seed(55)
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    
    # Scatter
    x = np.random.uniform(1, 10, 50)
    y = 0.5 * x + np.random.normal(0, 1.5, 50)
    axes[0,0].scatter(x, y, s=20, c="black")
    axes[0,0].set_title("plot(x, y)", fontsize=9, fontstyle="italic")
    
    # Histogram
    axes[0,1].hist(np.random.normal(50, 12, 300), bins=15, color="lightblue", edgecolor="black")
    axes[0,1].set_title("hist(x)", fontsize=9, fontstyle="italic")
    
    # Bar
    axes[1,0].bar(["A","B","C","D"], [34,52,28,45], color="grey", edgecolor="black", width=0.5)
    axes[1,0].set_title("barplot(vals)", fontsize=9, fontstyle="italic")
    
    # Box
    bp = axes[1,1].boxplot([np.random.normal(50, 10, 60), np.random.normal(55, 15, 60)],
                           labels=["G1", "G2"], patch_artist=True, widths=0.4)
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")
    axes[1,1].set_title("boxplot(x ~ g)", fontsize=9, fontstyle="italic")
    
    for ax in axes.flatten():
        ax.tick_params(labelsize=6)
        for sp in ax.spines.values():
            sp.set_linewidth(0.8)
    
    fig.suptitle("Base R: par(mfrow = c(2, 2)) — Four-Panel Layout",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/par_system.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. BASE R → ggplot2 COMPARISON
# ================================================================
def fig_base_vs_ggplot():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 80)
    y = 0.5 * x + np.random.normal(0, 0.8, 80)
    cats = np.random.choice(["A", "B", "C"], 80)
    palette = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Base R style
    ax1.scatter(x, y, s=25, c="black", marker="o")
    ax1.set_xlabel("x", fontsize=9)
    ax1.set_ylabel("y", fontsize=9)
    ax1.set_title("Base R: plot(x, y)\nDefault styling, no layers",
                  fontsize=9, fontweight="bold")
    for sp in ax1.spines.values():
        sp.set_linewidth(1)
    ax1.tick_params(labelsize=7)
    
    # ggplot2 style
    for c in ["A", "B", "C"]:
        mask = cats == c
        ax2.scatter(x[mask], y[mask], s=35, c=palette[c], alpha=0.7,
                   edgecolors="white", linewidth=0.3, label=c)
    m, b = np.polyfit(x, y, 1)
    xs_line = np.linspace(1, 6, 50)
    ax2.plot(xs_line, m*xs_line + b, color="#888", linewidth=1, linestyle="--")
    ax2.legend(fontsize=7, title="Group", title_fontsize=8)
    ax2.set_xlabel("Displacement (L)", fontsize=9)
    ax2.set_ylabel("Highway MPG", fontsize=9)
    ax2.set_title("ggplot2: aes(color = group) + geom_smooth()\nLayered grammar, themed",
                  fontsize=9, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_facecolor("#FAFAFA")
    ax2.grid(True, alpha=0.2)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Base R vs ggplot2: Same Data, Different Paradigms",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/base_vs_ggplot.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. PIPE OPERATOR — workflow diagram
# ================================================================
def fig_pipe_workflow():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis("off")
    
    steps = [
        ("data", "Start with\ndata frame", "#888888"),
        ("|>", "", "#333333"),
        ("filter()", "Keep rows\nmatching condition", "#1565C0"),
        ("|>", "", "#333333"),
        ("mutate()", "Add/transform\ncolumns", "#2E7D32"),
        ("|>", "", "#333333"),
        ("group_by()", "Set grouping\nvariable", "#E65100"),
        ("|>", "", "#333333"),
        ("summarise()", "Compute\naggregates", "#7B1FA2"),
        ("|>", "", "#333333"),
        ("ggplot()", "Visualize\nresult", "#C62828"),
    ]
    
    x = 0.02
    for label, desc, color in steps:
        if label == "|>":
            ax.text(x + 0.01, 0.5, "|>", ha="center", va="center",
                    fontsize=14, fontweight="bold", color="#888", fontfamily="monospace")
            x += 0.04
        else:
            w = 0.11
            ax.add_patch(FancyBboxPatch((x, 0.25), w, 0.5,
                         boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                         edgecolor=color, linewidth=1.5))
            ax.text(x + w/2, 0.6, label, ha="center", va="center",
                    fontsize=8, fontweight="bold", color=color, fontfamily="monospace")
            ax.text(x + w/2, 0.38, desc, ha="center", va="center",
                    fontsize=6, color="#555", linespacing=1.3)
            x += w + 0.005
    
    ax.set_xlim(-0.01, 1.01); ax.set_ylim(0.05, 0.95)
    ax.set_title("The Pipe Operator |> : Left-to-Right Data Flow",
                 fontsize=12, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/pipe_workflow.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. DATA TYPES in R — visual card
# ================================================================
def fig_data_types():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    
    types = [
        ("numeric", "42.5, 3.14, -7", "Continuous measurements", "#1565C0"),
        ("integer", "1L, 42L, -3L", "Whole numbers (suffix L)", "#2E7D32"),
        ("character", '"hello", "NYC"', "Text strings", "#E65100"),
        ("logical", "TRUE, FALSE, NA", "Boolean flags", "#7B1FA2"),
        ("factor", 'factor(c("A","B"))', "Categorical (ordered/unordered)", "#C62828"),
        ("Date", 'as.Date("2024-01-15")', "Calendar dates", "#00695C"),
    ]
    
    for i, (name, example, desc, color) in enumerate(types):
        y = 0.88 - i * 0.14
        # Name badge
        ax.add_patch(FancyBboxPatch((0.02, y - 0.04), 0.14, 0.08,
                     boxstyle="round,pad=0.01", facecolor=color, edgecolor="none", alpha=0.85))
        ax.text(0.09, y, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", fontfamily="monospace")
        # Example
        ax.text(0.20, y + 0.01, example, va="center", fontsize=9,
                fontfamily="monospace", color="#333")
        # Description
        ax.text(0.20, y - 0.03, desc, va="center", fontsize=7.5, color="#777")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.05, 1)
    ax.set_title("R Data Types for Visualization",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/data_types.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
if __name__ == "__main__":
    funcs = [
        ("rstudio_layout", fig_rstudio_layout),
        ("tidyverse_ecosystem", fig_tidyverse_ecosystem),
        ("base_scatter", fig_base_scatter),
        ("base_hist", fig_base_hist),
        ("base_bar", fig_base_bar),
        ("base_box", fig_base_box),
        ("par_system", fig_par_system),
        ("base_vs_ggplot", fig_base_vs_ggplot),
        ("pipe_workflow", fig_pipe_workflow),
        ("data_types", fig_data_types),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M08 figures saved to {OUT}/")
