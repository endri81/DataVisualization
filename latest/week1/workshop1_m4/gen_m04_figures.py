"""
Generate ALL figures for Workshop 1, Module 4
Color Theory & Accessibility
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, Rectangle
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m04"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. COLOR WHEEL — Hue, Saturation, Lightness
# ================================================================
def fig_hsl_wheel():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # Hue ring
    ax = axes[0]
    n = 256
    theta = np.linspace(0, 2*np.pi, n)
    for i in range(n-1):
        ax.barh(0, 1, left=i, height=1,
                color=plt.cm.hsv(i/n), edgecolor="none")
    ax.set_xlim(0, n)
    ax.set_yticks([])
    ax.set_xticks([0, 64, 128, 192, 256])
    ax.set_xticklabels(["0°", "90°", "180°", "270°", "360°"], fontsize=8)
    ax.set_title("Hue\n(the 'name' of the colour)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # Saturation gradient
    ax = axes[1]
    for i in range(256):
        s = i / 255
        c = (0.08 + 0.78*s, 0.33 - 0.15*(1-s), 0.73 * s + 0.73*(1-s)*0.3)
        ax.barh(0, 1, left=i, height=1, color=c, edgecolor="none")
    ax.set_xlim(0, 256)
    ax.set_yticks([])
    ax.set_xticks([0, 128, 256])
    ax.set_xticklabels(["Grey\n(0%)", "50%", "Vivid\n(100%)"], fontsize=8)
    ax.set_title("Saturation\n(intensity / vividness)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # Lightness gradient
    ax = axes[2]
    for i in range(256):
        v = i / 255
        ax.barh(0, 1, left=i, height=1, color=(v*0.08, v*0.33, v*0.73), edgecolor="none")
    ax.set_xlim(0, 256)
    ax.set_yticks([])
    ax.set_xticks([0, 128, 256])
    ax.set_xticklabels(["Black\n(0%)", "50%", "Full\n(100%)"], fontsize=8)
    ax.set_title("Lightness\n(dark to bright)", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    fig.suptitle("The Three Dimensions of Colour: Hue, Saturation, Lightness",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/hsl.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. THREE PALETTE TYPES: Sequential, Diverging, Qualitative
# ================================================================
def fig_palette_types():
    fig, axes = plt.subplots(3, 1, figsize=(8, 5))
    n = 9
    
    # Sequential
    ax = axes[0]
    cmap = plt.cm.Blues
    for i in range(n):
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=cmap((i+1)/(n+1)), edgecolor="white", lw=2))
    ax.set_xlim(0, n); ax.set_ylim(0, 1)
    ax.set_title("Sequential: low → high  (e.g., Blues, viridis)", fontsize=10, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.3, -0.25, "Low", fontsize=8, ha="center")
    ax.text(n-0.7, -0.25, "High", fontsize=8, ha="center")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    # Diverging
    ax = axes[1]
    cmap = plt.cm.RdBu_r
    for i in range(n):
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=cmap(i/(n-1)), edgecolor="white", lw=2))
    ax.set_xlim(0, n); ax.set_ylim(0, 1)
    ax.set_title("Diverging: negative ← neutral → positive  (e.g., RdBu)", fontsize=10, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.3, -0.25, "Negative", fontsize=8, ha="center")
    ax.text(n/2, -0.25, "Zero", fontsize=8, ha="center")
    ax.text(n-0.7, -0.25, "Positive", fontsize=8, ha="center")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    # Qualitative
    ax = axes[2]
    qual_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                   "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22"]
    for i in range(n):
        ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=qual_colors[i], edgecolor="white", lw=2))
    ax.set_xlim(0, n); ax.set_ylim(0, 1)
    ax.set_title("Qualitative: distinct categories  (e.g., Set1, tab10)", fontsize=10, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(n/2, -0.25, "No inherent order", fontsize=8, ha="center")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/palette_types.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. VIRIDIS FAMILY — perceptually uniform
# ================================================================
def fig_viridis_family():
    fig, axes = plt.subplots(4, 1, figsize=(8, 4))
    names = ["viridis", "magma", "plasma", "inferno"]
    
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    
    for ax, name in zip(axes, names):
        ax.imshow(gradient, aspect="auto", cmap=name)
        ax.set_ylabel(name, fontsize=9, fontweight="bold", rotation=0, labelpad=50, va="center")
        ax.set_xticks([]); ax.set_yticks([])
    
    fig.suptitle("The viridis Family: Perceptually Uniform, Colourblind-Safe, Print-Friendly",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/viridis_family.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. COLORBREWER — sequential, diverging, qualitative swatches
# ================================================================
def fig_colorbrewer():
    fig, axes = plt.subplots(3, 1, figsize=(8, 4.5))
    
    brewer = {
        "Sequential\n(YlGnBu)": ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#0c2c84"],
        "Diverging\n(RdYlBu)": ["#d73027","#f46d43","#fdae61","#fee090","#e0f3f8","#abd9e9","#74add1","#4575b4"],
        "Qualitative\n(Set2)": ["#66c2a5","#fc8d62","#8da0cb","#e78ac3","#a6d854","#ffd92f","#e5c494","#b3b3b3"],
    }
    
    for ax, (label, colors) in zip(axes, brewer.items()):
        for i, c in enumerate(colors):
            ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=c, edgecolor="white", lw=2))
        ax.set_xlim(0, len(colors)); ax.set_ylim(0, 1)
        ax.set_ylabel(label, fontsize=8, fontweight="bold", rotation=0, labelpad=70, va="center")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
    
    fig.suptitle("ColorBrewer Palettes (Brewer, 2003)\nhttps://colorbrewer2.org",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/colorbrewer.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. COLORBLINDNESS SIMULATION — Deuteranopia
# ================================================================
def fig_colorblind_sim():
    """Simulate how red-green deficient vision sees a standard palette."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Normal vision
    normal_colors = ["#d62728", "#2ca02c", "#1f77b4", "#ff7f0e", "#9467bd"]
    labels = ["Red", "Green", "Blue", "Orange", "Purple"]
    vals = [35, 28, 42, 31, 24]
    
    ax1.barh(labels, vals, color=normal_colors, height=0.6, edgecolor="white", lw=1)
    ax1.set_title("Normal Vision\n(trichromatic)", fontsize=10, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    for i, v in enumerate(vals):
        ax1.text(v + 0.5, i, str(v), va="center", fontsize=9)
    ax1.tick_params(labelsize=8)
    
    # Deuteranopia simulation (red and green become similar brownish)
    deutan_colors = ["#8B7D3C", "#8B8B3C", "#1f77b4", "#C4A040", "#6B5DA0"]
    ax2.barh(labels, vals, color=deutan_colors, height=0.6, edgecolor="white", lw=1)
    ax2.set_title("Deuteranopia Simulation\n(~8% of males)", fontsize=10, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    for i, v in enumerate(vals):
        ax2.text(v + 0.5, i, str(v), va="center", fontsize=9)
    ax2.tick_params(labelsize=8)
    
    fig.suptitle("Colour Vision Deficiency: Why Red-Green Palettes Fail",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/colorblind_sim.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. ACCESSIBLE PALETTE — viridis vs rainbow
# ================================================================
def fig_rainbow_vs_viridis():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    np.random.seed(7)
    x = np.random.uniform(0, 10, 200)
    y = np.random.uniform(0, 10, 200)
    z = np.sin(x) * np.cos(y) + np.random.normal(0, 0.3, 200)
    
    # Rainbow (bad)
    sc1 = ax1.scatter(x, y, c=z, cmap="rainbow", s=30, edgecolors="none")
    ax1.set_title("Rainbow\n(perceptual artefacts, colourblind-hostile)",
                  fontsize=9, fontweight="bold", color="#C62828")
    plt.colorbar(sc1, ax=ax1, shrink=0.7)
    ax1.tick_params(labelsize=7)
    
    # Viridis (good)
    sc2 = ax2.scatter(x, y, c=z, cmap="viridis", s=30, edgecolors="none")
    ax2.set_title("Viridis\n(perceptually uniform, colourblind-safe)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    plt.colorbar(sc2, ax=ax2, shrink=0.7)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Never Use Rainbow: Viridis Is Always Better",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/rainbow_vs_viridis.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. GREY + ACCENT STRATEGY
# ================================================================
def fig_grey_accent():
    np.random.seed(55)
    n = 100
    x = np.random.uniform(10, 100, n)
    y = 0.4 * x + np.random.normal(0, 12, n)
    cat = np.random.choice(["Other", "Other", "Other", "Highlight"], n, p=[0.3,0.3,0.3,0.1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # All coloured (confusing)
    colors_all = {"Other": "#1f77b4", "Highlight": "#d62728"}
    cats_unique = np.random.choice(["A","B","C","D"], n)
    palette4 = {"A": "#1f77b4", "B": "#ff7f0e", "C": "#2ca02c", "D": "#d62728"}
    for c in ["A","B","C","D"]:
        mask = cats_unique == c
        ax1.scatter(x[mask], y[mask], c=palette4[c], s=30, alpha=0.6, label=c)
    ax1.legend(fontsize=7, title="Category")
    ax1.set_title("All Categories Coloured\n(cluttered, no hierarchy)",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.tick_params(labelsize=7)
    
    # Grey + accent (clean)
    mask_hl = cats_unique == "D"
    ax2.scatter(x[~mask_hl], y[~mask_hl], c="#BBBBBB", s=25, alpha=0.4, label="Other")
    ax2.scatter(x[mask_hl], y[mask_hl], c="#E53935", s=50, alpha=0.8,
                edgecolors="white", linewidth=0.5, label="Category D", zorder=5)
    ax2.legend(fontsize=7)
    ax2.set_title("Grey + Accent\n(clear hierarchy, instant focus)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Strategic Colour: Grey + Accent > Rainbow Everything",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/grey_accent.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. WCAG CONTRAST CHECKER — good vs bad text
# ================================================================
def fig_wcag_contrast():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    
    combos = [
        ("#FFFF00", "#FFFFFF", "FAIL (1.07:1)\nYellow on white", "#C62828"),
        ("#1565C0", "#FFFFFF", "PASS AA (8.56:1)\nBlue on white", "#2E7D32"),
        ("#FFFFFF", "#333333", "PASS AAA (12.63:1)\nWhite on dark", "#2E7D32"),
    ]
    
    for ax, (fg, bg, label, verdict_color) in zip(axes, combos):
        ax.set_facecolor(bg)
        ax.text(0.5, 0.6, "Sample Text Aa", ha="center", va="center",
                fontsize=16, fontweight="bold", color=fg)
        ax.text(0.5, 0.2, label, ha="center", va="center",
                fontsize=9, color=verdict_color, fontweight="bold")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_linewidth(2)
            sp.set_color(fg)
    
    fig.suptitle("WCAG 2.1 Contrast Requirements\n"
                 "AA: ≥4.5:1 normal text, ≥3:1 large text  |  AAA: ≥7:1",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/wcag_contrast.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. SEQUENTIAL HEATMAP — R style
# ================================================================
def fig_heatmap_r():
    np.random.seed(33)
    data = np.random.uniform(10, 90, (6, 8))
    rows = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    cols = [f"W{i}" for i in range(1, 9)]
    
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    im = ax.imshow(data, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(8)); ax.set_xticklabels(cols, fontsize=7)
    ax.set_yticks(range(6)); ax.set_yticklabels(rows, fontsize=7)
    plt.colorbar(im, ax=ax, shrink=0.8, label="Value")
    ax.set_title("ggplot2: scale_fill_viridis_c()", fontsize=9, fontstyle="italic")
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/heatmap_r.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. SEQUENTIAL HEATMAP — Python style
# ================================================================
def fig_heatmap_py():
    np.random.seed(33)
    data = np.random.uniform(10, 90, (6, 8))
    rows = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    cols = [f"W{i}" for i in range(1, 9)]
    
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    im = ax.imshow(data, cmap="viridis", aspect="auto")
    ax.set_xticks(range(8)); ax.set_xticklabels(cols, fontsize=7)
    ax.set_yticks(range(6)); ax.set_yticklabels(rows, fontsize=7)
    plt.colorbar(im, ax=ax, shrink=0.8, label="Value")
    ax.set_title("plt.imshow(cmap='viridis')", fontsize=9, fontstyle="italic")
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/heatmap_py.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 11. DIVERGING CHOROPLETH — R style
# ================================================================
def fig_diverging_map():
    np.random.seed(44)
    n = 50
    x = np.random.uniform(0, 10, n)
    y = np.random.uniform(0, 8, n)
    z = np.random.uniform(-1, 1, n)
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    sc = ax.scatter(x, y, c=z, cmap="RdBu_r", s=80, edgecolors="white",
                    linewidth=0.5, vmin=-1, vmax=1)
    plt.colorbar(sc, ax=ax, shrink=0.8, label="Deviation from Mean")
    ax.set_title("Diverging Palette: RdBu\nCentred on zero, bidirectional",
                 fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/diverging_map.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 12. PALETTE DECISION TREE
# ================================================================
def fig_decision_tree():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    
    # Root
    ax.add_patch(FancyBboxPatch((2.8, 4.2), 2.4, 0.6, boxstyle="round,pad=0.1",
                 facecolor="#E3F2FD", edgecolor="#1565C0", lw=2))
    ax.text(4, 4.5, "What type\nof data?", ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Branches
    branches = [
        (1, 2.8, "Ordered\n(quantitative)", "#1565C0"),
        (4, 2.8, "Diverging\n(+/− from centre)", "#E53935"),
        (7, 2.8, "Categorical\n(nominal)", "#2E7D32"),
    ]
    for bx, by, label, color in branches:
        ax.add_patch(FancyBboxPatch((bx - 0.9, by - 0.3), 1.8, 0.6,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor="none", alpha=0.15))
        ax.text(bx, by, label, ha="center", va="center", fontsize=9, fontweight="bold", color=color)
        ax.annotate("", xy=(bx, by + 0.3), xytext=(4, 4.2),
                    arrowprops=dict(arrowstyle="->", color="#666", lw=1.2))
    
    # Leaves
    leaves = [
        (1, 1.2, "viridis, Blues,\nYlGnBu", "#1565C0"),
        (4, 1.2, "RdBu, RdYlGn,\nPiYG", "#E53935"),
        (7, 1.2, "Set1, Set2,\ntab10 (≤7)", "#2E7D32"),
    ]
    for lx, ly, label, color in leaves:
        ax.add_patch(FancyBboxPatch((lx - 0.9, ly - 0.3), 1.8, 0.6,
                     boxstyle="round,pad=0.1", facecolor=color, edgecolor="none", alpha=0.08))
        ax.text(lx, ly, label, ha="center", va="center", fontsize=8, color=color)
        ax.annotate("", xy=(lx, ly + 0.3), xytext=(lx, 2.5),
                    arrowprops=dict(arrowstyle="->", color="#666", lw=1))
    
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(0.5, 5.2)
    ax.set_title("Palette Decision Tree", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/decision_tree.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 13. COLOUR DO'S AND DON'TS — side by side
# ================================================================
def fig_dos_donts():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    cats = ["Cat A", "Cat B", "Cat C", "Cat D", "Cat E"]
    vals = [34, 45, 28, 52, 38]
    
    # DON'T: rainbow on nominal
    rainbow = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
    ax1.bar(cats, vals, color=rainbow, edgecolor="black", linewidth=1)
    ax1.set_title("DON'T: Saturated rainbow\n(garish, colourblind-hostile)",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.tick_params(labelsize=7)
    ax1.set_facecolor("#F5F5F5")
    
    # DO: muted qualitative
    muted = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]
    ax2.bar(cats, vals, color=muted, edgecolor="white", linewidth=1)
    ax2.set_title("DO: Muted Tableau 10\n(distinguishable, accessible)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Colour Selection: Muted Palettes Over Saturated Rainbow",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/dos_donts.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    funcs = [
        ("hsl", fig_hsl_wheel),
        ("palette_types", fig_palette_types),
        ("viridis_family", fig_viridis_family),
        ("colorbrewer", fig_colorbrewer),
        ("colorblind_sim", fig_colorblind_sim),
        ("rainbow_vs_viridis", fig_rainbow_vs_viridis),
        ("grey_accent", fig_grey_accent),
        ("wcag_contrast", fig_wcag_contrast),
        ("heatmap_r", fig_heatmap_r),
        ("heatmap_py", fig_heatmap_py),
        ("diverging_map", fig_diverging_map),
        ("decision_tree", fig_decision_tree),
        ("dos_donts", fig_dos_donts),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M04 figures saved to {OUT}/")
