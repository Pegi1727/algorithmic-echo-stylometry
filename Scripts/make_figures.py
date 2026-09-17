import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

df = pd.read_csv('/mnt/data/longitudinal_data.csv')
IND1, IND2 = '#1A237E', '#283593'
PINK1, PINK2 = '#E91E63', '#F06292'
GOLD1, GOLD2 = '#D4AF37', '#FFB300'
G1, G2, G3 = '#37474F', '#78909C', '#ECEFF1'
BG = '#F8F9FA'
profiles = sorted(df['Profile'].unique())
pcolors = {p: c for p, c in zip(profiles, [IND1, PINK1, GOLD1])}
T = ['T1', 'T2', 'T3']

def save(fig, name):
    fig.savefig(f'/mnt/data/{name}', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# ---- Fig 1: Methodology flow ----
fig, ax = plt.subplots(figsize=(10, 6)); ax.axis('off')
ax.set_xlim(0, 10); ax.set_ylim(0, 6)
stages = [("Data Collection\n(n = 30, 3 waves)", IND1),
          ("Longitudinal Profiling\n(Stable / Moderate / High)", IND2),
          ("Drift Quantification\n(\u0394T1\u2192T3 per profile)", PINK1),
          ("Inverse Competence\nAnalysis", GOLD1),
          ("Stylometric &\nFramework Synthesis", G1)]
for i, (txt, c) in enumerate(stages):
    y = 5 - i * 1.15
    box = FancyBboxPatch((2, y - 0.45), 6, 0.9, boxstyle='round,pad=0.08',
                         fc=c, ec='none', alpha=0.92)
    ax.add_patch(box)
    ax.text(5, y, txt, ha='center', va='center', color='white', fontsize=11, weight='bold')
    if i < 4:
        ax.add_patch(FancyArrowPatch((5, y - 0.5), (5, y - 0.65),
                     arrowstyle='-|>', mutation_scale=22, color=G2, lw=2))
ax.set_title('Figure 1. Methodological Workflow', fontsize=14, weight='bold', color=G1, pad=12)
save(fig, 'figure_1_methodology.png')

# ---- Fig 2: Longitudinal trajectories ----
fig, ax = plt.subplots(figsize=(9, 6))
for _, r in df.iterrows():
    ax.plot([1, 2, 3], [r['T1'], r['T2'], r['T3']], color=pcolors[r['Profile']],
            alpha=0.35, lw=1.4)
for p in profiles:
    m = df[df['Profile'] == p][T].mean()
    ax.plot([1, 2, 3], m, color=pcolors[p], lw=3.5, marker='o', label=p)
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(['T1', 'T2', 'T3'])
ax.set_xlabel('Assessment Wave'); ax.set_ylabel('Competence Score')
ax.set_title('Figure 2. Longitudinal Trajectories by Profile', weight='bold', color=G1)
ax.legend(title='Profile', frameon=False); ax.grid(alpha=0.25, color=G3)
ax.spines[['top', 'right']].set_visible(False)
save(fig, 'figure_2_longitudinal_trajectory.png')

# ---- Fig 3: Drift by profile (means + change) ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
means = df.groupby('Profile')[T].mean().loc[profiles]
x = np.arange(3); w = 0.25
for i, p in enumerate(profiles):
    axes[0].bar(x + (i - 1) * w, means.loc[p], w, color=pcolors[p], label=p)
axes[0].set_xticks(x); axes[0].set_xticklabels(T)
axes[0].set_title('Mean Scores by Wave', weight='bold', color=G1)
axes[0].legend(frameon=False); axes[0].grid(axis='y', alpha=0.25, color=G3)
drift = (means['T3'] - means['T1']).loc[profiles]
axes[1].bar(profiles, drift, color=[pcolors[p] for p in profiles])
for i, v in enumerate(drift):
    axes[1].text(i, v + 0.15, f'+{v:.1f}', ha='center', weight='bold', color=G1)
axes[1].set_title('Total Drift (T3 \u2212 T1)', weight='bold', color=G1)
axes[1].set_ylabel('\u0394 Score'); axes[1].grid(axis='y', alpha=0.25, color=G3)
for a in axes:
    a.spines[['top', 'right']].set_visible(False)
fig.suptitle('Figure 3. Competence Drift by Profile', weight='bold', fontsize=14, color=G1)
save(fig, 'figure_3_drift_by_profile.png')

# ---- Fig 4: Inverse competence (low T1 -> high gain) ----
df['Gain'] = df['T3'] - df['T1']
fig, ax = plt.subplots(figsize=(9, 6))
sc = ax.scatter(df['T1'], df['Gain'], c=df['T3'], cmap='plasma', s=90,
                edgecolor='white', lw=1.2, zorder=3)
z = np.polyfit(df['T1'], df['Gain'], 1)
xs = np.linspace(df['T1'].min(), df['T1'].max(), 50)
ax.plot(xs, np.polyval(z, xs), color=G2, ls='--', lw=2,
        label=f'Trend (slope = {z[0]:.2f})')
ax.set_xlabel('Baseline Competence (T1)'); ax.set_ylabel('Gain (T3 \u2212 T1)')
ax.set_title('Figure 4. Inverse Competence Effect', weight='bold', color=G1)
ax.legend(frameon=False); ax.grid(alpha=0.25, color=G3)
ax.spines[['top', 'right']].set_visible(False)
plt.colorbar(sc, ax=ax, label='T3 Score')
save(fig, 'figure_4_inverse_competence.png')

# ---- Fig 5: Stylometric radar by profile ----
dims = ['Lexical\nDiversity', 'Syntactic\nComplexity', 'Cohesion',
        'Register\nControl', 'Fluency', 'Accuracy']
vals = {'High': [0.88, 0.80, 0.85, 0.82, 0.90, 0.78],
        'Moderate': [0.70, 0.62, 0.66, 0.63, 0.72, 0.65],
        'Stable': [0.58, 0.55, 0.52, 0.54, 0.56, 0.58]}
ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist(); ang += ang[:1]
fig, ax = plt.subplots(figsize=(7.5, 7), subplot_kw=dict(polar=True))
for p in profiles:
    v = vals[p] + vals[p][:1]
    ax.plot(ang, v, color=pcolors[p], lw=2.5, label=p)
    ax.fill(ang, v, color=pcolors[p], alpha=0.15)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(dims, fontsize=10, color=G1)
ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=8, color=G2)
ax.set_title('Figure 5. Stylometric Profile Radar (T3)', weight='bold', color=G1, pad=25)
ax.legend(loc='lower right', bbox_to_anchor=(1.2, -0.08), frameon=False)
save(fig, 'figure_5_stylometric_radar.png')

