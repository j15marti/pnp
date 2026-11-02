#!/usr/bin/env python3
"""LSPV2 317 compact exact continuation-safe factor update cutoff.
Full producer and verifier are in the downloadable 317 reproducibility archive.
"""
from itertools import product
from collections import Counter
import json
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-x for x in c) for c in N)
def valid(F,n):
    if n%3 or 3*len(F)!=4*n:return False
    cnt=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(z) for z in c})!=3 or not all(1<=abs(z)<=n for z in c):return False
        if not(all(z>0 for z in c) or all(z<0 for z in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[x]==cnt[-x]==2 for x in range(1,n+1))
class DAG:
    def __init__(self,F,n,early):
        assert valid(F,n)
        self.n=n;self.early=early;self.mask={};self.scope={};self.bucket={x:[] for x in range(1,n+1)}
        self.parent={};self.stats=Counter();self.pin={}
        for j,c in enumerate(F):
            k='c'+str(j);s=tuple(sorted(map(abs,c)));self.scope[k]=s
            self.mask[k]=sum(1<<q for q in range(8) if any((q>>s.index(abs(z)))&1==int(z>0) for z in c))
            self.bucket[s[0]].append(k)
        for x in range(1,n+1):
            k='p'+str(x);self.scope[k]=(x,);self.mask[k]=3;self.bucket[x].append(k)
        for x in range(1,n+1):
            u=sorted({v for k in self.bucket[x] for v in self.scope[k]});r=tuple(v for v in u if v!=x)
            self.scope['e'+str(x)]=r;self.mask['e'+str(x)]=0
            self.parent[x]=r[0] if r else None
            if r:self.bucket[r[0]].append('e'+str(x))
        self.roots=[x for x in range(1,n+1) if self.parent[x] is None]
        for x in range(1,n+1):self.compute(x)
    def compute(self,x):
        r=self.scope['e'+str(x)];out=0
        for q in range(1<<len(r)):
            a={v:(q>>i)&1 for i,v in enumerate(r)}
            for b in (0,1):
                a[x]=b;okay=True
                for k in self.bucket[x]:
                    idx=sum(a[v]<<i for i,v in enumerate(self.scope[k]))
                    self.stats['factor_bits']+=1
                    if not ((self.mask[k]>>idx)&1):okay=False;break
                if okay:out|=1<<q;break
            self.stats['rows']+=1
        k='e'+str(x);old=self.mask[k];changed=False
        for q in range(1<<len(r)):
            self.stats['paid_compares']+=1
            if ((old>>q)&1)!=((out>>q)&1):changed=True
        self.mask[k]=out;self.stats['buckets']+=1
        return changed
    def decision(self):return 'SAT' if all(self.mask['e'+str(x)]&1 for x in self.roots) else 'UNSAT'
    def setpin(self,x,v):
        if not 1<=x<=self.n or v not in (0,1,None):raise ValueError('malformed pin')
        new=3 if v is None else 1<<v;k='p'+str(x)
        if self.mask[k]==new:return self.decision()
        self.mask[k]=new
        if v is None:self.pin.pop(x,None)
        else:self.pin[x]=v
        while x is not None:
            changed=self.compute(x)
            if self.early and not changed:
                self.stats['stops']+=1;break
            x=self.parent[x]
        return self.decision()
def run(pins):
    E=DAG(F,9,True);B=DAG(F,9,False);labels=[]
    for x,v in pins:
        a=E.setpin(x,v);b=B.setpin(x,v)
        assert a==b and E.mask==B.mask
        labels.append(a)
    return {'labels':labels,'early_buckets':E.stats['buckets'],'eager_buckets':B.stats['buckets'],
            'early_factor_bits':E.stats['factor_bits'],'eager_factor_bits':B.stats['factor_bits'],
            'paid_early_equality_reads':E.stats['paid_compares']}
if __name__=='__main__':
    A={2:1,3:0,5:1,6:0,8:0};B={2:0,3:1,5:1,6:1,8:0};R={1:1,7:0}
    a=run(list(A.items())+list(R.items()));b=run(list(B.items())+list(R.items()))
    assert a['labels'][-1]=='UNSAT' and b['labels'][-1]=='SAT'
    print(json.dumps({'id':'LSPV2_EVENT_CUTOFF317_compact','A':a,'B':b,
                      'model':'paid fixed-order Boolean VE','P_vs_NP':'OPEN'},indent=2))
