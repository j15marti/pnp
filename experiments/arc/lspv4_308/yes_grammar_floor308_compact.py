#!/usr/bin/env python3
"""LSPV-4 308 compact, independent standard-library reproducibility checker.
Full no-import producer/verifier and raw are in conversation ZIP.
No native FLMV whole-program benchmark is claimed.
"""
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P+tuple(tuple(-x for x in row) for row in M)
def family(t):
    out=[]
    for b in range(t):
        for j,row in enumerate(F9):
            out.append(tuple((1 if lit>0 else -1)*(9*((b+1)%t if (j==0 and abs(lit)==5) else b)+abs(lit)) for lit in row))
    return tuple(out)
def good(rows,n):
    if 3*len(rows)!=4*n:return False
    counts=Counter();seen=set()
    for row in rows:
        if len(row)!=3 or len({abs(z) for z in row})!=3:return False
        if any(abs(z)<1 or abs(z)>n for z in row):return False
        if len({z>0 for z in row})!=1:return False
        k=tuple(sorted(row))
        if k in seen:return False
        seen.add(k)
        for z in row:counts[abs(z),z>0]+=1
    return all(counts[v,True]==counts[v,False]==2 for v in range(1,n+1))
def gamma(n):
    b=bin(n)[2:];return '0'*(len(b)-1)+b
def encode(rows,n):
    w=n.bit_length()
    s=gamma(n)+gamma(len(rows));positions=[]
    for row in rows:
        positions.append(len(s))
        s+=('1' if row[0]>0 else '0')
        s+=''.join(format(abs(z),'0%db'%w) for z in row)
    return s,positions
def decode(s):
    def num(i):
        j=i
        while j<len(s) and s[j]=='0':j+=1
        if j==len(s):raise ValueError('gamma')
        z=j-i+1
        if j+z>len(s):raise ValueError('gamma width')
        return int(s[j:j+z],2),j+z
    try:
        n,i=num(0);m,i=num(i)
        if n<=0 or m<=0 or 3*m!=4*n:return None
        w=n.bit_length()
        if len(s)!=i+m*(1+3*w):return None
        out=[]
        for _ in range(m):
            sign=1 if s[i]=='1' else -1;i+=1
            row=[]
            for _ in range(3):
                row.append(sign*int(s[i:i+w],2));i+=w
            out.append(tuple(row))
        return tuple(out) if good(out,n) else None
    except (ValueError,IndexError):return None
def sat(rows,vals):
    return all(any(vals[abs(z)]==(1 if z>0 else 0) for z in row) for row in rows)
def models(rows,pins):
    free=[v for v in range(1,10) if v not in pins];out=0
    for bits in product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits))
        out+=sat(rows,a)
    return out
assert good(F9,9) and models(F9,{})==70
assert models(F9,{1:1,2:0,3:1,4:0,8:0})==1
assert models(F9,{1:1,2:1,3:0,4:0,8:0})==0
root_witness=next(dict(zip(range(1,10),bits)) for bits in product((0,1),repeat=9)
                  if bits[4]==0 and sat(F9,dict(zip(range(1,10),bits))))
table=[]
for t in (1,2,4,8,16,128):
    rows=family(t);n=9*t
    assert good(rows,n)
    a={9*b+j:root_witness[j] for b in range(t) for j in range(1,10)}
    assert sat(rows,a)
    s,positions=encode(rows,n)
    assert decode(s)==rows
    for p in positions:
        mutation=s[:p]+('0' if s[p]=='1' else '1')+s[p+1:]
        assert decode(mutation) is None
    table.append([t,len(s),len(positions)])
for c,expected in ((F(6,5),F(23,45)),(F(241,200),F(11642479,23232400))):
    fk=F(1);d={}
    for k in range(1,11):
        fk=c*fk/(1+fk)
        d[k]=min((1/fk-c)/k,c**(-k))
    assert d[2]==expected and d[1]<d[2] and d[3]<d[2] and c**(-4)<d[2]
print(json.dumps({'status':'PASS','same_original_F9_P_Q':[1,0],
                  'G_t_N_and_critical_polarity_bits':table,
                  'critical_mutation_rejections':sum(r[2] for r in table),
                  'FLMV_k2_unique_and_tail_verified':True,'P_vs_NP':'OPEN'},indent=2))
