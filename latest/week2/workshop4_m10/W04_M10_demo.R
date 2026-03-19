# ============================================================
# Workshop 4 — Module 10: Lab — Full EDA on Netflix
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)

nf <- read_csv("netflix.csv") |>
  mutate(date_added=mdy(str_trim(date_added)), year_added=year(date_added),
    dur_min=ifelse(type=="Movie",parse_number(duration),NA),
    seasons=ifelse(type=="TV Show",parse_number(duration),NA),
    primary_genre=str_trim(str_extract(listed_in,"^[^,]+")),
    primary_country=str_trim(str_extract(country,"^[^,]+")))
cat("Rows:", nrow(nf), "| Movies:", sum(nf$type=="Movie"), "| TV:", sum(nf$type=="TV Show"), "\n")

# Missingness
cat("\n── Missing % ──\n"); print(round(colMeans(is.na(nf))*100,1))

# Genre explosion
nf_genres <- nf |> separate_rows(listed_in, sep=", ") |> mutate(genre=str_trim(listed_in))

# Dashboard
p_miss <- tibble(col=names(nf),pct=colMeans(is.na(nf))*100) |> filter(pct>0) |>
  mutate(col=fct_reorder(col,pct)) |>
  ggplot(aes(x=col,y=pct)) + geom_col(fill="#E53935",width=0.5) + coord_flip() +
  geom_hline(yintercept=5,linetype="dashed",color="#888") +
  theme_minimal(base_size=8) + labs(title="(a) Missing %",y="%")

p_line <- nf |> filter(release_year>=2000) |> count(release_year,type) |>
  ggplot(aes(x=release_year,y=n,color=type)) + geom_line(linewidth=1) + geom_point(size=1.5) +
  scale_color_manual(values=c(Movie="#1565C0","TV Show"="#E53935")) +
  theme_minimal(base_size=8) + theme(legend.position="bottom") + labs(title="(b) Releases/Year")

p_genre <- nf_genres |> count(genre,sort=TRUE) |> slice_max(n,n=10) |> mutate(genre=fct_reorder(genre,n)) |>
  ggplot(aes(x=genre,y=n)) + geom_col(fill="#E53935",width=0.5) + coord_flip() +
  theme_minimal(base_size=8) + labs(title="(c) Top Genres",x=NULL)

p_dur <- nf |> filter(type=="Movie",!is.na(dur_min)) |>
  ggplot(aes(x=dur_min)) + geom_histogram(bins=40,fill="#1565C0",color="white") +
  geom_vline(xintercept=mean(nf$dur_min,na.rm=T),color="#E53935",linetype="dashed") +
  theme_minimal(base_size=8) + labs(title="(d) Movie Duration")

p_rating <- nf |> count(rating,sort=TRUE) |> slice_max(n,n=8) |> mutate(rating=fct_reorder(rating,n)) |>
  ggplot(aes(x=rating,y=n)) + geom_col(fill="#7B1FA2",width=0.5) + coord_flip() +
  theme_minimal(base_size=8) + labs(title="(e) Content Rating",x=NULL)

p_country <- nf |> count(primary_country,sort=TRUE) |> drop_na() |> slice_max(n,n=8) |>
  mutate(primary_country=fct_reorder(primary_country,n)) |>
  ggplot(aes(x=primary_country,y=n)) +
  geom_segment(aes(xend=primary_country,y=0,yend=n),color="grey75") +
  geom_point(color="#1565C0",size=2) + coord_flip() +
  theme_minimal(base_size=8) + labs(title="(f) Top Countries",x=NULL)

dashboard <- (p_miss|p_line|p_genre) / (p_dur|p_rating|p_country) +
  plot_annotation(title=paste0("Netflix EDA: ",nrow(nf)," Titles"),
    caption="Source: Kaggle | UNYT", tag_levels="a") & theme_minimal(base_size=8)
ggsave("output/W04_M10_netflix.pdf",dashboard,width=14,height=9)
ggsave("output/W04_M10_netflix.png",dashboard,width=14,height=9,dpi=300)
cat("\n── W04-M10 Lab Complete (R) ──\n")
