"""W07-M05: Assertion-Evidence Slide Design — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True)

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tvshows = yearly.query("type=='TV Show'")
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)

# ═══════════════════════════════════════════════════════
# 5-SLIDE ASSERTION-EVIDENCE DECK
# ═══════════════════════════════════════════════════════

def make_slide(fig_func, filename, title, subtitle=""):
    fig, ax = fig_func()
    ax.set_title(f"{title}", fontsize=13, fontweight="bold", pad=10)
    if subtitle:
        ax.text(0.5, 1.02, subtitle, transform=ax.transAxes, ha="center",
            fontsize=9, color="#666", fontstyle="italic")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout(); plt.savefig(f"output/{filename}", dpi=300); plt.close()

# Slide 1: Context
def s1():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    cum = nf.dropna(subset=["date_added"]).set_index("date_added").resample("ME").size().cumsum()
    ax.fill_between(cum.index, cum.values, alpha=0.15, color="#1565C0")
    ax.plot(cum.index, cum.values, color="#1565C0", lw=1.5)
    ax.xaxis.set_major_formatter(DateFormatter("%Y")); ax.set_ylabel("Cumulative Titles")
    return fig, ax
make_slide(s1, "slide1_context.png", "Netflix built a catalog of 8,800+ titles over a decade")

# Slide 2: Complication
def s2():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
    ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
    ax.text(2021.15, latest_n, " Movies", fontsize=9, fontweight="bold", color="#1565C0", va="center")
    ax.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8, color="#BBB", va="center")
    ax.annotate(f"–{decline}%", xy=(2020, (peak_n+latest_n)/2),
        fontsize=12, fontweight="bold", color="#E53935", ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
    ax.set_xlim(2014.5, 2022.5); ax.set_ylabel("Titles Added")
    return fig, ax
make_slide(s2, "slide2_complication.png", f"But movie additions declined {decline}% from their 2019 peak")

# Slide 3: Analysis
def s3():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    genres = nf["listed_in"].str.split(",").explode().str.strip()
    top5 = genres.value_counts().head(5).index
    nf_g = nf.assign(listed_in=nf["listed_in"].str.split(",")).explode("listed_in")
    nf_g["genre"] = nf_g["listed_in"].str.strip()
    gyr = nf_g.query("genre in @top5 and 2015<=year_added<=2021").groupby(["year_added","genre"]).size().reset_index(name="n")
    for g in top5:
        sub = gyr.query("genre==@g")
        color = "#2E7D32" if g == top5[0] else "#DDD"
        lw = 2.5 if g == top5[0] else 0.8
        ax.plot(sub.year_added, sub.n, "-o", color=color, lw=lw, markersize=3 if color=="#DDD" else 5)
        ax.text(sub.year_added.values[-1]+0.1, sub.n.values[-1],
            f" {g[:20]}", fontsize=7, color=color if color=="#2E7D32" else "#AAA",
            fontweight="bold" if color=="#2E7D32" else "normal", va="center")
    ax.set_xlim(2014.5, 2024); ax.set_ylabel("Titles Added")
    return fig, ax
make_slide(s3, "slide3_analysis.png", "International content is the fastest-growing category")

# Slide 4: Resolution
def s4():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    cyr = nf.dropna(subset=["primary_country"]).query("2016<=year_added<=2021")
    top10 = cyr.groupby("primary_country").size().nlargest(10).sort_values()
    colors = ["#E53935" if c=="India" else "#BBDEFB" for c in top10.index]
    ax.barh(top10.index, top10.values, color=colors, height=0.6)
    for i, (c, v) in enumerate(top10.items()):
        ax.text(v+10, i, f"{v:,}", va="center", fontsize=8, fontweight="bold")
    ax.set_xlabel("Total Titles")
    return fig, ax
make_slide(s4, "slide4_resolution.png", "India rose to #2 — invest in local-language content")

# Slide 5: Call to Action (text-based)
fig, ax = plt.subplots(figsize=(10, 5.5)); ax.axis("off")
actions = [
    ("1.", "Invest in 20 flagship originals per quarter", "Target: 80/year"),
    ("2.", "Grow India & Korea production 50%", "Target: +50% YoY"),
    ("3.", "Reduce catalog filler acquisitions", "Target: –30% YoY"),
    ("4.", "Launch 5 local-language content hubs", "Target: 5 by Q4")]
for i, (num, action, target) in enumerate(actions):
    y = 0.80 - i * 0.20
    ax.text(0.05, y, num, fontsize=14, fontweight="bold", color="#1565C0")
    ax.text(0.12, y, action, fontsize=11, fontweight="bold", color="#333")
    ax.text(0.12, y-0.06, target, fontsize=9, color="#888", fontstyle="italic")
ax.set_title("Reallocate content budget toward originals and local markets",
    fontsize=13, fontweight="bold", pad=15)
plt.tight_layout(); plt.savefig("output/slide5_cta.png", dpi=300); plt.close()

# ── PROGRESSIVE REVEAL: 4-panel build ────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for i, ax in enumerate(axes.flatten()):
    ax.set_xlim(2014.5, 2021.5); ax.set_ylim(0, peak_n * 1.15)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    if i >= 1:  # data
        ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2, markersize=5)
    if i >= 2:  # annotation
        ax.axhline(y=peak_n, ls=":", color="#888", lw=0.5)
        ax.annotate(f"–{decline}%", xy=(2020, (peak_n+latest_n)/2),
            fontsize=10, fontweight="bold", color="#E53935",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#E53935"))
    titles = ["Build 1: Frame (axes only)", "Build 2: + Data line",
        "Build 3: + Annotation", f"Build 4: + Assertion: 'Movies –{decline}%'"]
    ax.set_title(titles[i], fontsize=9, fontweight="bold")

fig.suptitle("Progressive Reveal: Build the Chart in 4 Steps", fontweight="bold")
plt.tight_layout(); plt.savefig("output/progressive_reveal.png", dpi=300); plt.close()

print("\nAll W07-M05 Python outputs saved")
print("Slides: slide1-5, progressive_reveal")
