#!/usr/bin/env python3
"""Exact minimum TREE-like resolution refutation size (= min refuting decision tree nodes)
for small UNSAT CNFs, by DP over partial assignments. COMPUTATIONAL only; tree-like, not DAG.
Each invocation targets <30s; families are chunked by CLI arg."""
import sys, json, random, itertools, time
from functools import lru_cache

def tree_size(nvars, clauses):
    # clause: tuple of nonzero ints. state: tuple of 0/1/2 per var (2=unset) -> encoded int base 3
    cl = [tuple(c) for c in clauses]
    @lru_cache(maxsize=None)
    def T(state):
        a = state
        for c in cl:
            if all(a[abs(l)-1] != 2 and (a[abs(l)-1] == (0 if l > 0 else 1)) for l in c):
                return 1  # clause falsified: leaf
        best = None
        for v in range(nvars):
            if a[v] == 2:
                s0 = a[:v]+(0,)+a[v+1:]; s1 = a[:v]+(1,)+a[v+1:]
                t = T(s0)+T(s1)+1
                if best is None or t < best: best = t
        if best is None: return 10**9  # total assignment satisfying: formula SAT
        return best
    return T(tuple([2]*nvars))

def php(n):  # n+1 pigeons, n holes
    v = lambda p,h: p*n+h+1
    cls = [[v(p,h) for h in range(n)] for p in range(n+1)]
    for h in range(n):
        for p in range(n+1):
            for q in range(p+1,n+1): cls.append([-v(p,h),-v(q,h)])
    return (n+1)*n, cls

def tseitin_cycle_k(k):  # odd Tseitin on cycle C_k doubled? use cycle with 1 charged vertex
    # edges e_i between vertex i and i+1; vertex i parity of (e_{i-1}, e_i) = charge_i
    cls=[]
    for i in range(k):
        a=(i-1)%k+1; b=i+1; charge = 1 if i==0 else 0
        for sa in (0,1):
            for sb in (0,1):
                if (sa+sb)%2 != charge:  # forbid wrong parity assignment
                    cls.append([(-a if sa else a),(-b if sb else b)])
    return k, cls

def rand3(n, m, rng):
    cls=[]
    for _ in range(m):
        vs = rng.sample(range(1,n+1),3)
        cls.append([v if rng.random()<.5 else -v for v in vs])
    return n, cls

def sat(n, cls):
    for bits in range(1<<n):
        if all(any(((bits>>(abs(l)-1))&1)==(1 if l>0 else 0) for l in c) for c in cls): return True
    return False

if __name__=="__main__":
    fam = sys.argv[1]; out=[]; t0=time.time()
    if fam=="php":
        for n in (1,2,3):
            nv,c = php(n); out.append(dict(family="PHP",n=n,vars=nv,clauses=len(c),tree_res=tree_size(nv,c)))
    elif fam=="tseitin":
        for k in (3,5,7,9):
            nv,c=tseitin_cycle_k(k); out.append(dict(family="TseitinCycle",k=k,vars=nv,clauses=len(c),tree_res=tree_size(nv,c)))
    elif fam.startswith("rand"):
        n=int(fam[4:]); rng=random.Random(2026110700+n); vals=[]; cnt=0
        while cnt<12:
            m=int(6.0*n); nv,c=rand3(n,m,rng)
            if sat(nv,c): continue
            vals.append(tree_size(nv,c)); cnt+=1
        out.append(dict(family="rand3CNF_m=6n",n=n,samples=len(vals),max=max(vals),min=min(vals),mean=sum(vals)/len(vals)))
    print(json.dumps(out)); sys.stderr.write(f"{fam} {time.time()-t0:.1f}s\n")
