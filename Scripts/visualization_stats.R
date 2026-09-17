# =====================================================================
# visualization_stats.R
# Study figures using ggplot2 / tidyverse
# Data: data_long.csv (ParticipantID, Profile, Wave, TimePoint,
#      Stylometry_Composite), data_wide.csv (T1, T2, T3, Drift)
# Requires: tidyverse, ggpubr (optional)
# =====================================================================

library(tidyverse)

long_df <- read.csv("data_long.csv", stringsAsFactors = FALSE)
wide_df <- read.csv("data_wide.csv", stringsAsFactors = FALSE)
long_df$TimePoint <- factor(long_df$TimePoint, levels = c("T1", "T2", "T3"))

theme_study <- theme_minimal(base_size = 13) +
  theme(legend.position = "bottom",
        panel.grid.minor = element_blank(),
        strip.text = element_text(face = "bold"))

profile_cols <- setNames(
  scales::hue_pal()(length(unique(long_df$Profile))),
  sort(unique(long_df$Profile)))

## --------------------------------------------------------------------
## Figure A: Longitudinal trajectories (spaghetti + group means)
## --------------------------------------------------------------------
fig_trajectories <- ggplot(long_df,
    aes(TimePoint, Stylometry_Composite, group = ParticipantID,
        color = Profile)) +
  geom_line(alpha = 0.25, linewidth = 0.4) +
  geom_line(data = long_df %>%
              group_by(Profile, TimePoint) %>%
              summarise(Stylometry_Composite = mean(Stylometry_Composite),
                        .groups = "drop"),
            aes(group = Profile), linewidth = 1.4) +
  scale_color_manual(values = profile_cols, name = "Profile") +
  labs(title = "Longitudinal Trajectory of Stylometric Composite",
       x = "Time Point", y = "Stylometric Composite Score") +
  theme_study
ggsave("fig_longitudinal_trajectory.png", fig_trajectories,
       width = 8, height = 6, dpi = 300)

## --------------------------------------------------------------------
## Figure B: Drift by profile (box + jitter)
## --------------------------------------------------------------------
fig_drift <- ggplot(wide_df, aes(Profile, Drift, fill = Profile)) +
  geom_boxplot(alpha = 0.6, outlier.shape = NA) +
  geom_jitter(width = 0.15, alpha = 0.5, color = "grey25") +
  scale_fill_manual(values = profile_cols, guide = "none") +
  labs(title = "Stylometric Drift by Writing Profile",
       x = NULL, y = "Drift Score (T3 - T1)") +
  theme_study
ggsave("fig_drift_by_profile.png", fig_drift, width = 7, height = 6, dpi = 300)

## --------------------------------------------------------------------
## Figure C: Group means with 95% CI at each time point
## --------------------------------------------------------------------
fig_means <- long_df %>%
  group_by(Profile, TimePoint) %>%
  summarise(mean = mean(Stylometry_Composite),
            sd   = sd(Stylometry_Composite),
            n    = n(),
            se   = sd / sqrt(n),
            .groups = "drop") %>%
  ggplot(aes(TimePoint, mean, color = Profile, group = Profile)) +
  geom_errorbar(aes(ymin = mean - 1.96 * se, ymax = mean + 1.96 * se),
                width = 0.12) +
  geom_point(size = 2.6) +
  geom_line(linewidth = 0.9) +
  scale_color_manual(values = profile_cols, name = "Profile") +
  labs(title = "Mean Composite Score (±95% CI) by Time Point",
       x = "Time Point", y = "Mean Score") +
  theme_study
ggsave("fig_group_means_ci.png", fig_means, width = 8, height = 6, dpi = 300)

## --------------------------------------------------------------------
## Figure D: Distribution change across waves (density ridge alternative)
## --------------------------------------------------------------------
fig_density <- ggplot(long_df, aes(Stylometry_Composite, fill = TimePoint)) +
  geom_density(alpha = 0.45, color = NA) +
  facet_wrap(~ Profile) +
  scale_fill_brewer(palette = "Blues", name = "Time Point") +
  labs(title = "Distribution of Composite Scores Across Waves",
       x = "Stylometric Composite Score", y = "Density") +
  theme_study
ggsave("fig_density_waves.png", fig_density, width = 9, height = 6, dpi = 300)

cat("Figures saved:",
    c("fig_longitudinal_trajectory.png", "fig_drift_by_profile.png",
      "fig_group_means_ci.png", "fig_density_waves.png"), sep = "\n  ")
