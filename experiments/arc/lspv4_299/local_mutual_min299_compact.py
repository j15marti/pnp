#!/usr/bin/env python3
"""LSPV-4 ARC299 compact replay, small canonical SAT sources.
The mathematical O(log N) incremental implementation streams source clauses
through indexed scans. This Python diagnostic materializes small F and edge
lists and is NOT an FLMV native time/space benchmark. P versus NP OPEN.
"""
from itertools import combinations, product
from collections import Counter
import json

P6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
N6=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y6=P6+tuple(tuple(-v for v in c) for c in N6)
P9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P9+tuple(tuple(-v for v in c) for c in N9)

def source_valid(F):
    if not F: return False
    n=max(abs(z) for c in F for z in c)
    occur=Counter((abs(z),z>0) for c in F for z in c)
    return len({tuple(sorted(c)) for c in F})==len(F) and all(
        len(c)==3 and len({abs(z) for z in c})==3 and
        (all(z>0 for z in c) or all(z<0 for z in c)) for c in F
    ) and all(occur[i,True]==occur[i,False]==2 for i in range(1,n+1))

def edges(F,p):
    out=[]
    for j,c in enumerate(F):
        if any(abs(z) in p and p[abs(z)]==(z>0) for z in c):continue
        rem=[abs(z) for z in c if abs(z) not in p]
        if not rem: return None
        if len(rem)==2:out.append((j,*rem))
    return out

def triangles(E):
    out=[]
    for triple in combinations(E,3):
        deg=Counter(v for _,a,b in triple for v in (a,b))
        if len(deg)==3 and all(q==2 for q in deg.values()):
            out.append(tuple(sorted(edge[0] for edge in triple)))
    return sorted(set(out))

def mu(e,T):
    return next((tr for tr in T if e in tr),None)

def select_mutual(T):
    return [tr for tr in T if all(mu(e,T)==tr for e in tr)]

def select_greedy(T):
    chosen=[];used=set()
    for tr in T:
        if not used.intersection(tr):chosen.append(tr);used.update(tr)
    return chosen

def sat(F,a):
    return all(any(a[abs(z)]==(z>0) for z in c) for c in F)

def test():
    result={}
    for name,F in [('Y6',Y6),('F9',F9)]:
        assert source_valid(F)
        n=max(abs(z) for c in F for z in c)
        total=bad=with_tri=unpacked=different=0
        for vec in product((-1,0,1),repeat=n):
            p={i:v for i,v in enumerate(vec,1) if v!=-1}
            E=edges(F,p);total+=1
            if E is None:bad+=1;continue
            T=triangles(E);S=select_mutual(T);G=select_greedy(T)
            with_tri+=bool(T);unpacked+=bool(S)
            different+=len(S)!=len(G)
            assert len({e for tr in S for e in tr})==3*len(S)
            assert bool(S)==bool(T)
            if name=='F9' and p=={1:1,4:0,5:1,8:0}:
                assert S==[(3,5,7)] and G==[(3,5,7),(4,10,11)]
        models=sum(sat(F,dict(enumerate(a,1))) for a in product((0,1),repeat=n))
        result[name]={'all_cubes':total,'empty':bad,'triangle_states':with_tri,
                      'nonempty_mutual':unpacked,'greedy_different':different,'models':models}
    assert result['Y6']=={'all_cubes':729,'empty':184,'triangle_states':4,'nonempty_mutual':4,'greedy_different':0,'models':20}
    assert result['F9']=={'all_cubes':19683,'empty':7000,'triangle_states':556,'nonempty_mutual':556,'greedy_different':3,'models':70}
    print(json.dumps({'result':result,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':test()
