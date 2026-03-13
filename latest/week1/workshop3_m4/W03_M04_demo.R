# ============================================================
# Workshop 3 — Module 4: Relationships — Scatter, Bubble & Hexbin
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"),!is.na(Rating)) |>
  mutate(Reviews=as.numeric(Reviews))

# 1. SCATTER + REGRESSION
p1 <- apps |> filter(Reviews>0) |>
  ggplot(aes(x=Reviews,y=Rating,color=Type)) +
  geom_point(alpha=0.3,size=0.5) +
  geom_smooth(method="lm",se=TRUE,linewidth=0.8) +
  scale_x_log10(labels=scales::comma) +
  scale_color_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  coord_cartesian(ylim=c(1,5)) + theme_minimal() +
  labs(title="(a) Scatter + OLS",x="Reviews (log)",y="Rating")

# 2. HEXBIN
p2 <- apps |> filter(Reviews>0,!is.na(Rating)) |>
  ggplot(aes(x=Reviews,y=Rating)) +
  geom_hex(bins=30) + scale_fill_viridis_c() + scale_x_log10(labels=scales::comma) +
  theme_minimal() + labs(title="(b) Hexbin (n > 9K)")

# 3. BUBBLE (simulated Gapminder-like)
set.seed(66)
gap <- tibble(gdp=runif(50,5,80),life=55+0.35*gdp+rnorm(50,0,5),pop=runif(50,1e6,8e8),
              cont=sample(c("Africa","Asia","Europe","Americas"),50,TRUE))
p3 <- ggplot(gap,aes(x=gdp,y=life,color=cont,size=pop)) +
  geom_point(alpha=0.5) + scale_size(range=c(1,12),guide="none") +
  scale_color_brewer(palette="Set2") + theme_minimal() +
  labs(title="(c) Bubble: 4 variables",x="GDP ($K)",y="Life Exp.",color="Continent")

# 4. 2D DENSITY
p4 <- apps |> filter(Reviews>0,!is.na(Rating)) |>
  ggplot(aes(x=Reviews,y=Rating)) +
  geom_density_2d_filled(alpha=0.7) + scale_x_log10(labels=scales::comma) +
  theme_minimal() + theme(legend.position="none") +
  labs(title="(d) 2D Density Contour")

p_all <- (p1 | p2) / (p3 | p4) + plot_annotation(title="Four Relationship Charts")
ggsave("output/relationship_charts.png",p_all,width=12,height=9,dpi=300)

# 5. MARGINAL (requires ggExtra)
# library(ggExtra)
# p_base <- ggplot(apps |> filter(Reviews>0), aes(x=Reviews,y=Rating)) +
#   geom_point(alpha=0.15,size=0.5) + scale_x_log10() + theme_minimal()
# p_marginal <- ggMarginal(p_base, type="histogram", fill="#1565C0", color="white")
# ggsave("output/marginal.png", p_marginal, width=7, height=6, dpi=300)

cat("\n── All W03-M04 R plots saved ──\n")
