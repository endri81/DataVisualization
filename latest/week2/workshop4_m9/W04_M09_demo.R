# ============================================================
# Workshop 4 — Module 9: EDA Automation & Reproducible Reports
# R Demo — UNYT Tirana
# ============================================================
library(tidyverse); dir.create("output",showWarnings=FALSE)
apps <- read_csv("googleplaystore.csv") |> mutate(Reviews=as.numeric(Reviews)) |> filter(!is.na(Rating))

# ── 1. SKIMR ──
library(skimr)
cat("── skimr output ──\n")
skim(apps |> select(Rating, Reviews, Type, Category))

# Grouped skim
apps |> group_by(Type) |> skim(Rating) |> print()

# ── 2. DataExplorer (generates HTML) ──
# library(DataExplorer)
# create_report(apps, output_file="output/auto_eda.html", y="Rating")
# Individual plots:
# plot_missing(apps)
# plot_histogram(apps)
# plot_correlation(apps |> select(where(is.numeric)))

# ── 3. PARAMETERISED REPORT DEMO ──
# Template: template.qmd (see slides)
# Render:
# quarto::quarto_render("template.qmd",
#   execute_params = list(dataset="googleplaystore.csv", target="Rating", group="Type"))
# Batch:
# datasets <- c("googleplaystore.csv","netflix.csv","ecar.csv")
# for (ds in datasets) {
#   quarto::quarto_render("template.qmd",
#     output_file=paste0("report_",tools::file_path_sans_ext(ds),".html"),
#     execute_params=list(dataset=ds))
# }

cat("\n── W04-M09 R demo complete ──\n")
