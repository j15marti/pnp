#!/usr/bin/env python3
"""LSPV-3/395 independent Python recomputation; no dependency on JS producer."""
from itertools import combinations

def source(h):
    clauses = []
    for pigeon in range(h + 1):
        clauses.append(tuple(pigeon*h + hole + 1 for hole in range(h)))
    for hole in range(h):
        for p,q in combinations(range(h+1), 2):
            clauses.append((-(p*h+hole+1), -(q*h+hole+1)))
    return h*(h+1),clauses

def satisfies(n, clauses):
    for a in range(1 << n):
        good = True
        for clause in clauses:
            if not any(bool(a & (1 << (abs(lit)-1))) == (lit > 0) for lit in clause):
                good = False
                break
        if good:
            return a
    return None

def min_core(n, clauses):
    for size in range(1,len(clauses)+1):
        for idx in combinations(range(len(clauses)),size):
            if satisfies(n,[clauses[i] for i in idx]) is None:
                return tuple(idx)
    raise AssertionError("Expected UNSAT core")

def run():
    out=[]
    for h in range(1,4):
        n,f=source(h)
        assert satisfies(n,f) is None
        assert all(satisfies(n,f[:i]+f[i+1:]) is not None for i in range(len(f)))
        g=f+[(n+1,),(-(n+1),)]
        assert satisfies(n+1,g) is None
        assert all(len(c)>0 for c in g)
        assert g[-1][0] == -g[-2][0]
        if h <= 2:
            k=len(min_core(n,f)); j=len(min_core(n+1,g))
            assert k==len(f) and j==2
        else:
            k=None;j=2
        out.append({"holes":h,"m":len(f),"original_min_core":k,
                    "augmented_min_core":j,"augmented_paid_inferences":1})
    for h in (1,2):
        n,f=source(h)
        plus=f+[(n+1,),(-(n+1),)]
        assert not any(not c for c in plus)
        assert all(satisfies(n+1,[c]) is not None for c in plus)
    return out

if __name__=="__main__":
    import json
    print(json.dumps(run(),indent=2))
