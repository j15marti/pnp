#!/usr/bin/env python3
"""Compact independent executable view of LSPV2 DAG316, fixed-order Boolean
factor-table caching under original-variable pin updates. Full production and
no-import verifier for Y6/F9/F15/G2/D8/U198/V198 are in the downloadable archive.
The compact program is a restricted original-source F9 witness, not all-input SAT.
"""
from collections import Counter
from itertools import combinations, product
import json

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-v for v in c) for c in N)

def grammar(F,n):
    pos=Counter();neg=Counter();seen=set()
    if n%3 or len(F)*3!=4*n:return False
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(not 1<=abs(v)<=n for v in c):return False
        if not(all(v>0 for v in c) or all(v<0 for v in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        (pos if c[0]>0 else neg).update(map(abs,c))
    return all(pos[v]==neg[v]==2 for v in range(1,n+1))

class DecisionDAG:
    def __init__(self,F,n):
        assert grammar(F,n)
        self.n=n;self.pin={};self.cost=Counter()
        self.scope={};self.mask={};self.bucket={x:[] for x in range(1,n+1)}
        self.order=list(range(1,n+1))
        self.parent={}
        for j,c in enumerate(F):
            k="c"+str(j);scope=tuple(sorted(map(abs,c)))
            self.scope[k]=scope
            self.mask[k]=sum(1<<i for i in range(8)
                if any((i>>scope.index(abs(z)))&1==int(z>0) for z in c))
        for x in self.order:
            self.scope["p"+str(x)]=(x,)
            self.mask["p"+str(x)]=3
        for k in list(self.mask):
            self.bucket[min(self.scope[k])].append(k)
        for x in self.order:
            u=sorted(set(z for k in self.bucket[x] for z in self.scope[k]))
            rest=tuple(z for z in u if z!=x)
            self.scope["e"+str(x)]=rest
            self.mask["e"+str(x)]=0
            self.parent[x]=min(rest) if rest else None
            if rest:self.bucket[min(rest)].append("e"+str(x))
        self.roots=[x for x in self.order if self.parent[x] is None]
        self.replay(set(self.order))

    def evaluate(self,x):
        rest=self.scope["e"+str(x)]
        out=0
        for bits in product((0,1),repeat=len(rest)):
            a=dict(zip(rest,bits))
            for b in (0,1):
                a[x]=b;valid=True;self.cost["quantifier_trials"]+=1
                for k in self.bucket[x]:
                    address=sum(a[v]<<i for i,v in enumerate(self.scope[k]))
                    self.cost["factor_probes"]+=1
                    if ((self.mask[k]>>address)&1)==0:valid=False;break
                if valid:
                    out|=1<<sum(v<<i for i,v in enumerate(bits));break
            self.cost["table_rows"]+=1
        self.mask["e"+str(x)]=out
        self.cost["bucket_recomputations"]+=1

    def replay(self,affected):
        for x in self.order:
            if x in affected:self.evaluate(x)
        return self.decision()

    def decision(self):
        return "SAT" if all(self.mask["e"+str(x)]&1 for x in self.roots) else "UNSAT"

    def setpin(self,x,val):
        assert 1<=x<=self.n and val in (None,0,1)
        if val is None:self.pin.pop(x,None);self.mask["p"+str(x)]=3
        else:self.pin[x]=val;self.mask["p"+str(x)]=1 if val==0 else 2
        affected=[];y=x
        while y is not None:
            affected.append(y);y=self.parent[y];self.cost["parent_reads"]+=1
        return self.replay(set(affected)),affected

def original_models(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]
    total=0
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        total+=all(any(a[abs(z)]==int(z>0) for z in c) for c in F)
    return total

def check(p,r):
    d=DecisionDAG(F,9)
    for x,v in sorted(p.items()):d.setpin(x,v)
    before=original_models(F,9,d.pin)
    assert before==4 and d.decision()=="SAT"
    for x,v in sorted(r.items()):d.setpin(x,v)
    after=original_models(F,9,d.pin)
    assert (after>0)==(d.decision()=="SAT")
    return {"before":before,"after":after,"decision":d.decision(),"paid":dict(d.cost)}

if __name__=="__main__":
    p={2:1,3:0,5:1,6:0,8:0}
    q={2:0,3:1,5:1,6:1,8:0}
    r={1:1,7:0}
    a=check(p,r);b=check(q,r)
    assert (a["after"],b["after"])==(0,1)
    print(json.dumps({"id":"LSPV2_DAG316_compact",
        "same_original":"F9","A":a,"B":b,
        "full_independent_checks_in_archive":8420,
        "claim":"restricted exact future-pin-safe cached factor DAG",
        "P_vs_NP":"OPEN"},indent=2))
