#!/usr/bin/env python3
"""Exact rational finite controls for MAGRED-SEEDMASS15; Python 3 standard library."""
import json, math
from itertools import combinations
from fractions import Fraction
from pathlib import Path


def binary_sharp(N):
    M,R=1<<N,1<<(N-1)
    counts={}
    for x,y in combinations(range(M),2):
        a,v=x>>(N-1),x&(R-1)
        b,w=y>>(N-1),y&(R-1)
        k=sum((a^((s&v).bit_count()&1))==(b^((s&w).bit_count()&1)) for s in range(R))
        counts[k]=counts.get(k,0)+1
        assert Fraction(k,R)<=Fraction(1,2)
    return {"N":N,"b":1,"r":N-1,"seeds":R,"total_pairs":M*(M-1)//2,
            "colliding_pairs":counts.get(R//2,0),"never_colliding_pairs":counts.get(0,0),
            "max_collision":"1/2"}


def gf4_mul(a,b):
    ans=0
    while b:
        if b&1: ans^=a
        b>>=1; a<<=1
        if a&4: a^=7
    return ans


def gf4_sharp():
    hist={}
    for x,y in combinations(range(16),2):
        a,v=x>>2,x&3
        b,w=y>>2,y&3
        k=sum((a^gf4_mul(s,v))==(b^gf4_mul(s,w)) for s in range(4))
        hist[k]=hist.get(k,0)+1
        assert k<=1
    assert hist=={1:96,0:24}
    return {"N":4,"b":2,"r":2,"seeds":4,
            "one_seed_collisions":hist[1],"zero_seed_collisions":hist[0],
            "max_collision":"1/4"}


def weighted():
    N=3;R=4;M=8
    ps=([Fraction(3,16)]*4)+([Fraction(1,1024)]*256)
    assert sum(ps)==1 and max(ps)==Fraction(3,16)
    for x,y in combinations(range(M),2):
        a,v=x>>2,x&3
        b,w=y>>2,y&3
        k=sum((a^((s&v).bit_count()&1))==(b^((s&w).bit_count()&1)) for s in range(R))
        c=Fraction(3,4)*Fraction(k,R)+Fraction(1,4)*Fraction(1,2)
        assert c<=Fraction(1,2)
    H=-sum(float(p)*math.log2(float(p)) for p in ps)
    return {"N":N,"b":1,"seed_outcomes":260,"max_seed_atom":"3/16",
            "max_pair_collision":"1/2","shannon_entropy":round(H,8)}


def almost():
    N=4;M=1<<N
    worst=Fraction(0)
    for x,y in combinations(range(M),2):
        k=sum(((x>>i)&1)==((y>>i)&1) for i in range(4))
        worst=max(worst,Fraction(k,4))
    assert worst==Fraction(3,4)
    return {"N":N,"b":1,"r":2,"worst_collision":"3/4","is_exact_2universal":False}


def main():
    sharp=[binary_sharp(N) for N in range(2,7)]
    codes=["","0","1","00"]
    nonprefix={"N":3,"b":1,"seed_codes":codes,
               "mean_total_length":sum(len(x)+1 for x in codes)/4,
               "worst_total_length":max(len(x)+1 for x in codes)}
    assert nonprefix["mean_total_length"]==2 and nonprefix["worst_total_length"]==3
    out={"report":"MAGRED-SEEDMASS15","classification":"COMPUTATIONAL exact rational controls",
         "sharp_binary":sharp,"sharp_gf4":gf4_sharp(),"weighted":weighted(),
         "nonprefix":nonprefix,"almost_universal":almost()}
    p=Path(__file__).resolve().with_name("2026-10-18_MAGRED_SEEDMASS15_raw.json")
    p.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
