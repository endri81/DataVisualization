# ============================================================
# Workshop 3 — Module 8: Small Multiples & Faceted Displays
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"),!is.na(Rating)) |>
  mutate(Reviews=as.numeric(Reviews))
top6 <- apps |> count(Category,sort=TRUE) |> slice_max(n,n=6) |> pull(Category)
df6 <- apps |> filter(Category %in% top6)

# 1. SPAGHETTI → SMALL MULTIPLES
p_spag <- ggplot(df6, aes(x=Rating,color=Category)) +
  geom_density(linewidth=0.8) + scale_color_brewer(palette="Set2") +
  theme_minimal() + theme(legend.position="bottom") +
  labs(title="(a) Spaghetti: 6 overlapping densities")

p_facet <- ggplot(df6, aes(x=Rating)) +
  geom_density(fill="#1565C0",alpha=0.2,color="#1565C0") +
  facet_wrap(~Category,ncol=3,scales="fixed") +
  theme_minimal(base_size=8) +
  labs(title="(b) Small Multiples: facet_wrap(~Category)")

ggsave("output/spag_vs_sm.png",p_spag / p_facet,width=9,height=8,dpi=300)

# 2. HETEROGENEOUS DASHBOARD — patchwork
p_bar <- df6 |> count(Category) |> mutate(Category=fct_reorder(Category,n)) |>
  ggplot(aes(x=Category,y=n,fill=Category)) +
  geom_col(show.legend=FALSE,width=0.5) + scale_fill_brewer(palette="Set2") +
  coord_flip() + theme_minimal(base_size=9) + labs(title="(a) Counts",x=NULL,y=NULL)

p_hist <- ggplot(df6, aes(x=Rating)) +
  geom_histogram(bins=30,fill="#1565C0",color="white") +
  theme_minimal(base_size=9) + labs(title="(b) Ratings")

p_scatter <- df6 |> filter(Reviews>0) |>
  ggplot(aes(x=Reviews,y=Rating,color=Type)) +
  geom_point(alpha=0.2,size=0.5) + scale_x_log10(labels=scales::comma) +
  scale_color_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal(base_size=9) + theme(legend.position="bottom") + labs(title="(c) Reviews vs Rating")

p_box <- ggplot(df6, aes(x=Type,y=Rating,fill=Type)) +
  geom_boxplot(width=0.5,outlier.alpha=0.1) +
  scale_fill_manual(values=c(Free="#BBDEFB",Paid="#FFCDD2")) +
  theme_minimal(base_size=9) + theme(legend.position="none") + labs(title="(d) Free vs Paid")

dashboard <- (p_bar | p_hist) / (p_scatter | p_box) +
  plot_annotation(
    title="Google Play Store: Multi-Panel Dashboard",
    subtitle="Four chart types composed with patchwork",
    caption="Source: Kaggle | UNYT Data Visualization Course",
    tag_levels="a") &
  theme_minimal(base_size=9)

ggsave("output/dashboard_patchwork.png",dashboard,width=11,height=8,dpi=300)
ggsave("output/dashboard_patchwork.pdf",dashboard,width=11,height=8)

# 3. ASYMMETRIC LAYOUT — wide + narrow
p_wide <- df6 |> filter(Reviews>0) |>
  ggplot(aes(x=Reviews,y=Rating)) +
  geom_point(alpha=0.1,size=0.3) + scale_x_log10() +
  geom_smooth(method="lm",color="#E53935") +
  theme_minimal(base_size=9) + labs(title="(a) Scatter + Trend (wide)")

p_narrow1 <- ggplot(df6,aes(x=Rating)) +
  geom_histogram(bins=30,fill="#2E7D32",color="white") +
  theme_minimal(base_size=8) + labs(title="(b) Histogram")

p_narrow2 <- ggplot(df6,aes(x=Type,y=Rating,fill=Type)) +
  geom_violin(alpha=0.3) + geom_boxplot(width=0.1,outlier.shape=NA,fill="white") +
  scale_fill_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal(base_size=8) + theme(legend.position="none") + labs(title="(c) Violin")

asymm <- p_wide / (p_narrow1 | p_narrow2) + plot_layout(heights=c(2,1))
ggsave("output/asymmetric.png",asymm,width=10,height=7,dpi=300)

cat("\n── All W03-M08 R plots saved ──\n")
