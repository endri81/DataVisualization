"""
Generate ALL figures for Workshop 1, Module 6
The Design Process: From Data to Display
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m06"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. CAIRO'S VISUALIZATION WHEEL
# ================================================================
def fig_cairo_wheel():
    """Cairo's two poles: abstraction↔figuration, density↔lightness, etc."""
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    
    dimensions = [
        ("Abstraction\n← → Figuration", 0.7),
        ("Functionality\n← → Decoration", 0.5),
        ("Density\n← → Lightness", 0.8),
        ("Multi-dimensional\n← → Unidimensional", 0.6),
        ("Originality\n← → Familiarity", 0.4),
        ("Novelty\n← → Redundancy", 0.55),
    ]
    
    N = len(dimensions)
    theta = np.linspace(0, 2*np.pi, N, endpoint=False)
    width = 2*np.pi / N * 0.85
    
    values = [d[1] for d in dimensions]
    colors = ["#1565C0", "#2E7D32", "#E53935", "#7B1FA2", "#E65100", "#00695C"]
    
    bars = ax.bar(theta, values, width=width, bottom=0.1,
                  color=colors, alpha=0.7, edgecolor="white", linewidth=1.5)
    
    ax.set_xticks(theta)
    ax.set_xticklabels([d[0] for d in dimensions], fontsize=7, fontweight="bold")
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(["", "", "", ""], fontsize=6)
    ax.set_ylim(0, 1.0)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    ax.set_title("Cairo's Visualization Wheel\n"
                 "Each axis is a continuum of design choices\n"
                 "(The Functional Art, 2012)",
                 fontsize=11, fontweight="bold", pad=25)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/cairo_wheel.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. MUNZNER'S NESTED MODEL
