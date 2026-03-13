# ============================================================
# Workshop 3 — Module 6: Rankings — Slope, Bump & Waterfall
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

cats <- c("FAMILY","GAME","TOOLS","PHOTOGRAPHY","PRODUCTIVITY","BUSINESS")
v2020 <- c(800,500,400,200,180,350); v2024 <- c(1832,959,843,376,374,420)
df <- tibble(category=cats,v2020=v2020,v2024=v2024)

# 1. SLOPEGRAPH
df_long <- df |> pivot_longer(c(v2020,v2024),names_to="year",values_to="value") |>
  mutate(year=parse_number(year), highlight=category=="FAMILY")

p_slope <- ggplot(df_long, aes(x=year,y=value,group=category,color=highlight,alpha=highlight)) +
  geom_line(linewidth=1.2) + geom_point(size=3) +
  scale_color_manual(values=c("TRUE"="#E53935","FALSE"="#CCCCCC")) +
  scale_alpha_manual(values=c("TRUE"=1,"FALSE"=0.4)) +
  geom_text(data=df_long |> filter(year==2020),
    aes(label=paste(category,scales::comma(value))),hjust=1.1,size=3) +
  geom_text(data=df_long |> filter(year==2024),
    aes(label=paste(category,scales::comma(value))),hjust=-0.1,size=3) +
  theme_void() + theme(legend.position="none") +
  labs(title="Slopegraph: FAMILY Surged to #1")
ggsave("output/slopegraph.png",p_slope,width=7,height=5,dpi=300)

# 2. BUMP CHART (manual — ggbump requires install)
years <- 2019:2024
ranks <- tibble(
  category=rep(c("FAMILY","GAME","TOOLS","BUSINESS"),each=6),
  year=rep(years,4),
  rank=c(2,2,1,1,1,1, 1,1,2,2,2,2, 3,3,3,3,3,3, 5,4,4,5,4,4))
ranks <- ranks |> mutate(highlight=category %in% c("FAMILY","GAME"))

p_bump <- ggplot(ranks, aes(x=year,y=rank,group=category,color=category,alpha=highlight)) +
  geom_line(aes(linewidth=highlight)) + geom_point(aes(size=highlight)) +
  scale_linewidth_manual(values=c("TRUE"=2,"FALSE"=0.8)) +
  scale_size_manual(values=c("TRUE"=3,"FALSE"=1.5)) +
  scale_alpha_manual(values=c("TRUE"=1,"FALSE"=0.3)) +
  scale_y_reverse(breaks=1:5,labels=paste0("#",1:5)) +
  scale_color_brewer(palette="Set2") +
  geom_text(data=ranks |> filter(year==2024),
    aes(label=category),hjust=-0.2,size=3,fontface="bold") +
  theme_minimal() + theme(legend.position="none",panel.grid.minor=element_blank()) +
  labs(title="Bump: FAMILY Overtook GAME in 2021",x="Year",y="Rank") +
  xlim(2018.5,2025.5)
ggsave("output/bump.png",p_bump,width=8,height=5,dpi=300)

# 3. WATERFALL (manual)
wf <- tibble(
  item=c("Start","Product A","Product B","Product C","Returns","Discounts","End"),
  value=c(800,450,280,190,-85,-35,0),
  type=c("total","pos","pos","pos","neg","neg","total")) |>
  mutate(end=cumsum(value), start=lag(end,default=0),
    item=fct_inorder(item))

p_wf <- ggplot(wf, aes(x=item)) +
  geom_rect(aes(xmin=as.numeric(item)-0.25, xmax=as.numeric(item)+0.25,
    ymin=pmin(start,end), ymax=pmax(start,end), fill=type)) +
  scale_fill_manual(values=c(total="#1565C0",pos="#2E7D32",neg="#E53935")) +
  geom_text(aes(y=end,label=ifelse(type=="total",paste0("$",scales::comma(end)),
    paste0(ifelse(value>0,"+",""),"$",scales::comma(value)))),
    vjust=ifelse(wf$value>=0,-0.5,1.5),size=3,fontface="bold") +
  theme_minimal() + theme(legend.position="none",axis.text.x=element_text(angle=20,hjust=1)) +
  labs(title="Waterfall: Revenue Breakdown",y="Revenue ($)",x=NULL)
ggsave("output/waterfall.png",p_wf,width=8,height=5,dpi=300)

ggsave("output/rankings_all.png",(p_slope | p_bump) / p_wf,width=14,height=9,dpi=300)
cat("\n── All W03-M06 R plots saved ──\n")
