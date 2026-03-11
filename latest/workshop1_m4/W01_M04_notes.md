# Workshop 1 · Module 4 — Course Notes
## Color Theory & Accessibility

---

### 1. The Three Dimensions of Colour

Every colour can be decomposed into three perceptual dimensions. **Hue** is the colour name — red, blue, green — and functions as a categorical channel: distinct hues represent distinct categories but imply no order. **Saturation** (chroma) measures the vividness of a colour relative to grey; it serves as an ordinal or emphasis channel. **Lightness** (value, luminance) runs from black to the full brightness of the hue and is the strongest perceptual channel for encoding quantitative magnitude because the human visual system is exquisitely sensitive to luminance gradients (Ware, 2021).

The critical design rule: map the data type to the correct colour dimension. Use hue for nominal distinctions, lightness for quantitative sequences, and saturation sparingly for emphasis. Conflating these dimensions — e.g., varying hue for a quantitative variable — produces the rainbow problem.


### 2. Palette Typology

**Sequential** palettes map low-to-high values as a monotonic lightness ramp (e.g., Blues, YlGnBu, viridis). They are appropriate for any ordered, single-direction variable: counts, proportions, concentrations.

**Diverging** palettes use two hues anchored at a neutral midpoint (e.g., RdBu, RdYlGn). They encode deviation from a meaningful centre — profit/loss, above/below average, positive/negative sentiment. The midpoint must align with the semantic zero of the data; otherwise the two hues create a false dichotomy.

**Qualitative** palettes use maximally distinguishable hues at similar lightness (e.g., Set1, Set2, tab10). They are appropriate for nominal categories. Effectiveness degrades sharply beyond 7 hues because perceptual distinctness collapses.

Brewer (2003) empirically tested palettes for cartographic legibility across media (screen, print, photocopy) and colour vision deficiency. The ColorBrewer tool (https://colorbrewer2.org) remains the standard reference for palette selection.


### 3. Perceptual Uniformity and the Rainbow Problem

A perceptually uniform colourmap ensures that equal steps in data produce equal perceived steps in colour. The rainbow (jet) colourmap violates this criterion: it contains abrupt lightness jumps at yellow and cyan that create false contour bands unrelated to data structure (Crameri et al., 2020). Borland and Taylor (2007) demonstrated that rainbow colourmaps cause misinterpretation in medical imaging, meteorology, and fluid dynamics.

The viridis family (viridis, magma, plasma, inferno) was designed by van der Walt and Smith (2015) to be perceptually uniform, monotonically increasing in lightness, and safe under all three forms of colour vision deficiency. The cividis palette (Nuñez et al., 2018) is optimised specifically for deuteranopia and protanopia.


### 4. Colour Vision Deficiency (CVD)

Approximately 8% of males and 0.5% of females have some form of CVD. The three main types are deuteranopia (red–green, most common), protanopia (red–green, shifted), and tritanopia (blue–yellow, rare). Red and green become nearly indistinguishable under deuteranopia, rendering red-green categorical palettes useless.

Accessible design strategies include: (a) using viridis or cividis, which are safe by construction; (b) supplementing colour with a redundant channel — shape, line style, pattern, or direct label; (c) simulating CVD before publication using R's `colorspace::deutan()` or Python's `colorspacious` package; and (d) limiting qualitative palettes to ≤7 hues.


### 5. WCAG Contrast and the Grey-Plus-Accent Strategy

The Web Content Accessibility Guidelines (WCAG 2.1) specify minimum contrast ratios for text legibility: 4.5:1 for AA (normal text), 3:1 for AA (large text), and 7:1 for AAA. These ratios apply to chart annotations, axis labels, and legend text. Tools such as WebAIM's contrast checker (https://webaim.org/resources/contrastchecker/) automate verification.

The grey-plus-accent strategy is the single most effective colour technique for explanatory visualization. All non-focal data points are rendered in neutral grey (#BBBBBB) at low alpha; the focal subset is highlighted with a single saturated accent colour (#E53935). This leverages pre-attentive colour pop-out (Module 3) while eliminating palette-selection complexity. The pattern works identically in R (via `scale_color_manual()`) and Python (via two sequential `scatter()` calls).


### References

- Borland, D. & Taylor, R. M. (2007). Rainbow color map (still) considered harmful. *IEEE CG&A*, 27(2), 14–17.
- Brewer, C. A. (2003). A transition in improving maps: The ColorBrewer example. *Cartography and GIS*, 30(2), 159–162.
- Crameri, F., Shephard, G. E. & Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications*, 11, 5444.
- Nuñez, J. R., Anderton, C. R. & Renslow, R. S. (2018). Optimizing colormaps with consideration for color vision deficiency. *PLOS ONE*, 13(7).
- van der Walt, S. & Smith, N. (2015). A better default colormap for matplotlib. SciPy 2015.
- Ware, C. (2021). *Information Visualization*, 4th ed. Morgan Kaufmann.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly.
