#!/usr/bin/env python3
"""GATE281 compact, stdlib-only independent finite reproducer.
The unbounded certificate uses Edmonds' perfect-matching polytope (1965).
This finite enumerator is NOT a general SAT algorithm or FLMV machine.
Run: python experiments/arc/lspv3_281/gate281_compact.py
"""
import itertools
from collections import Counter

def from_graph(edges, minus):
    n=len(edges)
    vertices=sorted(set(v for ab in edges for v in ab))
    pos=[tuple(i+1 for i,ab in enumerate(edges) if v in ab) for v in vertices]
    neg=[tuple(-x for x in row) for row in minus]
    return pos+neg

def valid(F):
    n=max(abs(x) for C in F for x in C)
    counts=Counter(x for C in F for x in C)
    return (n%3==0 and len(F)*3==4*n and
            len({tuple(sorted(C)) for C in F})==len(F) and
            all(len(C)==len(set(map(abs,C)))==3 and
                (all(x>0 for x in C) or all(x<0 for x in C))
                for C in F) and
            all(counts[i]==counts[-i]==2 for i in range(1,n+1)))

def models(F):
    n=max(abs(x) for C in F for x in C)
    return [S for mask in range(1<<n)
            if all(any(((mask>>(abs(x)-1))&1)==int(x>0) for x in C)
                   for C in F)
            for S in [set(i+1 for i in range(n) if mask&(1<<i))]]

def perfect_matchings(edges):
    vertices=set().union(*(set(ab) for ab in edges))
    n=len(edges)
    result=[]
    for selected in itertools.combinations(range(1,n+1),len(vertices)//2):
        used=[]
        for e in selected:
            used.extend(edges[e-1])
        if len(used)==len(vertices) and len(set(used))==len(vertices):
            result.append(set(selected))
    return result

def q(F,edges):
    neg=[tuple(abs(x) for x in C) for C in F if C[0]<0]
    return sum(all(set(edges[i-1]).isdisjoint(edges[j-1])
                   for i,j in itertools.combinations(C,2))
               for C in neg)

def one_side(F,edges):
    dangers=[tuple(abs(x) for x in C) for C in F if C[0]<0
             and all(set(edges[i-1]).isdisjoint(edges[j-1])
                     for i,j in itertools.combinations(map(abs,C),2))]
    if len(dangers)>2:return None
    forbidden={C[0] for C in dangers}
    choices=[M for M in perfect_matchings(edges) if not(M&forbidden)]
    assert choices, "The bridgeless-two-edge conclusion failed"
    for M in choices:
        if all(any(((i in M) if x>0 else (i not in M))
                   for x in C for i in [abs(x)]) for C in F):
            return M
    raise AssertionError("A matching did not satisfy original clauses")

def run():
    k4=list(itertools.combinations(range(4),2))
    p4=[tuple(i+1 for i,ab in enumerate(k4) if v in ab) for v in range(4)]
    K4=from_graph(k4,p4)
    prism=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),
           (0,3),(1,4),(2,5)]
    prism_q2=[(1,3,6),(1,2,3),(4,5,9),
              (4,6,8),(7,8,9),(2,5,7)]
    prism_F=from_graph(prism,prism_q2)
    k33=[(r,3+c) for r in range(3) for c in range(3)]
    plus33=[tuple(i+1 for i,ab in enumerate(k33) if v in ab)
            for v in range(6)]
    pm33=[tuple(sorted(M)) for M in perfect_matchings(k33)]
    F33=from_graph(k33,pm33)
    for name,edges,F,expected in [
        ("nonbipartite_K4",k4,K4,18),
        ("nonbipartite_PRISM_Q2",prism,prism_F,68),
        ("all_six_K33_SAT_NO_SAFE_PM",k33,F33,18)]:
        assert valid(F),(name,"invalid M22")
        P=perfect_matchings(edges)
        assert P
        if name!="all_six_K33_SAT_NO_SAFE_PM":
            assert q(F,edges)<=2
            for forbidden in itertools.combinations(range(1,len(edges)+1),2):
                assert any(not(set(forbidden)&M) for M in P)
            M=one_side(F,edges)
            assert M is not None
        else:
            assert all(any(set(map(abs,C))<=M for C in F if C[0]<0)
                       for M in P)
            assert q(F,edges)==6
        count=len(models(F))
        assert count==expected,(name,count,expected)
        print(name,"n=",len(edges),"m=",len(F),"q=",q(F,edges),
              "perfect_matchings=",len(P),"SAT_models=",count)
    print("PASS: finite original-source both-sign controls; no general SAT claim")

if __name__=="__main__":
    run()
