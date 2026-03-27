# Workshop 8 · Module 4 — Course Notes
## Shiny Fundamentals

### 1. From plotly to Shiny
plotly (M02–M03) provides client-side interactivity: hover, zoom, pan, and dropdown filters that run entirely in the browser with no server. Shiny extends this to **server-side interactivity**: R code runs on a server, processing user inputs in real time. This enables operations that plotly cannot do: database queries, complex data transformations, statistical computations, file generation, and multi-panel cross-filtering with complex business logic.

The trade-off: plotly charts are self-contained HTML files (no server needed). Shiny apps require a running R process — either locally in RStudio or on a deployment platform (shinyapps.io, Shiny Server, Posit Connect).

### 2. The Three-Part Architecture
Every Shiny app has three components:

**UI (User Interface)**: defines what the user sees — the page layout, input widgets (dropdowns, sliders, buttons), and output placeholders (chart areas, tables, text). The UI is declarative: you describe the structure, and Shiny generates the HTML/CSS/JavaScript.

**Server**: defines what R computes — how inputs are transformed into outputs. The server is a function `function(input, output, session)` where `input$x` reads the current value of widget "x", and `output$y <- renderPlot({...})` sends a rendered ggplot to placeholder "y".

**Reactivity**: the automatic mechanism that connects inputs to outputs. When the user changes a slider, Shiny automatically invalidates any reactive expression that depends on that slider, recalculates the affected outputs, and updates the UI. The programmer does not write event handlers — the reactive graph handles it.

### 3. Input Widgets
Shiny provides ~20 input widgets. The six most commonly used:

**`selectInput("id", "Label:", choices)`**: dropdown menu. The user selects one option. Access the selected value in the server as `input$id`.

**`sliderInput("id", "Label:", min, max, value)`**: numeric slider. For ranges, set `value = c(min, max)`. Access as `input$id` (a length-2 vector for ranges).

**`checkboxGroupInput("id", "Label:", choices)`**: multiple checkboxes. Returns a character vector of selected values.

**`radioButtons("id", "Label:", choices)`**: single selection from radio buttons.

**`textInput("id", "Label:", value)`**: free text entry.

**`actionButton("id", "Label")`**: triggers a specific event. Use with `observeEvent(input$id, {...})` to execute code only when clicked.

### 4. Output Renderers
Each output type has a matched pair: a **UI placeholder** and a **server render function**:

| UI Function | Server Function | Content |
|---|---|---|
| `plotOutput("id")` | `renderPlot({ggplot(...)})` | Static ggplot |
| `plotlyOutput("id")` | `renderPlotly({ggplotly(...)})` | Interactive plotly |
| `DTOutput("id")` | `renderDT({datatable(...)})` | Searchable data table |
| `textOutput("id")` | `renderText({paste(...)})` | Text string |
| `downloadButton("id")` | `downloadHandler(...)` | File download |

### 5. Reactivity: The Core Mental Model
Reactivity is what makes Shiny powerful and what makes it confusing. The core concept: **reactive expressions automatically re-execute when their inputs change**.

**`reactive({...})`**: creates a reactive expression that is lazy (only computes when requested), cached (doesn't recompute if inputs haven't changed), and automatically invalidated when any `input$` inside it changes. Access with parentheses: `filtered()`.

**`observe({...})`**: an eager reactive that runs immediately when any input inside it changes. Used for side effects (logging, updating other inputs). Does not return a value.

**`eventReactive(trigger, {...})`**: like `reactive()` but only re-executes when the specified trigger changes — not when other inputs change. Use for expensive computations with a "Go" button.

**`observeEvent(trigger, {...})`**: like `observe()` but only fires on a specific event. Use for reset buttons, navigation, and explicit user actions.

Rule of thumb: use `reactive()` for 90% of cases. Use `eventReactive()` when computation is expensive and you want a "Run" button.

### 6. Shneiderman's Mantra in Shiny
Each step of the mantra (M01) maps to Shiny components:

| Mantra Step | Shiny Implementation |
|---|---|
| Overview first | Default view with no filters applied |
| Zoom | plotly zoom (client-side) within `plotlyOutput` |
| Filter | `selectInput`, `sliderInput`, `checkboxGroupInput` |
| Details on demand | `DTOutput` (click to see row details), plotly hover |
| Relate | Multiple `plotlyOutput` panels sharing `reactive()` data |
| History | `actionButton("reset")` + `observeEvent` to restore defaults |
| Extract | `downloadButton` + `downloadHandler` for CSV/PNG |

### 7. Deployment Options
**Local**: `shiny::runApp()` in RStudio. For development and personal use.

**shinyapps.io**: Posit's hosted platform. Free tier: 25 active hours/month, 5 apps. Deploy with `rsconnect::deployApp()`. Best for: course submissions, sharing with colleagues.

**Shiny Server (Open Source)**: self-hosted on Linux. Free. Requires server administration. Best for: departmental dashboards.

**Posit Connect**: enterprise platform with authentication, scheduling, and multiple content types. Paid. Best for: production corporate dashboards.

### References
- Wickham, H. (2021). *Mastering Shiny*. O'Reilly. https://mastering-shiny.org
- Shiny gallery: https://shiny.posit.co/r/gallery/
- Shiny cheatsheet: https://posit.co/resources/cheatsheets/
- Chang, W. et al. (2023). shiny: Web Application Framework for R. R package.
