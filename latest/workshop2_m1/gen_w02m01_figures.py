"""
Generate ALL figures for Workshop 2, Module 1
Wilkinson's Grammar of Graphics: Theory
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_w02m01"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. THE SEVEN LAYERS — stacked diagram
# ================================================================
def fig_seven_layers():
    fig, ax = plt.subplots(figsize=(8, 6.5))
    ax.axis("off")
    
    layers = [
        ("7. THEME",        "Fonts, backgrounds, gridlines, legends",     "#90CAF9", "#1565C0"),
        ("6. COORDINATES",  "Cartesian, polar, map projections",          "#A5D6A7", "#2E7D32"),
        ("5. FACETS",       "Split data into panels (small multiples)",   "#FFCC80", "#E65100"),
        ("4. STATISTICS",   "Bins, smoothers, counts, summaries",         "#CE93D8", "#7B1FA2"),
        ("3. SCALES",       "Map data values → visual properties",        "#EF9A9A", "#C62828"),
        ("2. GEOMETRIES",   "Points, lines, bars, areas, polygons",       "#80CBC4", "#00695C"),
        ("1. DATA + AESTHETICS", "Variables → visual channels (x, y, color, size)", "#FFF59D", "#F57F17"),
    ]
    
    for i, (name, desc, fill, edge) in enumerate(layers):
        y = 0.90 - i * 0.12
        w = 0.75 - i * 0.02  # progressively narrower = pyramid
        x = (1 - w) / 2
        h = 0.09
        ax.add_patch(FancyBboxPatch((x, y - h/2), w, h,
                     boxstyle="round,pad=0.02", facecolor=fill, edgecolor=edge, linewidth=2))
        ax.text(x + w/2, y + 0.01, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color=edge)
        ax.text(x + w/2, y - 0.025, desc, ha="center", va="center",
                fontsize=7, color="#444")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.05, 1)
    ax.set_title("The Seven Layers of the Grammar of Graphics",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/seven_layers.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. TRADITIONAL vs GRAMMAR approach
# ================================================================
def fig_traditional_vs_grammar():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    
    # Left: Traditional (chart catalogue)
    ax1.axis("off")
    chart_types = [
        ("Bar Chart", 0.2, 0.78),
        ("Pie Chart", 0.5, 0.78),
        ("Line Chart", 0.8, 0.78),
        ("Scatter Plot", 0.2, 0.50),
        ("Histogram", 0.5, 0.50),
        ("Box Plot", 0.8, 0.50),
        ("Area Chart", 0.2, 0.22),
        ("Bubble Chart", 0.5, 0.22),
        ("Heatmap", 0.8, 0.22),
    ]
    for name, x, y in chart_types:
        ax1.add_patch(FancyBboxPatch((x-0.12, y-0.08), 0.24, 0.16,
                     boxstyle="round,pad=0.02", facecolor="#FFEBEE", edgecolor="#C62828", linewidth=1.5))
        ax1.text(x, y, name, ha="center", va="center", fontsize=8, fontweight="bold", color="#C62828")
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_title("Traditional: Memorise Chart Types\n(finite catalogue, rigid)",
                  fontsize=10, fontweight="bold", color="#C62828")
    
    # Right: Grammar (composable components)
    ax2.axis("off")
    components = [
        ("DATA", 0.5, 0.85, "#F57F17"),
        ("AESTHETICS", 0.5, 0.70, "#E65100"),
        ("GEOMETRIES", 0.5, 0.55, "#00695C"),
        ("SCALES", 0.5, 0.40, "#C62828"),
        ("FACETS", 0.5, 0.25, "#7B1FA2"),
        ("THEME", 0.5, 0.10, "#1565C0"),
    ]
    for name, x, y, color in components:
        ax2.add_patch(FancyBboxPatch((x-0.18, y-0.05), 0.36, 0.10,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                     edgecolor=color, linewidth=2))
        ax2.text(x, y, name, ha="center", va="center", fontsize=9, fontweight="bold", color=color)
    # Plus signs between layers
    for y in [0.775, 0.625, 0.475, 0.325, 0.175]:
        ax2.text(0.5, y, "+", ha="center", va="center", fontsize=14, fontweight="bold", color="#888")
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.set_title("Grammar: Compose Layers\n(infinite combinations, flexible)",
                  fontsize=10, fontweight="bold", color="#1565C0")
    
    fig.suptitle("Chart Catalogue vs Grammar of Graphics", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/traditional_vs_grammar.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. ALGEBRA OF GRAPHICS — data × aesthetics × geometry
# ================================================================
def fig_algebra():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")
    
    # Three boxes with × operators
    boxes = [
        (0.15, 0.5, "DATA\n\ndf with columns:\nx, y, group, size", "#F57F17"),
        (0.50, 0.5, "AESTHETICS\n\nx → position\ny → position\ngroup → color\nsize → size", "#E65100"),
        (0.85, 0.5, "GEOMETRY\n\ngeom_point()\ngeom_line()\ngeom_bar()", "#00695C"),
    ]
    
    for cx, cy, text, color in boxes:
        ax.add_patch(FancyBboxPatch((cx-0.14, cy-0.3), 0.28, 0.6,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.1,
                     edgecolor=color, linewidth=2))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=8,
                color=color, linespacing=1.5)
    
    # × operators
    ax.text(0.325, 0.5, "×", ha="center", va="center", fontsize=24, fontweight="bold", color="#333")
    ax.text(0.675, 0.5, "×", ha="center", va="center", fontsize=24, fontweight="bold", color="#333")
    
    # = result
    ax.text(0.5, 0.02, "= A unique, well-specified visualization",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#333", fontstyle="italic")
    
    ax.set_xlim(0, 1); ax.set_ylim(-0.1, 0.95)
    ax.set_title("The Algebra: Data × Aesthetics × Geometry = Chart",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig(f"{OUT}/algebra.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. SAME DATA, DIFFERENT GEOM — three chart types from one mapping
# ================================================================
def fig_same_data_diff_geom():
    np.random.seed(22)
    x = np.arange(1, 8)
    y = [23, 45, 31, 58, 40, 52, 35]
    cats = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # geom_col (bar)
    axes[0].bar(cats, y, color="#1565C0", width=0.55, edgecolor="none")
    axes[0].set_title("geom_col()\n(bars)", fontsize=10, fontweight="bold", color="#1565C0")
    axes[0].spines["top"].set_visible(False); axes[0].spines["right"].set_visible(False)
    axes[0].tick_params(labelsize=7)
    
    # geom_line (line)
    axes[1].plot(cats, y, "o-", color="#2E7D32", linewidth=2, markersize=6)
    axes[1].set_title("geom_line()\n(connected points)", fontsize=10, fontweight="bold", color="#2E7D32")
    axes[1].spines["top"].set_visible(False); axes[1].spines["right"].set_visible(False)
    axes[1].tick_params(labelsize=7)
    
    # geom_point (scatter)
    axes[2].scatter(cats, y, s=80, c="#E53935", edgecolors="white", linewidth=0.5, zorder=5)
    axes[2].set_title("geom_point()\n(dot plot)", fontsize=10, fontweight="bold", color="#E53935")
    axes[2].spines["top"].set_visible(False); axes[2].spines["right"].set_visible(False)
    axes[2].tick_params(labelsize=7)
    
    fig.suptitle("Same Data + Same Aesthetics, Different Geometry\naes(x = day, y = sales)",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/same_data_diff_geom.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. SAME DATA, DIFFERENT AESTHETIC — color vs facet
# ================================================================
def fig_same_data_diff_aes():
    np.random.seed(33)
    n = 150
    x = np.random.uniform(10, 100, n)
    y = 0.4 * x + np.random.normal(0, 12, n)
    group = np.random.choice(["A", "B", "C"], n)
    palette = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Color aesthetic
    for g, c in palette.items():
        mask = group == g
        ax1.scatter(x[mask], y[mask], s=25, c=c, alpha=0.6, edgecolors="none", label=g)
    ax1.legend(fontsize=7, title="Group")
    ax1.set_title("aes(color = group)\nOne panel, colour encodes group",
                  fontsize=9, fontweight="bold")
    ax1.set_xlabel("x"); ax1.set_ylabel("y")
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelsize=7)
    
    # Facet aesthetic (simulated as 1×3 subpanels)
    ax2.axis("off")
    ax2.set_title("facet_wrap(~group)\nThree panels, proximity encodes group",
                  fontsize=9, fontweight="bold")
    inner_gs = GridSpec(1, 3, left=0.55, right=0.98, bottom=0.15, top=0.75,
                        wspace=0.3, figure=fig)
    for i, g in enumerate(["A", "B", "C"]):
        ax_f = fig.add_subplot(inner_gs[0, i])
        mask = group == g
        ax_f.scatter(x[mask], y[mask], s=15, c="#1565C0", alpha=0.5, edgecolors="none")
        ax_f.set_title(f"Group {g}", fontsize=7, fontweight="bold")
        ax_f.tick_params(labelsize=5)
        ax_f.spines["top"].set_visible(False); ax_f.spines["right"].set_visible(False)
    
    fig.suptitle("Same Data + Same Geom, Different Aesthetic Strategy",
                 fontsize=12, fontweight="bold")
    fig.savefig(f"{OUT}/same_data_diff_aes.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. LAYERING — building up a plot step by step
# ================================================================
def fig_layering():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 60)
    y = 0.5 * x + np.random.normal(0, 0.8, 60)
    
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    titles = ["Layer 1: Data + Axes", "Layer 2: + geom_point()", 
              "Layer 3: + geom_smooth()", "Layer 4: + labs() + theme()"]
    
    # Layer 1: empty axes
    axes[0].set_xlim(0, 7); axes[0].set_ylim(-1, 5)
    axes[0].set_xlabel("x"); axes[0].set_ylabel("y")
    axes[0].set_title(titles[0], fontsize=8, fontweight="bold")
    axes[0].tick_params(labelsize=6)
    
    # Layer 2: + points
    axes[1].scatter(x, y, s=20, c="#1565C0", alpha=0.5, edgecolors="none")
    axes[1].set_xlim(0, 7); axes[1].set_ylim(-1, 5)
    axes[1].set_xlabel("x"); axes[1].set_ylabel("y")
    axes[1].set_title(titles[1], fontsize=8, fontweight="bold")
    axes[1].tick_params(labelsize=6)
    
    # Layer 3: + smooth
    axes[2].scatter(x, y, s=20, c="#1565C0", alpha=0.5, edgecolors="none")
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(1, 6, 50)
    axes[2].plot(xs, m*xs + b, color="#E53935", linewidth=2)
    axes[2].fill_between(xs, m*xs + b - 0.8, m*xs + b + 0.8, alpha=0.1, color="#E53935")
    axes[2].set_xlim(0, 7); axes[2].set_ylim(-1, 5)
    axes[2].set_xlabel("x"); axes[2].set_ylabel("y")
    axes[2].set_title(titles[2], fontsize=8, fontweight="bold")
    axes[2].tick_params(labelsize=6)
    
    # Layer 4: + theme
    axes[3].scatter(x, y, s=20, c="#1565C0", alpha=0.5, edgecolors="white", linewidth=0.3)
    axes[3].plot(xs, m*xs + b, color="#E53935", linewidth=2)
    axes[3].fill_between(xs, m*xs + b - 0.8, m*xs + b + 0.8, alpha=0.1, color="#E53935")
    axes[3].set_xlim(0, 7); axes[3].set_ylim(-1, 5)
    axes[3].set_xlabel("Displacement (L)", fontsize=8)
    axes[3].set_ylabel("Highway MPG", fontsize=8)
    axes[3].set_title(titles[3], fontsize=8, fontweight="bold")
    axes[3].spines["top"].set_visible(False); axes[3].spines["right"].set_visible(False)
    axes[3].set_facecolor("#FAFAFA")
    axes[3].grid(alpha=0.15)
    axes[3].tick_params(labelsize=6)
    
    fig.suptitle("Layered Construction: Each + Adds a Component",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/layering.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. WILKINSON vs WICKHAM — comparison table card
# ================================================================
def fig_wilkinson_vs_wickham():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axis("off")
    
    rows = [
        ("Published", "1999 (book)", "2010 (JCGS paper)"),
        ("Scope", "General theory\n(any software)", "R implementation\n(ggplot2 package)"),
        ("Layers", "7 theoretical\ncomponents", "7 practical layers\n(+ position adj.)"),
        ("Implementation", "Conceptual\nspecification", "Working R code\nwith + operator"),
        ("Statistics", "Explicit\ntransformation step", "Implicit via\nstat_*() functions"),
        ("Audience", "Researchers,\ntheory", "Practitioners,\napplied"),
    ]
    
    col_x = [0.01, 0.25, 0.62]
    headers = ["Dimension", "Wilkinson (1999)", "Wickham (2010)"]
    header_colors = ["#333", "#C62828", "#1565C0"]
    
    for x, h, hc in zip(col_x, headers, header_colors):
        ax.text(x, 0.95, h, fontsize=10, fontweight="bold", color=hc, va="center")
    ax.axhline(y=0.90, xmin=0.01, xmax=0.99, color="#333", linewidth=1.5)
    
    for i, (dim, wilk, wick) in enumerate(rows):
        y = 0.82 - i * 0.13
        ax.text(col_x[0], y, dim, fontsize=8, fontweight="bold", color="#555", va="center")
        ax.text(col_x[1], y, wilk, fontsize=7.5, color="#C62828", va="center", linespacing=1.3)
        ax.text(col_x[2], y, wick, fontsize=7.5, color="#1565C0", va="center", linespacing=1.3)
        if i < len(rows) - 1:
            ax.axhline(y=y - 0.065, xmin=0.01, xmax=0.99, color="#E0E0E0", linewidth=0.5)
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Wilkinson (1999) vs Wickham (2010): Theory → Implementation",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/wilkinson_vs_wickham.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. SPECIFICATION → CHART — pipeline diagram
# ================================================================
def fig_specification_pipeline():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axis("off")
    
    steps = [
        ("Data\nVariables", "#F57F17"),
        ("→", "#888"),
        ("Algebra\n(cross, nest,\nblend)", "#E65100"),
        ("→", "#888"),
        ("Scales\n(position,\ncolor, size)", "#C62828"),
        ("→", "#888"),
        ("Statistics\n(bin, smooth,\naggregate)", "#7B1FA2"),
        ("→", "#888"),
        ("Geometry\n(point, line,\nbar, area)", "#00695C"),
        ("→", "#888"),
        ("Coordinates\n(cartesian,\npolar, map)", "#2E7D32"),
        ("→", "#888"),
        ("Aesthetics\n(render to\nscreen/PDF)", "#1565C0"),
    ]
    
    x = 0.01
    for label, color in steps:
        if label == "→":
            ax.text(x + 0.01, 0.5, "→", ha="center", va="center",
                    fontsize=16, color="#888", fontweight="bold")
            x += 0.03
        else:
            w = 0.105
            ax.add_patch(FancyBboxPatch((x, 0.2), w, 0.6,
                         boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                         edgecolor=color, linewidth=1.5))
            ax.text(x + w/2, 0.5, label, ha="center", va="center",
                    fontsize=6.5, fontweight="bold", color=color, linespacing=1.3)
            x += w + 0.003
    
    ax.set_xlim(-0.01, 1.01); ax.set_ylim(0.05, 0.95)
    ax.set_title("Wilkinson's Specification Pipeline: From Variables to Rendered Chart",
                 fontsize=11, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/specification_pipeline.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. R ggplot2 — layer-by-layer build
# ================================================================
def fig_r_layered():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 60)
    y = 0.5 * x + np.random.normal(0, 0.8, 60)
    cats = np.random.choice(["A", "B", "C"], 60)
    palette = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
    
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    for c in ["A", "B", "C"]:
        mask = cats == c
        ax.scatter(x[mask], y[mask], s=35, c=palette[c], alpha=0.65,
                   edgecolors="white", linewidth=0.4, label=c)
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(1, 6, 50)
    ax.plot(xs, m*xs + b, color="#888", linewidth=1.2, linestyle="--")
    ax.set_xlabel("Displacement (L)", fontsize=9)
    ax.set_ylabel("Highway MPG", fontsize=9)
    ax.set_title("ggplot2: aes() + geom_point() + geom_smooth() + theme_minimal()",
                 fontsize=8, fontstyle="italic")
    ax.legend(fontsize=7, title="Class", title_fontsize=8, frameon=True)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.set_facecolor("#FAFAFA"); ax.grid(alpha=0.15)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/r_layered.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. Python plotnine — same grammar
# ================================================================
def fig_py_plotnine():
    np.random.seed(22)
    x = np.random.uniform(1, 6, 60)
    y = 0.5 * x + np.random.normal(0, 0.8, 60)
    cats = np.random.choice(["A", "B", "C"], 60)
    palette = {"A": "#1f77b4", "B": "#d62728", "C": "#2ca02c"}
    
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    for c in ["A", "B", "C"]:
        mask = cats == c
        ax.scatter(x[mask], y[mask], s=35, c=palette[c], alpha=0.65,
                   edgecolors="white", linewidth=0.4, label=c)
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(1, 6, 50)
    ax.plot(xs, m*xs + b, color="#888", linewidth=1.2, linestyle="--")
    ax.set_xlabel("Displacement", fontsize=9)
    ax.set_ylabel("MPG", fontsize=9)
    ax.set_title("plotnine: ggplot(df, aes()) + geom_point() + geom_smooth()",
                 fontsize=8, fontstyle="italic")
    ax.legend(fontsize=7, title="Class", title_fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.15)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/py_plotnine.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
if __name__ == "__main__":
    funcs = [
        ("seven_layers", fig_seven_layers),
        ("traditional_vs_grammar", fig_traditional_vs_grammar),
        ("algebra", fig_algebra),
        ("same_data_diff_geom", fig_same_data_diff_geom),
        ("same_data_diff_aes", fig_same_data_diff_aes),
        ("layering", fig_layering),
        ("wilkinson_vs_wickham", fig_wilkinson_vs_wickham),
        ("specification_pipeline", fig_specification_pipeline),
        ("r_layered", fig_r_layered),
        ("py_plotnine", fig_py_plotnine),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll W02-M01 figures saved to {OUT}/")
