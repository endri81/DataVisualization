"""
Generate ALL figures for Workshop 1, Module 3
Visual Perception & Pre-Attentive Attributes
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from matplotlib.collections import PatchCollection
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m03"
import os
os.makedirs(OUT, exist_ok=True)

np.random.seed(42)

# ================================================================
# 1. PRE-ATTENTIVE: Color pop-out
# ================================================================
def fig_preattentive_color():
    """Red circle among blue circles — instant detection."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    n = 80
    xs = np.random.uniform(0, 10, n)
    ys = np.random.uniform(0, 8, n)
    
    # Left: all same color (search task)
    ax1.scatter(xs, ys, s=120, c="#1565C0", edgecolors="white", linewidth=0.5)
    ax1.set_title("No Pop-Out\nFind the target: ~3 sec",
                  fontsize=10, fontweight="bold")
    ax1.set_xlim(-0.5, 10.5)
    ax1.set_ylim(-0.5, 8.5)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Right: one red among blue (pre-attentive)
    colors = ["#1565C0"] * n
    target = 37
    colors[target] = "#E53935"
    sizes = [120] * n
    sizes[target] = 180
    ax2.scatter(xs, ys, s=sizes, c=colors, edgecolors="white", linewidth=0.5)
    ax2.set_title("Pre-Attentive Pop-Out\nTarget found: <200 ms",
                  fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.5, 10.5)
    ax2.set_ylim(-0.5, 8.5)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Pre-Attentive Processing: Color", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/preattentive_color.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 2. PRE-ATTENTIVE: Shape pop-out
# ================================================================
def fig_preattentive_shape():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    n = 60
    xs = np.random.uniform(0, 10, n)
    ys = np.random.uniform(0, 8, n)
    
    # Left: all circles
    ax1.scatter(xs, ys, s=100, c="#1565C0", marker="o", edgecolors="white", linewidth=0.5)
    ax1.set_title("Homogeneous: All Circles", fontsize=10, fontweight="bold")
    ax1.set_xlim(-0.5, 10.5); ax1.set_ylim(-0.5, 8.5)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Right: one square among circles
    target = 25
    for i in range(n):
        if i == target:
            ax2.scatter(xs[i], ys[i], s=160, c="#E53935", marker="s",
                       edgecolors="white", linewidth=0.5, zorder=5)
        else:
            ax2.scatter(xs[i], ys[i], s=100, c="#1565C0", marker="o",
                       edgecolors="white", linewidth=0.5)
    ax2.set_title("Shape Pop-Out: Square Among Circles", fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.5, 10.5); ax2.set_ylim(-0.5, 8.5)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Pre-Attentive Processing: Shape", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/preattentive_shape.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 3. PRE-ATTENTIVE: Size pop-out
# ================================================================
def fig_preattentive_size():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    n = 60
    xs = np.random.uniform(0, 10, n)
    ys = np.random.uniform(0, 8, n)
    
    # Left: all same size
    ax1.scatter(xs, ys, s=80, c="#1565C0", edgecolors="white", linewidth=0.5)
    ax1.set_title("Uniform Size", fontsize=10, fontweight="bold")
    ax1.set_xlim(-0.5, 10.5); ax1.set_ylim(-0.5, 8.5)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Right: one large among small
    sizes = [80] * n
    target = 42
    sizes[target] = 500
    colors = ["#1565C0"] * n
    colors[target] = "#E53935"
    ax2.scatter(xs, ys, s=sizes, c=colors, edgecolors="white", linewidth=0.5)
    ax2.set_title("Size Pop-Out: Large Among Small", fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.5, 10.5); ax2.set_ylim(-0.5, 8.5)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Pre-Attentive Processing: Size", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/preattentive_size.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 4. PRE-ATTENTIVE: Orientation pop-out
