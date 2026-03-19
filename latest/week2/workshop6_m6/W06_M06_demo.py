"""W06-M06: Animation Fundamentals — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.animation import FuncAnimation
os.makedirs("output", exist_ok=True); np.random.seed(42)

# ── 1. SIMULATED GAPMINDER-STYLE DATA ───────────────────
n_countries = 40
continents = np.random.choice(["Europe","Asia","Africa","Americas"],
    n_countries, p=[0.25,0.30,0.25,0.20])
colors_map = {"Europe":"#1565C0","Asia":"#E53935","Africa":"#2E7D32","Americas":"#E65100"}

base_gdp = np.exp(np.random.uniform(6, 10, n_countries))
records = []
for yr in range(2000, 2021):
    base_gdp *= (1 + 0.02 + np.random.normal(0, 0.05, n_countries))
    life_exp = np.clip(45 + 8 * np.log(base_gdp / 1000) +
        np.random.normal(0, 0.3, n_countries), 30, 85)
    pop = np.abs(np.random.normal(5e6, 3e6, n_countries)) * (1 + (yr-2000)*0.01)
    for i in range(n_countries):
        records.append({"country": f"C{i}", "year": yr,
            "gdp": base_gdp[i], "life_exp": life_exp[i],
            "pop": pop[i], "continent": continents[i]})
df = pd.DataFrame(records)

# ── 2. STATIC FRAME — 2020 ──────────────────────────────
fr = df.query("year == 2020")
fig, ax = plt.subplots(figsize=(9, 6))
for cont, color in colors_map.items():
    sub = fr.query("continent == @cont")
    ax.scatter(sub["gdp"], sub["life_exp"], s=sub["pop"]/5e4,
        c=color, alpha=0.6, edgecolors="white", lw=0.5, label=cont)
ax.set_xscale("log")
ax.legend(fontsize=8)
ax.set_title("Gapminder-Style: 2020 (static base for animation)",
    fontweight="bold")
ax.set_xlabel("GDP per Capita (log)"); ax.set_ylabel("Life Expectancy")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/gapminder_static_2020.png", dpi=300); plt.close()

# ── 3. KEY FRAMES — 4-panel static alternative ──────────
fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharex=True, sharey=True)
for ax, yr in zip(axes, [2000, 2007, 2014, 2020]):
    fr = df.query("year == @yr")
    for cont, color in colors_map.items():
        sub = fr.query("continent == @cont")
        ax.scatter(sub["gdp"], sub["life_exp"], s=sub["pop"]/8e4,
            c=color, alpha=0.5, edgecolors="white", lw=0.3)
    ax.set_xscale("log"); ax.set_title(str(yr), fontsize=11, fontweight="bold")
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
axes[0].set_ylabel("Life Expectancy", fontsize=9)
fig.suptitle("Small Multiples: Static Alternative to Animation\n"
    "All 4 time points visible simultaneously", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/gapminder_keyframes.png", dpi=300); plt.close()

# ── 4. CUMULATIVE LINE ANIMATION (FuncAnimation) ────────
months = pd.date_range("2015-01", "2021-12", freq="ME")
titles = np.cumsum(np.random.poisson(120, len(months)))

fig, ax = plt.subplots(figsize=(9, 4))
line, = ax.plot([], [], color="#1565C0", lw=1.5)
dot, = ax.plot([], [], "o", color="#E53935", markersize=6)
fill = None
ax.set_xlim(months[0], months[-1])
ax.set_ylim(0, titles[-1] * 1.1)
ax.set_title("Cumulative Line: transition_reveal() equivalent", fontweight="bold")
ax.set_ylabel("Cumulative Titles")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
from matplotlib.dates import DateFormatter
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
title_text = ax.text(0.02, 0.95, "", transform=ax.transAxes,
    fontsize=10, fontweight="bold", va="top")

def init():
    line.set_data([], []); dot.set_data([], [])
    title_text.set_text(""); return line, dot, title_text

def update(frame):
    global fill
    if fill is not None:
        fill.remove()
    x = months[:frame+1]; y = titles[:frame+1]
    line.set_data(x, y)
    dot.set_data([x[-1]], [y[-1]])
    fill = ax.fill_between(x, y, alpha=0.06, color="#1565C0")
    title_text.set_text(f"{x[-1].strftime('%b %Y')} — {y[-1]:,} titles")
    return line, dot, title_text

anim = FuncAnimation(fig, update, frames=len(months),
    init_func=init, interval=80, blit=False)
try:
    anim.save("output/line_reveal.gif", writer="pillow", fps=12)
    print("Line reveal animation saved")
except Exception as e:
    print(f"Could not save line GIF: {e}")
plt.close()

# Static version showing 4 progress stages
fig, ax = plt.subplots(figsize=(9, 4))
for i, frac in enumerate([0.25, 0.50, 0.75, 1.0]):
    n = int(len(months) * frac)
    alpha = 0.2 if frac < 1.0 else 1.0
    lw = 0.8 if frac < 1.0 else 2.0
    label = f"{months[n-1].strftime('%b %Y')}" if frac == 1.0 else None
    ax.plot(months[:n], titles[:n], color="#1565C0", lw=lw, alpha=alpha, label=label)
    ax.scatter([months[n-1]], [titles[n-1]], s=30, c="#E53935", zorder=5)
ax.set_title("Line Reveal: 4 Progress Stages (static representation)",
    fontweight="bold")
ax.set_ylabel("Cumulative Titles"); ax.legend(fontsize=8)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.set_major_formatter(DateFormatter("%Y"))
plt.tight_layout(); plt.savefig("output/line_reveal_stages.png", dpi=300); plt.close()

# ── 5. GAPMINDER ANIMATION (FuncAnimation) ──────────────
years = list(range(2000, 2021))
fig, ax = plt.subplots(figsize=(9, 6))

def update_gap(frame_idx):
    ax.clear()
    yr = years[frame_idx]
    fr = df.query("year == @yr")
    for cont, color in colors_map.items():
        sub = fr.query("continent == @cont")
        ax.scatter(sub["gdp"], sub["life_exp"], s=sub["pop"]/5e4,
            c=color, alpha=0.6, edgecolors="white", lw=0.5, label=cont)
    ax.set_xscale("log")
    ax.set_xlim(200, 80000); ax.set_ylim(35, 90)
    ax.set_title(f"Year: {yr}", fontsize=14, fontweight="bold")
    ax.set_xlabel("GDP per Capita (log)"); ax.set_ylabel("Life Expectancy")
    ax.legend(fontsize=7, loc="lower right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    # Year watermark
    ax.text(0.95, 0.05, str(yr), transform=ax.transAxes, fontsize=40,
        fontweight="bold", color="#EEEEEE", ha="right", va="bottom")
    return []

anim_gap = FuncAnimation(fig, update_gap, frames=len(years),
    interval=300, blit=False, repeat=True)
try:
    anim_gap.save("output/gapminder.gif", writer="pillow", fps=5)
    print("Gapminder animation saved")
except Exception as e:
    print(f"Could not save Gapminder GIF: {e}")
plt.close()

# ── 6. 6-FRAME SEQUENCE (animation as stills) ───────────
fig, axes = plt.subplots(1, 6, figsize=(18, 3.5), sharex=True, sharey=True)
for ax, yr in zip(axes, [2000, 2004, 2008, 2012, 2016, 2020]):
    fr = df.query("year == @yr")
    for cont, color in colors_map.items():
        sub = fr.query("continent == @cont")
        ax.scatter(sub["gdp"], sub["life_exp"], s=sub["pop"]/1e5,
            c=color, alpha=0.5, edgecolors="white", lw=0.3)
    ax.set_xscale("log"); ax.set_title(str(yr), fontsize=10, fontweight="bold")
    ax.tick_params(labelsize=5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Animation as 6 Stills: frames FuncAnimation interpolates between",
    fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/frame_sequence.png", dpi=300); plt.close()

# ── 7. FuncAnimation CHEATSHEET ──────────────────────────
print("\n=== FuncAnimation Cheatsheet ===")
print("fig, ax = plt.subplots()")
print("def init(): ...          # initialise empty artists")
print("def update(frame): ...   # redraw for each frame")
print("anim = FuncAnimation(fig, update,")
print("    frames=N,            # total frames")
print("    init_func=init,")
print("    interval=50,         # ms between frames")
print("    blit=True)           # fast rendering")
print("")
print("Saving:")
print("  anim.save('f.gif', writer='pillow', fps=10)")
print("  anim.save('f.mp4', writer='ffmpeg', fps=15)")
print("")
print("=== gganimate Equivalents ===")
print("transition_time(year)   → FuncAnimation with year loop")
print("transition_reveal(date) → cumulative line update")
print("shadow_wake()           → draw fading trail manually")
print("ease_aes('cubic')       → scipy.interpolate for smooth")

print("\nAll W06-M06 Python outputs saved")
