#!/usr/bin/env python3
"""LSPV-1 326 compact source-primal projection test. Python stdlib only.
This program is finite verification, not a universal SAT complexity lower bound."""
import itertools,json,random
from collections import Counter
from fractions import Fraction
P9='156 238 135 469 247 789'; N9='468 167 234 358 129 579'
P6='123 145 246 356'
P30='1,2,26;1,3,23;2,6,13;3,10,15;4,18,29;4,25,27;5,12,14;5,16,20;6,19,21;7,11,13;7,23,30;8,9,28;8,17,24;9,27,28;10,22,30;11,18,21;12,17,20;14,16,24;15,26,29;19,22,25'
N30='21,25,30;17,20,28;14,19,22;12,16,29;11,13,21;11,12,18;9,17,20;8,24,25;8,13,18;7,27,29;7,26,27;5,10,19;5,6,24;4,15,26;3,6,23;3,4,14;2,22,23;2,16,28;1,10,30;1,9,15'
def triples(text,s):return [tuple(s*int(z) for z in (v.split(',') if ',' in v else v)) for v in text.replace(';',' ').split()]
def canon(rows):return tuple(sorted({tuple(sorted(set(c))) for c in rows if not any(-v in c for v in c)}))
def mk(p,n):return canon(triples(p,1)+triples(n,-1))
def join(a,b):
    k=max(abs(v) for c in a for v in c)
    return canon(list(a)+[tuple((1 if v>0 else -1)*(k+abs(v)) for v in c) for c in b])
def valid(rows):
    if not rows:return False
    n=max(abs(v) for c in rows for v in c)
    q=Counter((abs(v),v>0) for c in rows for v in c)
    return len(rows)==len(set(rows)) and all(len(c)==3 and len(set(map(abs,c)))==3 and (all(v>0 for v in c) or all(v<0 for v in c)) for c in rows) and all(q[(i,s)]==2 for i in range(1,n+1) for s in (0,1))
def neighbors(rows,free):
    g={i:set() for i in free}
    for c in rows:
        for a,b in itertools.combinations({abs(v) for v in c},2):g[a].add(b);g[b].add(a)
    return g
def eliminate(rows,pivot):
    A=[set(c)-{pivot} for c in rows if pivot in c]
    B=[set(c)-{-pivot} for c in rows if -pivot in c]
    left=[c for c in rows if pivot not in c and -pivot not in c]
    return canon(left+[tuple(a|b) for a in A for b in B if all(-v not in a|b for v in a|b)])
def three_rounds(rows):
    n=max(abs(v) for c in rows for v in c);free=set(range(1,n+1));result=[]
    for phase in range(3):
        g=neighbors(rows,free);active=set(free);pivots=[]
        while active:
            x=min(active);pivots.append(x);active-={x}|g[x]
        for x in pivots:rows=eliminate(rows,x)
        free-=set(pivots);d=max([len(s) for s in neighbors(rows,free).values()]+[0])
        oc=Counter((abs(v),v>0) for c in rows for v in c)
        p=max([oc[(v,s)] for v in free for s in (0,1)]+[0]);w=max([len(c) for c in rows]+[0])
        if phase==0:assert d<=20 and p<=4 and w<=4
        if phase==1:assert d<=108 and p<=16 and w<=6
        result.append({'I':pivots,'free':len(free),'degree':d,'per_sign':p,'width':w,'clauses':len(rows)})
    assert len(free)*763<=640*n+763
    return result
def sat_models(rows,pins):
    n=max(abs(v) for c in rows for v in c)
    free=[v for v in range(1,n+1) if v not in pins];models=0;bad=[]
    for bs in itertools.product([False,True],repeat=len(free)):
        a=pins|dict(zip(free,bs))
        falsified=[j for j,c in enumerate(rows) if not any(a[abs(v)]==(v>0) for v in c)]
        models+=not falsified
        if falsified:bad.append(falsified[0])
    return models,bad
def swap(rows,rng):
    for _ in range(120):
        a=[list(c) for c in rows];i,j=rng.sample(range(len(rows)),2)
        if a[i][0]*a[j][0]<0:continue
        u,v=rng.randrange(3),rng.randrange(3);a[i][u],a[j][v]=a[j][v],a[i][u]
        b=canon(a)
        if valid(b):return b
    return rows
def main():
    f9=mk(P9,N9);y6=mk(P6,P6)
    examples={'F9':f9,'Y6':y6,'H15':join(f9,y6),'F18':join(f9,f9),'SHARP30':mk(P30,N30)}
    rng=random.Random(20261102)
    for i in range(12):
        s=examples['H15'] if i%2 else examples['F18']
        for _ in range(1+i%5):s=swap(s,rng)
        examples['SWAP_%02d'%i]=s
    output={}
    for name,rows in examples.items():
        assert valid(rows)
        output[name]={'n':max(abs(v) for c in rows for v in c),'m':len(rows),'rounds':three_rounds(rows)}
    pins={1:False,3:False,5:True,6:False,7:False,8:False}
    s,_=sat_models(f9,pins);u,leaf=sat_models(f9,pins|{1:True})
    assert (s,u)==(2,0) and len(leaf)==8
    assert Fraction(8,9)*Fraction(20,21)*Fraction(108,109)==Fraction(640,763)
    return {'status':'PASS','seed':20261102,'valid_originals':len(examples),'exponent':'640/763','old_exponent':'25600/30429','F9_SAT_UNSAT':[s,u],'F9_UNSAT_original_clause_leaves':leaf,'instances':output}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))