#!/usr/bin/env python3
"""Small independent PAIRPATH73 reproduction, no third-party packages."""
import collections,itertools,json
F=[(1,2,4),(1,2,-4),(-2,3,5),(-2,3,-5),(-1,-3,6),(-1,-3,-6),(4,5,6),(-4,-5,-6)]
def truth(clauses,a):
    return all(any(a[abs(x)]==(x>0) for x in c) for c in clauses)
def canon(c):return tuple(sorted(c,key=lambda x:abs(x)))
def paired(F):
    indices={canon(c):i for i,c in enumerate(F)}
    matches=[];used=set()
    for i,c in enumerate(F):
        if i in used:continue
        partners=[]
        for x in c:
            twin=canon(tuple(-z if z==x else z for z in c))
            if twin in indices:partners.append(indices[twin])
        assert len(partners)<=1
        if partners:
            j=partners[0];assert j not in used
            matches.append((i,j));used.update((i,j))
    unmatched=[c for i,c in enumerate(F) if i not in used]
    B=[tuple(sorted(set(F[i])&set(F[j]),key=abs)) for i,j in matches]
    return B,unmatched

def test():
    counts=collections.Counter(x for c in F for x in c)
    assert len(F)==8 and all(counts[x]==counts[-x]==2 for x in range(1,7))
    assert all(len({abs(x) for x in c})==3 for c in F)
    B,T=paired(F)
    assert len(B)==3 and len(T)==2
    assert set(B)=={(1,2),(-2,3),(-1,-3)}
    checks=0
    for bits in itertools.product((False,True),repeat=6):
        a=dict(zip(range(1,7),bits))
        assert truth(F,a)==truth(B+T,a)
        checks+=1
    for tail in itertools.product((False,True),repeat=3):
        fixed=dict(zip((4,5,6),tail))
        exists=any(truth(F,{**fixed,1:a,2:b,3:c})
                   for a,b,c in itertools.product((False,True),repeat=3))
        residual=truth(T,fixed)
        assert exists==residual
        checks+=1
    assert any(truth(F,dict(zip(range(1,7),a)))
               for a in itertools.product((False,True),repeat=6))
    controls=[[(1,2),(-1,2),(1,-2),(-1,-2)],[(1,2),(-1,2),(1,-2)]]
    assert not any(truth(controls[0],dict(zip((1,2),a)))
                   for a in itertools.product((False,True),repeat=2))
    assert any(truth(controls[1],dict(zip((1,2),a)))
               for a in itertools.product((False,True),repeat=2))
    return dict(run_id='PAIRPATH73_MINIREPRO',source_clauses=len(F),paired=len(B),defect=len(T),projected_binaries=0,projection_checks=checks,failures=0)
if __name__=='__main__':print(json.dumps(test(),sort_keys=True))
