"""W03-M09: Tables as Visualization — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)

# Simulated summary data
cats=["FAMILY","GAME","TOOLS","BUSINESS","MEDICAL","SOCIAL"]
counts=[1832,959,843,420,395,259]; ratings=[4.18,4.05,4.12,4.22,3.95,4.30]
paid_pcts=[0.073,0.068,0.071,0.082,0.065,0.058]
trends=[[3.8,3.9,4.0,4.1,4.15,4.18],[4.2,4.15,4.1,4.05,4.05,4.05],
        [3.9,3.95,4.0,4.05,4.1,4.12],[4.0,4.05,4.1,4.15,4.2,4.22],
        [4.1,4.0,3.95,3.9,3.92,3.95],[4.1,4.15,4.2,4.25,4.28,4.30]]

df=pd.DataFrame({"Category":cats,"Count":counts,"Mean_Rating":ratings,"Paid_Pct":paid_pcts})

# 1. PANDAS STYLER — conditional formatting
styled=(df.style
    .background_gradient(subset=["Mean_Rating"],cmap="RdYlGn",vmin=3.8,vmax=4.4)
    .bar(subset=["Count"],color="#BBDEFB",vmin=0)
    .format({"Count":"{:,.0f}","Mean_Rating":"{:.2f}","Paid_Pct":"{:.1%}"})
    .highlight_max(subset=["Mean_Rating"],color="#C8E6C9")
    .set_caption("Google Play Store: Category Summary")
    .set_table_styles([{"selector":"caption","props":[("font-weight","bold"),("font-size","14px")]}]))
styled.to_html("output/styled_table.html")
print("  styled_table.html saved")

# 2. GREAT_TABLES (if installed)
try:
    from great_tables import GT
    gt_tbl=(GT(df)
        .tab_header(title="Category Summary",subtitle="Google Play Store")
        .data_color(columns="Mean_Rating",palette="RdYlGn")
        .fmt_number(columns="Count",decimals=0,use_seps=True)
        .fmt_percent(columns="Paid_Pct",decimals=1)
        .tab_source_note("Source: Kaggle"))
    gt_tbl.save("output/great_table.html")
    print("  great_table.html saved")
except ImportError:
    print("  great_tables not installed — pip install great_tables")

# 3. SPARKLINES — matplotlib table with inline plots
fig,ax=plt.subplots(figsize=(9,4.5)); ax.axis("off")
for j,col in enumerate(["Category","Trend (2019–2024)","Current","Change"]):
    ax.text(0.02+j*0.25,0.92,col,fontsize=9,fontweight="bold",color="#1565C0")
ax.axhline(y=0.86,xmin=0.01,xmax=0.99,color="#333",linewidth=1.5)
for i,(cat,tr) in enumerate(zip(cats,trends)):
    y=0.76-i*0.12
    ax.text(0.02,y,cat,fontsize=8,fontweight="bold",color="#333",va="center")
    xs=np.linspace(0.28,0.48,len(tr)); ys=[y-0.03+0.06*(v-3.8)/0.5 for v in tr]
    color="#2E7D32" if tr[-1]>tr[0] else "#E53935"
    ax.plot(xs,ys,color=color,linewidth=1.5); ax.scatter([xs[-1]],[ys[-1]],s=15,c=color,zorder=5)
    ax.text(0.55,y,f"{tr[-1]:.2f}",fontsize=8,va="center",fontweight="bold")
    change=tr[-1]-tr[0]; sign="+" if change>0 else ""
    ax.text(0.75,y,f"{sign}{change:.2f}",fontsize=8,va="center",fontweight="bold",color=color)
ax.set_xlim(0,1); ax.set_ylim(0.05,1)
ax.set_title("Sparklines in Tables: Tufte's Inline Graphics",fontweight="bold",pad=12)
plt.tight_layout(); plt.savefig("output/sparklines_py.png",dpi=300); plt.close()

print("All W03-M09 Python plots saved")
