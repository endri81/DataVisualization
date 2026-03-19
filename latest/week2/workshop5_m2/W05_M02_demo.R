# ============================================================
# Workshop 5 — Module 2: Parallel Coordinates & Radar Charts
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(GGally); dir.create("output",showWarnings=FALSE)
set.seed(42); n <- 500
ecar <- tibble(FICO=rnorm(n,700,50)|>pmax(500)|>pmin(850),
  Rate=12-0.01*FICO+rnorm(n,0,1), Amount=runif(n,5000,50000),
  Term=sample(c(36,48,60,72),n,replace=TRUE,prob=c(.15,.25,.35,.25)),
  Spread=Rate-runif(n,1,4), Tier=cut(FICO,breaks=c(0,620,680,720,760,900),labels=1:5))

# 1. PARALLEL COORDINATES — basic
p_par <- ggparcoord(ecar, columns=c("FICO","Rate","Amount","Term","Spread"),
  groupColumn="Tier", scale="uniminmax", alphaLines=0.15) +
  scale_color_viridis_d() + theme_minimal() +
  labs(title="Parallel Coordinates: Coloured by Tier", color="Tier")
ggsave("output/parcoord.png",p_par,width=9,height=5,dpi=300)

# 2. PARALLEL COORDINATES — highlight Tier 1
ecar2 <- ecar |> mutate(hl=Tier=="1")
p_hl <- ggparcoord(ecar2, columns=c("FICO","Rate","Amount","Term","Spread"),
  groupColumn="hl", scale="uniminmax", alphaLines=0.05) +
  scale_color_manual(values=c("TRUE"="#E53935","FALSE"="#CCCCCC"), guide="none") +
  theme_minimal() + labs(title="Highlight Tier 1 (grey+accent)")
ggsave("output/parcoord_highlight.png",p_hl,width=9,height=5,dpi=300)

# 3. RADAR CHART (manual coord_polar)
profiles <- ecar |> group_by(Tier) |>
  summarise(across(c(FICO,Rate,Amount,Term,Spread), ~scales::rescale(mean(.x),from=range(ecar[[cur_column()]])))) |>
  filter(Tier %in% c("1","5")) |>
  pivot_longer(-Tier, names_to="var", values_to="val")
p_radar <- ggplot(profiles, aes(x=var,y=val,group=Tier,color=Tier,fill=Tier)) +
  geom_polygon(alpha=0.1,linewidth=1.2) + geom_point(size=2) +
  coord_polar() + scale_color_manual(values=c("1"="#1565C0","5"="#E53935")) +
  scale_fill_manual(values=c("1"="#1565C0","5"="#E53935")) +
  theme_minimal() + labs(title="Radar: Tier 1 vs Tier 5 Profiles")
ggsave("output/radar.png",p_radar,width=6,height=6,dpi=300)

# 4. INTERACTIVE PARALLEL (plotly — uncomment to run)
# library(plotly)
# plot_ly(ecar, type="parcoords",
#   line=list(color=~as.numeric(Tier), colorscale="Viridis"),
#   dimensions=list(
#     list(label="FICO",values=~FICO), list(label="Rate",values=~Rate),
#     list(label="Amount",values=~Amount), list(label="Term",values=~Term),
#     list(label="Spread",values=~Spread)))

cat("\n── All W05-M02 R plots saved ──\n")
