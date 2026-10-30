#!/usr/bin/env python3
import json,math
import matplotlib.pyplot as plt
from pathlib import Path
p=Path(__file__).with_name('2026-10-29_1715_LSPV-2_AFFINE_PROFILE_CROSSOVER234_raw.json')
r=json.loads(p.read_text());rows=r['records']
k=[z['k'] for z in rows]
a=[math.log2(z['encoding']['sparse_affine_bits']) for z in rows]
b=[math.log2(z['encoding']['robdd_bits']) for z in rows]
d=[math.log2(z['encoding']['dense_bits']) for z in rows]
fig,ax=plt.subplots(figsize=(8.4,4.2))
ax.plot(k,d,marker='o',label='Dense explicit profile: log2 bits')
ax.plot(k,b,marker='s',label='Reduced ordered BDD: log2 bits')
ax.plot(k,a,marker='^',label='Sparse affine rows: log2 bits')
ax.axvline(3,linestyle='--',alpha=.7)
ax.text(3.2,26,'First BDD/dense size crossover at k=3',fontsize=9,va='center')
ax.set_xlabel('Independent parity blocks k (realized connected exact22 family)')
ax.set_ylabel('log2 physical encoded bits')
ax.grid(alpha=.25)
ax.legend(loc='upper left',fontsize=8)
fig.tight_layout()
out=Path(__file__).with_name('2026-10-29_1715_LSPV-2_AFFINE_PROFILE_CROSSOVER234_frontier.png')
fig.savefig(out,dpi=180)
print(out)