"""W07-M09: Audience Adaptation — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
yearly = nf.query("2016<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tv = yearly.query("type=='TV Show'")
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)

# ═══ THREE AUDIENCE VARIANTS ═══
fig, axes = plt.subplots(1, 3, figsize=(22, 6))

# EXECUTIVE
ax = axes[0]
ax.plot(tv.year_added, tv.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax.text(2021.1, latest_n, " Movies", fontsize=9, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.1, tv.iloc[-1]["n"], " TV", fontsize=8, color="#BBB", va="center")
ax.annotate(f"–{decline}%", xy=(2019.5, (peak_n+latest_n)/2),
    fontsize=14, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
ax.set_xlim(2015.5, 2022.5)
ax.set_title(f"EXECUTIVE\n'Movie additions declined {decline}%'\n1 message, grey+accent, callout",
    fontsize=10, fontweight="bold", color="#1565C0")
ax.set_ylabel("Titles Added")

# TECHNICAL
ax = axes[1]
for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
    sub = yearly.query("type==@t")
    ax.plot(sub.year_added, sub.n, "-o", color=c, lw=1.5, markersize=4, label=t)
    for _, row in sub.iterrows():
        ax.text(row.year_added, row.n+15, str(int(row.n)), ha="center", fontsize=5, color=c)
ax.legend(fontsize=7)
ax.set_title("TECHNICAL\n'Netflix Additions by Type (2016–2021)'\nBoth series, all values, legend",
    fontsize=10, fontweight="bold", color="#2E7D32")
ax.set_ylabel("Titles Added")

# PUBLIC
ax = axes[2]
ax.bar(movies.year_added, movies.n, color="#1565C0", width=0.6, alpha=0.8)
for _, row in movies.iterrows():
    ax.text(row.year_added, row.n+15, f"{int(row.n):,}", ha="center",
        fontsize=9, fontweight="bold")
ax.set_title("PUBLIC\n'Netflix added fewer movies each year since 2019'\nSimple bar, big labels, no jargon",
    fontsize=10, fontweight="bold", color="#E65100")
ax.set_ylabel("Movies Added"); ax.set_xlabel("Year")

for ax in axes:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Same Finding, Three Audiences", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.savefig("output/three_audiences.png", dpi=300); plt.close()

# ═══ INDIVIDUAL VARIANTS ═══
# Executive
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(tv.year_added, tv.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax.text(2021.15, latest_n, " Movies", fontsize=10, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, tv.iloc[-1]["n"], " TV Shows", fontsize=9, color="#BBB", va="center")
ax.annotate(f"–{decline}% decline\nfrom 2019 peak",
    xy=(2020, (peak_n+latest_n)/2), xytext=(2017.5, latest_n*0.65),
    fontsize=11, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#E53935", lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color="#E53935", lw=1.5))
ax.set_xlim(2015.5, 2022.8)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_title(f"Movie additions declined {decline}% from their 2019 peak",
    fontsize=14, fontweight="bold")
ax.set_ylabel("Titles Added")
plt.tight_layout(); plt.savefig("output/exec_variant.png", dpi=300); plt.close()

# Technical (monthly with rolling mean)
monthly = (nf.dropna(subset=["date_added"]).query("date_added.dt.year>=2016")
    .set_index("date_added").groupby("type").resample("ME").size()
    .reset_index(name="n"))
fig, ax = plt.subplots(figsize=(10, 5.5))
from matplotlib.dates import DateFormatter
for t, c in [("Movie","#1565C0"),("TV Show","#E53935")]:
    sub = monthly.query("type==@t").sort_values("date_added")
    ax.scatter(sub.date_added, sub.n, s=8, c=c, alpha=0.3)
    roll = sub.n.rolling(3).mean()
    ax.plot(sub.date_added, roll, color=c, lw=1.2, label=t)
    roll_std = sub.n.rolling(3).std()
    ax.fill_between(sub.date_added, (roll-1.96*roll_std).clip(lower=0),
        roll+1.96*roll_std, alpha=0.08, color=c)
ax.legend(fontsize=8)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_title("Netflix Monthly Additions by Type (2016–2021)\n"
    "3-month rolling mean ± 1.96σ | Raw points for variance", fontsize=12, fontweight="bold")
ax.set_ylabel("Monthly Titles")
plt.tight_layout(); plt.savefig("output/tech_variant.png", dpi=300); plt.close()

# Public
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(movies.year_added, movies.n, color="#1565C0", width=0.5, alpha=0.8)
for _, row in movies.iterrows():
    ax.text(row.year_added, row.n+15, f"{int(row.n):,}", ha="center",
        fontsize=10, fontweight="bold", color="#1565C0")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_title("Netflix is adding fewer movies every year since 2019",
    fontsize=16, fontweight="bold")
ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("")
plt.tight_layout(); plt.savefig("output/public_variant.png", dpi=300); plt.close()

# ═══ e-Car: 3 VARIANTS ═══
ec = pd.read_csv("ecar.csv"); ec.columns=[c.strip().replace("  "," ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec = ec.query("2002<=Year<=2012")
yr = ec.groupby("Year").agg(rate=("Rate","mean"),spread=("Spread","mean")).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(22, 6))
# Exec
ax = axes[0]
ax.axvspan(2007.5,2009.5,alpha=0.04,color="#E53935")
ax.plot(yr.Year, yr.spread, color="#DDD", lw=0.8)
ax.plot(yr.Year, yr.rate, "-o", color="#1565C0", lw=2.5, markersize=5)
ax.annotate("–2pp", xy=(2009, yr.rate.min()), fontsize=14, fontweight="bold",
    color="#E53935", bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
ax.set_title("EXECUTIVE\n'Rates dropped 2pp after 2008'", fontsize=10, fontweight="bold", color="#1565C0")
# Tech
ax = axes[1]
tyr = ec.groupby(["Year","Tier"])["Rate"].mean().reset_index()
for t in sorted(ec.Tier.unique()):
    sub = tyr.query("Tier==@t")
    ax.plot(sub.Year, sub.Rate, "-o", lw=0.8, markersize=3, label=f"Tier {t}")
ax.legend(fontsize=6); ax.axvline(x=2008, ls="--", color="#888", lw=0.5)
ax.set_title("TECHNICAL\n'Rate by Tier (2002–2012)'", fontsize=10, fontweight="bold", color="#2E7D32")
# Public
ax = axes[2]
ax.bar(yr.Year, yr.rate, color="#1565C0", width=0.5, alpha=0.8)
ax.set_title("PUBLIC\n'Car loan rates fell after 2008 crisis'", fontsize=10, fontweight="bold", color="#E65100")
for ax in axes: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("e-Car: Same Finding, Three Audiences", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.savefig("output/ecar_three_audiences.png", dpi=300); plt.close()

print("\nAll W07-M09 Python outputs saved")
print("Netflix: exec_variant, tech_variant, public_variant, three_audiences")
print("e-Car: ecar_three_audiences")
