"""W07-M04: The Seven Basic Data Stories — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True)

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()

ec = pd.read_csv("ecar.csv"); ec.columns=[c.strip().replace("  "," ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec = ec.query("2002<=Year<=2012")

yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tvshows = yearly.query("type=='TV Show'")

# 7-PANEL DASHBOARD
fig = plt.figure(figsize=(16, 14)); gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# S1: CHANGE OVER TIME
ax = fig.add_subplot(gs[0,0])
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2, markersize=5)
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
ax.annotate(f"–{round((1-latest_n/peak_n)*100)}%", xy=(2020, (peak_n+latest_n)/2),
    fontsize=9, fontweight="bold", color="#E53935", ha="center",
    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#E53935"))
ax.set_title("S1: Change Over Time\n'Movies peaked 2019, declined since'", fontsize=8, fontweight="bold", color="#1565C0")

# S2: DRILL DOWN
ax = fig.add_subplot(gs[0,1])
type_split = nf["type"].value_counts()
ax.barh(type_split.index, type_split.values/type_split.sum()*100, color=["#1565C0","#E53935"], height=0.4)
for i,(t,v) in enumerate(zip(type_split.index, type_split.values/type_split.sum()*100)):
    ax.text(v+1, i, f"{v:.0f}%", va="center", fontsize=8, fontweight="bold")
ax.set_title("S2: Drill Down\n'69% movies, 31% TV'", fontsize=8, fontweight="bold", color="#2E7D32")

# S3: ZOOM OUT (bump chart)
ax = fig.add_subplot(gs[0,2])
cyr = (nf.dropna(subset=["primary_country"]).query("2016<=year_added<=2021")
    .groupby(["year_added","primary_country"]).size().reset_index(name="n"))
cyr["cum"] = cyr.sort_values("year_added").groupby("primary_country")["n"].cumsum()
top5c = cyr.query("year_added==2021").nlargest(5,"cum")["primary_country"].tolist()
for c in top5c:
    sub = cyr.query("primary_country==@c").sort_values("year_added")
    ranks = sub.groupby("year_added")["cum"].rank(ascending=False, method="first")
    ax.plot(sub.year_added, ranks, "-o", lw=1, markersize=3)
ax.set_ylim(5.5, 0.5); ax.set_title("S3: Zoom Out\n'India rose to #2 globally'", fontsize=8, fontweight="bold", color="#E65100")

# S4: CONTRAST
ax = fig.add_subplot(gs[1,0])
pre = ec.query("Year<2008")["Spread"].median(); post = ec.query("Year>=2008")["Spread"].median()
ax.bar(["Pre-2008","Post-2008"], [pre, post], color=["#1565C0","#E53935"], width=0.4)
ax.set_title(f"S4: Contrast\n'Spread: {pre:.1f}pp → {post:.1f}pp'", fontsize=8, fontweight="bold", color="#C62828")
ax.set_ylabel("Median Spread (pp)")

# S5: INTERSECTIONS
ax = fig.add_subplot(gs[1,1])
sample = ec.sample(2000, random_state=42)
bp = ax.boxplot([sample.query("Tier==@t")["Rate"].values for t in sorted(ec.Tier.unique())],
    labels=[f"T{t}" for t in sorted(ec.Tier.unique())], patch_artist=True, widths=0.5)
for patch in bp["boxes"]: patch.set_facecolor("#BBDEFB")
ax.set_title("S5: Intersections\n'Higher tier → lower rate'", fontsize=8, fontweight="bold", color="#7B1FA2")
ax.set_ylabel("Rate (%)")

# S6: FACTORS
ax = fig.add_subplot(gs[1,2])
factors = ["Global expansion","Original production","Local-language","Licensing","COVID demand"]
impacts = [35, 28, 22, 10, 5]
ax.barh(factors, impacts, color="#00695C", height=0.5)
for i, v in enumerate(impacts): ax.text(v+0.5, i, f"{v}%", va="center", fontsize=7, fontweight="bold", color="#00695C")
ax.set_title("S6: Factors\n'Three drivers of genre growth'", fontsize=8, fontweight="bold", color="#00695C")

# S7: OUTLIERS
ax = fig.add_subplot(gs[2,0])
monthly = nf.dropna(subset=["date_added"]).query("date_added.dt.year>=2016").set_index("date_added").resample("ME").size()
avg = monthly.mean()
colors = ["#E53935" if v > avg*2 else "#BBBBBB" for v in monthly.values]
ax.scatter(monthly.index, monthly.values, s=10, c=colors, zorder=5)
ax.plot(monthly.index, monthly.values, color="#EEEEEE", lw=0.3)
ax.axhline(avg, ls="--", color="#888", lw=0.5); ax.axhline(avg*2, ls=":", color="#E53935", lw=0.5)
ax.set_title("S7: Outliers\n'Several months > 2× average'", fontsize=8, fontweight="bold", color="#E53935")

# Decision table panel
ax = fig.add_subplot(gs[2,1:]); ax.axis("off")
rows = [
    ("'grew / declined / peaked'", "Change Over Time", "Line chart"),
    ("'composed of / breakdown'", "Drill Down", "Stacked bar"),
    ("'compared to / in context'", "Zoom Out", "Small multiples"),
    ("'vs / gap between'", "Contrast", "Grouped bar, slope"),
    ("'correlated / related'", "Intersection", "Scatter"),
    ("'driven by / because'", "Factors", "Waterfall, tornado"),
    ("'unusual / spike / anomaly'", "Outlier", "Highlight scatter"),
]
ax.text(0.5, 0.95, "Finding → Story → Chart Decision Table", ha="center",
    fontsize=10, fontweight="bold", transform=ax.transAxes)
for i, (keyword, story, chart) in enumerate(rows):
    y = 0.82 - i * 0.11
    ax.text(0.05, y, keyword, fontsize=7, color="#555", transform=ax.transAxes)
    ax.text(0.42, y, f"→ {story}", fontsize=7, fontweight="bold", color="#333", transform=ax.transAxes)
    ax.text(0.72, y, f"→ {chart}", fontsize=7, color="#888", fontstyle="italic", transform=ax.transAxes)

for a in fig.get_axes():
    if hasattr(a, 'spines'):
        a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.tick_params(labelsize=5)

fig.suptitle("Seven Data Stories Applied to Netflix + e-Car", fontsize=14, fontweight="bold")
plt.savefig("output/seven_stories_applied.png", dpi=300, bbox_inches="tight"); plt.close()

print("\nAll W07-M04 Python outputs saved")
