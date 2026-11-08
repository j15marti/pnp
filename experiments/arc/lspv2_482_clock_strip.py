#!/usr/bin/env python3
"""LSPV-2/482 finite restricted padding-stripping controls, not a general SAT solver."""
from fractions import Fraction as Q
from itertools import product
import json
EDGES=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
def tseitin(ch):
    out=[]
    for v in range(4):
        ids=[i+1 for i,(a,b) in enumerate(EDGES) if a==v or b==v]
        for bits in product((0,1),repeat=3):
            if sum(bits)%2!=ch[v]:
                out.append(tuple(i if bit==0 else -i for i,bit in zip(ids,bits)))
    return out
def source(ch):
    return "p cnf 6 16\n"+''.join(' '.join(map(str,c))+' 0\n' for c in tseitin(ch))
def parse(txt):
    try:
        l=[s.strip() for s in txt.splitlines() if s.strip()]
        if len(l)!=17 or l[0]!='p cnf 6 16':return None
        cs=[]
        for s in l[1:]:
            a=s.split()
            if len(a)!=4 or a[3]!='0':return None
            c=tuple(map(int,a[:3]))
            if len({abs(z) for z in c})!=3 or not all(1<=abs(z)<=6 for z in c):return None
            cs.append(c)
        return cs
    except (ValueError,OverflowError):return None
def decide(txt):
    cs=parse(txt)
    if cs is None:return "MALFORMED"
    for bits in product((False,True),repeat=6):
        if all(any(bits[abs(z)-1] if z>0 else not bits[-z-1] for z in c) for c in cs):return "SAT"
    return "UNSAT"
def wrapper(txt,k,h):
    n=len(txt)
    a=bytearray(n**h)
    for i in range(len(a)):a[i]=i&255
    del a
    c=0
    for i in range(n**k):c+=1
    assert c==n**k
    return decide(txt)
def strip(ast):
    while isinstance(ast,tuple) and len(ast)==4 and ast[0]=='PAD' and type(ast[1])==int and type(ast[2])==int and min(ast[1:3])>=0:
        ast=ast[3]
    return ast
def f(t):return max(Q(11,10),Q(3,5)+t/2)
def g(s):return max(Q(1,2),s/2)
def tested(t,s,k,h):
    T=max(t,Q(k),Q(h));S=max(s,Q(h))
    return (t<=f(T) and s<=g(S)), (T>=2*t-Q(6,5) and S>=2*s)
checks=0
sat=unsat=0
for ch in product((0,1),repeat=4):
    src=source(ch);v=decide(src)
    assert v==('UNSAT' if sum(ch)%2 else 'SAT');checks+=1
    assert wrapper(src,1,1)==v;checks+=1
    assert strip(('PAD',5,4,('PAD',4,3,'CORE')))=='CORE';checks+=1
    sat+=v=='SAT';unsat+=v=='UNSAT'
src=source((0,0,0,0))
bad=[src.replace('p cnf 6 16','p cnf 6 15'),src.replace(' 0\n',' 1\n',1),src.replace('1 2 3','1 1 3',1),'nonsense','']
for b in bad:
    assert decide(b)=='MALFORMED';checks+=1
    assert wrapper(b,1,1)=='MALFORMED';checks+=1
for ti in range(5,21):
    for si in range(5,21):
        t=Q(ti,4);s=Q(si,4)
        for k in range(10):
            for h in range(10):
                assert tested(t,s,k,h)[0]==tested(t,s,k,h)[1]
                checks+=1
cases={(5,4):True,(4,3):False,(5,3):False,(4,4):False}
for (k,h),v in cases.items():assert tested(Q(3),Q(2),k,h)[0]==v
assert (sat,unsat)==(8,8) and checks==25658
print(json.dumps({"status":"COMPUTATIONAL; restricted theorem separate","checks":checks,"sat":sat,"unsat":unsat,"malformed":len(bad),"native_flmv":False,"unrestricted_sat":False},indent=2))
