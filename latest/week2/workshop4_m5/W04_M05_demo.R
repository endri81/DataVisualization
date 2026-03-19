# ============================================================
# Workshop 4 — Module 5: Outlier Detection & Visual Diagnostics
# R + Python patterns — UNYT Tirana
# ============================================================
library(tidyverse); library(broom); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |>
  mutate(Reviews=as.numeric(Reviews)) |> filter(!is.na(Rating),!is.na(Reviews),Reviews>0)

# 1. IQR DETECTION — boxplot with flagged outliers
q1 <- quantile(apps$Rating, 0.25); q3 <- quantile(apps$Rating, 0.75); iqr_val <- q3-q1
apps <- apps |> mutate(outlier_iqr = Rating < q1-1.5*iqr_val | Rating > q3+1.5*iqr_val)
cat("IQR outliers:", sum(apps$outlier_iqr), "of", nrow(apps), "\n")

p_box <- ggplot(apps, aes(x=Type, y=Rating)) +
  geom_boxplot(outlier.colour="#E53935", outlier.size=1, fill="#BBDEFB", width=0.4) +
  geom_jitter(data=apps |> filter(outlier_iqr), aes(color=outlier_iqr), width=0.15, size=0.5, alpha=0.5) +
  scale_color_manual(values=c("TRUE"="#E53935"), guide="none") +
  theme_minimal() + labs(title="IQR Outliers Flagged in Red")
ggsave("output/iqr_boxplot.png", p_box, width=6, height=5, dpi=300)

# 2. REGRESSION DIAGNOSTICS
model <- lm(Rating ~ log10(Reviews+1), data=apps)
diag_df <- augment(model)

p_resid <- ggplot(diag_df, aes(x=.fitted, y=.resid)) +
  geom_point(alpha=0.1, size=0.3) + geom_hline(yintercept=0, linetype="dashed") +
  geom_smooth(se=FALSE, color="#E53935", linewidth=0.8) +
  theme_minimal() + labs(title="(a) Residuals vs Fitted")

p_qq <- ggplot(diag_df, aes(sample=.std.resid)) +
  geom_qq(alpha=0.1, size=0.3) + geom_qq_line(color="#E53935") +
  theme_minimal() + labs(title="(b) Q-Q of Std Residuals")

p_cook <- ggplot(diag_df |> mutate(idx=row_number()), aes(x=idx, y=.cooksd)) +
  geom_col(width=0.3, fill="#1565C0") +
  geom_hline(yintercept=4/nrow(diag_df), color="#E53935", linetype="dashed") +
  theme_minimal() + labs(title="(c) Cook's Distance", x="Observation")

library(patchwork)
ggsave("output/regression_diag.png", (p_resid|p_qq)/p_cook, width=10, height=7, dpi=300)

# 3. FIT WITH AND WITHOUT
influential <- diag_df$.cooksd > 4/nrow(diag_df)
cat("Influential points:", sum(influential), "\n")
model2 <- lm(Rating ~ log10(Reviews+1), data=apps[!influential,])
cat("Full model: slope =", round(coef(model)[2],4), ", R² =", round(summary(model)$r.squared,4), "\n")
cat("Without influential: slope =", round(coef(model2)[2],4), ", R² =", round(summary(model2)$r.squared,4), "\n")

cat("\n── All W04-M05 R plots saved ──\n")
