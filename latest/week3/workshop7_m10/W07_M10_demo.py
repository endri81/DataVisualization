"""W07-M10: Lab — Build a 10-Slide Data Story Deck — Python Template — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True)

# STEP 1: Clean theme (M06)
plt.rcParams.update({
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#EEE", "axes.labelcolor": "#888",
    "xtick.color": "#888", "ytick.color": "#888",
    "grid.alpha": 0, "font.size": 10, "axes.titleweight": "bold"})

# STEP 2: Load data
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tv = yearly.query("type=='TV Show'")
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)

# STEP 3: Big Idea
print("══ BIG IDEA ══")
print(f"Netflix should pivot to originals and local-language content")
print(f"because movie additions declined {decline}% while international")
print(f"genres and TV Shows drive growth.\n")

# STEP 4: Storyboard
print("══ STORYBOARD ══")
storyboard = [
    ("1", "Title", "Netflix Content Strategy", "—"),
    ("2", "Context", "8,800+ titles over a decade", "Cumulative area"),
    ("3", "Hero", f"Movie additions declined {decline}%", "Grey+accent line"),
    ("4", "Evidence 1", "International = fastest genre", "Genre grey+accent"),
    ("5", "Evidence 2", "India rose to #2", "Country bar"),
    ("6", "Evidence 3", "Seasonal release calendar", "Subseries"),
    ("7", "Mechanism", "Drivers: expansion + originals", "Ranked bar"),
    ("8", "Resolution", "Pivot budget to originals", "Action items"),
    ("9", "Variant", "[TECHNICAL] Monthly + CI", "CI ribbon"),
    ("10", "CTA", "Approve Q2 reallocation", "Action summary"),
]
for s, role, headline, chart in storyboard:
    print(f"  Slide {s}: {role:<12} | {headline:<40} | {chart}")

# STEP 5: Build slides
# Helper
def save_slide(fig, filename):
    plt.tight_layout(); fig.savefig(f"output/{filename}", dpi=300); plt.close()

# S2: Context
fig, ax = plt.subplots(figsize=(10, 5.5))
cum = nf.dropna(subset=["date_added"]).set_index("date_added").resample("ME").size().cumsum()
ax.fill_between(cum.index, cum.values, alpha=0.12, color="#1565C0")
ax.plot(cum.index, cum.values, color="#1565C0", lw=1.5)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.set_title("Netflix built a catalog of 8,800+ titles over a decade", fontsize=14)
ax.set_ylabel("Cumulative Titles")
save_slide(fig, "slide02_context.png")

# S3: Hero
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(tv.year_added, tv.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=3, markersize=7)
ax.axhline(y=peak_n, ls=":", color="#CCC", lw=0.5)
ax.axvspan(2019.5, 2021.5, alpha=0.03, color="#E53935")
ax.annotate(f"–{decline}% from peak",
    xy=(2020, (peak_n+latest_n)/2), xytext=(2017, latest_n*0.65),
    fontsize=11, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#E53935", lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color="#E53935", lw=1.5))
ax.text(2021.15, latest_n, " Movies", fontsize=10, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, tv.iloc[-1]["n"], " TV Shows", fontsize=9, color="#BBB", va="center")
ax.set_xlim(2014.5, 2022.8)
ax.set_title(f"Movie additions declined {decline}% from their 2019 peak", fontsize=14)
ax.set_ylabel("Titles Added")
save_slide(fig, "slide03_hero.png")

# S4: Genre
fig, ax = plt.subplots(figsize=(10, 5.5))
genres = nf["listed_in"].str.split(",").explode().str.strip()
top5 = genres.value_counts().head(5).index
nf_g = nf.assign(listed_in=nf["listed_in"].str.split(",")).explode("listed_in")
nf_g["genre"] = nf_g["listed_in"].str.strip()
gyr = nf_g.query("genre in @top5 and 2015<=year_added<=2021").groupby(["year_added","genre"]).size().reset_index(name="n")
growth = {}
for g in top5:
    sub = gyr.query("genre==@g").sort_values("year_added")
    if len(sub)>=2 and sub.iloc[0]["n"]>0: growth[g]=sub.iloc[-1]["n"]/sub.iloc[0]["n"]
fastest = max(growth, key=growth.get) if growth else top5[0]
for g in top5:
    sub = gyr.query("genre==@g")
    c = "#2E7D32" if g==fastest else "#DDD"; lw = 2.5 if g==fastest else 0.8
    ax.plot(sub.year_added, sub.n, "-o", color=c, lw=lw, markersize=3 if c=="#DDD" else 5)
    ax.text(sub.year_added.values[-1]+0.1, sub.n.values[-1],
        f" {g[:22]}", fontsize=7, color=c if c=="#2E7D32" else "#AAA",
        fontweight="bold" if c=="#2E7D32" else "normal", va="center")
ax.set_xlim(2014.5, 2024)
ax.set_title(f"{fastest} is the fastest-growing genre category", fontsize=14)
ax.set_ylabel("Titles Added")
save_slide(fig, "slide04_genre.png")

# S5: Country
fig, ax = plt.subplots(figsize=(10, 5.5))
top10 = nf.dropna(subset=["primary_country"])["primary_country"].value_counts().head(10).sort_values()
colors = ["#E53935" if c=="India" else "#BBDEFB" for c in top10.index]
ax.barh(top10.index, top10.values, color=colors, height=0.6)
for i, (c, v) in enumerate(top10.items()):
    ax.text(v+10, i, f"{v:,}", va="center", fontsize=8, fontweight="bold")
ax.set_title("India rose to #2 in content production", fontsize=14)
save_slide(fig, "slide05_country.png")

# S6: Seasonal
fig, ax = plt.subplots(figsize=(10, 5.5))
months = np.arange(1, 13)
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
for yr in range(2016, 2022):
    sub = nf.query("year_added==@yr").groupby("month_added").size().reindex(range(1,13), fill_value=0)
    c = "#E53935" if yr==2021 else "#BBB"; a = 1.0 if yr==2021 else 0.25
    ax.plot(months, sub.values, "-o", color=c, alpha=a, lw=1.5 if yr==2021 else 0.5, markersize=2 if yr<2021 else 4)
ax.set_xticks(months); ax.set_xticklabels(month_labels)
ax.set_title("Consistent seasonal calendar: Q4 holiday spike every year", fontsize=14)
ax.set_ylabel("Titles Added")
save_slide(fig, "slide06_seasonal.png")

# S7: Mechanism
fig, ax = plt.subplots(figsize=(10, 5.5))
drivers = ["COVID demand","Licensing","Local-language","Original investment","Global expansion"]
impacts = [5, 10, 22, 28, 35]
ax.barh(drivers, impacts, color="#00695C", height=0.5)
for i, v in enumerate(impacts): ax.text(v+0.5, i, f"{v}%", va="center", fontsize=9, fontweight="bold", color="#00695C")
ax.set_title("Growth driven by global expansion + original investment", fontsize=14)
ax.set_xlabel("Estimated Impact (%)")
save_slide(fig, "slide07_mechanism.png")

# S8: Resolution
fig, ax = plt.subplots(figsize=(10, 5.5)); ax.axis("off")
actions = [("1.", "20 flagship originals / quarter", "80/year"),
    ("2.", "Grow India+Korea production 50%", "+50% YoY"),
    ("3.", "Cut catalog filler 30%", "–30% YoY"),
    ("4.", "Launch 5 local-language hubs", "5 by Q4")]
for i, (num, action, target) in enumerate(actions):
    y = 0.78 - i*0.20
    ax.text(0.05, y, num, fontsize=14, fontweight="bold", color="#1565C0")
    ax.text(0.12, y, action, fontsize=12, fontweight="bold", color="#333")
    ax.text(0.12, y-0.06, f"Target: {target}", fontsize=9, color="#888", fontstyle="italic")
ax.set_title("Pivot budget: originals + local-language content", fontsize=14, pad=15)
save_slide(fig, "slide08_resolution.png")

# S9: Technical variant
fig, ax = plt.subplots(figsize=(10, 5.5))
monthly = (nf.dropna(subset=["date_added"]).query("date_added.dt.year>=2016")
    .set_index("date_added").groupby("type").resample("ME").size().reset_index(name="n"))
for t, c in [("Movie","#1565C0"),("TV Show","#E53935")]:
    sub = monthly.query("type==@t").sort_values("date_added")
    ax.scatter(sub.date_added, sub.n, s=8, c=c, alpha=0.3)
    roll = sub.n.rolling(3).mean(); roll_std = sub.n.rolling(3).std()
    ax.plot(sub.date_added, roll, color=c, lw=1.2, label=t)
    ax.fill_between(sub.date_added, (roll-1.96*roll_std).clip(lower=0), roll+1.96*roll_std, alpha=0.08, color=c)
ax.legend(fontsize=8); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.set_title("[TECHNICAL] Monthly Additions: 3-month rolling mean ± 1.96σ", fontsize=13)
ax.set_ylabel("Monthly Titles")
save_slide(fig, "slide09_variant.png")

print(f"\n══ DECK COMPLETE ══")
print(f"8 slide PNGs saved (slide02–slide09)")
print(f"Big Idea and storyboard printed above")
print(f"Reflection: [STUDENT WRITES 300 WORDS]")
print(f"\nAll W07-M10 Lab Python outputs saved")
