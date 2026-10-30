"""Independent stdlib checker: ARC-MULTIINDEX-GATE254, deterministic."""
from itertools import permutations, product, combinations
from math import factorial
import json

def formula(pi, sat):
    m=len(pi); z=2*m+1; v=(z+1,z+2,z+3)
    clauses=[(pi[j],m+j+1,z) for j in range(m)]
    if sat: clauses.extend((v,tuple(-x for x in v)))
    else: clauses.extend(tuple(s[i]*v[i] for i in range(3)) for s in product((-1,1),repeat=3))
    return clauses,2*m+4

def clause_count(c,a):
    return sum(a[abs(l)-1]==int(l>0) for l in c)

def compat(c,d,p,q):
    demands={}
    for cl,st in ((c,p),(d,q)):
        for l in cl:
            value=int(l>0) if st=='S' else int(l<0)
            if abs(l) in demands and demands[abs(l)]!=value:return False
            demands[abs(l)]=value
    return True

def brute(c,d,p,q):
    ids=sorted({abs(l) for l in c+d})
    for b in product((0,1),repeat=len(ids)):
        a=dict(zip(ids,b))
        if all(sum(a[abs(l)]==int(l>0) for l in cl)==(len(cl) if st=='S' else 0)
               for cl,st in ((c,p),(d,q))):return True
    return False

def check():
    tests=0; counts=[]; labels=[]
    for m in range(2,8):
        for r in range(1,m+1):
            patterns={tuple(pi.index(i) for i in range(1,r+1)) for pi in permutations(range(1,m+1))}
            assert len(patterns)==factorial(m)//factorial(m-r);tests+=1
        counts.append((m, (factorial(m)-1).bit_length()))
    for m in (3,4):
        ps=list(permutations(range(1,m+1)))
        for pi in (ps[0],ps[len(ps)//2],ps[-1]):
            for is_sat in (True,False):
                f,n=formula(pi,is_sat)
                for i in range(1,m+1):
                    a=[0]*n; old=[clause_count(c,a) for c in f];a[i-1]=1
                    changed=[j for j,c in enumerate(f) if clause_count(c,a)!=old[j]]
                    assert changed==[pi.index(i)];tests+=1
                for c,d in combinations(f,2):
                    for p,q in product(('S','U'),repeat=2):
                        assert compat(c,d,p,q)==brute(c,d,p,q);tests+=1
                for c in f:
                    assert all(int(l>0)==1-int(l<0) for l in c);tests+=1
                models=0
                for a in product((0,1),repeat=n):
                    t=[clause_count(c,a) for c in f]
                    comp=[clause_count(c,tuple(1-x for x in a)) for c in f]
                    assert all(x+y==3 for x,y in zip(t,comp))
                    models+=int(min(t)>0);tests+=1
                assert (models>0)==is_sat
                labels.append({'m':m,'sat':is_sat,'models':models})
    return {'status':'PASS','checks':tests,'cache_bits':counts,'labels':labels,
            'scope':'zero source probes after preprocessing; clause-index updates, not SAT hardness'}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True))
