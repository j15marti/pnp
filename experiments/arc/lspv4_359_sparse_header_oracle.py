#!/usr/bin/env python3
"""LSPV-4 SPARSE-HEADER-ORACLE-AUDIT359.
Standalone standard-library controls. Run: python lspv4_359_sparse_header.py
This is a finite semantic oracle emulator, not a physical TQBF oracle.
Full DP proof DAGs, signed witnesses and independent JS verifier are in the ZIP.
"""
from itertools import combinations
import json

def parse(s):
    rows=s.splitlines()
    if not rows: raise ValueError("empty source")
    h=rows[0].split()
    if len(h)!=4 or h[:2]!=["p","cnf"] or not all(v.isdecimal() for v in h[2:]):
        raise ValueError("header")
    n,m=map(int,h[2:])
    if len(rows)!=m+1: raise ValueError("clause count")
    C=[]
    for row in rows[1:]:
        v=row.split()
        if not v or v[-1]!="0" or "0" in v[:-1]: raise ValueError("termination")
        try: c=tuple(map(int,v[:-1]))
        except ValueError: raise ValueError("literal")
        if any(not x or abs(x)>n for x in c): raise ValueError("range")
        C.append(c)
    return n,C

def query(s):
    _,C=parse(s)
    rank={}
    for c in C:
        for l in c:
            rank.setdefault(abs(l),len(rank)+1)
    prefix="exists "+",".join("x"+str(i) for i in range(1,len(rank)+1))+" : " if rank else ""
    mat=" & ".join("("+" | ".join(("~" if l<0 else "")+"x"+str(rank[abs(l)]) for l in c)+")" if c else "(false)" for c in C) if C else "(true)"
    return prefix+"("+mat+")"

def php(k):
    ix=lambda p,h: p*k+h+1
    C=[tuple(ix(p,h) for h in range(k)) for p in range(k+1)]
    C += [(-ix(p,h),-ix(q,h)) for h in range(k)
          for p,q in combinations(range(k+1),2)]
    return k*(k+1),C

def sat(C,a):
    return all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in c) for c in C)

def first_model(C,n):
    for a in range(1<<n):
        if sat(C,a): return a
    return None

out={"run":"LSPV4_SPARSE_HEADER_ORACLE_AUDIT359","php":[],"sparse":[]}
for k in (1,2,3):
    n,C=php(k)
    src=f"p cnf {n} {len(C)}\n"+"".join(" ".join(map(str,c))+" 0\n" for c in C)
    assert parse(src)==(n,C)
    assert first_model(C,n) is None
    deletions=0; flips=0
    for j,c in enumerate(C):
        assert first_model(C[:j]+C[j+1:],n) is not None
        deletions+=1
        for h in range(len(c)):
            D=C.copy(); t=list(c); t[h]=-t[h]; D[j]=tuple(t)
            assert first_model(D,n) is not None
            flips+=1
    out["php"].append({"holes":k,"variables":n,"clauses":len(C),
                       "source_bytes":len(src),"QBF_bytes":len(query(src)),
                       "source_deletions_SAT":deletions,"literal_flips_SAT":flips})
for src,want in [
    ("p cnf 1000000000 0\n",True),
    ("p cnf 1000000000 1\n1000000000 0\n",True),
    ("p cnf 1000000000 2\n1000000000 0\n-1000000000 0\n",False)]:
    n,C=parse(src); rank={abs(l) for c in C for l in c}
    assert n==10**9
    Q=query(src)
    assert len(Q)<4*len(src)
    assert want == (not C or (len(C)==1 and C[0][0]>0))
    out["sparse"].append({"source_bytes":len(src),"query_bytes":len(Q),
                          "appearing_variables":len(rank),"SAT":want,"query":Q})
malformed=["","p cfn 1 1\n1 0\n","p cnf -1 0\n",
           "p cnf 1 1\n2 0\n","p cnf 1 1\n1\n",
           "p cnf 1 2\n1 0\n","p cnf 1 1\n1 0\n-1 0\n",
           "p cnf 1 one\n1 0\n","p cnf 1 1\n1 0 0\n",
           "p cnf 1 1\n1 x 0\n"]
reject=0
for s in malformed:
    try: parse(s)
    except ValueError: reject+=1
assert reject==len(malformed)
out["malformed_rejected"]=reject
out["proof_status"]="FINITE CONTROLS; oracle model theorem requires Haken and PSPACE completeness"
print(json.dumps(out,indent=2))
