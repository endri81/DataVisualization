"""W06-M05: Seasonal & Calendar Visualizations — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True); np.random.seed(42)

# ── 1. SIMULATED DAILY DATA ─────────────────────────────
dates = pd.date_range("2022-01-01", "2023-12-31", freq="D")
n = len(dates)
weekday_eff = np.where(dates.dayofweek < 5, 4, 0)
seasonal_eff = 3 * np.sin(2 * np.pi * dates.dayofyear / 365)
noise = np.random.poisson(5, n)
activity = weekday_eff + seasonal_eff + noise + 8
daily = pd.DataFrame({"date": dates, "value": activity.clip(0)})
daily["dow"] = daily["date"].dt.dayofweek  # 0=Mon, 6=Sun
daily["week"] = daily["date"].dt.isocalendar().week.astype(int)
daily["year"] = daily["date"].dt.year
print(f"Daily data: {len(daily)} rows, {daily.date.min()} to {daily.date.max()}")

# ── 2. CALENDAR HEATMAP (2023) ──────────────────────────
cal = daily.query("year == 2023")
pivot = cal.pivot_table(index="dow", columns="week", values="value", aggfunc="mean")

fig, ax = plt.subplots(figsize=(14, 3.5))
im = ax.imshow(pivot.values, cmap="YlGn", aspect="auto", interpolation="nearest")
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=7)
ax.set_xlabel("Week of Year", fontsize=8)
ax.set_title("Calendar Heatmap: 2023 Activity (DOW × Week)", fontsize=11, fontweight="bold")
plt.colorbar(im, ax=ax, shrink=0.6, label="Activity")
ax.tick_params(labelsize=5)
plt.tight_layout(); plt.savefig("output/calendar_heatmap.png", dpi=300); plt.close()

# ── 3. NETFLIX SEASONAL SUBSERIES ───────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["month_added"] = nf["date_added"].dt.month
nf_filt = nf.query("2016 <= year_added <= 2021").dropna(subset=["year_added"])
monthly_yr = nf_filt.groupby(["year_added", "month_added"]).size().reset_index(name="n")

fig, ax = plt.subplots(figsize=(9, 5))
month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
for yr in sorted(monthly_yr.year_added.unique()):
    sub = monthly_yr.query("year_added == @yr")
    color = "#E53935" if yr == 2021 else "#CCCCCC"
    alpha = 1.0 if yr == 2021 else 0.3
    lw = 2.0 if yr == 2021 else 0.7
    ms = 5 if yr == 2021 else 2
    ax.plot(sub.month_added, sub.n, "-o", color=color, alpha=alpha,
        lw=lw, markersize=ms, label=str(int(yr)) if yr in [2016, 2021] else None)
ax.set_xticks(range(1, 13)); ax.set_xticklabels(month_labels, fontsize=8)
ax.legend(fontsize=7); ax.set_ylabel("Titles Added")
ax.set_title("Netflix Seasonal Subseries: 2016–2021 (2021 highlighted)",
    fontsize=11, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/seasonal_subseries.png", dpi=300); plt.close()

# ── 4. MONTHLY BOXPLOT ──────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
data_by_month = [monthly_yr.query("month_added == @m")["n"].values for m in range(1, 13)]
bp = ax.boxplot(data_by_month, labels=month_labels, patch_artist=True, widths=0.5,
    flierprops=dict(markersize=3))
for patch in bp["boxes"]:
    patch.set_facecolor("#BBDEFB"); patch.set_edgecolor("#1565C0")
for med in bp["medians"]:
    med.set_color("#C62828"); med.set_linewidth(1.5)
# Mean line overlay
means = [monthly_yr.query("month_added == @m")["n"].mean() for m in range(1, 13)]
ax.plot(range(1, 13), means, "-o", color="#E53935", lw=1.5, markersize=4, zorder=5, label="Mean")
ax.legend(fontsize=7)
ax.set_title("Monthly Boxplot: Netflix Addition Distribution by Month",
    fontsize=11, fontweight="bold")
ax.set_ylabel("Titles per Month"); ax.set_xlabel("Month")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/monthly_boxplot.png", dpi=300); plt.close()

# ── 5. POLAR TIME PLOT ──────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
bars = ax.bar(angles, means, width=0.4, color="#1565C0", alpha=0.7)
ax.set_xticks(angles)
ax.set_xticklabels(month_labels, fontsize=8, fontweight="bold")
ax.set_title("Polar: Average Monthly Netflix Additions", fontsize=11,
    fontweight="bold", pad=20)
plt.tight_layout(); plt.savefig("output/polar_month.png", dpi=300); plt.close()

# ── 6. MONTH × YEAR HEATMAP ─────────────────────────────
pivot_yr = monthly_yr.pivot_table(index="year_added", columns="month_added",
    values="n", aggfunc="sum")
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(pivot_yr.values, cmap="Blues", aspect="auto")
# Annotate cells
for i in range(pivot_yr.shape[0]):
    for j in range(pivot_yr.shape[1]):
        val = pivot_yr.values[i, j]
        if not np.isnan(val):
            ax.text(j, i, f"{int(val)}", ha="center", va="center",
                fontsize=7, fontweight="bold",
                color="white" if val > pivot_yr.values[~np.isnan(pivot_yr.values)].mean() else "black")
ax.set_xticks(range(12)); ax.set_xticklabels(month_labels, fontsize=8)
ax.set_yticks(range(len(pivot_yr.index)))
ax.set_yticklabels([str(int(y)) for y in pivot_yr.index], fontsize=8)
ax.set_title("Heatmap: Netflix Additions (Month × Year)", fontsize=11, fontweight="bold")
plt.colorbar(im, ax=ax, shrink=0.7, label="Titles Added")
plt.tight_layout(); plt.savefig("output/month_year_heatmap.png", dpi=300); plt.close()

# ── 7. COMPARISON: LINEAR vs POLAR ──────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5),
    gridspec_kw={"width_ratios": [2, 1]})
# Linear bar
ax1.bar(range(1, 13), means, color="#1565C0", width=0.5, alpha=0.7)
ax1.set_xticks(range(1, 13)); ax1.set_xticklabels(month_labels, fontsize=8)
ax1.set_title("Linear Bar: Easier to compare values", fontsize=10, fontweight="bold")
ax1.set_ylabel("Mean Titles"); ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
# Polar bar
ax2 = fig.add_subplot(122, polar=True)
ax2.bar(angles, means, width=0.4, color="#1565C0", alpha=0.7)
ax2.set_xticks(angles); ax2.set_xticklabels(month_labels, fontsize=7)
ax2.set_title("Polar: Emphasises cyclical nature", fontsize=10, fontweight="bold", pad=15)
fig.suptitle("Linear vs Polar: Same Monthly Data, Different Emphasis", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/linear_vs_polar.png", dpi=300); plt.close()

print("\nAll W06-M05 Python outputs saved")
print("Figures: calendar_heatmap, seasonal_subseries, monthly_boxplot,")
print("  polar_month, month_year_heatmap, linear_vs_polar")
