# ============================================================
# Workshop 3 — Module 10: Lab — Chart Selection Decision Framework
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output",showWarnings=FALSE)
netflix <- read_csv("netflix.csv")

# (a) SORTED BAR — top genres
genres <- netflix |> separate_rows(listed_in, sep=", ") |>
  count(listed_in, sort=TRUE) |> slice_max(n, n=8) |>
  mutate(listed_in=fct_reorder(listed_in, n), hl=n==max(n))
p_a <- ggplot(genres, aes(x=listed_in, y=n, fill=hl)) +
  geom_col(width=0.5, show.legend=FALSE) +
  geom_text(aes(label=scales::comma(n)), hjust=-0.15, size=3, fontface="bold") +
  scale_fill_manual(values=c("TRUE"="#E53935","FALSE"="#BBBBBB")) +
  coord_flip() + theme_minimal() + theme(panel.grid.major.y=element_blank()) +
  labs(title="(a) Top Genres", x=NULL, y=NULL)

# (b) HISTOGRAM — movie duration
p_b <- netflix |> filter(type=="Movie") |>
  mutate(dur=parse_number(duration)) |>
  ggplot(aes(x=dur)) +
  geom_histogram(bins=35, fill="#1565C0", color="white") +
  geom_vline(xintercept=100, linetype="dashed", color="#E53935") +
  theme_minimal() + labs(title="(b) Movie Duration (min)", x="Duration", y="Count")

# (c) STACKED BAR — rating x type
p_c <- netflix |> filter(rating %in% c("TV-MA","TV-14","TV-PG","R","PG-13")) |>
  ggplot(aes(x=rating, fill=type)) +
  geom_bar(position="stack") +
  scale_fill_manual(values=c(Movie="#1565C0","TV Show"="#E53935")) +
  theme_minimal() + theme(axis.text.x=element_text(angle=30,hjust=1,size=7)) +
  labs(title="(c) Rating × Type", fill="Type")

# (d) LINE — releases per year
p_d <- netflix |> filter(release_year>=2010) |>
  count(release_year, type) |>
  ggplot(aes(x=release_year, y=n, color=type)) +
  geom_line(linewidth=1.2) + geom_point(size=2) +
  scale_color_manual(values=c(Movie="#1565C0","TV Show"="#E53935")) +
  theme_minimal() + theme(legend.position="bottom") +
  labs(title="(e) Releases per Year", x="Year", y="Count", color=NULL)

# (e) BOXPLOT — movie duration by rating
p_e <- netflix |> filter(type=="Movie", rating %in% c("TV-MA","TV-14","R","PG-13","TV-PG")) |>
  mutate(dur=parse_number(duration)) |>
  ggplot(aes(x=fct_reorder(rating,dur,.fun=median), y=dur, fill=rating)) +
  geom_boxplot(width=0.5, outlier.alpha=0.1) +
  scale_fill_brewer(palette="Set2") +
  coord_flip() + theme_minimal() + theme(legend.position="none") +
  labs(title="(g) Duration by Rating", x=NULL, y="Minutes")

# (f) LOLLIPOP — top countries
countries <- netflix |> separate_rows(country, sep=", ") |>
  count(country, sort=TRUE) |> slice_max(n, n=8) |>
  mutate(country=fct_reorder(country, n), hl=n==max(n))
p_f <- ggplot(countries, aes(x=country, y=n)) +
  geom_segment(aes(xend=country, y=0, yend=n), color="grey75") +
  geom_point(aes(color=hl), size=3, show.legend=FALSE) +
  scale_color_manual(values=c("TRUE"="#1565C0","FALSE"="#BBBBBB")) +
  geom_text(aes(label=scales::comma(n)), hjust=-0.3, size=3, fontface="bold") +
  coord_flip() + theme_minimal() + theme(panel.grid.major.y=element_blank()) +
  labs(title="(h) Top Countries", x=NULL, y=NULL)

# COMPOSE DASHBOARD
dashboard <- (p_a | p_b | p_c) / (p_d | p_e | p_f) +
  plot_annotation(
    title="Netflix Dataset: Visual Report — 6 Chart Types",
    subtitle="Workshop 3 Lab — Chart Selection Decision Framework Applied",
    caption="Source: Netflix Dataset (Kaggle) | UNYT Data Visualization Course",
    tag_levels="a") &
  theme_minimal(base_size=9)

ggsave("output/W03_M10_netflix.pdf", dashboard, width=14, height=9, device=cairo_pdf)
ggsave("output/W03_M10_netflix.png", dashboard, width=14, height=9, dpi=300)
cat("\n── Workshop 3 Lab Complete (R) ──\n")
