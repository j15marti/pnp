#!/usr/bin/env python3
"""Public standalone spot check, not the complete independent archive verifier.
Validates pointwise DP and source-only proof stitching on SAT and UNSAT parents.
"""
import itertools

def canonical(clause):
    s=set(clause)
    if any(-x in s for x in s): return None
    return tuple(sorted(s,key=lambda v:(abs(v),v<0)))

def dp_step(clauses, pivot):
    pos=[c for c in clauses if pivot in c]
    neg=[c for c in clauses if -pivot in c]
    keep=[c for c in clauses if pivot not in c and -pivot not in c]
    for a in pos:
        for b in neg:
            res=canonical([x for x in a if x!=pivot]+[x for x in b if x!=-pivot])
            if res is not None: keep.append(res)
    return list(dict.fromkeys(keep))

def satisfied(formula,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in c) for c in formula)

def pointwise_project(source,B):
    original=[canonical(c) for c in source]
    others=sorted({abs(l) for c in original for l in c}-set(B))
    result=list(original)
    for x in others:result=dp_step(result,x)
    checks=0
    for bv in itertools.product((False,True),repeat=len(B)):
        boundary=dict(zip(B,bv))
        exists=any(satisfied(original,{**boundary,**dict(zip(others,ov))})
                   for ov in itertools.product((False,True),repeat=len(others)))
        child=satisfied(result,boundary)
        assert exists==child,(source,B,bv,exists,child)
        checks+=1
    return result,checks

def resolution_splice(source):
    """Resolution proof for forced x and forced not-x with source indexed leaves."""
    a,b,c,d=map(canonical,source)
    assert 1 in a and 1 in b and -1 in c and -1 in d
    y=next(abs(l) for l in a if abs(l)!=1)
    z=next(abs(l) for l in c if abs(l)!=1)
    assert y in a and -y in b and z in c and -z in d
    pos=canonical([l for l in a if l!=y]+[l for l in b if l!=-y])
    neg=canonical([l for l in c if l!=z]+[l for l in d if l!=-z])
    assert pos==(1,) and neg==(-1,)
    end=canonical([l for l in pos if l!=1]+[l for l in neg if l!=-1])
    assert end==()
    return 3

def main():
    yes=[[1,2],[1,-2],[1,3],[1,-3]]
    no=[[1,2],[1,-2],[-1,3],[-1,-3]]
    checks=0
    for formula,expected in ((yes,True),(no,False)):
        projected,n=pointwise_project(formula,(1,));checks+=n
        assert any(satisfied(projected,{1:v}) for v in (False,True))==expected
    checks+=resolution_splice(no)
    assert len(dp_step([canonical(c) for c in no],2))<=len(no)
    print('PASS: 7 pointwise/proof checks, source SAT+UNSAT, no free occurrence bits')
if __name__=='__main__': main()
