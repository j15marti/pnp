#!/usr/bin/env python3
"""Exact minimum tree-like resolution refutation size (= minimum DPLL decision-tree
size) for small UNSAT CNFs, compared with an F2 Gaussian-elimination certificate
cost for XOR-structured (Tseitin) families.

Measure: S_tree(F) = number of leaves of a minimum DPLL tree (each leaf falsifies a
clause of F). A minimum tree-like resolution refutation has exactly S_tree leaves
(axiom occurrences) and S_tree-1 resolution steps (Beame-Pitassi / folklore
equivalence: tree-like resolution <-> DPLL trees; minimum may be taken regular).
The optimal branching sequence is chosen FREE (min over all trees), matching the
directive's "free knowledge of the best sequence" convention.

Usage: python3 wcd_treeres.py <family> <param>   (each call < ~30 s)
Deterministic; no randomness except 'rand3' which takes seed explicitly.
"""
import sys, json, itertools, random, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j) = i*m+j+1
    cls=[]
    for i in range(m+1): cls.append(tuple(i*m+j+1 for j in range(m)))
    for j in range(m):
        for a in range(m+1):
            for b in range(a+1,m+1): cls.append((-(a*m+j+1),-(b*m+j+1)))
    return (m+1)*m, cls

def tseitin(edges, nverts, odd_vertex=0):
    # variable per edge; vertex parity charge 1 at odd_vertex only -> total odd -> UNSAT
    cls=[]; rows=[]
    for v in range(nverts):
        inc=[e+1 for e,(a,b) in enumerate(edges) if v in (a,b)]
        c = 1 if v==odd_vertex else 0
        rows.append((inc,c))
        for bits in itertools.product([0,1],repeat=len(inc)):
            if sum(bits)%2 != c:  # forbid this assignment
                cls.append(tuple(x if b==0 else -x for x,b in zip(inc,bits)))
    return len(edges), cls, rows

def circulant3(n):  # 3-regular: cycle + diameters (n even)
    E=set()
    for i in range(n):
        E.add(tuple(sorted((i,(i+1)%n)))); E.add(tuple(sorted((i,(i+n//2)%n))))
    return sorted(E)

def rand3(n,m,seed):
    r=random.Random(seed); cls=[]
    while len(cls)<m:
        vs=r.sample(range(1,n+1),3); cls.append(tuple(v if r.random()<.5 else -v for v in vs))
    return n,cls

def min_tree(nvars, clauses):
    clauses=[frozenset(c) for c in clauses]
    @lru_cache(maxsize=None)
    def S(asg):  # asg: frozenset of true literals
        live=[]
        for c in clauses:
            if any(l in asg for l in c): continue
            rest=frozenset(l for l in c if -l not in asg)
            if not rest: return 1   # falsified clause -> leaf
            live.append(rest)
        if not live: return None    # satisfiable branch (should not occur for UNSAT)
        # unit propagation is NOT free in tree-like resolution; branch on every var
        vars_=set(abs(l) for c in live for l in c)
        best=None
        for x in vars_:
            a=S(asg|{x}); 
            if a is None: continue
            if best is not None and a>=best: continue
            b=S(asg|{-x})
            if b is None: continue
            if best is None or a+b<best: best=a+b
        return best
    t=time.time(); v=S(frozenset()); return v, S.cache_info().currsize, time.time()-t

def gauss_cost(rows, nvars):
    # F2 row-reduction of the parity system; cost = number of row XOR operations,
    # each on a (nvars+1)-bit row: work = ops*(nvars+1) bit operations.
    R=[(sum(1<<(x-1) for x in inc), c) for inc,c in rows]; ops=0; piv=0
    R=[list(r) for r in R]
    for col in range(nvars):
        p=next((i for i in range(piv,len(R)) if R[i][0]>>col&1),None)
        if p is None: continue
        R[piv],R[p]=R[p],R[piv]
        for i in range(len(R)):
            if i!=piv and R[i][0]>>col&1:
                R[i][0]^=R[piv][0]; R[i][1]^=R[piv][1]; ops+=1
        piv+=1
    contradiction=any(r[0]==0 and r[1]==1 for r in R)
    return ops, ops*(nvars+1), contradiction

if __name__=="__main__":
    fam=sys.argv[1]; p=int(sys.argv[2]); out={"family":fam,"param":p}
    if fam=="php":
        n,cls=php(p)
    elif fam=="tseitin":
        E=circulant3(p); n,cls,rows=tseitin(E,p)
        out["gauss_row_ops"],out["gauss_bit_ops"],out["gauss_refutes"]=gauss_cost(rows,n)
    elif fam=="rand3":
        seed=int(sys.argv[3]); n,cls=rand3(p,int(round(6*p)),seed); out["seed"]=seed
    out["nvars"]=n; out["nclauses"]=len(cls)
    out["encoded_size_literals"]=sum(len(c) for c in cls)
    v,memo,dt=min_tree(n,cls)
    out["min_tree_leaves"]=v; out["memo_states"]=memo; out["seconds"]=round(dt,3)
    print(json.dumps(out))
