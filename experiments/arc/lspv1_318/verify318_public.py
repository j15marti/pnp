#!/usr/bin/env python3
"""Independent, no-producer-import source-bit verifier for LSPV-1 318."""
from itertools import product
from collections import Counter
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))

def checked(a):
    return all(any(a[i] for i in C) for C in P) and all(any(not a[i] for i in C) for C in N)
def score(p):
    counts=Counter(); contradictions=0
    for sign,blocks in ((1,P),(0,N)):
        for C in blocks:
            if any(i in p and p[i]==sign for i in C):counts[0]+=1
            else:
                k=sum(i not in p for i in C)
                counts[k]+=1
                contradictions+=(k==0)
    return counts,contradictions,sum(k*v for k,v in counts.items())
def completions(p):
    free=[x for x in range(1,10) if x not in p];yes=[];cover=Counter()
    for row in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,row))}
        if checked(a):yes.append(tuple(a[i] for i in range(1,10)))
        else:
            for j,C in enumerate(P,1):
                if not any(a[i] for i in C):cover[j]+=1;break
            else:
                for j,C in enumerate(N,7):
                    if not any(not a[i] for i in C):cover[j]+=1;break
    return yes,cover

base={2:0,3:0,6:1};sat={**base,7:1};unsat={**base,7:0}
assert len(completions({})[0])==70
assert [len(completions(p)[0]) for p in (base,sat,unsat)]==[1,1,0]
assert completions(sat)[0][0]==(0,0,0,0,1,1,1,1,0)
assert completions(unsat)[1]==Counter({2:16,3:4,5:6,7:6})
assert score(sat)==score(unsat)==(Counter({0:7,1:2,2:3}),0,8)
assert score(base)==(Counter({0:5,1:1,2:4,3:2}),0,15)
for i in range(1,10):
    for b in (0,1):
        assert score({i:b})==(Counter({0:2,2:2,3:8}),0,28)
assert all(sum((a[i] if sg else not a[i]) for i in c)+sum(((1-a[i]) if sg else a[i]) for i in c)==3
           for a in (dict(zip(range(1,10),row)) for row in product((0,1),repeat=9))
           for sg,blocks in ((1,P),(0,N)) for c in blocks)
print('NO-IMPORT PASS: 70 original models; 1/0 residuals; matching 7/7 private gates; 32 original-source UNSAT leaves; 18 first cofactors; 6144 complement identities; P versus NP OPEN')
