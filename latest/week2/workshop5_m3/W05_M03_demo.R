# ============================================================
# Workshop 5 — Module 3: Dimensionality Reduction Visualization
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(ggfortify); dir.create("output",showWarnings=FALSE)
set.seed(42)
# Simulated 6D 3-cluster data
c1 <- MASS::mvrnorm(150, mu=c(5,5,2,8,3,6), Sigma=diag(6)*0.8)
c2 <- MASS::mvrnorm(150, mu=c(2,8,5,3,7,2), Sigma=diag(6)*0.8)
c3 <- MASS::mvrnorm(100, mu=c(8,2,7,5,5,4), Sigma=diag(6)*0.8)
X <- rbind(c1,c2,c3); colnames(X) <- paste0("V",1:6)
labels <- factor(c(rep(1,150),rep(2,150),rep(3,100)))
df <- as_tibble(X) |> mutate(Cluster=labels)

# 1. PCA BIPLOT
pca <- prcomp(df |> select(V1:V6), scale.=TRUE)
p_biplot <- autoplot(pca, data=df, colour="Cluster", loadings=TRUE, loadings.label=TRUE,
  loadings.colour="#E65100", loadings.label.colour="#E65100", alpha=0.5, size=1) +
  scale_color_manual(values=c("1"="#1565C0","2"="#E53935","3"="#2E7D32")) +
  theme_minimal() + labs(title="PCA Biplot: Scores + Loadings")
ggsave("output/pca_biplot.png",p_biplot,width=7,height=6,dpi=300)

# 2. SCREE PLOT
var_exp <- summary(pca)$importance[2,]*100; cum_var <- cumsum(var_exp)
p_scree <- tibble(PC=1:6,var=var_exp,cum=cum_var) |>
  ggplot(aes(x=PC)) +
  geom_col(aes(y=var),fill="#1565C0",width=0.5,alpha=0.7) +
  geom_line(aes(y=cum),color="#E53935",linewidth=1) +
  geom_point(aes(y=cum),color="#E53935",size=3) +
  geom_hline(yintercept=80,linetype="dashed",color="#888") +
  theme_minimal() + labs(title="Scree Plot",y="Variance Explained (%)")
ggsave("output/scree.png",p_scree,width=6,height=4,dpi=300)

# 3. t-SNE
library(Rtsne)
tsne <- Rtsne(scale(X), dims=2, perplexity=30, check_duplicates=FALSE)
p_tsne <- tibble(x=tsne$Y[,1],y=tsne$Y[,2],Cluster=labels) |>
  ggplot(aes(x,y,color=Cluster)) + geom_point(alpha=0.5,size=1) +
  scale_color_manual(values=c("1"="#1565C0","2"="#E53935","3"="#2E7D32")) +
  theme_minimal() + labs(title="t-SNE (perplexity=30)")
ggsave("output/tsne.png",p_tsne,width=6,height=5,dpi=300)

# 4. PERPLEXITY COMPARISON
library(patchwork)
perps <- c(5,15,30,100)
tsne_plots <- map(perps, ~{
  t <- Rtsne(scale(X),dims=2,perplexity=.x,check_duplicates=FALSE)
  tibble(x=t$Y[,1],y=t$Y[,2],Cluster=labels) |>
    ggplot(aes(x,y,color=Cluster)) + geom_point(alpha=0.5,size=0.5) +
    scale_color_manual(values=c("1"="#1565C0","2"="#E53935","3"="#2E7D32")) +
    theme_minimal(base_size=7) + theme(legend.position="none") +
    labs(title=paste0("perp=",.x))
})
ggsave("output/tsne_perplexity.png",wrap_plots(tsne_plots,nrow=1),width=14,height=3.5,dpi=300)

cat("\n── All W05-M03 R plots saved ──\n")
