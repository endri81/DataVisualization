"""
Generate ALL figures for Workshop 1, Module 7
Critique & Redesign Workshop
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures_m07"
import os
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)


# ================================================================
# 1. CRITIQUE FRAMEWORK — 4-quadrant rubric
# ================================================================
def fig_critique_framework():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("off")
    
    quadrants = [
        (0.25, 0.72, "1. DATA INTEGRITY", 
         "• Is the data accurate?\n• Are axes labelled correctly?\n• Lie factor ≈ 1.0?\n• No cherry-picking?",
         "#1565C0"),
        (0.75, 0.72, "2. VISUAL ENCODING",
         "• Best channel for each variable?\n• Cleveland ranking respected?\n• Appropriate chart type?\n• Colour palette correct?",
         "#2E7D32"),
        (0.25, 0.28, "3. DESIGN CRAFT",
         "• Typographic hierarchy clear?\n• Data-ink ratio high?\n• Whitespace adequate?\n• Consistent style?",
         "#E65100"),
        (0.75, 0.28, "4. COMMUNICATION",
         "• Clear title states the finding?\n• Audience appropriate?\n• Annotations guide reading?\n• Actionable insight?",
         "#7B1FA2"),
    ]
    
    for cx, cy, title, items, color in quadrants:
        ax.add_patch(FancyBboxPatch((cx - 0.23, cy - 0.18), 0.46, 0.36,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.08,
                     edgecolor=color, linewidth=2))
        ax.text(cx, cy + 0.12, title, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)
        ax.text(cx, cy - 0.04, items, ha="center", va="center",
                fontsize=7.5, color="#444", linespacing=1.5)
    
    # Centre label
    ax.add_patch(FancyBboxPatch((0.38, 0.44), 0.24, 0.12,
                 boxstyle="round,pad=0.02", facecolor="white",
                 edgecolor="#333", linewidth=2))
    ax.text(0.5, 0.5, "CRITIQUE\nRUBRIC", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#333")
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("The Four-Quadrant Critique Framework",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/critique_framework.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 2. BEFORE/AFTER: 3D exploding pie → horizontal bar
# ================================================================
def fig_redesign_pie():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    labels = ["Marketing", "Engineering", "Sales", "Support", "R&D", "HR", "Legal"]
    sizes = [22, 28, 18, 12, 10, 6, 4]
    
    # BEFORE: 3D exploding pie
    explode = [0.05]*7
    ax1.pie(sizes, explode=explode, labels=labels, autopct="%1.0f%%",
            shadow=True, startangle=90,
            colors=["#FF6B6B","#4ECDC4","#FFE66D","#A8E6CF","#DDA0DD","#87CEEB","#F0E68C"],
            textprops={"fontsize": 7})
    ax1.set_title("BEFORE: 3D Exploding Pie\n7 categories, shadow, explosion",
                  fontsize=9, fontweight="bold", color="#C62828")
    
    # AFTER: sorted horizontal bar
    idx = np.argsort(sizes)
    s_labels = [labels[i] for i in idx]
    s_sizes = [sizes[i] for i in idx]
    
    ax2.barh(s_labels, s_sizes, color="#1565C0", height=0.55, edgecolor="none")
    for i, v in enumerate(s_sizes):
        ax2.text(v + 0.3, i, f"{v}%", va="center", fontsize=9, fontweight="bold", color="#333")
    ax2.set_xlabel("Budget Share (%)", fontsize=9)
    ax2.set_title("AFTER: Sorted Horizontal Bar\nDirect labels, no legend needed",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="x", alpha=0.15)
    ax2.tick_params(labelsize=8)
    
    fig.suptitle("Redesign 1: Pie → Bar", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/redesign_pie.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 3. BEFORE/AFTER: Dual-axis line → indexed line
# ================================================================
def fig_redesign_dual_axis():
    np.random.seed(11)
    months = np.arange(1, 13)
    revenue = np.cumsum(np.random.normal(5, 8, 12)) + 200
    users = np.cumsum(np.random.normal(50, 80, 12)) + 1000
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # BEFORE: dual y-axis (misleading correlation)
    color1, color2 = "#1565C0", "#E53935"
    ax1.plot(months, revenue, color=color1, linewidth=2, label="Revenue ($K)")
    ax1.set_ylabel("Revenue ($K)", color=color1, fontsize=9)
    ax1.tick_params(axis="y", labelcolor=color1, labelsize=7)
    ax1b = ax1.twinx()
    ax1b.plot(months, users, color=color2, linewidth=2, label="Users")
    ax1b.set_ylabel("Users", color=color2, fontsize=9)
    ax1b.tick_params(axis="y", labelcolor=color2, labelsize=7)
    ax1.set_title("BEFORE: Dual Y-Axis\nImplied correlation is misleading",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_xlabel("Month", fontsize=8)
    
    # AFTER: indexed to 100 at month 1
    rev_idx = revenue / revenue[0] * 100
    usr_idx = users / users[0] * 100
    
    ax2.plot(months, rev_idx, color="#1565C0", linewidth=2)
    ax2.plot(months, usr_idx, color="#E53935", linewidth=2)
    ax2.text(12.2, rev_idx[-1], "Revenue", fontsize=8, fontweight="bold",
             color="#1565C0", va="center")
    ax2.text(12.2, usr_idx[-1], "Users", fontsize=8, fontweight="bold",
             color="#E53935", va="center")
    ax2.axhline(y=100, color="#888", linewidth=0.8, linestyle="--")
    ax2.set_xlim(1, 14)
    ax2.set_ylabel("Indexed (Month 1 = 100)", fontsize=9)
    ax2.set_xlabel("Month", fontsize=8)
    ax2.set_title("AFTER: Indexed Lines\nCommon scale, honest comparison",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Redesign 2: Dual Axis → Indexed Lines", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/redesign_dual_axis.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 4. BEFORE/AFTER: Spaghetti lines → small multiples
# ================================================================
def fig_redesign_spaghetti():
    np.random.seed(33)
    months = np.arange(1, 13)
    regions = ["North", "South", "East", "West", "Central", "Coastal"]
    colors_all = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b"]
    
    data = {}
    for r in regions:
        data[r] = np.cumsum(np.random.normal(2, 6, 12)) + np.random.uniform(30, 80)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    # BEFORE: spaghetti
    ax = axes[0]
    for (r, d), c in zip(data.items(), colors_all):
        ax.plot(months, d, color=c, linewidth=1.5, label=r)
    ax.legend(fontsize=6, ncol=2, frameon=True, loc="upper left")
    ax.set_title("BEFORE: Spaghetti Lines\n6 overlapping series, legend required",
                 fontsize=9, fontweight="bold", color="#C62828")
    ax.set_xlabel("Month", fontsize=8)
    ax.set_ylabel("Revenue ($K)", fontsize=8)
    ax.tick_params(labelsize=7)
    
    # AFTER: small multiples (simulated as 2x3 inset)
    ax = axes[1]
    ax.axis("off")
    ax.set_title("AFTER: Small Multiples\nOne panel per region, shared scale",
                 fontsize=9, fontweight="bold", color="#1565C0")
    
    inner_gs = GridSpec(2, 3, left=0.55, right=0.98, bottom=0.12, top=0.82,
                        hspace=0.45, wspace=0.3, figure=fig)
    
    y_min = min(min(d) for d in data.values()) - 5
    y_max = max(max(d) for d in data.values()) + 5
    
    for i, (r, d) in enumerate(data.items()):
        row, col = divmod(i, 3)
        ax_sm = fig.add_subplot(inner_gs[row, col])
        ax_sm.plot(months, d, color="#1565C0", linewidth=1.2)
        ax_sm.fill_between(months, d, alpha=0.06, color="#1565C0")
        ax_sm.set_title(r, fontsize=7, fontweight="bold", pad=2)
        ax_sm.set_ylim(y_min, y_max)
        ax_sm.set_xticks([1, 6, 12])
        ax_sm.set_xticklabels(["J", "J", "D"], fontsize=5)
        ax_sm.tick_params(labelsize=5)
        ax_sm.spines["top"].set_visible(False)
        ax_sm.spines["right"].set_visible(False)
    
    fig.suptitle("Redesign 3: Spaghetti → Small Multiples", fontsize=12, fontweight="bold")
    fig.savefig(f"{OUT}/redesign_spaghetti.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 5. BEFORE/AFTER: Cluttered scatter → grey-accent scatter
# ================================================================
def fig_redesign_scatter():
    np.random.seed(55)
    n = 120
    x = np.random.uniform(10, 100, n)
    y = 0.4 * x + np.random.normal(0, 12, n)
    cats = np.random.choice(["A","B","C","D","E"], n)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # BEFORE: all categories coloured
    palette = {"A":"#1f77b4","B":"#ff7f0e","C":"#2ca02c","D":"#d62728","E":"#9467bd"}
    for c in ["A","B","C","D","E"]:
        mask = cats == c
        ax1.scatter(x[mask], y[mask], c=palette[c], s=25, alpha=0.6, label=c)
    ax1.legend(fontsize=7, title="Cat", title_fontsize=7)
    ax1.set_title("BEFORE: All Categories Coloured\n(no visual hierarchy)",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_xlabel("Spend ($K)", fontsize=8)
    ax1.set_ylabel("ROI (%)", fontsize=8)
    ax1.tick_params(labelsize=7)
    
    # AFTER: grey + accent on category D
    mask_d = cats == "D"
    ax2.scatter(x[~mask_d], y[~mask_d], c="#CCCCCC", s=18, alpha=0.3,
                edgecolors="none", label="Other")
    ax2.scatter(x[mask_d], y[mask_d], c="#E53935", s=50, alpha=0.85,
                edgecolors="white", linewidth=0.5, zorder=5, label="Category D")
    # Add regression line for D only
    mask_arr = mask_d
    m, b = np.polyfit(x[mask_arr], y[mask_arr], 1)
    xs = np.linspace(10, 100, 50)
    ax2.plot(xs, m*xs + b, color="#E53935", linewidth=1.2, linestyle="--", alpha=0.7)
    ax2.legend(fontsize=7)
    ax2.set_title("AFTER: Grey + Accent on Category D\n(clear focus, regression visible)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.set_xlabel("Spend ($K)", fontsize=8)
    ax2.set_ylabel("ROI (%)", fontsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Redesign 4: Rainbow Scatter → Grey + Accent", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/redesign_scatter.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 6. BEFORE/AFTER: Truncated axis bar → honest bar
# ================================================================
def fig_redesign_truncated():
    years = ["2020", "2021", "2022", "2023", "2024"]
    vals = [96.2, 97.1, 97.8, 98.3, 99.0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # BEFORE: truncated
    ax1.bar(years, vals, color="#E53935", width=0.5)
    ax1.set_ylim(95, 100)
    ax1.set_title("BEFORE: Truncated Axis\n\"Massive growth!\" (Lie Factor ≈ 17)",
                  fontsize=9, fontweight="bold", color="#C62828")
    ax1.set_ylabel("Score", fontsize=8)
    ax1.tick_params(labelsize=7)
    
    # AFTER: full axis + annotation
    ax2.bar(years, vals, color="#1565C0", width=0.5)
    ax2.set_ylim(0, 110)
    for i, v in enumerate(vals):
        ax2.text(i, v + 1.5, f"{v}", ha="center", fontsize=8, color="#333")
    ax2.axhline(y=vals[0], color="#888", linewidth=0.8, linestyle="--")
    ax2.text(4.4, vals[0], f"Baseline:\n{vals[0]}", fontsize=7, va="center", color="#888")
    ax2.set_title("AFTER: Full Axis + Baseline\n\"Steady improvement\" (Lie Factor ≈ 1.0)",
                  fontsize=9, fontweight="bold", color="#1565C0")
    ax2.set_ylabel("Score", fontsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.tick_params(labelsize=7)
    
    fig.suptitle("Redesign 5: Truncated Axis → Honest Baseline", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/redesign_truncated.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 7. PEER REVIEW PROTOCOL — checklist card
# ================================================================
def fig_peer_review():
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.axis("off")
    
    steps = [
        ("1", "First Impression (5 sec)", "What do you see first?\nWhat is the main message?", "#1565C0"),
        ("2", "Data Integrity Check", "Verify axes, scales, labels.\nCalculate lie factor if suspicious.", "#2E7D32"),
        ("3", "Encoding Audit", "Is each variable on the best channel?\nWould a different chart work better?", "#E65100"),
        ("4", "Design Craft Review", "Data-ink ratio? Chartjunk?\nTypography? Whitespace?", "#7B1FA2"),
        ("5", "Communication Test", "Can a non-expert understand in 30 sec?\nIs there a clear takeaway?", "#C62828"),
    ]
    
    for i, (num, title, desc, color) in enumerate(steps):
        y = 0.88 - i * 0.17
        ax.add_patch(FancyBboxPatch((0.02, y - 0.06), 0.06, 0.12,
                     boxstyle="round,pad=0.01", facecolor=color, edgecolor="none"))
        ax.text(0.05, y, num, ha="center", va="center", fontsize=13,
                fontweight="bold", color="white")
        ax.text(0.12, y + 0.025, title, fontsize=10, fontweight="bold",
                va="center", color="#222")
        ax.text(0.12, y - 0.03, desc, fontsize=7.5, va="center", color="#555",
                linespacing=1.4)
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Peer Review Protocol: 5-Step Critique",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(f"{OUT}/peer_review.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 8. REDESIGN WORKFLOW — diagram
# ================================================================
def fig_redesign_workflow():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis("off")
    
    steps = [
        ("Identify\nProblem", "#C62828"),
        ("Diagnose\n(which quadrant?)", "#E65100"),
        ("Sketch\nAlternative", "#1565C0"),
        ("Implement\nin Code", "#2E7D32"),
        ("Validate\n(peer review)", "#7B1FA2"),
    ]
    
    for i, (label, color) in enumerate(steps):
        x = 0.08 + i * 0.18
        ax.add_patch(FancyBboxPatch((x, 0.2), 0.14, 0.6,
                     boxstyle="round,pad=0.02", facecolor=color, alpha=0.12,
                     edgecolor=color, linewidth=2))
        ax.text(x + 0.07, 0.5, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color, linespacing=1.3)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.16, 0.5), xytext=(x + 0.18, 0.5),
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("The Redesign Workflow", fontsize=12, fontweight="bold", pad=10)
    plt.tight_layout()
    fig.savefig(f"{OUT}/redesign_workflow.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 9. R output — redesigned bar
# ================================================================
def fig_r_redesign():
    cats = ["HR", "Legal", "R&D", "Support", "Sales", "Marketing", "Engineering"]
    vals = [6, 4, 10, 12, 18, 22, 28]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    colors = ["#1565C0"] * 7
    colors[-1] = "#E53935"
    ax.barh(cats, vals, color=colors, height=0.55, edgecolor="none")
    for i, v in enumerate(vals):
        ax.text(v + 0.3, i, f"{v}%", va="center", fontsize=8,
                fontweight="bold", color="#E53935" if i == 6 else "#333")
    ax.set_title("ggplot2 redesign: sorted + accent on max",
                 fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(left=False, labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/r_redesign.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# 10. Python output — redesigned indexed lines
# ================================================================
def fig_py_redesign():
    np.random.seed(11)
    months = np.arange(1, 13)
    revenue = np.cumsum(np.random.normal(5, 8, 12)) + 200
    users = np.cumsum(np.random.normal(50, 80, 12)) + 1000
    rev_idx = revenue / revenue[0] * 100
    usr_idx = users / users[0] * 100
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(months, rev_idx, color="#1565C0", linewidth=2)
    ax.plot(months, usr_idx, color="#E53935", linewidth=2)
    ax.text(12.2, rev_idx[-1], "Revenue", fontsize=8, fontweight="bold",
            color="#1565C0", va="center")
    ax.text(12.2, usr_idx[-1], "Users", fontsize=8, fontweight="bold",
            color="#E53935", va="center")
    ax.axhline(y=100, color="#888", linewidth=0.8, linestyle="--")
    ax.set_xlim(1, 14)
    ax.set_ylabel("Index (M1 = 100)", fontsize=8)
    ax.set_title("matplotlib redesign: indexed lines",
                 fontsize=9, fontstyle="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    fig.savefig(f"{OUT}/py_redesign.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
if __name__ == "__main__":
    funcs = [
        ("critique_framework", fig_critique_framework),
        ("redesign_pie", fig_redesign_pie),
        ("redesign_dual_axis", fig_redesign_dual_axis),
        ("redesign_spaghetti", fig_redesign_spaghetti),
        ("redesign_scatter", fig_redesign_scatter),
        ("redesign_truncated", fig_redesign_truncated),
        ("peer_review", fig_peer_review),
        ("redesign_workflow", fig_redesign_workflow),
        ("r_redesign", fig_r_redesign),
        ("py_redesign", fig_py_redesign),
    ]
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    print(f"\nAll M07 figures saved to {OUT}/")
