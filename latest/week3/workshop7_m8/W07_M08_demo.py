"""W07-M08: Case Study — e-Car Data Story — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True)

plt.rcParams.update({
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#EEE", "axes.labelcolor": "#888",
    "xtick.color": "#888", "ytick.color": "#888",
    "grid.alpha": 0, "font.size": 10, "axes.titleweight": "bold"})

ec = pd.read_csv("ecar.csv"); ec.columns=[c.strip().replace("  "," ") for c in ec.columns]
ec["ApproveDate"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce")
ec["Year"] = ec["ApproveDate"].dt.year; ec["Quarter"] = ec["ApproveDate"].dt.quarter
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec = ec.query("2002<=Year<=2012")
yr = ec.groupby("Year").agg(rate=("Rate","mean"), cof=("Cost of Funds","mean"),
    spread=("Spread","mean"), volume=("Rate","size"), approval=("Outcome","mean")).reset_index()

peak_rate = yr.rate.max(); trough_rate = yr.rate.min()
drop_pp = round(peak_rate - trough_rate, 1)

# ═══ S1: CONTEXT ═══
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(yr.Year, yr.volume/1000, color="#1565C0", width=0.6, alpha=0.7)
for _, row in yr.iterrows():
    ax.text(row.Year, row.volume/1000+0.3, f"{row.volume/1000:.1f}k",
        ha="center", fontsize=7, fontweight="bold", color="#1565C0")
ax.set_xticks(range(2002,2013))
ax.set_title("150,000 auto loans processed across five credit tiers (2002–2012)", fontsize=14)
ax.set_ylabel("Loans (thousands)")
plt.tight_layout(); plt.savefig("output/s1_context.png", dpi=300); plt.close()

# ═══ S2: HERO — Rate drop ═══
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axvspan(2007.5, 2009.5, alpha=0.04, color="#E53935")
ax.plot(yr.Year, yr.spread, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(yr.Year, yr.rate, "-o", color="#1565C0", lw=3, markersize=7)
ax.axhline(y=peak_rate, ls=":", color="#CCC", lw=0.5)
ax.annotate(f"–{drop_pp}pp rate drop\n(Fed response to crisis)",
    xy=(2009, trough_rate), xytext=(2004, trough_rate*0.85),
    fontsize=11, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#E53935", lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.3", color="#E53935", lw=1.5))
ax.annotate("Lehman\ncollapse", xy=(2008, yr.query("Year==2008").rate.values[0]),
    xytext=(2008, peak_rate+0.3), fontsize=8, fontweight="bold", color="#888", ha="center",
    arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
ax.text(2012.2, yr.iloc[-1].rate, " Rate", fontsize=10, fontweight="bold", color="#1565C0", va="center")
ax.text(2012.2, yr.iloc[-1].spread, " Spread", fontsize=9, color="#BBB", va="center")
ax.set_xlim(2001.5, 2013.5); ax.set_xticks(range(2002,2013))
ax.set_title(f"Loan rates dropped {drop_pp}pp after the 2008 financial crisis", fontsize=14)
ax.set_ylabel("Percentage Points")
plt.tight_layout(); plt.savefig("output/s2_hero.png", dpi=300); plt.close()

# ═══ S3: MECHANISM — 3-line decomposition ═══
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axvspan(2007.5, 2009.5, alpha=0.03, color="#E53935")
ax.plot(yr.Year, yr.rate, "-o", color="#1565C0", lw=2, markersize=5, label="Offered Rate")
ax.plot(yr.Year, yr.cof, "--^", color="#2E7D32", lw=1.5, markersize=4, label="Cost of Funds")
ax.plot(yr.Year, yr.spread, "-s", color="#E53935", lw=1.5, markersize=4, label="Spread")
ax.text(2012.2, yr.iloc[-1].rate, " Rate", fontsize=9, fontweight="bold", color="#1565C0", va="center")
ax.text(2012.2, yr.iloc[-1].cof, " CoF", fontsize=8, color="#2E7D32", va="center")
ax.text(2012.2, yr.iloc[-1].spread, " Spread", fontsize=8, color="#E53935", va="center")
ax.set_xlim(2001.5, 2013.5); ax.set_xticks(range(2002,2013))
ax.set_title("The mechanism: Fed cut Cost of Funds; spread compressed under competition", fontsize=13)
ax.set_ylabel("Percentage Points")
plt.tight_layout(); plt.savefig("output/s3_mechanism.png", dpi=300); plt.close()

# ═══ S4: TIER IMPACT — grey+accent ═══
tier_yr = ec.groupby(["Year","Tier"])["Rate"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5.5))
for tier in sorted(ec.Tier.unique()):
    sub = tier_yr.query("Tier==@tier")
    c = "#E53935" if tier==1 else "#DDD"; lw = 2.5 if tier==1 else 0.7
    ax.plot(sub.Year, sub.Rate, "-o", color=c, lw=lw, markersize=3 if tier>1 else 5)
    ax.text(sub.Year.values[-1]+0.15, sub.Rate.values[-1],
        f"T{tier}", fontsize=7, fontweight="bold" if tier==1 else "normal",
        color=c if c=="#E53935" else "#AAA", va="center")
ax.axvline(x=2008, ls="--", color="#888", lw=0.3)
ax.set_xlim(2001.5, 2013.5); ax.set_xticks(range(2002,2013))
ax.set_title("Tier 1 borrowers received the largest rate cuts — a regressive benefit", fontsize=13)
ax.set_ylabel("Mean Rate (%)")
plt.tight_layout(); plt.savefig("output/s4_tiers.png", dpi=300); plt.close()

# ═══ S5: UNCERTAINTY — CI ribbon ═══
qr = ec.groupby(["Year","Quarter"]).agg(rate=("Rate","mean"), se=("Rate","sem")).reset_index()
qr["date"] = pd.to_datetime(qr.apply(lambda r: f"{int(r.Year)}-{int(r.Quarter)*3-2:02d}-01", axis=1))
qr["lower"] = qr.rate - 1.96*qr.se; qr["upper"] = qr.rate + 1.96*qr.se

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.fill_between(qr.date, qr.lower, qr.upper, alpha=0.15, color="#1565C0")
ax.plot(qr.date, qr.rate, color="#1565C0", lw=0.8)
ax.axvline(x=pd.Timestamp("2008-09-15"), ls="--", color="#E53935", lw=0.6)
ax.annotate("CI widens during crisis\n= pricing uncertainty",
    xy=(pd.Timestamp("2008-10-01"), qr.upper.max()*0.92),
    xytext=(pd.Timestamp("2010-01-01"), qr.upper.max()*0.98),
    fontsize=9, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"),
    arrowprops=dict(arrowstyle="->", color="#E53935", lw=1))
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
ax.set_title("Quarterly CI width is an early warning indicator of financial stress", fontsize=13)
ax.set_ylabel("Rate (%)")
plt.tight_layout(); plt.savefig("output/s5_uncertainty.png", dpi=300); plt.close()

# ═══ S6: RECOVERY ═══
fig, ax = plt.subplots(figsize=(10, 5.5))
periods = ["Pre-crisis\n(2002–2007)", "Crisis\n(2008–2009)", "Recovery\n(2010–2012)"]
spreads = [ec.query("Year<2008").Spread.median(),
    ec.query("2008<=Year<=2009").Spread.median(),
    ec.query("Year>=2010").Spread.median()]
colors = ["#1565C0", "#E53935", "#2E7D32"]
ax.bar(periods, spreads, color=colors, width=0.4)
for i, v in enumerate(spreads):
    ax.text(i, v+0.05, f"{v:.1f}pp", ha="center", fontsize=11, fontweight="bold", color=colors[i])
ax.set_title("Spread recovered post-2010 but never returned to pre-crisis levels", fontsize=13)
ax.set_ylabel("Median Spread (pp)")
plt.tight_layout(); plt.savefig("output/s6_recovery.png", dpi=300); plt.close()

# ═══ KEY OUTPUT ═══
print(f"\n=== e-Car Data Story Deck ===")
print(f"Big Idea: 'The bank should integrate CI-based pricing volatility")
print(f"  monitoring because the 2008 crisis caused a {drop_pp}pp rate drop")
print(f"  with differential tier impact and slow spread recovery.'")
print(f"\nStory arc:")
print(f"  1. Context: 150K loans, 5 tiers")
print(f"  2. Complication: –{drop_pp}pp rate drop")
print(f"  3. Mechanism: Rate = CoF + Spread")
print(f"  4. Tier impact: Tier 1 largest cuts")
print(f"  5. Early warning: CI width signal")
print(f"  6. Recovery: partial, new equilibrium")
print(f"  CTA: Integrate CI monitoring")
print(f"\nAll W07-M08 Python outputs saved")
