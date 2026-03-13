# Workshop 2 · Module 8 — Homework
## Annotations & Storytelling Mastery

**Due**: Before Workshop 2, Module 10
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 2 homework (5% of total grade)

### Part A — labs() Complete Set (20 points)
Using any chart from your Google Play Store analysis, add all five labs() elements: declarative title, contextual subtitle, source caption, axis labels with units, and legend title. Produce in both R and Python.

### Part B — Four Annotation Types (30 points)
Create a line chart of simulated monthly revenue (12 months). Add all four annotation types: (1) text callout with arrow on the peak month, (2) horizontal mean reference line, (3) target band (axhspan), (4) vertical event marker at month 6. Produce in both R and Python.

### Part C — Storytelling Layers (30 points)
Using the same revenue data, produce four versions showing progressive reveal: (1) data only, (2) + trend line, (3) + event annotation, (4) + declarative title. Arrange as a 2×2 grid using patchwork (R) / GridSpec (Python).

### Part D — Direct Labelling with Repulsion (20 points)
Using the top 15 Google Play Store apps by review count, create a scatter of Reviews (log x) vs Rating. Label each point with the app name using geom_text_repel (R) or adjustText (Python). Show before (overlapping) and after (repelled) versions.

### Submission Checklist
- [ ] `W02_M08_homework.R` + `W02_M08_homework.py`
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
