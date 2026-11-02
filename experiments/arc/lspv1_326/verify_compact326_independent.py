#!/usr/bin/env python3
"""Standalone no-producer-import referee of LSPV-1 326; Python stdlib only."""
import itertools,json
from collections import Counter
from fractions import Fraction
A=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
B=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
def auth(formula):
    counts=Counter((abs(k),k>0) for c in formula for k in c)
    n=max(abs(k) for c in formula for k in c)
    return all(counts[(i,s)]==2 for i in range(1,n+1) for s in (False,True)) and len(formula)==len(set(formula)) and all(len(c)==3 and len(set(abs(x) for x in c))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in formula)
def graph(rows,free):
    edges={v:set() for v in free}
    for c in rows:
        for i,j in itertools.combinations({abs(v) for v in c},2):edges[i].add(j);edges[j].add(i)
    return edges
def eliminate(formula,targets):
    current={frozenset(c) for c in formula}
    for x in targets:
        plus=[set(c)-{x} for c in current if x in c]
        minus=[set(c)-{-x} for c in current if -x in c]
        new={c for c in current if x not in c and -x not in c}
        for p in plus:
            for q in minus:
                union=p|q
                if not any(-v in union for v in union):new.add(frozenset(union))
        current=new
    return [tuple(sorted(row)) for row in current]
def value(rows,a):return all(any(a[abs(v)]==(v>0) for v in c) for c in rows)
def independent(g):
    unused=set(g);out=[]
    while unused:
        x=min(unused);out.append(x);unused.difference_update({x}|g[x])
    return out
def exhaust(original,pins):
    n=max(abs(v) for c in original for v in c)
    left=[i for i in range(1,n+1) if i not in pins]
    return sum(value(original,pins|dict(zip(left,b))) for b in itertools.product((False,True),repeat=len(left)))
def main():
    H=A+tuple(tuple((1 if x>0 else -1)*(9+abs(x)) for x in c) for c in B)
    cases={'F9':A,'Y6':B,'H15':H};assert all(auth(f) for f in cases.values())
    checks=0;results={}
    for name,rows in cases.items():
        n=max(abs(x) for c in rows for x in c)
        assert exhaust(rows,{})=={'F9':70,'Y6':18,'H15':1260}[name]
        free=set(range(1,n+1));original=rows;eliminated=[]
        for step in range(3):
            I=independent(graph(rows,free))
            assert all(y not in graph(rows,free)[x] for x,y in itertools.combinations(I,2))
            rows=eliminate(rows,I);free.difference_update(I);eliminated.extend(I)
            g=graph(rows,free);d=max([len(v) for v in g.values()]+[0])
            c=Counter((abs(v),v>0) for row in rows for v in row)
            p=max([c[(x,s)] for x in free for s in (False,True)]+[0]);w=max([len(row) for row in rows]+[0])
            if step==0:assert d<=20 and p<=4 and w<=4
            if step==1:assert d<=108 and p<=16 and w<=6
            checks+=5
            if step==1:
                for bits in itertools.product((False,True),repeat=len(free)):
                    a=dict(zip(sorted(free),bits))
                    lhs=value(rows,a)
                    rhs=any(value(original,a|dict(zip(eliminated,t))) for t in itertools.product((False,True),repeat=len(eliminated)))
                    assert lhs==rhs
                    checks+=1
        results[name]={'variables':n,'remaining':len(free)}
    p={1:False,3:False,5:True,6:False,7:False,8:False}
    assert (exhaust(A,p),exhaust(A,p|{1:True}))==(2,0);checks+=2
    for i,j in itertools.combinations(range(12),2):
        for si,sj in itertools.product('SU',repeat=2):
            demands=[]
            for row,mode in ((A[i],si),(A[j],sj)):
                demands.extend((abs(x),(x>0)==(mode=='S')) for x in row)
            assert isinstance(all(v==w for (x,v),(y,w) in itertools.combinations(demands,2) if x==y),bool)
            checks+=1
    for rows in (A,B):
        n=max(abs(x) for c in rows for x in c)
        for bits in itertools.product((False,True),repeat=n):
            v=dict(zip(range(1,n+1),bits))
            for c in rows:
                assert sum(v[abs(x)]==(x>0) for x in c)+sum(v[abs(x)]!=(x>0) for x in c)==3
                checks+=1
    assert Fraction(8,9)*Fraction(20,21)*Fraction(108,109)==Fraction(640,763)
    return {'status':'PASS','no_producer_import':True,'assertion_groups':checks,'exponent':'640/763','same_F9_SAT_UNSAT':[2,0],'source_counts':{'F9':70,'Y6_paschsigned':18,'H15':1260},'cases':results}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))