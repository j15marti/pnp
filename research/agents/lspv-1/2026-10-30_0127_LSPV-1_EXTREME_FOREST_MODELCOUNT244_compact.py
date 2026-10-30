#!/usr/bin/env python3
"""Independent standard-library check of LSPV-1 EXTREME-FOREST-MODELCOUNT244.
Original source clauses, shared original variables, exact arithmetic.
Run: python 2026-10-30_0127_LSPV-1_EXTREME_FOREST_MODELCOUNT244_compact.py
This checks the sharp n=6 instance; the expanded eleven-family search/work
audit is in the local reproducibility bundle, not reconstructed here.
"""
import json
from fractions import Fraction
from itertools import combinations
C = [
    (-1,2,-5), (-3,-2,-5), (1,-6,-4), (6,-3,5),
    (6,3,-4), (1,2,4), (-6,-1,5), (-2,3,4)
]
n = 6
forest = [(0,4), (1,2), (3,5), (6,7)]
def val(lit, a):
    bit = (a >> (abs(lit)-1)) & 1
    return bool(bit) if lit>0 else not bit
def counts(a):
    t = [sum(val(l,a) for l in c) for c in C]
    return t,[t.count(r) for r in range(4)]
def needs(c, mode):
    return {abs(l): int(l>0) ^ int(mode=="U") for l in c}
def merge(a,b):
    if any(v in a and a[v]!=x for v,x in b.items()):
        return None
    return {**a, **b}
def compat(j,k,mode):
    return merge(needs(C[j],mode[0]),needs(C[k],mode[1])) is not None
def brute_pair(j,k,mode):
    def hits(a,j,m):
        return sum(val(l,a) for l in C[j]) == (3 if m=="S" else 0)
    return any(hits(a,j,mode[0]) and hits(a,k,mode[1]) for a in range(64))
def event_prob(source_ids, pinned):
    demand = {}
    for j in source_ids:
        demand=merge(demand,needs(C[j],"U"))
        if demand is None: return Fraction(0)
    demand=merge(pinned,demand)
    if demand is None: return Fraction(0)
    original=dict(pinned)
    return Fraction(1,2**(len(demand)-len(original)))
def forest_bound(pinned):
    return (Fraction(1)
        -sum((event_prob((j,),pinned) for j in range(len(C))),Fraction(0))
        +sum((event_prob((j,k),pinned) for j,k in forest),Fraction(0)))
def model_from_forest():
    rho={}
    assert forest_bound(rho)==Fraction(1,16)
    trace=[]
    for i in range(1,n+1):
        b0=forest_bound({**rho,i:0})
        b1=forest_bound({**rho,i:1})
        assert 2*forest_bound(rho)==b0+b1
        x=0 if b0>0 else 1
        assert (b0 if x==0 else b1)>0
        rho[i]=x
        trace.append({"original_variable":i,"chosen":x,
                      "forest_B0":str(b0),"forest_B1":str(b1)})
    a=sum(bit<<(i-1) for i,bit in rho.items())
    assert counts(a)[1][0]==0
    return a,trace
assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in C)
for i in range(1,7):
    assert sum(l==i for c in C for l in c)==2
    assert sum(l==-i for c in C for l in c)==2
records=[]
for j,c in enumerate(C):
    occ=[]
    for l in c:
        S=int(l>0)
        U=1-S
        occ.append({"source_clause":j, "source_signed_occurrence":l,
           "source_variable":abs(l),"S_all_literals_TRUE":S,
           "inverted_S_is_U":1-S,"U_all_literals_FALSE":U,
           "inverted_U_is_S":1-U})
    records.append({"source_clause":j,"signed_literals":c,
      "per_occurrence_targets":occ,
      "local_S":needs(c,"S"),"local_U":needs(c,"U")})
pairs=[]
nonconf=[]
for j,k in combinations(range(8),2):
    matrix={m:compat(j,k,m) for m in ("SS","SU","US","UU")}
    for m,v in matrix.items(): assert v==brute_pair(j,k,m)
    if matrix["UU"]: nonconf.append((j,k))
    pairs.append({"original_source_clause_indices":[j,k],**matrix})
assert nonconf==forest
models=[a for a in range(64) if counts(a)[1][0]==0]
assert models==[1,28,38,59]
all_counts={}
for a in range(64):
    t,v=counts(a)
    tc,vc=counts(a^63)
    assert tc==[3-x for x in t]
    assert vc==v[::-1]
    for flip in range(64):
        other,_=counts(a^flip)
        expected=[]
        for c in C:
            falseflips=sum(((flip>>(abs(l)-1))&1) for l in c if not val(l,a))
            trueflips=sum(((flip>>(abs(l)-1))&1) for l in c if val(l,a))
            expected.append(sum(val(l,a) for l in c)+falseflips-trueflips)
        assert other==expected
for a in [0,63,1,3,7,31,32]:
    all_counts[str(a)]={"true_literal_counts":counts(a)[0],
                        "N0_N1_N2_N3":counts(a)[1],
                        "SAT":counts(a)[1][0]==0,
                        "complement":a^63}
assert counts(0)[1]==counts(63)[1]==[1,3,3,1]
assert counts(1)[1]==[0,6,0,2]
witness,path=model_from_forest()
# C0 (+x2) and C1 (-x2) imply (-x1 or -x3 or -x5):
assert 2 in C[0] and -2 in C[1]
resolvent=set(C[0]+C[1])-{2,-2}
assert resolvent=={-1,-3,-5}
for a in range(64):
    if all(((a>>(i-1))&1)==1 for i in (1,3,5)):
        assert not all(any(val(l,a) for l in c) for c in C[:2])
out={"status":"COMPUTATIONAL independent sharp-instance checker",
     "original_source_S_U_targets":records,
     "source_indexed_pair_SS_SU_US_UU":pairs,
     "UU_nonconflict_graph_edges":nonconf,
     "n":n,"m":len(C),"exact_models_as_bit_masks":models,
     "Hunter_forest_lower_bound":str(forest_bound({})),
     "count_guarantee":4,
     "coherent_endpoints_and_flip_trail":all_counts,
     "constructive_witness_mask":witness,
     "conditional_forest_path":path,
     "prohibited_cube":{"source_parent_indices":[0,1],"pivot":2,
         "non_tautological_resolvent":sorted(resolvent),
         "excluded_original_variable_assignments":{"1":1,"3":1,"5":1}},
     "scope":"sharp n6 only; main run and charged work in complete bundle",
     "P_vs_NP":"OPEN"}
print(json.dumps(out,indent=2))
