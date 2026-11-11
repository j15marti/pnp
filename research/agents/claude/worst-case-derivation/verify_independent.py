#!/usr/bin/env python3
"""Independent verifier (no import of wbar_exact).  Clauses as frozensets of signed ints.
Checks for every stored class: (1) F is UNSAT and minimally UNSAT by brute force over assignments;
(2) the stored proof is a valid resolution DAG ending in the empty clause with W distinct derived
clauses; (3) no refutation with W-1 derived clauses exists, by an UNPRUNED iterative-deepening search
(no subsumption normalization); (4) the orbit sizes sum to the MU count."""
import json, itertools, sys
def conv(c):
    P,N=c; return frozenset([i+1 for i in range(8) if P>>i&1]+[-(i+1) for i in range(8) if N>>i&1])
def sat(F,n):
    for a in itertools.product((False,True),repeat=n):
        if all(any((l>0)==a[abs(l)-1] for l in c) for c in F): return True
    return False
def res(a,b):
    out=[]
    for l in a:
        if -l in b:
            r=(a|b)-{l,-l}
            if not any(-x in r for x in r): out.append(frozenset(r))
    return out
def exists_le(F,k):
    """Is there a refutation with <= k distinct derived clauses?  Unpruned DFS with memo."""
    src=frozenset(F); seen=set()
    def go(S,k):
        if frozenset() in S: return True
        if k==0 or S in seen: return False
        seen.add(S)
        K=list(S); cand=set()
        for a,b in itertools.combinations(K,2):
            for r in res(a,b):
                if r not in S: cand.add(r)
        if frozenset() in cand: return True
        if k==1: return False
        return any(go(S|{r},k-1) for r in cand)
    return go(src,k)
fails=0; tot=0
for fn in sys.argv[1:]:
    d=json.load(open(fn)); n=d["n"]
    assert sum(r["orbit"] for r in d["rows"])==d["num_MU"] or d["chunk"][1]>1
    for r in d["rows"]:
        F=[conv(c) for c in r["F"]]; W=r["W"]; tot+=1
        ok = not sat(F,n) and all(sat(F[:i]+F[i+1:],n) for i in range(len(F)))
        have=set(F)
        for a,b,c in r["proof"]:
            a,b,c=conv(a),conv(b),conv(c)
            ok &= a in have and b in have and c in res(a,b); have.add(c)
        ok &= frozenset() in have and len(have)-len(set(F))==W==len(r["proof"])
        ok &= (W==0) or not exists_le(F,W-1)
        if not ok: fails+=1; print("FAIL",r)
    print(fn,"classes",len(d["rows"]),"max W",max(x["W"] for x in d["rows"]))
print("checked",tot,"fails",fails)
