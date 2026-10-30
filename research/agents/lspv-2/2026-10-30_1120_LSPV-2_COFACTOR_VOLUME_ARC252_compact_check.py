#!/usr/bin/env python3
"""Compact independent reproducer: sign-blind raw cofactor volume.
Full provenance DAG and adaptive controller are in the companion ZIP.
"""
from itertools import combinations, product
from collections import Counter

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

def parse(s):
    return tuple(tuple(map(int,block.split())) for block in s.split(';'))

def truth(l,a):
    return bool(a & (1 << (abs(l)-1))) == (l>0)

def count_models(F):
    n=max(abs(l) for C in F for l in C)
    return sum(all(any(truth(l,a) for l in C) for C in F) for a in range(1<<n))

def volume(F,B):
    b=len(B);B=set(B)
    return (sum(1<<(b-sum(abs(l) in B for l in C)) for C in F),
            sum((len(C)-sum(abs(l) in B for l in C)) *
                (1<<(b-sum(abs(l) in B for l in C))) for C in F))

def materialized(F,B):
    clause_count=literal_count=0
    for assignment in product((0,1),repeat=len(B)):
        a=dict(zip(B,assignment))
        for C in F:
            if any(abs(l) in a and a[abs(l)] == (l>0) for l in C):
                continue
            remain=[l for l in C if abs(l) not in a]
            clause_count+=1;literal_count+=len(remain)
    return clause_count,literal_count

def main():
    W,S=map(parse,(W1,S15))
    assert [tuple(map(abs,C)) for C in W]==[tuple(map(abs,C)) for C in S]
    assert count_models(W)==0 and count_models(S)==861
    for F in (W,S):
        assert len(F)==20
        assert all(len(C)==3 and len({abs(l) for l in C})==3 for C in F)
        ct=Counter(l for C in F for l in C)
        assert all(ct[x]==ct[-x]==2 for x in range(1,16))
        for b in range(4):
            for B in combinations(range(1,16),b):
                assert volume(F,B)==materialized(F,B)
                assert sum(all(abs(l) not in B for l in C) for C in F)>=20-4*b
    print({'W1_models':0,'S15_models':861,
           'subsets_B_b_at_most_3':sum(__import__('math').comb(15,b) for b in range(4)),
           'W1_S15_prefix5':volume(W,tuple(range(1,6)))})

if __name__=='__main__':main()
