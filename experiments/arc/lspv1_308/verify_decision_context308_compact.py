#!/usr/bin/env python3
"""Independent no-import source enumeration for LSPV-1 CONTINUATION308."""
from itertools import product
from collections import Counter
P=["156","238","135","469","247","789"]
N=["468","167","234","358","129","579"]
K=(1,2,3,4,8)
X=(0,0,0,0,1);Y=(0,0,0,1,1);C=(0,0,1,0,1)
cs=[]
for i in range(2):
 for j,row in enumerate(P):
  cs.append(tuple(9*((i+1)%2)+5 if j==0 and int(k)==5 else 9*i+int(k) for k in row))
 for row in N:cs.append(tuple(-(9*i+int(k)) for k in row))
assert len(cs)==24 and len({tuple(sorted(c)) for c in cs})==24
counts=Counter((abs(z),z>0) for cl in cs for z in cl)
assert all(counts[(i,sign)]==2 for i in range(1,19) for sign in (0,1))
def test(a,b):
 pin={}
 for block,values in enumerate((a,b)):
  if values is not None:pin.update({9*block+k:v for k,v in zip(K,values)})
 free=[i for i in range(1,19) if i not in pin]
 hits=0;bad=0
 for bits in product((0,1),repeat=len(free)):
  d=dict(pin);d.update(zip(free,bits))
  falsified=[j for j,cl in enumerate(cs) if all(d[abs(z)]!=int(z>0) for z in cl)]
  if falsified:bad+=1
  else:hits+=1
 assert hits+bad==2**len(free)
 return hits,bad
assert test(X,None)[0]==83
assert test(Y,None)[0]==108
assert test(X,C)[0]==3
assert test(Y,C)==(0,256)
print("PASS independent original-source SAT and UNSAT (83,108,3,0), 256 complete falsified-clause leaves")
