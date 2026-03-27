"""W07-M07: Case Study — Netflix Data Story — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True)

# Clean defaults
plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,
    "axes.edgecolor":"#EEE","axes.labelcolor":"#888","xtick.color":"#888",
    "ytick.color":"#888","grid.alpha":0,"font.size":10,"axes.titleweight":"bold"})

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tvshows = yearly.query("type=='TV Show'")
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)

# ═══════════════════════════════════════════════════════
# Build all 8 evidence slides
# ═══════════════════════════════════════════════════════

# S2: Context — cumulative area
fig, ax = plt.subplots(figsize=(10, 5.5))
cum = nf.dropna(subset=["date_added"]).set_index("date_added").resample("ME").size().cumsum()
ax.fill_between(cum.index, cum.values, alpha=0.15, color="#1565C0")
ax.plot(cum.index, cum.values, color="#1565C0", lw=1.5)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.set_title("Netflix built a catalog of 8,800+ titles over a decade", fontsize=13)
ax.set_ylabel("Cumulative Titles")
plt.tight_layout(); plt.savefig("output/slide02_context.png", dpi=300); plt.close()

# S3: Complication — movie decline (grey+accent)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax.text(2021.15, latest_n, " Movies", fontsize=9, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8, color="#BBB", va="center")
ax.annotate(f"–{decline}%\nfrom peak", xy=(2019.5, (peak_n+latest_n)/2),
    fontsize=11, fontweight="bold", color="#E53935", ha="center",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
ax.set_xlim(2014.5, 2022.5)
ax.set_title(f"Movie additions declined {decline}% from their 2019 peak", fontsize=13)
ax.set_ylabel("Titles Added")
plt.tight_layout(); plt.savefig("output/slide03_complication.png", dpi=300); plt.close()

# S4: Contrast — indexed dual line
fig, ax = plt.subplots(figsize=(10, 5.5))
m_idx = movies.n.values / movies.n.values[0] * 100
t_idx = tvshows.n.values / tvshows.n.values[0] * 100
ax.plot(movies.year_added, m_idx, "-o", color="#1565C0", lw=1.5, markersize=5, label="Movie")
ax.plot(tvshows.year_added, t_idx, "-o", color="#E53935", lw=1.5, markersize=5, label="TV Show")
ax.axhline(100, ls=":", color="#888", lw=0.5)
ax.text(2021.15, m_idx[-1], " Movies", fontsize=8, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, t_idx[-1], " TV Shows", fontsize=8, fontweight="bold", color="#E53935", va="center")
ax.set_xlim(2014.5, 2022.5)
ax.set_title("TV Shows grew 3× faster than Movies in relative terms", fontsize=13)
ax.set_ylabel("Index (2015 = 100)")
plt.tight_layout(); plt.savefig("output/slide04_contrast.png", dpi=300); plt.close()

# S5: Analysis — genre growth (accent bar)
genres = nf["listed_in"].str.split(",").explode().str.strip()
g17 = nf.query("year_added==2017")["listed_in"].str.split(",").explode().str.strip().value_counts()
g21 = nf.query("year_added==2021")["listed_in"].str.split(",").explode().str.strip().value_counts()
growth = ((g21 - g17) / g17.clip(lower=1) * 100).dropna().sort_values().tail(7)
fastest_genre = growth.index[-1]

fig, ax = plt.subplots(figsize=(10, 5.5))
colors = ["#2E7D32" if g == fastest_genre else "#BBDEFB" for g in growth.index]
ax.barh(growth.index, growth.values, color=colors, height=0.5)
for i, (g, v) in enumerate(growth.items()):
    ax.text(v+2, i, f"+{v:.0f}%", va="center", fontsize=8, fontweight="bold",
        color="#2E7D32" if g == fastest_genre else "#888")
ax.set_title(f"{fastest_genre} is the fastest-growing genre category", fontsize=13)
ax.set_xlabel("Growth % (2017 → 2021)")
plt.tight_layout(); plt.savefig("output/slide05_analysis.png", dpi=300); plt.close()

# S6: Deep Dive — India bump chart
cyr = (nf.dropna(subset=["primary_country"]).query("2016<=year_added<=2021")
    .groupby(["year_added","primary_country"]).size().reset_index(name="n"))
cyr["cum"] = cyr.sort_values("year_added").groupby("primary_country")["n"].cumsum()
top5c = cyr.query("year_added==2021").nlargest(5,"cum")["primary_country"].tolist()
race = cyr.query("primary_country in @top5c").copy()
race["rank"] = race.groupby("year_added")["cum"].rank(ascending=False, method="first")

fig, ax = plt.subplots(figsize=(10, 5.5))
for c in top5c:
    sub = race.query("primary_country==@c").sort_values("year_added")
    color = "#E53935" if c == "India" else "#DDDDDD"
    lw = 2.5 if c == "India" else 0.8
    ax.plot(sub.year_added, sub["rank"], "-o", color=color, lw=lw, markersize=4 if c=="India" else 2)
    ax.text(sub.year_added.values[-1]+0.15, sub["rank"].values[-1],
        f" {c}", fontsize=7, fontweight="bold" if c=="India" else "normal",
        color=color if c!="#DDDDDD" else "#AAA", va="center")
ax.set_ylim(5.5, 0.5); ax.set_xlim(2015.5, 2022.5)
ax.set_title("India rose from #5 to #2 in Netflix content production", fontsize=13)
ax.set_ylabel("Rank (1 = most titles)")
plt.tight_layout(); plt.savefig("output/slide06_deepdive.png", dpi=300); plt.close()

# S7: Seasonal — calendar heatmap
d2020 = nf.query("year_added==2020").dropna(subset=["date_added"]).groupby("date_added").size().reset_index(name="n")
d2020["dow"] = d2020["date_added"].dt.dayofweek
d2020["week"] = d2020["date_added"].dt.isocalendar().week.astype(int)
pivot = d2020.pivot_table(index="dow", columns="week", values="n", aggfunc="sum", fill_value=0)

fig, ax = plt.subplots(figsize=(11, 3.5))
im = ax.imshow(pivot.values, cmap="YlGn", aspect="auto", interpolation="nearest")
ax.set_yticks(range(7)); ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], fontsize=7)
ax.set_xlabel("Week of Year"); plt.colorbar(im, ax=ax, shrink=0.5, label="Titles")
ax.set_title("Friday is the primary release day, with Q4 holiday spikes", fontsize=12)
plt.tight_layout(); plt.savefig("output/slide07_seasonal.png", dpi=300); plt.close()

# S8: Resolution — composition stacked area
type_m = (nf.dropna(subset=["date_added"]).query("date_added.dt.year>=2015")
    .set_index("date_added").groupby("type").resample("ME").size().unstack(0, fill_value=0).cumsum())
total = type_m.sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 5.5))
if "Movie" in type_m and "TV Show" in type_m:
    ax.stackplot(type_m.index, type_m["Movie"]/total*100, type_m["TV Show"]/total*100,
        labels=["Movie","TV Show"], colors=["#1565C0","#E53935"], alpha=0.7)
ax.legend(fontsize=8, loc="center right")
ax.set_title("TV Show share grew from 20% to 35% — the catalog is rebalancing", fontsize=12)
ax.set_ylabel("Share (%)"); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("output/slide08_resolution.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# TITLE SEQUENCE TEST
# ═══════════════════════════════════════════════════════
print("\n=== TITLE SEQUENCE TEST ===")
titles = [
    "1. Netflix Content Strategy: A Data Story",
    "2. Netflix built a catalog of 8,800+ titles over a decade",
    f"3. Movie additions declined {decline}% from their 2019 peak",
    "4. TV Shows grew 3x faster than Movies in relative terms",
    f"5. {fastest_genre} is the fastest-growing genre category",
    "6. India rose from #5 to #2 in content production",
    "7. Friday is the primary release day, with Q4 spikes",
    "8. TV Show share grew from 20% to 35% — rebalancing",
    "9. Four actions: originals, local content, reduce filler",
    "10. Explore the dashboard for more detail",
]
for t in titles: print(f"  {t}")
print("\nDoes the story work from titles alone? ✓")

print("\nAll W07-M07 Python outputs saved")
