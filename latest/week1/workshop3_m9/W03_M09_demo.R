# ============================================================
# Workshop 3 — Module 9: Tables as Visualization
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"),!is.na(Rating))

# 1. GT STYLED TABLE
# install.packages("gt")
# library(gt)
# summary_df <- apps |>
#   group_by(Category) |>
#   summarise(Count=n(), `Mean Rating`=mean(Rating),
#     `Paid %`=mean(Type=="Paid"), .groups="drop") |>
#   slice_max(Count, n=8)
#
# gt_table <- summary_df |>
#   gt() |>
#   tab_header(title="Top 8 App Categories",
#     subtitle="Google Play Store Summary Statistics") |>
#   data_color(columns=`Mean Rating`, palette="RdYlGn") |>
#   fmt_number(columns=Count, use_seps=TRUE) |>
#   fmt_percent(columns=`Paid %`, decimals=0) |>
#   tab_source_note("Source: Kaggle Google Play Store dataset") |>
#   opt_row_striping() |>
#   tab_style(style=cell_text(weight="bold"),
#     locations=cells_column_labels())
# gtsave(gt_table, "output/gt_styled.html")

# 2. KABLEEXTRA
# library(kableExtra)
# summary_df |>
#   kable(format="html", digits=c(0,0,2,2),
#     col.names=c("Category","Count","Mean Rating","Paid %")) |>
#   kable_styling(bootstrap_options=c("striped","hover","condensed"),
#     full_width=FALSE, font_size=12) |>
#   row_spec(0, bold=TRUE, color="white", background="#1565C0") |>
#   column_spec(2, bold=TRUE) |>
#   save_kable("output/kable_styled.html")

# 3. CONDITIONAL FORMATTING — simulated with ggplot table
summary_df <- apps |>
  group_by(Category) |>
  summarise(Count=n(), Mean_Rating=mean(Rating),
    Paid_Pct=mean(Type=="Paid"), .groups="drop") |>
  slice_max(Count, n=6) |>
  arrange(desc(Count))

# Heatmap-style table via ggplot
p_heat <- ggplot(summary_df |> mutate(Category=fct_inorder(Category)),
  aes(x=1, y=fct_rev(Category), fill=Mean_Rating)) +
  geom_tile(color="white", linewidth=1.5) +
  geom_text(aes(label=sprintf("%.2f", Mean_Rating)), fontface="bold", size=4) +
  scale_fill_gradient2(low="#E53935", mid="#FFECB3", high="#2E7D32",
    midpoint=mean(summary_df$Mean_Rating)) +
  theme_void() + theme(legend.position="none",
    axis.text.y=element_text(hjust=1, size=9, face="bold")) +
  labs(title="Mean Rating by Category (Heatmap Table)")
ggsave("output/heatmap_table.png", p_heat, width=4, height=4, dpi=300)

cat("\n── All W03-M09 R plots saved ──\n")
cat("Note: gt and kableExtra examples are commented; uncomment to run.\n")
