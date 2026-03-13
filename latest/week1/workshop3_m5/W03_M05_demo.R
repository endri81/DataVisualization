# ============================================================
# Workshop 3 — Module 5: Proportions — Pie, Donut, Treemap & Waffle
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"),!is.na(Rating))
top6 <- apps |> count(Category,sort=TRUE) |> slice_max(n,n=6)

# 1. PIE (to show why it fails)
p_pie <- top6 |>
  ggplot(aes(x="",y=n,fill=Category)) +
  geom_col(width=1,color="white",linewidth=1) +
  coord_polar(theta="y") +
  scale_fill_brewer(palette="Set2") +
  theme_void() + labs(title="Pie: Hard to Compare 6 Slices")
ggsave("output/pie_fail.png",p_pie,width=5,height=5,dpi=300)

# 2. DONUT (KPI)
df_kpi <- tibble(cat=c("Free","Paid"),n=c(sum(apps$Type=="Free"),sum(apps$Type=="Paid")))
p_donut <- ggplot(df_kpi,aes(x=2,y=n,fill=cat)) +
  geom_col(width=1,color="white",linewidth=2) +
  coord_polar(theta="y") + xlim(0.5,2.5) +
  scale_fill_manual(values=c(Free="#1565C0",Paid="#EEEEEE")) +
  annotate("text",x=0.5,y=0,label=paste0(round(df_kpi$n[1]/sum(df_kpi$n)*100),"%"),
    size=12,fontface="bold",color="#1565C0") +
  annotate("text",x=0.5,y=sum(df_kpi$n)*0.05,label="Free Apps",size=4,color="#555") +
  theme_void() + theme(legend.position="none") +
  labs(title="Donut: Single KPI")
ggsave("output/donut_kpi.png",p_donut,width=5,height=5,dpi=300)

# 3. 100% STACKED BAR (the better alternative)
p_stacked <- top6 |>
  mutate(pct=n/sum(n)) |>
  ggplot(aes(x="Apps",y=pct,fill=fct_reorder(Category,n))) +
  geom_col(width=0.6,color="white",linewidth=1.5) +
  geom_text(aes(label=paste0(round(pct*100),"%")),
    position=position_stack(vjust=0.5),size=3,fontface="bold",color="white") +
  scale_fill_brewer(palette="Set2") +
  scale_y_continuous(labels=scales::percent) +
  coord_flip() + theme_minimal() +
  labs(title="100% Stacked Bar: Better Than Pie",fill="Category",y=NULL,x=NULL)
ggsave("output/stacked_bar.png",p_stacked,width=8,height=3,dpi=300)

# 4. TREEMAP
# library(treemapify)
# p_tree <- ggplot(top6, aes(area=n, fill=Category,
#     label=paste(Category,scales::comma(n),sep="\n"))) +
#   geom_treemap(color="white",size=2) +
#   geom_treemap_text(fontface="bold",color="white",place="centre") +
#   scale_fill_brewer(palette="Set2") + theme(legend.position="none") +
#   labs(title="Treemap: Area = Count")
# ggsave("output/treemap.png",p_tree,width=7,height=5,dpi=300)

# 5. WAFFLE
# library(waffle)
# waffle(c(FAMILY=38,GAME=20,TOOLS=18,PHOTO=8,PROD=8,BUS=8),
#   rows=10,colors=c("#1565C0","#E53935","#2E7D32","#E65100","#7B1FA2","#00695C"),
#   title="App Categories (%)")

cat("\n── All W03-M05 R plots saved ──\n")
