"""
Generate ALL figures for Workshop 1, Module 1 Beamer slides.
Each figure is saved as PDF (vector) for crisp LaTeX embedding.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.ticker as ticker
import seaborn as sns
from math import pi, sqrt
import warnings
warnings.filterwarnings("ignore")

OUT = "/home/claude/figures"
sns.set_theme(style="whitegrid", font_scale=0.9)

# ================================================================
# 1. DATA GROWTH INFOGRAPHIC
# ================================================================
def fig_data_growth():
    years = np.arange(2010, 2026)
    zettabytes = [2, 2.8, 4, 5.5, 7.5, 10, 13, 18, 26, 33, 41, 59, 74, 97, 120, 147]
    
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    ax.fill_between(years, zettabytes, alpha=0.3, color="#1565C0")
    ax.plot(years, zettabytes, color="#1565C0", linewidth=2.5, marker="o", markersize=4)
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel("Zettabytes Created/Year", fontsize=9)
    ax.set_title("Global Data Creation", fontsize=11, fontweight="bold")
    ax.annotate("147 ZB\n(projected)", xy=(2025, 147), fontsize=8,
                ha="center", va="bottom", color="#C62828", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    fig.savefig(f"{OUT}/data_growth.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 2. GROUPED BAR CHART (table vs chart comparison)
# ================================================================
def fig_grouped_bar():
    regions = ["North", "South", "East", "West"]
    q1 = [142, 98, 205, 167]
    q2 = [189, 115, 178, 201]
    
    x = np.arange(len(regions))
    w = 0.35
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    bars1 = ax.bar(x - w/2, q1, w, label="Q1", color="#1565C0", edgecolor="white")
    bars2 = ax.bar(x + w/2, q2, w, label="Q2", color="#E53935", edgecolor="white")
    
    ax.set_xticks(x)
    ax.set_xticklabels(regions, fontsize=9)
    ax.set_ylabel("Sales", fontsize=9)
    ax.set_title("Regional Sales: Q1 vs Q2", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    
    for bars in [bars1, bars2]:
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 3,
                    str(int(b.get_height())), ha="center", va="bottom", fontsize=7)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/grouped_bar.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 3. NIGHTINGALE COXCOMB DIAGRAM
# ================================================================
def fig_coxcomb():
    """
    Recreation of Nightingale's polar-area (coxcomb) diagram.
    Data: monthly deaths in the Crimean War (1854-1855)
    Three causes: preventable disease, wounds, other.
    """
    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    
    # Approximate Crimean War mortality data (per 1000)
    # Source: reconstructed from Nightingale's original
    disease = [1, 12, 11, 359, 828, 788, 503, 844, 1725, 2761, 2120, 1205]
    wounds  = [0, 0, 0, 0, 20, 32, 122, 104, 131, 83, 42, 32]
    other   = [5, 9, 11, 7, 30, 29, 25, 15, 46, 57, 37, 31]
    
    N = len(months)
    theta = np.linspace(0, 2*pi, N, endpoint=False)
    width = 2*pi / N
    
    # Convert to radii (area ∝ value, so radius ∝ sqrt(value))
    scale = 0.015
    r_disease = np.sqrt(np.array(disease) * scale)
    r_wounds  = np.sqrt(np.array(wounds) * scale)
    r_other   = np.sqrt(np.array(other) * scale)
    
    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw={"projection": "polar"})
    
    # Plot from largest to smallest so smaller wedges are visible
    ax.bar(theta, r_disease, width=width, bottom=0,
           color="#5C9BD5", alpha=0.7, edgecolor="white", linewidth=0.5,
           label="Preventable Disease")
    ax.bar(theta, r_wounds, width=width, bottom=0,
           color="#ED7D7D", alpha=0.8, edgecolor="white", linewidth=0.5,
           label="Battle Wounds")
    ax.bar(theta, r_other, width=width, bottom=0,
           color="#333333", alpha=0.6, edgecolor="white", linewidth=0.5,
           label="Other Causes")
    
    # Month labels
    ax.set_xticks(theta)
    ax.set_xticklabels(months, fontsize=8, fontweight="bold")
    
    # Remove radial tick labels for clean look
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Title and legend
    ax.set_title("Nightingale's Coxcomb Diagram\n"
                 "Causes of Mortality in the Crimean War (1854–55)",
                 fontsize=10, fontweight="bold", pad=20)
    ax.legend(loc="lower right", bbox_to_anchor=(1.3, 0), fontsize=7,
              frameon=True, fancybox=True, shadow=False)
    
    # Start from the top (12 o'clock)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/coxcomb.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 4. MINARD'S MARCH (simplified recreation)
# ================================================================
def fig_minard():
    """
    Simplified recreation of Minard's Napoleon's March map.
    Uses the classic city coordinates and troop counts.
    """
    # Advance (tan/gold) — city positions and troop counts (thousands)
    adv_lon  = [24.0, 24.5, 25.5, 26.0, 27.0, 28.0, 28.5, 29.0, 30.0,
                31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 37.6]
    adv_lat  = [54.9, 55.0, 54.5, 54.7, 54.8, 54.9, 55.0, 55.1, 55.2,
                55.3, 54.8, 54.9, 55.1, 55.2, 55.5, 55.7, 55.8]
    adv_size = [422, 400, 380, 350, 320, 300, 280, 250, 220,
                200, 180, 160, 145, 130, 120, 110, 100]
    
    # Retreat (black) — fewer stops, dramatic attrition
    ret_lon  = [37.6, 36.0, 35.0, 33.5, 32.0, 30.5, 29.0, 27.5, 26.0, 24.0]
    ret_lat  = [55.8, 55.3, 55.0, 54.5, 54.3, 54.1, 54.0, 54.2, 54.4, 54.9]
    ret_size = [100, 55, 37, 24, 20, 18, 15, 12, 10, 10]
    
    fig, ax = plt.subplots(figsize=(7, 3))
    
    # Scale line widths
    max_width = 30
    
    # Draw advance (tan)
    for i in range(len(adv_lon) - 1):
        lw = adv_size[i] / max(adv_size) * max_width
        ax.plot([adv_lon[i], adv_lon[i+1]], [adv_lat[i], adv_lat[i+1]],
                color="#C5A059", linewidth=lw, solid_capstyle="round", alpha=0.85)
    
    # Draw retreat (black)
    for i in range(len(ret_lon) - 1):
        lw = ret_size[i] / max(adv_size) * max_width
        ax.plot([ret_lon[i], ret_lon[i+1]], [ret_lat[i], ret_lat[i+1]],
                color="#2C2C2C", linewidth=lw, solid_capstyle="round", alpha=0.85)
    
    # City labels
    cities = {
        "Kaunas": (24.0, 54.9), "Vilna": (25.5, 54.5),
        "Vitebsk": (30.0, 55.2), "Smolensk": (32.0, 54.8),
        "Moscow": (37.6, 55.8), "Minsk": (27.5, 54.2),
    }
    for city, (lon, lat) in cities.items():
        ax.annotate(city, (lon, lat), fontsize=7, ha="center", va="bottom",
                    fontweight="bold", color="#333333",
                    xytext=(0, 5), textcoords="offset points")
        ax.plot(lon, lat, "ko", markersize=3)
    
    # Annotations
    ax.annotate("422,000", (24.0, 55.15), fontsize=6, color="#8B6914", ha="center")
    ax.annotate("100,000", (37.6, 56.05), fontsize=6, color="#555", ha="center")
    ax.annotate("10,000", (24.0, 54.6), fontsize=6, color="#2C2C2C", ha="center")
    
    ax.set_xlim(23, 39)
    ax.set_ylim(53.5, 56.5)
    ax.set_title("Minard's Map: Napoleon's Russian Campaign (1812–13)",
                 fontsize=10, fontweight="bold")
    ax.set_xlabel("Longitude", fontsize=8)
    ax.set_ylabel("Latitude", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # Legend patches
    adv_patch = mpatches.Patch(color="#C5A059", label="Advance (422K → 100K)")
    ret_patch = mpatches.Patch(color="#2C2C2C", label="Retreat (100K → 10K)")
    ax.legend(handles=[adv_patch, ret_patch], fontsize=7, loc="lower right",
              frameon=True, fancybox=True)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/minard.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 5. SNOW'S CHOLERA MAP (simplified)
# ================================================================
def fig_cholera_map():
    """Simplified recreation of Snow's Broad Street cholera map."""
    np.random.seed(42)
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Street grid
    streets = [
        ([0, 10], [3, 3]),    # Broad Street (horizontal)
        ([0, 10], [6, 6]),    # Oxford Street
        ([2, 2], [0, 10]),    # vertical street
        ([5, 5], [0, 10]),    # vertical street
        ([8, 8], [0, 10]),    # vertical street
        ([0, 10], [0, 0]),
        ([0, 10], [9, 9]),
    ]
    for xs, ys in streets:
        ax.plot(xs, ys, color="#CCCCCC", linewidth=3, solid_capstyle="round")
    
    # Broad Street pump location
    pump_x, pump_y = 5.0, 3.0
    ax.plot(pump_x, pump_y, "s", color="#1565C0", markersize=12, zorder=5)
    ax.annotate("Broad St.\nPump", (pump_x, pump_y), fontsize=7,
                ha="center", va="bottom", fontweight="bold", color="#1565C0",
                xytext=(0, 12), textcoords="offset points")
    
    # Other pumps (fewer deaths nearby)
    other_pumps = [(1.5, 7), (8.5, 1), (8.5, 8)]
    for px, py in other_pumps:
        ax.plot(px, py, "s", color="#90CAF9", markersize=8, zorder=5)
    
    # Death locations — clustered around Broad Street pump
    n_deaths = 180
    death_x = np.random.normal(pump_x, 1.2, n_deaths).clip(0.5, 9.5)
    death_y = np.random.normal(pump_y, 1.2, n_deaths).clip(0.5, 9.5)
    
    # Add some scattered deaths further away (fewer)
    n_far = 25
    far_x = np.random.uniform(0.5, 9.5, n_far)
    far_y = np.random.uniform(0.5, 9.5, n_far)
    
    all_x = np.concatenate([death_x, far_x])
    all_y = np.concatenate([death_y, far_y])
    
    ax.scatter(all_x, all_y, c="#C62828", s=8, alpha=0.6, zorder=3,
               label=f"Deaths (n={len(all_x)})")
    
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal")
    ax.set_title("Snow's Cholera Map (1854)\nBroad Street, London (simplified)",
                 fontsize=10, fontweight="bold")
    ax.legend(fontsize=7, loc="upper right", frameon=True)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/cholera_map.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 6. DU BOIS DATA PORTRAIT (simplified spiral bar chart)
