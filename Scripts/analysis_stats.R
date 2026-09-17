# =====================================================================
# analysis_stats.R
# Statistical modeling for the longitudinal stylometric drift study
# Data: data_long.csv (ParticipantID, Profile, Wave, TimePoint,
#      Stylometry_Composite), data_wide.csv (T1, T2, T3, Drift)
# Requires: lme4, lmerTest, afex, emmeans, car, dplyr, tidyr
# =====================================================================

library(afex)      # convenience wrappers for ANOVA + mixed models
library(lme4)      # linear mixed-effects models
library(lmerTest)  # p-values (Satterthwaite) for lmer models
library(emmeans)   # estimated marginal means & pairwise contrasts
library(car)       # Mauchly's test, Greenhouse-Geisser correction
library(dplyr)
library(tidyr)

## --------------------------------------------------------------------
## 1. Load data
## --------------------------------------------------------------------
long_df <- read.csv("data_long.csv", stringsAsFactors = FALSE)
wide_df <- read.csv("data_wide.csv", stringsAsFactors = FALSE)

# Ensure correct factor ordering: TimePoint T1 < T2 < T3
long_df$TimePoint <- factor(long_df$TimePoint, levels = c("T1", "T2", "T3"))
long_df$Profile   <- factor(long_df$Profile)

## --------------------------------------------------------------------
## 2. Repeated-measures ANOVA (RM-ANOVA)
## --------------------------------------------------------------------
# 2x3 mixed design: Profile (between) x TimePoint (within, 3 levels)
# afex::aov_ez handles sphericity corrections (Greenhouse-Geisser)
anova_fit <- aov_ez(
  id       = "ParticipantID",
  dv       = "Stylometry_Composite",
  data     = long_df,
  between  = "Profile",
  within   = "TimePoint"
)
print(an          # includes GG correction where applicable

# Explicit sphericity sphericity diagnostics on the wide-format data
mlm_fit <- lm(cbind(T1, T2, T3) ~ Profile, data = wide_df)
mlm_res <- Anova(mlm_fit, idata = data.frame(Time = factor(c("T1","T2","T3"))),
                 idesign = ~Time, type = "III")
print(mlm_res)

## --------------------------------------------------------------------
## 3. Linear Mixed Model (LMM) -- the modern equivalent
## --------------------------------------------------------------------
# Random intercept per participant; Profile as a fixed effect.
# By-participant random slopes for Time are tested below.
lmm_fit <- lmer(Stylometry_Composite ~ TimePoint * Profile + (1 | ParticipantID),
                data = long_df, REML = TRUE)
summary(lmm_fit)
anova(lmm_fit, type = "III")   # Satterthwaite df, Type III F-tests

# Model comparison: does adding random Time slopes improve fit?
lmm_slope <- lmer(Stylometry_Composite ~ TimePoint * Profile +
                    (TimePoint | ParticipantID),
                  data = long_df, REML = FALSE)
lmm_fit_ml <- lmer(Stylometry_Composite ~ TimePoint * Profile +
                     (1 | ParticipantID),
                   data = long_df, REML = FALSE)
anova(lmm_fit_ml, lmm_slope)   # likelihood-ratio test

## --------------------------------------------------------------------
## 4. Estimated marginal means & planned contrasts
## --------------------------------------------------------------------
emm <- emmeans(lmm_fit, ~ TimePoint | Profile)
pairs(emm)                  # T2-T1, T3-T2, T3-T1 within each profile
contrast(emm, "poly")       # linear & quadratic trends over time
emmip(lmm_fit, Profile ~ TimePoint)  # interaction plot via emmeans

## --------------------------------------------------------------------
## 5. Drift score modeling (wide format)
## --------------------------------------------------------------------
# Drift = change score; test whether drift differs across profiles
drift_fit <- aov(Drift ~ Profile, data = wide_df)
summary(drift_fit)
TukeyHSD(drift_fit)

## --------------------------------------------------------------------
## 6. Effect sizes & assumption checks
## --------------------------------------------------------------------
# Partial eta squared from the afex ANOVA
summary(anova_fit)$anova  # contains ges (generalized eta-squared)

# Residual diagnostics for the LMM
plot(lmm_fit, main = "Residuals vs Fitted")
qqnorm(residuals(lmm_fit)); qqline(residuals(lmm_fit))
