"""W08-M04: Shiny Fundamentals — Python companion
Shows the Dash equivalents for each Shiny pattern (preview for M05).
"""
import os; os.makedirs("output", exist_ok=True)

# ══════════════════════════════════════════════════════════
# SHINY ↔ DASH EQUIVALENCE TABLE
# (Full Dash tutorial in M05; this module is R-focused)
# ══════════════════════════════════════════════════════════

print("=== Shiny (R) ↔ Dash (Python) Equivalence ===\n")
equivalences = [
    ("ARCHITECTURE", "", ""),
    ("  fluidPage()", "app.layout = html.Div([...])", "Page container"),
    ("  sidebarLayout()", "dbc.Row([dbc.Col(...)])", "Layout grid"),
    ("  server <- function(input,output)", "@app.callback(...)", "Server logic"),
    ("", "", ""),
    ("INPUTS", "", ""),
    ("  selectInput('id', ...)", "dcc.Dropdown(id='id', ...)", "Dropdown"),
    ("  sliderInput('id', ...)", "dcc.RangeSlider(id='id', ...)", "Slider"),
    ("  checkboxGroupInput()", "dcc.Checklist(id='id', ...)", "Checkboxes"),
    ("  radioButtons()", "dcc.RadioItems(id='id', ...)", "Radio"),
    ("  actionButton()", "html.Button('Reset', id='id')", "Button"),
    ("", "", ""),
    ("OUTPUTS", "", ""),
    ("  plotOutput() + renderPlot()", "dcc.Graph(id='chart')", "Chart"),
    ("  DTOutput() + renderDT()", "dash_table.DataTable()", "Table"),
    ("  textOutput() + renderText()", "html.P(id='text')", "Text"),
    ("", "", ""),
    ("REACTIVITY", "", ""),
    ("  reactive({...})", "@app.callback(Output, Input)", "Auto-update"),
    ("  observeEvent(input$btn)", "@app.callback(..., Input('btn','n_clicks'))", "Event"),
    ("  eventReactive(input$go)", "Same callback, check n_clicks", "Lazy compute"),
]
for shiny, dash, note in equivalences:
    if not shiny: print(); continue
    print(f"  {shiny:<35} {dash:<40} {note}")

# ══════════════════════════════════════════════════════════
# MINIMAL DASH APP (preview for M05)
# ══════════════════════════════════════════════════════════
dash_template = '''
# ── MINIMAL DASH APP (W08-M05 preview) ──
# pip install dash pandas plotly

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Netflix Content Explorer"),

    # Inputs
    html.Div([
        html.Label("Content Type:"),
        dcc.Dropdown(
            id="type-dropdown",
            options=[{"label": t, "value": t}
                     for t in ["All", "Movie", "TV Show"]],
            value="All"),

        html.Label("Year Range:"),
        dcc.RangeSlider(
            id="year-slider",
            min=2015, max=2021, step=1,
            value=[2015, 2021],
            marks={y: str(y) for y in range(2015, 2022)}),
    ], style={"width": "25%", "display": "inline-block",
              "verticalAlign": "top", "padding": "20px"}),

    # Output
    html.Div([
        dcc.Graph(id="trend-chart"),
        html.P(id="summary-text"),
    ], style={"width": "70%", "display": "inline-block"}),
])

@app.callback(
    [Output("trend-chart", "figure"),
     Output("summary-text", "children")],
    [Input("type-dropdown", "value"),
     Input("year-slider", "value")])
def update_chart(content_type, year_range):
    df = nf.query(f"{year_range[0]} <= year_added <= {year_range[1]}")
    if content_type != "All":
        df = df.query(f"type == '{content_type}'")

    yearly = df.groupby(["year_added", "type"]).size().reset_index(name="n")
    fig = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True, title="Netflix Additions by Type")
    fig.update_layout(template="plotly_white", hovermode="x unified")

    summary = f"Showing {len(df):,} titles ({year_range[0]}–{year_range[1]})"
    return fig, summary

if __name__ == "__main__":
    app.run(debug=True)
'''

with open("output/dash_preview_app.py", "w") as f:
    f.write(dash_template)
print("\nDash preview app saved: output/dash_preview_app.py")
print("(Full Dash tutorial in W08-M05)")

# ══════════════════════════════════════════════════════════
# REACTIVITY COMPARISON
# ══════════════════════════════════════════════════════════
print("\n=== Reactivity: Shiny vs Dash ===")
print("  Shiny: reactive() = lazy, cached, auto-invalidates")
print("  Dash:  @callback  = triggers on any Input change")
print("")
print("  Shiny: observe()  = eager, side effects")
print("  Dash:  No direct equivalent (callbacks always return)")
print("")
print("  Shiny: eventReactive(input$btn) = trigger on click only")
print("  Dash:  Check n_clicks in callback; prevent_initial_call=True")
print("")
print("  Key difference: Shiny uses a REACTIVE GRAPH (implicit);")
print("  Dash uses EXPLICIT callbacks (you declare Input → Output).")
print("  Both achieve the same result; Shiny is more 'magical',")
print("  Dash is more explicit and debuggable.")

print("\nAll W08-M04 Python outputs saved")
