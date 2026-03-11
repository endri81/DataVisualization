"""
Generate ALL figures for Workshop 1, Module 5
Typography, Layout & Composition
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m05"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. TYPOGRAPHIC HIERARCHY — title / subtitle / body / caption
# ================================================================
def fig_type_hierarchy():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.axis("off")
    
    levels = [
        (0.5, 0.88, "Chart Title: GDP Growth by Region", 18, "bold", "#1A237E"),
        (0.5, 0.76, "Subtitle: Quarterly data, 2020–2024, seasonally adjusted", 12, "normal", "#555555"),
        (0.5, 0.58, "Body Text / Axis Labels: 10–11pt, regular weight,\nhigh contrast against background", 11, "normal", "#333333"),
        (0.5, 0.40, "Annotation: Direct labels on data points,\n8–9pt, can use colour to match data series", 9, "normal", "#1565C0"),
        (0.5, 0.24, "Caption / Source: Source: World Bank (2024). Note: excludes tax havens.", 8, "italic", "#888888"),
    ]
    
    for x, y, text, size, weight, color in levels:
        ax.text(x, y, text, ha="center", va="center", fontsize=size,
                fontweight=weight, color=color, fontstyle="italic" if weight == "italic" else "normal",
                linespacing=1.4)
    
    # Separators
    for y_sep in [0.82, 0.68, 0.49, 0.32]:
        ax.axhline(y=y_sep, xmin=0.1, xmax=0.9, color="#E0E0E0", linewidth=0.8, linestyle="--")
    
    # Size annotations on right
    sizes = [("18pt Bold", 0.88), ("12pt Regular", 0.76), ("11pt Regular", 0.58),
             ("9pt Regular", 0.40), ("8pt Italic", 0.24)]
    for label, y in sizes:
        ax.text(0.95, y, label, ha="right", va="center", fontsize=7,
                color="#999", fontfamily="monospace")
    
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 1)
    ax.set_title("Typographic Hierarchy in Data Visualization",
                 fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/type_hierarchy.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. FONT PAIRING — Sans-serif for charts
# ================================================================
def fig_font_pairing():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    fonts_info = [
        ("Sans-Serif\n(Recommended)", "Fira Sans, Helvetica,\nArial, Source Sans Pro",
         "#1565C0", "Clean, modern, legible\nat small sizes on screen"),
        ("Serif\n(Use sparingly)", "Georgia, Palatino,\nTimes New Roman",
         "#E65100", "Better for long prose;\naxis labels can look heavy"),
        ("Monospace\n(Code only)", "Fira Code, Consolas,\nSource Code Pro",
         "#2E7D32", "For code blocks and\nnumeric tables only"),
    ]
    
    for ax, (title, examples, color, note) in zip(axes, fonts_info):
        ax.add_patch(FancyBboxPatch((0.05, 0.15), 0.9, 0.7,
                     boxstyle="round,pad=0.05", facecolor=color, alpha=0.08,
                     edgecolor=color, linewidth=2))
        ax.text(0.5, 0.72, title, ha="center", va="center", fontsize=12,
                fontweight="bold", color=color)
        ax.text(0.5, 0.48, examples, ha="center", va="center", fontsize=9, color="#444")
        ax.text(0.5, 0.25, note, ha="center", va="center", fontsize=8,
                color="#666", fontstyle="italic")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Font Selection for Data Visualization",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/font_pairing.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. WHITESPACE — cramped vs breathing room
# ================================================================
def fig_whitespace():
    cats = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    vals = [42, 58, 35, 67, 51]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Cramped: no margins, tight bars, heavy borders
    ax1.bar(cats, vals, color="#1565C0", edgecolor="black", linewidth=1.5, width=0.95)
    ax1.set_title("CRAMPED: No Whitespace", fontsize=10, fontweight="bold", color="#C62828", pad=2)
    ax1.set_ylabel("Sales ($K)", fontsize=9, labelpad=1)
    ax1.tick_params(labelsize=7, pad=1)
    ax1.set_xticklabels(cats, rotation=45, ha="right")
    ax1.set_facecolor("#F0F0F0")
    ax1.grid(True, color="gray", linewidth=0.8)
    # Simulate no margin
    ax1.margins(x=0, y=0)
    
    # Breathing: generous margins, thin bars, no border
    sorted_idx = np.argsort(vals)[::-1]
    s_cats = [cats[i] for i in sorted_idx]
    s_vals = [vals[i] for i in sorted_idx]
    
    ax2.barh(s_cats, s_vals, color="#1565C0", height=0.5, edgecolor="none")
    for i, v in enumerate(s_vals):
        ax2.text(v + 1, i, str(v), va="center", fontsize=9, color="#333")
    ax2.set_title("BREATHING: Generous Whitespace", fontsize=10, fontweight="bold",
                  color="#1565C0", pad=15)
    ax2.set_xlabel("Sales ($K)", fontsize=9, labelpad=10)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.tick_params(left=False, labelsize=8, pad=5)
    ax2.set_xlim(0, 80)
    ax2.grid(axis="x", alpha=0.12)
    
    fig.suptitle("Whitespace Is Not Wasted Space — It Guides the Eye",
                 fontsize=12, fontweight="bold")
    plt.tight_layout(pad=2.0)
    fig.savefig(f"{OUT}/whitespace.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. GRID SYSTEMS — 1-col, 2-col, dashboard grid
# ================================================================
def fig_grid_layouts():
    fig = plt.figure(figsize=(12, 5))
    
    # Layout A: single chart (full width)
    ax_a = fig.add_axes([0.02, 0.1, 0.28, 0.75])
    ax_a.text(0.5, 0.5, "Single Chart\n(Full Width)", ha="center", va="center",
              fontsize=10, fontweight="bold", color="#1565C0")
    ax_a.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                   edgecolor="#1565C0", linewidth=2, linestyle="--"))
    ax_a.set_xlim(0, 1); ax_a.set_ylim(0, 1)
    ax_a.set_xticks([]); ax_a.set_yticks([])
    ax_a.set_title("Layout A", fontsize=9, fontweight="bold")
    for sp in ax_a.spines.values(): sp.set_visible(False)
    
    # Layout B: 2-column
    ax_b = fig.add_axes([0.35, 0.1, 0.28, 0.75])
    for i, (x, label) in enumerate([(0.05, "Left\nPanel"), (0.52, "Right\nPanel")]):
        ax_b.add_patch(Rectangle((x, 0.05), 0.43, 0.9, fill=False,
                       edgecolor="#E53935", linewidth=2, linestyle="--"))
        ax_b.text(x + 0.215, 0.5, label, ha="center", va="center",
                  fontsize=9, fontweight="bold", color="#E53935")
    ax_b.set_xlim(0, 1); ax_b.set_ylim(0, 1)
    ax_b.set_xticks([]); ax_b.set_yticks([])
    ax_b.set_title("Layout B", fontsize=9, fontweight="bold")
    for sp in ax_b.spines.values(): sp.set_visible(False)
    
    # Layout C: dashboard grid (2x2 + KPI row)
    ax_c = fig.add_axes([0.68, 0.1, 0.28, 0.75])
    # KPI row
    for i in range(3):
        x = 0.03 + i * 0.33
        ax_c.add_patch(Rectangle((x, 0.72), 0.28, 0.22, fill=False,
                       edgecolor="#2E7D32", linewidth=1.5, linestyle="--"))
        ax_c.text(x + 0.14, 0.83, f"KPI {i+1}", ha="center", va="center",
                  fontsize=7, fontweight="bold", color="#2E7D32")
    # Main charts (2x2)
    positions = [(0.03, 0.38, 0.44, 0.28), (0.53, 0.38, 0.44, 0.28),
                 (0.03, 0.05, 0.44, 0.28), (0.53, 0.05, 0.44, 0.28)]
    for j, (x, y, w, h) in enumerate(positions):
        ax_c.add_patch(Rectangle((x, y), w, h, fill=False,
                       edgecolor="#2E7D32", linewidth=1.5, linestyle="--"))
        ax_c.text(x + w/2, y + h/2, f"Chart {j+1}", ha="center", va="center",
                  fontsize=7, color="#2E7D32")
    ax_c.set_xlim(0, 1); ax_c.set_ylim(0, 1)
    ax_c.set_xticks([]); ax_c.set_yticks([])
    ax_c.set_title("Layout C", fontsize=9, fontweight="bold")
    for sp in ax_c.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Grid Systems: Single → Two-Column → Dashboard",
                 fontsize=12, fontweight="bold", y=0.98)
    fig.savefig(f"{OUT}/grid_layouts.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. ALIGNMENT — left-aligned vs centred labels
# ================================================================
def fig_alignment():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    labels = ["Revenue ($M)", "Operating Income", "Net Margin (%)", "EPS ($)", "FCF ($M)"]
    values = [2450, 680, 27.8, 4.52, 410]
    
    # Misaligned (centred numbers — hard to compare)
    ax1.barh(range(5), values, color="#BBBBBB", height=0.5)
    for i, (l, v) in enumerate(zip(labels, values)):
        ax1.text(max(values)/2, i, f"{v}", ha="center", va="center", fontsize=9, fontweight="bold")
    ax1.set_yticks(range(5)); ax1.set_yticklabels(labels, fontsize=8)
    ax1.set_title("Centred Labels\n(hard to compare numbers)", fontsize=9, fontweight="bold", color="#C62828")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.invert_yaxis()
    ax1.tick_params(labelsize=7)
    
    # Right-aligned (easy to compare)
    ax2.barh(range(5), values, color="#1565C0", height=0.5, edgecolor="none")
    for i, (l, v) in enumerate(zip(labels, values)):
        ax2.text(v + 30, i, f"{v:>8}", ha="left", va="center", fontsize=9,
                 fontfamily="monospace", color="#333")
    ax2.set_yticks(range(5)); ax2.set_yticklabels(labels, fontsize=8)
    ax2.set_title("Right-Aligned Labels\n(easy to compare digits)", fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.invert_yaxis()
    ax2.tick_params(left=False, labelsize=7)
    
    fig.suptitle("Alignment: Numbers Should Right-Align for Easy Comparison",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/alignment.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. DIRECT LABELLING vs LEGEND
# ================================================================
def fig_direct_label():
    np.random.seed(7)
    months = np.arange(1, 13)
    series = {
        "Product A": np.cumsum(np.random.normal(3, 4, 12)) + 40,
        "Product B": np.cumsum(np.random.normal(2, 3, 12)) + 30,
        "Product C": np.cumsum(np.random.normal(1, 5, 12)) + 20,
    }
    colors = {"Product A": "#1565C0", "Product B": "#E53935", "Product C": "#2E7D32"}
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    
    # With legend (forces eye to shuttle back and forth)
    for name, data in series.items():
        ax1.plot(months, data, color=colors[name], linewidth=2, label=name)
    ax1.legend(fontsize=7, frameon=True, loc="upper left")
    ax1.set_title("Legend Box\n(eye shuttles between legend & lines)",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_xlabel("Month", fontsize=8)
    ax1.set_ylabel("Revenue ($K)", fontsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelsize=7)
    
    # With direct labels (label at line endpoint)
    for name, data in series.items():
        ax2.plot(months, data, color=colors[name], linewidth=2)
        ax2.text(12.3, data[-1], name, fontsize=8, fontweight="bold",
                 color=colors[name], va="center")
    ax2.set_title("Direct Labels\n(label at endpoint — no eye shuttling)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.set_xlabel("Month", fontsize=8)
    ax2.set_ylabel("Revenue ($K)", fontsize=8)
    ax2.set_xlim(1, 15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Direct Labelling Reduces Cognitive Load",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/direct_label.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. ANNOTATION PATTERNS — callout, highlight, context
# ================================================================
def fig_annotation_patterns():
    np.random.seed(99)
    months = np.arange(1, 25)
    values = np.cumsum(np.random.normal(2, 6, 24)) + 100
    values[11] = values[10] - 25  # Create a dip
    values[12:] = values[12:] + 15
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(months, values, color="#1565C0", linewidth=2)
    ax.fill_between(months, values, alpha=0.06, color="#1565C0")
    
    # Annotation 1: Callout with arrow
    ax.annotate("Product recall\n(Mar 2023)",
                xy=(12, values[11]), xytext=(16, values[11] - 20),
                fontsize=8, fontweight="bold", color="#C62828",
                arrowprops=dict(arrowstyle="->", color="#C62828", linewidth=1.5),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEBEE", edgecolor="#C62828", alpha=0.8))
    
    # Annotation 2: Shaded context region
    ax.axvspan(14, 18, color="#E8F5E9", alpha=0.6)
    ax.text(16, max(values) + 5, "Recovery\nperiod", ha="center", fontsize=8,
            fontweight="bold", color="#2E7D32")
    
    # Annotation 3: Reference line
    mean_val = np.mean(values)
    ax.axhline(y=mean_val, color="#888888", linewidth=1, linestyle="--")
    ax.text(24.5, mean_val, f"Mean: {mean_val:.0f}", fontsize=7, va="center", color="#888")
    
    ax.set_xlabel("Month", fontsize=9)
    ax.set_ylabel("Revenue ($K)", fontsize=9)
    ax.set_title("Three Annotation Patterns: Callout, Context Band, Reference Line",
                 fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/annotation_patterns.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. PATCHWORK / COWPLOT — multi-panel composition (R-style)
# ================================================================
def fig_multipanel_r():
    np.random.seed(55)
    fig = plt.figure(figsize=(8, 5))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # Top-left: bar chart
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.barh(["A", "B", "C", "D"], [42, 58, 35, 67], color="#1565C0", height=0.5)
    ax1.set_title("(a) Revenue", fontsize=8, fontweight="bold")
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelsize=6)
    
    # Top-middle: scatter
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.scatter(np.random.uniform(0, 10, 40), np.random.uniform(0, 10, 40),
                s=20, c="#E53935", alpha=0.6)
    ax2.set_title("(b) Scatter", fontsize=8, fontweight="bold")
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=6)
    
    # Top-right: line
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(np.arange(12), np.cumsum(np.random.normal(1, 3, 12)) + 20,
             color="#2E7D32", linewidth=1.5)
    ax3.set_title("(c) Trend", fontsize=8, fontweight="bold")
    ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
    ax3.tick_params(labelsize=6)
    
    # Bottom: full-width panel
    ax4 = fig.add_subplot(gs[1, :])
    t = np.arange(1, 25)
    ax4.plot(t, np.cumsum(np.random.normal(2, 5, 24)) + 100, color="#1565C0", linewidth=2)
    ax4.fill_between(t, np.cumsum(np.random.normal(2, 5, 24)) + 100, alpha=0.06, color="#1565C0")
    ax4.set_title("(d) 24-Month Timeline (full width)", fontsize=8, fontweight="bold")
    ax4.spines["top"].set_visible(False); ax4.spines["right"].set_visible(False)
    ax4.tick_params(labelsize=6)
    
    fig.suptitle("Multi-Panel Composition: patchwork (R) / GridSpec (Python)",
                 fontsize=11, fontweight="bold")
    fig.savefig(f"{OUT}/multipanel.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. ASPECT RATIO — banking to 45 degrees
# ================================================================
def fig_aspect_ratio():
    np.random.seed(22)
    x = np.arange(1, 25)
    y = np.cumsum(np.random.normal(0.5, 2, 24)) + 50
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.5))
    
    # Square (bad for time series)
    ax1.plot(x, y, color="#1565C0", linewidth=1.5)
    ax1.set_aspect("equal", adjustable="datalim")
    ax1.set_title("Square Aspect\n(slopes compressed)", fontsize=9, fontweight="bold", color="#C62828")
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelsize=7)
    
    # Wide (banked to ~45°)
    ax2.plot(x, y, color="#1565C0", linewidth=1.5)
    ax2.set_title("Banked to 45°\n(slopes readable)", fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Aspect Ratio: Banking to 45° Makes Slopes Readable (Cleveland, 1993)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/aspect_ratio.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. EXPORT FORMATS — vector vs raster comparison card
# ================================================================
def fig_export_formats():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis("off")
    
    rows = [
        ("PDF", "Vector", "Publication, print", "Infinite", "#1565C0"),
        ("SVG", "Vector", "Web, interactive", "Infinite", "#1565C0"),
        ("PNG", "Raster", "Web, presentations", "≥150 dpi", "#E65100"),
        ("JPEG", "Raster (lossy)", "Photos only", "≥150 dpi", "#C62828"),
        ("TIFF", "Raster", "Journal submission", "≥300 dpi", "#E65100"),
    ]
    
    headers = ["Format", "Type", "Best For", "Resolution", ""]
    col_x = [0.08, 0.22, 0.48, 0.75]
    
    # Header
    for j, (x, h) in enumerate(zip(col_x, headers[:4])):
        ax.text(x, 0.92, h, fontsize=10, fontweight="bold", color="#1A237E", va="center")
    ax.axhline(y=0.87, xmin=0.04, xmax=0.92, color="#1A237E", linewidth=1.5)
    
    for i, (fmt, typ, use, res, color) in enumerate(rows):
        y = 0.78 - i * 0.14
        ax.text(col_x[0], y, fmt, fontsize=10, fontweight="bold", color=color, va="center",
                fontfamily="monospace")
        ax.text(col_x[1], y, typ, fontsize=9, va="center", color="#444")
        ax.text(col_x[2], y, use, fontsize=9, va="center", color="#444")
        ax.text(col_x[3], y, res, fontsize=9, va="center", color="#444")
        if i < len(rows) - 1:
            ax.axhline(y=y - 0.07, xmin=0.04, xmax=0.92, color="#E0E0E0", linewidth=0.5)
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Export Format Decision Guide", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/export_formats.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    funcs = [
        ("type_hierarchy", fig_type_hierarchy),
        ("font_pairing", fig_font_pairing),
        ("whitespace", fig_whitespace),
        ("grid_layouts", fig_grid_layouts),
        ("alignment", fig_alignment),
        ("direct_label", fig_direct_label),
        ("annotation_patterns", fig_annotation_patterns),
        ("multipanel", fig_multipanel_r),
        ("aspect_ratio", fig_aspect_ratio),
        ("export_formats", fig_export_formats),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M05 figures saved to {OUT}/")
