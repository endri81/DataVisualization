# ============================================================
# Workshop 4 — Module 1: Tukey's EDA Philosophy
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(!is.na(Rating))

# 1. INSPECT
cat("Dimensions:", dim(apps), "\n")
glimpse(apps)
summary(apps$Rating)

# 2. 4-PLOT DIAGNOSTIC PANEL
n <- nrow(apps); vals <- apps$Rating
p_run <- ggplot(tibble(i=1:n, v=vals), aes(x=i, y=v)) +
  geom_line(linewidth=0.1, alpha=0.3, color="#1565C0") +
  geom_hline(yintercept=mean(vals), color="#E53935", linetype="dashed") +
  theme_minimal(base_size=8) + labs(title="(a) Run Sequence", x="Index", y="Rating")

p_lag <- ggplot(tibble(x=vals[-n], y=vals[-1]), aes(x=x, y=y)) +
  geom_point(alpha=0.05, size=0.3, color="#1565C0") +
  theme_minimal(base_size=8) + labs(title="(b) Lag-1 Plot", x="Y(i)", y="Y(i+1)")

p_hist <- ggplot(apps, aes(x=Rating)) +
  geom_histogram(bins=30, fill="#1565C0", color="white") +
  theme_minimal(base_size=8) + labs(title="(c) Histogram")

p_qq <- ggplot(apps, aes(sample=Rating)) +
  geom_qq(alpha=0.1, size=0.3, color="#1565C0") +
  geom_qq_line(color="#E53935", linewidth=1) +
  theme_minimal(base_size=8) + labs(title="(d) Q-Q Plot")

four_plot <- (p_run | p_lag) / (p_hist | p_qq) +
  plot_annotation(title="Tukey's 4-Plot: Google Play Store Ratings")
ggsave("output/four_plot.png", four_plot, width=9, height=7, dpi=300)

# 3. EDA FIRST LOOK: hist + box + qq
p1 <- ggplot(apps, aes(x=Rating)) + geom_histogram(bins=30, fill="#1565C0", color="white") +
  theme_minimal(base_size=9) + labs(title="(a) Histogram")
p2 <- ggplot(apps, aes(x="", y=Rating)) + geom_boxplot(fill="#BBDEFB", width=0.3) +
  theme_minimal(base_size=9) + labs(title="(b) Boxplot", x=NULL)
p3 <- ggplot(apps, aes(sample=Rating)) + geom_qq(alpha=0.1, size=0.3) +
  geom_qq_line(color="#E53935") + theme_minimal(base_size=9) + labs(title="(c) Q-Q")
ggsave("output/eda_first_look.png", p1|p2|p3, width=10, height=3.5, dpi=300)

# 4. LETTER-VALUE PLOT (geom_lv requires lvplot extension, so show boxenplot concept)
# library(lvplot)
# ggplot(apps, aes(x=Type, y=Rating)) + geom_lv(fill="#1565C0", alpha=0.3) + theme_minimal()

# 5. SKIMR SUMMARY
# library(skimr)
# skim(apps |> select(Rating, Reviews, Type, Category))

cat("\n── All W04-M01 R plots saved ──\n")