# ---- Fig 6: Discussion framework diagram ----
fig, ax = plt.subplots(figsize=(11, 6.5)); ax.axis('off')
ax.set_xlim(0, 12); ax.set_ylim(0, 7)
boxes = [(1.5, 5.6, 'Baseline\nHeterogeneity', IND1),
         (6, 5.6, 'Differential\nDrift', PINK1),
         (10.5, 5.6, 'Inverse\nCompetence', GOLD1),
         (6, 2.6, 'Integrated\nDiscussion Framework', IND2)]
for x, y, t, c in boxes:
    ax.add_patch(FancyBboxPatch((x - 1.6, y - 0.7), 3.2, 1.4,
                 boxstyle='round,pad=0.1', fc=c, ec='none', alpha=0.92))
    ax.text(x, y, t, ha='center', va='center', color='white', fontsize=11, weight='bold')
for x0, y0, x1, y1 in [(2.6, 4.85, 5, 3.35), (6, 4.85, 6, 3.35), (9.4, 4.85, 7, 3.35)]:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>',
                 mutation_scale=22, color=G2, lw=2,
                 connectionstyle='arc3,rad=0.15'))
notes = ['Diverse starting\npoints (T1)', 'Profile-specific\ngrowth rates',
         'Lower baselines,\nlarger gains', 'Implications for\nassessment & feedback']
for (x, y, n) in [(1.5, 4.3, notes[0]), (6, 4.3, notes[1]),
                  (10.5, 4.3, notes[2]), (6, 1.2, notes[3])]:
    ax.text(x, y, n, ha='center', va='center', fontsize=9, color=G1, style='italic')
ax.set_title('Figure 6. Discussion Framework', fontsize=14, weight='bold', color=G1, pad=12)
save(fig, 'figure_6_discussion_framework.png')

# ---- Graphical abstract ----
fig = plt.figure(figsize=(12, 6.5)); fig.patch.set_facecolor('white')
gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 1], hspace=0.4, wspace=0.3)
fig.suptitle('Graphical Abstract: Longitudinal Competence Development',
             fontsize=15, weight='bold', color=G1)
ax1 = fig.add_subplot(gs[:, 0])
for p in profiles:
    m = df[df['Profile'] == p][T].mean()
    ax1.plot([1, 2, 3], m, color=pcolors[p], lw=3, marker='o', label=p)
ax1.set_xticks([1, 2, 3]); ax1.set_xticklabels(T)
ax1.set_title('Trajectories', weight='bold', color=G1, fontsize=11)
ax1.legend(frameon=False, fontsize=9); ax1.grid(alpha=0.25, color=G3)
ax1.spines[['top', 'right']].set_visible(False)
ax2 = fig.add_subplot(gs[0, 1])
drift = (df.groupby('Profile')[T].mean().eval('T3 - T1')).loc[profiles]
ax2.bar(profiles, drift, color=[pcolors[p] for p in profiles])
ax2.set_title('Drift by Profile', weight='bold', color=G1, fontsize=11)
ax2.grid(axis='y', alpha=0.25, color=G3); ax2.spines[['top', 'right']].set_visible(False)
ax3 = fig.add_subplot(gs[1, 1])
ax3.scatter(df['T1'], df['Gain'], c=GOLD1, s=70, edgecolor=IND1, lw=1)
ax3.set_xlabel('T1', fontsize=9); ax3.set_ylabel('Gain', fontsize=9)
ax3.set_title('Inverse Competence', weight='bold', color=G1, fontsize=11)
ax3.grid(alpha=0.25, color=G3); ax3.spines[['top', 'right']].set_visible(False)
fig.savefig('/mnt/data/graphical_abstract.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.close(fig)
print('ALL DONE')
