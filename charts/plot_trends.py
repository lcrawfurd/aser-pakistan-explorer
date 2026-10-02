import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=json.load(open('data/data.json'))
L={(r[0],r[1],r[2],r[3]):r for r in D['ladders']}
E={(r[0],r[1],r[2]):r for r in D['enrol']}
YEARS=[2012,2013,2014,2015,2016,2018,2019,2021,2023,2025]
GEOS=['Pakistan','Punjab','Sindh','Khyber Pakhtunkhwa','Balochistan','Gilgit-Baltistan','AJK','ICT','FATA']
TITLE={'ICT':'Islamabad (ICT)','FATA':'FATA / KP merged districts','AJK':'Azad Jammu & Kashmir'}
def lad(y,g,t,th):
    r=L.get((y,g,t,5))
    if not r or 'dup' in r[7] or 'sum' in r[7]: return None,False
    v=[x for x in r[4][th:] if x is not None]
    return (sum(v) if v else None),('ru' in r[7])
def oos(y,g):
    r=E.get((y,g,'6-16'))
    if not r or 'Never enrolled' not in r[3]: return None,False
    v=r[3]; return v['Never enrolled']+v.get('Dropped out',0),('ru' in r[6])
SER=[('Class 5: read a story (Urdu/Sindhi/Pashto)',lambda y,g:lad(y,g,'language',4),'#1f5f6b'),
     ('Class 5: read English sentences',lambda y,g:lad(y,g,'english',4),'#c9811f'),
     ('Class 5: 2-digit division',lambda y,g:lad(y,g,'arithmetic',6),'#7a4b8c'),
     ('Out of school, ages 6–16',oos,'#a34a2a')]
plt.rcParams.update({'font.size':9})
fig,axs=plt.subplots(3,3,figsize=(12,10.5),sharex=True,sharey=True)
for ax,g in zip(axs.flat,GEOS):
    for name,f,c in SER:
        pts=[(y,)+f(y,g) for y in YEARS]
        rur=[(y,v) for y,v,ru in pts if v is not None and not ru]
        if rur: ax.plot([p[0] for p in rur],[p[1] for p in rur],'-o',color=c,ms=3.5,lw=1.8,label=name)
        for y,v,ru in pts:
            if v is not None and ru: ax.plot([y],[v],'o',mfc='white',mec=c,mew=1.6,ms=5)
    ax.set_title(TITLE.get(g,g),fontsize=11,fontweight='bold',loc='left')
    ax.set_ylim(0,100); ax.set_xlim(2011.3,2025.7); ax.set_xticks([2012,2015,2018,2021,2025])
    ax.grid(axis='y',color='#ddd',lw=.6)
    for s in ('top','right'): ax.spines[s].set_visible(False)
for ax in axs[:,0]: ax.set_ylabel('% of children')
h,l=axs[0,0].get_legend_handles_labels()
fig.legend(h,l,loc='upper center',ncol=4,frameon=False,fontsize=9.5,bbox_to_anchor=(0.5,0.965))
fig.suptitle('ASER Pakistan (rural), 2012–2025: Class 5 learning and out-of-school rates by province',fontsize=13,fontweight='bold',y=0.995)
fig.text(0.01,0.005,'Source: ASER Pakistan national reports 2012–2025 (ITA), class-wise learning and enrolment tables. Class 5 shares are of children enrolled in Class 5, tested on Class 2-level tools.\n'
 'Hollow dots = 2025, which reports rural + urban combined for all except AJK and GB (not comparable with the rural series). 2025 AJK/GB English and division withheld (duplicated tables in report).\n'
 '2012 division is 3-digit. 2021 Punjab division withheld (printed rows do not sum to 100). FATA reported as KP merged districts from 2018; ICT has no 2023 section.',fontsize=7.5,color='#555',va='bottom')
fig.tight_layout(rect=(0,0.06,1,0.95))
fig.savefig('charts/trends_by_province.png',dpi=160)
print('ok')
