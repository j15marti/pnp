#!/usr/bin/env python3
"""LSPV2 286 compact independent reproduction of the canonical SAT tail-peel.
Full event-sourced producer, independent verifier, original U198/V198 source
proofs and raw physical event streams are in the conversation ZIP.
Only standard Python library needed; no external SAT oracle.
"""
from itertools import product
from collections import Counter

Y6_POS=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Y6=Y6_POS+((-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def gamma(n):
    assert n>=1
    b=bin(n)[2:]
    return "0"*(len(b)-1)+b

def encode(n, clauses):
    w=n.bit_length()
    return gamma(n)+gamma(len(clauses))+"".join(
        ("0" if c[0]>0 else "1")+
        "".join(format(abs(x),f"0{w}b") for x in c)
        for c in clauses)

def valid(n, clauses):
    if not isinstance(n,int) or n<1 or len(clauses)!=4*n//3 or n%3:
        return False
    seen=set();counts=Counter()
    for c in clauses:
        if len(c)!=3 or len({abs(x) for x in c})!=3:
            return False
        if not all((x>0)==(c[0]>0) and 1<=abs(x)<=n for x in c):
            return False
        canon=(c[0]>0,tuple(sorted(abs(x) for x in c)))
        if canon in seen:return False
        seen.add(canon)
        for x in c:counts[(abs(x),x>0)]+=1
    return all(counts[(i,b)]==2 for i in range(1,n+1) for b in (False,True))

def sat_model(n, clauses):
    for a in product((False,True),repeat=n):
        if all(any(a[abs(x)-1]==(x>0) for x in c) for c in clauses):
            return a
    return None

def shift_clauses(clauses, d):
    return tuple(tuple((abs(x)+d)*(1 if x>0 else -1) for x in c)
                 for c in clauses)

def counter_flip_sum(M):
    return sum((i^(i+1)).bit_count() for i in range(M))

def main():
    child=Y6
    parent=child+shift_clauses(Y6,6)
    assert valid(6,child) and valid(12,parent)
    child_bytes=encode(6,child)
    parent_bytes=encode(12,parent)
    assert (len(parent_bytes),len(child_bytes))==(224,92)
    assert sat_model(6,child) is not None
    assert sat_model(12,parent) is not None
    assert counter_flip_sum(len(child_bytes)) == (
        2*len(child_bytes)-len(child_bytes).bit_count())
    # A sequential emitter can output child bytes after reading parent
    # in source order. The correct child header has new dimensions/width.
    assert encode(6,parent[:8])==child_bytes
    # Degree quota, mixed-sign clause, repeated variable are malformed.
    assert not valid(6,child[:-1])
    assert not valid(6,(tuple(-x for x in child[0]),)+child[1:])
    assert not valid(6,((1,1,2),)+child[1:])
    print({"verdict":"PASS","N":224,"M":92,
           "models_Y6":sum(1 for a in product((0,1),repeat=6)
                           if all(any(a[abs(x)-1]==(x>0) for x in c)
                                  for c in child)),
           "counter_bit_flips":counter_flip_sum(92),
           "power_short":92*92<=224,
           "scope":"restricted certified component peel only"})

if __name__=="__main__":
    main()
