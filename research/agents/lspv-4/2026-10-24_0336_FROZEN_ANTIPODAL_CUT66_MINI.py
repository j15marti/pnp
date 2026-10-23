#!/usr/bin/env python3
"""FROZEN-ANTIPODAL-CUT66 minimal independent standard-library reproducer."""
from itertools import product, combinations

H=[(0,1,2),(0,3,4),(1,3,5),(2,4,5),
   (3,4,5),(1,2,5),(0,2,4),(0,1,3)]
E=[(v,c) for c,C in enumerate(H) for v in C]
n,m=6,8
assert len(E)==24 and all(sum(v in C for C in H)==4 for v in range(n))
incident=[[i for i,(u,c) in enumerate(E) if u==v] for v in range(n)]
byclause=[[i for i,(v,d) in enumerate(E) if c==d] for c in range(m)]
options=[[sum(1<<i for i in pair) for pair in combinations(incident[v],2)]
         for v in range(n)]
balanced=0; nae=[]
for pieces in product(*options):
    signmask=0
    for piece in pieces: signmask|=piece
    balanced+=1
    if all(1<=sum(bool(signmask&(1<<i)) for i in byclause[c])<=2
           for c in range(m)):
        nae.append(signmask)
assert balanced==6**6==46656
assert len(nae)==5904
# Fixed truth values on named 0-based flattened occurrence sockets.
pins={2:1,3:1,6:1,15:0,18:0,21:0,22:0}
assert len(pins)==7
# Every single variable quota is locally feasible.
for v in range(n):
    p=sum(pins[i] for i in incident[v] if i in pins)
    f=sum(i not in pins for i in incident[v])
    assert 0<=2-p<=f
# Every single clause range is locally feasible.
for c in range(m):
    p=sum(pins[i] for i in byclause[c] if i in pins)
    f=sum(i not in pins for i in byclause[c])
    assert max(0,1-p)<=min(f,2-p)
pm=sum(1<<i for i,val in pins.items() if val)
zm=sum(1<<i for i,val in pins.items() if not val)
assert not any((s&pm)==pm and (s&zm)==0 for s in nae)
# Hoffman cut: X={0,1}, Y={C0}; supplies two and capacity one.
X={0,1};Y={0}
R=sum(2-sum(pins[i] for i in incident[v] if i in pins) for v in X)
out=sum(i not in pins and v in X and c not in Y for i,(v,c) in enumerate(E))
pc=sum(pins[i] for i in byclause[0] if i in pins)
fc=sum(i not in pins for i in byclause[0])
U=min(fc,2-pc)
assert (R,out,U)==(2,0,1) and R>out+U
print({"balanced_signings":balanced,"two_witness_signings":len(nae),
       "local_tests":"PASS","global_completion":"INFEASIBLE",
       "violated_cut":[R,out,U],"checks":"PASS"})
