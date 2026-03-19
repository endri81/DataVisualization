"""W04-M09: EDA Automation & Reproducible Reports — Python — UNYT"""
import pandas as pd, os
os.makedirs("output",exist_ok=True)

apps = pd.read_csv("googleplaystore.csv")
apps["Reviews"] = pd.to_numeric(apps["Reviews"], errors="coerce")
apps = apps.dropna(subset=["Rating"])

# 1. YDATA-PROFILING
try:
    from ydata_profiling import ProfileReport
    report = ProfileReport(apps, title="Google Play Store EDA", explorative=True, minimal=True)
    report.to_file("output/auto_eda.html")
    print("  ydata-profiling report saved")
except ImportError:
    print("  ydata-profiling not installed (pip install ydata-profiling)")

# 2. SWEETVIZ (comparison)
try:
    import sweetviz as sv
    free = apps.query("Type=='Free'")
    paid = apps.query("Type=='Paid'")
    report = sv.compare([free,"Free"],[paid,"Paid"])
    report.show_html("output/free_vs_paid.html", open_browser=False)
    print("  sweetviz comparison saved")
except ImportError:
    print("  sweetviz not installed (pip install sweetviz)")

# 3. BUILT-IN PANDAS PROFILING
print("\n── Built-in pandas summary ──")
print(apps.describe().round(2))
print("\n── Missing % ──")
print((apps.isna().mean()*100).round(1).sort_values(ascending=False))
print("\n── dtypes ──")
print(apps.dtypes)

print("\nAll W04-M09 Python outputs saved")
