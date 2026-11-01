#!/usr/bin/env python3
"""ARC292 restricted canonical source-survivor theorem checker.
Run at repository root: python experiments/arc/lspv4_292/arc_survivor_frontier292_compact.py
This program checks a combinatorial resource invariant. It is not a SAT solver,
a SAT/UNSAT certificate producer, or a native FLMV Turing-machine simulator.
"""
import ast
import itertools
import collections
import json
from fractions import Fraction
from pathlib import Path

Y = [[1,2,3],[1,4,5],[2,4,6],[3,5,6],
     [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]

def valid(f):
    if not f: return False
    n=max(abs(z) for c in f for z in c)
    if n%3 or len(f)*3!=4*n: return False
    counter=collections.Counter(z for c in f for z in c)
    if len(set(tuple(sorted(c)) for c in f))!=len(f):return False
    return (all(len(c)==3 and len(set(map(abs,c)))==3
                and (all(z>0 for z in c) or all(z<0 for z in c))
                and all(isinstance(z,int) and 1<=abs(z)<=n for z in c)
                for c in f)
            and all(counter[x]==counter[-x]==2 for x in range(1,n+1)))

def codec(n):
    def gamma(k):return 2*k.bit_length()-1
    return gamma(n)+gamma(4*n//3)+(4*n//3)*(1+3*n.bit_length())

def evaluate(f,p):
    n=max(abs(z) for c in f for z in c)
    keep=[];plus=minus=0
    for C in f:
        if any(abs(z) in p and p[abs(z)]==int(z>0) for z in C):
            if C[0]>0:plus+=1
            else:minus+=1
        else:keep.append([z for z in C if abs(z) not in p])
    support={abs(z) for c in keep for z in c}
    free=set(range(1,n+1))-p.keys()
    lost=free-support
    k0=sum(v==0 for v in p.values())
    k1=len(p)-k0
    assert plus<=2*k1 and minus<=2*k0
    assert len(lost)<=2*min(k0,k1)
    assert len(support)>=n-len(p)-2*min(k0,k1)
    if k0*k1==0:assert not lost
    if len(p)==1:
        assert len(support)==n-1
        child_min=3*((len(support)+2)//3)
        assert child_min==n and codec(child_min)>=codec(n)
    return len(lost)

def source198():
    path=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
    if not path.exists():raise FileNotFoundError(path)
    t=path.read_text()
    U=[list(c) for c in ast.literal_eval(t[t.index('[['):])]
    V=[c.copy() for c in U]
    V[1][0],V[7][0]=V[7][0],V[1][0]
    return U,V

def envelope(c):
    f=Fraction(1);best=Fraction(-1);winner=-1
    for k in range(1,100):
        f=c*f/(1+f)
        d=min((1/f-c)/k,c**(-k))
        if d>best:best=d;winner=k
        if c**(-(k+1))<best:return winner,best,k
    raise RuntimeError("uncertified infinite tail")

def main():
    U,V=source198()
    results={}
    for name,F in [('Y6',Y),('U198',U),('V198',V)]:
        assert valid(F)
        n=max(abs(z) for c in F for z in c)
        root=0
        for x in range(1,n+1):
            for bit in (0,1):
                evaluate(F,{x:bit});root+=1
        if n==6:
            cubes=0
            for state in itertools.product((None,0,1),repeat=n):
                evaluate(F,{i+1:state[i] for i in range(n) if state[i] is not None})
                cubes+=1
        else:cubes=0
        results[name]={'n':n,'m':len(F),'encoded_bits':codec(n),
                       'both_polarity_pivots_verified':root,'small_exhaustive_cubes':cubes}
    for c,expect in [(Fraction(6,5),Fraction(23,45)),
                     (Fraction(241,200),Fraction(11642479,23232400))]:
        k,best,last=envelope(c)
        assert k==2 and best==expect and last>=3
    assert sum(all(any((bits[abs(v)-1]==1)==(v>0) for v in cl) for cl in Y)
               for bits in itertools.product((0,1),repeat=6))==20
    print(json.dumps({'status':'PASS','scope':'restricted source-injective repair',
                      'FLMV_native_simulation':False,'cases':results},indent=2))

if __name__=="__main__":main()
