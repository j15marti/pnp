#!/usr/bin/env python3
"""Independent stdlib bitmask/graph verifier for ARC signed phase 302.
Does NOT import the producer. Complete no-import verifier and 198-variable
source-certificate replay are in the reproducibility archive. P vs NP OPEN.
"""
from itertools import product,combinations
from collections import Counter,defaultdict
import json
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
CHECK=Counter()
def ask(b,key):
    CHECK[key]+=1
    assert b,key
def metrics(clauses,vec):
    free=[i for i,a in enumerate(vec,1) if a==2]
    plus=Counter();minus=Counter();u=0;edges=[]
    for j,cl in enumerate(clauses,1):
        satisfied=False;remaining=[]
        for z in cl:
            q=vec[abs(z)-1]
            if q==2:remaining.append(z)
            elif q==int(z>0):satisfied=True
        if satisfied:
            for z in remaining:
                if z>0:plus[z]+=1
                else:minus[-z]+=1
        else:
            u+=1
            if len(remaining)==2:edges.append(tuple(map(abs,remaining)))
    e=2*len(free)-u
    eta=sum(min(plus[i],minus[i]) for i in free)
    return e,eta,e-eta,plus,minus,edges
def independent_ids(clauses,n):
    g={i:set() for i in range(1,n+1)}
    for cl in clauses:
        for x,y in combinations(map(abs,cl),2):
            g[x].add(y);g[y].add(x)
    s=[];remain=set(g)
    while remain:
        x=min(remain);s.append(x)
        rm={x}|g[x]
        for v in g[x]:rm|=g[v]
        remain-=rm
    return s,g
def no_odd_cycle(edges):
    adj=defaultdict(set)
    for x,y in edges:adj[x].add(y);adj[y].add(x)
    color={}
    for v in adj:
        if v in color:continue
        color[v]=0;queue=[v]
        for u in queue:
            for w in adj[u]:
                if w not in color:
                    color[w]=color[u]^1;queue.append(w)
                elif color[w]==color[u]:return False
    return True
def truth(c,mask):
    return any(bool(mask & (1<<(abs(z)-1)))==(z>0) for z in c)
def main():
    summary={}
    for name,F,models_expected in (("Y6",Y,20),("F9",F9,70)):
        n=max(abs(z) for c in F for z in c)
        cnt=Counter(z for c in F for z in c)
        ask(n%3==0 and len(F)*3==4*n,'canonical_length')
        ask(all(cnt[i]==cnt[-i]==2 for i in range(1,n+1)),'canonical_signed_quota')
        ask(len(set(tuple(sorted(c)) for c in F))==len(F),'no_duplicate_clauses')
        models=[mask for mask in range(1<<n) if all(truth(c,mask) for c in F)]
        ask(len(models)==models_expected,'complete_models')
        chosen,g=independent_ids(F,n)
        ask(len(chosen)>= (n+64)//65,'greedy_bound')
        for u,v in combinations(chosen,2):
            ask(v not in g[u] and not(g[u]&g[v]),'distance_three')
        for flags in product((0,1),repeat=len(chosen)):
            vec=[2]*n
            for t,(v,b) in enumerate(zip(chosen,flags),1):
                vec[v-1]=b
                e,eta,r,plus,minus,edges=metrics(F,vec)
                ask(e==r==2*n//3 and eta==0,'plateau_r_eta')
                ask(len(edges)==2*t and no_odd_cycle(edges),'plateau_nu')
        for p in product((0,1,2),repeat=n):
            for x in range(1,n+1):
                if p[x-1]!=2:continue
                e,h,r,plus,minus,edges=metrics(F,p)
                for b in (0,1):
                    q=list(p);q[x-1]=b
                    e2,h2,r2,pos2,neg2,edges2=metrics(F,q)
                    signed=plus[x] if b else minus[x]
                    activated=sum(min(pos2[y],neg2[y])-min(plus[y],minus[y])
                                  for y in range(1,n+1) if p[y-1]==2 and y!=x)
                    ask(e-e2==signed,'e_source_quota')
                    ask(r-r2==signed-min(plus[x],minus[x])+activated,'signed_phase_payment')
                    ask(r2<=r,'monotonic')
        # Brute-force all four source-pair extreme compatibilities, all assignments.
        for j,k in combinations(range(len(F)),2):
            L={abs(l):l>0 for l in F[j]}
            R={abs(l):l>0 for l in F[k]}
            same=any(L[x]==R[x] for x in L.keys()&R.keys())
            opp=any(L[x]!=R[x] for x in L.keys()&R.keys())
            for a,b in ((3,3),(3,0),(0,3),(0,0)):
                possible=any(sum(bool(mask&(1<<(abs(z)-1)))==(z>0) for z in F[j])==a and
                             sum(bool(mask&(1<<(abs(z)-1)))==(z>0) for z in F[k])==b
                             for mask in range(1<<n))
                predicted=(not opp) if a==b else (not same)
                ask(possible==predicted,'fourway_extremes')
        summary[name]={'n':n,'m':len(F),'models':len(models),'distance_three_set':chosen}
    print(json.dumps({'status':'PASS','independent':True,'sources':summary,
          'assertions':dict(CHECK),'total':sum(CHECK.values()),
          'native_FLMV':'NOT MEASURED','P_versus_NP':'OPEN'},indent=2,sort_keys=True))
if __name__=="__main__":main()
