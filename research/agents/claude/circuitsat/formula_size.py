"""Exact leaf-size L(f) of De Morgan formulas (AND/OR, free negation on edges)
for all Boolean functions on n<=4 variables, by Dijkstra-like closure over leaf counts.
Wires of a formula with L leaves: 2(L-1) gate-input wires (tree, fan-out 1) + L leaf wires = counted as 'edges' E=2L-2.
Runs well under 30 s for n<=4."""
import sys, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
var=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
L={}
lvl={}
for v in var:
    for f in (v, M^v): L[f]=1; lvl.setdefault(1,[]).append(f)
for k in range(2,40):
    new=[]
    for a in range(1,k//2+1):
        b=k-a
        for f in lvl.get(a,[]):
            for g in lvl.get(b,[]):
                for h in (f&g, f|g):
                    if h not in L and h not in (0,M):
                        L[h]=k; new.append(h)
    for h in new:
        if (M^h) not in L and (M^h) not in (0,M): L[M^h]=k; new.append(M^h)
    lvl[k]=new
    if len(L)==(1<<N)-2+2 and False: break
    if len(L)>=(1<<N)-2: break
# constants need no leaves; skip
vals=[L[f] for f in L]
mx=max(vals)
hist={}
for f,l in L.items(): hist[l]=hist.get(l,0)+1
# hardest = max over functions of L; also max L among functions with exactly 1 satisfying assignment, and parity
par=0
for a in range(N):
    if bin(a).count('1')%2: par|=1<<a
print(json.dumps({"n":n,"nonconst_functions":len(L),"max_leaves":mx,"hist":dict(sorted(hist.items())),
 "parity_leaves":L[par],"unique_sat_max_leaves":max(l for f,l in L.items() if bin(f).count('1')==1)}))
