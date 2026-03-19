# ============================================================
# Workshop 4 — Module 8: EDA Case Study — e-Car Loan Pricing
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

ecar <- read_csv("ecar.csv") |>
  rename(CarType = `Car  Type`, CompRate = `Competition rate`,
         PrevRate = `Previous Rate`, CoF = `Cost of Funds`,
         PartnerBin = `Partner Bin`, ApproveDate = `Approve Date`) |>
  mutate(PrevRate = as.numeric(PrevRate), ApproveDate = mdy(ApproveDate),
         Year = year(ApproveDate), Spread = Rate - CoF,
         Tier = factor(Tier, levels=1:5, ordered=TRUE),
         is_new = is.na(PrevRate), CarType = str_trim(CarType))
cat("Rows:", nrow(ecar), "| Cols:", ncol(ecar), "\n")

# ── DASHBOARD ──
p_fico <- ggplot(ecar |> sample_n(20000), aes(x=FICO)) +
  geom_histogram(bins=50,fill="#1565C0",color="white") +
  geom_vline(xintercept=median(ecar$FICO),color="#E53935",linetype="dashed") +
  theme_minimal(base_size=8) + labs(title="(a) FICO")

p_rate <- ggplot(ecar |> sample_n(20000), aes(x=Rate)) +
  geom_histogram(bins=50,fill="#2E7D32",color="white") +
  theme_minimal(base_size=8) + labs(title="(b) Rate")

p_scatter <- ecar |> sample_n(5000) |>
  ggplot(aes(x=FICO,y=Rate)) + geom_point(alpha=0.05,size=0.3,color="#1565C0") +
  geom_smooth(method="lm",color="#E53935",se=FALSE) +
  theme_minimal(base_size=8) + labs(title="(c) FICO vs Rate")

p_tier <- ggplot(ecar |> sample_n(20000), aes(x=Tier,y=Rate,fill=Tier)) +
  geom_boxplot(width=0.5,outlier.size=0.3,outlier.alpha=0.1) +
  scale_fill_brewer(palette="Set2") + theme_minimal(base_size=8) +
  theme(legend.position="none") + labs(title="(d) Rate by Tier")

p_spread <- ecar |> group_by(Year) |>
  summarise(m=mean(Spread),se=sd(Spread)/sqrt(n()),.groups="drop") |>
  filter(Year>=2002,Year<=2012) |>
  ggplot(aes(x=Year,y=m)) +
  geom_ribbon(aes(ymin=m-1.96*se,ymax=m+1.96*se),fill="#1565C0",alpha=0.15) +
  geom_line(color="#1565C0",linewidth=1) + geom_point(color="#1565C0",size=2) +
  theme_minimal(base_size=8) + labs(title="(e) Spread Over Time",y="Spread (pp)")

p_car <- ggplot(ecar |> sample_n(20000), aes(x=CarType,y=Rate,fill=CarType)) +
  geom_violin(alpha=0.3) + geom_boxplot(width=0.1,outlier.shape=NA,fill="white") +
  scale_fill_manual(values=c(N="#1565C0",U="#E53935")) +
  theme_minimal(base_size=8) + theme(legend.position="none") + labs(title="(f) New vs Used")

dashboard <- (p_fico|p_rate|p_scatter) / (p_tier|p_spread|p_car) +
  plot_annotation(title="e-Car Loan: EDA Dashboard (208K applications)",
    caption="Source: e-Car Dataset | UNYT", tag_levels="a") &
  theme_minimal(base_size=8)
ggsave("output/W04_M08_dashboard.pdf",dashboard,width=14,height=9)
ggsave("output/W04_M08_dashboard.png",dashboard,width=14,height=9,dpi=300)

# ── STRUCTURAL MNAR ──
p_shadow <- ecar |> mutate(PrevAvail=ifelse(is_new,"No Prev Rate","Has Prev Rate")) |>
  ggplot(aes(x=FICO,fill=PrevAvail)) +
  geom_histogram(bins=40,position="identity",alpha=0.5) +
  scale_fill_manual(values=c("Has Prev Rate"="#1565C0","No Prev Rate"="#E53935")) +
  theme_minimal() + labs(title="FICO by Previous Rate Availability (MNAR)")
ggsave("output/W04_M08_shadow.png",p_shadow,width=7,height=4,dpi=300)

# ── KEY STATS ──
cat("Spearman(FICO,Rate):", round(cor(ecar$FICO,ecar$Rate,method="spearman"),3), "\n")
cat("Previous Rate missing:", round(mean(ecar$is_new)*100,1), "%\n")
cat("Median Rate (New):", round(median(ecar$Rate[ecar$CarType=="N"]),2), "%\n")
cat("Median Rate (Used):", round(median(ecar$Rate[ecar$CarType=="U"]),2), "%\n")
cat("\n── All W04-M08 R outputs saved ──\n")
