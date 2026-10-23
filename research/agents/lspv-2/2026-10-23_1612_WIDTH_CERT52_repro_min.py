#!/usr/bin/env python3
"""WIDTH-CERT52 minimal reproducibility: stdlib Python 3, no dependencies.
Tests matched 3-color CNF input, induced width, exact elimination, and counts.
The complete 666-check audit is in the conversation artifact; this is a
standalone smaller independently runnable reproduction of the core theorem.
"""
from itertools import combinations, product

def edges_ladder(t, unsat):
    assert t >= 3
    E = {tuple(sorted((2*i, 2*i+1))) for i in range(t)}
    for i in range(t-1):
        E.add((2*i, 2*i+2))
        E.add((2*i+1, 2*i+3))
    E.add((0, 3))
    E.add((1, 2) if unsat else (3, 4))
    assert len(E) == 3*t
    return 2*t, sorted(E)

def edges_wheel(g, unsat):
    assert g >= 7 and g%2==1
    E = {tuple(sorted((i,(i+1)%g))) for i in range(g)}
    E.update((i,g) for i in range(g) if unsat or i != 0)
    if not unsat: E.add((1,4))
    return g+1, sorted(E)

def source_cnf(q, E):
    def x(v,c):return 3*v+c+1
    cs=[]
    for v in range(q):
        cs.append(tuple(x(v,c) for c in range(3)))
        cs.extend((-x(v,a),-x(v,b)) for a,b in combinations(range(3),2))
    for u,v in E:cs.extend((-x(u,c),-x(v,c)) for c in range(3))
    return cs

def width(q, E):
    G={v:set() for v in range(q)}
    for u,v in E:G[u].add(v);G[v].add(u)
    h=0
    for v in range(q):
        N=list(G[v]);h=max(h,len(N))
        for x,y in combinations(N,2):G[x].add(y);G[y].add(x)
        for x in N:G[x].remove(v)
        del G[v]
    return h

def exact_eliminate(q,E):
    factors=[((u,v),{(a,b) for a in range(3) for b in range(3) if a != b}) for u,v in E]
    saved=[]
    for v in range(q):
        curr=[f for f in factors if v in f[0]]
        factors=[f for f in factors if v not in f[0]]
        others=tuple(sorted({i for scope,_ in curr for i in scope if i!=v}))
        assert len(others) <= 4
        accepted=set();choice={}
        for row in product(range(3),repeat=len(others)):
            env=dict(zip(others,row))
            for x in range(3):
                env[v]=x
                if all(tuple(env[j] for j in scope) in allowed for scope,allowed in curr):
                    accepted.add(row);choice[row]=x;break
        factors.append((others,accepted))
        saved.append((v,others,choice))
    sat=all(() in allow for scope,allow in factors)
    if not sat:return False,None
    a={}
    for v,others,choice in reversed(saved):
        a[v]=choice[tuple(a[x] for x in others)]
    result=tuple(a[i] for i in range(q))
    assert all(result[u]!=result[v] for u,v in E)
    return True,result

def evaluate(cnf,onehot):
    return all(any(onehot[abs(l)-1]==(l>0) for l in clause) for clause in cnf)

def brute_colors(q,E):
    return sum(all(a[u]!=a[v] for u,v in E) for a in product(range(3),repeat=q))

def main():
    checks=0
    for t in [3,4,5,12,24,64,160]:
        for bad in (False,True):
            q,E=edges_ladder(t,bad)
            C=source_cnf(q,E)
            assert len(C)==17*t
            assert width(q,E)<=3
            sat,colors=exact_eliminate(q,E)
            assert sat != bad
            if sat:
                bits=[int(colors[v]==c) for v in range(q) for c in range(3)]
                assert evaluate(C,bits)
            if t<=5:
                count=brute_colors(q,E)
                assert count==(0 if bad else 6*3**(t-3))
            checks+=4
    for g in [7,9,11,31,63,127]:
        for bad in (False,True):
            q,E=edges_wheel(g,bad)
            assert len(E)==2*g and width(q,E)<=4
            sat,colors=exact_eliminate(q,E)
            assert sat != bad
            if sat:
                bits=[int(colors[v]==c) for v in range(q) for c in range(3)]
                assert evaluate(source_cnf(q,E),bits)
            if g==7:assert (brute_colors(q,E)>0)==sat
            checks+=3
    print({"run":"WIDTH-CERT52-repro-min","checks":checks,"failures":0,
           "P_vs_NP":"OPEN", "meaning":"restricted charged upper bound only"})
if __name__=="__main__":main()
