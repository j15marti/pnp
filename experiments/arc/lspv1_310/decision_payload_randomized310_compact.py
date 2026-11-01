#!/usr/bin/env python3
"""LSPV-1 310: all-source SAT grammar and bounded-error payload-query floor.
Standard-library reproducible finite controls. OFFLINE, not native FLMV.
"""
import json
from collections import Counter
from itertools import combinations,product
from fractions import Fraction
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def grammar(n,cs):
    if n<=0 or n%3 or len(cs)*3!=4*n:return False
    cnt=Counter();seen=set()
    for c in cs:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        cnt.update((abs(x),x>0) for x in c)
    return all(cnt[i,s]==2 for i in range(1,n+1) for s in (False,True))
def gamma(v):
    z=format(v,'b');return '0'*(len(z)-1)+z
def encode(n,cs):
    w=n.bit_length();h=gamma(n)+gamma(len(cs))
    return h+''.join(str(int(c[0]>0))+''.join(format(abs(x),f'0{w}b') for x in c) for c in cs),len(h)
def decode(t):
    off=0;head=[]
    try:
        for _ in range(2):
            z=0
            while off<len(t) and t[off]=='0':off+=1;z+=1
            if off+z>=len(t):return None
            head.append(int(t[off:off+z+1],2));off+=z+1
        n,m=head;w=n.bit_length();size=1+3*w
        if n<=0 or len(t)!=off+m*size:return None
        cs=[]
        for i in range(m):
            k=off+i*size;s=1 if t[k]=='1' else -1
            cs.append(tuple(s*int(t[k+1+j*w:k+1+(j+1)*w],2) for j in range(3)))
        return (n,tuple(cs)) if grammar(n,cs) else None
    except (ValueError,IndexError):return None
def tcount(c,a):
    return sum(bool((a>>(abs(l)-1))&1)==(l>0) for l in c)
def sat_models(n,cs,p=None):
    p={} if p is None else p
    return sum(all(((a>>(i-1))&1)==v for i,v in p.items()) and all(tcount(c,a)>=1 for c in cs) for a in range(1<<n))
def run():
    rows=[]
    for label,n,cs in [('Y6',6,Y),('F9',9,F)]:
        assert grammar(n,cs)
        bits,head=encode(n,cs);assert decode(bits)==(n,cs)
        M=len(bits)-head
        for i in range(head,len(bits)):
            mutant=bits[:i]+str(1-int(bits[i]))+bits[i+1:]
            assert decode(mutant) is None
        pairs=0;comp=0
        for a in range(1<<n):
            for c in cs:
                assert tcount(c,a)+tcount(c,((1<<n)-1)^a)==3
                comp+=1
        for c,d in combinations(cs,2):
            for s,t in product((0,1),repeat=2):
                demands={};possible=True
                for C,alltrue in ((c,s),(d,t)):
                    for lit in C:
                        wanted=(lit>0)==bool(alltrue)
                        if abs(lit) in demands and demands[abs(lit)]!=wanted:possible=False
                        demands[abs(lit)]=wanted
                brute=any(all(((a>>(abs(lit)-1))&1)==int((lit>0)==bool(alltrue))
                        for C,alltrue in ((c,s),(d,t)) for lit in C) for a in range(1<<n))
                assert possible==brute
                pairs+=1
        models=sat_models(n,cs);assert models=={6:20,9:70}[n]
        rows.append(dict(source=label,encoded_bits=len(bits),header_bits=head,payload_bits=M,
                         invalid_one_bit_mutants=M,models=models,complement_checks=comp,
                         pair_modes=pairs,randomized_epsilon='1/3',expected_read_floor=str(Fraction(M,3))))
    yes={1:1,2:0,3:1,4:0,8:0};no={1:1,2:1,3:0,4:0,8:0}
    assert sat_models(9,F,yes)==1 and sat_models(9,F,no)==0
    return dict(run='LSPV1_RANDOMIZED_PAYLOAD_GRAMMAR310',status='PASS',
                controls=rows,same_original_F9={'SAT_completions':1,'UNSAT_completions':0},
                notes='OFFLINE finite checks, not native FLMV, general randomized coupling proven separately')
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
