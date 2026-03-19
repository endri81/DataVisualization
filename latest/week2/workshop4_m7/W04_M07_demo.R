# ============================================================
# Workshop 4 — Module 7: EDA Case Study — Google Play Store
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

# ── PHASE 1: CLEAN ──────────────────────────────────────
apps_clean <- read_csv("googleplaystore.csv") |>
  distinct(App, .keep_all = TRUE) |>
  mutate(Reviews = as.numeric(Reviews),
    Installs = str_remove_all(Installs, "[+,]") |> as.numeric(),
    Price = str_remove(Price, "\\$") |> as.numeric(),
    log_reviews = log10(pmax(Reviews, 1)),
    log_installs = log10(pmax(Installs, 1))) |>
  drop_na(Rating) |>
  filter(Type %in% c("Free","Paid"), Rating >= 1, Rating <= 5) |>
  mutate(Category = fct_lump_n(Category, 8) |> fct_infreq())

cat("Cleaned:", nrow(apps_clean), "rows\n")
cat("Free:", sum(apps_clean$Type=="Free"), "| Paid:", sum(apps_clean$Type=="Paid"), "\n")

# ── PHASE 2: DASHBOARD ──────────────────────────────────
p_hist <- ggplot(apps_clean, aes(x=Rating)) + geom_histogram(bins=40,fill="#1565C0",color="white") +
  geom_vline(xintercept=mean(apps_clean$Rating),color="#E53935",linetype="dashed") +
  theme_minimal(base_size=8) + labs(title="(a) Rating Distribution")

p_violin <- ggplot(apps_clean, aes(x=Type,y=Rating,fill=Type)) +
  geom_violin(alpha=0.3) + geom_boxplot(width=0.1,outlier.shape=NA,fill="white") +
  scale_fill_manual(values=c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal(base_size=8) + theme(legend.position="none") + labs(title="(b) Rating by Type")

p_bar <- apps_clean |> count(Category) |> mutate(Category=fct_reorder(Category,n)) |>
  ggplot(aes(x=Category,y=n)) + geom_col(fill="#1565C0",width=0.5) +
  coord_flip() + theme_minimal(base_size=8) + labs(title="(c) Top Categories")

p_scatter <- apps_clean |> filter(Reviews>0) |> slice_sample(n=2000) |>
  ggplot(aes(x=log_reviews,y=Rating)) + geom_point(alpha=0.1,size=0.3,color="#1565C0") +
  geom_smooth(method="lm",color="#E53935",se=FALSE) +
  theme_minimal(base_size=8) + labs(title="(d) log(Reviews) vs Rating")

p_point <- apps_clean |> filter(Category!="Other") |>
  group_by(Category) |> summarise(m=mean(Rating),se=sd(Rating)/sqrt(n()),.groups="drop") |>
  mutate(Category=fct_reorder(Category,m)) |>
  ggplot(aes(x=Category,y=m)) +
  geom_pointrange(aes(ymin=m-1.96*se,ymax=m+1.96*se),color="#1565C0") +
  coord_flip() + theme_minimal(base_size=8) + labs(title="(e) Mean ± 95% CI")

p_qq <- ggplot(apps_clean, aes(sample=Rating)) + geom_qq(alpha=0.1,size=0.3) +
  geom_qq_line(color="#E53935") + theme_minimal(base_size=8) + labs(title="(f) Q-Q")

dashboard <- (p_hist | p_violin | p_bar) / (p_scatter | p_point | p_qq) +
  plot_annotation(title="Google Play Store: EDA Dashboard",
    subtitle=paste0(nrow(apps_clean)," apps | Cleaned & Wrangled"),
    caption="Source: Kaggle | UNYT", tag_levels="a") &
  theme_minimal(base_size=8)
ggsave("output/W04_M07_dashboard.pdf", dashboard, width=14, height=9)
ggsave("output/W04_M07_dashboard.png", dashboard, width=14, height=9, dpi=300)

# ── PHASE 3: KEY STATISTICS ──────────────────────────────
cat("\n── Key Statistics ──\n")
cat("Mean Rating:", round(mean(apps_clean$Rating),3), "\n")
cat("Median Rating:", round(median(apps_clean$Rating),3), "\n")
cat("Spearman (log_reviews, Rating):", round(cor(apps_clean$log_reviews, apps_clean$Rating, method="spearman"),3), "\n")
cat("Free %:", round(mean(apps_clean$Type=="Free")*100,1), "%\n")
cat("\n── All W04-M07 R outputs saved ──\n")
