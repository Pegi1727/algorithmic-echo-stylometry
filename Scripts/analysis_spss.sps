* =====================================================================.
* analysis_spss.sps
* SPSS syntax for the longitudinal stylometric drift study.
* Design: 2 (Profile, between) x 3 (Time, within) mixed design.
* Requires wide-format data: data_wide.csv imported as the active
* dataset (ParticipantID, Profile, T1, T2, T3, Drift).
* =====================================================================.

* ---- Import wide data (adjust path if needed). ----.
GET DATA /TYPE=TXT /FILE="data_wide.csv" /DELIMITERS="," /QUALIFIER='"'
  /FIRSTCASE=2
  /VARIABLES=
    ParticipantID A10 Profile A20 T1 F10.5 T2 F10.5 T3 F10.5 Drift F10.5.
DATASET NAME drift WINDOW=FRONT.

* ---- Define within-subject factor. ----.
GLM T1 T2 T3 BY Profile
  /WSFACTOR=Time 3 Polynomial
  /MEASURE=Composite
  /METHOD=SSTYPE(3)
  /EMMEANS=TABLES(Profile) COMPARE ADJ(BONFERRONI)
  /EMMEANS=TABLES(Time)   COMPARE ADJ(BONFERRONI)
  /EMMEANS=TABLES(Profile*Time) COMPARE(Profile) ADJ(BONFERRONI)
  /PRINT=DESCRIPTIVE ETASQ OPOWER HOMOGENEITY
  /PLOT=PROFILE(Time*Profile)
  /WSDESIGN=Time
  /DESIGN=Profile.

* Notes:
* - Mauchly's test of sphericity and Greenhouse-Geisser / Huynh-Feldt
*   corrections appear automatically in the output.
* - The Polynomial contrast gives linear and quadratic trends over Time.
* - Partial eta squared is requested via ETASQ.

* ---- Between-group test on drift scores (T3 - T1). ----.
ONEWAY Drift BY Profile
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /POSTHOC=TUKEY ALPHA(0.05)
  /PLOT=NONE.

* ---- Optional: reliability / distribution checks. ----.
DESCRIPTIVES VARIABLES=T1 T2 T3 Drift /STATISTICS=MEAN STDDEV MINift /STATISTICS=MEAN STDDEV MIN Profile /PLOT=BOXPLOT NPPLOT /STATISTICS=NONE.
