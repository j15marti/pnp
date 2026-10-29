#!/usr/bin/env python3
"""Static-interface proxy frontier plots and restricted hybrid experiment."""
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
p=Path(__file__).resolve().parent
raw=json.loads((p/'2026-10-29_1500_ARC232_results.json').read_text())
n=1200
bs=list(range(1,n+1))
qs=[max(0,math.ceil(n/(12*b)-.25-1e-12)) for b in bs]
ts=[b+q for b,q in zip(bs,qs)]
fig,ax=plt.subplots(figsize=(9,5.2))
ax.plot(bs,ts,label='log2 time enumeration proxy b+q')
ax.plot(bs,bs,linestyle='--',label='log2 explicit-table space proxy b')
ax.scatter([9,10,11],[20,20,20])
ax.axvline(400,linestyle=':',linewidth=1)
ax.annotate('integer time minimum: 20 at b=9,10,11',xy=(9,20),xytext=(20,125),arrowprops={'arrowstyle':'->'})
ax.annotate('first T/S log-proxy equality: b=400',xy=(400,400),xytext=(80,700),arrowprops={'arrowstyle':'->'})
ax.set_xscale('log')
ax.set_xlabel('fixed structural boundary b (log scale)')
ax.set_ylabel('binary exponent; polynomial overhead not included')
ax.set_title('n=1200: necessary static inequality, NOT a SAT lower bound')
ax.legend(loc='upper left');ax.grid(alpha=.22);fig.tight_layout()
fig.savefig(p/'2026-10-29_1500_ARC232_static_frontier.png',dpi=145);plt.close(fig)
stars={v['q']:v for v in raw['family'] if v['kind']=='star' and v['rhs']==0}
qs=sorted(stars)
raw_b=[stars[q]['full_b'] for q in qs]
local=[math.log2(stars[q]['stats']['local_2subsat_calls']) for q in qs]
slots=[math.log2(stars[q]['stats']['total_separator_table_slots']) for q in qs]
fig,ax=plt.subplots(figsize=(9,5.2))
ax.plot(qs,raw_b,'--',label='log2 full-interface enumeration count (not executed)')
ax.plot(qs,local,'o-',label='log2 observed fixed-e calls (all modules)')
ax.plot(qs,slots,'s-',label='log2 observed separator table slots')
ax.set_xlabel('number of bijunctive children q');ax.set_ylabel('log2 counts (different operations)')
ax.set_title('Certified star class; rank at most 1, one ternary parity message')
ax.grid(alpha=.22);ax.legend();fig.tight_layout()
fig.savefig(p/'2026-10-29_1500_ARC232_restricted_hybrid.png',dpi=145);plt.close(fig)
print('N proxy (n=1200):',round(n*math.log2(n)), 'log2N:',round(math.log2(n*math.log2(n)),4))
print('b=9: proxy t additive',round(20/math.log2(n*math.log2(n)),4),'s additive',round(9/math.log2(n*math.log2(n)),4))