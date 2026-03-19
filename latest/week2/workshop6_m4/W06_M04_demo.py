"""W06-M04: Sparklines & Small Temporal Multiples — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter, YearLocator
os.makedirs("output", exist_ok=True)

# ── 1. LOAD NETFLIX DATA ────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year

# Top 6 genres
genres_all = nf["listed_in"].str.split(",").explode().str.strip()
top6 = genres_all.value_counts().head(6).index.tolist()

# Monthly additions per genre (2016–2021)
nf_genres = nf.assign(
    listed_in=nf["listed_in"].str.split(",")).explode("listed_in")
nf_genres["genre"] = nf_genres["listed_in"].str.strip()
nf_genres = nf_genres.query("genre in @top6 and 2016 <= year_added <= 2021")
nf_genres["month"] = nf_genres["date_added"].dt.to_period("M").dt.to_timestamp()
genre_monthly = nf_genres.groupby(["month", "genre"]).size().reset_index(name="n")

# ── 2. SPAGHETTI CHART (BAD) ────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
for g in top6:
    sub = genre_monthly.query("genre == @g")
    ax.plot(sub["month"], sub["n"], lw=0.8, label=g[:25])
ax.legend(fontsize=6, loc="upper left")
ax.set_title("BAD: Spaghetti (6 overlapping lines)\n"
    "Which genre grows fastest? Impossible to tell.", fontweight="bold")
ax.set_ylabel("Monthly Additions")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("output/spaghetti.png", dpi=300); plt.close()

# ── 3. SMALL TEMPORAL MULTIPLES ──────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=True)
for ax, g in zip(axes.flatten(), top6):
    sub = genre_monthly.query("genre == @g")
    ax.plot(sub["month"], sub["n"], color="#1565C0", lw=1)
    ax.set_title(g[:25], fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=5)
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("GOOD: Small Multiples — One Panel per Genre\n"
    "Shared x-axis, individual y-scales reveal each genre's pattern",
    fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/small_multiples.png", dpi=300); plt.close()

# ── 4. HIGHLIGHTED MULTIPLES ────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=True)
# Precompute all genre data for background
all_genre_data = {g: genre_monthly.query("genre == @g") for g in top6}

for ax, focal in zip(axes.flatten(), top6):
    # Grey background: all genres
    for g, gdata in all_genre_data.items():
        ax.plot(gdata["month"], gdata["n"], color="#EEEEEE", lw=0.4)
    # Red foreground: focal genre
    focal_data = all_genre_data[focal]
    ax.plot(focal_data["month"], focal_data["n"], color="#E53935", lw=1.5)
    ax.set_title(focal[:25], fontsize=9, fontweight="bold", color="#E53935")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=5)
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Highlighted Multiples: Focal Genre (red) vs All Others (grey)",
    fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/highlighted_multiples.png", dpi=300); plt.close()

# ── 5. SPARKLINE PANEL (Tufte-style) ────────────────────
fig, axes = plt.subplots(len(top6), 1, figsize=(8, 7))
for i, (ax, g) in enumerate(zip(axes, top6)):
    sub = genre_monthly.query("genre == @g").sort_values("month")
    x = sub["month"].values
    y = sub["n"].values

    # Line + subtle fill
    ax.plot(x, y, color="#1565C0", lw=0.7)
    ax.fill_between(x, y, alpha=0.06, color="#1565C0")

    # Min (red), Max (green), Current (blue)
    ax.scatter([x[np.argmin(y)]], [y.min()], s=18, c="#E53935", zorder=5)
    ax.scatter([x[np.argmax(y)]], [y.max()], s=18, c="#2E7D32", zorder=5)
    ax.scatter([x[-1]], [y[-1]], s=25, c="#1565C0", zorder=5)

    ax.set_xlim(x[0], x[-1])
    ax.axis("off")

    # Genre label on left, current value on right
    ax.text(x[0] - pd.Timedelta(days=30), np.mean(y), g[:20],
        fontsize=8, fontweight="bold", ha="right", va="center", color="#333")
    ax.text(x[-1] + pd.Timedelta(days=15), y[-1], f"{y[-1]:.0f}",
        fontsize=7, va="center", color="#1565C0", fontweight="bold")

fig.suptitle("Sparklines: Netflix Genre Trends (Tufte, 2006)\n"
    "Red = min, Green = max, Blue = current",
    fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/sparklines.png", dpi=300, bbox_inches="tight"); plt.close()

# ── 6. MOVIE vs TV SHOW SPARKLINES ──────────────────────
type_monthly = (nf.query("2016 <= year_added <= 2021")
    .dropna(subset=["date_added"])
    .assign(month=lambda d: d["date_added"].dt.to_period("M").dt.to_timestamp())
    .groupby(["month", "type"]).size().reset_index(name="n"))

fig, axes = plt.subplots(2, 1, figsize=(9, 4))
for ax, t, c in zip(axes, ["Movie", "TV Show"], ["#1565C0", "#E53935"]):
    sub = type_monthly.query("type == @t").sort_values("month")
    ax.plot(sub["month"], sub["n"], color=c, lw=1)
    ax.fill_between(sub["month"], sub["n"], alpha=0.08, color=c)
    # Peak (green dot) and current (coloured dot)
    ax.scatter([sub["month"].iloc[sub["n"].idxmax()]], [sub["n"].max()],
        s=30, c="#2E7D32", zorder=5)
    ax.scatter([sub["month"].iloc[-1]], [sub["n"].iloc[-1]],
        s=30, c=c, zorder=5)
    ax.set_title(f"{t}", fontsize=10, fontweight="bold", color=c)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Netflix: Movie vs TV Show Sparklines (2016–2021)\n"
    "Green = peak, Coloured = latest",
    fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/type_sparklines.png", dpi=300); plt.close()

# ── 7. COMPARISON SUMMARY TABLE (printed) ───────────────
print("\n=== Small Multiples Decision Table ===")
print(f"{'Scenario':<35} {'Recommendation':<25} {'Why'}")
print(f"{'-'*85}")
print(f"{'≤5 series, relationship matters':<35} {'Multi-line chart':<25} Crossovers visible")
print(f"{'6-12 series, individual patterns':<35} {'Small multiples':<25} Each panel clear")
print(f"{'10-50 series, overview only':<35} {'Sparklines in table':<25} Compact, scannable")
print(f"{'6-12 series + context needed':<35} {'Highlighted multiples':<25} Focal vs background")
print(f"{'Dashboard KPI row':<35} {'Sparklines inline':<25} Minimal space")

print("\nAll W06-M04 Python outputs saved")
