"""W06-M09: Case Study — e-Car Temporal Analysis — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True)

# ── 1. LOAD AND PREPARE ─────────────────────────────────
ec = pd.read_csv("ecar.csv")
ec.columns = [c.strip().replace("  ", " ") for c in ec.columns]
ec["ApproveDate"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce")
ec["Year"] = ec["ApproveDate"].dt.year
ec["Month"] = ec["ApproveDate"].dt.month
ec["Quarter"] = ec["ApproveDate"].dt.quarter
ec["YearMonth"] = ec["ApproveDate"].dt.to_period("M").dt.to_timestamp()
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec["Approved"] = ec["Outcome"] == 1
ec = ec.query("2002 <= Year <= 2012")

print(f"Dataset: {len(ec)} loans, {ec['Year'].min()}–{ec['Year'].max()}")

# ── 2. YEARLY RATE + SPREAD + CoF ───────────────────────
yr = ec.groupby("Year").agg(
    rate=("Rate", "mean"), spread=("Spread", "mean"),
    cof=("Cost of Funds", "mean"), volume=("Rate", "size"),
    approval=("Approved", "mean")).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(yr.Year, yr.rate, "-o", color="#1565C0", lw=1.5, markersize=5, label="Offered Rate")
ax.plot(yr.Year, yr.spread, "-s", color="#E53935", lw=1.5, markersize=5, label="Spread")
ax.plot(yr.Year, yr.cof, "--^", color="#2E7D32", lw=1, markersize=4, label="Cost of Funds")
# 2008 annotation
ax.axvspan(2007.5, 2009.5, alpha=0.05, color="#E53935")
ax.axvline(x=2008, ls="--", color="#888", lw=0.6)
ax.text(2008, yr.rate.max() * 0.95, "2008\nCrisis", fontsize=8,
    fontweight="bold", color="#888", ha="center")
ax.legend(fontsize=8)
ax.set_title("e-Car: Rate, Cost of Funds, and Spread (2002–2012)\n"
    "Rate dropped post-2008 (Fed cuts); Spread compressed then recovered",
    fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Percentage Points")
ax.set_xticks(range(2002, 2013))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/rate_spread_cof.png", dpi=300); plt.close()

# ── 3. VOLUME + APPROVAL ────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.bar(yr.Year, yr.volume / 1000, color="#2E7D32", width=0.6, alpha=0.7)
for _, row in yr.iterrows():
    ax1.text(row.Year, row.volume/1000 + 0.3, f"{row.volume/1000:.1f}k",
        ha="center", fontsize=6, fontweight="bold")
ax1.axvline(x=2008, ls="--", color="#888")
ax1.set_title("(a) Loan Volume (thousands/year)", fontweight="bold")
ax1.set_ylabel("Loans (000s)"); ax1.set_xticks(range(2002, 2013))
ax1.tick_params(labelsize=7)

ax2.plot(yr.Year, yr.approval * 100, "-o", color="#7B1FA2", lw=1.5, markersize=5)
for _, row in yr.iterrows():
    ax2.text(row.Year, row.approval*100 + 0.8, f"{row.approval*100:.1f}%",
        ha="center", fontsize=6, color="#7B1FA2", fontweight="bold")
ax2.axvline(x=2008, ls="--", color="#888")
ax2.set_title("(b) Approval Rate (%)", fontweight="bold")
ax2.set_ylabel("Approval %"); ax2.set_xticks(range(2002, 2013))
ax2.tick_params(labelsize=7)

for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/volume_approval.png", dpi=300); plt.close()

# ── 4. QUARTERLY RATE WITH CI RIBBON ─────────────────────
qr = ec.groupby(["Year", "Quarter"]).agg(
    rate=("Rate", "mean"), se=("Rate", "sem"), n=("Rate", "size")).reset_index()
qr["date"] = pd.to_datetime(
    qr.apply(lambda r: f"{int(r.Year)}-{int(r.Quarter)*3-2:02d}-01", axis=1))
qr["lower"] = qr.rate - 1.96 * qr.se
qr["upper"] = qr.rate + 1.96 * qr.se

fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(qr.date, qr.lower, qr.upper, alpha=0.15, color="#1565C0")
ax.plot(qr.date, qr.rate, color="#1565C0", lw=0.8)
ax.axvline(x=pd.Timestamp("2008-09-15"), ls="--", color="#E53935", lw=0.8)
ax.annotate("Lehman\ncollapse", xy=(pd.Timestamp("2008-09-15"), qr.rate.max() * 0.95),
    xytext=(pd.Timestamp("2009-03-01"), qr.rate.max() * 0.90),
    fontsize=8, fontweight="bold", color="#E53935",
    arrowprops=dict(arrowstyle="->", color="#E53935", lw=0.8))
ax.set_title("Quarterly Mean Rate ± 95% CI\n"
    "CI widens during crisis = more pricing volatility", fontweight="bold")
ax.set_ylabel("Rate (%)"); ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/quarterly_ci.png", dpi=300); plt.close()

# ── 5. RATE BY TIER — SMALL MULTIPLES ───────────────────
tiers = sorted(ec["Tier"].unique())
fig, axes = plt.subplots(1, len(tiers), figsize=(14, 4), sharey=True)
for ax, tier in zip(axes, tiers):
    ty = ec.query("Tier == @tier").groupby("Year")["Rate"].mean()
    ax.plot(ty.index, ty.values, "-o", color="#1565C0", lw=1, markersize=3)
    ax.axvline(x=2008, ls="--", color="#888", lw=0.3)
    ax.set_title(f"Tier {tier}", fontsize=9, fontweight="bold")
    ax.set_xticks([2002, 2005, 2008, 2012]); ax.tick_params(labelsize=5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
axes[0].set_ylabel("Mean Rate (%)", fontsize=8)
fig.suptitle("Rate by Credit Tier (2002–2012): All tiers dropped post-2008",
    fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/tier_multiples.png", dpi=300); plt.close()

# Grey+accent on Tier 1
fig, ax = plt.subplots(figsize=(10, 5))
tier_yr = ec.groupby(["Year", "Tier"])["Rate"].mean().reset_index()
for tier in tiers:
    sub = tier_yr.query("Tier == @tier")
    ax.plot(sub.Year, sub.Rate, color="#DDDDDD", lw=0.7)
sub1 = tier_yr.query("Tier == 1")
ax.plot(sub1.Year, sub1.Rate, color="#E53935", lw=2.5, label="Tier 1 (best credit)")
for tier in tiers:
    sub = tier_yr.query("Tier == @tier")
    color = "#E53935" if tier == 1 else "#AAAAAA"
    ax.text(sub.Year.values[-1] + 0.15, sub.Rate.values[-1],
        f"T{tier}", fontsize=7, fontweight="bold", color=color, va="center")
ax.axvline(x=2008, ls="--", color="#888")
ax.set_title("Rate by Tier: Grey+Accent on Tier 1\n"
    "Tier 1 dropped most (banks competed for safest borrowers)", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Mean Rate (%)")
ax.set_xticks(range(2002, 2013)); ax.set_xlim(2001.5, 2013.5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/tier_accent.png", dpi=300); plt.close()

# ── 6. SPREAD: PRE vs POST 2008 ─────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
pre = ec.query("Year < 2008")["Spread"]
post = ec.query("Year >= 2008")["Spread"]
ax.hist(pre, bins=50, alpha=0.5, color="#1565C0",
    label=f"Pre-2008 (med={pre.median():.2f})")
ax.hist(post, bins=50, alpha=0.5, color="#E53935",
    label=f"Post-2008 (med={post.median():.2f})")
ax.axvline(x=pre.median(), ls="--", color="#1565C0", lw=1.5)
ax.axvline(x=post.median(), ls="--", color="#E53935", lw=1.5)
ax.legend(fontsize=9)
ax.set_title("Spread Distribution: Pre vs Post 2008\n"
    "Post-2008 spread compressed (dashed = median)", fontweight="bold")
ax.set_xlabel("Spread (pp)"); ax.set_ylabel("Count")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/spread_pre_post.png", dpi=300); plt.close()

# ── 7. STL DECOMPOSITION OF MONTHLY RATE ────────────────
try:
    from statsmodels.tsa.seasonal import STL
    monthly_rate = ec.groupby("YearMonth")["Rate"].mean().sort_index()
    stl = STL(monthly_rate, period=12, robust=True)
    res = stl.fit()

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    panels = [(monthly_rate, "Observed", "#333"),
              (res.trend, "Trend", "#1565C0"),
              (res.seasonal, "Seasonal", "#2E7D32"),
              (res.resid, "Residual", "#E53935")]
    for ax, (data, title, color) in zip(axes, panels):
        ax.plot(data.index, data.values, color=color, lw=0.6)
        ax.axvline(x=pd.Timestamp("2008-09-15"), ls="--", color="#888", lw=0.3)
        ax.set_title(title, fontsize=9, fontweight="bold", color=color, loc="left")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=6)
    fig.suptitle("STL Decomposition: Monthly Mean Rate (2002–2012)", fontweight="bold")
    plt.tight_layout(); plt.savefig("output/rate_stl.png", dpi=300); plt.close()
    print("STL decomposition saved")
except ImportError:
    print("statsmodels not available — skipping STL")

# ── 8. KEY FINDINGS ──────────────────────────────────────
print(f"\n=== KEY FINDINGS ===")
print(f"1. Rate peak: {yr.rate.max():.2f}% in {int(yr.loc[yr.rate.idxmax(),'Year'])}")
print(f"2. Rate trough: {yr.rate.min():.2f}% in {int(yr.loc[yr.rate.idxmin(),'Year'])}")
print(f"3. Spread pre-2008 median: {pre.median():.2f}pp")
print(f"4. Spread post-2008 median: {post.median():.2f}pp")
print(f"5. Volume peak: {int(yr.volume.max()):,} in {int(yr.loc[yr.volume.idxmax(),'Year'])}")
print(f"6. Approval range: {yr.approval.min()*100:.1f}–{yr.approval.max()*100:.1f}%")

print("\nAll W06-M09 Python outputs saved")
