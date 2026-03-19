# ============================================================
# Workshop 4 — Module 2: Data Wrangling for Visualization (R)
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

# ── FULL CLEANING PIPELINE ──────────────────────────────
apps_clean <- read_csv("googleplaystore.csv") |>
  distinct(App, .keep_all = TRUE) |>
  mutate(
    Reviews  = as.numeric(Reviews),
    Installs = str_remove_all(Installs, "[+,]") |> as.numeric(),
    Size     = case_when(
      str_detect(Size, "M") ~ str_remove(Size, "M") |> as.numeric(),
      str_detect(Size, "k") ~ str_remove(Size, "k") |> as.numeric() / 1024,
      TRUE ~ NA_real_),
    Price    = str_remove(Price, "\\$") |> as.numeric(),
    date     = mdy(`Last Updated`),
    year     = year(date)
  ) |>
  filter(!is.na(Rating), Type %in% c("Free", "Paid")) |>
  mutate(Category = fct_lump_n(Category, 8) |> fct_infreq())

# ── 1. PIPE-TO-PLOT: summarise → bar ────────────────────
p1 <- apps_clean |>
  group_by(Category) |>
  summarise(mean_r=mean(Rating), n=n(), .groups="drop") |>
  slice_max(n, n=8) |>
  mutate(Category=fct_reorder(Category, mean_r), hl=mean_r==max(mean_r)) |>
  ggplot(aes(x=Category, y=mean_r, fill=hl)) +
  geom_col(width=0.5, show.legend=FALSE) +
  geom_text(aes(label=round(mean_r,2)), hjust=-0.2, size=3, fontface="bold") +
  scale_fill_manual(values=c("TRUE"="#1565C0","FALSE"="#BBBBBB")) +
  coord_flip() + theme_minimal() +
  labs(title="(a) Mean Rating by Top Categories", x=NULL, y="Mean Rating")

# ── 2. PIPE-TO-PLOT: filter → scatter ───────────────────
p2 <- apps_clean |>
  filter(Reviews > 0) |>
  ggplot(aes(x=Reviews, y=Rating, color=Type)) +
  geom_point(alpha=0.2, size=0.5) +
  scale_x_log10(labels=scales::comma) +
  scale_color_manual(values=c(Free="#1565C0", Paid="#E53935")) +
  theme_minimal() + theme(legend.position="bottom") +
  labs(title="(b) Reviews vs Rating (pipe → scatter)", x="Reviews (log)", y="Rating")

# ── 3. PIVOT_LONGER DEMO ────────────────────────────────
# Simulated wide data
df_wide <- tibble(
  region = c("Tirana","Durres","Vlore","Elbasan"),
  Q1 = c(120,90,65,78), Q2 = c(135,95,72,82),
  Q3 = c(128,88,70,75), Q4 = c(150,110,80,95))

p3 <- df_wide |>
  pivot_longer(cols=Q1:Q4, names_to="quarter", values_to="revenue") |>
  ggplot(aes(x=quarter, y=revenue, color=region, group=region)) +
  geom_line(linewidth=1) + geom_point(size=2) +
  scale_color_brewer(palette="Set2") +
  theme_minimal() + labs(title="(c) After pivot_longer: Line Chart Ready")

# ── 4. GROUP_BY + SUMMARISE → POINTRANGE ────────────────
p4 <- apps_clean |>
  filter(Category != "Other") |>
  group_by(Category) |>
  summarise(mean_r=mean(Rating), se=sd(Rating)/sqrt(n()), .groups="drop") |>
  mutate(Category=fct_reorder(Category, mean_r)) |>
  ggplot(aes(x=Category, y=mean_r)) +
  geom_pointrange(aes(ymin=mean_r-1.96*se, ymax=mean_r+1.96*se), color="#1565C0", linewidth=0.8) +
  coord_flip() + theme_minimal() +
  labs(title="(d) group_by → summarise → pointrange", x=NULL, y="Mean Rating ± 95% CI")

ggsave("output/wrangling_panels.png", (p1|p2)/(p3|p4), width=12, height=9, dpi=300)

# ── 5. CLEANING BEFORE/AFTER ────────────────────────────
cat("── Before cleaning ──\n")
cat("Rows:", nrow(read_csv("googleplaystore.csv", show_col_types=FALSE)), "\n")
cat("── After cleaning ──\n")
cat("Rows:", nrow(apps_clean), "\n")
cat("Columns:", ncol(apps_clean), "\n")
cat("NA in Rating:", sum(is.na(apps_clean$Rating)), "\n")

cat("\n── All W04-M02 R plots saved ──\n")
