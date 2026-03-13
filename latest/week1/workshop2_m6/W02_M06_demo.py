"""W02-M06: Themes & Publication-Quality Styling — Python — UNYT Tirana"""
import numpy as np, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. GLOBAL THEME via rcParams
plt.rcParams.update({
    "figure.figsize": (7, 5), "figure.dpi": 150, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.12, "axes.facecolor": "white",
    "axes.titleweight": "bold", "axes.labelweight": "bold",
})

# 2. BEFORE vs AFTER
np.random.seed(22); x=np.random.uniform(1,6,60); y=0.5*x+np.random.normal(0,0.8,60)

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))
# Before: raw matplotlib defaults (temporarily reset)
ax1.scatter(x,y,s=20,c="steelblue")
ax1.set_title("BEFORE: Defaults",color="#C62828")
ax1.set_facecolor("#EBEBEB"); ax1.grid(True,color="white")
for sp in ax1.spines.values(): sp.set_visible(True)
# After: rcParams applied
ax2.scatter(x,y,s=25,c="#1565C0",alpha=0.6,edgecolors="white",linewidth=0.3)
ax2.set_title("AFTER: rcParams + manual")
fig.suptitle("Theme Transformation",fontsize=12,fontweight="bold")
plt.tight_layout(); plt.savefig("output/before_after_py.png",dpi=300); plt.close()

# 3. REUSABLE THEME FUNCTION
def apply_unyt_theme(ax, title="", subtitle="", caption=""):
    """Apply UNYT branded styling to any axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("white")
    ax.grid(axis="y", alpha=0.12)
    ax.tick_params(labelsize=9)
    if title: ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    if caption:
        ax.figure.text(0.12, 0.01, caption, fontsize=7, color="#AAA", fontstyle="italic")

np.random.seed(22); n=80; x2=np.random.uniform(1,6,n); y2=0.5*x2+np.random.normal(0,0.8,n)
cls=np.random.choice(["A","B","C"],n)
pal={"A":"#1565C0","B":"#E53935","C":"#2E7D32"}

fig,ax=plt.subplots(figsize=(7,5))
for c,col in pal.items():
    mask=cls==c; ax.scatter(x2[mask],y2[mask],s=30,c=col,alpha=0.6,edgecolors="white",linewidth=0.4,label=c)
ax.legend(fontsize=8,title="Class",title_fontsize=9,frameon=False)
ax.set_xlabel("Displacement (L)"); ax.set_ylabel("Highway MPG")
apply_unyt_theme(ax, title="Engine Size vs Fuel Economy",
                 caption="Source: mpg dataset | UNYT Data Visualization Course")
plt.tight_layout()
plt.savefig("output/branded_py.pdf", bbox_inches="tight")
plt.savefig("output/branded_py.png", dpi=300, bbox_inches="tight")
plt.close()

# 4. plt.style.use() demo
styles = ["seaborn-v0_8-whitegrid", "ggplot", "bmh", "fivethirtyeight"]
fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
for ax, s in zip(axes, styles):
    with plt.style.context(s):
        ax.scatter(x, y, s=15, alpha=0.6)
        ax.set_title(s, fontsize=7, fontweight="bold")
        ax.tick_params(labelsize=5)
fig.suptitle("plt.style.use(): Built-In Style Sheets", fontsize=11, fontweight="bold")
plt.tight_layout(); plt.savefig("output/styles_py.png", dpi=300); plt.close()

# 5. EXPORT comparison
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(x2, y2, s=20, c="#1565C0", alpha=0.6)
apply_unyt_theme(ax, title="Export Test")
plt.tight_layout()
fig.savefig("output/export_test.pdf", bbox_inches="tight")
fig.savefig("output/export_test.png", dpi=300, bbox_inches="tight")
fig.savefig("output/export_test.svg", bbox_inches="tight")
plt.close()

print("All W02-M06 Python plots saved")
for f in ["export_test.pdf", "export_test.png", "export_test.svg"]:
    sz = os.path.getsize(f"output/{f}")
    print(f"  {f}: {sz/1024:.0f} KB")
