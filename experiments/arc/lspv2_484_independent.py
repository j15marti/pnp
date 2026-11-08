#!/usr/bin/env python3
"""Independent symbolic/source audit for LSPV-2/484; not native FLMV."""
from fractions import Fraction
from itertools import product
import json
EDGES=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
checks=0
def cnf(charge,t):
    cs=[]
    for vertex in range(4):
        ids=[i+1 for i,p in enumerate(EDGES) if vertex in p]
        assert len(ids)==3
        for b in product((0,1),repeat=3):
            if (b[0]^b[1]^b[2])!=charge[vertex]:
                cs.append(tuple(x if not val else -x for x,val in zip(ids,b)))
    cs.extend((7+3*i,8+3*i,9+3*i) for i in range(t))
    return (6+3*t,tuple(cs))
def model_count(f):
    n,cs=f;count=0
    for a in product((0,1),repeat=n):
        if all(any(a[abs(x)-1]==int(x>0) for x in cl) for cl in cs):count+=1
    return count
def gamma_len(x):return 2*(x.bit_length()-1)+1
def size_bits(f):
    n,cs=f
    w=n.bit_length()
    return gamma_len(n+1)+gamma_len(len(cs)+1)+3*len(cs)*(1+w)
for t in range(3):
    selected=set()
    for mask in range(16):
        charge=tuple((mask>>i)&1 for i in range(4))
        f=cnf(charge,t)
        assert len(f[1])==16+t
        assert model_count(f)==(0 if sum(charge)%2 else 8*7**t)
        checks+=2
        if charge==(1,0,0,0):selected.add(f)
    assert len(selected)==1
    anchor=next(iter(selected))
    for mask in range(8**t):
        cs=list(anchor[1]);q=mask
        for j in range(t):
            pattern=q%8;q//=8;b=cs[16+j]
            cs[16+j]=tuple(-abs(z) if (pattern>>i)&1 else abs(z) for i,z in enumerate(b))
        assert size_bits((anchor[0],tuple(cs)))==size_bits(anchor)
        checks+=1
    checks+=1
for k in (2,3,4,8,16):
    tg=max(Fraction(11,10),Fraction(3,5)+Fraction(k,2))
    sg=max(Fraction(1,2),Fraction(k,2))
    assert Fraction(k)>tg and Fraction(k)>sg
    assert Fraction(k,2)<=sg and Fraction(3,5)+Fraction(k,2)<=tg
    checks+=4
print(json.dumps({'role':'LSPV-2/484','checks':checks,'signedCNFTests':48,'SATTests':24,'UNSATTests':24,'countBySideGadget':[8,56,392],'formalSATinP':'conditional only','nativeFLMV':False,'proofStatus':'PROVED/RESTRICTED; OPEN'},indent=2))