#!/usr/bin/env python3
"""Complete relaxed q=m one-cycle certificate exclusion; n in {4,5,6}.
This is a finite, representation-restricted diagnostic, not P versus NP.
"""
from functools import lru_cache
from itertools import combinations
import json

def solve(n):
    C=([(1,2),(3,4),(-1,-3),(-2,-4),(1,-2,-3,4),(-1,2,3,-4)] if n==4 else
       [(-i,i+1) for i in range(1,n)]+[(1,-n),tuple(range(1,n+1)),tuple(-i for i in range(1,n+1))])
    m=len(C); rows=range(1<<n)
    def tab(c):
        return sum(1<<a for a in rows if any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c))
    def aff(mask,rhs):
        return sum(1<<a for a in rows if ((a&mask).bit_count()&1)==rhs)
    ca={}
    for z in range(3**n):
        t=z;c=[]
        for i in range(1,n+1):
            d=t%3;t//=3
            if d:c.append(i if d==1 else -i)
        ca[tab(c)]=tuple(c)
    af={aff(mask,rhs):(mask,rhs) for mask in range(1<<n) for rhs in (0,1)}
    @lru_cache(None)
    def join(a,b):
        out=set();v=a&b
        supp=sum(any(bool(v>>x&1)!=bool(v>>(x^(1<<i))&1) for x in rows) for i in range(n))
        if supp<=3:out.add(v)
        if a in af and b in af:
            (x,c),(y,d)=af[a],af[b];out.add(aff(x^y,c^d))
        if a in ca and b in ca:
            for A,B in ((ca[a],ca[b]),(ca[b],ca[a])):
                for p in A:
                    if -p in B:
                        z=(set(A)|set(B))-{p,-p}
                        if not any(-t in z for t in z):out.add(tab(z))
        return tuple(out)
    def closure(leaves,all_states=False):
        d=[set() for _ in range(1<<len(leaves))]
        for i,v in enumerate(leaves):d[1<<i].add(v)
        for size in range(2,len(leaves)+1):
            for mask in range(1,1<<len(leaves)):
                if mask.bit_count()!=size:continue
                s=(mask-1)&mask
                while s:
                    t=mask^s
                    if s<t:
                        for a in d[s]:
                            for b in d[t]:d[mask].update(join(min(a,b),max(a,b)))
                    s=(s-1)&mask
        return d if all_states else d[-1]
    sources=[tab(c) for c in C]; inner=closure(sources,True)
    assert 0 not in inner[-1]
    counts=[]
    for size in range(1,m+1):
        tested=0
        for ix in combinations(range(m),size):
            mask=sum(1<<i for i in ix)
            rest=[sources[i] for i in range(m) if not mask>>i&1]
            for f in inner[mask]:
                tested+=1
                assert 0 not in closure([f,f]+rest), ('CYCLE',n,ix)
        counts.append(tested)
    return {'n':n,'m':m,'source_floor':m-1,'one_cycle_budget':m,
            'not_at_m':True,'subtree_cases':counts,'unique_joins':join.cache_info().currsize}

if __name__=='__main__':
    print(json.dumps([solve(n) for n in (4,5,6)],indent=2))
