#!/usr/bin/env python3
"""Exact minimum DAG-resolution refutation length (# derived clauses) for tiny UNSAT CNFs.
BFS over sets of derived clauses (dedupe by frozenset) = free-knowledge optimal derivation.
Each run is time-capped (<30s); instances chosen small. Usage: minres.py NAME"""
import sys, time, itertools
def resolvents(c1,c2):
    out=[]
    for l in c1:
        if -l in c2:
            r=(c1-{l})|(c2-{-l})
            if any(-x in r for x in r): continue
            out.append(frozenset(r))
    return out
def php(n):  # n+1 pigeons, n holes ; var p(i,j)=i*n+j+1
    v=lambda i,j:i*n+j+1
    cl=[frozenset(v(i,j) for j in range(n)) for i in range(n+1)]
    for j in range(n):
        for i in range(n+1):
            for k in range(i+1,n+1): cl.append(frozenset({-v(i,j),-v(k,j)}))
    return cl
def tseitin_cycle(n):  # odd-charged cycle C_n: unsat, edge vars e_i; vertex i: e_{i-1} xor e_i = charge
    cl=[]
    for i in range(n):
        a=(i-1)%n+1; b=i+1; ch=1 if i==0 else 0
        for sa in (0,1):
            for sb in (0,1):
                if (sa^sb)!=ch:  # forbid assignment with wrong parity
                    cl.append(frozenset({(-a if sa else a),(-b if sb else b)}))
    return cl
INST={'php2':php(2),'cycle3':tseitin_cycle(3),'cycle4':tseitin_cycle(4),'cycle5':tseitin_cycle(5)}
def run(name,limit=25):
    F=list(set(INST[name])); base=frozenset(F); t0=time.time()
    seen={frozenset()}; level=[frozenset()]; d=0
    while level:
        if time.time()-t0>limit: return (name,None,d,len(seen),'timeout')
        nxt=[]
        for S in level:
            allc=list(base|S)
            for c1,c2 in itertools.combinations(allc,2):
                for r in resolvents(c1,c2):
                    if r in base or r in S: continue
                    if not r: return (name,d+1,d+1,len(seen),'ok')
                    T=S|{r}
                    if T not in seen: seen.add(T); nxt.append(T)
        level=nxt; d+=1
    return (name,None,d,len(seen),'exhausted')
if __name__=='__main__':
    print(run(sys.argv[1]))
