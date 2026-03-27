"""W08-M08: e-Car Interactive Dashboard — Complete Dash App — UNYT"""
import os; os.makedirs("output", exist_ok=True)

dash_app = '''
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd, plotly.express as px, plotly.graph_objects as go

ec = pd.read_csv("ecar.csv")
ec.columns = [c.strip().replace("  "," ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Quarter"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.quarter
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec["Approved"] = ec["Outcome"] == 1
ec = ec.query("2002 <= Year <= 2012")

TIER_PALETTE = {1:"#BBDEFB",2:"#64B5F6",3:"#1E88E5",4:"#1565C0",5:"#0D47A1"}
tiers = sorted(ec.Tier.unique())

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

def make_kpi(title, value, color):
    fmt = f"{value:,.0f}" if value > 100 else f"{value:.1f}%"
    return dbc.Card(dbc.CardBody([
        html.H6(title, className="text-muted mb-1", style={"fontSize":"0.75rem"}),
        html.H3(fmt, className="fw-bold mb-0", style={"color":color}),
    ]), className="text-center shadow-sm")

def crisis_shapes():
    return [dict(type="rect",x0=2007.5,x1=2009.5,y0=0,y1=1,yref="paper",
        fillcolor="#E53935",opacity=0.04,line=dict(width=0))]

app.layout = dbc.Container([
    html.H3("e-Car Loan Analytics Dashboard", className="text-primary fw-bold mt-2 mb-2"),
    dbc.Row([
        dbc.Col([html.Label("Tiers:"),
            dcc.Checklist(id="tier-check",
                options=[{"label":f" T{t}","value":t} for t in tiers],
                value=tiers, inline=True)], width=4),
        dbc.Col([html.Label("Years:"),
            dcc.RangeSlider(id="year-sl",min=2002,max=2012,step=1,value=[2002,2012],
                marks={y:str(y) for y in range(2002,2013,2)})], width=3),
        dbc.Col([html.Label("Metric:"),
            dcc.RadioItems(id="metric",
                options=[{"label":m,"value":m} for m in ["Rate","Spread","Cost of Funds"]],
                value="Rate", inline=True)], width=3),
        dbc.Col(html.Button("Reset",id="reset",n_clicks=0,
            className="btn btn-outline-secondary btn-sm mt-3"), width=2),
    ], className="mb-2 p-2", style={"background":"#f9f9f9","borderRadius":"8px"}),

    dbc.Row(id="kpi-row", className="mb-2"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="trend",style={"height":"300px"}),width=6),
        dbc.Col(dcc.Graph(id="dist",style={"height":"300px"}),width=6)]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="ci",style={"height":"260px"}),width=4),
        dbc.Col(dcc.Graph(id="approval",style={"height":"260px"}),width=4),
        dbc.Col(dash_table.DataTable(id="table",
            columns=[{"name":c,"id":c} for c in ["Year","Tier","Rate","Cost of Funds","Spread","Outcome"]],
            page_size=8,sort_action="native",filter_action="native",
            style_table={"overflowX":"auto","maxHeight":"260px"},
            style_cell={"fontSize":"11px","padding":"4px"}),width=4)]),
], fluid=True)

@app.callback(
    Output("trend","figure"),Output("dist","figure"),
    Output("ci","figure"),Output("approval","figure"),
    Output("table","data"),Output("kpi-row","children"),
    Input("tier-check","value"),Input("year-sl","value"),Input("metric","value"))
def update(tiers_sel, years, metric):
    df = ec.query("Tier in @tiers_sel and @years[0] <= Year <= @years[1]")

    # Trend
    agg = df.groupby(["Year","Tier"])[metric].mean().reset_index()
    fig_trend = px.line(agg, x="Year",y=metric,color="Tier",
        color_discrete_map={t:TIER_PALETTE[t] for t in tiers},markers=True,
        title=f"{metric} Trend by Tier")
    fig_trend.update_layout(template="plotly_white",hovermode="x unified",
        shapes=crisis_shapes(),margin=dict(t=40,b=20),
        legend=dict(orientation="h",y=-0.15))

    # Distribution
    fig_dist = px.histogram(df,x=metric,color="Tier",
        color_discrete_map={t:TIER_PALETTE[t] for t in tiers},
        nbins=40,opacity=0.5,barmode="overlay",title=f"{metric} Distribution")
    fig_dist.update_layout(template="plotly_white",margin=dict(t=40,b=20))

    # CI ribbon
    qr = df.groupby(["Year","Quarter"]).agg(
        rate=("Rate","mean"),se=("Rate","sem")).reset_index()
    qr["date"] = pd.to_datetime(qr.apply(lambda r:f"{int(r.Year)}-{int(r.Quarter)*3-2:02d}-01",axis=1))
    fig_ci = go.Figure()
    fig_ci.add_trace(go.Scatter(x=qr.date,y=qr.rate+1.96*qr.se,mode="lines",
        line=dict(width=0),showlegend=False))
    fig_ci.add_trace(go.Scatter(x=qr.date,y=qr.rate-1.96*qr.se,mode="lines",
        line=dict(width=0),fill="tonexty",fillcolor="rgba(21,101,192,0.15)",
        name="95% CI"))
    fig_ci.add_trace(go.Scatter(x=qr.date,y=qr.rate,mode="lines",
        line=dict(color="#1565C0",width=1.5),name="Mean Rate"))
    fig_ci.update_layout(title=dict(text="Quarterly Rate ± 95% CI",font=dict(size=12)),
        template="plotly_white",hovermode="x unified",margin=dict(t=40,b=20),
        shapes=[dict(type="line",x0="2008-09-15",x1="2008-09-15",y0=0,y1=1,
            yref="paper",line=dict(color="#E53935",dash="dash",width=1))])

    # Approval
    apr = df.groupby(["Year","Tier"])["Approved"].mean().reset_index()
    apr["Approved"] = apr["Approved"]*100
    fig_apr = px.line(apr,x="Year",y="Approved",color="Tier",
        color_discrete_map={t:TIER_PALETTE[t] for t in tiers},markers=True,
        title="Approval Rate by Tier")
    fig_apr.update_layout(template="plotly_white",hovermode="x unified",
        shapes=crisis_shapes(),margin=dict(t=40,b=20))

    # Table
    table_data = df[["Year","Tier","Rate","Cost of Funds","Spread","Outcome"]].head(300).to_dict("records")

    # KPIs
    kpis = dbc.Row([
        dbc.Col(make_kpi("Filtered Loans",len(df),"#333"),width=3),
        dbc.Col(make_kpi("Avg Rate",df.Rate.mean(),"#1565C0"),width=3),
        dbc.Col(make_kpi("Avg Spread",df.Spread.mean(),"#E53935"),width=3),
        dbc.Col(make_kpi("Approval",df.Approved.mean()*100,"#2E7D32"),width=3)])
    return fig_trend, fig_dist, fig_ci, fig_apr, table_data, kpis

@app.callback(Output("tier-check","value"),Output("year-sl","value"),Output("metric","value"),
    Input("reset","n_clicks"),prevent_initial_call=True)
def reset(n): return tiers, [2002,2012], "Rate"

if __name__=="__main__": app.run(debug=True,port=8051)
'''
with open("output/ecar_dashboard.py","w") as f: f.write(dash_app)
print("e-Car Dash app saved: output/ecar_dashboard.py")

print("\n=== e-Car Dashboard: Unique Financial Features ===")
features = [
    ("Sequential palette", "Tiers 1→5 map to light→dark blue (ordered, not categorical)"),
    ("Metric switcher", "RadioItems: Rate / Spread / CoF — same chart, different y"),
    ("CI ribbon", "Quarterly mean ± 1.96·SE — volatility = risk signal"),
    ("Crisis annotation", "2008 shaded region on ALL temporal panels"),
    ("Approval trend", "Credit-standard tightening visible by tier"),
]
for name, desc in features:
    print(f"  {name}: {desc}")

print("\nAll W08-M08 Python outputs saved")
