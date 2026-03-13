# ============================================================
# Workshop 3 — Module 7: Uncertainty — Error Bars, Confidence & Gradient
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"),!is.na(Rating))
top6 <- apps |> count(Category,sort=TRUE) |> slice_max(n,n=6) |> pull(Category)
df6 <- apps |> filter(Category %in% top6)

# 1. POINTRANGE — mean + 95% CI
p_point <- ggplot(df6, aes(x=fct_reorder(Category,Rating,.fun=mean),y=Rating)) +
  stat_summary(fun.data=mean_cl_normal,geom="pointrange",color="#1565C0",size=0.5,linewidth=1) +
  coord_flip() + geom_hline(yintercept=mean(df6$Rating),linetype="dashed",color="grey50") +
  theme_minimal() + labs(title="Pointrange: Mean ± 95% CI",x=NULL,y="Rating")
ggsave("output/pointrange.png",p_point,width=7,height=5,dpi=300)

# 2. ERROR BAR — mean + SE
p_errbar <- ggplot(df6, aes(x=fct_reorder(Category,Rating,.fun=mean),y=Rating)) +
  stat_summary(fun=mean,geom="point",size=3,color="#1565C0") +
  stat_summary(fun.data=mean_se,geom="errorbar",width=0.2,color="#E53935",linewidth=1) +
  coord_flip() + theme_minimal() + labs(title="Error Bar: Mean ± 1 SE",x=NULL,y="Rating")
ggsave("output/errorbar.png",p_errbar,width=7,height=5,dpi=300)

# 3. RIBBON — time series with CI
set.seed(33)
ts <- tibble(year=2015:2024,revenue=c(120,135,128,142,155,170,145,180,195,220),
             se=runif(10,8,18))
p_ribbon <- ggplot(ts, aes(x=year,y=revenue)) +
  geom_ribbon(aes(ymin=revenue-1.96*se,ymax=revenue+1.96*se),fill="#1565C0",alpha=0.12) +
  geom_ribbon(aes(ymin=revenue-se,ymax=revenue+se),fill="#1565C0",alpha=0.25) +
  geom_line(color="#1565C0",linewidth=1.2) + geom_point(color="#1565C0",size=2) +
  theme_minimal() + labs(title="Ribbon: Trend with 95% CI + SE bands",x="Year",y="Revenue ($M)")
ggsave("output/ribbon.png",p_ribbon,width=7,height=5,dpi=300)

# 4. SMOOTH WITH CI — automatic
p_smooth <- ggplot(df6 |> filter(as.numeric(Reviews)>0),
    aes(x=as.numeric(Reviews),y=Rating)) +
  geom_point(alpha=0.1,size=0.3) +
  geom_smooth(method="lm",se=TRUE,color="#E53935",fill="#E53935",alpha=0.15) +
  scale_x_log10(labels=scales::comma) + theme_minimal() +
  labs(title="geom_smooth(se=TRUE): Auto CI band",x="Reviews (log)",y="Rating")
ggsave("output/smooth_ci.png",p_smooth,width=7,height=5,dpi=300)

# 5. ALL TOGETHER
p_all <- (p_point | p_errbar) / (p_ribbon | p_smooth) +
  plot_annotation(title="Four Uncertainty Visualization Patterns")
ggsave("output/uncertainty_all.png",p_all,width=12,height=9,dpi=300)
cat("\n── All W03-M07 R plots saved ──\n")
