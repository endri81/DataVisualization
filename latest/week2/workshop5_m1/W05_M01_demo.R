# ============================================================
# Workshop 5 — Module 1: High-Dimensional Data
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

# Simulated e-Car-like data for demo
set.seed(42); n <- 2000
ecar <- tibble(
  FICO = rnorm(n, 700, 50) |> pmax(500) |> pmin(850),
  Rate = 12 - 0.01*FICO + rnorm(n, 0, 1),
  Amount = runif(n, 5000, 50000),
  Tier = cut(FICO, breaks=c(0,620,680,720,760,900), labels=1:5),
  CarType = sample(c("New","Used"), n, replace=TRUE, prob=c(0.6,0.4)))

# 1. MULTI-ENCODED SCATTER — 5 variables
p_multi <- ggplot(ecar, aes(x=FICO, y=Rate, color=as.numeric(Tier), size=Amount, shape=CarType)) +
  geom_point(alpha=0.4) +
  scale_color_viridis_c(name="Tier") +
  scale_size(range=c(1,6), name="Amount ($)") +
  scale_shape_manual(values=c(New=16, Used=17)) +
  theme_minimal() + labs(title="5 Variables on 1 Scatter", x="FICO", y="Rate (%)")
ggsave("output/multi_scatter.png", p_multi, width=8, height=6, dpi=300)

# 2. HEXBIN — for large n
p_hex <- ggplot(ecar, aes(x=FICO, y=Rate)) +
  geom_hex(bins=30) + scale_fill_viridis_c() +
  theme_minimal() + labs(title="Hexbin: Aggregated Scatter for Large n")
ggsave("output/hexbin.png", p_hex, width=7, height=5, dpi=300)

# 3. MARGINAL DISTRIBUTIONS
library(ggExtra)
p_base <- ggplot(ecar, aes(x=FICO, y=Rate, color=CarType)) +
  geom_point(alpha=0.2, size=0.5) +
  scale_color_manual(values=c(New="#1565C0", Used="#E53935")) +
  theme_minimal(base_size=9) + theme(legend.position="bottom")
p_marg <- ggMarginal(p_base, type="histogram", groupColour=TRUE, groupFill=TRUE)
ggsave("output/marginal.png", p_marg, width=7, height=6, dpi=300)

# 4. OVERLOAD DEMO — too many encodings
p_over <- ecar |> mutate(PriceBin=cut(Amount,5)) |>
  ggplot(aes(x=FICO,y=Rate,color=PriceBin,size=Amount,shape=CarType)) +
  geom_point(alpha=0.3) + theme_minimal(base_size=8) +
  labs(title="Overloaded: 5 colour bins × 2 shapes × continuous size\n(hard to read)")
ggsave("output/overload.png", p_over, width=8, height=6, dpi=300)

cat("\n── All W05-M01 R plots saved ──\n")
