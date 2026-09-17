import numpy as np, pandas as pd, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

IND1, IND2 = '#1A237E', '#283593'
PNK1, PNK2 = '#E91E63', '#F06292'
GLD1, GLD2 = '#D4AF37', '#FFB300'
GRY1, GRY2, GRY3 = '#37474F', '#78909C', '#ECEFF1'
BG, WHITE = '#F8F9FA', '#FFFFFF'

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.edgecolor':GRY1,
 'axes.labelcolor':GRY1,'text.color':GRY1,'xtick.color':GRY1,'ytick.color':GRY1,
 'axes.linewidth':0.9,'figure.facecolor':WHITE,'axes.facecolor':WHITE,
 'savefig.dpi':300,'savefig.bbox':'tight','savefig.facecolor':WHITE})
OUT = '/mnt/data/'
df = pd.read_csv(OUTate':GLD1,'Stable':_COLOR = {'High':PNK1,'Moderate':GLD1,'Stable':GRY2}
PROF_ORDER = ['High','Moderate','Stable']

def check(name):
Moderate','Stable']

def check(name):
 os.path.exists(p) and os.path.getsize(p) > 0
    print(name, 'OK' if ok else 'MISSING', os.path.getsize(p) if os.path.exists(p) else 0)

# ---------------- graphical abstract ----------------
fig = plt.figure(figsize=(11,7.5))
gs = fig.add_gridspec(3,3,hspace=0.55,wspace=0.35)
axt = fig.add_subplot(gs[0,:]); axt.axis('off')
axt.add_patch(plt.Rectangle((0,0.1),1,0.8,transform=axt.transAxes,color=IND1,zorder=1))
axt.text(0.5,0.5,'Longitudinal Growth of AI-Mediated Competence:\nInverse Trajectories across Learner Profiles (T1-T3)',
 transform=axt.transAxes,ha='center',va='center',color=WHITE,fontsize=14,fontweight='bold',zorder=2,linespacing=1.5)
axA = fig.add_subplot(gs[1,0])
for prof in PROF_ORDER:
    sub = df[df.Profile==prof]
    axA.plot([1,2,3],sub[['T1','T2','T3']].mean(),'o-',lw=2.5,ms=6,color=PROF_COLOR[prof],label=prof)
axA.set_title('A  Trajectories',loc='left',fontweight='bold',color=IND1)
axA.set_xticks([1,2,3]); axA.set_xticklabels(['T1','T2','T3'])
axA.set_ylabel('Competence score'); axA.legend(frameon=False,fontsize=8); axA.set_facecolor(BG)
axB = fig.add_subplot(gs[1,1])
df['gain'] = df.T3-df.T1
for prof in PROF_ORDER:
    s = df[df.Profile==prof]
    axB.scatter(s.T1,s.gain,s=45,color=PROF_COLOR[prof],alpha=.85,edgecolor=WHITE,lw=.6,label=prof)
x = df.T1.values.astype(float); y = df.gain.values.astype(float)
b = np.polyfit(x,y,1); r = np.corrcoef(x,y)[0,1]
xs = np.linspace(x.min(),x.max(),10)
axB.plot(xs,np.polyval(b,xs),'--',color=IND1,lw=1.6)
axB.text(0.05,0.9,'r = %.2f'%r,transform=axB.transAxes,fontweight='bold',color=IND1)
axB.set_title('B bold',color=IND1left',fontweight='bold',color=IND1)
axB.set_xlabel('Baseline T1'); axB.set_ylabel('Gain (T3-T1)'); axB.set_facecolor(BG)
axC = fig.add_subplot(gs[1,2])
w = 0.26
for i,t in enumerate(['T1','T2','T3']):
    m = df.groupby('Profile')[t].mean().reindex(PROF_ORDER)
    axC.bar(np.arange(3)+(i-1)*w,m,w,color=[IND2,PNK2,GLD2][i],label=t,edgecolor=WHITE)
axC.set_xticks(range(3)); axC.set_xticklabels(PROF_ORDER)
axC.set_title('C  Profile means',loc='left',fontweight='bold',color=IND1)
axC.legend(frameon=False,fontsize=8,ncol=3,loc='upper left'); axC.set_facecolor(BG)
axD = fig.add_subplot(gs[2,:]); axD.axis('off')
msgs = [('High start, small gain',PNK1),('Weakest baseline, steepest gain',IND1),('Drift is profile-specific',GLD1)]
for i,(m,c) in enumerate(msgs):
    axD.add_patch(FancyBboxPatch((i*0.34+0.02,0.25),0.29,0.5,transform=axD.transAxes,
      boxstyle='round,pad=0.02',fc=GRY3,ec=c,lw=2))
    axD.text(i*0.34+0.165,0.5,m,transform=axD.transAxes,ha='center',va='center',fontsize=9,color=GRY1,fontweight='bold')
fig.savefig(OUT+'graphical_abstract.png'); plt.close(fig); check('graphical_abstract.png')

# ---------------- figure 1: methodology ----------------
fig, ax = plt.subplots(figsize=(10,7.2)); ax.axis('off')
ax.set_xlim(0,10); ax.set_ylim(0,10)
def box(x,y,w,h,txt,fc,tc,fs=10,ec=GRY1,lw=1.4):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.12',fc=fc,ec=ec,lw=lw))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,color=tc,fontweight='bold',linespacing=1.35)
def arrow(x1,y1,x2,y2,c=GRY2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=16,color=c,lw=1.6,shrinkA=3,shrinkB=3))
ax.text(5,9.6,'Figure 1.  Study Design and Analytic Pipeline',ha='center',fontsize=14,fontweight='bold',color=IND1)
box(3.1,8.2,3.8,0.9,'N = 30 participants\nLongitudinal panel (T1-T3)',IND1,WHITE)
arrow(3.5,8.65,1.8,7.75); arrow(5,8.2,5,7.75); arrow(6.5,8.65,8.2,7.75)
box(0.5,6.6,2.6,1.1,'Instrument\nCompetence test\n+ writing samples',GRY3,GRY1,ec=IND2)
box(3.7,6.6,2.6,1.1,'Repeated\nmeasurement\n3 waves',GRY3,GRY1,ec=PNK2)
box(6.9,6.6,2.6,1.1,'Ethical approval\n+ informed consent\n(anonymous IDs)',GRY3,GRY1,ec=GLD1)
arrow(1.8,6.6,1.8,5.85); arrow(5,6.6,5,5.85); arrow(8.2,6.6,8.2,5.85)
box(0.5,4.7,2.6,1.1,'Latent profile\nanalysis\n(High / Moderate / Stable)',WHITE,GRY1,ec=IND1)
box(3.7,4.7,2.6,1.1,'Longitudinal\nmixed / repeated-\nmeasures models',WHITE,GRY1,ec=PNK1)
box(6.9,4.7,2.6,1.1,'Stylometric\nanalysis\n(lexical, syntactic)',WHITE,GRY1,ec=GLD1)
arrow(1.8,4.7,1.8,3.95); arrow(5,4.7,5,3.95); arrow(8.2,4.7,8.2,3.95)
box(0.5,2.9,2.6,1.0,'Trajectory\nclassification',IND2,WHITE)
box(3.7,2.9,2.6,1.0,'Drift estimation\n(delta per profile)',PNK2,WHITE)
box(6.9,2.9,2.6,1.0,'Authorship /\nstyle fingerprints',GLD1,WHITE)
arrow(1.8,2.9,3.2(8.2,2.9,2.9,5,2.15); arrow(8.2,2.9,6.8,2.15)
box(2.2,1.1,5.6,1.0,'Integration: inverse-competence model of AI-mediated writing',IND1,WHITE,fs=11)
fig.savefig(OUT+'figure_1_methodology.png'); plt.close(fig); check('figure_1_methodology.png')

# ---------------- figure 2: trajectory ----------------
fig,axes = plt.subplots(1,2,figsize=(11,4.8),gridspec_kw={'width_ratios':[1.15,1]})
ax = axes[0]
rng = np.random.default_rng(7)
for prof in PROF_ORDER:
    sub = df[df.Profile==prof]
    for _,row in sub.iterrows():
        yv = row[['T1','T2','T3']].values.astype(float).copy()+rng.normal(0,0.22,3)
        ax.plot([1,2,3],yv,color=PROF_COLOR[prof],alpha=0.25,lw=1.1,zorder=1)
for prof in PROF_ORDER:
    sub = df[df.Profile==prof]
    m = sub[['T1','T2','T3']].mean(); se = sub[['T1','T2','T3']].std()/np.sqrt(len(sub))
    ax.errorbar([1,2,3],m,yerr=se,fmt='o-',lw=2.8,ms=8,color=PROF_COLOR[prof],capsize=4,
                label='%s (n=%d)'%(prof,len(sub)),zorder=3)
ax.set_xticks([1,2,3]); ax.set_xticklabels(['T1 (baseline)','T2 (mid)','T3 (post)'])
ax.set_ylabel('Competence score'); ax.set_title('A  Individual and mean trajectories',loc='left',fontweight='bold',color=IND1)
ax.legend(frameon=False,fontsize=8.5); ax.set_facecolor(BG); ax.grid(axis='y',color=GRY3,lw=0.8)
ax = axes[1]
pm = df.groupby('Profile')[['T1','T3']].mean().reindex(PROF_ORDER)
g = df.assign(g=df.T3-df.T1).groupby('Profile')['g'].mean().reindex(PROF_ORDER)
xx = np.arange(3); w = 0.32
ax.bar(xx-w/2,pm.T1,w,color=GRY2,label='T1',edgecolor=WHITE)
ax.bar(xx+w/2,pm.T3,w,color=PNK1,label='T3',edgecolor=WHITE)
for i,prof in enumerate(PROF_ORDER):
    ax.annotate('Delta = %+.1f'%g[prof],(i,max(pm.loc[prof])+1.0),ha='center',fontweight='bold',color=PROF_COLOR[prof],fontsize=10)
ax.set_xticks(xx); ax.set_xticklabels(PROF_ORDER)
ax.set_ylabel('Mean competence score'); ax.set_title('B  Baseline vs. post with total change',loc='left',fontweight='bold',color=IND1)
ax.legend(frameon=False); ax.set_facecolor(BG); ax.grid(axis='y',color=GRY3,lw=0.8)
fig.tight_layout(); fig.savefig(OUT+'figure_2_longitudinal_trajectory.png'); plt.close(fig); check('figure_2_longitudinal_trajectory.png')

# ---------------- figure 3: drift by profile ----------------
fig,axes = plt.subplots(1,3,figsize=(12,4.3),sharey=True)
for ax,prof in zip(axes,PROF_ORDER):
    sub = df[df.Profile==prof]
    for _,row in sub.iterrows():
        ax.plot([1,2,3],row[['T1','T2','T3']].astype(float),color=PROF_COLOR[prof],alpha=0.45,lw=1.4)
        ax.scatter([1,2,3],row[['T1','T2','T3']].astype(float),s=14,color=PROF_COLOR[prof],alpha=0.6)
    m = sub[['T1','T2','T3']].mean(); sd = sub[['T1','T2','T3']].std()
    ax.plot([1,2,3],m,color=IND1,lw=3,zorder=3)
    ax.fill_between([1,2,3],m-sd,m+sd,color=PROF_COLOR[prof],alpha=0.12,zorder=2)
    ax.set_title('%s (n=%d)\nDelta T1-T3 = %+.1f pts'%(prof,len(sub),m['T3']-m['T1']),fontweight='bold',color=PROF_COLOR[prof])
    ax.set_xticks([1,2,3]); ax.set_xticklabels(['T1','T2','T3']); ax.set_facecolor(BG); ax.grid(axis='y',color=GRY3,lw=0.8)
axes[0].set_ylabel('Competence score')
fig.suptitle('Figure 3.  Within-Profile Drift across the Three Waves',fontweight='bold',color=IND1,y=1.02)
fig.tight_layout(); fig.savefig(OUT+'figure_3_drift_by_profile.png'); plt.close(fig); check('figure_3_drift_by_profile.png')

# ---------------- figure 4: inverse competence ----------------
fig,axes = plt.subplots(1,2,figsize=(11,4.8))
ax = axes[0]
df['gain'] = df.T3-df.T1
for prof in PROF_ORDER:
    s = df[df.Profile==prof]
    ax.scatter(s.T1,s.gain,s=70,color=PROF_COLOR[prof],alpha=.85,edgecolor=WHITE,lw=1,label=prof)
x = df.T1.values.astype(float); y = df.gain.values.astype(float)
b = np.polyfit(x,y,1); r = np.corrcoef(x,y)[0,1]
xs = np.linspace(x.min()-0.5,x.max()+0.5,20)
ax.plot(xs,np.polyval(b,xs),'--',color=IND1,lw=2)
ax.text(0.04,0.93,'Pearson r = %.2f   slope = %.2f'%(r,b[0]),transform=ax.transAxes,
        fontweight='bold',color=IND1,bbox=dict(fc=GRY3,ec='none',alpha=0.9,pad=3))
ax.set_xlabel('Baseline competence (T1)'); ax.set_ylabel('Total gain (T3-T1)')
ax.set_title('A  Inverse relationship: start vs. gain',loc='left',fontweight='bold',color=IND1)
ax.legend(frameon=False,fontsize=8.5); ax.set_facecolor(BG); ax.grid(color=GRY3,lw=0.7)
ax = axes[1]
per_id = df.sort_values('T1')
ax.bar(np.arange(len(per_id)),per_id.gain,color=[PROF_COLOR[p] for p in per_id.Profile],
       edgecolor=WHITE,alpha=0.9)
ax.axhline(0,color=GRY1,lw=1)
ax.set_xticks(np.arange(len(per_id))); ax.set_xticklabels(per_id.ID,rotation=90,fontsize=6)
ax.set_ylabel('Total gain (T3 - T1)')
ax.set_title('B  Individual gains ordered by baseline',loc='left',fontweight='bold',color=IND1)
ax.set_facecolor(BG); ax.grid(axis='y',color=GRY3,lw=0.7)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=PROF_COLOR[p],label=p) for p in PROF_ORDER],frameon=False,fontsize=8.5)
fig.tight_layout(); fig.savefig(OUT+'figure_4_inverse_competence.png'); plt.close(fig); check('figure_4_inverse_competence.png')
print('r = %.3f slope = %.3f'%(r,b[0]))
