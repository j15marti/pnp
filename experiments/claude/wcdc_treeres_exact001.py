#!/usr/bin/env python3
"""WCDC-0001: exact minimum tree-like Resolution(+weakening) refutation size.
Clause code: base-3 digit per variable (0 absent, 1 positive, 2 negative).
s(C)=1 if C weakens an axiom; else min_x s(C+x)+s(C+~x)+1 over absent x.
s(empty) = exact minimum tree-like refutation size (nodes). Infinite iff SAT.
Contrast: GF(2) Gaussian elimination row-operation count for Tseitin (poly).
Each instance n<=12 runs in a few seconds; total < 30 s.
Usage: python3 wcdc_treeres_exact001.py OUT.json
"""
import itertools, json, sys, time, hashlib
import numpy as np
INF=np.int64(1<<40)
def tree_min(n, clauses):
    N=3**n; pw=[3**i for i in range(n)]
    codes=np.arange(N,dtype=np.int64)
    dig=[(codes//pw[i])%3 for i in range(n)]
    width=sum((d>0).astype(np.int64) for d in dig)
    cont=np.zeros(N,dtype=bool)
    for cl in clauses:
        c=0
        for l in set(cl):
            v=abs(l)-1; c+=pw[v]*(1 if l>0 else 2)
        if any(-l in cl for l in cl): continue
        cont[c]=True
    for i in range(n):            # superset (zeta) closure per dimension
        z=np.nonzero(dig[i]==0)[0]
        cont[z+pw[i]]|=cont[z]; cont[z+2*pw[i]]|=cont[z]
    s=np.where(cont,1,INF).astype(np.int64)
    for w in range(n-1,-1,-1):
        for i in range(n):
            z=np.nonzero((width==w)&(dig[i]==0)&(~cont))[0]
            cand=s[z+pw[i]]+s[z+2*pw[i]]+1
            s[z]=np.minimum(s[z],np.minimum(cand,INF))
    r=int(s[0]); return None if r>=INF else r
def php(m):
    var=lambda p,h:p*m+h+1
    C=[[var(p,h) for h in range(m)] for p in range(m+1)]
    C+=[[-var(p,h),-var(q,h)] for h in range(m) for p,q in itertools.combinations(range(m+1),2)]
    return (m+1)*m,C
def tseitin(V,E):
    charge={v:(1 if v==V[0] else 0) for v in V}   # total charge odd -> UNSAT
    C=[]
    for v in V:
        inc=[k+1 for k,e in enumerate(E) if v in e]
        for signs in itertools.product([0,1],repeat=len(inc)):
            if sum(signs)%2!=charge[v]:          # forbid assignments of wrong parity
                C.append([x if b==0 else -x for x,b in zip(inc,signs)])
    return len(E),C,charge
def gf2_ops(V,E,charge):
    rows=[(sum(1<<k for k,e in enumerate(E) if v in e),charge[v]) for v in V]
    ops=0; m=len(E); r=0; rows=list(rows)
    for col in range(m):
        piv=next((j for j in range(r,len(rows)) if rows[j][0]>>col&1),None)
        if piv is None: continue
        rows[r],rows[piv]=rows[piv],rows[r]
        for j in range(len(rows)):
            if j!=r and rows[j][0]>>col&1:
                rows[j]=(rows[j][0]^rows[r][0],rows[j][1]^rows[r][1]); ops+=1
        r+=1
    inconsistent=any(a==0 and b==1 for a,b in rows)
    return ops,inconsistent
def rand3(n,m,seed):
    rng=np.random.default_rng(seed); C=[]
    for _ in range(m):
        vs=rng.choice(n,3,replace=False)+1; sg=rng.integers(0,2,3)
        C.append([int(v) if s else -int(v) for v,s in zip(vs,sg)])
    return C
out={'experiment':'WCDC-0001 exact tree-like resolution minima','system':'tree-like Resolution with weakening, cost=number of proof-tree nodes','rows':[]}
t0=time.time()
for m in (1,2,3):
    n,C=php(m); t=time.time(); val=tree_min(n,C)
    out['rows'].append({'family':'PHP','param':m,'n':n,'clauses':len(C),'tree_min':val,'trivial_cap':2**(n+1)-1,'sec':round(time.time()-t,2)})
graphs={'K4':([0,1,2,3],list(itertools.combinations(range(4),2))),
 'K33':(list(range(6)),[(a,b) for a in range(3) for b in range(3,6)]),
 'prism':(list(range(6)),[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),
 'Q3':(list(range(8)),[(a,b) for a in range(8) for b in range(a+1,8) if bin(a^b).count('1')==1])}
for name,(V,E) in graphs.items():
    n,C,ch=tseitin(V,E); t=time.time(); val=tree_min(n,C); ops,inc=gf2_ops(V,E,ch)
    out['rows'].append({'family':'Tseitin','param':name,'n':n,'clauses':len(C),'tree_min':val,'trivial_cap':2**(n+1)-1,'gf2_row_ops':ops,'gf2_inconsistent':inc,'sec':round(time.time()-t,2)})
# hostile controls: satisfiable Tseitin (even charge) must give None; random 3-CNF worst over seeds
V,E=graphs['K4']; n,C,ch=tseitin(V,E); C2=[]
for v in V:
    inc=[k+1 for k,e in enumerate(E) if v in e]
    for signs in itertools.product([0,1],repeat=len(inc)):
        if sum(signs)%2!=0: C2.append([x if b==0 else -x for x,b in zip(inc,signs)])
out['controls']={'K4_even_charge_SAT_tree_min':tree_min(n,C2)}
for n in (8,10,12):
    vals=[]
    for seed in range(4 if n==12 else 10):
        v=tree_min(n,rand3(n,int(6*n),1000*n+seed))
        if v is not None: vals.append(v)
    out['rows'].append({'family':'random3CNF_ratio6','param':'max over seeds','n':n,'unsat_seeds':len(vals),'tree_min_max':max(vals) if vals else None,'tree_min_min':min(vals) if vals else None,'trivial_cap':2**(n+1)-1})
out['total_sec']=round(time.time()-t0,2)
out['script_sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
json.dump(out,open(sys.argv[1],'w'),indent=1); print(json.dumps(out,indent=1))
