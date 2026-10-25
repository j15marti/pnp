#!/usr/bin/env python3
"""Portable independent-block two-level ARC selector concurrency audit.
Logical output bits and literal buffer footprints; not physical TM steps.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt
import json

def block(i,unsat):
    v=(3*i+1,3*i+2,3*i+3)
    return tuple(tuple(x if not bit else -x for x,bit in zip(v,row))
                 for row in product((0,1),repeat=3)
                 if unsat or row!=(1,1,1))

def sat(cs):
    vs=sorted({abs(x) for c in cs for x in c})
    for row in product((False,True),repeat=len(vs)):
        a=dict(zip(vs,row))
        if all(any(a[abs(x)]==(x>0) for x in c) for c in cs):return True
    return False

def qh(n):
    q=1
    while q**5<n**3:q+=1
    h=isqrt(n)
    if h*h<n:h+=1
    return q,h

def cover(ids):
    n=len(ids);q,h=qh(n)
    out=[tuple(ids[(j*h+i)%n] for i in range(h)) for j in range(q)]
    assert set(ids)==set().union(*(set(x) for x in out))
    return out

def clauses(ids,bad):
    return tuple(c for i in ids for c in block(i,i in bad))

def size(cs,p):
    w=(3*p).bit_length()
    return 64+2*w+3*len(cs)*(w+1)

def audit(p,bad):
    ids=tuple(range(p));first=cover(ids);second=[cover(z) for z in first]
    vals1=[all(sat(block(i,i in bad)) for i in x) for x in first]
    vals2=[[all(sat(block(i,i in bad)) for i in y) for y in x] for x in second]
    actual=all(sat(block(i,i in bad)) for i in ids)
    assert actual==all(vals1)==all(all(x) for x in vals2)
    assert all(v==all(w) for v,w in zip(vals1,vals2))
    c0=clauses(ids,bad)
    b1=[size(clauses(x,bad),p) for x in first]
    b2=[size(clauses(y,bad),p) for x in second for y in x]
    return dict(p=p,bad=sorted(bad),SAT=actual,parent_bits=size(c0,p),
        first_children=len(b1),second_children=len(b2),
        first_all_live_bits=sum(b1),second_all_live_bits=sum(b2),
        serial_two_buffer_upper=max(b1)+max(b2))

def main():
    d=((Q(241,200)+2)/Q(241,200)**2-Q(241,200))/2
    assert d==Q(11642479,23232400)
    alpha=Q(3,5);lam=Q(1,2);s=Q(1,2)
    levels=[]
    for j in (1,2):
        count=alpha*sum((lam**i for i in range(j)),Q(0))
        levels.append(dict(level=j,live_independent_work_exponent=str(count+lam**j*s),
                           live_materialized_input_exponent=str(count+lam**j)))
    assert levels[0]['live_independent_work_exponent']=='17/20'
    assert levels[1]['live_independent_work_exponent']=='41/40'
    rows=[audit(p,bad) for p in (2,3,4,8,16,64,256,512)
          for bad in (set(),{0},{p-1},{0,p-1})]
    assert len(rows)==32
    r=next(x for x in rows if x['p']==256 and not x['bad'])
    assert (r['parent_bits'],r['first_children'],r['second_children'],
            r['first_all_live_bits'],r['second_all_live_bits'],r['serial_two_buffer_upper'])==(
                59220,28,168,105840,169344,4788)
    return {'source':'ARC-SELECTOR-CONCURRENCY110','tests':len(rows),
            'failures':0,'scope':'restricted ordinary-CNF independent blocks',
            'FLMV_beta':str(d),'levels':levels,'p256_SAT':r,
            'p256_UNSAT':next(x for x in rows if x['p']==256 and x['bad']==[255]),
            'ARC_EDGE_90':'OPEN','P_vs_NP':'OPEN'}

if __name__=='__main__':
    result=main()
    print(json.dumps(result,sort_keys=True,indent=2))
