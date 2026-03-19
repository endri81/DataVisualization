# ============================================================
# Workshop 4 — Module 6: Correlation & Association Visualization
# R + Python demo — UNYT Tirana
# ============================================================
library(tidyverse); library(GGally); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |>
  mutate(Reviews=as.numeric(Reviews), Installs=str_remove_all(Installs,"[+,]") |> as.numeric(),
         Price=str_remove(Price,"\\$") |> as.numeric()) |>
  filter(!is.na(Rating), Reviews>0) |>
  mutate(log_reviews=log10(Reviews+1), log_installs=log10(Installs+1))

# 1. ANSCOMBE'S QUARTET
p_ans <- datasets::anscombe |> pivot_longer(everything(),
  names_to=c(".value","set"), names_pattern="(.)(.)" ) |>
  ggplot(aes(x=x, y=y)) + geom_point(color="#1565C0") +
  geom_smooth(method="lm", se=FALSE, color="#E53935", linewidth=0.8) +
  facet_wrap(~set, ncol=2) + theme_minimal(base_size=9) +
  labs(title="Anscombe's Quartet: r = 0.82 in all four")
ggsave("output/anscombe.png", p_ans, width=7, height=6, dpi=300)

# 2. CORRELATION HEATMAP
num_cols <- apps |> select(Rating, log_reviews, log_installs, Price) |> drop_na()
corr <- cor(num_cols)
# Manual ggplot heatmap
corr_df <- as.data.frame(as.table(corr)) |> rename(Var1=Var1, Var2=Var2, r=Freq) |>
  mutate(lower=as.numeric(Var1)>=as.numeric(Var2))
p_heat <- ggplot(corr_df |> filter(lower), aes(x=Var1, y=Var2, fill=r)) +
  geom_tile(color="white", linewidth=1) +
  geom_text(aes(label=round(r,2)), size=4, fontface="bold") +
  scale_fill_gradient2(low="#E53935", mid="white", high="#1565C0", midpoint=0, limits=c(-1,1)) +
  theme_minimal() + labs(title="Correlation Heatmap (lower triangle)", fill="Pearson r") +
  theme(axis.text.x=element_text(angle=30, hjust=1))
ggsave("output/corr_heatmap.png", p_heat, width=6, height=5, dpi=300)

# 3. PAIRS PLOT
p_pairs <- ggpairs(apps |> select(Rating, log_reviews, Price, Type) |> drop_na() |> slice_sample(n=1000),
  mapping=aes(color=Type, alpha=0.3),
  lower=list(continuous=wrap("points",size=0.5)),
  diag=list(continuous=wrap("densityDiag")),
  upper=list(continuous=wrap("cor",size=3))) +
  scale_color_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal(base_size=7)
ggsave("output/pairs_plot.png", p_pairs, width=8, height=8, dpi=300)

# 4. CATEGORICAL ASSOCIATION
cat_table <- apps |> filter(Category %in% c("GAME","FAMILY","TOOLS","BUSINESS","MEDICAL")) |>
  count(Category, Type) |> group_by(Category) |> mutate(pct=n/sum(n))
p_cat <- ggplot(cat_table, aes(x=Category, y=pct, fill=Type)) +
  geom_col(width=0.6, color="white") +
  scale_fill_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  scale_y_continuous(labels=scales::percent) + coord_flip() +
  theme_minimal() + labs(title="100% Stacked: Type x Category")
ggsave("output/categorical_assoc.png", p_cat, width=7, height=4, dpi=300)

cat("\n── All W04-M06 R plots saved ──\n")
