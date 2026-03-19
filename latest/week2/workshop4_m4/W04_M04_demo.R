# ============================================================
# Workshop 4 — Module 4: Missing Data Visualization
# R + Python patterns on one script — UNYT Tirana
# ============================================================
library(tidyverse); library(naniar); library(visdat); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv")

# ── Step 1: How much is missing? ──
cat("── Missing % per column ──\n")
miss_var_summary(apps) |> print(n=20)

p_bar <- gg_miss_var(apps) + labs(title="Missing % per Variable")
ggsave("output/miss_bar.png", p_bar, width=7, height=5, dpi=300)

# ── Step 2: Where is it missing? ──
p_matrix <- vis_miss(apps) + labs(title="Missingness Matrix")
ggsave("output/miss_matrix.png", p_matrix, width=8, height=5, dpi=300)

p_dat <- vis_dat(apps) + labs(title="Variable Types + NA")
ggsave("output/vis_dat.png", p_dat, width=8, height=5, dpi=300)

# ── Step 3: Co-occurrence ──
# gg_miss_upset requires at least 2 variables with missing
tryCatch({
  p_upset <- gg_miss_upset(apps, nsets=5)
  ggsave("output/miss_upset.png", p_upset, width=8, height=5, dpi=300)
}, error=function(e) cat("UpSet skipped:", e$message, "\n"))

# ── Step 4: Shadow-augmented scatter ──
apps_num <- apps |> mutate(Reviews=as.numeric(Reviews)) |> filter(!is.na(Rating) | !is.na(Reviews))
p_shadow <- ggplot(apps_num, aes(x=Reviews, y=Rating)) +
  geom_miss_point(alpha=0.3, size=0.5) +
  scale_x_log10(labels=scales::comma) +
  theme_minimal() + labs(title="Shadow Scatter: Reviews vs Rating (NA shown at margin)")
ggsave("output/shadow_scatter.png", p_shadow, width=7, height=5, dpi=300)

# ── Step 5: Shadow histogram — Rating distribution by Size_NA ──
apps_sh <- apps |> mutate(Size_num=case_when(str_detect(Size,"M")~str_remove(Size,"M") |> as.numeric(), TRUE~NA_real_)) |>
  bind_shadow(only_miss=TRUE)
p_sh_hist <- ggplot(apps_sh |> filter(!is.na(Rating)), aes(x=Rating, fill=Size_num_NA)) +
  geom_histogram(bins=30, position="identity", alpha=0.5) +
  scale_fill_manual(values=c("!NA"="#1565C0","NA"="#E53935"), labels=c("Size present","Size missing")) +
  theme_minimal() + labs(title="Rating Distribution: Size Present vs Size Missing", fill=NULL)
ggsave("output/shadow_hist.png", p_sh_hist, width=7, height=4, dpi=300)

cat("\n── All W04-M04 R plots saved ──\n")