# ================================================================
def fig_preattentive_orientation():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    n = 48
    xs = np.tile(np.linspace(1, 9, 8), 6)
    ys = np.repeat(np.linspace(1, 7, 6), 8)
    
    # Left: all vertical lines
    for x, y in zip(xs, ys):
        ax1.plot([x, x], [y-0.3, y+0.3], color="#1565C0", linewidth=2)
    ax1.set_title("All Vertical", fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 8)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Right: one tilted
    target = 29
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == target:
            ax2.plot([x-0.3, x+0.3], [y-0.3, y+0.3], color="#E53935", linewidth=3)
        else:
            ax2.plot([x, x], [y-0.3, y+0.3], color="#1565C0", linewidth=2)
    ax2.set_title("Orientation Pop-Out: Tilted Line", fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 8)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Pre-Attentive Processing: Orientation", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/preattentive_orientation.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 5. CONJUNCTION FAILURE — no pop-out
# ================================================================
def fig_conjunction():
    """Red square among red circles and blue squares — serial search."""
    fig, ax = plt.subplots(figsize=(5.5, 5))
    n = 60
    xs = np.random.uniform(0.5, 9.5, n)
    ys = np.random.uniform(0.5, 7.5, n)
    
    for i in range(n):
        if i == 33:  # target: red square
            ax.scatter(xs[i], ys[i], s=160, c="#E53935", marker="s",
                      edgecolors="white", linewidth=0.5, zorder=5)
        elif i % 3 == 0:  # red circles
            ax.scatter(xs[i], ys[i], s=100, c="#E53935", marker="o",
                      edgecolors="white", linewidth=0.5)
        elif i % 3 == 1:  # blue squares
            ax.scatter(xs[i], ys[i], s=100, c="#1565C0", marker="s",
                      edgecolors="white", linewidth=0.5)
        else:  # blue circles
            ax.scatter(xs[i], ys[i], s=100, c="#1565C0", marker="o",
                      edgecolors="white", linewidth=0.5)
    
    ax.set_title("Conjunction Search: Red Square Among\nRed Circles & Blue Squares\n"
                 "No pop-out → requires serial scanning (~50 ms/item)",
                 fontsize=10, fontweight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/conjunction.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 6. GESTALT: Proximity
# ================================================================
def fig_gestalt_proximity():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Left: uniform spacing — no grouping perceived
    xs = np.tile(np.arange(0, 10, 1), 5)
    ys = np.repeat(np.arange(0, 5, 1), 10)
    ax1.scatter(xs, ys, s=80, c="#1565C0", edgecolors="white", linewidth=0.5)
    ax1.set_title("Uniform Spacing\n(no grouping)", fontsize=10, fontweight="bold")
    ax1.set_xlim(-1, 11); ax1.set_ylim(-1, 6)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Right: grouped by proximity — 3 clusters perceived
    groups = [
        (np.random.normal(2, 0.5, 15), np.random.normal(3, 0.5, 15)),
        (np.random.normal(5.5, 0.5, 15), np.random.normal(3, 0.5, 15)),
        (np.random.normal(9, 0.5, 15), np.random.normal(3, 0.5, 15)),
    ]
    colors = ["#E53935", "#1565C0", "#2E7D32"]
    for (gx, gy), c in zip(groups, colors):
        ax2.scatter(gx, gy, s=80, c=c, edgecolors="white", linewidth=0.5)
    ax2.set_title("Proximity Grouping\n(3 clusters perceived)", fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.5, 11); ax2.set_ylim(0, 6)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Gestalt Law: Proximity", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/gestalt_proximity.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 7. GESTALT: Similarity
# ================================================================
def fig_gestalt_similarity():
    fig, ax = plt.subplots(figsize=(6, 5))
    
    xs = np.tile(np.arange(0, 8, 1), 6)
    ys = np.repeat(np.arange(0, 6, 1), 8)
    
    for x, y in zip(xs, ys):
        if y % 2 == 0:
            ax.scatter(x, y, s=120, c="#1565C0", marker="o",
                      edgecolors="white", linewidth=0.5)
        else:
            ax.scatter(x, y, s=120, c="#E53935", marker="s",
                      edgecolors="white", linewidth=0.5)
    
    ax.set_title("Gestalt Law: Similarity\nAlternating rows perceived as groups\n"
                 "despite equal spacing",
                 fontsize=10, fontweight="bold")
    ax.set_xlim(-1, 9); ax.set_ylim(-1, 7)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/gestalt_similarity.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 8. GESTALT: Continuity & Closure
# ================================================================
def fig_gestalt_continuity():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Continuity: crossing lines seen as two smooth paths
    t = np.linspace(0, 10, 100)
    ax1.plot(t, np.sin(t) * 2 + 4, color="#1565C0", linewidth=2.5, label="Path A")
    ax1.plot(t, -np.sin(t) * 2 + 4, color="#E53935", linewidth=2.5, label="Path B")
    ax1.set_title("Continuity\nTwo smooth paths, not four segments",
                  fontsize=10, fontweight="bold")
    ax1.legend(fontsize=8, frameon=False)
    ax1.set_xticks([]); ax1.set_yticks([])
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Closure: incomplete circle perceived as complete
    theta = np.linspace(0, 2*np.pi * 0.85, 100)
    ax2.plot(3 + 2*np.cos(theta), 4 + 2*np.sin(theta),
             color="#1565C0", linewidth=3)
    theta2 = np.linspace(0.5, 2*np.pi * 0.75 + 0.5, 100)
    ax2.plot(7 + 1.5*np.cos(theta2), 4 + 1.5*np.sin(theta2),
             color="#E53935", linewidth=3)
    ax2.set_title("Closure\nBrain completes the missing arcs",
                  fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 8)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Gestalt Laws: Continuity & Closure", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/gestalt_continuity.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 9. GESTALT: Enclosure & Connection
# ================================================================
def fig_gestalt_enclosure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Enclosure: points grouped by shaded regions
    np.random.seed(11)
    g1x, g1y = np.random.normal(3, 0.8, 12), np.random.normal(4, 0.8, 12)
    g2x, g2y = np.random.normal(7, 0.8, 12), np.random.normal(4, 0.8, 12)
    
    rect1 = plt.Rectangle((1, 2), 4, 4, facecolor="#E3F2FD", edgecolor="#1565C0",
                           linewidth=1.5, linestyle="--", zorder=0)
    rect2 = plt.Rectangle((5.2, 2), 4, 4, facecolor="#FFEBEE", edgecolor="#E53935",
                           linewidth=1.5, linestyle="--", zorder=0)
    ax1.add_patch(rect1)
    ax1.add_patch(rect2)
    ax1.scatter(g1x, g1y, s=80, c="#1565C0", edgecolors="white", linewidth=0.5, zorder=3)
    ax1.scatter(g2x, g2y, s=80, c="#E53935", edgecolors="white", linewidth=0.5, zorder=3)
    ax1.set_title("Enclosure\nShaded regions create groups",
                  fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 8)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_aspect("equal")
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Connection: lines create grouping
    pts = [(1,2), (3,6), (5,3), (7,5), (9,2)]
    ax2.scatter([p[0] for p in pts], [p[1] for p in pts],
               s=120, c="#1565C0", edgecolors="white", linewidth=0.5, zorder=3)
    # Connect pairs
    ax2.plot([1, 3], [2, 6], color="#1565C0", linewidth=2, zorder=2)
    ax2.plot([5, 7], [3, 5], color="#E53935", linewidth=2, zorder=2)
    ax2.scatter([9], [2], s=120, c="#888888", edgecolors="white", linewidth=0.5, zorder=3)
    ax2.set_title("Connection\nLines create perceived pairs",
                  fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 8)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.set_aspect("equal")
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Gestalt Laws: Enclosure & Connection", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/gestalt_enclosure.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 10. CHANNEL EFFECTIVENESS RANKING (Cleveland & McGill)
# ================================================================
def fig_channel_ranking():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.axis("off")
    
    channels = [
        ("1", "Position on common scale", "#1565C0", "bar chart, dot plot"),
        ("2", "Position on non-aligned scale", "#1976D2", "small multiples"),
        ("3", "Length", "#1E88E5", "bar chart (no baseline)"),
        ("4", "Angle / Slope", "#42A5F5", "pie chart, line chart"),
        ("5", "Area", "#90CAF9", "bubble chart, treemap"),
        ("6", "Volume / Curvature", "#BBDEFB", "3-D chart"),
        ("7", "Color saturation / Hue", "#E3F2FD", "heatmap, choropleth"),
    ]
    
    bar_width = 0.65
    for i, (rank, name, color, example) in enumerate(channels):
        y = 0.92 - i * 0.125
        width = 0.55 - i * 0.05
        
        ax.add_patch(FancyBboxPatch((0.02, y - 0.04), width, 0.08,
                     boxstyle="round,pad=0.01", facecolor=color, edgecolor="none", alpha=0.85))
        ax.text(0.02 + width / 2, y, f"{rank}. {name}",
                ha="center", va="center", fontsize=9, fontweight="bold",
                color="white" if i < 4 else "#333")
        ax.text(0.65, y, f"e.g. {example}", va="center", fontsize=8, color="#555")
    
    ax.text(0.02, 0.02, "← More accurate                    Less accurate →",
            fontsize=9, fontstyle="italic", color="#777")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1)
    ax.set_title("Channel Effectiveness Ranking\n(Cleveland & McGill, 1984)",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/channel_ranking.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 11. WEBER'S LAW — JND illustration
# ================================================================
def fig_weber():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    
    # Position: easy to compare
    ax = axes[0]
    cats = ["A", "B", "C", "D"]
    vals = [42, 45, 43, 44]
    ax.bar(cats, vals, color="#1565C0", width=0.5)
    ax.set_ylim(0, 50)
    ax.set_title("Position\n(easy: ΔV = 1–3)", fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    
    # Area: harder to compare
    ax = axes[1]
    for i, (c, v) in enumerate(zip(cats, vals)):
        r = np.sqrt(v / np.pi)
        circle = plt.Circle((i*2.5 + 1, 4), r * 0.3, color="#E53935", alpha=0.7)
        ax.add_patch(circle)
        ax.text(i*2.5 + 1, 1.5, c, ha="center", fontsize=9, fontweight="bold")
    ax.set_xlim(-0.5, 10); ax.set_ylim(0, 8)
    ax.set_title("Area\n(harder: which circle is largest?)", fontsize=9, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    for sp in ax.spines.values(): sp.set_visible(False)
    
    # Color: hardest to compare
    ax = axes[2]
    saturations = [v / 50 for v in vals]
    for i, (c, s) in enumerate(zip(cats, saturations)):
        rect = plt.Rectangle((i*2.2 + 0.5, 2), 1.5, 4,
                             facecolor=(0.09, 0.33, 0.73, s), edgecolor="none")
        ax.add_patch(rect)
        ax.text(i*2.2 + 1.25, 1.2, c, ha="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_title("Color Saturation\n(hardest: which is darkest?)", fontsize=9, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Weber's Law: Just-Noticeable Difference Depends on Channel",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/weber.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 12. CHANGE BLINDNESS demo
# ================================================================
def fig_change_blindness():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    
    np.random.seed(99)
    n = 40
    x = np.random.uniform(1, 9, n)
    y = np.random.uniform(1, 7, n)
    sizes = np.random.uniform(40, 120, n)
    
    # Version A
    ax1.scatter(x, y, s=sizes, c="#1565C0", alpha=0.6, edgecolors="white", linewidth=0.5)
    ax1.set_title("Version A", fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 8)
    ax1.set_xticks([]); ax1.set_yticks([])
    for sp in ax1.spines.values(): sp.set_visible(False)
    
    # Version B — one point changed color and moved slightly
    colors = ["#1565C0"] * n
    x2 = x.copy(); y2 = y.copy()
    changed = [12, 27]
    colors[changed[0]] = "#E53935"
    x2[changed[1]] += 0.8
    y2[changed[1]] -= 0.6
    
    ax2.scatter(x2, y2, s=sizes, c=colors, alpha=0.6, edgecolors="white", linewidth=0.5)
    ax2.set_title("Version B (2 changes — can you spot them?)",
                  fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 8)
    ax2.set_xticks([]); ax2.set_yticks([])
    for sp in ax2.spines.values(): sp.set_visible(False)
    
    fig.suptitle("Change Blindness: Unguided Attention Misses Subtle Differences",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/change_blindness.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 13. VISUAL ENCODING EXAMPLES — R-style scatter with channels
# ================================================================
def fig_encoding_example_r():
    np.random.seed(55)
    n = 60
    spend = np.random.uniform(10, 100, n)
    roi = 0.4 * spend + np.random.normal(0, 12, n)
    category = np.random.choice(["A", "B", "C"], n)
    size_val = np.random.uniform(20, 200, n)
    
    palette = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    for cat in ["A", "B", "C"]:
        mask = category == cat
        ax.scatter(spend[mask], roi[mask], s=size_val[mask] * 0.8,
                  c=palette[cat], alpha=0.6, edgecolors="white",
                  linewidth=0.4, label=f"Cat {cat}")
    
    ax.set_xlabel("Spend ($K)", fontsize=9)
    ax.set_ylabel("ROI (%)", fontsize=9)
    ax.set_title("Four Channels: Position (x, y) + Color + Size",
                 fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, title="Category", title_fontsize=8, frameon=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.15)
    ax.set_facecolor("#FAFAFA")
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/encoding_r.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 14. Same — Python-style
# ================================================================
def fig_encoding_example_py():
    np.random.seed(55)
    n = 60
    spend = np.random.uniform(10, 100, n)
    roi = 0.4 * spend + np.random.normal(0, 12, n)
    category = np.random.choice(["A", "B", "C"], n)
    size_val = np.random.uniform(20, 200, n)
    
    palette = {"A": "#1f77b4", "B": "#d62728", "C": "#2ca02c"}
    
    fig, ax = plt.subplots(figsize=(5.5, 4))
    for cat in ["A", "B", "C"]:
        mask = category == cat
        ax.scatter(spend[mask], roi[mask], s=size_val[mask] * 0.8,
                  c=palette[cat], alpha=0.65, edgecolors="white",
                  linewidth=0.3, label=f"Cat {cat}")
    
    ax.set_xlabel("Spend ($K)", fontsize=9)
    ax.set_ylabel("ROI (%)", fontsize=9)
    ax.set_title("sns.scatterplot: hue + size encoding",
                 fontsize=10, fontstyle="italic")
    ax.legend(fontsize=7, title="Category", title_fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.15)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/encoding_py.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 15. GESTALT SUMMARY — visual card
# ================================================================
def fig_gestalt_summary():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.axis("off")
    
    laws = [
        ("Proximity", "Near elements grouped together", "#1565C0"),
        ("Similarity", "Like elements grouped together", "#E53935"),
        ("Continuity", "Smooth paths preferred over abrupt changes", "#2E7D32"),
        ("Closure", "Brain completes incomplete shapes", "#7B1FA2"),
        ("Enclosure", "Bounded regions create groups", "#E65100"),
        ("Connection", "Linked elements seen as related", "#00695C"),
    ]
    
    for i, (name, desc, color) in enumerate(laws):
        col = i % 2
        row = i // 2
        x = 0.02 + col * 0.5
        y = 0.78 - row * 0.3
        
        ax.add_patch(FancyBboxPatch((x, y - 0.08), 0.44, 0.22,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                     edgecolor=color, linewidth=1.5))
        ax.text(x + 0.22, y + 0.06, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color)
        ax.text(x + 0.22, y - 0.03, desc, ha="center", va="center",
                fontsize=8, color="#444")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1)
    ax.set_title("The Six Gestalt Laws for Data Visualization",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/gestalt_summary.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    funcs = [
        ("preattentive_color", fig_preattentive_color),
        ("preattentive_shape", fig_preattentive_shape),
        ("preattentive_size", fig_preattentive_size),
        ("preattentive_orientation", fig_preattentive_orientation),
        ("conjunction", fig_conjunction),
        ("gestalt_proximity", fig_gestalt_proximity),
        ("gestalt_similarity", fig_gestalt_similarity),
        ("gestalt_continuity", fig_gestalt_continuity),
        ("gestalt_enclosure", fig_gestalt_enclosure),
        ("channel_ranking", fig_channel_ranking),
        ("weber", fig_weber),
        ("change_blindness", fig_change_blindness),
        ("encoding_r", fig_encoding_example_r),
        ("encoding_py", fig_encoding_example_py),
        ("gestalt_summary", fig_gestalt_summary),
    ]
    
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    print(f"\nAll M03 figures saved to {OUT}/")
