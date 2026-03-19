"""W06-M07: Advanced Animation — Bar Chart Races — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.animation import FuncAnimation
os.makedirs("output", exist_ok=True)

# ── 1. LOAD AND PREPARE NETFLIX DATA ────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
nf = nf.dropna(subset=["date_added", "primary_country"])
nf = nf.query("2016 <= year_added <= 2021")

# Cumulative titles per country per year
country_yearly = (nf.groupby(["year_added", "primary_country"]).size()
    .reset_index(name="n"))
country_yearly["cumulative"] = (country_yearly
    .sort_values("year_added")
    .groupby("primary_country")["n"]
    .cumsum())

# Top 10 by 2021 total
top10_2021 = (country_yearly.query("year_added == 2021")
    .nlargest(10, "cumulative")["primary_country"].tolist())
race_data = country_yearly.query("primary_country in @top10_2021").copy()
race_data["rank"] = (race_data.groupby("year_added")["cumulative"]
    .rank(method="first", ascending=False).astype(int))

# ── 2. STATIC BAR CHART FRAME — 2021 ────────────────────
frame = race_data.query("year_added == 2021").sort_values("cumulative")
colors = plt.cm.turbo(np.linspace(0.15, 0.85, len(frame)))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(frame["primary_country"], frame["cumulative"],
    color=colors, height=0.6)
for i, (_, row) in enumerate(frame.iterrows()):
    ax.text(row["cumulative"] + 20, i, f"{row['cumulative']:,}",
        va="center", fontsize=8, fontweight="bold")
ax.text(0.95, 0.05, "2021", transform=ax.transAxes, fontsize=35,
    fontweight="bold", color="#DDDDDD", ha="right", va="bottom")
ax.set_title("Netflix Titles by Country: 2021\n"
    "Bar chart race: final frame (cumulative)", fontweight="bold")
ax.set_xlabel("Cumulative Titles")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/bar_race_frame_2021.png", dpi=300); plt.close()

# ── 3. KEY FRAMES PANEL (2017, 2019, 2021) ──────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
for ax, yr in zip(axes, [2017, 2019, 2021]):
    fr = race_data.query("year_added == @yr").sort_values("cumulative")
    ax.barh(fr["primary_country"], fr["cumulative"],
        color=plt.cm.turbo(np.linspace(0.15, 0.85, len(fr))), height=0.6)
    for _, row in fr.iterrows():
        ax.text(row["cumulative"] + 10, row["primary_country"],
            f"{row['cumulative']:,}", va="center", fontsize=6)
    ax.set_title(f"{yr}", fontsize=12, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=7)
fig.suptitle("Bar Chart Race: Key Frames (static alternative for reports)",
    fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("output/keyframes_panel.png", dpi=300); plt.close()

# ── 4. BUMP CHART — Rank plot (static alternative) ──────
fig, ax = plt.subplots(figsize=(10, 6))
cmap = plt.cm.turbo
for i, country in enumerate(top10_2021):
    sub = race_data.query("primary_country == @country").sort_values("year_added")
    color = cmap(i / len(top10_2021))
    ax.plot(sub["year_added"], sub["rank"], "-o", color=color,
        lw=1.5, markersize=5, zorder=5)
    # Label at right end
    last = sub.iloc[-1]
    ax.text(last["year_added"] + 0.15, last["rank"],
        f" {country}", fontsize=7, fontweight="bold",
        color=color, va="center")

ax.set_ylim(10.5, 0.5)  # 1 at top
ax.set_xlim(2015.5, 2022.5)
ax.set_yticks(range(1, 11))
ax.set_xlabel("Year"); ax.set_ylabel("Rank (1 = most titles)")
ax.set_title("Bump Chart: Country Rank Changes (2016–2021)\n"
    "Static alternative — all years visible simultaneously",
    fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.2)
plt.tight_layout()
plt.savefig("output/bump_chart.png", dpi=300); plt.close()

# ── 5. SLOPE CHART (2016 → 2021) ────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
for i, country in enumerate(top10_2021):
    sub = race_data.query("primary_country == @country and year_added in [2016, 2021]")
    if len(sub) == 2:
        sub = sub.sort_values("year_added")
        color = cmap(i / len(top10_2021))
        ax.plot([0, 1], sub["rank"].values, "-o", color=color,
            lw=1.5, markersize=6)
        # Left label
        ax.text(-0.05, sub["rank"].values[0], country,
            ha="right", va="center", fontsize=7, color=color, fontweight="bold")
        # Right label with count
        ax.text(1.05, sub["rank"].values[1],
            f"{country} ({sub['cumulative'].values[1]:,})",
            ha="left", va="center", fontsize=7, color=color, fontweight="bold")

ax.set_ylim(10.5, 0.5)
ax.set_xlim(-0.4, 1.4)
ax.set_xticks([0, 1]); ax.set_xticklabels(["2016", "2021"], fontsize=11, fontweight="bold")
ax.set_ylabel("Rank")
ax.set_title("Slope Chart: Who Climbed? Who Fell?\n"
    "Rank shift 2016 → 2021 (values = 2021 cumulative)", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.2)
plt.tight_layout()
plt.savefig("output/slope_chart.png", dpi=300); plt.close()

# ── 6. ANIMATED BAR CHART RACE (FuncAnimation) ──────────
years = sorted(race_data["year_added"].unique())
fig, ax = plt.subplots(figsize=(9, 5))

def update(frame_idx):
    ax.clear()
    yr = years[frame_idx]
    fr = race_data.query("year_added == @yr").sort_values("cumulative")
    colors_f = plt.cm.turbo(np.linspace(0.15, 0.85, len(fr)))
    ax.barh(fr["primary_country"], fr["cumulative"],
        color=colors_f, height=0.6)
    for _, row in fr.iterrows():
        ax.text(row["cumulative"] + 10, row["primary_country"],
            f"{row['cumulative']:,}", va="center", fontsize=7, fontweight="bold")
    ax.text(0.95, 0.05, str(yr), transform=ax.transAxes, fontsize=35,
        fontweight="bold", color="#DDDDDD", ha="right", va="bottom")
    ax.set_title("Netflix Titles by Country", fontweight="bold")
    ax.set_xlabel("Cumulative Titles")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    return []

anim = FuncAnimation(fig, update, frames=len(years),
    interval=800, blit=False, repeat=True)
try:
    anim.save("output/bar_race.gif", writer="pillow", fps=2)
    print("Animated bar race saved: output/bar_race.gif")
except Exception as e:
    print(f"Could not save GIF: {e}")
plt.close()

# ── 7. bar_chart_race PACKAGE (if installed) ────────────
# try:
#     import bar_chart_race as bcr
#     # Pivot to wide format: index=year, columns=country, values=cumulative
#     pivot = (race_data
#         .pivot(index="year_added", columns="primary_country", values="cumulative")
#         .fillna(method="ffill").fillna(0))
#     bcr.bar_chart_race(
#         pivot,
#         filename="output/bar_race_bcr.gif",
#         n_bars=10,
#         period_length=800,
#         figsize=(7, 4),
#         title="Netflix by Country",
#         bar_size=0.7,
#         period_fmt="{x:.0f}")
#     print("bcr bar race saved")
# except ImportError:
#     print("bar_chart_race not installed (pip install bar_chart_race)")

# ── 8. KEY STATISTICS ────────────────────────────────────
print("\n=== Country Rankings ===")
for yr in [2016, 2021]:
    print(f"\n{yr} Top 5:")
    top5 = race_data.query("year_added == @yr").nsmallest(5, "rank")
    for _, row in top5.iterrows():
        print(f"  #{int(row['rank'])}: {row['primary_country']} ({row['cumulative']:,})")

# Rank changes
r16 = race_data.query("year_added == 2016")[["primary_country","rank"]].set_index("primary_country")
r21 = race_data.query("year_added == 2021")[["primary_country","rank"]].set_index("primary_country")
changes = r16.join(r21, lsuffix="_2016", rsuffix="_2021").dropna()
changes["improvement"] = changes["rank_2016"] - changes["rank_2021"]
print("\nBiggest rank improvers:")
print(changes.sort_values("improvement", ascending=False).head(5).to_string())

print("\nAll W06-M07 Python outputs saved")
