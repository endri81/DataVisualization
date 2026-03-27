# Workshop 7 — Final Homework
## Lab: Build a 10-Slide Data Story Deck

**Due**: Before Workshop 8, Module 1
**Format**: R script + Python script + PDF report (max 10 pages)
**Weight**: 5% of total grade (summative assessment for Workshop 7)

### Dataset Choice
Choose ONE: Netflix, e-Car, Google Play Store, or Real Estate.

### Required Components (100 marks)

**1. Big Idea Statement (10 marks)**
Write one sentence: "[Subject] should [action] because [evidence]." This sentence anchors the entire deck. State the target audience (executive, technical, or public).

**2. Storyboard Table (15 marks)**
A 10-row table with columns: slide number, role (context/complication/evidence/mechanism/resolution/CTA), assertion headline (<15 words), story type (from M04), chart type. The storyboard must follow a coherent story arc.

**3. Hero Chart — Slide 3 (15 marks)**
The complication/hero chart with ALL annotation techniques: declarative title, grey+accent, direct labels, callout box with curved arrow, reference line, shaded region. This is the single most important chart. Produce in both R and Python.

**4. Six Supporting Slides — Slides 2, 4–8 (30 marks)**
Six assertion-evidence slides: context, three evidence slides (at least 3 different story types from M04), mechanism, and resolution. Each slide = one assertion headline + one full-width annotated chart. No bullet points. Produce in both R and Python.

**5. Audience Variant — Slide 9 (10 marks)**
Take the hero finding and adapt it for a DIFFERENT audience than the main deck. If the deck targets executives, produce the technical or public version. Adjust all six adaptation dimensions (title, complexity, annotations, legend, jargon, CTA).

**6. Composed Deck Panel (5 marks)**
Compose slides 2–9 as a vertical panel using patchwork (R) / subplots (Python). Save as PNG (300 DPI) and include in the PDF report.

**7. Code Quality (5 marks)**
Scripts must run end-to-end without errors, use `theme_set()` / `rcParams` for global clean theme, and include comments explaining each slide's narrative role.

**8. Reflection Essay (10 marks)**
In 300 words: (a) how many EDA findings did you start with, and how many survived? (b) what was your selection criterion? (c) which slide was hardest to build? (d) what would you change if the audience were different? (e) what did you learn about the difference between finding patterns and communicating them?

### Submission Checklist
- [ ] `W07_homework.R` + `W07_homework.py` (complete scripts)
- [ ] Individual slide PNGs: slide02–slide09 (300 DPI each)
- [ ] Composed deck panel PNG (300 DPI)
- [ ] PDF report (max 10 pages): Big Idea, storyboard table, all slides, reflection
