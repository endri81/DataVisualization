# Workshop 8 · Module 5 — Course Notes
## Dash Fundamentals

### 1. Dash = Python's Shiny
Dash is Plotly's open-source framework for building reactive web applications in Python. It maps directly to Shiny's architecture: **layout** (what the user sees) replaces Shiny's **UI**, and **callbacks** (how Python responds to user actions) replace Shiny's **server + reactivity**. If you understand Shiny, Dash takes an afternoon to learn; the concepts are identical, only the syntax differs.

### 2. The Two-Part Architecture
**Layout**: built from three component libraries. `html.*` provides HTML tags (`html.Div`, `html.H1`, `html.P`). `dcc.*` (Dash Core Components) provides interactive widgets (`dcc.Dropdown`, `dcc.RangeSlider`, `dcc.Graph`, `dcc.Tabs`). `dash_bootstrap_components` (dbc) provides Bootstrap's responsive grid (`dbc.Container`, `dbc.Row`, `dbc.Col`, `dbc.Card`) — always use dbc for layout rather than nesting `html.Div` with inline CSS.

**Callbacks**: Python functions decorated with `@app.callback(Output, Input)`. When any `Input` component changes value, the decorated function re-executes and returns new values for the `Output` components. This is explicit (you declare every Input and Output) compared to Shiny's implicit reactive graph.

### 3. Callback Patterns
**Basic**: `@app.callback(Output("chart", "figure"), Input("dd", "value"))` → `def update(val): return fig`. One input triggers one output.

**Multi-output**: `@app.callback([Output("a", "figure"), Output("b", "children")], Input(...))` → `def update(val): return fig, text`. One callback updates multiple components simultaneously.

**Multi-input**: `@app.callback(Output(...), Input("dd", "value"), Input("slider", "value"))` → `def update(dd_val, slider_val): ...`. The callback fires when ANY input changes.

**State**: `@app.callback(Output(...), Input("btn", "n_clicks"), State("text", "value"))`. `State` reads a component's current value WITHOUT triggering the callback. This is equivalent to Shiny's `eventReactive(input$btn, { input$text })` — the callback fires only when the button is clicked, but reads the text field's value at that moment.

**prevent_initial_call**: `@app.callback(..., prevent_initial_call=True)`. Prevents the callback from firing when the page first loads. Equivalent to Shiny's `eventReactive(..., ignoreNULL=TRUE)`.

**Chained callbacks**: the Output of one callback can be the Input of another, creating a processing pipeline. Dash resolves these automatically in dependency order.

### 4. Component Libraries

| Library | Import | Key Components |
|---------|--------|----------------|
| `dash.html` | `from dash import html` | Div, H1, H2, P, Span, Br, Hr, Button, Img |
| `dash.dcc` | `from dash import dcc` | Dropdown, Slider, RangeSlider, RadioItems, Checklist, Graph, Tabs, Store, Interval |
| `dash_bootstrap` | `import dash_bootstrap_components as dbc` | Container, Row, Col, Card, CardBody, Navbar |
| `dash_table` | `import dash_table` | DataTable (sortable, filterable, editable) |

### 5. Shiny ↔ Dash Complete Mapping

| Concept | Shiny (R) | Dash (Python) |
|---------|-----------|---------------|
| Page container | `fluidPage()` | `html.Div()` or `dbc.Container()` |
| Grid layout | `sidebarLayout()` | `dbc.Row([dbc.Col(...)])` |
| Dropdown | `selectInput("id", choices=...)` | `dcc.Dropdown(id="id", options=[...])` |
| Slider | `sliderInput("id", min, max, value)` | `dcc.RangeSlider(id="id", min=, max=, value=)` |
| Checkboxes | `checkboxGroupInput("id", choices)` | `dcc.Checklist(id="id", options=[...])` |
| Radio | `radioButtons("id", choices)` | `dcc.RadioItems(id="id", options=[...])` |
| Button | `actionButton("id", "Label")` | `html.Button("Label", id="id")` |
| Chart placeholder | `plotOutput("id")` / `plotlyOutput("id")` | `dcc.Graph(id="id")` |
| Chart render | `renderPlot({...})` / `renderPlotly({...})` | Return figure from callback |
| Data table | `DTOutput("id")` + `renderDT({...})` | `dash_table.DataTable(id="id", data=...)` |
| Reactive data | `reactive({filter(df, ...)})` | Filter inside callback function |
| Event trigger | `observeEvent(input$btn, {...})` | `@callback(..., Input("btn","n_clicks"), prevent_initial_call=True)` |
| Read without trigger | `eventReactive(input$btn, {input$text})` | `State("text", "value")` in callback |

### 6. Deployment
**Local**: `python app.py` → `http://localhost:8050`. For development.

**Render.com**: connect GitHub repo, add `requirements.txt` + `Procfile` (`web: gunicorn app:server`). Free tier available. Auto-deploys on push.

**Heroku**: similar to Render. Requires `Procfile`, `requirements.txt`, `runtime.txt`.

**JupyterDash**: `from jupyter_dash import JupyterDash; app = JupyterDash(__name__)`. Runs Dash inside Jupyter notebooks — useful for prototyping without leaving the notebook environment.

### 7. When to Use Dash vs Shiny vs plotly Alone
**plotly alone** (M02–M03): when you just need an interactive chart with hover, zoom, and a dropdown filter. No server needed. Self-contained HTML.

**Shiny**: when your team uses R, you have existing ggplot2 code, and you want shinyapps.io deployment. Implicit reactivity feels more "magical."

**Dash**: when your team uses Python, you have existing pandas/plotly code, and you want cloud deployment (Render, Heroku, AWS). Explicit callbacks feel more debuggable.

### References
- Dash documentation: https://dash.plotly.com/
- Dash Bootstrap Components: https://dash-bootstrap-components.opensource.faculty.ai/
- Render deployment guide: https://render.com/docs/deploy-a-dash-app
- Huss, E. (2022). *Plotly Dash Cookbook*. Packt.
