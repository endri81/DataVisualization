# ============================================================
# Workshop 3 — Module 3: Comparisons — Bar, Lollipop, Cleveland Dot
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> filter(Type %in% c("Free","Paid"), !is.na(Rating))
top8 <- apps |> count(Category, sort=TRUE) |> slice_max(n,n=8) |> mutate(Category=fct_reorder(Category,n),hl=n==max(n))

# 1. SORTED HORIZONTAL BAR
p_bar <- ggplot(top8, aes(x=Category,y=n,fill=hl)) +
  geom_col(width=0.5,show.legend=FALSE) +
  geom_text(aes(label=scales::comma(n)),hjust=-0.15,size=3,fontface="bold") +
  scale_fill_manual(values=c("TRUE"="#1565C0","FALSE"="#BBBBBB")) +
  coord_flip() + theme_minimal() + theme(panel.grid.major.y=element_blank()) +
  labs(title="(a) Horizontal Bar",x=NULL,y=NULL)

# 2. LOLLIPOP
p_lollipop <- ggplot(top8, aes(x=Category,y=n)) +
  geom_segment(aes(xend=Category,y=0,yend=n),color="grey75") +
  geom_point(aes(color=hl),size=3,show.legend=FALSE) +
  scale_color_manual(values=c("TRUE"="#1565C0","FALSE"="#BBBBBB")) +
  geom_text(aes(label=scales::comma(n)),hjust=-0.3,size=3,fontface="bold") +
  coord_flip() + theme_minimal() + theme(panel.grid.major.y=element_blank()) +
  labs(title="(b) Lollipop",x=NULL,y=NULL)

# 3. CLEVELAND DOT
p_dot <- ggplot(top8, aes(x=n,y=Category)) +
  geom_point(aes(color=hl),size=3,show.legend=FALSE) +
  scale_color_manual(values=c("TRUE"="#1565C0","FALSE"="#BBBBBB")) +
  geom_text(aes(label=scales::comma(n)),hjust=-0.3,size=3,fontface="bold") +
  geom_vline(xintercept=mean(top8$n),linetype="dashed",color="grey50") +
  theme_minimal() + labs(title="(c) Cleveland Dot",x="Count",y=NULL)

# 4. GROUPED BAR
apps_cr <- apps |> filter(`Content Rating` %in% c("Everyone","Teen","Mature 17+","Everyone 10+"))
p_grouped <- ggplot(apps_cr, aes(x=`Content Rating`,fill=Type)) +
  geom_bar(position=position_dodge(width=0.8),width=0.7) +
  scale_fill_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal() + labs(title="(d) Grouped Bar")

# 5. DUMBBELL
df_db <- tibble(cat=c("GAME","FAMILY","TOOLS","BUSINESS","MEDICAL"),
  v2020=c(500,800,400,200,150),v2024=c(959,1832,843,420,395)) |> mutate(cat=fct_reorder(cat,v2024))
p_dumb <- ggplot(df_db, aes(y=cat)) +
  geom_segment(aes(x=v2020,xend=v2024,yend=cat),color="grey80",linewidth=1.5) +
  geom_point(aes(x=v2020),size=3,color="#1565C0") +
  geom_point(aes(x=v2024),size=3,color="#E53935") +
  geom_text(aes(x=v2024,label=paste0("+",v2024-v2020)),hjust=-0.3,size=3,color="#E53935",fontface="bold") +
  theme_minimal() + labs(title="(e) Dumbbell: 2020→2024",x="Count",y=NULL)

p_all <- (p_bar | p_lollipop | p_dot) / (p_grouped | p_dumb) +
  plot_annotation(title="Five Comparison Chart Types")
ggsave("output/comparison_charts.png",p_all,width=14,height=9,dpi=300)
cat("\n── All W03-M03 R plots saved ──\n")