# ================================================================
def fig_dubois():
    """Simplified recreation of Du Bois's 1900 Paris Exposition style."""
    categories = [
        "Rent", "Food", "Clothing", "Tax", "Other"
    ]
    # Approximate proportions from Du Bois's household expenditure chart
    values = [19, 43, 13, 8, 17]
    colors = ["#DC143C", "#4169E1", "#DAA520", "#8B4513", "#2F4F4F"]
    
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    
    # Horizontal bar chart in Du Bois's distinctive style
    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, values, color=colors, edgecolor="black",
                   linewidth=0.8, height=0.7)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=9, fontweight="bold")
    ax.set_xlabel("Percentage of Income", fontsize=9)
    ax.set_title("Income Expenditure of\n150 African-American Families\n"
                 "(Du Bois, Paris Exposition, 1900)",
                 fontsize=10, fontweight="bold", fontstyle="italic")
    
    # Direct labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val}%", va="center", fontsize=8, fontweight="bold")
    
    ax.set_xlim(0, 55)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    ax.tick_params(labelsize=8)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/dubois.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 7. ANSCOMBE'S QUARTET — summary table
# ================================================================
def fig_anscombe_table():
    """Visual table showing Anscombe's four datasets side by side."""
    # Anscombe's data
    data = {
        "I":   {"x": [10,8,13,9,11,14,6,4,12,7,5],
                "y": [8.04,6.95,7.58,8.81,8.33,9.96,7.24,4.26,10.84,4.82,5.68]},
        "II":  {"x": [10,8,13,9,11,14,6,4,12,7,5],
                "y": [9.14,8.14,8.74,8.77,9.26,8.10,6.13,3.10,9.13,7.26,4.74]},
        "III": {"x": [10,8,13,9,11,14,6,4,12,7,5],
                "y": [7.46,6.77,12.74,7.11,7.81,8.84,6.08,5.39,8.15,6.42,5.73]},
        "IV":  {"x": [8,8,8,8,8,8,8,19,8,8,8],
                "y": [6.58,5.76,7.71,8.84,8.47,7.04,5.25,12.50,5.56,7.91,6.89]},
    }
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.axis("off")
    
    # Build table data
    headers = ["Stat", "Dataset I", "Dataset II", "Dataset III", "Dataset IV"]
    rows = []
    for ds_name, ds in data.items():
        x, y = np.array(ds["x"]), np.array(ds["y"])
        stats = {
            "Mean x": f"{np.mean(x):.1f}",
            "Mean y": f"{np.mean(y):.2f}",
            "SD x":   f"{np.std(x, ddof=1):.2f}",
            "SD y":   f"{np.std(y, ddof=1):.2f}",
            "r":      f"{np.corrcoef(x, y)[0,1]:.3f}",
        }
        if not rows:
            rows = [[k] for k in stats.keys()]
        for i, v in enumerate(stats.values()):
            rows[i].append(v)
    
    table = ax.table(cellText=rows, colLabels=headers,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.5)
    
    # Style header row
    for j in range(len(headers)):
        table[0, j].set_facecolor("#1565C0")
        table[0, j].set_text_props(color="white", fontweight="bold")
    
    # Alternate row colors
    for i in range(1, len(rows) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[i, j].set_facecolor("#E3F2FD")
    
    ax.set_title("Anscombe's Quartet: Identical Summary Statistics",
                 fontsize=11, fontweight="bold", pad=20)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/anscombe_table.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 8. ANSCOMBE'S QUARTET — 2×2 scatterplots
# ================================================================
def fig_anscombe_scatter():
    df = sns.load_dataset("anscombe")
    
    g = sns.lmplot(data=df, x="x", y="y", col="dataset", col_wrap=2,
                   ci=None, height=2.8, aspect=1.1,
                   scatter_kws={"s": 40, "color": "#1565C0", "edgecolor": "white", "linewidth": 0.5},
                   line_kws={"color": "#E53935", "linewidth": 1.5})
    g.set_titles("Dataset {col_name}", fontweight="bold", fontsize=10)
    g.figure.suptitle("Anscombe's Quartet — Visualized",
                      fontsize=12, fontweight="bold", y=1.03)
    plt.tight_layout()
    g.savefig(f"{OUT}/anscombe_scatter.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 9. ANSCOMBE — R-style output (simulate ggplot2 look)
# ================================================================
def fig_anscombe_r_style():
    """Simulate ggplot2 minimal theme output for the R slide."""
    df = sns.load_dataset("anscombe")
    
    fig, axes = plt.subplots(2, 2, figsize=(5, 4))
    datasets = ["I", "II", "III", "IV"]
    
    for ax, ds in zip(axes.flatten(), datasets):
        sub = df[df["dataset"] == ds]
        ax.scatter(sub["x"], sub["y"], s=35, c="#1565C0", edgecolor="white", linewidth=0.5)
        # Regression line
        m, b = np.polyfit(sub["x"], sub["y"], 1)
        xs = np.linspace(sub["x"].min(), sub["x"].max(), 50)
        ax.plot(xs, m*xs + b, color="#4682B4", linewidth=1.2)
        ax.set_title(f"Dataset {ds}", fontsize=8, fontweight="bold")
        ax.tick_params(labelsize=6)
        ax.set_facecolor("#FAFAFA")
        ax.grid(True, alpha=0.3)
    
    fig.suptitle("ggplot2 output: facet_wrap(~set)", fontsize=9, fontstyle="italic")
    plt.tight_layout()
    fig.savefig(f"{OUT}/anscombe_r_output.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 10. ANSCOMBE — Python-style output (seaborn look)
# ================================================================
def fig_anscombe_py_style():
    """Seaborn lmplot for the Python slide."""
    df = sns.load_dataset("anscombe")
    g = sns.lmplot(data=df, x="x", y="y", col="dataset", col_wrap=2,
                   ci=None, height=2.5, aspect=1.0,
                   scatter_kws={"s": 35, "color": "#2E7D32"},
                   line_kws={"color": "#E53935", "linewidth": 1.2})
    g.set_titles("Dataset {col_name}", fontsize=9)
    g.figure.suptitle("seaborn output: sns.lmplot()", fontsize=9, fontstyle="italic", y=1.02)
    plt.tight_layout()
    g.savefig(f"{OUT}/anscombe_py_output.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 11. DATASAURUS DOZEN — full grid
# ================================================================
def fig_datasaurus():
    """Generate the Datasaurus Dozen grid. Uses local synthetic data."""
    np.random.seed(2017)
    
    # Create synthetic datasets that mimic the Datasaurus shapes
    n = 142
    base_x, base_y = 54.26, 47.83
    
    datasets = {}
    
    # Dino (rough T-rex shape)
    t = np.linspace(0, 2*pi, n)
    dx = 16 * np.sin(t) * np.abs(np.sin(t * 2.5))
    dy = 26 * np.cos(t) * np.abs(np.cos(t * 1.5))
    datasets["dino"] = (base_x + dx + np.random.normal(0, 2, n),
                        base_y + dy + np.random.normal(0, 2, n))
    
    # Circle
    datasets["circle"] = (base_x + 16*np.cos(t) + np.random.normal(0, 1, n),
                          base_y + 26*np.sin(t) + np.random.normal(0, 1, n))
    
    # Star
    r = 16 + 8*np.sin(5*t)
    datasets["star"] = (base_x + r*np.cos(t) + np.random.normal(0, 1.5, n),
                        base_y + r*np.sin(t)*1.5 + np.random.normal(0, 1.5, n))
    
    # X shape
    half = n // 2
    datasets["x_shape"] = (
        np.concatenate([np.linspace(base_x-16, base_x+16, half),
                        np.linspace(base_x-16, base_x+16, n-half)]) + np.random.normal(0, 2, n),
        np.concatenate([np.linspace(base_y-26, base_y+26, half),
                        np.linspace(base_y+26, base_y-26, n-half)]) + np.random.normal(0, 2, n)
    )
    
    # H lines
    third = n // 3
    datasets["h_lines"] = (
        np.random.uniform(base_x-16, base_x+16, n),
        np.concatenate([np.full(third, base_y-20) + np.random.normal(0, 1, third),
                        np.full(third, base_y) + np.random.normal(0, 1, third),
                        np.full(n-2*third, base_y+20) + np.random.normal(0, 1, n-2*third)])
    )
    
    # V lines
    datasets["v_lines"] = (
        np.concatenate([np.full(third, base_x-12) + np.random.normal(0, 1, third),
                        np.full(third, base_x) + np.random.normal(0, 1, third),
                        np.full(n-2*third, base_x+12) + np.random.normal(0, 1, n-2*third)]),
        np.random.uniform(base_y-26, base_y+26, n)
    )
    
    # Dots (single cluster)
    datasets["dots"] = (base_x + np.random.normal(0, 3, n),
                        base_y + np.random.normal(0, 4, n))
    
    # Wide lines
    datasets["wide_lines"] = (
        np.concatenate([np.full(n//2, base_x-10) + np.random.normal(0, 1, n//2),
                        np.full(n - n//2, base_x+10) + np.random.normal(0, 1, n-n//2)]),
        np.random.uniform(base_y-26, base_y+26, n)
    )
    
    # Bullseye
    r_inner = np.random.uniform(0, 8, n//2)
    r_outer = np.random.uniform(14, 18, n - n//2)
    theta_i = np.random.uniform(0, 2*pi, n//2)
    theta_o = np.random.uniform(0, 2*pi, n - n//2)
    datasets["bullseye"] = (
        np.concatenate([base_x + r_inner*np.cos(theta_i), base_x + r_outer*np.cos(theta_o)]),
        np.concatenate([base_y + r_inner*np.sin(theta_i)*1.5, base_y + r_outer*np.sin(theta_o)*1.5])
    )
    
    # Slant up
    datasets["slant_up"] = (
        np.linspace(base_x-16, base_x+16, n) + np.random.normal(0, 3, n),
        np.linspace(base_y-26, base_y+26, n) + np.random.normal(0, 5, n)
    )
    
    # Slant down
    datasets["slant_down"] = (
        np.linspace(base_x-16, base_x+16, n) + np.random.normal(0, 3, n),
        np.linspace(base_y+26, base_y-26, n) + np.random.normal(0, 5, n)
    )
    
    # High lines
    fifth = n // 5
    datasets["high_lines"] = (
        np.random.uniform(base_x-16, base_x+16, n),
        np.concatenate([np.full(fifth, base_y + i*10 - 20) + np.random.normal(0, 0.8, fifth)
                        for i in range(5)][:n])[:n]
    )
    
    # Away
    datasets["away"] = (
        base_x + np.random.normal(0, 16, n),
        base_y + np.random.normal(0, 26, n)
    )
    
    # Plot
    names = list(datasets.keys())
    ncols = 5
    nrows = 3
    fig, axes = plt.subplots(nrows, ncols, figsize=(11, 6.5))
    
    for i, (name, (x, y)) in enumerate(datasets.items()):
        if i >= nrows * ncols:
            break
        r, c = divmod(i, ncols)
        ax = axes[r][c]
        ax.scatter(x, y, s=3, alpha=0.5, c="#2E7D32", edgecolors="none")
        ax.set_title(name.replace("_", " "), fontsize=7, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(base_x - 30, base_x + 30)
        ax.set_ylim(base_y - 40, base_y + 40)
    
    # Hide leftover subplots
    for j in range(len(datasets), nrows * ncols):
        r, c = divmod(j, ncols)
        axes[r][c].set_visible(False)
    
    fig.suptitle("The Datasaurus Dozen — Same Stats, Different Graphs\n"
                 "(μx ≈ 54.3, μy ≈ 47.8, σx ≈ 16.8, σy ≈ 26.9, r ≈ −0.06)",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/datasaurus.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 12. CHART JUNK EXAMPLE
# ================================================================
def fig_chartjunk():
    """Create a deliberately bad chart to illustrate chartjunk."""
    categories = ["Product A", "Product B", "Product C", "Product D"]
    values = [45, 38, 52, 41]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Garish colors, 3D-like bars with shadows
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A8E6CF"]
    bars = ax.bar(categories, values, color=colors, edgecolor="black",
                  linewidth=2, width=0.6)
    
    # Add fake 3D shadow
    for bar, val in zip(bars, values):
        x = bar.get_x()
        w = bar.get_width()
        h = bar.get_height()
        shadow = plt.Rectangle((x + 0.08, 0), w, h, 
                               color="gray", alpha=0.3, zorder=0)
        ax.add_patch(shadow)
    
    # Heavy gridlines
    ax.grid(True, which="both", linewidth=1.5, color="gray", alpha=0.7)
    ax.set_facecolor("#F0E68C")
    
    # Excessive decoration
    ax.set_title("📊 QUARTERLY SALES REPORT 📊\n★ ★ ★ AMAZING RESULTS ★ ★ ★",
                 fontsize=12, fontweight="bold", color="red")
    ax.set_ylabel("UNITS SOLD!!!", fontsize=11, fontweight="bold", color="blue")
    
    # Rotated labels
    ax.set_xticklabels(categories, rotation=45, ha="right", fontsize=10,
                       fontweight="bold", color="purple")
    
    # Unnecessary annotations everywhere
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"${val}K!!!", ha="center", fontsize=9, fontweight="bold",
                color="red", fontstyle="italic")
    
    ax.set_ylim(0, 65)
    fig.patch.set_facecolor("#FFFACD")
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/chartjunk.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 13. BEFORE / AFTER — cluttered vs clean
# ================================================================
def fig_before_after():
    categories = ["Compact", "Midsize", "SUV", "Pickup", "Minivan", "Subcompact", "2seater"]
    values = [47, 41, 62, 33, 11, 35, 5]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # BEFORE — cluttered
    colors_bad = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A8E6CF", "#DDA0DD", "#87CEEB", "#F0E68C"]
    ax1.bar(categories, values, color=colors_bad, edgecolor="black", linewidth=1.5)
    ax1.grid(True, linewidth=1, color="gray")
    ax1.set_facecolor("#F5F5DC")
    ax1.set_xticklabels(categories, rotation=60, ha="right", fontsize=7)
    ax1.set_title("BEFORE: Cluttered Design", fontsize=10, fontweight="bold",
                  color="#C62828")
    ax1.set_ylabel("Count", fontsize=9)
    
    # AFTER — clean
    sorted_idx = np.argsort(values)
    sorted_cats = [categories[i] for i in sorted_idx]
    sorted_vals = [values[i] for i in sorted_idx]
    
    ax2.barh(sorted_cats, sorted_vals, color="#1565C0", height=0.65,
             edgecolor="white", linewidth=0.5)
    for i, v in enumerate(sorted_vals):
        ax2.text(v + 0.8, i, str(v), va="center", fontsize=8, color="#333")
    ax2.set_title("AFTER: Clean Redesign", fontsize=10, fontweight="bold",
                  color="#1565C0")
    ax2.set_xlabel("Count", fontsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="x", alpha=0.2)
    ax2.tick_params(labelsize=8)
    
    fig.suptitle("Data-Ink Ratio: Before & After", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/before_after.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 14. LIE FACTOR ILLUSTRATION
# ================================================================
def fig_lie_factor():
    """Show a truncated y-axis creating a visual lie."""
    years = ["2021", "2022", "2023", "2024"]
    values = [98.0, 99.2, 100.5, 101.0]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Misleading (truncated axis)
    ax1.bar(years, values, color="#E53935", width=0.5, edgecolor="white")
    ax1.set_ylim(97, 102)
    ax1.set_title("Misleading: Truncated Axis\n(Lie Factor ≈ 10×)", 
                  fontsize=10, fontweight="bold", color="#C62828")
    ax1.set_ylabel("Revenue ($B)", fontsize=9)
    for i, v in enumerate(values):
        ax1.text(i, v + 0.1, f"${v}B", ha="center", fontsize=8)
    
    # Honest (full axis)
    ax2.bar(years, values, color="#1565C0", width=0.5, edgecolor="white")
    ax2.set_ylim(0, 120)
    ax2.set_title("Honest: Full Axis\n(Lie Factor ≈ 1.0)", 
                  fontsize=10, fontweight="bold", color="#1565C0")
    ax2.set_ylabel("Revenue ($B)", fontsize=9)
    for i, v in enumerate(values):
        ax2.text(i, v + 1.5, f"${v}B", ha="center", fontsize=8)
    
    fig.suptitle("The Lie Factor: Truncated Axes Distort Perception",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{OUT}/lie_factor.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 15. MPG SCATTERPLOT — R style
# ================================================================
def fig_mpg_r():
    mpg = sns.load_dataset("mpg").dropna()
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    classes = mpg["origin"].unique()
    palette = {"usa": "#E53935", "europe": "#1565C0", "japan": "#2E7D32"}
    
    for cls in classes:
        sub = mpg[mpg["origin"] == cls]
        ax.scatter(sub["displacement"], sub["mpg"], s=30, alpha=0.6,
                   label=cls.title(), color=palette.get(cls, "gray"),
                   edgecolor="white", linewidth=0.3)
    
    ax.set_xlabel("Engine Displacement (L)", fontsize=9)
    ax.set_ylabel("Highway MPG", fontsize=9)
    ax.set_title("Engine Size vs Highway MPG", fontsize=10, fontweight="bold")
    ax.legend(title="Origin", fontsize=7, title_fontsize=8, frameon=True)
    ax.set_facecolor("#FAFAFA")
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpg_r_output.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 16. MPG SCATTERPLOT — Python style
# ================================================================
def fig_mpg_py():
    mpg = sns.load_dataset("mpg").dropna()
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    sns.scatterplot(data=mpg, x="displacement", y="mpg", hue="origin",
                    alpha=0.7, s=40, palette="Set1", ax=ax)
    ax.set_title("Displacement vs MPG", fontsize=10, fontweight="bold")
    ax.set_xlabel("Displacement (cu in)", fontsize=9)
    ax.set_ylabel("Miles per Gallon", fontsize=9)
    ax.legend(title="Origin", fontsize=7, title_fontsize=8)
    ax.tick_params(labelsize=7)
    
    plt.tight_layout()
    fig.savefig(f"{OUT}/mpg_py_output.pdf", bbox_inches="tight")
    plt.close()

# ================================================================
# 17. TUFTE BOOK COVER (text-based placeholder)
# ================================================================
def fig_tufte_portrait():
    fig, ax = plt.subplots(figsize=(3.5, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_facecolor("#FFFEF5")
    
    # Book-cover style
    rect = FancyBboxPatch((0.5, 0.5), 9, 11, boxstyle="round,pad=0.3",
                          facecolor="#1A237E", edgecolor="#0D1B42", linewidth=2)
    ax.add_patch(rect)
    
    ax.text(5, 9, "THE VISUAL\nDISPLAY OF\nQUANTITATIVE\nINFORMATION",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color="white", linespacing=1.3)
    ax.text(5, 5.5, "Edward R. Tufte", ha="center", va="center",
            fontsize=10, color="#C5CAE9", fontstyle="italic")
    ax.text(5, 2, "Graphics Press\n1983", ha="center", va="center",
            fontsize=8, color="#7986CB")
    
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(f"{OUT}/tufte_book.pdf", bbox_inches="tight")
    plt.close()


# ================================================================
# GENERATE ALL FIGURES
# ================================================================
if __name__ == "__main__":
    print("Generating figures...")
    
    funcs = [
        ("data_growth", fig_data_growth),
        ("grouped_bar", fig_grouped_bar),
        ("coxcomb", fig_coxcomb),
        ("minard", fig_minard),
        ("cholera_map", fig_cholera_map),
        ("dubois", fig_dubois),
        ("anscombe_table", fig_anscombe_table),
        ("anscombe_scatter", fig_anscombe_scatter),
        ("anscombe_r_output", fig_anscombe_r_style),
        ("anscombe_py_output", fig_anscombe_py_style),
        ("datasaurus", fig_datasaurus),
        ("chartjunk", fig_chartjunk),
        ("before_after", fig_before_after),
        ("lie_factor", fig_lie_factor),
        ("mpg_r_output", fig_mpg_r),
        ("mpg_py_output", fig_mpg_py),
        ("tufte_book", fig_tufte_portrait),
    ]
    
    for name, func in funcs:
        try:
            func()
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    print(f"\nAll figures saved to {OUT}/")
