# analysis_script.R
# RM-ANOVA, Linear Mixed Models (lme4), and correlation plots
# Install packages if needed:
# install.packages(c("lme4", "ggplot2", "afex", "dplyr", "tidyr"))

library(lme4)
library(ggplot2)
library(afex)
library(dplyr)
library(tidyr)

# ------------------------------------------------------------------
# 0. Example data (replace with: dat <- read.csv("your_data.csv"))
set.seed(42)
n_sub  <- 30
conds  <- c("A", "B", "C")
times  <- c("T1", "T2", "T3")
dat <- expand.grid(subject = factor(1:n_sub),
                   condition = factor(conds),
                   time = factor(times),
                   stringsAsFactors = TRUE)
mu_vec <- 10 + 2 * as.numeric(dat$condition) + as.numeric(dat$time)
dat$y  <- rnorm(nrow(dat), mean = mu_vec, sd = 2)
# ------------------------------------------------------------------

# 1. Repeated-measures ANOVA
rm_anova <- aov_ez(id = "subject", dv = "y",
                   within = c("condition", "time"), data = dat)
print(rm_anova)
print(summary(rm_anova))

# 2. Linear Mixed Models (lme4)
# Random-intercept model
m0 <- lmer(y ~ condition * time + (1 | subject), data = dat, REML = TRUE)
# Random-slope model
m1 <- lmer(y ~ condition * time + (1 + time | subject), data = dat, REML = TRUE)
summary(m0)
anova(m0, m1)   # model comparison

# Random effects / diagnostics
print(VarCorr(m1), comp = "Variance")
plot(fitted(m1), resid(m1),
     main = "Residuals vs Fitted (m1)",
     xlab = "Fitted", ylab = "Residual"); abline(h = 0, col = "red")

# 3. Correlation plots
# (a) subject-level means per condition -> correlation heatmap
subj_means <- dat %>%
  group_by(subject, condition) %>%
  summarise(mean_y = mean(y), .groups = "drop") %>%
  pivot_wider(names_from = condition, values_from = mean_y)

cor_mat <- cor(subj_means[, conds])
print(cor_mat)

corr_df <- expand.grid(Var1 = conds, Var2 = conds, stringsAsFactors = TRUE)
corr_df$value <- as.vector(cor_mat)

p1 <- ggplot(corr_df, aes(Var1, Var2, fill = value)) +
  geom_tile() +
  geom_text(aes(label = sprintf("%.2f", value))) +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red",
                       limits = c(-1, 1)) +
  labs(title = "Correlation between conditions (subject means)",
       x = NULL, y = NULL, fill = "r") +
  theme_minimal()
ggsave("correlation_heatmap.png", p1, width = 6, height = 5, dpi = 150)

# (b) pairwise scatter plot with regression line
p2 <- ggplot(subj_means, aes(A, B)) +
  geom_point() +
  geom_smooth(method = "lm") +
  labs(title = sprintf("A vs B (r = %.2f)", cor(subj_means$A, subj_means$B)),
       x = "Condition A (subject mean)", y = "Condition B (subject mean)") +
  theme_minimal()
ggsave("scatter_A_B.png", p2, width = 5, height = 4, dpi = 150)

cat("Analysis complete.\n")
