#!/usr/bin/env python3
# GATE331: exact original-source F9 cut ranks. Standard library, offline diagnostic.
from collections import Counter
from hashlib import sha256
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=tuple(P)+tuple(tuple(-v for v in c) for c in N)
def valid(source,n):
    if 3*len(source)!=4*n or len(set(tuple(sorted(c)) for c in source))!=len(source):return False
    counts=[[0,0] for _ in range(n)]
    for c in source:
        if len(c)!=3 or any(type(v)!=int or not v or abs(v)>n for v in c):return False
        if len(set(abs(v) for v in c))!=3 or len(set(v>0 for v in c))!=1:return False
        for v in c:counts[abs(v)-1][int(v>0)]+=1
    return all(c==[2,2] for c in counts)
def sat(bits,source=F):
    return all(any(bool(bits & (1<<(abs(v)-1)))==(v>0) for v in c) for c in source)
def rank(rows):
    piv={}
    for r in rows:
        while r:
            i=r.bit_length()-1
            if i in piv:r ^= piv[i]
            else:piv[i]=r;break
    return len(piv)
def cut(mask):
    A=[i for i in range(9) if (mask>>i)&1]
    B=[i for i in range(9) if not (mask>>i)&1]
    rows=[]
    for a in range(1<<len(A)):
        fixed=sum(((a>>j)&1)<<i for j,i in enumerate(A)); row=0
        for b in range(1<<len(B)):
            other=sum(((b>>j)&1)<<i for j,i in enumerate(B))
            if sat(fixed|other):row |= 1<<b
        rows.append(row)
    return rank(rows)
def pin_count(pin):
    return sum(sat(x) and all(((x>>(v-1))&1)==b for v,b in pin.items()) for x in range(512))
if __name__=="__main__":
    assert valid(F,9)
    assert sum(sat(x) for x in range(512))==70 and sat(75)
    ranks=[cut(s) for s in range(512)]
    assert ranks[0]==ranks[511]==1 and all(r>1 for r in ranks[1:511])
    assert ranks[15]==14
    assert sha256(bytes(ranks)).hexdigest()=="f5ba80b421caf81d366dd66c949c13530c9a4588c74a0d14b75a382ebed4ef1d"
    p0={1:0,2:0,3:0,6:1};p1={1:1,2:0,3:0,6:1}
    assert pin_count(p0)==1 and pin_count(p1)==0
    for k in range(10):print(k,sorted(Counter(ranks[s] for s in range(512) if s.bit_count()==k).items()))
    print("F9 exact model count 70; all 510 proper-cut ranks>=2; same-source SAT1/UNSAT0")
    print("This is a restricted full-function OBDD rank diagnostic, NOT SAT decision hardness.")
