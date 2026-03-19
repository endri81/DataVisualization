# Workshop 6 · Module 6 — Course Notes
## Animation Fundamentals

### 1. Why Animate?
Animation adds a dimension that static charts cannot provide: the perception of **change as movement**. When a data point moves across the screen, the human visual system tracks it as a continuous trajectory, engaging motion-processing pathways that are faster and more intuitive than comparing static snapshots. This makes animation uniquely powerful for showing: (a) how entities evolve over time (Gapminder scatter), (b) the process of data accumulation (line reveal), (c) rank changes (bar chart race), and (d) transitions between states (morphing distributions).

However, animation also has fundamental limitations: the viewer cannot compare two frames precisely (temporal memory is poor), cannot refer back to earlier frames without replaying, and cannot control the pace. This makes animation better for **storytelling/presentation** than for **analysis/reference**. The golden rule: every animation should have a static companion (small multiples, key-frames panel) for the report.

### 2. The Animation Workflow (5 Steps)
**Step 1 — Build the static base**: create a ggplot or matplotlib figure for a single time point. This is your "frame zero." Every element that will be animated must be present in this static version.

**Step 2 — Add the transition layer**: in R, add one `transition_*()` function to the ggplot. In Python, define an `update(frame)` function that modifies the plot for each frame. The transition determines what changes between frames.

**Step 3 — Configure easing and shadow**: easing controls the speed curve (constant, accelerating, decelerating). Shadow controls what trace is left behind (wake trail, persistent marks, nothing). In R: `ease_aes("cubic-in-out")` + `shadow_wake(wake_length=0.1)`. In Python: implement manually by drawing fading previous positions.

**Step 4 — Render**: convert the animation into a file format. GIF (universal, plays anywhere, no audio) or MP4 (smaller file, better quality, requires video player). In R: `animate(p, nframes=100, fps=10, renderer=gifski_renderer("file.gif"))`. In Python: `anim.save("file.gif", writer="pillow", fps=10)` or `writer="ffmpeg"` for MP4.

**Step 5 — Embed**: include the animation in the output. GIF embeds directly in HTML, Quarto, Jupyter, email, and social media. MP4 works in PowerPoint and video platforms. For PDF reports: include a key-frames panel (static) and a link to the GIF/video.

### 3. gganimate (R) — Transition Types
gganimate extends ggplot2 with a declarative animation grammar. You add transition and shadow layers just like adding `geom_*()` layers:

**`transition_time(year)`**: continuous interpolation between numeric time values. Points move smoothly from their positions at year T to year T+1. Best for: Gapminder-style scatter. Title template: `{frame_time}` inserts the current year.

**`transition_states(state, transition_length, state_length)`**: discrete jumps between categorical states with smooth interpolation. The `transition_length` parameter controls how many frames are spent interpolating between states; `state_length` controls how many frames pause at each state. Best for: bar chart race, before/after comparisons.

**`transition_reveal(date)`**: cumulative reveal — each frame adds new data without removing previous data. The line "grows" from left to right. Best for: line charts, time series accumulation. A red dot at the growing tip helps track the current position.

**`transition_filter(condition)`**: show/hide points based on a logical condition that changes over time. Best for: highlighting subsets sequentially.

**`transition_layers()`**: add ggplot layers one by one across frames. Best for: build-up reveal in presentations (first show axes, then trend line, then data points, then annotations).

### 4. FuncAnimation (Python)
matplotlib's `FuncAnimation` is more manual but more flexible. Structure:

```python
fig, ax = plt.subplots()
# Initialize artists (lines, scatter, text)
line, = ax.plot([], [], color="#1565C0")

def init():
    line.set_data([], [])
    return line,

def update(frame):
    # Update data for this frame
    line.set_data(x[:frame], y[:frame])
    return line,

anim = FuncAnimation(fig, update, frames=N,
    init_func=init, blit=True, interval=50)
anim.save("output.gif", writer="pillow", fps=10)
```

Key parameters: `frames` (total number of frames — more = smoother, larger file), `interval` (milliseconds between frames — 50ms = 20fps, 100ms = 10fps), `blit` (True for faster rendering — the update function must return only modified artists).

For the Gapminder scatter: `update()` clears the axes with `ax.clear()` and redraws all scatter points for the current year. This is slower than blitting but simpler when the entire plot changes each frame.

### 5. Easing Functions
Easing controls the acceleration profile between frames. Without easing, all transitions are linear (constant speed), which feels mechanical.

**linear**: constant speed throughout. Use when the data genuinely changes at a constant rate.

**cubic-in-out**: starts slow, accelerates to midpoint, decelerates to end. The most natural-feeling easing for most transitions. In gganimate: `ease_aes("cubic-in-out")`.

**bounce-out**: the element "bounces" at its destination. Playful, best for informal/social media content.

In Python, implement easing manually by interpolating positions with a nonlinear function (e.g., scipy's cubic interpolation) rather than linear interpolation.

### 6. Shadow and Trail
Shadows show where data points came from, adding trajectory information:

**`shadow_wake(wake_length=0.1, alpha=0.2)`**: a fading trail behind each point, like a comet. The wake_length parameter controls how many previous frames are visible. Best for: showing trajectory direction and speed.

**`shadow_mark(past=TRUE, future=FALSE)`**: all previous positions are retained as faint dots, building up a complete trajectory map. Best for: showing the full path of each entity.

In Python: implement by storing previous positions and drawing them with decreasing alpha in the update function.

### 7. Rendering and File Formats
**GIF**: universal compatibility (browsers, email, social media, Jupyter), loops automatically, no audio. File size can be large (10–50 MB for complex animations). Use `gifski` renderer in R (optimised compression) or `pillow` writer in Python.

**MP4**: smaller file size for equivalent quality, supports audio if needed, requires a video player. Use `ffmpeg` renderer/writer. Better for presentations (PowerPoint plays MP4 natively).

**HTML widget**: `plotly` and `gganimate` can produce HTML animations that play in browsers with interactive controls (play, pause, scrub). Best for dashboards and web reports.

File size optimisation: reduce `nframes` (60–100 is usually sufficient), reduce resolution (`width=600, height=400`), reduce the number of animated elements, use `gifski` which produces ~50% smaller GIFs than alternatives.

### 8. When to Animate: Decision Framework
| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| Show trajectory over time | ANIMATE | Movement IS the story |
| Keynote presentation | ANIMATE | Sequential, captive audience |
| Social media / blog | ANIMATE | Engagement, shareability |
| Compare exact values | STATIC | Can't freeze animation |
| PDF / journal paper | STATIC | Medium doesn't support GIF |
| Analytical dashboard | STATIC | Need random access |
| Gapminder exploration | ANIMATE | Trajectory + wake = insight |
| Print poster | STATIC | No animation on paper |

### References
- Pedersen, T. L. (2020). gganimate: A Grammar of Animated Graphics. https://gganimate.com
- matplotlib.animation: https://matplotlib.org/stable/api/animation_api.html
- Rosling, H. (2006). "The best stats you've ever seen." TED talk.
- Heer, J. & Robertson, G. (2007). "Animated Transitions in Statistical Data Graphics." *IEEE InfoVis*.
- Robertson, G. et al. (2008). "Effectiveness of Animation in Trend Visualization." *IEEE TVCG*.
