# Workshop 1 · Module 6 — Homework
## End-to-End Design Process

**Due**: Before Workshop 1, Module 8  
**Format**: PDF report (max 5 pages) + R script + Python script  
**Weight**: Part of Workshop 1 homework (5% of total grade)

---

### Part A — Pipeline Walkthrough (40 points)

1. Using the Google Play Store dataset (`googleplaystore.csv`), execute the
   complete five-step pipeline in both R and Python:

   a. **Acquire**: Load the CSV and print dimensions + column types.
   b. **Parse**: Convert Reviews to integer, handle "Varies with device" in
      Size, filter out rows where Type is neither "Free" nor "Paid".
   c. **Filter**: Keep only the top 10 categories by count.
   d. **Mine**: Compute mean Rating and median Reviews per category.
   e. **Represent**: Produce a polished horizontal bar chart of mean Rating
      by category (sorted, direct-labelled, Tufte-styled).

2. For each step, write a one-sentence comment explaining the design
   decision (e.g., "Filtering to top 10 prevents label overplotting").

---

### Part B — Audience Adaptation (30 points)

Using the output from Part A, create **two versions** of the same chart:

1. **Executive version**: One chart, grey + accent on the highest-rated
   category, bold title stating the key finding, no gridlines, caption
   with source.

2. **Analyst version**: A four-panel dashboard (patchwork / GridSpec)
   showing: (a) bar chart of counts, (b) bar chart of mean ratings,
   (c) boxplot of ratings by category, (d) scatter of Reviews vs Rating.

Produce both versions in R and Python. In 150 words, explain which
design decisions changed and why, referencing Cairo's visualization wheel.

---

### Part C — Munzner Threat Audit (30 points)

Find one published visualization (news, corporate report, or academic paper)
and evaluate it against Munzner's four nested layers:

1. **Layer 1**: Does the chart address a real question the audience has?
2. **Layer 2**: Are the data types correctly abstracted?
3. **Layer 3**: Is the visual encoding effective (channel ranking)?
4. **Layer 4**: Does it render correctly (no overlapping labels, readable)?

Write 200 words identifying the most serious threat and propose a redesign
(sketch or code) that addresses it.

---

### Submission Checklist

- [ ] PDF report (max 5 pages)
- [ ] `W01_M06_homework.R` — complete pipeline + two audience versions
- [ ] `W01_M06_homework.py` — same
- [ ] Exported figures (PDF + PNG)
- [ ] Screenshot/URL of the chart for Part C
