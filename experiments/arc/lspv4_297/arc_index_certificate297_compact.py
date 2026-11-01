#!/usr/bin/env python3
"""Deterministic compact reproducer for ARC-INDEXED-CERTIFICATE-AUDIT297.
Restricted original-source SAT/UNSAT and indexed-tape controls, not a SAT lower bound.
The longer independent verifier and raw traces are in the run's reproducibility ZIP.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json, math

POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=POS+tuple(tuple(-x for x in c) for c in NEG)
P={8:0,3:0,7:0,6:0,1:1,5:1}
CY=(3,4,10)
def grammar(F,n):
    q=Counter((abs(x),x>0) for c in F for x in c)
    return (len(F)==4*n//3 and len(set(map(lambda c:tuple(sorted(c)),F)))==len(F)
            and all(len(c)==3 and len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
            and all(q[x,s]==2 for x in range(1,n+1) for s in (False,True)))
def sat(F,a):
    return all(any(a[abs(v)]==int(v>0) for v in c) for c in F)
def affine_rows(chosen):
    free={2:0,4:1,9:2}; rows=[]
    for j in (1,5):
        r=[v for v in F[j] if abs(v) in free]
        rows.append((sum(1<<free[abs(v)] for v in r),
                     (1 if F[j][0]>0 else 1^(len(r)&1)),f'C{j}'))
    rows.append((1<<free[4],1,'pref_x4'))
    for j in CY:
        r=[v for v in F[j] if abs(v) in free]
        if j==chosen:
            for v in r:rows.append((1<<free[abs(v)],int(v>0),f'C{j}_endpoint_x{abs(v)}'))
        else:rows.append((sum(1<<free[abs(v)] for v in r),1,f'C{j}_xor'))
    return rows
def contradiction(rows):
    # Acquire an explicit minimal xor refutation, then verify it independently.
    for k in range(1,len(rows)+1):
        from itertools import combinations
        for ids in combinations(range(len(rows)),k):
            mask=rhs=0
            for i in ids:mask^=rows[i][0];rhs^=rows[i][1]
            if (mask,rhs)==(0,1):
                assert all(sum(((rows[i][0]>>v)&1) for i in ids)%2==0 for v in range(3))
                assert sum(rows[i][1] for i in ids)%2==1
                return [rows[i][2] for i in ids]
    raise AssertionError('missing GF2 refutation')
def flmv(c):
    f=Fraction(1);ds=[]
    for k in range(1,10):
        f=c*f/(1+f)
        ds.append(min((1/f-c)/k,1/c**k))
    assert ds[1]>max(ds[0],ds[2]) and c**(-4)<ds[1]
    return [ds[1].numerator,ds[1].denominator]
def main():
    assert grammar(F,9)
    root=sum(sat(F,dict(enumerate(bits,1))) for bits in product((0,1),repeat=9))
    assert root==70
    for rest in product((0,1),repeat=3):
        a={**P,**dict(zip((2,4,9),rest))}
        assert not sat(F,a)
    uncovered=[i for i,c in enumerate(F) if not any(abs(v) in P and P[abs(v)]==int(v>0) for v in c)]
    assert uncovered==[1,3,4,5,10]
    cert={j:contradiction(affine_rows(j)) for j in CY}
    assert all(1<=len(c)<=3 for c in cert.values())
    products=[]
    for t in range(1,7):
        G=tuple(tuple((1 if v>0 else -1)*(abs(v)+9*k) for v in clause)
                for k in range(t) for clause in F)
        assert grammar(G,9*t)
        B=(9*t+1-1).bit_length();H=(12*t+1-1).bit_length()
        products.append({'copies':t,'bits':2*H+36*t*(B+1),'cycles':t,
                         'explicit_branches':3**t,'global_models':70**t,'pinned_models':0})
    traces=[{'index_width':w,'native_steps':w+2,'cumulative_tape_xor':2*w,'endpoint_xor':0}
            for w in (1,2,4,8,16)]
    assert traces[-1]['native_steps']<traces[-1]['cumulative_tape_xor']
    d1=flmv(Fraction(6,5));d2=flmv(Fraction(241,200))
    assert d1==[23,45] and d2==[11642479,23232400]
    print(json.dumps({'root_SAT_models':root,'cube_SAT_models':0,
        'certificate_rows':cert,'products':products,'index_traces':traces,
        'flmv_d_star':{'6/5':d1,'241/200':d2},
        'transport_strict_b':[11642479,11616200],
        'qualified_scope':'explicit proof format and given-proof verifier only',
        'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
