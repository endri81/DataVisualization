"""
============================================================
Workshop 1 — Module 3: Visual Perception & Pre-Attentive Attributes
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)
plt.rcParams["figure.dpi"] = 150
np.random.seed(42)


# ── 1. Pre-Attentive Pop-Out: Color ────────────────────────
n = 80
xs, ys = np.random.uniform(0, 10, n), np.random.uniform(0, 8, n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# No pop-out: uniform color
ax1.scatter(xs, ys, s=100, c="#1565C0", edgecolors="white", linewidth=0.5)
ax1.set_title("No Pop-Out\n(serial search required)", fontsize=10, fontweight="bold")
for sp in ax1.spines.values(): sp.set_visible(False)
ax1.set_xticks([]); ax1.set_yticks([])

# Pop-out: one red among blue
colors = ["#1565C0"] * n
colors[37] = "#E53935"
sizes = [100] * n
sizes[37] = 200
ax2.scatter(xs, ys, s=sizes, c=colors, edgecolors="white", linewidth=0.5)
ax2.set_title("Color Pop-Out\n(pre-attentive: <200 ms)", fontsize=10, fontweight="bold")
for sp in ax2.spines.values(): sp.set_visible(False)
ax2.set_xticks([]); ax2.set_yticks([])

fig.suptitle("Pre-Attentive Processing: Color Channel", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/preattentive_popout_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 2. Conjunction Search ──────────────────────────────────
n_c = 60
xc, yc = np.random.uniform(0.5, 9.5, n_c), np.random.uniform(0.5, 7.5, n_c)

fig, ax = plt.subplots(figsize=(6, 5))
for i in range(n_c):
    if i == 33:  # target: red square
        ax.scatter(xc[i], yc[i], s=160, c="#E53935", marker="s",
                   edgecolors="white", linewidth=0.5, zorder=5)
    elif i % 3 == 0:  # red circles (distractors)
        ax.scatter(xc[i], yc[i], s=100, c="#E53935", marker="o",
                   edgecolors="white", linewidth=0.5)
    elif i % 3 == 1:  # blue squares (distractors)
        ax.scatter(xc[i], yc[i], s=100, c="#1565C0", marker="s",
                   edgecolors="white", linewidth=0.5)
    else:  # blue circles
        ax.scatter(xc[i], yc[i], s=100, c="#1565C0", marker="o",
                   edgecolors="white", linewidth=0.5)

ax.set_title("Conjunction Search: Red Square Among Mixed Distractors\n"
             "No pop-out — serial scan at ~50 ms/item",
             fontsize=10, fontweight="bold")
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.savefig("output/conjunction_search_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 3. Gestalt: Proximity via Subplots ─────────────────────
np.random.seed(7)
groups = {"A": (np.random.normal(0, 1, 50), np.random.normal(0, 1, 50)),
          "B": (np.random.normal(0, 1, 50), np.random.normal(0, 1, 50)),
          "C": (np.random.normal(0, 1, 50), np.random.normal(0, 1, 50))}

fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharey=True)
for ax, (name, (gx, gy)) in zip(axes, groups.items()):
    ax.scatter(gx, gy, s=25, c="#1565C0", alpha=0.6, edgecolors="white", linewidth=0.3)
    ax.set_title(f"Group {name}", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)

fig.suptitle("Gestalt Proximity: Physical Separation Creates Groups",
             fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/gestalt_proximity_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 4. Gestalt: Enclosure with axvspan ─────────────────────
np.random.seed(99)
months = np.arange(1, 13)
values = np.cumsum(np.random.normal(3, 5, 12)) + 50

fig, ax = plt.subplots(figsize=(7, 4))

# Enclosure: shaded band for Q2 (months 4-6)
ax.axvspan(4, 6, color="#E3F2FD", alpha=0.7, label="Q2 Promotion")
ax.plot(months, values, "o-", color="#1565C0", linewidth=1.5, markersize=5)
ax.text(5, max(values) + 2, "Q2 Promotion\nPeriod", ha="center",
        fontsize=8, fontweight="bold", color="#1565C0")

ax.set_xlabel("Month", fontsize=9)
ax.set_ylabel("Revenue ($K)", fontsize=9)
ax.set_title("Gestalt Enclosure: axvspan() Highlights a Period",
             fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=7)
plt.tight_layout()
plt.savefig("output/gestalt_enclosure_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 5. Multi-Channel Encoding ─────────────────────────────
np.random.seed(55)
n_e = 80
spend = np.random.uniform(10, 100, n_e)
roi = 0.4 * spend + np.random.normal(0, 12, n_e)
cat = np.random.choice(["A", "B", "C"], n_e)
budget = np.random.uniform(20, 200, n_e)

palette = {"A": "#1f77b4", "B": "#d62728", "C": "#2ca02c"}

fig, ax = plt.subplots(figsize=(7, 5))
for c in ["A", "B", "C"]:
    mask = cat == c
    ax.scatter(spend[mask], roi[mask], s=budget[mask] * 0.8,
               c=palette[c], alpha=0.6, edgecolors="white",
               linewidth=0.3, label=f"Cat {c}")

ax.set_xlabel("Marketing Spend ($K)", fontsize=9)
ax.set_ylabel("ROI (%)", fontsize=9)
ax.set_title("Four Encoding Channels: Position(x,y) + Color + Size",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8, title="Category", title_fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(alpha=0.15)
ax.tick_params(labelsize=7)
plt.tight_layout()
plt.savefig("output/multi_channel_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 6. Channel Accuracy Comparison ────────────────────────
cats = ["A", "B", "C", "D"]
vals = [42, 45, 43, 44]

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

# Position (most accurate)
axes[0].bar(cats, vals, color="#1565C0", width=0.5)
axes[0].set_ylim(0, 50)
axes[0].set_title("Position\n(most accurate)", fontsize=9, fontweight="bold")
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

# Area (less accurate)
for i, (c, v) in enumerate(zip(cats, vals)):
    r = np.sqrt(v / np.pi) * 0.3
    circle = plt.Circle((i, 0.5), r, color="#E53935", alpha=0.7)
    axes[1].add_patch(circle)
    axes[1].text(i, -0.2, c, ha="center", fontsize=9, fontweight="bold")
axes[1].set_xlim(-1, 4)
axes[1].set_ylim(-0.5, 1.5)
axes[1].set_aspect("equal")
axes[1].set_title("Area\n(less accurate)", fontsize=9, fontweight="bold")
for sp in axes[1].spines.values(): sp.set_visible(False)
axes[1].set_xticks([]); axes[1].set_yticks([])

# Color saturation (least accurate)
for i, (c, v) in enumerate(zip(cats, vals)):
    alpha = v / 50
    rect = plt.Rectangle((i - 0.35, 0), 0.7, 1,
                          facecolor=(0.08, 0.33, 0.73, alpha))
    axes[2].add_patch(rect)
    axes[2].text(i, -0.15, c, ha="center", fontsize=9, fontweight="bold")
axes[2].set_xlim(-0.8, 3.8)
axes[2].set_ylim(-0.3, 1.3)
axes[2].set_title("Saturation\n(least accurate)", fontsize=9, fontweight="bold")
for sp in axes[2].spines.values(): sp.set_visible(False)
axes[2].set_xticks([]); axes[2].set_yticks([])

fig.suptitle("Cleveland & McGill: Same Data, Different Accuracy\n"
             "Values: A=42, B=45, C=43, D=44",
             fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/channel_comparison_py.png", dpi=150, bbox_inches="tight")
plt.close()


print("── All M03 plots saved to output/ ──")
