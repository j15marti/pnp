"""Exact minimum tree-like Resolution refutation size (= min decision-tree size
for the false-clause search problem) for small UNSAT CNFs.  COMPUTATIONAL only.
Usage: python3 treeres_exact.py [family] ; each invocation designed for < 30 s."""
import sys, json, itertools, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes
    v = {}
    for p in range(m+1):
        for h in range(m):
            v[(p,h)] = len(v)
    cl = [[(v[(p,h)],1) for h in range(m)] for p in range(m+1)]
    for h in range(m):
        for p,q in itertools.combinations(range(m+1),2):
            cl.append([(v[(p,h)],0),(v[(q,h)],0)])
    return len(v), cl

def tseitin_k4_odd():  # K4, all vertex charges odd sum => UNSAT
    E = list(itertools.combinations(range(4),2)); idx = {e:i for i,e in enumerate(E)}
    cl = []
    for u in range(4):
        inc = [idx[e] for e in E if u in e]; chg = 1 if u==0 else 0
        for bits in itertools.product([0,1], repeat=3):
            if sum(bits)%2 != chg:   # forbid assignment 'bits'
                cl.append([(x,1-b) for x,b in zip(inc,bits)])
    return len(E), cl

def min_tree(n, cl):
    # clause as (mask, valmask): falsified by rho iff all vars assigned and opposite of literal
    C = []
    for c in cl:
        m = 0; val = 0
        for x,pos in c:
            m |= 1<<x
            if not pos: val |= 1<<x   # falsifying value is 1 for negative literal
        C.append((m,val))
    @lru_cache(maxsize=None)
    def S(am, av):
        for m,val in C:
            if (am & m) == m and (av & m) == val:
                return 1
        best = None
        for x in range(n):
            if not (am>>x)&1:
                b = 1 + S(am|1<<x, av) + S(am|1<<x, av|1<<x)
                if best is None or b < best: best = b
        return best
    r = S(0,0); return r, S.cache_info().currsize

def brute_unsat(n, cl):
    for a in range(1<<n):
        if all(any(((a>>x)&1)==pos for x,pos in c) for c in cl): return False
    return True

if __name__ == "__main__":
    fam = sys.argv[1] if len(sys.argv)>1 else "all"
    out = []
    jobs = []
    if fam in ("all","php"): jobs += [("PHP^%d_%d"%(m+1,m), php(m)) for m in (1,2,3)]
    if fam in ("all","tseitin"): jobs += [("Tseitin_K4_odd", tseitin_k4_odd())]
    for name,(n,cl) in jobs:
        t=time.time(); u = brute_unsat(n,cl); s,states = min_tree(n,cl)
        enc_bits = sum(len(c) for c in cl)*(1+max(1,(n-1).bit_length()))
        out.append(dict(name=name, vars=n, clauses=len(cl), approx_bits=enc_bits,
                        unsat=u, min_treelike_size=s, memo_states=states, secs=round(time.time()-t,2)))
        print(out[-1], flush=True)
    json.dump(out, open(sys.argv[2] if len(sys.argv)>2 else "/dev/stdout","w"), indent=1)
