"""W06-M08: Case Study — Netflix Content Trends — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter, YearLocator
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True)

# ── 1. LOAD AND PREPARE ─────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["month_added"] = nf["date_added"].dt.month
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()

print(f"Dataset: {len(nf)} titles, {nf['date_added'].notna().sum()} with dates")
print(f"Range: {nf['date_added'].min()} to {nf['date_added'].max()}")

# ── 2. YEARLY ADDITIONS BY TYPE ─────────────────────────
yearly = (nf.query("2015 <= year_added <= 2021")
    .groupby(["year_added", "type"]).size()
    .reset_index(name="n"))

fig, ax = plt.subplots(figsize=(9, 5))
for t, c, m in [("Movie", "#1565C0", "o"), ("TV Show", "#E53935", "s")]:
    sub = yearly.query("type == @t")
    ax.plot(sub["year_added"], sub["n"], f"-{m}", color=c, lw=1.5,
        markersize=6, label=t)
    for _, row in sub.iterrows():
        ax.text(row["year_added"], row["n"] + 15, str(int(row["n"])),
            ha="center", fontsize=7, color=c, fontweight="bold")
ax.legend(fontsize=9)
ax.set_title("Netflix: Yearly Additions by Type (2015–2021)\n"
    "Movies peaked ~2019; TV Shows grew steadily", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/yearly_type.png", dpi=300); plt.close()

# ── 3. MONTHLY WITH EVENT ANNOTATIONS ───────────────────
monthly = (nf.dropna(subset=["date_added"])
    .query("date_added.dt.year >= 2015")
    .set_index("date_added")
    .resample("ME").size()
    .reset_index(name="n"))
monthly.columns = ["month", "n"]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly["month"], monthly["n"], color="#1565C0", lw=0.8)

# Event annotations
events = [
    (pd.Timestamp("2016-01-01"), "#2E7D32", "Global expansion\n(130 countries)", 0.95),
    (pd.Timestamp("2020-03-01"), "#E53935", "COVID-19\nlockdown", 0.85),
    (pd.Timestamp("2021-06-01"), "#E65100", "Content\nslowdown", 0.55)]
for date, color, label, y_frac in events:
    ax.axvline(x=date, ls="--", color=color, lw=0.6)
    ax.text(date + pd.Timedelta(days=30), monthly["n"].max() * y_frac,
        label, fontsize=7, color=color, ha="left")

ax.set_title("Netflix Monthly Additions + Event Annotations",
    fontweight="bold")
ax.set_ylabel("Titles Added"); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/monthly_annotated.png", dpi=300); plt.close()

# ── 4. GENRE EVOLUTION — GREY+ACCENT ────────────────────
genres = nf["listed_in"].str.split(",").explode().str.strip()
top5 = genres.value_counts().head(5).index.tolist()

nf_g = nf.assign(listed_in=nf["listed_in"].str.split(",")).explode("listed_in")
nf_g["genre"] = nf_g["listed_in"].str.strip()
genre_yr = (nf_g.query("genre in @top5 and 2015 <= year_added <= 2021")
    .groupby(["year_added", "genre"]).size()
    .reset_index(name="n"))

# Find fastest relative grower
growth_rates = {}
for g in top5:
    sub = genre_yr.query("genre == @g").sort_values("year_added")
    if len(sub) >= 2 and sub.iloc[0]["n"] > 0:
        growth_rates[g] = sub.iloc[-1]["n"] / sub.iloc[0]["n"]
fastest = max(growth_rates, key=growth_rates.get) if growth_rates else top5[0]

fig, ax = plt.subplots(figsize=(10, 5))
for g in top5:
    sub = genre_yr.query("genre == @g")
    if g == fastest:
        ax.plot(sub["year_added"], sub["n"], "-o", color="#E53935",
            lw=2.5, markersize=5, zorder=5)
        ax.text(sub["year_added"].values[-1] + 0.1, sub["n"].values[-1],
            f" {g}", fontsize=8, fontweight="bold", color="#E53935", va="center")
    else:
        ax.plot(sub["year_added"], sub["n"], "-o", color="#DDDDDD",
            lw=0.8, markersize=3)
        ax.text(sub["year_added"].values[-1] + 0.1, sub["n"].values[-1],
            f" {g}", fontsize=6, color="#AAAAAA", va="center")

ax.set_xlim(2014.5, 2023)
ax.set_title(f"Top 5 Genre Trends: Grey+Accent on Fastest Grower ({fastest})",
    fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/genre_trends.png", dpi=300); plt.close()

# ── 5. CUMULATIVE STACKED AREA BY TYPE ──────────────────
type_m = (nf.dropna(subset=["date_added"])
    .query("date_added.dt.year >= 2015")
    .assign(month=lambda d: d["date_added"].dt.to_period("M").dt.to_timestamp())
    .groupby(["month", "type"]).size()
    .unstack(fill_value=0)
    .cumsum())

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Absolute cumulative
if "Movie" in type_m and "TV Show" in type_m:
    ax1.stackplot(type_m.index, type_m["Movie"], type_m["TV Show"],
        labels=["Movie", "TV Show"], colors=["#1565C0", "#E53935"], alpha=0.7)
ax1.legend(fontsize=8)
ax1.set_title("(a) Cumulative Catalog: Absolute", fontweight="bold")
ax1.set_ylabel("Cumulative Titles")

# Percentage
if "Movie" in type_m and "TV Show" in type_m:
    total = type_m.sum(axis=1)
    ax2.stackplot(type_m.index,
        type_m["Movie"] / total * 100, type_m["TV Show"] / total * 100,
        labels=["Movie", "TV Show"], colors=["#1565C0", "#E53935"], alpha=0.7)
ax2.legend(fontsize=8)
ax2.set_title("(b) Catalog Composition: % by Type", fontweight="bold")
ax2.set_ylabel("Share (%)")
ax2.xaxis.set_major_formatter(DateFormatter("%Y"))

for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/cumulative_stacked.png", dpi=300); plt.close()

# ── 6. SEASONAL SUBSERIES ───────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
months = np.arange(1, 13)

for yr in range(2016, 2022):
    sub = nf.query("year_added == @yr").groupby("month_added").size()
    sub = sub.reindex(range(1, 13), fill_value=0)
    color = "#E53935" if yr == 2021 else "#BBBBBB"
    alpha = 1.0 if yr == 2021 else 0.3
    lw = 1.8 if yr == 2021 else 0.7
    ms = 4 if yr == 2021 else 1.5
    label = str(yr) if yr in [2016, 2021] else None
    ax.plot(months, sub.values, "-o", color=color, alpha=alpha,
        lw=lw, markersize=ms, label=label)

ax.set_xticks(months); ax.set_xticklabels(month_labels)
ax.legend(fontsize=8)
ax.set_title("Seasonal Pattern: Monthly Additions (2016–2021)\n"
    "Grey = 2016–2020, Red = 2021", fontweight="bold")
ax.set_ylabel("Titles Added")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/seasonal_subseries.png", dpi=300); plt.close()

# ── 7. TOP 5 COUNTRIES ──────────────────────────────────
top5_countries = (nf.dropna(subset=["primary_country"])
    ["primary_country"].value_counts().head(5).index.tolist())
country_yr = (nf.query("primary_country in @top5_countries and 2016 <= year_added <= 2021")
    .groupby(["year_added", "primary_country"]).size()
    .reset_index(name="n"))

fig, ax = plt.subplots(figsize=(9, 5))
for country in top5_countries:
    sub = country_yr.query("primary_country == @country")
    ax.plot(sub["year_added"], sub["n"], "-o", lw=1.2, markersize=4, label=country)
ax.legend(fontsize=7)
ax.set_title("Top 5 Countries: Yearly Additions", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/country_trends.png", dpi=300); plt.close()

# ── 8. KEY FINDINGS ──────────────────────────────────────
movie_peak = yearly.query("type == 'Movie'").nlargest(1, "n")
print(f"\n=== KEY FINDINGS ===")
print(f"1. Movie peak: {int(movie_peak['year_added'].values[0])} "
    f"({int(movie_peak['n'].values[0])} titles). Declined after.")
print(f"2. TV pivot: TV Shows grew every year 2015–2020")
print(f"3. Fastest-growing genre (relative): {fastest}")
print(f"4. COVID visible as dip in monthly additions mid-2020")
print(f"5. Seasonal: releases cluster in December/January (holiday)")
print(f"6. Top country: {top5_countries[0]}")

print("\nAll W06-M08 Python outputs saved")