# ================================================================
def fig_munzner_nested():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    
    layers = [
        (0.5, 0.82, 0.85, 0.14, "1. Domain Problem Characterisation",
         "WHO are the users? WHAT questions do they ask?", "#E3F2FD", "#1565C0"),
        (0.5, 0.62, 0.72, 0.14, "2. Data / Task Abstraction",
         "WHAT data types? WHAT tasks (compare, trend, outlier)?", "#E8F5E9", "#2E7D32"),
        (0.5, 0.42, 0.58, 0.14, "3. Visual Encoding / Interaction Idiom",
         "HOW to encode? Marks, channels, layouts, interactions", "#FFF3E0", "#E65100"),
        (0.5, 0.22, 0.44, 0.14, "4. Algorithm Design",
         "Computational efficiency, rendering, scalability", "#FCE4EC", "#C62828"),
    ]
    
    for cx, cy, w, h, title, desc, fill, edge in layers:
        ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                     boxstyle="round,pad=0.02", facecolor=fill,
                     edgecolor=edge, linewidth=2))
        ax.text(cx, cy + 0.02, title, ha="center", va="center",
                fontsize=10, fontweight="bold", color=edge)
        ax.text(cx, cy - 0.035, desc, ha="center", va="center",
                fontsize=7.5, color="#555")
    
    # Arrows between layers
    for y in [0.74, 0.54, 0.34]:
        ax.annotate("", xy=(0.5, y - 0.01), xytext=(0.5, y + 0.01),
                    arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))
    
    # Threat labels
    threats = [
        (0.95, 0.82, "Threat: wrong\nproblem"),
        (0.95, 0.62, "Threat: wrong\nabstraction"),
        (0.95, 0.42, "Threat: ineffective\nencoding"),
        (0.95, 0.22, "Threat: slow\nalgorithm"),
    ]
    for tx, ty, label in threats:
        ax.text(tx, ty, label, ha="right", va="center", fontsize=7,
                color="#C62828", fontstyle="italic")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.08, 0.95)
    ax.set_title("Munzner's Nested Model for Visualization Design (2014)",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/munzner_nested.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. FIVE-STEP DESIGN PROCESS
# ================================================================
def fig_design_process():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axis("off")
    
    steps = [
        ("1\nAcquire", "Get the data\nAPI, CSV, DB", "#1565C0"),
        ("2\nParse", "Structure &\nclean", "#1976D2"),
        ("3\nFilter", "Remove noise,\nfocus scope", "#1E88E5"),
        ("4\nMine", "Find patterns,\ncompute stats", "#42A5F5"),
        ("5\nRepresent", "Map data to\nvisual form", "#E53935"),
    ]
    
    n = len(steps)
    for i, (label, desc, color) in enumerate(steps):
        x = 0.08 + i * 0.18
        # Box
        ax.add_patch(FancyBboxPatch((x, 0.25), 0.14, 0.55,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.15,
                     edgecolor=color, linewidth=2))
        # Circle number
        circle = plt.Circle((x + 0.07, 0.65), 0.04, color=color, zorder=5)
        ax.add_patch(circle)
        ax.text(x + 0.07, 0.65, label.split("\n")[0], ha="center", va="center",
                fontsize=10, fontweight="bold", color="white", zorder=6)
        # Step name
        ax.text(x + 0.07, 0.52, label.split("\n")[1] if "\n" in label else "",
                ha="center", va="center", fontsize=9, fontweight="bold", color=color)
        # Description
        ax.text(x + 0.07, 0.38, desc, ha="center", va="center",
                fontsize=7, color="#555")
        
        # Arrow to next
        if i < n - 1:
            ax.annotate("", xy=(x + 0.155, 0.52), xytext=(x + 0.175, 0.52),
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))
    
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 0.9)
    ax.set_title("The Five-Step Visualization Pipeline",
                 fontsize=12, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/design_process.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. TASK TAXONOMY (Munzner: why, what, how)
# ================================================================
def fig_task_taxonomy():
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.axis("off")
    
    categories = {
        "WHY (Task)": [
            "Discover  — find new patterns",
            "Present   — communicate known findings",
            "Enjoy     — casual browsing / exploration",
        ],
        "WHAT (Data)": [
            "Tables    — rows × columns",
            "Networks  — nodes + edges",
            "Spatial   — geographic / field data",
            "Temporal  — time-indexed sequences",
        ],
        "HOW (Idiom)": [
            "Encode    — marks + channels",
            "Manipulate — select, navigate, arrange",
            "Facet     — juxtapose, partition, layer",
            "Reduce    — aggregate, filter, sample",
        ],
    }
    
    col_colors = {"WHY (Task)": "#1565C0", "WHAT (Data)": "#2E7D32", "HOW (Idiom)": "#E53935"}
    
    for j, (cat, items) in enumerate(categories.items()):
        x = 0.02 + j * 0.34
        ax.add_patch(FancyBboxPatch((x, 0.72), 0.30, 0.15,
                     boxstyle="round,pad=0.02",
                     facecolor=col_colors[cat], edgecolor="none", alpha=0.15))
        ax.text(x + 0.15, 0.795, cat, ha="center", va="center",
                fontsize=11, fontweight="bold", color=col_colors[cat])
        
        for i, item in enumerate(items):
            y = 0.58 - i * 0.13
            ax.text(x + 0.15, y, item, ha="center", va="center",
                    fontsize=8, color="#444")
            ax.add_patch(FancyBboxPatch((x + 0.01, y - 0.045), 0.28, 0.09,
                         boxstyle="round,pad=0.01",
                         facecolor=col_colors[cat], edgecolor="none", alpha=0.05))
    
    ax.set_xlim(0, 1); ax.set_ylim(0.05, 0.95)
    ax.set_title("Munzner's Task Taxonomy: Why × What × How",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/task_taxonomy.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. DATA TYPE → CHART TYPE decision matrix
# ================================================================
def fig_chart_decision():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axis("off")
    
    matrix = [
        ("Comparison", "Bar, Dot, Lollipop", "across categories"),
        ("Distribution", "Histogram, Density, Boxplot", "of a single variable"),
        ("Relationship", "Scatter, Bubble, Hexbin", "between two+ variables"),
        ("Composition", "Stacked Bar, Treemap, Waffle", "parts of a whole"),
        ("Trend", "Line, Area, Sparkline", "change over time"),
        ("Ranking", "Horizontal Bar, Bump, Slope", "ordered categories"),
        ("Spatial", "Choropleth, Point Map, Hexbin", "geographic patterns"),
    ]
    
    colors = ["#1565C0", "#2E7D32", "#E53935", "#7B1FA2", "#E65100", "#00695C", "#5D4037"]
    
    for i, (goal, charts, desc) in enumerate(matrix):
        y = 0.9 - i * 0.12
        # Goal badge
        ax.add_patch(FancyBboxPatch((0.02, y - 0.04), 0.18, 0.08,
                     boxstyle="round,pad=0.01", facecolor=colors[i],
                     edgecolor="none", alpha=0.85))
        ax.text(0.11, y, goal, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white")
        # Charts
        ax.text(0.24, y + 0.01, charts, va="center", fontsize=9,
                fontweight="bold", color="#333")
        ax.text(0.24, y - 0.025, desc, va="center", fontsize=7, color="#777")
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Chart Selection: Match the Analytical Goal to the Visual Form",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/chart_decision.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. AUDIENCE ANALYSIS — three personas
# ================================================================
def fig_audience():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    personas = [
        ("Executive", "Wants: key takeaway\nFormat: 1 chart, annotated\nDetail: minimal\nTime: 10 seconds",
         "#1565C0"),
        ("Analyst", "Wants: explore data\nFormat: interactive dashboard\nDetail: full granularity\nTime: 30 minutes",
         "#2E7D32"),
        ("Public", "Wants: understand the story\nFormat: infographic / article\nDetail: curated highlights\nTime: 2 minutes",
         "#E53935"),
    ]
    
    for ax, (name, desc, color) in zip(axes, personas):
        ax.add_patch(FancyBboxPatch((0.05, 0.1), 0.9, 0.75,
                     boxstyle="round,pad=0.05", facecolor=color, alpha=0.08,
                     edgecolor=color, linewidth=2))
        # Icon circle
        circle = plt.Circle((0.5, 0.72), 0.08, color=color, alpha=0.2)
        ax.add_patch(circle)
        ax.text(0.5, 0.72, name[0], ha="center", va="center",
                fontsize=16, fontweight="bold", color=color)
        ax.text(0.5, 0.55, name, ha="center", va="center",
                fontsize=12, fontweight="bold", color=color)
        ax.text(0.5, 0.32, desc, ha="center", va="center",
                fontsize=8, color="#444", linespacing=1.6)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Know Your Audience: Three Visualization Personas",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/audience.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. ITERATIVE REFINEMENT — sketch → draft → polished
# ================================================================
def fig_iteration():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    np.random.seed(7)
    cats = ["A", "B", "C", "D", "E"]
    vals = [42, 58, 35, 67, 51]
    
    # Stage 1: Sketch (rough, no styling)
    ax = axes[0]
    ax.bar(cats, vals, color="#AAAAAA", edgecolor="black")
    ax.set_title("Stage 1: Sketch\n(quick & rough)", fontsize=9, fontweight="bold")
    ax.tick_params(labelsize=7)
    
    # Stage 2: Draft (some cleanup)
    ax = axes[1]
    ax.barh(cats, vals, color="#64B5F6", height=0.6, edgecolor="none")
    ax.set_title("Stage 2: Draft\n(correct form, basic style)", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    
    # Stage 3: Polished (Tufte-quality)
    ax = axes[2]
    sorted_idx = np.argsort(vals)[::-1]
    s_cats = [cats[i] for i in sorted_idx]
    s_vals = [vals[i] for i in sorted_idx]
    ax.barh(s_cats, s_vals, color="#1565C0", height=0.5, edgecolor="none")
    for i, v in enumerate(s_vals):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=9, fontweight="bold", color="#333")
    ax.set_title("Stage 3: Polished\n(sorted, labelled, Tufte-clean)", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=8)
    
    fig.suptitle("Iterative Refinement: Sketch → Draft → Polished",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/iteration.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. COMPLETE WORKED EXAMPLE: from raw data to final chart
# ================================================================
def fig_worked_example():
    """Show the full pipeline on a small dataset."""
    np.random.seed(33)
    
    fig = plt.figure(figsize=(12, 5))
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(1, 4, figure=fig, wspace=0.35)
    
    # Step 1: Raw data table
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis("off")
    data = [["Q1", 245], ["Q2", 310], ["Q3", 280], ["Q4", 395]]
    table = ax1.table(cellText=data, colLabels=["Quarter", "Revenue"],
                      loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.8)
    for j in range(2):
        table[0, j].set_facecolor("#1565C0")
        table[0, j].set_text_props(color="white", fontweight="bold")
    ax1.set_title("1. Acquire\n(raw data)", fontsize=9, fontweight="bold", color="#1565C0")
    
    # Step 2: Default chart
    ax2 = fig.add_subplot(gs[0, 1])
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    revenues = [245, 310, 280, 395]
    ax2.bar(quarters, revenues, color="#AAAAAA", edgecolor="black")
    ax2.set_title("2. Default Chart\n(unrefined)", fontsize=9, fontweight="bold", color="#888")
    ax2.tick_params(labelsize=7)
    
    # Step 3: Encode (choose chart type)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.bar(quarters, revenues, color="#64B5F6", width=0.5, edgecolor="none")
    ax3.set_ylim(0, 450)
    ax3.set_title("3. Encode\n(correct form)", fontsize=9, fontweight="bold", color="#1976D2")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.tick_params(labelsize=7)
    
    # Step 4: Refine (Tufte-quality)
    ax4 = fig.add_subplot(gs[0, 3])
    colors_bar = ["#1565C0"] * 4
    colors_bar[3] = "#E53935"  # Highlight Q4
    ax4.bar(quarters, revenues, color=colors_bar, width=0.5, edgecolor="none")
    for i, v in enumerate(revenues):
        ax4.text(i, v + 8, f"${v}K", ha="center", fontsize=8, fontweight="bold", color="#333")
    ax4.set_ylim(0, 450)
    ax4.set_title("4. Refine\n(annotated, highlighted)", fontsize=9, fontweight="bold", color="#E53935")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.spines["left"].set_visible(False)
    ax4.set_yticks([])
    ax4.tick_params(labelsize=8)
    ax4.text(3, 360, "Best quarter!", fontsize=7, ha="center",
             color="#E53935", fontstyle="italic")
    
    fig.suptitle("From Data to Display: A Complete Worked Example",
                 fontsize=12, fontweight="bold")
    fig.savefig(f"{OUT}/worked_example.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. R output — iterative theme refinement
# ================================================================
def fig_r_iteration():
    np.random.seed(55)
    cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
    vals = [47, 41, 62, 33, 11]
    sorted_idx = np.argsort(vals)[::-1]
    s_c = [cats[i] for i in sorted_idx]
    s_v = [vals[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.barh(s_c, s_v, color="#1565C0", height=0.5, edgecolor="none")
    # Highlight max
    bars[0].set_color("#E53935")
    for i, v in enumerate(s_v):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=8, fontweight="bold",
                color="#E53935" if i == 0 else "#333")
    ax.set_title("Final: sorted, labelled, accent on max",
                 fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/r_iteration.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. Python output — same
# ================================================================
def fig_py_iteration():
    np.random.seed(55)
    cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan"]
    vals = [47, 41, 62, 33, 11]
    sorted_idx = np.argsort(vals)[::-1]
    s_c = [cats[i] for i in sorted_idx]
    s_v = [vals[i] for i in sorted_idx]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    colors_list = ["#E53935"] + ["#2E7D32"] * (len(s_v) - 1)
    ax.barh(s_c, s_v, color=colors_list, height=0.5, edgecolor="none")
    for i, v in enumerate(s_v):
        ax.text(v + 0.8, i, str(v), va="center", fontsize=8, fontweight="bold",
                color="#E53935" if i == 0 else "#333")
    ax.set_title("matplotlib: grey-accent with sorted bars",
                 fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/py_iteration.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    funcs = [
        ("cairo_wheel", fig_cairo_wheel),
        ("munzner_nested", fig_munzner_nested),
        ("design_process", fig_design_process),
        ("task_taxonomy", fig_task_taxonomy),
        ("chart_decision", fig_chart_decision),
        ("audience", fig_audience),
        ("iteration", fig_iteration),
        ("worked_example", fig_worked_example),
        ("r_iteration", fig_r_iteration),
        ("py_iteration", fig_py_iteration),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M06 figures saved to {OUT}/")
