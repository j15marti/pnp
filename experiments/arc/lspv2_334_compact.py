#!/usr/bin/env python3
"""LSPV-2 334: connected canonical paired-NAE prism, bad/good OBDD orders.
Stdlib only. python lspv2_334_compact.py. NOT a SAT decision lower bound.
"""
from collections import Counter
from functools import lru_cache
import json

def prism(k):
    assert k>=4 and k%2==0
    clauses=[]
    for base in (0,k):
        for i in range(k):
            clauses.append((base+(i-1)%k+1,base+i+1,2*k+i+1))
    return tuple(clauses+[tuple(-x for x in c) for c in clauses])

def valid(k,cs):
    ct=Counter(x for c in cs for x in c)
    return (len(cs)==4*k and len(set(tuple(sorted(c)) for c in cs))==len(cs)
        and all(len(c)==3 and len(set(map(abs,c)))==3 and
            (all(x>0 for x in c) or all(x<0 for x in c)) for c in cs)
        and all(ct[i]==ct[-i]==2 for i in range(1,3*k+1)))

def satisfy(cs,a):
    return all(any(a[abs(x)-1]==(x>0) for x in c) for c in cs)

def signature(t,b):
    k=len(t);mask=value=0
    for i in range(k):
        x=None if t[i]!=t[i-1] else 1-t[i]
        y=None if b[i]!=b[i-1] else 1-b[i]
        if x is not None and y is not None and x!=y:return None
        z=x if x is not None else y
        if z is not None:
            mask|=1<<i
            value|=z<<i
    return mask,value

def reduced_bdd(k,order):
    unique={};sizes=Counter();states=Counter()
    @lru_cache(None)
    def build(level,cnf):
        states['reached']+=1
        if not cnf:return 1
        if cnf==((),):return 0
        assert level<len(order)
        v=order[level]
        def descend(bit):
            rows=[]
            for clause in cnf:
                if (v if bit else -v) in clause:continue
                rest=tuple(x for x in clause if x!=(-v if bit else v))
                if not rest:return ((),)
                rows.append(rest)
            return tuple(rows)
        low=build(level+1,descend(False))
        high=build(level+1,descend(True))
        if low==high:return low
        key=(level,low,high)
        if key not in unique:
            unique[key]=len(unique)+2
            sizes[level]+=1
        return unique[key]
    root=build(0,prism(k))
    return dict(nodes=len(unique),width=max(sizes.values()),
        first_spoke_width=sizes[2*k] if order[2*k]==2*k+2 else None,
        acquired_residual_states=states['reached'],root=root)

def run(k):
    cs=prism(k);assert valid(k,cs)
    distinct=set()
    for q in range(1<<(k//2)):
        t=[(q>>(i//2))&1 for i in range(k)]
        b=[i&1 for i in range(k)]
        s=signature(t,b);assert s is not None
        mask,value=s
        assert all((mask>>(2*j+1))&1 and
                   ((value>>(2*j+1))&1)==1-((q>>j)&1)
                   for j in range(k//2))
        a=[(value>>i)&1 if (mask>>i)&1 else 0 for i in range(k)]
        assert satisfy(cs,t+b+a)
        distinct.add(s)
    assert len(distinct)==1<<(k//2)
    bad=list(range(1,2*k+1))+[2*k+2,2*k+1]+list(range(2*k+3,3*k+1))
    good=[v for i in range(k) for v in (i+1,k+i+1,2*k+i+1)]
    out=dict(k=k,n=3*k,m=4*k,proved_bad_width_lower_bound=len(distinct),
        restricted_forward_gates=8*k-1,
        bad=reduced_bdd(k,bad) if k<=8 else None,good=reduced_bdd(k,good))
    assert out['good']['width']<=146
    if out['bad']:assert out['bad']['first_spoke_width']>=len(distinct)
    return out

if __name__=='__main__':
    print(json.dumps([run(k) for k in (4,6,8,10,12)],indent=2))
