#!/usr/bin/env python3
"""SUPPORT_LOCALITY63: stdlib-only independent minimal reproducibility check."""
from itertools import product

def forcing(lit, p, q):
    return [(lit, a*p, b*q) for a,b in product((1,-1),repeat=2)]

def target(satisfiable):
    C=forcing(-1,4,5)+forcing(-2,6,7)+forcing(-3,8,9)
    C.append((-1 if satisfiable else 1,2,3))
    assert len(C)==13 and all(len(set(map(abs,c)))==3 for c in C)
    return tuple(C)

def encode(C):
    W=5
    words=[9,13]
    for c in C:
        for l in c:
            words.append((16 if l<0 else 0)|abs(l))
    assert len(words)==41
    return ''.join(format(w,'05b') for w in words)

def count_models(C):
    return sum(all(any(bool(x & (1<<(abs(l)-1)))==(l>0) for l in c) for c in C)
               for x in range(1<<9))

def role4(b,d):
    return any(sum(1 for j in range(d) if b[i*d+j]==0)==1 for i in range(d))

def role4_independent(b,d):
    return any(all((b[i*d+k]==0)==(k==j) for k in range(d))
               for i in range(d) for j in range(d))

def main():
    sat=encode(target(True)); unsat=encode(target(False))
    assert len(sat)==len(unsat)==205
    assert [i for i,(a,b) in enumerate(zip(sat,unsat)) if a!=b]==[190]
    assert count_models(target(True))==64
    assert count_models(target(False))==0
    tested=0
    for q in (1,2,4,8,12):
        for b in product((0,1),repeat=q):
            out=unsat if all(b) else sat
            assert (out==unsat)==all(b)
            tested+=1
        for i in range(q):
            x=[1]*q
            assert all(x)
            x[i]=0
            assert not all(x)
    for d in (2,3):
        for b in product((0,1),repeat=d*d):
            f=role4(b,d)
            assert f==role4_independent(b,d)
            out=sat if f else unsat
            assert (out==sat)==f
            tested+=1
    assert tested==4902
    print('SUPPORT_LOCALITY63 PASS:',tested,'source inputs; 205 target bits; one informative bit; 64/0 models')

if __name__=='__main__':
    main()
