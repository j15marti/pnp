"""LSPV-4 MU16 minimal UNSAT Horn-lift controls; Python 3 standard library only."""
from itertools import combinations
import json

U=[
(3,7,15),(2,-3,7),(1,-2,-3),(-1,-2,-3),
(6,-7,15),(5,-6,-7),(4,-5,-6),(-4,-5,-6),
(10,14,-15),(9,-10,14),(8,-9,-10),(-8,-9,-10),
(13,-14,-15),(12,-13,-14),(11,-12,-13),(-11,-12,-13)]

def ok(clause,assignment):
    return any(bool(assignment.get(abs(lit),False)) == (lit>0) for lit in clause)

def model_count(clauses,n):
    total=0; witness=None
    for mask in range(1<<n):
        a={i:bool(mask & (1<<(i-1))) for i in range(1,n+1)}
        if all(ok(clause,a) for clause in clauses):
            total+=1; witness=a
    return total,witness

def lifted(U):
    H=[]; groups=[]
    for j,c in enumerate(U):
        s=[16+3*j+a for a in range(3)]
        groups.append(s)
        H.append(tuple(s))
        H.extend([(-s[a],c[a]) for a in range(3)])
    return H,groups

def horn_witness(original,groups,deleted_clause,source_witness):
    a=dict(source_witness)
    for j,c in enumerate(original):
        which=None
        if deleted_clause//4 == j:
            if deleted_clause%4 == 0:
                continue
            which=deleted_clause%4-1
        else:
            which=next(i for i,l in enumerate(c) if ok((l,),a))
        if which is not None:a[groups[j][which]]=True
    return a

def padded(H):
    P=[];padding=[]
    n=63
    for i,c in enumerate(H):
        if len(c)==3:
            P.append(c)
        else:
            n+=1
            padding.append((i,n,len(P)))
            P.append(c+(n,))
            P.append(c+(-n,))
    return P,padding,n

def test():
    checks=0
    assert max(sum(abs(x)==v for c in U for x in c) for v in range(1,16))==4;checks+=1
    assert model_count(U,15)[0]==0;checks+=1
    witness=[]
    for j in range(len(U)):
        count,alpha=model_count(U[:j]+U[j+1:],15)
        assert count>0;checks+=1
        witness.append(alpha)
        for a in range(3):
            V=list(U);l=list(V[j]);l[a]=-l[a];V[j]=tuple(l)
            assert all(ok(c,alpha) for c in V);checks+=1
    hit=[{abs(x) for x in c} for c in U]
    assert all(bool(c&{3,6,10,13}) for c in hit);checks+=1
    assert not any(all(bool(set(s)&c) for c in hit)
                   for r in range(4) for s in combinations(range(1,16),r));checks+=1
    H,groups=lifted(U)
    assert len(H)==64 and sum(len(c)==2 for c in H)==48;checks+=1
    H_witness=[]
    for idx in range(len(H)):
        alpha=horn_witness(U,groups,idx,witness[idx//4])
        assert all(ok(c,alpha) for j,c in enumerate(H) if j!=idx);checks+=1
        H_witness.append(alpha)
    P,padding,n=padded(H)
    assert len(P)==112 and n==111 and all(len(c)==3 for c in P);checks+=1
    pad_map={h:(y,start) for h,y,start in padding}
    for i,c in enumerate(H):
        if len(c)==3:
            a=dict(H_witness[i])
            assert all(ok(x,a) for j,x in enumerate(P) if j!=i+sum(len(t)==2 for t in H[:i]));checks+=1
        else:
            y,start=pad_map[i]
            a=H_witness[i]
            assert not ok(c,a)
            for removed, surviving_y in ((start,False),(start+1,True)):
                b=dict(a);b[y]=surviving_y
                assert all(ok(t,b) for j,t in enumerate(P) if j!=removed);checks+=1
    result={"core_variables":15,"core_clauses":16,"horn_variables":63,
            "horn_clauses":64,"proper_variables":111,"proper_clauses":112,
            "checks":checks,"failures":0}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":test()
