#!/usr/bin/env python3
"""TMR-3/100 independent strict-C finite smoke test. Python stdlib only."""
from itertools import product, combinations, permutations
from hashlib import sha256
from json import dumps

A = range(5)
def R(x,y): return ((y-x)%5) in (1,3)
def C(x,y,z): return (R(x,y) and R(y,z) and R(z,x)) or (R(x,z) and R(z,y) and R(y,x))
def S(x,y,z): return (R(x,y) and R(z,x)) or (R(x,z) and R(y,x))
def W(x,y): return sum(C(h,x,y) for h in A)

def orbits(s):
    for tail in product(A,repeat=s-1):
        if tail<=tuple((-t)%5 for t in tail): yield (0,)+tail

def count_deleted(edge):
    edges=list(combinations(range(6),2))
    total=0
    for base in product(A,repeat=6):
        prod=5
        for u,v in edges:
            if (u,v)==edge: continue
            prod*=W(base[u],base[v])
            if not prod: break
        total+=prod
    return total

def solve(edges,quotient=True):
    cnt=dict(assignments=0,children=0,pos=0,neg=0,predicate=0)
    ziter=orbits(6) if quotient else product(A,repeat=6)
    for z in ziter:
        cnt['assignments']+=1
        hs=[]
        for u,v in edges:
            cnt['children']+=1
            h=None
            for p in A:
                cnt['predicate']+=1
                if C(p,z[u],z[v]): h=p;break
            if h is None:
                cnt['neg']+=1;break
            cnt['pos']+=1;hs.append(h)
        else:
            assert len(hs)==len(edges) and all(C(h,z[u],z[v]) for h,(u,v) in zip(hs,edges))
            return 'SAT',cnt
    return 'UNSAT',cnt

def main():
    tuples=list(product(A,repeat=3))
    assert sum(map(lambda t:C(*t),tuples))==30
    assert all(C(*t)==(S(*t) and S(t[1],t[0],t[2])) for t in tuples)
    assert all(S(h,u,v)==any(C(h,u,q) and C(h,q,p) and C(h,p,v) for p,q in product(A,repeat=2)) for h,u,v in tuples)
    good={p for p in permutations(A) if all(C(*t)==C(*(p[i] for i in t)) for t in tuples)}
    assert good=={tuple((sg*i+j)%5 for i in A) for j in A for sg in (1,-1)}
    assert [W(0,i) for i in A]==[0,2,1,1,2]
    assert [len(list(orbits(s))) for s in range(1,7)]==[1,3,13,63,313,1563]
    edges=list(combinations(range(6),2))
    assert all(count_deleted(e)==76800 for e in edges)
    results={'unsat_plain':solve(edges,False),
             'unsat_orbit':solve(edges,True),
             'sat_plain':solve([e for e in edges if e!=(0,1)],False),
             'sat_orbit':solve([e for e in edges if e!=(0,1)],True)}
    assert results['unsat_plain'][0]==results['unsat_orbit'][0]=='UNSAT'
    assert results['sat_plain'][0]==results['sat_orbit'][0]=='SAT'
    print(dumps(results,sort_keys=True,indent=2))
if __name__=='__main__': main()
