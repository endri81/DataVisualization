"""
W02-M07: seaborn & plotnine for Python — Demo Script — UNYT Tirana
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# ── Simulate data (since we can't load seaborn datasets in sandbox) ──
n = 200
df = pd.DataFrame({
    "displ": np.random.uniform(1, 7, n),
    "hwy": lambda d: 35 - 3 * d["displ"] + np.random.normal(0, 3, n),
    "class": np.random.choice(["compact", "midsize", "suv", "pickup"], n),
    "cyl": np.random.choice([4, 6, 8], n),
}.items())
# Fix: build properly
displ = np.random.uniform(1, 7, n)
hwy = 35 - 3 * displ + np.random.normal(0, 3, n)
df = pd.DataFrame({
    "displ": displ, "hwy": hwy,
    "class": np.random.choice(["compact", "midsize", "suv", "pickup"], n),
    "cyl": np.random.choice([4, 6, 8], n),
    "type": np.random.choice(["Free", "Paid"], n, p=[0.9, 0.1]),
    "rating": np.random.normal(4.0, 0.5, n).clip(1, 5),
})

# ── 1. AXES-LEVEL: seaborn-style scatter + box + violin ──
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=False)

# Scatter with hue
pal = {"compact": "#1565C0", "midsize": "#E53935", "suv": "#2E7D32", "pickup": "#E65100"}
for cls, c in pal.items():
    mask = df["class"] == cls
    axes[0].scatter(df.loc[mask, "displ"], df.loc[mask, "hwy"], s=15, c=c, alpha=0.5,
                    edgecolors="none", label=cls)
axes[0].legend(fontsize=6, title="class"); axes[0].set_title("scatterplot(hue='class')", fontsize=8, fontweight="bold")
axes[0].set_xlabel("displ"); axes[0].set_ylabel("hwy")

# Boxplot
data_box = [df.loc[df["class"] == c, "hwy"].values for c in ["compact", "midsize", "suv", "pickup"]]
bp = axes[1].boxplot(data_box, labels=["compact", "midsize", "suv", "pickup"],
                     patch_artist=True, widths=0.4)
for patch, c in zip(bp["boxes"], pal.values()):
    patch.set_facecolor(c); patch.set_alpha(0.3)
axes[1].set_title("boxplot()", fontsize=8, fontweight="bold"); axes[1].tick_params(axis="x", labelsize=6)

# Violin
parts = axes[2].violinplot(data_box, positions=range(1, 5), showmeans=True, showmedians=True)
for pc, c in zip(parts["bodies"], pal.values()):
    pc.set_facecolor(c); pc.set_alpha(0.3)
axes[2].set_xticks(range(1, 5)); axes[2].set_xticklabels(["compact", "midsize", "suv", "pickup"], fontsize=6)
axes[2].set_title("violinplot()", fontsize=8, fontweight="bold")

for ax in axes:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
fig.suptitle("seaborn axes-level: Embed in Custom Layouts", fontsize=11, fontweight="bold")
plt.tight_layout(); plt.savefig("output/sns_axes_level.png", dpi=300); plt.close()

# ── 2. FIGURE-LEVEL: faceted scatter ──
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
for ax, cyl in zip(axes, [4, 6, 8]):
    sub = df.query("cyl == @cyl")
    for cls, c in pal.items():
        mask = sub["class"] == cls
        ax.scatter(sub.loc[mask, "displ"], sub.loc[mask, "hwy"], s=12, c=c, alpha=0.5, edgecolors="none", label=cls)
    ax.set_title(f"cyl = {cyl}", fontsize=9, fontweight="bold")
    ax.set_xlabel("displ"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
axes[0].set_ylabel("hwy"); axes[0].legend(fontsize=5, title="class", title_fontsize=6)
fig.suptitle("sns.relplot(col='cyl') equivalent: Faceted Scatter", fontsize=11, fontweight="bold")
plt.tight_layout(); plt.savefig("output/sns_figure_level.png", dpi=300); plt.close()

# ── 3. MULTI-AESTHETIC: hue + style + size ──
fig, ax = plt.subplots(figsize=(7, 5))
markers = {"compact": "o", "midsize": "s", "suv": "^", "pickup": "D"}
for cls in ["compact", "midsize", "suv", "pickup"]:
    mask = df["class"] == cls
    ax.scatter(df.loc[mask, "displ"], df.loc[mask, "hwy"],
               s=np.abs(df.loc[mask, "rating"]) * 30, c=pal[cls], alpha=0.5,
               marker=markers[cls], edgecolors="white", linewidth=0.4, label=cls)
ax.legend(fontsize=7, title="hue + style")
ax.set_xlabel("Displacement", fontsize=9); ax.set_ylabel("Highway MPG", fontsize=9)
ax.set_title("sns.scatterplot(hue=, style=, size=)", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(alpha=0.12); plt.tight_layout()
plt.savefig("output/sns_multi_aes.png", dpi=300); plt.close()

# ── 4. HEATMAP ──
np.random.seed(55)
corr = np.corrcoef(np.random.normal(0, 1, (6, n)))
labels = ["displ", "hwy", "cyl", "rating", "reviews", "installs"]
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(6)); ax.set_yticks(range(6))
ax.set_xticklabels(labels, fontsize=7, rotation=45, ha="right")
ax.set_yticklabels(labels, fontsize=7)
for i in range(6):
    for j in range(6):
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=6,
                color="white" if abs(corr[i, j]) > 0.5 else "black")
fig.colorbar(im, ax=ax, shrink=0.8)
ax.set_title("sns.heatmap(annot=True, cmap='RdBu_r')", fontsize=10, fontweight="bold")
plt.tight_layout(); plt.savefig("output/heatmap.png", dpi=300); plt.close()

# ── 5. REGPLOT equivalent ──
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(df["displ"], df["hwy"], s=12, c="#1565C0", alpha=0.3, edgecolors="none")
m, b = np.polyfit(df["displ"], df["hwy"], 1)
xs = np.linspace(1, 7, 50)
ax.plot(xs, m * xs + b, color="#E53935", linewidth=2)
ax.fill_between(xs, m * xs + b - 3, m * xs + b + 3, alpha=0.1, color="#E53935")
ax.set_xlabel("Displacement"); ax.set_ylabel("Highway MPG")
ax.set_title("sns.regplot() equivalent: scatter + regression + CI", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/regplot.png", dpi=300); plt.close()

# ── 6. plotnine example (if installed) ──
try:
    from plotnine import ggplot as p9ggplot, aes as p9aes, geom_point, geom_smooth, theme_minimal, labs, scale_color_manual
    p = (p9ggplot(df, p9aes(x="displ", y="hwy", color="class"))
         + geom_point(alpha=0.5, size=1.5)
         + geom_smooth(method="lm", se=True, color="grey")
         + scale_color_manual(values=pal)
         + theme_minimal()
         + labs(title="plotnine: ggplot2 syntax in Python", x="Displacement", y="Highway MPG"))
    p.save("output/plotnine_demo.png", dpi=300, width=7, height=5)
    print("  plotnine demo saved")
except ImportError:
    print("  plotnine not installed — pip install plotnine")

print("\nAll W02-M07 Python plots saved")
