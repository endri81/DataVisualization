# ============================================================
# Workshop 1 — Module 8: R Environment Setup & Base Graphics
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

# ── 0. Verify Installation ─────────────────────────────────
cat("R version:", R.version.string, "\n")
cat("Working directory:", getwd(), "\n\n")

# ── 1. Install & Load Packages ─────────────────────────────
# Run once: install.packages("tidyverse")
library(tidyverse)
dir.create("output", showWarnings = FALSE)

# ── 2. Data Types ──────────────────────────────────────────
# Numeric
x_num <- c(10.5, 20.3, 30.1)
cat("numeric:", class(x_num), "\n")

# Integer
x_int <- c(1L, 2L, 3L)
cat("integer:", class(x_int), "\n")

# Character
x_chr <- c("Alice", "Bob", "Carol")
cat("character:", class(x_chr), "\n")

# Logical
x_lgl <- c(TRUE, FALSE, TRUE)
cat("logical:", class(x_lgl), "\n")

# Factor (categorical)
x_fct <- factor(c("Low", "Med", "High"), levels = c("Low", "Med", "High"), ordered = TRUE)
cat("factor:", class(x_fct), "\n")

# Date
x_date <- as.Date("2024-01-15")
cat("Date:", class(x_date), "\n\n")


# ── 3. Load & Inspect Data ────────────────────────────────
# Using built-in mpg dataset
data(mpg)
cat("Dimensions:", dim(mpg), "\n")
glimpse(mpg)
cat("\nMissing values:", sum(is.na(mpg)), "\n\n")


# ── 4. Base R: Scatterplot ─────────────────────────────────
png("output/base_scatter.png", width = 600, height = 450, res = 150)
plot(mpg$displ, mpg$hwy,
     main = "Engine Displacement vs Highway MPG",
     xlab = "Displacement (litres)",
     ylab = "Highway MPG",
     pch  = 16,
     col  = adjustcolor("steelblue", alpha = 0.6),
     cex  = 0.8)
abline(lm(hwy ~ displ, data = mpg), col = "red", lwd = 2)
legend("topright", legend = "OLS fit", col = "red", lwd = 2, bty = "n")
dev.off()


# ── 5. Base R: Histogram ──────────────────────────────────
png("output/base_hist.png", width = 600, height = 450, res = 150)
hist(mpg$hwy,
     breaks = 25,
     col    = "lightblue",
     border = "white",
     main   = "Highway MPG Distribution",
     xlab   = "Highway MPG",
     las    = 1)
abline(v = mean(mpg$hwy), col = "red", lwd = 2, lty = 2)
legend("topright", legend = paste("Mean:", round(mean(mpg$hwy), 1)),
       col = "red", lwd = 2, lty = 2, bty = "n")
dev.off()


# ── 6. Base R: Bar Chart ──────────────────────────────────
png("output/base_bar.png", width = 600, height = 500, res = 150)
par(mar = c(5, 8, 4, 2))  # Extra left margin for labels
counts <- sort(table(mpg$class))
barplot(counts,
        horiz     = TRUE,
        col       = "steelblue",
        border    = NA,
        main      = "Vehicle Count by Class",
        xlab      = "Count",
        las       = 1,
        cex.names = 0.8)
dev.off()


# ── 7. Base R: Boxplot ────────────────────────────────────
png("output/base_box.png", width = 600, height = 450, res = 150)
boxplot(hwy ~ cyl, data = mpg,
        main   = "Highway MPG by Cylinder Count",
        xlab   = "Cylinders",
        ylab   = "Highway MPG",
        col    = c("#E3F2FD", "#BBDEFB", "#90CAF9", "#42A5F5"),
        border = "grey40",
        las    = 1)
# Add mean points
means <- tapply(mpg$hwy, mpg$cyl, mean)
points(seq_along(means), means, pch = 18, col = "red", cex = 1.5)
dev.off()


# ── 8. Multi-Panel with par(mfrow) ────────────────────────
png("output/base_multipanel.png", width = 800, height = 600, res = 150)
old_par <- par(mfrow = c(2, 2), mar = c(4, 4, 3, 1))

# Panel 1: scatter
plot(mpg$displ, mpg$hwy, pch = 16, cex = 0.5, col = "steelblue",
     main = "Scatter", xlab = "Displacement", ylab = "MPG")

# Panel 2: histogram
hist(mpg$hwy, breaks = 20, col = "lightblue", border = "white",
     main = "Distribution", xlab = "Highway MPG")

# Panel 3: bar chart
barplot(table(mpg$class), col = "steelblue", border = NA,
        main = "Vehicle Class", las = 2, cex.names = 0.6)

# Panel 4: boxplot
boxplot(hwy ~ cyl, data = mpg, col = "lightblue",
        main = "MPG by Cylinders", xlab = "Cyl", ylab = "MPG")

par(old_par)  # Restore
dev.off()


# ── 9. Pipe Operator Demo ─────────────────────────────────
# The pipe |> passes the left side as the first argument
# to the right side function

result <- mpg |>
  filter(year == 2008, cyl %in% c(4, 6)) |>
  group_by(class) |>
  summarise(
    n = n(),
    mean_hwy = round(mean(hwy), 1),
    .groups = "drop"
  ) |>
  arrange(desc(mean_hwy))

cat("\n── Pipe result: 2008 4/6-cyl vehicles ──\n")
print(result)

# Quick ggplot2 preview (covered in Workshop 2)
p_preview <- ggplot(result, aes(x = reorder(class, mean_hwy), y = mean_hwy)) +
  geom_col(fill = "#1565C0", width = 0.6) +
  geom_text(aes(label = mean_hwy), hjust = -0.2, size = 3, fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  labs(title = "Mean Highway MPG by Class (2008, 4/6-cyl)",
       x = NULL, y = "Mean Highway MPG")

ggsave("output/pipe_ggplot_preview.png", p_preview, width = 7, height = 4, dpi = 300)

cat("\n── All M08 plots saved to output/ ──\n")
