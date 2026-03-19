"""W06-M01: Time as a Visual Dimension — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. SIMULATED DAILY TIME SERIES
dates = pd.date_range("2020-01-01", "2023-12-31", freq="D")
n = len(dates)
trend = 100 + 0.05 * np.arange(n)
seasonal = 15 * np.sin(2 * np.pi * np.arange(n) / 365)
residual = np.random.normal(0, 5, n)
value = trend + seasonal + residual
daily = pd.DataFrame({"date": dates, "value": value}).set_index("date")
print(f"Daily series: {len(daily)} observations, {daily.index.min()} to {daily.index.max()}")

# 2. GRANULARITY COMPARISON
weekly = daily.resample("W").mean()
monthly = daily.resample("ME").mean()
yearly = daily.resample("YE").mean()

fig, axes = plt.subplots(2, 2, figsize=(12, 7))
for ax, data, title, color in zip(axes.flatten(),
    [daily, weekly, monthly, yearly],
    ["(a) Daily", "(b) Weekly", "(c) Monthly", "(d) Yearly"],
    ["#BBBBBB", "#1565C0", "#E53935", "#2E7D32"]):
    ax.plot(data.index, data["value"], color=color, lw=0.5 if "Daily" in title else 1.5)
    if "Monthly" in title or "Yearly" in title:
        ax.plot(data.index, data["value"], "o", color=color, markersize=3 if "Monthly" in title else 6)
    ax.set_title(title, fontsize=9, fontweight="bold", color=color)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
fig.suptitle("Same Data, Four Granularities", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/granularity.png", dpi=300); plt.close()

# 3. DECOMPOSITION
try:
    from statsmodels.tsa.seasonal import STL
    stl = STL(daily["value"], period=365, robust=True)
    res = stl.fit()

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    panels = [(daily["value"], "Observed", "#333"),
              (res.trend, "Trend", "#1565C0"),
              (res.seasonal, "Seasonal", "#2E7D32"),
              (res.resid, "Residual", "#E53935")]
    for ax, (data, title, color) in zip(axes, panels):
        ax.plot(data.index, data.values, color=color, lw=0.5)
        ax.set_title(title, fontsize=9, fontweight="bold", color=color, loc="left")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
    fig.suptitle("STL Decomposition: Trend + Seasonal + Residual", fontsize=12, fontweight="bold")
    plt.tight_layout(); plt.savefig("output/decomposition.png", dpi=300); plt.close()
    print("STL decomposition saved")
except ImportError:
    print("statsmodels not available — skipping decomposition")

# 4. CHART TYPE COMPARISON
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
# Line
axes[0,0].plot(monthly.index, monthly["value"], color="#1565C0", lw=1.5)
axes[0,0].set_title("(a) Line Chart", fontsize=9, fontweight="bold")
# Area
axes[0,1].fill_between(monthly.index, monthly["value"], alpha=0.3, color="#1565C0")
axes[0,1].plot(monthly.index, monthly["value"], color="#1565C0", lw=0.8)
axes[0,1].set_title("(b) Area Chart", fontsize=9, fontweight="bold")
# Step
axes[1,0].step(monthly.index, monthly["value"], color="#E53935", lw=1.5, where="mid")
axes[1,0].set_title("(c) Step Chart", fontsize=9, fontweight="bold")
# Bar
axes[1,1].bar(monthly.index, monthly["value"], width=25, color="#7B1FA2", alpha=0.7)
axes[1,1].set_title("(d) Bar (monthly)", fontsize=9, fontweight="bold")
for ax in axes.flatten():
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6); ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
fig.suptitle("Four Temporal Chart Types: Same Monthly Data", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/chart_types.png", dpi=300); plt.close()

# 5. PITFALL: CATEGORICAL vs DATE AXIS
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
bad_dates_str = ["2020-01", "2020-06", "2020-12", "2022-01", "2023-06"]
vals = [10, 15, 18, 22, 28]
ax1.plot(range(len(bad_dates_str)), vals, "-o", color="#E53935", lw=2, markersize=6)
ax1.set_xticks(range(len(bad_dates_str))); ax1.set_xticklabels(bad_dates_str, fontsize=7, rotation=30)
ax1.set_title("BAD: Categorical spacing", fontsize=9, fontweight="bold", color="#C62828")

real_dates = pd.to_datetime([d + "-01" for d in bad_dates_str])
ax2.plot(real_dates, vals, "-o", color="#1565C0", lw=2, markersize=6)
ax2.set_title("GOOD: True date axis", fontsize=9, fontweight="bold", color="#1565C0")
ax2.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
for ax in [ax1, ax2]: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Time Axis Pitfall: Always Use True Date Spacing", fontsize=11, fontweight="bold")
plt.tight_layout(); plt.savefig("output/pitfall_axis.png", dpi=300); plt.close()

# 6. DATE FORMATTING CHEATSHEET
print("\n── pandas resample codes ──")
print("  D=daily, W=weekly, ME=month-end, MS=month-start")
print("  QE=quarter-end, YE=year-end")
print("── matplotlib DateFormatter ──")
print("  %Y=year, %m=month, %d=day, %b=abbrev month, %B=full month")

print("\nAll W06-M01 Python outputs saved")
