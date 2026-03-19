"""W06-M03: Line Charts in Code — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True); np.random.seed(42)

months = pd.date_range("2020-01", "2023-12", freq="ME")
n = len(months)
val = 100 + np.cumsum(np.random.normal(0.5, 3, n))

# ── 1. ax.plot(): BASIC LINE CHART ──────────────────────
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(months, val, color="#1565C0", lw=1.5)
ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(MonthLocator(interval=6))
plt.setp(ax.get_xticklabels(), rotation=30, fontsize=7)
ax.set_title("ax.plot(): Continuous Time Series\n"
    "DateFormatter('%b %Y') + MonthLocator(interval=6)", fontweight="bold")
ax.set_ylabel("Value"); ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/line_basic.png", dpi=300); plt.close()

# ── 2. ax.step(): DISCRETE CHANGES ──────────────────────
rates = np.array([5.5]*12 + [4.5]*12 + [3.0]*12 + [3.5]*12)
change_dates = [pd.Timestamp("2021-01-01"), pd.Timestamp("2022-01-01"),
    pd.Timestamp("2023-01-01")]
change_rates = [4.5, 3.0, 3.5]

fig, ax = plt.subplots(figsize=(8, 4))
ax.step(months, rates, color="#E53935", lw=1.5, where="post")
ax.scatter(change_dates, change_rates, color="#E53935", s=40, zorder=5,
    edgecolors="white", lw=1)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.set_title("ax.step(): Discrete Rate Changes\n"
    "Horizontal segments + vertical jumps", fontweight="bold")
ax.set_ylabel("Interest Rate (%)"); ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/step_chart.png", dpi=300); plt.close()

# ── 3. fill_between(): AREA CHART ───────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.fill_between(months, val, alpha=0.3, color="#1565C0")
ax.plot(months, val, color="#1565C0", lw=0.8)
ax.xaxis.set_major_formatter(DateFormatter("%b\n%Y"))
ax.xaxis.set_major_locator(MonthLocator(interval=6))
ax.set_title("fill_between(): Filled Area\n"
    "Emphasises magnitude / cumulative volume", fontweight="bold")
ax.set_ylabel("Value"); ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/area_chart.png", dpi=300); plt.close()

# ── 4. stackplot(): STACKED AREA ────────────────────────
v1 = np.abs(np.random.normal(30, 5, n))
v2 = np.abs(np.random.normal(25, 5, n))
v3 = np.abs(np.random.normal(15, 5, n))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Absolute stacked
ax1.stackplot(months, v1, v2, v3, labels=["Product A", "Product B", "Product C"],
    colors=["#1565C0", "#E53935", "#2E7D32"], alpha=0.7)
ax1.legend(fontsize=7, loc="upper left")
ax1.set_title("Stacked Area: Absolute Values\n"
    "Bands sum to total", fontsize=10, fontweight="bold")
ax1.set_ylabel("Revenue (EUR)")
ax1.xaxis.set_major_formatter(DateFormatter("%Y"))

# 100% stacked
total = v1 + v2 + v3
ax2.stackplot(months, v1/total*100, v2/total*100, v3/total*100,
    labels=["Product A", "Product B", "Product C"],
    colors=["#1565C0", "#E53935", "#2E7D32"], alpha=0.7)
ax2.legend(fontsize=7, loc="upper left")
ax2.set_title("100% Stacked: Proportions\n"
    "Each point sums to 100%", fontsize=10, fontweight="bold")
ax2.set_ylabel("Share (%)")
ax2.xaxis.set_major_formatter(DateFormatter("%Y"))

for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/stacked_area.png", dpi=300); plt.close()

# ── 5. fill_between(): RIBBON (CONFIDENCE BAND) ─────────
lower = val - 8 - np.random.uniform(0, 3, n)
upper = val + 8 + np.random.uniform(0, 3, n)

fig, ax = plt.subplots(figsize=(8, 4))
ax.fill_between(months, lower, upper, alpha=0.15, color="#1565C0")
ax.plot(months, val, color="#1565C0", lw=1.5)
ax.set_title("fill_between(lower, upper): Confidence Ribbon\n"
    "Shaded region = uncertainty around central estimate", fontweight="bold")
ax.set_ylabel("Value"); ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(MonthLocator(interval=6))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/ribbon.png", dpi=300); plt.close()

# ── 6. SIX-PANEL COMPARISON DASHBOARD ───────────────────
fig = plt.figure(figsize=(14, 8))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)

ax = fig.add_subplot(gs[0,0])
ax.plot(months, val, color="#1565C0", lw=1.2)
ax.set_title("(a) Line: ax.plot()", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[0,1])
ax.step(months, rates, color="#E53935", lw=1.2, where="post")
ax.set_title("(b) Step: ax.step()", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[0,2])
ax.fill_between(months, val, alpha=0.3, color="#2E7D32")
ax.plot(months, val, color="#2E7D32", lw=0.5)
ax.set_title("(c) Area: fill_between()", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[1,0])
ax.stackplot(months, v1, v2, v3, colors=["#1565C0","#E53935","#2E7D32"], alpha=0.7)
ax.set_title("(d) Stacked: stackplot()", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[1,1])
ax.stackplot(months, v1/total*100, v2/total*100, v3/total*100,
    colors=["#1565C0","#E53935","#2E7D32"], alpha=0.7)
ax.set_title("(e) 100% Stacked", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[1,2])
ax.fill_between(months, lower, upper, alpha=0.15, color="#1565C0")
ax.plot(months, val, color="#1565C0", lw=1.2)
ax.set_title("(f) Ribbon: fill_between(CI)", fontsize=9, fontweight="bold")

for a in fig.get_axes():
    a.tick_params(labelsize=5); a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.xaxis.set_major_formatter(DateFormatter("%Y"))
fig.suptitle("Six Line Geometries in Python", fontsize=13, fontweight="bold")
plt.savefig("output/six_geoms.png", dpi=300, bbox_inches="tight"); plt.close()

# ── 7. DATE FORMATTING COMPARISON ───────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
fmts = [("%b %Y", "Jan 2020"), ("%Y-%m", "2020-01"),
        ("%Y", "2020"), ("%b\\n%Y", "Jan\\n2020")]
for ax, (fmt, desc) in zip(axes.flatten(), fmts):
    ax.plot(months[:24], val[:24], color="#1565C0", lw=1.2)
    ax.xaxis.set_major_formatter(DateFormatter(fmt.replace("\\n", "\n")))
    ax.xaxis.set_major_locator(MonthLocator(interval=3))
    ax.set_title(f"Format: '{fmt}' → {desc}", fontsize=9, fontweight="bold")
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Date Formatting Options in matplotlib", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/date_formats.png", dpi=300); plt.close()

# ── 8. REAL DATA: NETFLIX ───────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf = nf.dropna(subset=["date_added"]).query("date_added.dt.year >= 2015")

# Monthly additions
nf_monthly = nf.set_index("date_added").resample("ME").size()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Line chart
ax1.plot(nf_monthly.index, nf_monthly.values, color="#E53935", lw=1)
ax1.set_title("Netflix: Monthly Additions (line)", fontweight="bold")
ax1.set_ylabel("Titles Added")

# Stacked area by type
type_monthly = nf.set_index("date_added").groupby("type").resample("ME").size().unstack(0, fill_value=0)
if "Movie" in type_monthly and "TV Show" in type_monthly:
    ax2.stackplot(type_monthly.index,
        type_monthly["Movie"], type_monthly["TV Show"],
        labels=["Movie", "TV Show"],
        colors=["#1565C0", "#E53935"], alpha=0.7)
    ax2.legend(fontsize=7)
ax2.set_title("Netflix: Monthly Additions by Type (stacked area)", fontweight="bold")
ax2.set_ylabel("Titles Added")
ax2.xaxis.set_major_formatter(DateFormatter("%b %Y"))

for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/netflix_lines.png", dpi=300); plt.close()

# ── CHEATSHEET ───────────────────────────────────────────
print("\n=== Line Geometry Cheatsheet ===")
print("ax.plot(x, y)          → continuous line (default)")
print("ax.step(x, y, where=)  → discrete jumps ('pre','post','mid')")
print("ax.fill_between(x, y)  → filled area below line")
print("ax.stackplot(x,y1,y2)  → stacked area (parts of whole)")
print("ax.fill_between(x,lo,hi) → ribbon (confidence band)")
print("")
print("=== Date Formatting ===")
print("DateFormatter('%b %Y')  → Jan 2020")
print("DateFormatter('%Y-%m')  → 2020-01")
print("MonthLocator(interval=3) → tick every 3 months")
print("YearLocator()            → tick every year")

print("\nAll W06-M03 Python outputs saved")
