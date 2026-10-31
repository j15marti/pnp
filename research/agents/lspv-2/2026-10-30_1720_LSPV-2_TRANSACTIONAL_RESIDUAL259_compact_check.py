#!/usr/bin/env python3
"""Independent standalone exhaustive check of TRANSACTIONAL-RESIDUAL259 lemma.
Python standard library only. No prior archive or external solver is required.
"""
import itertools,json,random

def canon(seq):
    s=set(seq)
    return None if any(-x in s for x in s) else tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def sat(F,a):
    return all(any((a[abs(l)] if l>0 else not a[abs(l)]) for l in c) for c in F)

def modes(F,pivot):
    plus=[c for c in F if pivot in c]
    minus=[c for c in F if -pivot in c]
    independent=[c for c in F if abs(pivot) not in set(map(abs,c))]
    resolutions=[]
    for pos in plus:
        for neg in minus:
            r=canon([l for l in pos if l!=pivot]+[l for l in neg if l!=-pivot])
            if r is not None:resolutions.append((pos,neg,r))
    return independent,plus,minus,resolutions

def check(F,pivot):
    ind,plus,minus,triples=modes(F,pivot)
    res=[r for _,_,r in triples]
    xs=sorted(set(abs(l) for c in F for l in c)-{pivot})
    count=0
    for vals in itertools.product([False,True],repeat=len(xs)):
        a=dict(zip(xs,vals))
        exists=any(sat(F,{**a,pivot:b}) for b in [False,True])
        assert exists==sat(ind+res,a)
        count+=1
        for cutoff in range(len(res)+1):
            for b in [False,True]:
                ass={**a,pivot:b}
                assert sat(F,ass)==sat(F+res[:cutoff],ass)
                count+=1
    return count

def main():
    clauses=[]
    for n in range(1,4):
        for vs in itertools.combinations([1,2,3],n):
            for signs in itertools.product([-1,1],repeat=n):
                clauses.append(tuple(sign*v for sign,v in zip(signs,vs)))
    rng=random.Random(259); checks=0
    examples=[[(1,2),(-1,3),(-2,),(-3,)]]
    for _ in range(256):
        examples.append(rng.sample(clauses,rng.randrange(1,13)))
    for F in examples:
        for x in (1,2,3):checks+=check(F,x)
    bad=[(-2,),(-3,)]
    assert not any(sat(examples[0],dict(zip((1,2,3),vals))) for vals in itertools.product([False,True],repeat=3))
    assert any(sat(bad,dict(zip((2,3),vals))) for vals in itertools.product([False,True],repeat=2))
    print(json.dumps({'runs':len(examples)*3,'pointwise_checks':checks,'early_deletion_false_SAT':True,'status':'PASS'}))
if __name__=='__main__':main()
