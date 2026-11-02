#!/usr/bin/env python3
"""LSPV-2 336 independent original-source oracle-free FINITE checker.
Does NOT import the 336 producer. O(2^n) exhaustive control, not a
polynomial SAT algorithm or a general hardness claim.
"""
from itertools import product
from collections import Counter
def valid(F,n):
    if type(n)!=int or n<3 or n%3 or len(F)*3!=n*4:return False
    sig=Counter();seen=set()
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        if any(type(x)!=int or abs(x)<1 or abs(x)>n for x in C):return False
        if not (all(x>0 for x in C) or all(x<0 for x in C)):return False
        q=tuple(sorted(C))
        if q in seen:return False
        seen.add(q);sig.update(C)
    return all(sig[x]==sig[-x]==2 for x in range(1,n+1))
def models(F,n,pins=None):
    pins=pins or {};count=0;covers=[]
    for bits in product((0,1),repeat=n):
        if any(bits[x-1]!=b for x,b in pins.items()):continue
        false=next((j for j,C in enumerate(F)
            if not any(bits[abs(x)-1]==int(x>0) for x in C)),None)
        if false is None:count+=1
        else:covers.append(false)
    return count,covers
def source_prism(k):
    p=[(base+(i-1)%k+1,base+i+1,2*k+i+1)
       for base in (0,k) for i in range(k)]
    return [list(c) for c in p]+[[-x for x in c] for c in p]
def one_swap(k):
    F=source_prism(k)
    for i in range(2*k):
        for j in range(i+1,2*k):
            if set(F[i])&set(F[j]):continue
            for a in range(3):
                for b in range(3):
                    G=[C[:] for C in F]
                    G[i][a],G[j][b]=G[j][b],G[i][a]
                    if valid(G,3*k):
                        p={frozenset(c) for c in G if c[0]>0}
                        m={frozenset(-x for x in c) for c in G if c[0]<0}
                        if len(p-m)==2:return G
    raise AssertionError("no valid swap")
def main():
    F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
        (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
    for k,expected in ((3,84),(4,466),(5,1896)):
        F=one_swap(k);assert models(F,3*k)[0]==expected
    assert models(F9,9)[0]==70
    F=one_swap(3)
    satpin={4:0,5:0,6:0,7:1,8:1,9:1}
    unsatpin={**satpin,7:0}
    assert models(F,9,satpin)[0]==4
    count,cover=models(F,9,unsatpin)
    assert count==0 and sorted(cover)==[0,0,0,0,3,3,3,3]
    assert not valid([[1,2,3],[1,2,3]],6)
    print("PASS: independent original clauses, both labels, malformed; P vs NP OPEN")
if __name__=="__main__":main()
